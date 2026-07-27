#!/usr/bin/env python3
"""Tests for lint-commit-message beforeShell hook."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from kf_lint_test_support import (
    COMMIT_MESSAGE_HOOK,
    GOOD_COMMIT,
    GOOD_CSS,
    TempGitRepo,
    make_kf_lint_wrapper,
    run_hook,
)

GOOD_COMMIT_CMD = "git commit -m 'fix__: lint_hook検証' -m '- 概要: hook\\n- Why: test'"


class CommitMessageHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TempGitRepo()
        self.wrapper_dir = Path(tempfile.mkdtemp(prefix="kf-lint-bin-"))
        self.wrapper = make_kf_lint_wrapper(self.wrapper_dir)
        self.env = {"KF_LINT_BIN": str(self.wrapper), "PATH": os.environ.get("PATH", "")}

    def tearDown(self) -> None:
        self.repo.close()

    def test_non_commit_command_allows(self) -> None:
        code, out = run_hook(COMMIT_MESSAGE_HOOK, {"command": "git status", "cwd": str(self.repo.root)}, self.env)
        self.assertEqual(code, 0)
        self.assertEqual(out, {})

    def test_bad_commit_message_denies(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -m 'bad message'", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")
        self.assertIn("commit/japanese-prefix-format", out.get("agent_message", ""))

    def test_good_message_allows(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_multiple_m_concatenates(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_file_message_allows(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        msg_file = self.repo.write("msg.txt", GOOD_COMMIT)
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": f"git commit -F {msg_file}", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})

    def test_empty_stage_still_lints_message(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -m 'bad message'", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_no_message_denies(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_editor_mode_denies(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -e", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_dynamic_message_denies(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": 'git commit -m "$(date)"', "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_stdin_file_denies(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -F -", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_parse_failure_denies(self) -> None:
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -m 'unterminated", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_missing_cli_denies(self) -> None:
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": GOOD_COMMIT_CMD, "cwd": str(self.repo.root)},
            {"KF_LINT_BIN": "/definitely/missing/kf-lint"},
        )
        self.assertEqual(out.get("permission"), "deny")

    def test_temp_message_file_cleaned_up(self) -> None:
        before = set(Path(tempfile.gettempdir()).glob("kf-lint-commit-msg-*"))
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        run_hook(
            COMMIT_MESSAGE_HOOK,
            {"command": "git commit -m 'fix__: lint_hook検証\\n\\n- 概要: hook\\n- Why: test'", "cwd": str(self.repo.root)},
            self.env,
        )
        after = set(Path(tempfile.gettempdir()).glob("kf-lint-commit-msg-*"))
        self.assertEqual(before, after)

    def test_shell_alias_denies(self) -> None:
        self.repo.set_alias("ci", "!git commit")
        self.repo.write("styles/good.css", GOOD_CSS)
        self.repo.stage("styles/good.css")
        code, out = run_hook(
            COMMIT_MESSAGE_HOOK,
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
            COMMIT_MESSAGE_HOOK,
            {"command": "git st", "cwd": str(self.repo.root)},
            self.env,
        )
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
