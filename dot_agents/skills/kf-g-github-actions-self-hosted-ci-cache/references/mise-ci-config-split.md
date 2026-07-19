# mise CI config 分割

workflow ごとに `MISE_OVERRIDE_CONFIG_FILENAMES` で専用 config を指定する。ローカル dev 用 `mise.toml` と CI 用を混ぜない。

## ファイル役割の例

| ファイル | 用途 | 利用先 |
|----------|------|--------|
| `mise.toml` | ローカル dev（hooks 等含む） | devcontainer / 手元 |
| `mise.ci-deploy.toml` | 本番 deploy | deploy workflow |
| `mise.ci-build.toml` | build + deploy（PR 向け等） | build deploy job |
| `mise.ci-cleanup.toml` | cleanup 専用（CLI のみ） | cleanup job |

命名はリポジトリ規約でよい。要点は **workflow 責務ごとに config を分ける** こと。

## workflow 側

```yaml
env:
  MISE_OVERRIDE_CONFIG_FILENAMES: mise.ci-deploy.toml
```

cleanup job だけ別 config にする場合は job `env` で上書き。

```yaml
cleanup:
  env:
    MISE_OVERRIDE_CONFIG_FILENAMES: mise.ci-cleanup.toml
```

## CI 用 config の中身

build + deploy 最小構成:

```toml
[tools]
node = "24"
"npm:pnpm" = "11.10.0"

[env]
NODE_ENV = "production"
_.path = ["./node_modules/.bin"]

[tasks.install]
run = "pnpm install --frozen-lockfile"

[tasks.build]
run = "pnpm build"
```

cleanup 最小構成（deploy CLI のみ必要な場合）:

```toml
[tools]
node = "24"
"npm:<cli>" = "<version>"
```

`<cli>` は cleanup script が呼ぶコマンド（例: インフラ deploy CLI）。

## `"npm:pnpm"` backend を使う理由

`RUNNER_TOOL_CACHE` 移行後、aqua backend の `pnpm` install が self-hosted Mac で失敗することがある。

- 採用: `"npm:pnpm"` — node 同梱 npm 経由で入れられ再現性がある
- 実測環境: Apple Silicon（darwin/arm64）self-hosted Mac
- 採用理由は「aqua backend の install 失敗回避」に寄せる（アーキ固有の一般論に依存しない）

ref: https://mise.jdx.dev/dev-tools/backends/npm.html
ref: https://github.com/jdx/mise/discussions/9453

## cache 共有

`MISE_DATA_DIR` は workflow 共通の `RUNNER_TOOL_CACHE/mise` を使うため、config ファイル名が違っても **tool 実体は job 間で共有**される。実行時間への影響なし。

## drift 防止

| 変更対象 | 同期先 |
|----------|--------|
| `node` / `pnpm` バージョン | `mise.toml` と各 `mise.ci-*.toml` |
| cleanup CLI バージョン | `package.json`（該当する場合）と `mise.ci-cleanup.toml` |

## CI 用 config に入れない tool

- dev 専用 hook runner（`pre-commit`, `gitleaks` 等）

入れると cache miss 時の download が増え、mise-action が再び支配的になる（~100s 級）。
