---
name: kf-g-css-flex-grid
description: Use this skill when designing, reviewing, or generating CSS layout with display grid or flex. Apply it whenever the user asks about grid-template, grid-area naming, flex-direction, or needs to choose between grid and flex for component or page layout.
---

# CSS Grid / Flex レイアウトルール

この skill は、`display: grid` を第一候補にしつつ、`display: flex` の使いどころを絞り、視覚配置をコードへそのまま写すためのものです。
`grid-template`、空セル、`grid-area` 命名、`flex-direction` の選択を主に扱います。
ブレイクポイント、Container Queries、流体サイズの単位選定は [../kf-g-css-tak-responsive-rules/SKILL.md](../kf-g-css-tak-responsive-rules/SKILL.md) を優先し、`gap` と `margin` の責務分離は [../kf-g-css-spacing-gap-margin-rules/SKILL.md](../kf-g-css-spacing-gap-margin-rules/SKILL.md) を優先します。

## この skill を使う場面

- `display: grid` と `display: flex` のどちらを選ぶか決めるとき
- `grid-template` と `grid-template-areas` のどちらで書くか見直すとき
- `grid-area` の命名ルールを決めるとき
- `flex-direction: column` を使いたくなったとき
- AI が生成した CSS に、場当たり的な `flex` が混ざっていないか確認するとき

## 最初に決めること

1. その要素は本当にレイアウトコンテナにすべきか
1. 視覚配置を `grid-template` でそのまま表現できないか
1. `flex` が必要なのは一列方向の整列だけか
1. レイアウト名と見た目用クラス名を分離すべきか

## 選択順序

### 0. 通常フロー

- 文書フローだけで成立する要素に、安易に `grid` や `flex` を足さない。
- 見出し、本文、単純な縦積みが自然に流れるなら、まず通常フローのままで良い。

### 1. Grid

- セクション、カード、メディアオブジェクト、フォーム、情報パネルのように、行と列の関係で考えたほうが自然なレイアウトでは `grid` を第一候補にする。
- 見た目を図として説明したくなるなら、まず `grid-template` で書けないか考える。
- 要素を縦に積みたいだけに見える場面でも、`gap`、開始位置、将来の並び替えを考えると `grid` のほうが崩れにくいことが多い。
- `flex-direction: column` を書きたくなったら、先に `display: grid` へ置き換えられないか確認する。

### 2. Flex

- `flex` は横一列の整列、両端寄せ、中央寄せ、折り返し可能な軽い並びに限定して使う。
- 代表例は、ボタン群、チップ列、ツールバー、ナビゲーション、インライン方向の操作群である。
- `flex` を選ぶ理由は、一方向の分配や整列で十分だからであり、二次元の配置や空白の設計が主題になった時点で `grid` に戻す。
- `flex-direction: column` は原則使わない。縦積みは `grid` と `gap` で解く。

## Grid のルール

### `grid-template` を最優先にする

- レイアウトを組むときは、まず `grid-template` で視覚的に表現できないか考える。
- `grid-template-areas` より `grid-template` を優先する。エリア名とトラックサイズを同じ場所に書けるため、見た目と実装の対応が崩れにくい。
- 行文字列の中では、スペースを使ってカラムが視覚的に整列するように書く。
- 行と列のサイズを別宣言へ分散させず、読んだ瞬間に構造が分かる形を優先する。

```css
.feature {
  display: grid;
  gap: 1rem 1.5rem;
  grid-template:
    "...     title" auto
    "media   body " auto
    "media   meta " auto
    / 12rem 1fr;
}
```

### 空のグリッドセルを使う

- 空白がレイアウトの一部なら、空のグリッドセルを積極的に使う。
- 空のグリッドセルは必ず `...` の 3 つのドットで表現する。
- 空セルは余白の代用品ではなく、構造を明示するために使う。
- `gap` と `margin` の使い分けは [../kf-g-css-spacing-gap-margin-rules/SKILL.md](../kf-g-css-spacing-gap-margin-rules/SKILL.md) を参照する。

### `grid-area` 名は `[grid-area]` で持つ

