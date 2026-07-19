---
name: kf-g-code-comment-rules
description: Use this project skill whenever adding, editing, reviewing, or deciding whether to keep source-code comments in this repository. It is the authoritative rule set for code comments, including WHY-only content, official-doc URL breadcrumbs, and comment placement.
---

# コードコメント規約

この skill は、このリポジトリのコードコメント全般の入口。
詳細は `references/why-only.md` と `references/official-doc-url.md` に分ける。

## 使う場面

- コメントを追加、編集、レビュー、削除判断する時
- コメントを残すか迷う時
- 公式ドキュメント URL の残し方を決める時
- コメントの配置を決める時

## 参照ファイル

- `references/why-only.md`: WHY-only の基準、判断手順、例
- `references/official-doc-url.md`: 公式ドキュメント URL の扱い、配置ルール、例

## 読み進め方

1. `references/why-only.md` を読む
1. `references/official-doc-url.md` を読む
1. 必要なら周辺コードと関連ドキュメントを読む
1. コメントは WHY と根拠だけに絞る

## 最終チェック

- コメントは WHY を説明しているか
- 参照した公式ドキュメント URL を残しているか
- ファイル全体向けか局所向けかで配置を分けているか
- WHAT の説明になっていないか
