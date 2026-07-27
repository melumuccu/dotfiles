#!/usr/bin/env python3
"""stop hook: kf-lint verify on working tree delta."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "modules"))

import cursor_hook_io as hook_io
import git_changed_files as git_files
import kf_lint_cli as kf_lint


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        hook_io.empty()

    status = payload.get("status")
    loop_count = payload.get("loop_count", 0)
    if status != "completed" or not isinstance(loop_count, int) or loop_count >= 3:
        hook_io.empty()

    roots = payload.get("workspace_roots") or []
    if not isinstance(roots, list) or not roots:
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd:
            roots = [cwd]
        else:
            hook_io.empty()

    kf_lint_bin = kf_lint.resolve_kf_lint()
    if not kf_lint_bin:
        hook_io.empty()

    all_errors: list[dict] = []
    for root in roots:
        if not isinstance(root, str) or not root.strip():
            continue
        repo_root = Path(root).expanduser().resolve()
        if not git_files.is_git_repo(repo_root):
            continue
        paths = git_files.collect_working_tree_paths(repo_root)
        if not paths:
            continue
        result = kf_lint.run_kf_lint_verify(repo_root, paths, kf_lint_bin)
        if result is None:
            hook_io.empty()
        diagnostics, _exit_code = result
        all_errors.extend(kf_lint.error_diagnostics(diagnostics))

    if all_errors:
        hook_io.followup(kf_lint.format_stop_followup(all_errors))
    hook_io.empty()


if __name__ == "__main__":
    main()
