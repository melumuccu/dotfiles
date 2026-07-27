#!/usr/bin/env python3
"""Git repository detection and changed-path collection."""

from __future__ import annotations

import subprocess
from pathlib import Path

FIXTURES_MARKER = "packages/kf-lint/fixtures/"


def normalize_rel_path(path: str) -> str:
    return path.replace("\\", "/")


def should_exclude_path(rel_path: str) -> bool:
    normalized = normalize_rel_path(rel_path)
    return normalized.startswith(FIXTURES_MARKER) or f"/{FIXTURES_MARKER}" in f"/{normalized}/"


def parse_nul_paths(data: bytes) -> list[str]:
    if not data:
        return []
    parts = data.split(b"\0")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [part.decode("utf-8", errors="surrogateescape") for part in parts if part]


def run_git(repo_root: Path, args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        check=check,
    )


def is_git_repo(path: Path) -> bool:
    try:
        proc = run_git(path, ["rev-parse", "--git-dir"])
    except (OSError, subprocess.SubprocessError):
        return False
    return proc.returncode == 0


def filter_repo_paths(repo_root: Path, rel_paths: list[str]) -> list[str]:
    filtered: list[str] = []
    seen: set[str] = set()
    for rel in rel_paths:
        normalized = normalize_rel_path(rel)
        if should_exclude_path(normalized):
            continue
        abs_path = (repo_root / rel).resolve()
        try:
            abs_path.relative_to(repo_root.resolve())
        except ValueError:
            continue
        key = str(abs_path)
        if key in seen:
            continue
        seen.add(key)
        filtered.append(str(abs_path))
    return filtered


def collect_staged_paths(repo_root: Path) -> list[str]:
    proc = run_git(repo_root, ["diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR"])
    if proc.returncode != 0:
        return []
    return filter_repo_paths(repo_root, parse_nul_paths(proc.stdout))


def collect_working_tree_paths(repo_root: Path) -> list[str]:
    rel_paths: list[str] = []
    for args in (
        ["diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR"],
        ["diff", "--name-only", "-z", "--diff-filter=ACMR"],
        ["ls-files", "--others", "--exclude-standard", "-z"],
    ):
        proc = run_git(repo_root, args)
        if proc.returncode != 0:
            return []
        rel_paths.extend(parse_nul_paths(proc.stdout))
    return filter_repo_paths(repo_root, rel_paths)
