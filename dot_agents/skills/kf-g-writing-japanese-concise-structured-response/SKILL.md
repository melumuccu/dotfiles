---
name: kf-g-writing-japanese-concise-structured-response
description: Write or revise Japanese Markdown documents and code comments in this repository with a concise, structured style. Use this whenever the task involves drafting Markdown, especially maintainable ordered lists with 1.-style numbering and anchor-based cross references, or writing code comments.
---

# Japanese Writing Style For Markdown And Comments

この skill の目的は、日本語の Markdown 文書とコードコメントに一貫した書き方を適用し、順序付きリストと相互参照も保守しやすい形にそろえること。

## 使う場面

- Markdown ファイルを書くとき
- Markdown ファイルを修正するとき
- ガイド、手順、ランブック、メモなどで順序付きリストを扱うとき
- 項目番号は必要だが、途中追加や並び替えのたびに採番し直したくないとき
- 後続の項目や本文から、前の項目を壊れにくい形で参照したいとき
- コードコメントを書くとき
- コードコメントを修正するとき

## 適用範囲

- Markdown ファイル本文
- 見出し
- 箇条書き
- 順序付きリスト
- 内部リンク
- アンカー
- コード内コメント

## 適用範囲外

- ユーザー向け回答本文 (通常通りの対話口調とする)

## 参照ファイル

- `references/markdown-style.md`: Markdown 本文の基本ルール、出力方針、編集時の注意
- `references/ordered-list-cross-reference.md`: 順序付きリストの `1.` 運用とアンカー相互参照
- `references/code-comments.md`: コードコメントの書き方、良い例、避ける例

## 読み進め方

1. 対象が Markdown 本文かコードコメントかを確認する
1. Markdown 本文を扱うなら `references/markdown-style.md` を読む
1. 順序付きリストや内部参照があるなら `references/ordered-list-cross-reference.md` も読む
1. コードコメントを書くなら `references/code-comments.md` を読む
1. 必要な観点だけ適用して出力する

## 共通方針

- 敬語を使わない
- 体言止めを多めに使う
- 一文を短く保つ
- 箇条書きと数字リストを優先
- 余分な接続詞を減らす
- 抽象語の連打を避ける
- 依頼範囲外の文章まで全面的に書き換えない
- 既存情報の意味を変えない
- 既存フォーマットに明確な制約がある場合は、その制約を優先する

## 出力方針

- Markdown 本文を求められたら、本文の完成形を優先する
- 解説を求められていない限り、文書外の説明を増やしすぎない
- 元の文書のトーンや文体は可能な限り維持する
- この skill のスタイルはチャット応答本文には適用しない

## 最終チェック

- Markdown 本文なら `references/markdown-style.md` を確認したか
- 順序付きリストや内部参照があるなら `references/ordered-list-cross-reference.md` を確認したか
- コードコメントなら `references/code-comments.md` を確認したか
- この skill のスタイルをチャット応答本文へ持ち込んでいないか
