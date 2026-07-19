# アンチパターン

self-hosted + mise + pnpm で実行時間短縮する文脈で、**採用しなかった** 変更。

| アンチパターン | なぜダメ | 典型観測 |
|---------------|----------|----------|
| `actions/cache@v4`（pnpm store） | restore ~20s が install 本体より重い | 合計 job 時間が悪化 |
| `mise-action cache: true` | warm でも毎回 download+展開 | mise step が ~20s 級に戻る |
| `PNPM_STORE_DIR` のみ | pnpm 11 が無視。GHA cache save 失敗 | cache step エラー |
| workflow/job で `runner.tool_cache` env | `runner` context 未使用で validation 失敗 | workflow 起動前に落ちる |
| aqua `pnpm` shorthand | self-hosted Mac で install 失敗することがある | mise-action 失敗 |
| 冗長 `mise install` step | `mise-action` の `install: true` と重複 | 0s だがノイズ |
| cleanup で full `pnpm install` | 削除用 CLI だけなら不要 | ~10s 無駄 |
| deploy action ラッパー（計測時） | packageManager 推論・追加 install | 計測が汚れる |
| Docker `build` stage を CI に流用 | 変更コスト大。RUNNER_TOOL_CACHE で足りる場合が多い | 見送り |
| `node_modules` GHA cache | store 永続で install ~10s。invalidation 設計が複雑 | 見送り |
| github-hosted runner へ戻す | self-hosted 採用理由（制御・コスト）を損なう | 見送り |
| ephemeral deploy に deploy スキップ input | 環境作成が目的の workflow では不可 | 不要 |

## 誤解しやすい点

### 「GHA cache を足せば速くなる」

self-hosted ではディスクが job 間で残る。`RUNNER_TOOL_CACHE` 永続化の方が warm run で安い。GHA cache は restore の固定コストが支配的になりやすい。

### 「`PNPM_STORE_DIR` と `PNPM_CONFIG_STORE_DIR` は同じ」

pnpm 11 が store に読むのは `PNPM_CONFIG_STORE_DIR`。`PNPM_STORE_DIR` だけでは意図した path に行かない。

### 「2 回目の短縮は pnpm cache の追加効果」

連続 run では install は横ばい（~11s）のことが多い。差分は remote deploy ステップ（incremental upload 等）側に出やすい。