- class 名をそのまま `grid-area` 名のソースにしない。
- class は見た目や責務に対するセレクタとして使い、レイアウト上の面名は `[grid-area]` 属性へ分離する。
- `[grid-area]` の値は、見た目ではなくレイアウト上の役割で命名する。
- BEM 名や装飾クラスを、そのまま面名へ流し込まない。
- 共通 rule を置くなら、`*` ではなく `:where([grid-area])` に限定する。
- `[grid-area]` へ限定した共通 rule のパフォーマンス懸念は小さい。属性セレクタの一致対象が絞られ、`grid-area` 自体も grid item にしか効かないためである。
- ただし、`attr()` を `content` 以外で使う typed syntax は互換性がまだ揃っていない。基礎 CSS に入れる場合は、対応ブラウザが保証される案件か、`@supports` 付きのプログレッシブエンハンスメントに限る。

```html
<section class="feature">
  <h1 class="feature-title" grid-area="title">タイトル</h1>
  <div class="feature-media" grid-area="media">...</div>
  <p class="feature-body" grid-area="body">...</p>
</section>
```

```css
@supports (grid-area: attr(grid-area type(<custom-ident>), auto)) {
  :where([grid-area]) {
    grid-area: attr(grid-area type(<custom-ident>), auto);
  }
}
```

- 面名の責務を class から切り離しておくと、見た目のクラス名変更でレイアウト定義まで巻き込まれにくい。
- Safari や Firefox まで広く保証したい案件では、この共通 rule を前提にせず、個別の `grid-area` 宣言をフォールバックとして持つ。

## Flex のルール

### `flex-direction: column` は使わない

- 縦方向に積みたいだけなら、`grid` と `gap` を使う。
- 縦積みの並びに対して `flex-direction: column` を入れると、将来の行列化、開始位置調整、空白の設計が窮屈になりやすい。
- カード本文、フォーム要素群、説明文リスト、メディアの下に続くテキスト群は、まず `grid` で考える。

```css
.stack {
  display: grid;
  gap: 0.75rem;
}
```

### `flex` は横一列の整列に絞る

- 一列方向の配列と分配だけで十分なら `flex` を使ってよい。
- 横並びで `justify-content`、`align-items`、`flex-wrap` を使いたい場面は `flex` が自然である。
- ただし、折り返した後の行同士の関係や列方向の揃いまで気になり始めたら `grid` へ戻す。

```css
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
```

## よくある書き換え

### `flex-direction: column` を `grid` に置き換える

```css
/* before */
.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* after */
.card {
  display: grid;
  gap: 1rem;
}
```

## AI 出力の確認項目

- `grid-template` で書けるのに、`grid-template-areas` と行列定義が分かれていないか。
- 空セルが `.` になっていないか。必ず `...` になっているか。
- 行文字列のスペースが崩れていて、列の対応が読み取りにくくなっていないか。
- `grid-area` 名を class 名から流用していないか。
- `grid-area` の共通 rule を `*` へ当てていないか。`[grid-area]` へ限定しているか。
- typed `attr()` を使う前提なのに、対応ブラウザや `@supports` を無視していないか。
- `flex-direction: column` を惰性で使っていないか。
- `flex` で二次元レイアウトを無理に組んでいないか。

## 出力時の方針

- まず `grid` と `flex` のどちらを選ぶか、その理由を一文で明示する。
- `grid` を選ぶ場合は、`grid-template` で視覚構造を先に示す。
- `flex` を選ぶ場合は、一方向の整列だけで十分な理由を示す。
- `flex-direction: column` を置き換える場合は、なぜ `grid` のほうが自然なレイアウトモデルかを短く説明する。
- `[grid-area]` を使う場合は、class とレイアウト名の責務分離を明示する。
- `[grid-area]` の共通 rule を使う場合は、パフォーマンスより互換性が論点であることと、`[grid-area]` 限定かどうかを明示する。
- 間隔責務が論点なら [../kf-g-css-spacing-gap-margin-rules/SKILL.md](../kf-g-css-spacing-gap-margin-rules/SKILL.md) を併用する。

## 最終チェック

- 通常フローで足りる要素に `grid` や `flex` を足していないか。
- 視覚配置を `grid-template` で表現できるのに、別の書き方へ逃げていないか。
- 空セルは必ず `...` で書かれているか。
- 列が読み取りやすいよう、行文字列のスペースが整列しているか。
- `grid-area` 名は `[grid-area]` へ分離されているか。
- typed `attr()` を使う共通 rule は `:where([grid-area])` へ限定し、`@supports` か対応ブラウザ保証の条件があるか。
- `flex` は横一列の整列に限定されているか。
- `flex-direction: column` を使っていないか。

## 参考資料

- [Promote spacing design using empty grid cells](https://www.tak-dcxi.com/article/promote-spacing-design-using-empty-grid-cells/)
