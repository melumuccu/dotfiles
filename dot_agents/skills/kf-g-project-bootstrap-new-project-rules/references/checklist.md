# 最終チェック

入口フローで承認されたルール適用表に **適用** とされた項目だけを確認する。不適用ルールに該当する行はスキップする。

- devcontainer を **適用** とした場合、`.devcontainer/devcontainer.json` を作成したか。
- devcontainer を **適用** とした場合、user settings の `dev.containers.*`, `dotfiles.*` を確認したか。
- `mise.toml` が tools / env / tasks の中心になっているか。
- `mise.toml` の `[tools]` に `pre-commit` と `gitleaks` を載せているか。
- `references/sample-files/` の該当サンプルを確認したか。
- `.github/workflows/gitleaks.yml` で公式 gitleaks action を設定したか。
- `.pre-commit-config.yaml` で `pre-commit` 用 hook と `pre-push` 用 hook の `stages` を明示したか。
- `mise run hooks-install` で `pre-commit install` と `pre-commit install --hook-type pre-push` の両方を実行できるか。
- `pre-commit validate-config` と `pre-commit run --hook-stage pre-push` で hook 設定を検証したか。
- pre-push 全テストを **適用** とした場合、`.pre-commit-config.yaml` に `test-pre-push` hook（`entry: mise run test`, `stages: [pre-push]`）を追加したか。
- pre-push 全テストを **適用** とした場合、`mise run test` が PJ 内の全テストを実行し、`pre-commit run test-pre-push --hook-stage pre-push` で動作確認したか。
- GitHub Action に `GITHUB_TOKEN` を渡し、`GITLEAKS_LICENSE` を不要な既定値として扱っているか。
- frontend なら package manager が pnpm に固定されているか。
- `pnpm-workspace.yaml` に `minimumReleaseAge: 10080` を入れたか。
- Vite+ のコマンド群に寄せた構成になっているか。
- Svelte / SvelteKit を採用する場合、最新安定版を使っているか。
- kiso.css を pnpm で導入しているか。
- lint / format コマンドを `package.json` scripts と `mise run` task に載せたか。
- frontend なら Oxlint / Oxfmt を基本推奨として選定したか。未対応があれば代替を調査したか。
- project hooks に AI エージェント編集後の lint/fmt を登録したか。
- 編集後に対象ファイルへ lint/fmt が走ることを確認したか。
- 利用ツールが Tab 補完後 hook を提供する場合、その登録も確認したか。
