# Bot Comment / Review

Issue または PR conversation comment:

```sh
node .agents/credentials/github/scripts/github-agent-comment.mjs OWNER/REPO ISSUE_OR_PR_NUMBER BODY_FILE
```

PR review comment:

```sh
node .agents/credentials/github/scripts/github-agent-review.mjs OWNER/REPO PR_NUMBER BODY_FILE
```

運用:

- 投稿本文は一時ファイルに作る。
- 投稿後、URL をユーザに報告する。
- 失敗時は HTTP status と GitHub API message を読む。
- user token に自動 fallback しない。bot credential が壊れている場合は原因を直す。

Token:

- `github-agent-comment.mjs` / `github-agent-review.mjs` は投稿直前に installation token を発行する。
- 長期間未使用でも、`.env` と private key が有効ならユーザ操作は不要。
- `github-agent-token.mjs` の手動実行は診断用。通常投稿前に毎回実行しなくてよい。
