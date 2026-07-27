#!/usr/bin/env python3
"""kf-lint CLI discovery, invocation, and diagnostic formatting."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def resolve_kf_lint() -> str | None:
    override = os.environ.get("KF_LINT_BIN")
    if override:
        path = Path(override)
        if path.is_file() and os.access(path, os.X_OK):
            return str(path.resolve())
        found = shutil.which(override)
        if found:
            return found
        return None

    found = shutil.which("kf-lint")
    if found:
        return found

    candidates: list[Path] = []
    pnpm_home = os.environ.get("PNPM_HOME")
    if pnpm_home:
        candidates.append(Path(pnpm_home))
    candidates.extend(
        [
            Path.home() / "Library/pnpm",
            Path.home() / ".local/share/pnpm",
            Path.home() / ".pnpm",
        ]
    )
    for base in candidates:
        direct = base / "kf-lint"
        if direct.is_file() and os.access(direct, os.X_OK):
            return str(direct.resolve())
        for match in base.glob("**/kf-lint"):
            if match.is_file() and os.access(match, os.X_OK):
                return str(match.resolve())
    return None


def run_kf_lint_verify(repo_root: Path, paths: list[str], kf_lint: str) -> tuple[list[dict[str, Any]], int] | None:
    if not paths:
        return ([], 0)
    proc = subprocess.run(
        [kf_lint, "verify", "--format", "json", *paths],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode not in (0, 1):
        return None
    stdout = proc.stdout.strip()
    if not stdout:
        return ([], proc.returncode)
    try:
        diagnostics = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    if not isinstance(diagnostics, list):
        return None
    return (diagnostics, proc.returncode)


def run_kf_lint_commit_msg(repo_root: Path, message_file: Path, kf_lint: str) -> tuple[list[dict[str, Any]], int] | None:
    proc = subprocess.run(
        [kf_lint, "commit-msg", str(message_file)],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode not in (0, 1):
        return None
    if proc.returncode == 0:
        return ([], 0)
    stderr = proc.stderr.strip()
    stdout = proc.stdout.strip()
    payload = stdout or stderr
    if not payload:
        return ([], proc.returncode)
    if payload.startswith("[") or payload.startswith("{"):
        try:
            parsed = json.loads(payload)
            if isinstance(parsed, list):
                return (parsed, proc.returncode)
        except json.JSONDecodeError:
            pass
    return ([{"ruleId": "commit/japanese-prefix-format", "message": payload, "severity": "error"}], proc.returncode)


def error_diagnostics(diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in diagnostics if item.get("severity") == "error"]


def format_diagnostics_block(diagnostics: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for item in diagnostics:
        rule_id = item.get("ruleId", "unknown")
        message = item.get("message", "")
        file_path = item.get("filePath", "")
        line = item.get("line")
        loc = f"{file_path}:{line}" if line else file_path
        lines.append(f"- {loc} [{rule_id}] {message}".strip())
    return "\n".join(lines)


def format_stop_followup(errors: list[dict[str, Any]]) -> str:
    body = format_diagnostics_block(errors)
    return (
        "kf-lint detected lint errors in the working tree. Fix them before finishing:\n"
        f"{body}\n\n"
        "Re-run kf-lint locally with `kf-lint verify <paths>` and apply the suggested fixes."
    )
