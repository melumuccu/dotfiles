# 公式ドキュメント URL 記載

## 基本方針

- 参照した公式ドキュメント URL があるなら、コメントに残す
- URL は根拠として残す。WHAT の説明で埋めない

## 配置ルール

- 1ファイル全体に関係するドキュメントはファイル先頭周辺に置く
- 特定のコードだけに関係するドキュメントは、そのコードの直上に置く
- コメントは対象コードに近いほどよい。後ろの説明で読ませない

## 書き方

- URL は短く、直接貼る
- 1つのコメントに WHY と URL を並べてよい
- URL だけのコメントにしない

## 例

ファイル全体:

```ts
// 公式ドキュメント: https://example.com/sdk/auth
// このモジュールは認証更新を一元化する。個別実装に散らすと失効時の挙動が揺れる。
export async function refreshToken() {}
```

局所:

```ts
// 公式ドキュメント: https://example.com/immich-api-assets
// Immich API の空 ID は上位で入力エラーに正規化する。
if (!assetId) {
  return error(400, "assetId is required");
}
```

## 注意

- WHAT の説明を URL コメントに混ぜない
- URL は公式ドキュメントを優先する
