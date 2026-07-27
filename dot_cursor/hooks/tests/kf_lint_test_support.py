#!/usr/bin/env python3
"""Shared helpers for kf-lint hook tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = HOOKS_DIR / "modules"
if str(MODULES_DIR) not in sys.path:
    sys.path.insert(0, str(MODULES_DIR))

HOOKS_JSON = HOOKS_DIR.parent / "hooks.json"
PACKAGE_KF_LINT = Path("/Users/fujisawakoki/projects/ai/packages/kf-lint/bin/kf-lint.js")

WORKING_TREE_HOOK = HOOKS_DIR / "lint-working-tree.py"
STAGED_FILES_HOOK = HOOKS_DIR / "lint-staged-files.py"
COMMIT_MESSAGE_HOOK = HOOKS_DIR / "lint-commit-message.py"

BAD_CSS = textwrap.dedent(
    """
    .hero {
      width: 100vw;
    }

    .stack {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    """
).strip()

GOOD_CSS = textwrap.dedent(
    """
    .hero {
      width: 100%;
    }
    """
).strip()

GOOD_COMMIT = textwrap.dedent(
    """
    fix__: lint_hook検証

    - 概要: hook検証
    - Why: 本番導入前確認
    """
).strip()


def make_kf_lint_wrapper(dest: Path) -> Path:
    wrapper = dest / "kf-lint"
    wrapper.write_text(
        textwrap.dedent(
            f"""\
            #!/bin/bash
            exec node "{PACKAGE_KF_LINT}" "$@"
            """
        ),
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


class TempGitRepo:
    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(prefix="kf-lint-hook-test-")
        self.root = Path(self._tmpdir.name)
        self.env = env or {}
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True)
        (self.root / ".kf-lintrc.json").write_text(
            json.dumps({"extendsRecommended": True}),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".kf-lintrc.json"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.root, check=True)

    def write(self, rel: str, content: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def stage(self, rel: str) -> None:
        subprocess.run(["git", "add", "--", rel], cwd=self.root, check=True)

    def set_alias(self, name: str, value: str) -> None:
        subprocess.run(["git", "config", "alias." + name, value], cwd=self.root, check=True)

    def close(self) -> None:
        self._tmpdir.cleanup()


def run_hook(script: Path, payload: dict, env: dict[str, str] | None = None) -> tuple[int, dict]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    proc = subprocess.run(
        ["python3", str(script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
        env=merged,
    )
    stdout = proc.stdout.strip() or "{}"
    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid JSON from {script.name}: {stdout!r}") from exc
    return proc.returncode, parsed
