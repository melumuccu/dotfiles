# GitHub App Credentials

AI agent 用 credential は repository local の `.agents/credentials/github` を使う。
このディレクトリは local-only で、git 管理しない。

## setup

PJ local に `.agents/credentials/github` が存在しない場合:

1. sample credential ディレクトリを repository local の `.agents/credentials/github` へコピーする。
1. sample 配下のファイル群をすべてコピーする。
1. `.agents/credentials/github/.env.example` を `.agents/credentials/github/.env` にリネームする。
1. ここまでを AI agent の作業対象とする。
1. コピー後、残りのユーザ作業をチャットに出力する。

注: AI agent が secret を作成、推測、生成、貼り付けしない。

コマンド例:

```sh
mkdir -p .agents/credentials/github

cp -R .agents/skills/kf-g-github-operations-bot-workflow/sample/. \
  .agents/credentials/github/

mv .agents/credentials/github/.env.example \
  .agents/credentials/github/.env
```

コピー元: この skill 配下の下記ディレクトリ

```text
sample
```

コピー先: local repository 配下の下記ディレクトリ

```text
.agents/credentials/github
```

ユーザへ出力する残作業:

1. `.env` に読み取り用の `GH_TOKEN` を記入する。
1. `.env` に投稿用の `AI_AGENT_GITHUB_CLIENT_ID`、`AI_AGENT_GITHUB_INSTALLATION_ID`、`AI_AGENT_GITHUB_PRIVATE_KEY_PATH` を記入する。
1. GitHub App の private key (`ai-agent-melumuccu.{YYYY-MM-DD}.private-key.pem`) を `.agents/credentials/github` 直下へ配置する。
1. `.env` と private key に `chmod 600` を設定する。
1. 設定完了後、AI agent に GitHub bot 投稿の再実行を依頼する。

コマンド例:

```sh
chmod 600 .agents/credentials/github/.env
chmod 600 .agents/credentials/github/ai-agent-melumuccu.{YYYY-MM-DD}.private-key.pem
```
