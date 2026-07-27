#!/usr/bin/env python3
"""Shell command parsing for git commit invocations and messages."""

from __future__ import annotations

import os
import re
import shlex
import tempfile
from dataclasses import dataclass
from pathlib import Path

from git_changed_files import is_git_repo, run_git

SEGMENT_SPLIT = re.compile(r"\s*(?:;|&&|\|\||\|)\s*")
ALIAS_CHAIN_LIMIT = 5
ALIAS_UNSAFE_PATTERN = re.compile(r"[;&|`]|<<|\$\(")


@dataclass(frozen=True)
class GitCommitInvocation:
    segment: str
    repo_cwd: Path | None
    commit_argv: list[str]


@dataclass(frozen=True)
class CommitMessageResult:
    ok: bool
    message: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class AliasResolution:
    kind: str
    commit_prefix_argv: tuple[str, ...] = ()
    reason: str | None = None


def split_segments(command: str) -> list[str]:
    return [part.strip() for part in SEGMENT_SPLIT.split(command) if part.strip()]


def skip_env_assignments(tokens: list[str], index: int) -> int:
    while index < len(tokens) and "=" in tokens[index] and not tokens[index].startswith("-"):
        index += 1
    return index


def consume_git_global_option(tokens: list[str], index: int) -> tuple[int, Path | None]:
    token = tokens[index]
    if token in ("-C", "--git-dir", "--work-tree"):
        if index + 1 >= len(tokens):
            raise ValueError("missing git global option value")
        if token == "-C":
            return index + 2, Path(tokens[index + 1]).expanduser()
        return index + 2, None
    if token.startswith("-C") and len(token) > 2:
        return index + 1, Path(token[2:]).expanduser()
    if token.startswith("-") and "=" in token:
        return index + 1, None
    if token.startswith("-"):
        return index + 1, None
    return index, None


def get_git_alias(repo_root: Path, name: str) -> str | None:
    proc = run_git(repo_root, ["config", "--get", f"alias.{name}"])
    if proc.returncode != 0:
        return None
    value = proc.stdout.decode("utf-8", errors="surrogateescape").strip()
    return value or None


def alias_value_is_unsafe(alias_value: str) -> str | None:
    if alias_value.startswith("!"):
        return "shell git aliases are unsupported"
    if "$" in alias_value:
        return "complex git aliases with variable expansion are unsupported"
    if ALIAS_UNSAFE_PATTERN.search(alias_value):
        return "complex git aliases with shell operators are unsupported"
    return None


def resolve_git_alias_subcommand(repo_root: Path | None, subcommand: str, depth: int = 0) -> AliasResolution:
    if subcommand == "commit":
        return AliasResolution("commit")

    if repo_root is None or not is_git_repo(repo_root):
        return AliasResolution("other")

    alias_value = get_git_alias(repo_root, subcommand)
    if alias_value is None:
        return AliasResolution("other")

    unsafe = alias_value_is_unsafe(alias_value)
    if unsafe:
        return AliasResolution("deny", reason=unsafe)

    if depth >= ALIAS_CHAIN_LIMIT:
        return AliasResolution("deny", reason="git alias chain exceeds limit")

    try:
        alias_tokens = shlex.split(alias_value, posix=True)
    except ValueError:
        return AliasResolution("deny", reason="unable to parse git alias")

    if not alias_tokens:
        return AliasResolution("deny", reason="empty git alias")

    head = alias_tokens[0]
    tail = alias_tokens[1:]

    if head == "commit":
        return AliasResolution("commit", commit_prefix_argv=tuple(tail))

    chained = resolve_git_alias_subcommand(repo_root, head, depth + 1)
    if chained.kind == "deny":
        return chained
    if chained.kind == "commit":
        return AliasResolution("commit", commit_prefix_argv=tuple(tail) + chained.commit_prefix_argv)
    return AliasResolution("other")


def find_git_commit_in_tokens(tokens: list[str], default_cwd: Path | None) -> tuple[GitCommitInvocation | None, str | None]:
    index = 0
    repo_cwd = default_cwd
    while index < len(tokens):
        token = tokens[index]
        if token == "env":
            index = skip_env_assignments(tokens, index + 1)
            continue
        if token != "git":
            index += 1
            continue

        index += 1
        while index < len(tokens) and tokens[index].startswith("-"):
            try:
                index, maybe_cwd = consume_git_global_option(tokens, index)
            except ValueError:
                return None, "unable to parse git global options"
            if maybe_cwd is not None:
                repo_cwd = maybe_cwd
            continue

        if index < len(tokens):
            subcommand = tokens[index]
            repo_for_alias = repo_cwd if repo_cwd is not None else default_cwd
            if repo_for_alias is not None:
                repo_for_alias = repo_for_alias.expanduser().resolve()
            resolved = resolve_git_alias_subcommand(repo_for_alias, subcommand)
            if resolved.kind == "deny":
                return None, resolved.reason or "unsupported git alias"
            if resolved.kind == "commit":
                remaining = tokens[index + 1 :]
                return (
                    GitCommitInvocation(
                        segment="",
                        repo_cwd=repo_cwd,
                        commit_argv=list(resolved.commit_prefix_argv) + remaining,
                    ),
                    None,
                )
        index += 1
    return None, None


