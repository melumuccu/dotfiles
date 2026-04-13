---
name: kf-g-css-tak-typography
description: Use this skill when designing, reviewing, or generating CSS for typography in Japanese or multilingual interfaces. Apply it for font family, text wrapping, kerning, line height, fluid type, truncation, manual line breaks, and related text layout decisions.
---

# CSS タイポグラフィ実装ルール

この skill は、tak-dcxi の Typography gist をもとに、日本語中心または多言語 UI のタイポグラフィ実装判断を揃えるためのものです。
kiso.css を採用している前提で整理し、未採用の場合は必要な reset を `@layer reset` へ移植する前提で使います。

## この skill を使う場面

- `font-family` や `font-weight` の方針を決めるとき
- 日本語と英語が混在する見出しや本文の折り返しを設計するとき
- `text-wrap`, `font-kerning`, `font-feature-settings`, `text-autospace` などの使い分けを決めるとき
- `line-height`, `text-box-trim`, `hanging-punctuation`, `line-clamp` をレビューするとき
- `clamp()` を使った流体タイポグラフィや `px` / `rem` の使い分けを決めるとき
- 手動改行、文節改行、分離禁止のような文章組版の細部を扱うとき
- AI が生成した文字組み CSS に危ない指定が混ざっていないか確認するとき

## 前提

- リセット CSS には kiso.css を採用している前提で考える
- kiso.css を採用していない場合は、`overflow-wrap`, `line-break`, `text-autospace`, `text-spacing-trim`, 日本語向けの `font-style` リセットなど、必要な reset を `@layer reset` へ移植する
- `hyphens`, `font-kerning`, `text-wrap`, 日本語向けの例外処理は `lang` 属性が付いていることを前提にする
- 日本語本文はベタ組みを優先し、見出しや短文だけを例外的に締める

## 最初に決めること

1. そのテキストは本文か、見出しか、UI ラベルか
1. 主言語は日本語か、英語か、混在か
1. ベタ組みを優先すべきか、見出しの引き締めを優先すべきか
1. そのルールは `@layer reset`, `@layer base`, `@layer utilities` のどこへ置くべきか
1. ユーザーの文字拡大設定に追従すべき値か、装飾として固定すべき値か

## レイヤー別の責務

### `@layer reset`

- ルートの折り返し指定は reset で済ませる
- `text-autospace` と `text-spacing-trim` は reset で全体方針を敷く
- 日本語の `em`, `cite`, `dfn` などの斜体解除も reset で扱う

### `@layer base`

- 言語別の既定 `font-kerning` は base に置く
- 見出しの `font-feature-settings: "palt"` や英語見出しの `text-wrap: balance` は base で与える
- 既定の `line-height` や太字トークンも base でそろえる

### `@layer utilities`

- opt-in なユーティリティだけを置く
- 代表例は `-fluid-text`, `-text-center`, `-trim-both`, `-kerning`, `-auto-phrase`, `-hanging`, `-tabular-nums`, `-uppercase`, `-hyphens`, `-line-clamp`, `-br`, `-wbr` である

## 実装ルール

### `font-family`

- 特別な指定が無い場合、日本語 UI では `font-family: sans-serif` のみで良い
- 日本語環境では `system-ui` を安易に使わない。Windows では游ゴシック系 UI 書体が前に出やすく、意図しない見た目になりやすい
- Tailwind CSS など、未設定時に `system-ui` が入る仕組みは必ず点検する
- Noto Sans JP や Noto Serif JP を全端末で強制する要件があるときは、`@font-face` でローカルフォントを優先し、二重読み込みを避ける
- 明朝体は Android で欠落している場合があるため、デバイス依存の前提で組まない

### `font-style` と `font-weight`

- 日本語では `em`, `cite`, `dfn`, `i`, `address` の斜体を前提にしない
- kiso.css を使わない場合は `:lang(ja)` に限定して斜体解除と `em` の太字化を reset で補う
- `font-weight` はキーワードより数値指定を優先し、`--font-bold: 700` のようなトークンに寄せる
- kiso.css 側がキーワード指定を持っている場合は、base レイヤーで数値へ上書きする

### 折り返しと揃え

- ルートには `overflow-wrap: anywhere` と `line-break: strict` を前提にする
- `text-align: center` を使う場合は `text-wrap: balance` をセットで考える
- `text-align: justify` は原則禁止にする。英語混在時の破綻リスクが大きい
- 英語本文は `text-wrap: pretty`、英語見出しは `text-wrap: balance` を基本にする
- 日本語本文には `text-wrap` を基本入れない。ベタ組みを崩しやすいため
- 日本語見出しは `word-break: auto-phrase` と `text-wrap: balance` の組み合わせを第一候補にし、対応ブラウザだけへ段階適用する
- Safari では日本語の `text-wrap: pretty` が崩れやすいため、現状では避ける
- 段落の rag を少し整えたい場合だけ `inline-size: round(down, 100%, 1ic)` を検討する

