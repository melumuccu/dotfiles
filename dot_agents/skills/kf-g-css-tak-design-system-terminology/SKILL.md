---
name: kf-g-css-tak-design-system-terminology
description: Use this skill when defining, reviewing, or correcting design system terminology for CSS, layout, components, and UI concepts. Apply it when names may conflict with Web standards, HTML semantics, or responsibility boundaries.
---

# デザインシステム用語ガイドライン

この skill は、デザインシステムや UI 実装で使う名称を、Web 標準と責務境界に沿って揃えるためのものです。
命名を見た目や慣習で決めず、HTML と CSS の意味、責務、再利用契約、適用範囲に基づいて判断します。

## この skill を使う場面

- デザインシステムや UI ライブラリの正式名称を決めるとき
- `Container` `Wrapper` `Block` `Text` のような曖昧語が混ざっている設計や文書を見直すとき
- `Link` と `Button`、`Navigation` と `Menu`、`Pattern` と `Component` と `Template` を切り分けるとき
- レイアウトラッパー、余白、列構造、テキスト種別の命名を整理するとき
- 用語集、実装ガイド、Figma 名称、CMS 名称、レビューコメントを統一するとき

## 最初に確認すること

1. その語は Web 標準で意味が確立しているか
1. その名前は見た目ではなく責務を表しているか
1. それは構造か、挙動か、再利用単位か、ページ描画定義か、外観差分か
1. 単一ソースで管理される再利用契約を持つか
1. ページ全体に適用される上位定義か

情報が足りず、上の判定ができない場合だけ、次を短く確認すること。

- 実体はどの HTML 要素か
- 状態変化や JavaScript を伴うか
- 単一の定義から再利用されるか
- ページ全体の描画定義か、局所的な UI 断片か

## 最重要方針

- 用語は既存の Web 標準と矛盾させない
- 見た目ではなく責務で命名する
- 構造、挙動、再利用単位、ページ描画定義、テーマを混同しない
- 広すぎる総称を正式名称にしない
- 名前で設計境界と再利用条件が分かるようにする

## 用語の基準

### Element

- HTML 要素そのもの、または HTML 要素に直接対応する最小単位を指す
- HTML 要素の総称は `Element` を優先する
- すべての要素を `Block` `Module` `Widget` と呼ばない

### Section

- ページ内の意味的または構造的な区画を指す
- `section` 要素が第一候補だが、文脈に応じて `article` などを使ってよい
- 内容幅ラッパーの意味で `Section` を使わない

### Container

- CSS の `container` 系プロパティが適用された要素だけを指す
- `section container` のように関連対象とセットで呼ぶ
- 内容幅制御のための構造ラッパーを `Container` と呼ばない

### Inner / Outer

- `Inner` は内容幅制御や中央寄せを担う内側ラッパーを指す
- `Outer` は外部余白、周辺配置、周囲との関係調整を担う外側ラッパーを指す
- `Inner / Outer` は単体で万能ラッパー名にせず、`section inner` `card outer` のように関連対象とセットで扱う
- `Inner / Outer` をコンテナクエリ対象の概念と混同しない

### Gutter

- コンテンツ外縁とビューポート端のあいだを保護するインライン方向の余白を指す
- 値はトークン化し、Section ごとの場当たり的な padding 調整に置き換えない
- 列間や要素間の空きを `Gutter` と呼ばない

### Gap

- Flex、Grid、Multi-column などにおける子要素間の間隔を指す
- 行間、列間、カード間、チップ間の距離は `gap` の概念で扱う
- 通常フローの `margin` を `Gap` と呼ばない

### Columns / Flex Columns / Grid / Row

- `Columns` は CSS Multi-column Layout による列配置だけを指す
- Flexbox による列配置は `Flex Columns` と呼ぶ
- CSS Grid Layout による構造配置は `Grid` と呼ぶ
- `Row` は親レイアウト文脈で成立する配置結果であり、独立した要素名として定義しない

### Paragraph / Rich Text

- 単一段落、または単一のテキストブロックは `Paragraph` と呼ぶ
- 複数のインライン装飾や複数種の子要素を内包する編集領域は `Rich Text` と呼ぶ
- 単一段落、インラインテキスト、長文編集領域をまとめて `Text` と呼ばない

### Link / Button

- `<a>` を用いる要素は `Link` と呼ぶ
- `<button>` と `<input type="submit">` `<input type="button">` `<input type="reset">` は `Button` として扱う
- ボタンのように見えるだけでは `Button` と命名しない
- `<a role="button">` は境界ケースとして `Button` に近いが、原則としてその実装自体を避ける
- ARIA role は正式名称の第一決定要因にしない

### Navigation / Menu

- サイト内やアプリ内の移動導線は `Navigation` と呼ぶ
- 必要なら `Primary Navigation` `Footer Navigation` `Local Navigation` のように責務を補う
- コマンド実行や操作選択の UI は `Menu` と呼ぶ
- サイト導線を `Menu` と呼ばず、操作メニューを `Nav` とも呼ばない

