# RUNNER_TOOL_CACHE bootstrap

self-hosted runner では job 間でディスクが残る。`MISE_DATA_DIR` / pnpm store を `runner.tool_cache` 配下に固定すると 2 回目以降の cold download を避けられる。

## 採用パターン

build + deploy 系 job の checkout 直後に置く。

```yaml
- name: Configure cache directories
  run: |
    echo "MISE_DATA_DIR=$RUNNER_TOOL_CACHE/mise" >> "$GITHUB_ENV"
    echo "PNPM_CONFIG_STORE_DIR=$RUNNER_TOOL_CACHE/pnpm-store" >> "$GITHUB_ENV"
    mkdir -p "$RUNNER_TOOL_CACHE/mise" "$RUNNER_TOOL_CACHE/pnpm-store"

- uses: jdx/mise-action@v3
  with:
    cache: false
```

cleanup job で pnpm 不要なら `PNPM_CONFIG_STORE_DIR` と pnpm-store の `mkdir` は省略可。

```yaml
- name: Configure cache directories
  run: |
    echo "MISE_DATA_DIR=$RUNNER_TOOL_CACHE/mise" >> "$GITHUB_ENV"
    mkdir -p "$RUNNER_TOOL_CACHE/mise"
```

## Why 採用

| 判断 | 理由 |
|------|------|
| bootstrap step で `$RUNNER_TOOL_CACHE` | step スコープの env 変数として安全に参照できる |
| `mkdir -p` | 初回 job でも directory 不足で落ちない |
| `cache: false` | 永続化済みなら GHA cache hit でも毎回 download+展開 ~20s が乗る |
| GHA cache 不採用 | restore ~20s が pnpm install 本体より重いことがある |

## Why workflow/job `env` に `${{ runner.tool_cache }}` を書かない

`runner` context は **step スコープのみ**。workflow / job レベルだと job 起動前に評価され workflow file validation で落ちる。

正: bootstrap step 内で `$RUNNER_TOOL_CACHE`（shell env）を使う。

## env 変数

| 変数 | 用途 |
|------|------|
| `MISE_DATA_DIR` | mise が tool を保持する directory |
| `PNPM_CONFIG_STORE_DIR` | pnpm 11 が読む package store（**`PNPM_STORE_DIR` ではない**） |

`PNPM_STORE_DIR` のみだと pnpm が無視し、GHA cache path が空のまま save 失敗することがある。

ref: https://pnpm.io/configuring

## runner `.env` 保険（任意）

workflow bootstrap で足りることが多い。runner 再構築時の保険として host `.env` に固定してもよい。

```sh
MISE_DATA_DIR=/Users/<user>/.cache/<repo>/mise
PNPM_CONFIG_STORE_DIR=/Users/<user>/.cache/<repo>/pnpm-store
```

## 成功のログ指標

warm run で mise-action ログに次が出る。

```
mise all tools are installed
```