def segment_has_unsupported_shell(segment: str) -> str | None:
    if "<<" in segment:
        return "heredoc commit messages are unsupported"
    if re.search(r"\$\([^)]*\)", segment):
        return "command substitution in commit command is unsupported"
    if re.search(r"`[^`]+`", segment):
        return "command substitution in commit command is unsupported"
    if re.search(r"(?:^|\s)(?:-F|--file)\s+-", segment):
        return "stdin commit message file (-F -) is unsupported"
    if re.search(r"(?:^|\s)(?:-F|--file)=-", segment):
        return "stdin commit message file (-F -) is unsupported"
    return None


def parse_git_commits(command: str, default_cwd: Path | None) -> tuple[list[GitCommitInvocation], str | None]:
    commits: list[GitCommitInvocation] = []
    for segment in split_segments(command):
        try:
            tokens = shlex.split(segment, posix=True)
        except ValueError:
            return [], "unable to parse shell command"
        invocation, deny_reason = find_git_commit_in_tokens(tokens, default_cwd)
        if deny_reason:
            return [], deny_reason
        if invocation is None:
            continue
        unsupported = segment_has_unsupported_shell(segment)
        if unsupported:
            return [], unsupported
        commits.append(
            GitCommitInvocation(
                segment=segment,
                repo_cwd=invocation.repo_cwd,
                commit_argv=invocation.commit_argv,
            )
        )
    return commits, None


def message_has_dynamic_content(text: str) -> bool:
    return bool(re.search(r"\$\(|`|\$[A-Za-z_{]", text))


def parse_commit_message(commit_argv: list[str]) -> CommitMessageResult:
    messages: list[str] = []
    file_paths: list[str] = []
    index = 0
    while index < len(commit_argv):
        token = commit_argv[index]
        if token == "--":
            break
        if token in ("-e", "--edit", "--amend", "--fixup", "--squash"):
            if token in ("-e", "--edit"):
                return CommitMessageResult(ok=False, reason="editor commit messages are unsupported")
            if token == "--amend" and not any(
                commit_argv[i] in ("-m", "--message", "-F", "--file")
                or (commit_argv[i].startswith("-m") and len(commit_argv[i]) > 2)
                for i in range(index + 1, len(commit_argv))
            ):
                return CommitMessageResult(ok=False, reason="amend without explicit message is unsupported")
        if token in ("-m", "--message"):
            if index + 1 >= len(commit_argv):
                return CommitMessageResult(ok=False, reason="missing commit message value")
            value = commit_argv[index + 1]
            if message_has_dynamic_content(value):
                return CommitMessageResult(ok=False, reason="dynamic commit messages are unsupported")
            messages.append(value)
            index += 2
            continue
        if token.startswith("-m") and len(token) > 2:
            value = token[2:]
            if message_has_dynamic_content(value):
                return CommitMessageResult(ok=False, reason="dynamic commit messages are unsupported")
            messages.append(value)
            index += 1
            continue
        if token.startswith("--message="):
            value = token.split("=", 1)[1]
            if message_has_dynamic_content(value):
                return CommitMessageResult(ok=False, reason="dynamic commit messages are unsupported")
            messages.append(value)
            index += 1
            continue
        if token in ("-F", "--file"):
            if index + 1 >= len(commit_argv):
                return CommitMessageResult(ok=False, reason="missing commit message file")
            value = commit_argv[index + 1]
            if value == "-":
                return CommitMessageResult(ok=False, reason="stdin commit message file (-F -) is unsupported")
            if message_has_dynamic_content(value):
                return CommitMessageResult(ok=False, reason="dynamic commit message file paths are unsupported")
            file_paths.append(value)
            index += 2
            continue
        if token.startswith("--file="):
            value = token.split("=", 1)[1]
            if value == "-":
                return CommitMessageResult(ok=False, reason="stdin commit message file (-F -) is unsupported")
            if message_has_dynamic_content(value):
                return CommitMessageResult(ok=False, reason="dynamic commit message file paths are unsupported")
            file_paths.append(value)
            index += 1
            continue
        if token.startswith("-") and not token.startswith("--"):
            if len(token) > 2 and token[1] not in "mFC":
                index += 1
                continue
        index += 1

    if file_paths and messages:
        return CommitMessageResult(ok=False, reason="mixing -m and -F commit messages is unsupported")
    if len(file_paths) > 1:
        return CommitMessageResult(ok=False, reason="multiple -F commit message files are unsupported")

    if file_paths:
        file_path = Path(file_paths[0]).expanduser()
        if not file_path.is_file():
            return CommitMessageResult(ok=False, reason=f"commit message file not found: {file_paths[0]}")
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            return CommitMessageResult(ok=False, reason=f"unable to read commit message file: {exc}")
        return CommitMessageResult(ok=True, message=content)

    if not messages:
        return CommitMessageResult(ok=False, reason="commit message is required (-m/--message or -F/--file)")

    return CommitMessageResult(ok=True, message="\n\n".join(messages))


def write_temp_message(message: str) -> Path:
    fd, raw_path = tempfile.mkstemp(prefix="kf-lint-commit-msg-", suffix=".txt")
    os.close(fd)
    path = Path(raw_path)
    path.write_text(message, encoding="utf-8")
    return path


def cleanup_temp_message(path: Path | None) -> None:
    if path is None:
        return
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
