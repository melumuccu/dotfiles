# pnpm

## 1. package manager は pnpm 固定

- Node.js 系の package manager は pnpm だけを使う。
- npm / yarn / bun を併用しない。
- lockfile は `pnpm-lock.yaml` のみを正本にする。
- `package.json` の `packageManager` は pnpm に固定する。
- pnpm 自体の導入も `mise.toml` の `[tools]` で管理する。

## 2. pnpm の supply chain ルールを最初に入れる

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
