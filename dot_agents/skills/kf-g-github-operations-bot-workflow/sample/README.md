# .agents/credentials/github

このディレクトリは AI agent が GitHub 連携に必要な認証情報を格納するためのもの。

このディレクトリは local-only。git 管理しない。(グローバル gitignore に登録済みなので local gitignore に登録する必要はない)

## GitHub App

- Name: `ai-agent-melumuccu`

## `.env`

このディレクトリの `.env` に以下を記載する。
値は GitHub App 作成後に取得する。Bitwarden の GitHub にも記録する。

```sh
GH_TOKEN=github_pat_xxx
AI_AGENT_GITHUB_CLIENT_ID=xxx
AI_AGENT_GITHUB_INSTALLATION_ID=xxx
AI_AGENT_GITHUB_PRIVATE_KEY_PATH=.agents/credentials/github/ai-agent-melumuccu.xxxxxxxxxxx.private-key.pem
```

`GH_TOKEN` は読み取り操作で使うユーザ本人 token。
AI agent は sandbox 環境で動くため、host 側の `gh auth login` 済み状態を前提にしない。

JWT の `iss` には GitHub docs 推奨の Client ID を使う。
古い local 設定との互換用に script は `AI_AGENT_GITHUB_APP_ID` も fallback として読む。
旧 `GITDOC_AGENT_*` も fallback として読む。

```sh
chmod 600 .agents/credentials/github/.env
```

## Private key

GitHub App の private key をこのディレクトリに配置する。

```sh
chmod 600 .agents/credentials/github/ai-agent-melumuccu.xxxxxxxxxxx.private-key.pem
```

private key を紛失した場合は GitHub App 設定画面で再発行する。
古い key が不要なら削除する。

## Scripts

AI agent が使う補助 script。
人間が日常的に直接使う前提ではない。

```sh
node .agents/credentials/github/scripts/github-agent-token.mjs
node .agents/credentials/github/scripts/github-agent-comment.mjs OWNER/REPO ISSUE_OR_PR_NUMBER BODY_FILE
node .agents/credentials/github/scripts/github-agent-review.mjs OWNER/REPO PR_NUMBER BODY_FILE
```

`github-agent-token.mjs` は GitHub App private key から installation token を発行する。
installation token は約 1 時間で失効する。
AI agent は投稿直前に毎回この script 相当の処理を実行する。

`github-agent-comment.mjs` は issue / PR conversation comment 用。
`github-agent-review.mjs` は PR review / inline review comment 用。
どちらも user token ではなく GitHub App installation token を使うため、投稿者がユーザ本人と分離される。

`mise.toml` task は追加しない。
このディレクトリは local-only で、tracked task から参照すると他環境で壊れるため。
