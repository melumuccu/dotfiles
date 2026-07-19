# job 軽量化パターン

job の責務に必要な tool だけ入れる。build 不要 job に full `pnpm install` を載せない。

## build + deploy 系

例: 本番 deploy、PR 向け ephemeral deploy。

- config: `mise.ci-deploy.toml` または `mise.ci-build.toml`
- steps: bootstrap → mise-action → `mise run install` → `mise run build` → deploy
- deploy CLI 利用: `pnpm install` 後の `node_modules/.bin`（`_.path` 設定）

```toml
[env]
_.path = ["./node_modules/.bin"]
```

スクリプトからは PATH 上の CLI を直呼び（`pnpm exec` 不要）。

## cleanup 系（API 削除のみ）

例: ephemeral 環境のリソース削除。

- config: `mise.ci-cleanup.toml`（`node` + deploy CLI のみ）
- **省略**: `mise run install`、build
- bootstrap: `MISE_DATA_DIR` のみで可（pnpm store 不要）

```yaml
cleanup:
  env:
    MISE_OVERRIDE_CONFIG_FILENAMES: mise.ci-cleanup.toml
  steps:
    - uses: actions/checkout@v6
    - name: Configure cache directories
      run: |
        echo "MISE_DATA_DIR=$RUNNER_TOOL_CACHE/mise" >> "$GITHUB_ENV"
        mkdir -p "$RUNNER_TOOL_CACHE/mise"
    - uses: jdx/mise-action@v3
      with:
        cache: false
    - run: node scripts/<cleanup-script>.mjs
```

効果の目安: full install あり ~130s → 軽量化後 ~30s（mise cache + `pnpm install` 省略）。

初回 CLI cold install は数秒。その後は `all tools are installed` で ~1s。

## CLI 直呼び

build + deploy 系: `node_modules/.bin` 経由。
cleanup 系: mise shims 経由。

どちらも spawn 先は PATH 上の CLI 名（`pnpm exec` 不要）。

```javascript
spawnSync('<cli>', args, { cwd: REPO_ROOT, ... });
```

## deploy workflow 専用

### CLI 直呼び

vendor deploy action より CLI 直呼び。推論・追加 install を避ける。

### `skip_deploy` input（計測用）

build まで隔離して mise / pnpm / build の短縮効果を測る。

```yaml
workflow_dispatch:
  inputs:
    skip_deploy:
      type: boolean
      default: false

- name: Deploy
  if: github.event_name != 'workflow_dispatch' || inputs.skip_deploy != true
  run: <cli> deploy
```

ephemeral 環境作成が必須の workflow には不要。
