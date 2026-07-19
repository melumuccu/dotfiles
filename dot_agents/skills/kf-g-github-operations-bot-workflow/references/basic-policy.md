# 基本方針

- GitHub 上の issue / PR / comment / review 操作は `gh` または GitHub API で行う。
- AI agent は sandbox 環境で動く前提。host 側でユーザが `gh auth login` 済みでも、sandbox から同じ認証状態を使えるとは限らない。
- issue / PR / repository metadata などの読み取りだけなら、`.agents/credentials/github/.env` の `GH_TOKEN` を環境変数へ読み込み、ユーザ本人 token で `gh` または GitHub API を使う。
- 既存の `gh` 認証を使う場合は、sandbox 内で実際に使えることを確認してから使う。
- GitHub App bot credential は、PR 作成 / comment / review など bot の profile が露出する操作に限って使う。
- 投稿者を人間ユーザと分けるため、投稿時は `.agents/credentials/github/scripts/github-agent-comment.mjs` と `github-agent-review.mjs` が使えるならそれを使う。
- secret や token を出力しない。token 確認時は期限、権限、repository selection など非秘密情報だけ表示する。
