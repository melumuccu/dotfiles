---
name: kf-g-github-actions-self-hosted-ci-cache
description: Use when optimizing GitHub Actions workflows on self-hosted runners with mise and pnpm. Covers RUNNER_TOOL_CACHE persistence, mise CI config split, and patterns to avoid (GHA cache, PNPM_STORE_DIR). Apply before editing build-and-deploy CI workflows.
---

# GitHub Actions self-hosted CI cache 規約

この SKILL.md は入口として扱い、詳細は `references` 配下の該当ファイルを読む。
一般的な GitHub Actions 最適化手順は重複して書かない。
この skill は、self-hosted runner + mise + pnpm で **実行時間を短くする** ための検証済み判断だけを補完する。

## 使う場面

- self-hosted runner 上の GHA workflow を新規設計、短縮、review する
- `mise-action` / `pnpm install` が支配的な job を直す
- build + deploy 系 workflow を横展開する
- cleanup など build 不要 job を軽量化する
- GHA cache 導入の是非を判断する

## 前提

- **Apple Silicon Mac** self-hosted runner（darwin/arm64）を想定（他アーキでも bootstrap 方針は同じ）
- `mise` + `pnpm` + `node`
- runner は常時起動推奨（queue 待ち回避）

## 採用パターン要約

| 項目 | 採用 |
|------|------|
| cache 本体 | `RUNNER_TOOL_CACHE` 永続化（bootstrap step） |
| mise env | `MISE_DATA_DIR=$RUNNER_TOOL_CACHE/mise` |
| pnpm env | `PNPM_CONFIG_STORE_DIR=$RUNNER_TOOL_CACHE/pnpm-store` |
| mise-action | `cache: false` |
| GHA cache | 使わない（self-hosted では restore オーバーヘッドが重い） |
| mise config | workflow ごとに `mise.*.toml` を分離 |
| pnpm backend | `"npm:pnpm"`（aqua install 失敗回避） |
| 冗長 step | `mise install` 削除 |
| cleanup job | CLI のみの軽量 config、`pnpm install` 省略 |

## 計測実績の目安（warm run）

| 対象 | 改修前の典型 | warm run 後の典型 | 主因 |
|------|-------------|------------------|------|
| build+deploy job | ~140s | ~35–60s | mise ~100s→~1s |
| cleanup job（軽量化後） | ~130s | ~25–35s | mise 短縮 + `pnpm install` 省略 |

warm run 基準: `mise-action` ~1s（ログ `all tools are installed`）、`pnpm install` ~10s 台。

## 残ボトルネック

- `pnpm install` ~11s: store cache 済みでも毎 job `node_modules` リンクは必須
- remote deploy ステップ: クラウド API 待ち（短縮しにくい）
- `build` ~7–8s: cache ROI 低、見送り推奨

## 読み進め方

1. bootstrap と env 変数 → [bootstrap-runner-tool-cache.md](references/bootstrap-runner-tool-cache.md)
2. mise config 分割 → [mise-ci-config-split.md](references/mise-ci-config-split.md)
3. やってはいけないこと → [anti-patterns.md](references/anti-patterns.md)
4. job 軽量化 → [job-lightweight-pattern.md](references/job-lightweight-pattern.md)
5. 計測と次手 → [measurement-and-verification.md](references/measurement-and-verification.md)

## 参照ファイル

- [bootstrap-runner-tool-cache.md](references/bootstrap-runner-tool-cache.md): `RUNNER_TOOL_CACHE` bootstrap と mise-action 設定
- [mise-ci-config-split.md](references/mise-ci-config-split.md): workflow 別 `mise.*.toml` の分離
- [anti-patterns.md](references/anti-patterns.md): GHA cache、`PNPM_STORE_DIR`、aqua pnpm 等
- [job-lightweight-pattern.md](references/job-lightweight-pattern.md): cleanup 軽量化、CLI 直呼び
- [measurement-and-verification.md](references/measurement-and-verification.md): deploy スキップ計測、warm run 2 回比較

## 共通チェック

- bootstrap step が checkout 直後にあるか
- `PNPM_CONFIG_STORE_DIR` を使っているか（`PNPM_STORE_DIR` だけではないか）
- workflow/job `env` に `${{ runner.tool_cache }}` を書いていないか
- `mise-action` が `cache: false` か
- `actions/cache@v4` を pnpm/mise に足していないか
- CI 用 mise config に dev 専用 tool（hooks 等）が入っていないか
- cleanup job が build + full `pnpm install` 不要なのにやっていないか
