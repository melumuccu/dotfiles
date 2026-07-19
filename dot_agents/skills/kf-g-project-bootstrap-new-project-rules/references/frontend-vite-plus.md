# Vite+ と kiso.css

## 1. Vite+ の ecosystem に乗る

- frontend の scaffold は、まず Vite+ で組めるかを確認する。
- 新規作成の標準フローは `vp create` `vp install` `vp dev` `vp check` `vp test` `vp build` `vp run` を基本にする。
- framework を選ぶときは、Vite plugin として自然に乗るものを優先する。
- Svelte / SvelteKit を選ぶ場合は、リリース種別を確認し、最新の安定版を採用する。
- preview / next / rc などの不安定版は、明確な採用理由がある場合だけ使う。
- lint / format / type-check / test / build は、Vite+ が前提にしている toolchain を優先し、無関係な tool をむやみに混在させない。
- `mise` task も Vite+ のコマンド群を包む形で定義する。
- Vite+ に乗らない構成を採る場合は、採用理由を先に明確にする。

## 2. reset css は kiso.css を採用する

- reset css は kiso.css を標準採用する。
- 導入は `pnpm add kiso.css` で行う。
- app の entry stylesheet か main entry から、project 固有の style より先に読み込む。
- CDN 参照や vendor copy を既定にせず、pnpm 経由で依存管理する。
- 日本語向け設計、低い詳細度、accessibility 配慮、モダン HTML/CSS 対応を前提に採用する。
