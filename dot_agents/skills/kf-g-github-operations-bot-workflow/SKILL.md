---
name: kf-g-github-operations-bot-workflow
description: Use this skill whenever working with GitHub issues, pull requests, comments, reviews, repository metadata, or agent-authored GitHub activity. Always use it before posting GitHub comments or reviews, checking remote repository context, or deciding whether GitHub App bot credentials are available.
---

# GitHub 操作と AI agent bot 投稿

この SKILL.md は入口として扱い、詳細は `references` 配下の該当ファイルを読む。
この skill は GitHub 操作全般の基本ルールを扱う。

issue 管理の進め方は `kf-g-github-issue-worktree-management`、PR 作成・レビューの詳細は `kf-g-github-pr-review-workflow` も使う。

## 使う場面

- GitHub issue / PR / comment / review を扱う。
- GitHub repository metadata や remote context を確認する。
- AI agent が GitHub App bot credential で投稿する。
- `.agents/credentials/github` の有無や setup 方法を判断する。
- commit / push 時の gitleaks 検知を扱う。

## 読み進め方

1. まず [basic-policy.md](references/basic-policy.md) を読む。
1. GitHub 操作先を確認するなら [repository-context.md](references/repository-context.md) を読む。
1. GitHub App credential の setup や有無を確認するなら [github-app-credentials.md](references/github-app-credentials.md) を読む。
1. Issue / PR comment または PR review を投稿するなら [bot-comment-review.md](references/bot-comment-review.md) を読む。
1. gitleaks 検知を扱うなら [gitleaks.md](references/gitleaks.md) を読む。
1. 作業完了前に [checklist.md](references/checklist.md) を確認する。

## 参照ファイル

- [basic-policy.md](references/basic-policy.md): GitHub 操作と secret 取り扱いの基本方針
- [repository-context.md](references/repository-context.md): 操作先 remote 確認
- [github-app-credentials.md](references/github-app-credentials.md): GitHub App credential の setup とユーザ残作業
- [bot-comment-review.md](references/bot-comment-review.md): bot comment / review script の使い方
- [gitleaks.md](references/gitleaks.md): gitleaks 検知時の禁止事項と対応
- [checklist.md](references/checklist.md): 作業完了前の確認項目
