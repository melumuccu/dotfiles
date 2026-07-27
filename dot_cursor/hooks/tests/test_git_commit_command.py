#!/usr/bin/env python3
"""Unit tests for git commit command parsing."""

from __future__ import annotations

import unittest
from pathlib import Path

from kf_lint_test_support import TempGitRepo

import git_commit_command as git_commit


class CommonParserTests(unittest.TestCase):
    def test_parse_git_commit_direct(self) -> None:
        commits, error = git_commit.parse_git_commits("git commit -m 'fix__: ok'", Path("/tmp/repo"))
        self.assertIsNone(error)
        self.assertEqual(len(commits), 1)

    def test_parse_git_commit_with_c_and_env(self) -> None:
        commits, error = git_commit.parse_git_commits(
            "env CI=1 git -C /tmp/repo commit -m 'fix__: ok'",
            None,
        )
        self.assertIsNone(error)
        self.assertEqual(len(commits), 1)
        self.assertEqual(str(commits[0].repo_cwd), "/tmp/repo")

    def test_parse_compound_command(self) -> None:
        commits, error = git_commit.parse_git_commits(
            "git status && git commit -m 'fix__: ok'",
            Path("/tmp/repo"),
        )
        self.assertIsNone(error)
        self.assertEqual(len(commits), 1)

    def test_parse_multiple_messages(self) -> None:
        result = git_commit.parse_commit_message(["-m", "title", "-m", "body"])
        self.assertTrue(result.ok)
        self.assertEqual(result.message, "title\n\nbody")

    def test_parse_unsupported_dynamic_message(self) -> None:
        result = git_commit.parse_commit_message(["-m", "$(date)"])
        self.assertFalse(result.ok)

    def test_parse_unsupported_no_message(self) -> None:
        result = git_commit.parse_commit_message(["-a"])
        self.assertFalse(result.ok)


class AliasParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TempGitRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_commit_alias_resolves(self) -> None:
        self.repo.set_alias("ci", "commit")
        commits, error = git_commit.parse_git_commits(
            "git ci -m 'fix__: ok'",
            self.repo.root,
        )
        self.assertIsNone(error)
        self.assertEqual(len(commits), 1)

    def test_chained_alias_resolves(self) -> None:
        self.repo.set_alias("c", "ci")
        self.repo.set_alias("ci", "commit")
        commits, error = git_commit.parse_git_commits(
            "git c -m 'fix__: ok'",
            self.repo.root,
        )
        self.assertIsNone(error)
        self.assertEqual(len(commits), 1)

    def test_shell_alias_denies(self) -> None:
        self.repo.set_alias("ci", "!git commit")
        _commits, error = git_commit.parse_git_commits(
            "git ci -m 'fix__: ok'",
            self.repo.root,
        )
        self.assertIn("shell git aliases", error or "")


if __name__ == "__main__":
    unittest.main()
