---
name: kf-g-project-bootstrap-new-project-rules
description: Use this skill when starting a new project and defining baseline repository rules, especially for devcontainer setup, mise-first tooling, pnpm security settings, Vite+ workflows, and kiso.css adoption.
---

# 新規プロジェクト立ち上げルール

この skill は、PJ を新規に立ち上げるときの初期方針を揃えるためのものです。
まず devcontainer と mise を土台に置き、その上で frontend は pnpm + Vite+ + kiso.css を標準にします。

## この skill を使う場面

- 新しい PJ を作る
- 新規リポジトリの初期構成を決める
- devcontainer や mise を含む開発基盤を最初から整える
- frontend の標準 toolchain を決める
- pnpm の supply chain 対策を初期設定へ組み込みたい

## 基本方針

1. 開発環境は必ず devcontainer を作る。
1. tools と日常コマンドの中心は `mise.toml` に集約する。
1. frontend の package manager は pnpm に固定する。
1. frontend の build / dev / check / test は Vite+ の流れに寄せる。
1. reset css は kiso.css を pnpm で導入する。

## 作業手順

1. PJ に frontend が含まれるか確認する。
1. VS Code の user settings.json にある `dev.containers.*`, `dotfiles.*` を確認する。
1. user settings で既に効いている値と、PJ 固有で必要な値を切り分ける。
1. `.devcontainer/` と `mise.toml` を先に設計する。
1. frontend がある場合は `pnpm-workspace.yaml` を作り、pnpm のセキュリティ設定を先に入れる。
1. Vite+ を前提に scaffold と日常コマンドを決める。
1. kiso.css を導入し、エントリ側で最初に読み込む。
1. 最後に `mise run` 系 task で install / dev / check / test / build を揃える。

## PJ全体

### 1. devcontainer を必須にする

- `.devcontainer/devcontainer.json` を必ず作る。
- runtime や package manager の版管理は devcontainer 内に分散させず、原則 `mise.toml` を正本にする。
- devcontainer では `mise install` を実行して、PJ が要求する tool 群を揃える。
- `postCreateCommand` や同等の初期化処理は、`mise install` と `mise run` を中心に組む。
- apt, brew, curl などで個別に runtime を入れるのは、mise で扱えない OS パッケージに限る。

### 2. user settings の dev.containers・dotfiles 設定を先に確認する

- まず user settings.json の `dev.containers.*`, `dotfiles.*` を確認する。
- 既に user settings にある値は、devcontainer 側へ重複して書かない。
- 特に `dev.containers.defaultExtensions` に含まれる拡張は、PJ 固有の理由がない限り `.devcontainer/devcontainer.json` の `customizations.vscode.extensions` へ重複追加しない。
- `dev.containers.copyGitConfig` のような user 方針も、PJ 側で上書きが必要なときだけ明示する。
- override が必要な場合は、なぜ user 設定ではなく PJ 側に置くのかを説明できる状態にする。
- `dotfiles.repository` で指定されたリポジトリの dotfiles は devcontainer 内で常に効く前提で、PJ 固有の devcontainer 設定を考える。

### 3. mise をフル活用する

`mise.toml` は単なる version 指定ファイルとしてではなく、PJ の開発基盤の中心として扱う。

必須方針:

- `[tools]` で runtime と主要 CLI を管理する。
- `[env]` で PJ 固有の環境変数を管理する。
- `[tasks]` で install / dev / check / test / build などの日常コマンドを管理する。
- コマンド実行は `mise run <task>` または `mise exec -- <command>` を優先する。
- README や devcontainer の手順も `mise` ベースで統一する。
- CI でもローカルと同じ `mise` task 名を使い、コマンド定義を二重化しない。

活用観点:

- runtime の version は `[tools]` に寄せる。
- `.env` 読み込みが必要なら `[env]` の `_.file` を使う。
- `node_modules/.bin` や独自 bin を通したいなら `[env]` の `_.path` を使う。
- 必須 secret や接続先は `required = true` で明示する。
- OS 依存や install 順依存がある tool は `os` と `depends` を使って `mise.toml` に閉じ込める。

