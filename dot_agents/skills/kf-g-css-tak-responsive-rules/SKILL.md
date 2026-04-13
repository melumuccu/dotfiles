---
name: kf-g-css-tak-responsive-rules
description: Use this skill when designing, reviewing, or generating responsive CSS. Apply it whenever the user asks about breakpoints, media queries, container queries, fluid sizing, viewport or container units, or needs to validate responsive component behavior, even if they do not explicitly mention responsive design.
---

# CSS レスポンシブ実装ルール

この skill は、レスポンシブ CSS の判断順序を揃え、不要なブレイクポイントと場当たり的な単位選択を減らすためのものです。
CSS はブラウザへの提案であり、まずは Intrinsic な適応を優先します。

## この skill を使う場面

- 新規に CSS を書くとき
- 既存のレスポンシブ実装をレビューするとき
- Media Queries と Container Queries の使い分けを決めるとき
- `clamp()` や流動値の設計をするとき
- `vw` `vh` `cqi` などの単位選択を見直すとき
- AI が生成した CSS に危ないレスポンシブ実装が混ざっていないか確認するとき

## 最初に決めること

1. その要素は、そもそもレスポンシブにすべきか。
1. クエリなしで成立させられないか。
1. 依存先は親要素の幅か、ビューポート全体か。

## エスカレーション順序

### 0. 静的

- タグ、バッジ、ラベル、アイコン、区切り線、固定サイズのロゴやアバターのように、本質的に小さく固定的な要素はレスポンシブにしない。
- こうした要素へ `clamp()` やクエリを足すのは過剰であり、複雑さだけを増やす。

### 1. Intrinsic

- 最優先で使う。
- `auto` `fit-content` `min-content` `max-content` を使った自然なサイズ決定を優先する。
- `flex-wrap: wrap`、`grid` と `auto-fit` `auto-fill` `minmax()` で自然に折り返す。
- 流動値は `clamp()` `min()` `max()` を使って滑らかに調整する。
- 固定 `width` より `max-inline-size`、固定 `height` より `min-block-size` または `aspect-ratio` を優先する。
- レイヤー構成がある場合は、まずコンポーネント非依存のレイアウト層で解決できないか確認する。

### 2. Container Queries

- 同じコンポーネントが複数の配置先へ再利用されるときに使う。
- サイドバー、カード、モーダル内など、親幅で見え方が変わる要素を対象にする。
- ビューポートではなく、配置先の幅に応じて切り替えたいときに使う。

### 3. Media Queries

- 上位の手法で解決できない場合だけ使う。
- ページ全体のマクロレイアウト変更に使う。
- ビューポートに固定された UI や、ページ全幅でしか成立しないブロックに使う。
- 再配置される可能性があるコンポーネントへ、安易に Media Queries を持ち込まない。

## コンテナクエリの必須ルール

### 名前付きコンテナを必須にする

- `container-name` は必須にする。
- `container-type` 単体ではなく、必ず `container` ショートハンドを使う。
- 名前は必ず dashed ident にし、`--` で始める。

```css
:scope {
  container: --cards / inline-size;
}

@container --cards (inline-size >= calc(420 / 16 * 1rem)) {
  ...
}
```

- 名前なしの `@container (...)` は禁止にする。
- `container: cards / inline-size;` のような `--` なしの名前は使わない。

### 適用箇所を絞る

- コンポーネントルート、または本当に必要なラッパーにのみ付与する。
- とりあえず全体へ `container-type` を付ける運用はしない。
- `:scope` 以外でコンテナを定義する場合は、`.sidebar-container` のように意味が分かるクラス名を使う。
- 汎用ラッパーへ `.container` というクラス名を使わない。
- `html` `body` やページ全体のレイアウト要素へ `container-type` を指定しない。ページレベルは Media Queries で扱う。

### 副作用を前提に設計する

