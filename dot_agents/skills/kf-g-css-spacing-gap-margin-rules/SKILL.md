---
name: kf-g-css-spacing-gap-margin-rules
description: Use this skill when designing, reviewing, or generating CSS spacing rules. Apply it whenever the user asks whether spacing should use gap, margin, or structural empty space, wants to avoid margin-based layout spacing, or needs rules for container-owned spacing in grid or flex layouts.
---

# CSS 間隔設計ルール

この skill は、間隔の責務を子要素ではなくコンテナ側へ戻し、規則的な間隔は `gap`、構造的な空白は空のグリッドセル、`margin` は例外に限定するためのものです。
`grid-template` の書き方や空セルの表記ルールは [../kf-g-css-flex-grid/SKILL.md](../kf-g-css-flex-grid/SKILL.md) を優先し、この skill では間隔責務の分離に絞って扱います。

## この skill を使う場面

- `gap` と `margin` のどちらを使うか決めるとき
- siblings 間の余白を `margin` で積んでよいか見直すとき
- レイアウト内の空白を `gap`、空セル、`margin` のどれで表現するか決めるとき
- grid や flex の子要素間隔を、コンテナ責務へ戻せないか検討するとき
- AI が生成した CSS に、場当たり的な `margin-block-start` や `margin-inline-start` が混ざっていないか確認するとき

## 最初に決めること

1. その間隔は同一コンテナ内の規則的な間隔か
1. その空白はレイアウト上の位置関係そのものを表すか
1. その余白はコンテナ内の責務か、コンテナ外との関係か
1. 既存構造を変えられるか

## 基本方針

### 1. 規則的な間隔は `gap`

- 同じコンテナ内で繰り返される子要素間の距離は、まず `gap` を使う。
- `grid` と `flex` の子要素間隔を、兄弟要素同士の `margin` で表現しない。
- 縦積みの並びも、共有コンテナを持てるなら `display: grid` と `gap` を優先する。
- レイアウトのリズムを子要素側の `margin-block-start` や `margin-inline-start` に持たせない。

```css
.stack {
  display: grid;
  gap: 0.75rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
```

### 2. 構造的な空白は空のグリッドセル

- 空白そのものが配置の意味を持つなら、`gap` ではなく `grid-template` 上の空セルで表現する。
- 見出しだけをずらす、画像の横へ意図的な余白列を残す、本文の開始位置を段ごとにそろえる、といった場面が対象である。
- 空セルは余白の代用品ではなく、レイアウト構造の一部として扱う。
- 空セルの表記は必ず `...` を使う。

```css
.hero {
  display: grid;
  grid-template:
    "...   title" auto
    "media body " auto
    / 4rem 1fr;
}
```

### 3. `margin` は補足的に扱う

- `margin` は内部レイアウトの主手段にしない。
- `margin` を使ってよいのは、コンテナ外との関係を作る場面か、既存構造を変えられず `gap` を持つコンテナを用意できない例外に限る。
- コンポーネント内部の規則的な余白を、子要素ごとの `margin` で管理しない。
- 構造的なズレや位置調整を、要素側の `margin` でごまかさない。

### 4. `margin` を使うなら責務を限定する

- 使う場所は、コンポーネントルートか、外部レイアウトとの接続点に寄せる。
- 同じパターンの繰り返しに複数の child margin が並ぶなら、コンテナへ責務を戻せないか見直す。
- `margin` を残す場合は、なぜ `gap` や空セルではなく `margin` なのかを説明できる状態にする。

## よくある書き換え

### 子要素の `margin` を `gap` に戻す

```css
/* before */
.list > * + * {
  margin-block-start: 1rem;
}

/* after */
.list {
  display: grid;
  gap: 1rem;
}
```

### `margin` で作ったズレを空セルへ戻す

```css
/* before */
.hero-title {
  margin-inline-start: 4rem;
}

/* after */
.hero {
  display: grid;
  grid-template:
    "...   title" auto
    "media body " auto
    / 4rem 1fr;
}
```

## AI 出力の確認項目

- 同一コンテナ内の規則的な間隔を `margin` で作っていないか。
- 共有コンテナを持てるのに、child margin へ責務を逃がしていないか。
- 構造的な空白を `margin` や `padding` でごまかしていないか。
- `gap` と child margin を混在させて、二重の間隔になっていないか。
- `margin` を残す理由が、外部関係か構造制約として説明できるか。

## 出力時の方針

- まずその間隔を `gap`、空セル、`margin` のどれで扱うべきかを明示する。
- 規則的な間隔なら、なぜコンテナ責務として `gap` に戻すべきかを短く説明する。
- 構造的な空白なら、なぜ `margin` ではなく空セルで表すべきかを説明する。
- `margin` を許容する場合は、例外であることと、その理由を明示する。

## 最終チェック

- 規則的な子要素間隔は `gap` で表現できているか。
- 構造的な空白は空セルで表現できているか。
- `margin` を内部レイアウトの主手段にしていないか。
- child margin の連鎖を放置していないか。
- `margin` を残す場合、その理由が外部関係か構造制約として説明できるか。

## 参考資料

- [Promote spacing design using empty grid cells](https://www.tak-dcxi.com/article/promote-spacing-design-using-empty-grid-cells/)