### 4. devcontainer と mise の役割分担

- devcontainer は「実行場所」を揃える。
- mise は「PJ が必要とする tools / env / tasks」を揃える。
- 同じ version 情報を Dockerfile と `mise.toml` の両方に持たない。
- Dockerfile へ version を直書きするのは、base image の都合で避けられない場合だけにする。
- 日常コマンドは shell script の散在より `mise run` を優先する。

## フロントエンド

### 1. package manager は pnpm 固定

- Node.js 系の package manager は pnpm だけを使う。
- npm / yarn / bun を併用しない。
- lockfile は `pnpm-lock.yaml` のみを正本にする。
- `package.json` の `packageManager` は pnpm に固定する。
- pnpm 自体の導入も `mise.toml` の `[tools]` で管理する。

### 2. pnpm の supply chain ルールを最初に入れる

pnpm の security 設定は `pnpm-workspace.yaml` へ置く。single package 構成でも、このファイルを作って設定を入れる。

初期値:

```yaml
minimumReleaseAge: 10080
strictDepBuilds: true
blockExoticSubdeps: true
trustPolicy: no-downgrade
onlyBuiltDependencies: []
```

運用ルール:

- `minimumReleaseAge` は 7日間、つまり `10080` 分で固定する。
- lifecycle script を実行させる package は、`onlyBuiltDependencies` に明示的に許可したものだけにする。
- install 時に未承認 script が出たら、その package が本当に必要かをレビューしてから allowlist へ追加する。
- `strictDepBuilds: true` にして、未承認 script を CI で見逃さない。
- `blockExoticSubdeps: true` にして、推移的依存の git / tarball URL を遮断する。
- `trustPolicy: no-downgrade` にして、公開経路の信頼性低下を検知する。
- project local の `.npmrc` に機密情報や token helper を置かない。

### 3. Vite+ の ecosystem に乗る

- frontend の scaffold は、まず Vite+ で組めるかを確認する。
- 新規作成の標準フローは `vp create` `vp install` `vp dev` `vp check` `vp test` `vp build` `vp run` を基本にする。
- framework を選ぶときは、Vite plugin として自然に乗るものを優先する。
- lint / format / type-check / test / build は、Vite+ が前提にしている toolchain を優先し、無関係な tool をむやみに混在させない。
- `mise` task も Vite+ のコマンド群を包む形で定義する。
- Vite+ に乗らない構成を採る場合は、採用理由を先に明確にする。

### 4. reset css は kiso.css を採用する

- reset css は kiso.css を標準採用する。
- 導入は `pnpm add kiso.css` で行う。
- app の entry stylesheet か main entry から、project 固有の style より先に読み込む。
- CDN 参照や vendor copy を既定にせず、pnpm 経由で依存管理する。
- 日本語向け設計、低い詳細度、accessibility 配慮、モダン HTML/CSS 対応を前提に採用する。

## 最低限そろえる対象

frontend を含む新規 PJ では、少なくとも次を用意する。

- `.devcontainer/devcontainer.json`
- `mise.toml`
- `pnpm-workspace.yaml`
- `package.json` の `packageManager`
- kiso.css を読み込む entry 側の style または import
- `mise run` で叩ける install / dev / check / test / build task

## 出力方針

- 実際に新規 PJ を作る依頼では、方針説明だけで止めずに必要ファイルを作る。
- user settings から再利用した `dev.containers.*`, `dotfiles.*` と、PJ 側で追加した差分を短く説明する。
- pnpm の allowlist に package を追加した場合は、その理由を残す。
- Vite+ に乗らない例外を選んだ場合は、理由を明記する。

## 最終チェック

- devcontainer を作成したか。
- user settings の `dev.containers.*`, `dotfiles.*` を確認したか。
- `mise.toml` が tools / env / tasks の中心になっているか。
- frontend なら package manager が pnpm に固定されているか。
- `pnpm-workspace.yaml` に `minimumReleaseAge: 10080` を入れたか。
- Vite+ のコマンド群に寄せた構成になっているか。
- kiso.css を pnpm で導入しているか。