- コンテナ自身は自分の `@container` 条件を参照できない。コンテナは親、切り替えは子で使う。
- `container-type: inline-size` は `contain: inline-size` を伴うため、内容依存で幅が決まる要素へ付けるとサイズ崩壊しやすい。
- `inline` 要素、`fit-content` 依存要素、`flex-grow` `flex-basis` が未調整の flex item、`auto` や Intrinsic な grid item への付与は慎重に扱う。
- コンテナ要素には `padding` や `border` を持たせず、内部レイアウトは子要素へ逃がす。閾値や `cqi` 計算がずれやすいため。
- `subgrid` と併用したい場面では、親をコンテナにし、子の切り替え条件は `calc()` で組む。
- 旧実装が残る環境では `position: fixed` が壊れる可能性があるため、コンテナ内部へ固定配置要素を抱え込ませない。
- `container-type: size` は高さ確定が前提になり扱いにくいため、原則使わない。
- `<source media>` は Container Queries を理解しない。画像ソース切り替えはビューポート基準かマークアップ分岐で扱う。

## ビューポート単位とコンテナ単位

### `vw` と `vh` は禁止

- `vw` と `vh` は使わない。
- 横方向は `svi` `dvi` `lvi`、縦方向は `svb` `dvb` `lvb` を文脈で選ぶ。
- 迷ったら `svi` と `svb` を優先する。
- `dvb` はレイアウトシフトを招きやすいため、必要性が明確な場合だけ使う。
- 常に画面高いっぱいを狙う場合でも、固定 `block-size` より `min-block-size` を優先する。

### ビューポート単位はページ文脈で使う

- ビューポート単位は Media Queries やページレベルの判断と対で使う。
- ページ余白、ヒーロー、全幅背景など、ページ全体に対して成立する値へ使う。
- 再配置されるコンポーネントの `inline-size` `block-size` やフォントサイズを、ビューポート単位だけで決めない。

### `cqi` 系はコンテナ文脈が保証されるときだけ使う

- `cqi` は descendant 側で使い、コンテナ自身の自己サイジングには使わない。
- `cqi` を使うなら、同じコンポーネント内に `container: --name / inline-size` と対応する `@container --name (...)` が存在することを確認する。
- 有効なクエリコンテナが保証できない場所で `cqi` を使わない。未解決時は small viewport ベースへフォールバックして意味が変わるため。
- `cqb` `cqw` `cqmin` `cqmax` は `size` コンテナ前提で扱いにくいため、原則使わない。

### 実装上の補足

- `sv*` `dv*` `lv*` の生値を乱用せず、`%` や Intrinsic なレイアウトで解決できるならそちらを優先する。
- ビューポート単位ベースの流動値を多用する場合は、値を直接散らさずトークンやユーティリティへ寄せる。
- Chrome 145 以降では `scrollbar-gutter: stable` がある環境で `vw` 系の挙動が変わるが、それでも Safari と Firefox を考えると `100vw` は避ける。
- 挙動差が減っても `inline-size: 100vw` は多くの場合不要であり、コードスメルとして扱う。

## クエリの構文ルール

- Media Queries と Container Queries はレンジ構文を使う。
- `min-width` `max-width` のプレフィックス構文は使わない。
- Container Queries の軸は `width` ではなく `inline-size` を使う。

```css
@media (width >= calc(720 / 16 * 1rem)) {
  ...
}

@container --card (inline-size >= calc(420 / 16 * 1rem)) {
  ...
}
```

## レイヤー別の優先手法

- `@layer pages` では Media Queries を優先する。
- `@layer components` では Container Queries を優先する。
- モーダル、トースト、ポップオーバーされた内容のようにビューポート依存が本質なコンポーネントだけ、例外的に Media Queries を使う。

## ブレイクポイントの考え方

### デバイスカテゴリで考えない

- `sp` `tablet` `pc` のようなデバイス起点の分類は使わない。
- `.sp-only` `.pc-only` のような切り替えクラスは作らない。
- ブレイクポイントはコンテンツが破綻する位置で決める。

### `rem` と `calc()` を使う

