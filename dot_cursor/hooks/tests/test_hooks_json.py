#!/usr/bin/env python3
"""Tests for hooks.json kf-lint registration."""

from __future__ import annotations

import json
import unittest

from kf_lint_test_support import HOOKS_JSON


class HooksJsonTests(unittest.TestCase):
    def test_hooks_json_valid_and_preserves_security_hook(self) -> None:
        data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        commands = [entry["command"] for entry in data["hooks"]["beforeShellExecution"]]
        self.assertIn("python3 ./hooks/deny-dangerous-shell.py", commands)
        self.assertIn("python3 ./hooks/lint-staged-files.py", commands)
        self.assertIn("python3 ./hooks/lint-commit-message.py", commands)
        self.assertNotIn("python3 ./hooks/kf-lint-before-shell.py", commands)
        self.assertNotIn("python3 ./hooks/kf-lint-on-stop.py", commands)

        stop_commands = [entry["command"] for entry in data["hooks"]["stop"]]
        self.assertIn("python3 ./hooks/lint-working-tree.py", stop_commands)
        stop_entry = data["hooks"]["stop"][0]
        self.assertEqual(stop_entry.get("loop_limit"), 3)
        self.assertEqual(stop_entry.get("timeout"), 60)
        self.assertFalse(stop_entry.get("failClosed"))

        staged_entry = [entry for entry in data["hooks"]["beforeShellExecution"] if "lint-staged-files" in entry["command"]][0]
        commit_entry = [entry for entry in data["hooks"]["beforeShellExecution"] if "lint-commit-message" in entry["command"]][0]
        self.assertTrue(staged_entry.get("failClosed"))
        self.assertTrue(commit_entry.get("failClosed"))
        self.assertEqual(staged_entry.get("timeout"), 30)
        self.assertEqual(commit_entry.get("timeout"), 30)


if __name__ == "__main__":
    unittest.main()
