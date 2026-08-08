#!/usr/bin/env python3
"""Tests for lint-working-tree stop hook."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from kf_lint_test_support import (
    BAD_CSS,
    GOOD_CSS,
    WORKING_TREE_HOOK,
    TempGitRepo,
    make_kf_lint_wrapper,
    run_hook,
)


class WorkingTreeHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TempGitRepo()
        self.wrapper_dir = Path(tempfile.mkdtemp(prefix="kf-lint-bin-"))
        self.wrapper = make_kf_lint_wrapper(self.wrapper_dir)
        self.env = {"KF_LINT_BIN": str(self.wrapper)}

    def tearDown(self) -> None:
        self.repo.close()

    def test_unstaged_invalid_css_returns_followup(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertIn("followup_message", out)
        self.assertIn("css/no-vw-vh", out["followup_message"])

    def test_clean_returns_empty(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_staged_invalid_css_returns_followup(self) -> None:
        path = self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.stage("styles/bad.css")
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertIn("followup_message", out)
        self.assertIn(str(path), out["followup_message"])

    def test_warn_only_returns_followup(self) -> None:
        self.repo.write(
            "Dockerfile",
            "FROM node:24-slim AS base\nFROM base AS runtime\n",
        )
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertIn("followup_message", out)
        self.assertIn("到達性 warn", out["followup_message"])
        self.assertIn("user confirmation fallback", out["followup_message"])
        self.assertIn("docker/layer-heading", out["followup_message"])

    def test_error_takes_priority_over_warn_followup(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        self.repo.write(
            "Dockerfile",
            "FROM node:24-slim AS base\nFROM base AS runtime\n",
        )
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertIn("followup_message", out)
        self.assertIn("css/no-vw-vh", out["followup_message"])
        self.assertIn("Fix them before finishing", out["followup_message"])
        self.assertNotIn("到達性 warn", out["followup_message"])

    def test_fixture_path_skipped(self) -> None:
        self.repo.write("packages/kf-lint/fixtures/css/phase1-bad.css", BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_deleted_file_excluded(self) -> None:
        rel = "styles/remove.css"
        self.repo.write(rel, GOOD_CSS)
        self.repo.stage(rel)
        subprocess.run(["git", "commit", "-m", "add css"], cwd=self.repo.root, check=True)
        (self.repo.root / rel).unlink()
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_path_with_spaces(self) -> None:
        rel = "styles/my bad.css"
        self.repo.write(rel, BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertIn("followup_message", out)
        self.assertIn("css/no-vw-vh", out["followup_message"])

    def test_non_git_root_returns_empty(self) -> None:
        non_git = Path(tempfile.mkdtemp(prefix="non-git-"))
        try:
            code, out = run_hook(
                WORKING_TREE_HOOK,
                {
                    "status": "completed",
                    "loop_count": 0,
                    "workspace_roots": [str(non_git)],
                },
                self.env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(out, {})
        finally:
            non_git.rmdir()

    def test_non_completed_status_returns_empty(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {"status": "aborted", "loop_count": 0, "workspace_roots": [str(self.repo.root)]},
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_loop_limit_returns_empty(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {"status": "completed", "loop_count": 3, "workspace_roots": [str(self.repo.root)]},
            self.env,
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_missing_cli_returns_empty(self) -> None:
        self.repo.write("styles/bad.css", BAD_CSS)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            {"KF_LINT_BIN": "/definitely/missing/kf-lint"},
        )
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_multi_root_one_error_one_clean(self) -> None:
        clean_repo = TempGitRepo()
        try:
            self.repo.write("styles/bad.css", BAD_CSS)
            clean_repo.write("styles/good.css", GOOD_CSS)
            code, out = run_hook(
                WORKING_TREE_HOOK,
                {
                    "status": "completed",
                    "loop_count": 0,
                    "workspace_roots": [str(clean_repo.root), str(self.repo.root)],
                },
                self.env,
            )
            self.assertIn("followup_message", out)
            self.assertIn("css/no-vw-vh", out["followup_message"])
        finally:
            clean_repo.close()

    def test_multi_root_both_error(self) -> None:
        other = TempGitRepo()
        try:
            self.repo.write("styles/bad.css", BAD_CSS)
            other.write("styles/also bad.css", BAD_CSS)
            code, out = run_hook(
                WORKING_TREE_HOOK,
                {
                    "status": "completed",
                    "loop_count": 0,
                    "workspace_roots": [str(self.repo.root), str(other.root)],
                },
                self.env,
            )
            self.assertIn("followup_message", out)
            self.assertEqual(out["followup_message"].count("css/no-vw-vh"), 2)
        finally:
            other.close()

    def test_renamed_path_is_linted(self) -> None:
        rel_old = "styles/old.css"
        rel_new = "styles/renamed bad.css"
        self.repo.write(rel_old, BAD_CSS)
        self.repo.stage(rel_old)
        subprocess.run(["git", "commit", "-m", "add css"], cwd=self.repo.root, check=True)
        subprocess.run(["git", "mv", rel_old, rel_new], cwd=self.repo.root, check=True)
        code, out = run_hook(
            WORKING_TREE_HOOK,
            {
                "status": "completed",
                "loop_count": 0,
                "workspace_roots": [str(self.repo.root)],
            },
            self.env,
        )
        self.assertIn("followup_message", out)
        self.assertIn("css/no-vw-vh", out["followup_message"])
        self.assertIn("renamed bad.css", out["followup_message"])


if __name__ == "__main__":
    unittest.main()