- ブレイクポイントの単位は `rem` を使う。
- `calc(640 / 16 * 1rem)` のように、px 由来の値は `calc()` で意味を残したまま変換する。
- 閾値はマジックナンバーではなく、列数、最小幅、gap、余白などの成立条件として書く。
- `clamp()` `min()` `max()` の内部も、意味が増えるなら `calc()` で式に分解する。

### クエリ条件内で `var()` を使わない

- `@media` と `@container` の条件式に `var()` を入れない。
- クエリ条件に必要な値は最終的にリテラルで書く。
- カスタムプロパティはプロパティ値の組み立てにのみ使う。

```css
/* 禁止 */
@container --cards (inline-size >= calc(var(--_column-width) * 3)) {
  ...
}

/* 許可 */
@container --cards (inline-size >= calc(160 / 16 * 1rem * 3)) {
  ...
}
```

### AI 出力の確認項目

- 条件式に `var()` が混ざっていないか。
- 閾値がデバイス慣習値ではなく、レイアウト成立条件になっているか。
- gap、列数、padding など必要な要素が式に含まれているか。
- 単に `calc(48rem)` のように包んだだけの偽装 `calc()` になっていないか。

## 流動的なサイジング

- `clamp(min, preferred, max)` を使い、最小値と最大値の間を滑らかに補間する。
- preferred 値は、可読性が重要な箇所では `rem + 相対単位` の合計で作る。
- ページレベルの流動値はビューポート単位、コンポーネントレベルの流動値は `cqi` を使い分ける。
- フォントサイズへ相対単位だけを直接入れない。最小値は必ず `rem` で固定する。

```css
font-size: clamp(
  14 / 16 * 1rem,
  0.00455 * 100svi + 12.18 / 16 * 1rem,
  18 / 16 * 1rem
);
```

- 単位なしトークンを持っている場合は、プロパティ値の中でカスタムプロパティと `calc()` を使って slope と intercept を組み立ててよい。

## レイアウトパターン

### 固定サイズを避ける

- 固定 `width` ではなく `max-inline-size` を使う。
- 固定 `height` ではなく `min-block-size` または `aspect-ratio` を使う。
- 固定値が必要なときは `min(100%, var(--_size))` のようにオーバーフロー防止を先に考える。

### `zoom` は最後の保険

- `zoom` は Intrinsic、Container Queries、Media Queries を試した後でも破綻を避けられない場合だけ使う。
- 想定最小幅が明確なコンポーネントルートに限定して使う。
- クエリコンテナが保証される文脈でのみ使う。
- `zoom` は `1` を上限にし、拡大には使わない。
- 文字サイズをビューポート単位で縮める代替として使わない。
- `progress()` 非対応環境でも読めて操作できる状態を保つ。

## 出力時の方針

- まず 0 から 3 のどこで解くかを明示する。
- Media Queries を入れる場合は、なぜ Intrinsic や Container Queries では足りないのかを説明する。
- Container Queries を入れる場合は、どの要素をコンテナにし、どの子を切り替えるかを明確にする。
- 既存コードや AI 出力に禁止事項がある場合は、単に書き換えるだけでなく、何が危ないのかも短く説明する。
- 既存のレイヤー構成や命名規則がある場合は、それを壊さない。

## 最終チェック

- その要素は本当にレスポンシブ化が必要か。
- Intrinsic な手法を先に試したか。
- 親幅依存とビューポート依存を切り分けたか。
- コンテナは名前付きで、`--` 始まりになっているか。
- `vw` `vh` を使っていないか。
- 条件式に `var()` を入れていないか。
- `sp` `tablet` `pc` のような命名や `.sp-only` `.pc-only` を作っていないか。
- Media Queries は本当にページレベルかビューポート依存の要件か。
- `zoom` を安易な逃げ道にしていないか。

## 参考資料

- [TAK - CSS Responsive Rules](https://gist.github.com/tak-dcxi/acd985cd8b7486a807f1c240731cc7e0)