### Template / Pattern / Component / Dynamic Element / Theme

- `Template` はページレベル、または同等の上位単位に適用される描画定義を指す
- `Pattern` は静的で再利用可能な表示断片を指し、動的データや条件ロジックを前提にしない
- `Component` は単一ソースから管理され、差し替え可能な入力点を持つ再利用単位を指す
- `Dynamic Element` は JavaScript や状態遷移を伴う挙動中心の UI を指し、`Component` と排他的ではない
- `Theme` は共有アーキテクチャの上に乗る見た目、トークン、タイポグラフィ、色、余白、既定レイアウトの差分を指す
- 静的断片を `Template` と呼ばず、単なる複製物を自動的に `Component` と見なさず、アーキテクチャそのものを `Theme` と呼ばない

## 非推奨語

### Block

- `display: block` などの既存意味と衝突しやすく、一般総称として曖昧すぎる

### Wrapper

- 何の責務を持つラッパーかを表さない
- 幅制御なら `Inner`、外部関連型レイアウトなら `Outer` を優先する

### Text

- 単一段落、インラインテキスト、長文編集領域を区別できない

### Widget / Module

- 責務範囲が曖昧で、設計境界を表しにくい

## 推奨対応表

| 用途 | 推奨語 | 非推奨語 |
| --- | --- | --- |
| HTML 要素の総称 | Element | Block, Module, Widget |
| セクション境界 | Section | Group |
| CSS の container 機能を持つ要素 | Container | Generic container, Wrapper |
| 内容幅ラッパー | Inner | Container, Wrapper |
| 外部関連型レイアウト用ラッパー | Outer | Wrapper |
| 外縁保護余白 | Gutter | Padding, Column gutter |
| 要素間余白 | Gap | Gutter |
| Multi-column による列配置 | Columns | Flex Columns, Grid Columns |
| Flex による列配置 | Flex Columns | Columns |
| Grid による構造配置 | Grid | Columns, Grid Columns |
| 単一段落 | Paragraph | Text |
| 長文編集領域 | Rich Text | Text |
| `<a>` | Link | Button, Link Button |
| `<button>` | Button | Link Button |
| サイト導線 | Navigation | Menu |
| 操作メニュー | Menu | Nav |
| 静的再利用断片 | Pattern | Template |
| ページ描画定義 | Template | Pattern |
| 再利用契約を持つ単位 | Component | Static copy |
| 挙動中心 UI | Dynamic Element | Component の一括呼称 |
| 外観差分 | Theme | Architecture |

## 判定フロー

1. その語は Web 標準で意味が定まっているか確認する
1. 見た目起点の名前になっていないか確認する
1. 静的な表示断片か、動的 UI かを切り分ける
1. 単一ソースで再利用契約を持つなら `Component` を検討する
1. ページ単位かつ条件付きの描画定義なら `Template` を検討する
1. それ以外は `Element` `Section` `Pattern` など、より狭い語へ落とし込む

## ドキュメント運用ルール

- すべての正式用語に、何を指すか、何を指さないか、どこで使うか、どこでは使わないかを定義する
- UI ラベルと正式名称は、可能な限り一致させる
- 用語の追加や変更は単なる表記修正ではなく、互換性変更として扱う
- 俗称を許容する場合でも、正式名称を別に定義する

## 出力時の方針

- まず対象を `Element` `Section` `Container` `Inner` `Outer` `Gutter` `Gap` `Columns` `Flex Columns` `Grid` `Paragraph` `Rich Text` `Link` `Button` `Navigation` `Menu` `Pattern` `Component` `Dynamic Element` `Template` `Theme` のどれで扱うか明示する
- 既存名称を否定する場合は、何が危ないかを短く示す。観点は Web 標準との衝突、見た目起点、責務の曖昧さ、設計境界の不明瞭さ
- `Container` を内容幅ラッパーに使っている場合は `Inner` への置き換えを優先する
- `Wrapper` `Block` `Text` のような曖昧語は、より責務が明確な語へ分解して提案する
- `Pattern` `Component` `Template` のどれかで迷う場合は、動的データ、入力点、単一ソース管理、ページ全体適用の有無で切り分ける

## 最終チェック

- その名前は HTML と CSS の既存意味に矛盾していないか
- その名前は見た目ではなく責務を表しているか
- 構造、挙動、再利用単位、ページ描画定義、テーマを混同していないか
- 再利用条件と管理単位が名前から分かるか
- 広すぎる総称を正式名称にしていないか
- UI ラベル、実装名、ドキュメント名のズレを放置していないか
- 用語変更の影響範囲を確認しているか

## 参考資料

- [TAK - Design System Terminology Guideline](https://gist.github.com/tak-dcxi/6608f35343e2b411d591dc28795ebae0)
