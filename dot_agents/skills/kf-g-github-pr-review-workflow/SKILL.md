---
name: kf-g-github-pr-review-workflow
description: Use this skill whenever creating, updating, reviewing, commenting on, or preparing a GitHub pull request. Always use it for issue-linked PRs, reviewer assignment, PR body conventions, PR comments, PR reviews, and deciding whether to use GitHub App bot review scripts.
---

# GitHub PR 作成・レビュー運用

この skill は PR 作成、更新、レビュー、comment のルール。
GitHub 操作全般は `kf-g-github-operations-bot-workflow`、issue 起点の作業は `kf-g-github-issue-worktree-management` も使う。

## 基本方針

- 1 issue 1 PR を基本にする。
- PR は対応 issue に紐づけ、merge / close 時に issue が閉じる形を優先する。
- PR 作成後、issue comment に PR URL を残す。
- reviewer は　gh コマンドでログイン済みのユーザーを reviewer に設定する
- AI agent の PR 作成 / comment / review は GitHub App bot credential を優先する。

## PR 作成前

確認:

1. issue 番号、issue URL、完了条件
1. branch が issue 用 branch か
1. worktree が issue 用 worktree か
1. unrelated change が混ざっていないか
1. repository native の check が通るか

## PR body

PR body には最低限これを含める。

- 対応 issue
- 変更概要
- 検証結果
- 未確認事項または残リスク

Issue 自動 close が必要なら、body に `Closes #<issue-number>` または repository で定めた closing keyword を入れる。

## PR description / comment のリンク化

PR description / comment / reply の本文作成時、下記対象が本文に出るなら可能な限りリンク形式で記述する。
URL が未確定の対象は、URL 判明後に本文更新または comment / reply で補う。

- issue: `#<issue-number>`。別 repository なら `OWNER/REPO#<issue-number>`。
- PR: `#<pr-number>`。別 repository なら `OWNER/REPO#<pr-number>`。
- commit: `[{short commit id}]({PR base URL}/changes/{commit id})`。
- file: `[path/to/file](<repository URL>/blob/<branch-or-commit>/path/to/file)`。
- file line: `[path/to/file:L<line>](<repository URL>/blob/<branch-or-commit>/path/to/file#L<line>)`。
- review comment / thread: `[review comment](<comment URL>)`。
- CI / check run: `[<check name>](<check run URL>)`。

## PR 作成後

実施:

1. PR URL を issue に comment する。
1. reviewer を設定する。
1. issue status を review 待ちへ更新する。
1. CI / checks を確認する。
1. 失敗時は原因を調査し、必要なら issue / PR に状況を残す。

## Bot comment / review

PR conversation comment:

```sh
node .agents/credentials/github/scripts/github-agent-comment.mjs OWNER/REPO PR_NUMBER BODY_FILE
```

PR review comment:

```sh
node .agents/credentials/github/scripts/github-agent-review.mjs OWNER/REPO PR_NUMBER BODY_FILE --event COMMENT
```

Review event:

- `COMMENT`: 通知・確認・中立コメント。
- `APPROVE`: repository ルール上、AI agent approval が許されている場合だけ使う。
- `REQUEST_CHANGES`: 明確な blocker があり、repository ルール上 AI agent が requested changes を出してよい場合だけ使う。

## Review 対応

レビューコメント対応時:

- 未解決 thread / requested changes / CI failure を確認する。
- ユーザからの PR comment / review comment には必ず reply で応答する。
- 複数の review comment が 1 つの review に含まれる場合でも、各 review comment / thread ごとに個別 reply する。
- 指摘ごとに修正、説明、保留を分ける。
- 修正、説明、保留の内容は該当 comment / thread の reply に残す。
- 自分が作った unrelated change を混ぜない。

## 禁止事項

- Merge 処理
- 複数の comment がまとまった review に対して、まとめて 1 つの comment を作成して reply すること。

## 最終確認

- 1 issue 1 PR の対応になっているか。
- issue に PR URL を残したか。
- reviewer を設定したか。
- AI agent comment / review は bot credential で投稿したか。
- ユーザからの PR comment / review comment へ個別に reply したか。
- PR description / comment / reply のリンク化対象を可能な限りリンク形式で書いたか。
- gitleaks 失敗を回避していないか。