### 文字詰めと OpenType 機能

- `:lang(en)` には `font-kerning: normal` を与える
- `:lang(ja)` には `font-kerning: none` を既定にし、日本語本文のベタ組みを優先する
- ただしこの方針は、日本語文中の英単語もカーニングされなくなるトレードオフを含む。欧文の見え方を優先する案件では例外を検討する
- 見出しやキャプションには `font-kerning: normal` を与える
- 日本語見出しには `font-feature-settings: "palt"` を使う。縦書きでは `vpal` を使う
- `font-feature-settings: "pwid"` を使う場面では、上位互換の `font-variant-east-asian: proportional-width` を優先する
- 数字を揃えたい UI では `font-variant-numeric: tabular-nums` を使う

### 余白処理と行間

- `text-autospace: normal` を全体方針にする
- `pre`, `time`, `input`, `textarea`, `[contenteditable]` には `text-autospace: no-autospace` を明示する
- `text-spacing-trim: trim-start` を既定にし、`pre` だけ `space-all` を明示する
- 既定の `line-height` は 1.5 以上にする
- `line-height` は unitless number を使い、トークン化する
- 本文の目安は和文 1.7 から 2、英文 1.5 から 1.8、見出しの目安は和文 1.25 から 1.5、英文 1.2 から 1.4
- `line-height: 1` は禁止にする。ハーフレディングを消したいなら `text-box-trim` / `text-box-edge` を検討する
- `text-box-trim` はプログレッシブ・エンハンスメントとして使う。英語では `text-box-edge: cap alphabetic`、日本語では既定値 `text` を優先する
- 厳密に詰めたい場合だけ `margin-block: calc((1em - 1lh) / 2)` を追加検討する

### 約物、省略、ハイフネーション

- `hanging-punctuation` は段落でのみ使う
- 約物ぶら下げは水平スクロールを誘発しうるため、インライン方向の余白とセットで設計する
- 英語では `hanging-punctuation: first allow-end last`、日本語では `last allow-end` を基準にする
- `line-clamp` はプレフィックス付きで実装する。`display: -webkit-box` と `-webkit-box-orient` と `-webkit-line-clamp` をセットにする
- 省略時のオーバーフロー制御は `overflow: hidden` ではなく `overflow-block: clip` を第一候補にする
- フォールバックでは `overflow-y: clip` を使う。`overflow: hidden` は `sticky` や約物ぶら下げを壊しやすい
- `hyphens: auto` は `lang="en"` などの言語明示がある時だけ使う
- 大文字化はセレクタへ直書きせず、`text-transform: uppercase` のユーティリティで扱う

### 注釈、文節改行、手動改行

- 通常の Web 段落で字下げを前提にしない
- 注釈は `role="note"` を付け、`text-indent: hanging 1ic` を使う
- `word-break: auto-phrase` は日本語見出し、キャプション、短文などに限定する
- 日本語段落全体へ文節改行を広げない。空きが不自然になりやすい
- Firefox や Safari でも文節改行が必須なら BudouX を検討する
- 意味的な改行以外で `<br>` を増やさない
- 日本語の見出しだけ改行位置を制御したい時は、`display: contents` と `display: inline flow-root` / `block flow` を使って CSS で改行させる
- 段落の手動改行はレスポンシブと相性が悪いので避ける
- 分離させたくない語は `&zwj;` で結び、意図を明示する

### 流体タイポグラフィと単位選択

- `font-size` をクエリで刻む前に `clamp()` を検討する
- 計算過程が消える外部ジェネレーター依存は避け、式が残る形で管理する
- API 的なカスタムプロパティと内部計算用のカスタムプロパティは分離する
- ページ全体に対して滑らかに変えるなら `100svi`、コンポーネントローカルで変えるなら `100cqi` を使う
- `100cqi` は有効なコンテナが保証される場合だけ使う。単位判断はレスポンシブ skill の規約も参照する
- `rem` と `px` は役割で使い分ける
- フォントサイズ、行間、段落の縦余白、文字を含む幅、ブレイクポイントは `rem` / `em` を優先する
- 境界線幅や細部装飾、文字サイズと連動して大きくなってほしくない値は `px` を検討する
- `rem` を使うならブラウザの文字拡大機能を有効にして検証する
- `:root { font-size: 10px; }` のような固定化は避ける

