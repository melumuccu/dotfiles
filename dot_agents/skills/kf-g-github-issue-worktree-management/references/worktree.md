# Worktree 作成

issue 着手時は repository 外の sibling directory に worktree を作る。

## 命名

- branch: `issue-<issue-number>-<slug>`
- path: `../<repo-name>-issue-<issue-number>-<slug>`

## 作成手順

1. リポに `worktree:add` 系 mise task があればそれを使う。
   例
   ```sh
   mise run worktree:add -- <issue-number> <slug>
   ```
1. なければ `git worktree add` で上記命名規約どおり作成する。

## `.worktreeinclude`

- worktree 側へ継承すると有益と思われる gitignored ファイルは、ユーザに提案し、承認を得た上で `.worktreeinclude` に記載する。
- 例: `.dev.vars` / `.agent-browser/` / `.agents/credentials/github/`
- Claude Code `--worktree` も同ファイルを参照する。
- bootstrap があるリポでは `pnpm install` と `hooks-install`（gitleaks）まで含める。GVS 有効時の install は実質瞬時。

## ルール

- main worktree は同期、確認、緊急操作用に残す。
- 既存 worktree がある場合は `git worktree list` で確認する。
- network share や外部 volume に置く場合は `git worktree lock --reason <reason>` を検討する。
- `--force` は原則禁止。clean にしてから remove / recreate する。
