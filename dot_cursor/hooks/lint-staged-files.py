#!/usr/bin/env python3
"""beforeShellExecution hook: staged file verify only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "modules"))

import cursor_hook_io as hook_io
import git_changed_files as git_files
import git_commit_command as git_commit
import kf_lint_cli as kf_lint


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        hook_io.deny("kf-lint hook received invalid JSON input.", "Invalid hook input JSON.")

    command = payload.get("command", "")
    if not isinstance(command, str) or not command.strip():
        hook_io.allow()

    default_cwd = payload.get("cwd")
    cwd_path = Path(default_cwd).expanduser().resolve() if isinstance(default_cwd, str) and default_cwd else None

    commits, parse_error = git_commit.parse_git_commits(command.strip(), cwd_path)
    if parse_error:
        hook_io.deny(
            f"kf-lint blocked git commit: {parse_error}",
            f"Commit command blocked by kf-lint hook: {parse_error}",
        )
    if not commits:
        hook_io.allow()

    kf_lint_bin = kf_lint.resolve_kf_lint()
    if not kf_lint_bin:
        hook_io.deny(
            "kf-lint CLI is unavailable; commit blocked.",
            "Global kf-lint CLI was not found. Install @kf/lint before committing.",
        )

    for invocation in commits:
        repo_root = invocation.repo_cwd or cwd_path
        if repo_root is None:
            hook_io.deny(
                "kf-lint could not resolve git repository for commit.",
                "Unable to resolve repository root for git commit.",
            )
        repo_root = repo_root.expanduser().resolve()
        if not git_files.is_git_repo(repo_root):
            hook_io.deny(
                "kf-lint blocked commit outside a git repository.",
                f"Not a git repository: {repo_root}",
            )

        staged_paths = git_files.collect_staged_paths(repo_root)
        if staged_paths:
            verify_result = kf_lint.run_kf_lint_verify(repo_root, staged_paths, kf_lint_bin)
            if verify_result is None:
                hook_io.deny(
                    "kf-lint verify failed; commit blocked.",
                    "kf-lint verify command failed unexpectedly.",
                )
            diagnostics, _exit_code = verify_result
            errors = kf_lint.error_diagnostics(diagnostics)
            if errors:
                details = kf_lint.format_diagnostics_block(errors)
                hook_io.deny(
                    "kf-lint found staged lint errors; commit blocked.",
                    "Staged files failed kf-lint verify:\n" + details,
                )

    hook_io.allow()


if __name__ == "__main__":
    main()