## 推奨ベース実装

```css
:where(:lang(en)) {
  font-kerning: normal;
}

:where(:lang(ja)) {
  font-kerning: none;
}

:where(h1, h2, h3, h4, h5, h6, caption) {
  font-kerning: normal;

  &:lang(en) {
    text-wrap: balance;
  }

  &:lang(ja) {
    font-feature-settings: "palt";

    @supports (word-break: auto-phrase) {
      word-break: auto-phrase;
      text-wrap: balance;
    }
  }
}

:where(p:lang(en)) {
  text-wrap: pretty;
}
```

## 推奨ユーティリティ

```css
.-fluid-text {
  --_u-relative-max-width: var(--fluid-text--relative-max-width, 1280);
  --_u-relative-min-width: var(--fluid-text--relative-min-width, 375);
  --_u-min-font-size: var(--fluid-text--min-font-size, 14);
  --_u-max-font-size: var(--fluid-text--max-font-size, 16);
  --_u-base-font-size: var(--fluid-text--base-font-size, 16);
  --_u-relative-unit: var(--fluid-text--relative-unit, 100svi);

  --_u-fluid-slope: calc(
    (var(--_u-max-font-size) - var(--_u-min-font-size)) /
      (var(--_u-relative-max-width) - var(--_u-relative-min-width))
  );
  --_u-fluid-intercept: calc(
    var(--_u-min-font-size) - var(--_u-fluid-slope) *
      var(--_u-relative-min-width)
  );

  font-size: clamp(
    var(--_u-min-font-size) / var(--_u-base-font-size) * 1rem,
    var(--_u-fluid-slope) * var(--_u-relative-unit) + var(--_u-fluid-intercept) /
      var(--_u-base-font-size) * 1rem,
    var(--_u-max-font-size) / var(--_u-base-font-size) * 1rem
  );
}

.-text-center {
  text-align: center;
  text-wrap: balance;
}

.-trim-both {
  text-box-trim: trim-both;

  &:lang(en) {
    text-box-edge: cap alphabetic;
  }
}

.-kerning {
  font-kerning: normal;

  &:lang(ja) {
    font-feature-settings: "palt";
  }
}

.-auto-phrase {
  &:lang(ja) {
    @supports (word-break: auto-phrase) {
      word-break: auto-phrase;
      text-wrap: balance;
    }
  }
}

.-hanging {
  hanging-punctuation: last allow-end;

  &:lang(en) {
    hanging-punctuation: first allow-end last;
  }
}

.-tabular-nums {
  font-variant-numeric: tabular-nums;
}

.-uppercase {
  text-transform: uppercase;
}

.-hyphens {
  hyphens: auto;
}

.-line-clamp {
  display: -webkit-box;
  overflow-block: clip;
  -webkit-box-orient: block-axis;
  -webkit-line-clamp: var(--line-clamp--limit, 3);

  @supports not (overflow-block: clip) {
    overflow-y: clip;
  }
}

.-br {
  display: contents;

  &:lang(ja) {
    display: block flow;
  }
}

.-wbr {
  display: contents;

  &:lang(ja) {
    display: inline flow-root;
  }
}
```

## 出力時の方針

- まず対象テキストが本文か見出しか、主言語が何かを明示する
- kiso.css が吸収する reset と、今回追加する base / utilities を切り分けて説明する
- `font-kerning`, `text-wrap`, `text-box-trim`, `word-break: auto-phrase` を使う場合は、ブラウザ差分とトレードオフを短く添える
- `line-clamp`, 手動改行、注釈の字下げでは、必要なら CSS だけでなくマークアップ要件も併記する
- `rem` と `px` を選ぶ時は、文字拡大に追従すべきかどうかを判断理由として示す

## 最終チェック

- `lang` 属性が付いているか
- kiso.css を使っているか、未採用なら必要な reset を移植したか
- 日本語 UI で `system-ui` を安易に使っていないか
- `text-align: center` と `text-wrap: balance` を切り離していないか
- 日本語本文へ `text-wrap` を入れていないか
- `line-height: 1` を使っていないか
- `line-clamp` で `overflow: hidden` を安易に使っていないか
- `hyphens: auto` に言語明示があるか
- 手動改行を段落へ持ち込んでいないか
- `rem` と `px` の使い分けに理由があり、文字拡大で検証したか

## 参考資料

- [TAK - Typography](https://gist.github.com/tak-dcxi/0f8b924d6dd81aaeb58dc2e287f2ab3a)
