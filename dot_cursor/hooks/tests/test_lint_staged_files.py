#!/usr/bin/env python3
"""Tests for lint-staged-files beforeShell hook."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from kf_lint_test_support import (
    BAD_CSS,
    GOOD_CSS,
    STAGED_FILES_HOOK,
    TempGitRepo,
    make_kf_lint_wrapper,
    run_hook,
)

GOOD_COMMIT_CMD = "git commit -m 'fix__: lint_hook検証' -m '- 概要: hook\\n- Why: test'"


class StagedFilesHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TempGitRepo()
        self.wrapper_dir = Path(tempfile.mkdtemp(prefix="kf-lint-bin-"))
        self.wrapper = make_kf_lint_wrapper(self.wrapper_dir)
        self.env = {"KF_LINT_BIN": str(self.wrapper), "PATH": os.environ.get("PATH", "")}

    def tearDown(self) -> None:
        self.repo.close()

    def test_non_commit_command_allows(self) -> None:
        code, out = run_hook(STAGED_FILES_HOOK, {"command": "git status", "cwd": str(self.repo.root)}, self.env)
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_staged_invalid_css_denies(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": "git commit -m 'fix__: lint_hook検証\\n\\n- 概要: hook\\n- Why: test'", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("css/no-vw-vh", out.get("agent_message", ""))

    def test_staged_good_allows(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_git_c_env_compound(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        cmd = f"env CI=1 git -C {self.repo.root} commit -m 'bad message'"
        code, out = run_hook(STAGED_FILES_HOOK, {"command": cmd, "cwd": str(self.repo.root)}, self.env)
        self.assertEqual(out.get("permission"), "deny")

    def test_missing_cli_denies(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            {"KF_LINT_BIN": "/definitely/missing/kf-lint"},
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_alias_commit_direct_denies(self) -> None:
        self.repo.set_alias("ci", "commit")
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {
                "command": "git ci -m 'fix__: lint_hook検証' -m '- 概要: hook\\n- Why: test'",
                "cwd": str(self.repo.root),
            },
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("css/no-vw-vh", out.get("agent_message", ""))

    def test_alias_commit_chained_denies(self) -> None:
        self.repo.set_alias("c", "ci")
        self.repo.set_alias("ci", "commit")
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": "git c -m 'bad message'", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_alias_commit_with_c_and_env(self) -> None:
        self.repo.set_alias("ci", "commit")
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        cmd = f"env CI=1 git -C {self.repo.root} ci -m 'bad message'"
        code, out = run_hook(STAGED_FILES_HOOK, {"command": cmd, "cwd": str(self.repo.root)}, self.env)
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("css/no-vw-vh", out.get("agent_message", ""))

    def test_shell_alias_denies(self) -> None:
        self.repo.set_alias("ci", "!git commit")
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {
                "command": "git ci -m 'fix__: lint_hook検証' -m '- 概要: hook\\n- Why: test'",
                "cwd": str(self.repo.root),
            },
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("shell git aliases", out.get("agent_message", ""))

    def test_harmless_alias_allows(self) -> None:
        self.repo.set_alias("st", "status")
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": "git st", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_staged_rename_with_spaces_denies(self) -> None:
        rel_old = "styles/old.css"
        rel_new = "styles/new bad.css"
        self.repo.write(rel_old, BAD_CSS)
        self.repo.stage(rel_old)
        subprocess.run(["git", "commit", "-m", "add css"], cwd=self.repo.root, check=True)
        subprocess.run(["git", "mv", rel_old, rel_new], cwd=self.repo.root, check=True)
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("css/no-vw-vh", out.get("agent_message", ""))

    def test_staged_deleted_excluded(self) -> None:
        rel = "styles/remove.css"
        self.repo.write(rel, GOOD_CSS)
        self.repo.stage(rel)
        subprocess.run(["git", "commit", "-m", "add css"], cwd=self.repo.root, check=True)
        subprocess.run(["git", "rm", rel], cwd=self.repo.root, check=True)
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_empty_stage_allows(self) -> None:
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_parse_failure_denies(self) -> None:
        code, out = run_hook(
            STAGED_FILES_HOOK,
            {"command": "git commit -m 'unterminated", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")


if __name__ == "__main__":
    unittest.main()
