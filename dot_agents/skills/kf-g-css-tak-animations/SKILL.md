---
name: kf-g-css-tak-animations
description: UI animations necessity judgment, recommendations for motion design, implementation strategies, and performance/accessibility reviews. Targets include hover, active, focus, popover, tooltip, dropdown, dialog, tab, segmented control, card, button, toast, accordion, carousel, scroll-linked animation, View Transitions, and more.
---

# Animations Skill

以下のようなタスクでこの Skill を使うこと。

- UI にアニメーションを追加する
- モーションデザインの品質をレビューする
- hover, popover, tooltip, dropdown, dialog, tab, segmented control, card, button, toast, accordion, scroll-linked animation, View Transitions などの動きを改善する
- アニメーションを削除すべきか判断する
- property, easing, duration, transform-origin などを選定する
- `prefers-reduced-motion` を尊重すべきかどうかを判断する
- `@starting-style`, `transition-behavior`, `interpolate-size` などの出現・退場アニメーション手法を選定する
- `@keyframes` の命名規則・スコープ管理・API 的カスタムプロパティ設計を行う

---

## 基本原則

1. アニメーションは目的ではなく手段である
2. そのアニメーションが「機能的」か「装飾的」かを常に区別する
3. 最良のアニメーションは「アニメーション無し」である場合もある
4. UI の動きは速く、応答的に感じられるべきである。ユーザーが求めているのは「すぐ反応した」という知覚速度である
5. 高頻度で操作される UI では装飾的なアニメーションを避ける
6. イージングはアニメーションにおいて最重要である。同じ duration でもイージング次第で体感速度は大きく変わる
7. 視覚変化はトリガーとの因果関係が感じられるべきである
8. 複数の視覚変化を同期させたい場合、個別の `transition` では不十分なことがある。`@keyframes` animation、Web Animations API、あるいは CSS トランジションと `transition-behavior` の組み合わせなど、適切な手法を選ぶこと
9. アニメーションはパフォーマンスに大きく影響する
10. アクセシビリティのため、`prefers-reduced-motion` を尊重しているユーザーにどう見せるかを常に考える

## 必須の評価順序

### Step 1: そのアニメーションは必要か？

必ず次を確認する。

- この動きは何の問題を解決するのか
- 状態、因果関係、フィードバックを明確にしているか
- 機能的なのか、装飾的なのか
- ユーザーはどれくらい頻繁にこれを見るのか
- キーボード操作や高速操作の邪魔にならないか

#### 判断基準

| 目的                               | 判断               | 例                                             |
| ---------------------------------- | ------------------ | ---------------------------------------------- |
| 状態遷移の因果関係を示す           | 必要               | アコーディオン開閉、タブ切替                   |
| ユーザーの注意を新出要素に誘導する | 必要               | toast 通知、バリデーションエラー               |
| 操作のフィードバックを返す         | 必要               | ボタンの `:active`、チェックボックスのチェック |
| 空間的連続性を保つ                 | 条件付き           | ページ遷移の View Transitions、ドリルダウン    |
| ブランド個性の表現                 | 低頻度 UI のみ許容 | LP のヒーロー、初回訪問のオンボーディング      |
| 単に見た目の華やかさ               | 高頻度 UI では不要 | ダッシュボードのカードがスライドして現れるなど |

強い理由がない場合は、削除を提案すること。

### Step 2: どの実装形が適切か？

#### Step 2A: イージング・タイミングの選定

**イージング**

- `ease-in` 系や `linear` 系は物理的に不自然で機械的な印象を与えがちである。`linear` は一定速度を表現したい連続運動（marquee やプログレスバー）にのみ適用する。
- 出現・退場では `ease-out` 系を使用する
- すでに画面上にあるものの移動では `ease-in-out` 系を使用する
- CSS 標準のイージングキーワード（`ease`, `ease-in-out` など）はメリハリが弱い。プロジェクトにアニメーショントークンがある場合はそれを参照し、`quint` 系か `expo` 系のイージングを使用する
  - トークンが存在しない場合は以下を推奨する

```css
/* ease-out 系（出現・退場向き） */
--ease--out-quint: cubic-bezier(0.22, 1, 0.36, 1);
--ease--out-expo: cubic-bezier(0.16, 1, 0.3, 1);

/* ease-in-out 系（移動向き） */
--ease--in-out-quint: cubic-bezier(0.86, 0, 0.07, 1);
--ease--in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
```

- 全てのプロパティに同一の `transition-duration` と `transition-timing-function` を適用するのは雑である。プロパティごとにカーブを選び分けること

**タイミング**

- 原則として機能的なアニメーションの duration は `300ms` 以下とする
- 例外: dialog, drawer, sheet など大型 UI の遷移は `300ms〜500ms` を許容する
- 日常的に何十回も触る UI では、1 回あたり `100ms` の差でも体感負荷が大きくなる

#### Step 2B: transform-origin と空間的整合性

- `transform-origin` は常にトリガーとの位置関係を考慮して設定する
- Popover はトリガー要素を起点として拡大・縮小させる。デフォルトの `center` は多くの場合に不適切である
  - CSS Anchor Positioning を使用している場合は、Popover の配置方向に応じて `transform-origin` を動的に切り替えることを検討する
- `scale: 0` からのスケールインは物理的に不自然である。「そこにあったものが少し離れた位置から立ち上がる」ほうが自然であるため、要素のサイズに応じた起点値を選ぶこと

| 要素種別              | スケールイン起点 |
| --------------------- | ---------------- |
| tooltip, popover      | `0.95〜0.98`     |
| dropdown menu         | `0.92〜0.96`     |
| dialog, drawer, sheet | `0.85〜0.92`     |

#### Step 2C: インタラクション種別ごとの指針

**ホバー**

- ホバーの視覚変化は `150ms〜200ms` を目安とする
- タッチデバイスでは hover が存在しないため、`@media (any-hover: hover)` で切り分けることを検討する
  - カレントリンクなど `href` が存在しないアンカーリンクでホバーが起こるのは避ける。必ず `:any-link:hover` のように定義すること
  - 有効ではないボタンでホバーが起こるのは避ける。必ず `:enabled:hover` のように定義すること

**active（押下フィードバック）**

- ボタン等の押下時に `scale: 0.96〜0.98` 程度の短い縮小を挟むことで、押下されたことへの物理的なフィードバックを提示する
- duration は `100ms〜150ms` を目安とする
- あくまで押下が伝わることが重要な UI でのみ適用する

**focus / keyboard**

- キーボード操作中に視覚的な移動やハイライトにアニメーションがあると、入力と表示がズレて感じられ、反応が遅く見える
- キーボード操作時のアニメーションは厳禁とする
- `:not(:focus-visible)` 内で `transition` や `animation` を定義し、キーボードフォーカス時にはアニメーションが適用されないようにする

**tooltip**

- ホバーの誤作動を防ぐため、初回表示は `300ms〜500ms` 遅延させる
- 連続操作時（Warm Up 中）は `0ms〜50ms` で即時表示する
- 離脱後のクールダウンは `300ms〜500ms` で、この間に別のトリガーに触れた場合は即時表示を継続する

**出現・退場（display の切替を伴う場合）**

- `display: none` から表示状態へのアニメーションには `@starting-style` で初期スタイルを定義し、`transition-behavior: allow-discrete` で `display` や `overlay` をトランジション可能にする
- Popover API（`[popover]`）や `<dialog>` のアニメーションでは、この手法を第一候補とする
- `@starting-style` は詳細度を生成しないことを留意する
- `display: none` への `transition` は Firefox、`@keyframes` 内の `display` は Safari で動作しない。前者はプログレッシブ・エンハンスメントとして許容する

**高さのアニメーション（accordion 等）**

- `height: auto` へのアニメーションには `interpolate-size: allow-keywords` の使用を検討する
- Safari、Firefox でも動作するようにオーダーを受けた場合には、CSS Grid の `grid-template-rows: 0fr / 1fr` パターンにフォールバックする
- layout を起こすアニメーションであるため、パフォーマンスに注意するが、アコーディオンの用途では許容する

**scroll-linked animation**

- 実装の優先順位
  1. CSS scroll-driven animations（`animation-timeline`, `view-timeline` 等）
  2. `IntersectionObserver` による状態トグル + CSS transition/animation
  3. 本当に必要な場合に限って JS で毎フレーム同期
- `scrollTop` を毎フレーム読んでアニメーションを駆動している実装には必ず警告すること
- Scroll-driven animations を使う判断基準
  - スクロール位置に連動して連続的に変化する値がある場合 → CSS scroll-driven animations
  - 要素がビューポートに入った/出たタイミングで 1 回だけ状態変化する場合 → `IntersectionObserver`
  - スクロール量に応じて複雑なロジック分岐が必要な場合 → JS（ただし `requestAnimationFrame` で制御する）
- `IntersectionObserver` による状態トグルで発火させる場合は、`animation-fill-mode: both` と `animation-play-state: paused` を組み合わせた初期非表示パターンを使う

```css
.reveal {
  animation-name: --fade-in, --translate-from;
  animation-duration: 600ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
  animation-play-state: paused;

  /* アクティブ時に発火 */
  &[data-revealed="true"] {
    animation-play-state: initial;
  }
}
```

- `animation-fill-mode: both` により、`paused` 状態でも keyframes の `from` フレームが適用される。これにより要素は keyframes 上の開始地点（例: `opacity: 0`, `translate: 0 20px`）で描画される
- アクティブ化（属性付与等）で `animation-play-state` を `initial`（= `running`）に戻すだけでアニメーションが発火する
- この手法の利点は、初期の非表示状態のために `opacity: 0` 等を別途記述する必要がないこと。アニメーションの開始地点がそのまま初期表示となるため、keyframes を単一の情報源（single source of truth）として扱える
- `@media (prefers-reduced-motion: reduce)` では `animation-play-state` の制御ごと無効化するか、アニメーションをフェードのみに簡素化すること

**View Transitions**

- View Transitions を扱うときは次を分けて考えること
  - スナップショットの視覚アニメーション（見た目の動き）
  - 実際のレイアウト変化（DOM の差分）
- SPA では `document.startViewTransition()` を、MPA では `@view-transition` at-rule を使用する
- `view-transition-name` の命名は CSS カスタムプロパティの命名規則に準じる

#### Step 2D: `@keyframes` の命名と設計

`@keyframes` はグローバルスコープで動作するため、命名と管理に厳格なルールを設けること。

詳細なパターンとコード例は [`reference/keyframes.md`](./references/keyframes.md) を参照すること。

**必須ルール**

1. keyframes 名は必ず dashed ident（`--` で始まる名前）にする
2. グローバル keyframes は `base/keyframes.css` に集約する
3. コンポーネント固有の keyframes は `--{component-name}--{animation-name}` の形式で命名し、そのコンポーネントの CSS 内に定義する
4. 条件によってアニメーションの起点・方向を変えたい場合は、API 的カスタムプロパティを keyframes 内に定義し、利用側から値を注入する

**設計原則**

5. グローバル keyframes はユーティリティクラスのように扱う。1 keyframes = 1 プロパティの変化に限定し、`animation-name` のカンマ区切りで組み合わせる
6. グローバル keyframes は `from` / `to` の 2 フレームで完結するものに限定する。中間フレームを含む keyframes はコンポーネントなどのローカルとして定義する
7. 自明な `from` や `to` は省略する。省略されたフレームには要素の現在値が使われるため、カスケーディングに沿った自然なアニメーションになる。値をハードコードすると、要素の現在値が想定と異なる場合にジャンプが発生する

```css
/* グローバル keyframes（base/keyframes.css に配置） */
@keyframes --scale-from {
  from {
    scale: var(--scale-from--x-value, 1) var(--scale-from--y-value, 1);
  }
}

/* 利用側: カスタムプロパティで起点を注入 */
[popover] {
  --scale-from--x-value: 0.96;
  --scale-from--y-value: 0.96;

  animation-name: --scale-from;
  animation-duration: 200ms;
  animation-timing-function: var(--ease--out-quint);
  animation-fill-mode: both;
}
```

**その他**

- `animation-fill-mode` を明示する場合は `both` を第一候補とすることを推奨する

### Step 3: パフォーマンスは適切か？

#### 基本的なレンダリングコスト判断

必ず次の観点で考えること。

- layout / paint / composite のどれを起こすか
- main thread と compositor thread のどちらが関与するか

#### プロパティの選定

| 優先度   | 手法                                                                                                                                                                        | 備考                                         |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| 高       | compositor で処理される `transform`, `opacity`, 一部の `filter`, 一部の `clip-path`, CSS scroll-driven animations                                                           | GPU 合成のみで完結                           |
| 中       | JS から `transform` / `opacity` を更新する実装、FLIP パターン                                                                                                               | main thread が関与するが layout/paint は最小 |
| 低       | paint を起こすプロパティ（`background-color`, `box-shadow` 等）                                                                                                             | 描画コストは面積に依存。ホバーなどでは許容する                       |
| 避ける   | layout を起こすプロパティ（`width`, `height`, `padding`, `inset` 等）                                                                                                       | accordion 等やむを得ない場合を除く           |
| リスク大 | 大きい半径の `blur()` / `backdrop-filter`、巨大な composited layer、グローバル CSS カスタムプロパティの毎フレーム更新、`scrollTop` を毎フレーム読む scroll-linked animation |                                              |

#### `filter` / `backdrop-filter` の注意

- `filter` はハードウェアアクセラレーションされる場合があっても、コストが低いわけではない
- `backdrop-filter` は `filter` よりもさらに高コストになり得る。背面の描画面積全体を再描画するためである
- 以下のケースは逆効果になり得るので避けること
  - 大きい blur 半径
  - 広い描画面積（`backdrop-filter` は特に注意）
  - アニメーション中のレイヤー
  - 複数の重なったエフェクト

#### カスタムプロパティの更新

- グローバルに適用されるカスタムプロパティを毎フレーム更新してはいけない
- 可能な限りローカルスコープのカスタムプロパティを更新する
- 継承が行われると連鎖的に計算が走るため、`@property` で `inherits: false` を設定して継承をオフにする
- DOM 全体が必要としていない値を継承させないこと

#### `will-change` の扱い

- `will-change` はアニメーション開始直前に付与し、完了後に除去するのが原則である
- 常時指定は逆効果になり得る（GPU メモリの浪費、合成レイヤーの不要な生成）
- 原則的に`will-change` は使用せず、どうしても必要な場合のみ JS で取り除く処理を必須としつつ使用すること

#### `contain` の活用

- 必要に応じて `contain: content` を指定してレイアウト・描画・スタイル計算の影響範囲を限定する。ただし機械的に指定するのではなく、以下の副作用には注意する必要がある
  - 内包される `position: fixed` はトップレイヤーを除いて `absolute` のように扱われる
  - オーバーフローがクリップされる
  - スタッキングコンテキストが生成される

#### `transition-property` の `all` 指定は厳禁

- 関係ないプロパティにも適用され、意図しない動きや無駄にパフォーマンスを下げる要因になる
- 必ず必要なプロパティだけを明示すること

#### `transform` の独立プロパティ

- 差分の明確化とコードの読みやすさを優先して独立プロパティ（`translate`, `rotate`, `scale`）を使用する
- ただし、以下のケースでは `transform` を使用してよい
  - 独立プロパティの実行順序（translate → rotate → scale）では都合が悪い場合
  - `skew()` を使用する場合
  - 独立プロパティではかえって読みにくくなる 3D 系の複合指定の場合

### Step 4: アニメーションの中断・キャンセル

操作中にアニメーションが完了する前に次のインタラクションが発生した場合の挙動を考慮すること。

#### 判断基準

| 状況                   | 推奨挙動                                 | 実装手法                                                                                                |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| hover → 即 unhover     | 中間状態から逆再生                       | CSS `transition`                                                                                        |
| dialog 開く → 即閉じる | 中間状態から退場アニメーション開始       | `@starting-style` + `transition` なら自動。`@keyframes` の場合は `animation-fill-mode` と JS 制御が必要 |
| タブ切替の連打         | 即座に切り替え、アニメーションをスキップ | `animation: none` の強制リセット、または View Transitions の `skipTransition()`                         |
| スクロール方向の急変   | 現在位置から新しい方向に即追従           | CSS scroll-driven animations なら自動追従                                                               |

#### 原則

- CSS `transition` は中間状態からの逆再生が自動で行われるため、中断が頻発する UI では `transition` を優先する
- `@keyframes` animation は中断制御が難しいため、中断が想定される UI では避けるか、Web Animations API で `cancel()` / `reverse()` を使う
- 高速連打される UI（タブ、セグメンテッドコントロール等）では、アニメーションそのものを短くする（`100ms〜150ms`）か、スキップする仕組みを入れる

### Step 5: `prefers-reduced-motion` を尊重しているか？

#### 段階的な対応方針

全てのアニメーションを一律に無効化するのではなく、段階的に対応すること。

| 対応レベル | 内容                                                          | 対象例                                                                                |
| ---------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 無効化     | `@media (prefers-reduced-motion: no-preference)` 内でのみ定義 | パララックス、自動ループカルーセル、marquee、`transform` 系の scroll-linked animation |
| 簡素化     | 動きを crossfade やフェードのみに置き換え                     | ページ遷移の View Transitions、大型 UI の出現・退場                                   |
| 短縮       | duration を大幅に短縮（`50ms` 以下）                          | tooltip/popover のフェードイン                                                        |
| 維持       | 変更不要                                                      | スピナー、プログレスバー、フォーカスリングの表示                                      |

#### 「大きな変動」の判断基準

以下のいずれかに該当する場合は「大きな変動」とみなし、無効化または簡素化する。

- 画面の 1/3 以上を占める要素の移動
- 回転を伴う動き
- ズーム（`scale` の変化量が `0.5` 以上）
- スクロールに連動する `transform` 系のアニメーション
- 視覚的に揺れる、振動する動き

#### 注意

- 装飾的なアニメーションはフェードイン・フェードアウト以外は全て `@media (prefers-reduced-motion: no-preference)` 内で定義すること
- 機能的なアニメーションであっても、「大きな変動」に該当する場合は簡素化を行うこと

### Step 6: リスクの最終確認

全ての Step を通過した後、最終チェックとして次を確認する。

- [ ] duration が長すぎないか（機能的なら原則 `300ms` 以下、大型 UI でも `500ms` 以下）
- [ ] イージングが弱すぎないか（CSS 標準キーワードのまま放置していないか）
- [ ] `transform-origin` がトリガーと合っているか
- [ ] 物理的に不自然なアニメーションになっていないか（`scale: 0` からなど）
- [ ] キーボード操作にモーションを入れていないか
- [ ] 複数の視覚変化がズレていないか
- [ ] 初回のみ遅延し、その後は即時にすべき UI ではないか（tooltip 等）
- [ ] 中断・キャンセル時の挙動は考慮されているか
- [ ] パフォーマンス（layout/paint の最小化、`transition-property: all` の不使用、`will-change` の適切な管理）
- [ ] `prefers-reduced-motion` を尊重しているユーザーにとって適切か
- [ ] scroll-linked animation で初期非表示が必要な場合、`animation-fill-mode: both` + `animation-play-state: paused` パターンを使い、keyframes 外に `opacity: 0` 等を二重定義していないか
- [ ] `@keyframes` は dashed ident で命名されているか、スコープと配置場所は適切か

## 返答フォーマット

### 新規アニメーション提案時

1. **判断**: 必要 / 不要（判断マトリクスの根拠を示す）
2. **分類**: 機能的 / 装飾的
3. **動き方**: easing / duration / property / transform-origin
4. **実装方針**: CSS のみ（`transition` or `@keyframes` or `@starting-style`）/ CSS + JS / Web Animations API / FLIP
5. **keyframes 設計**（`@keyframes` 使用時）: 命名（dashed ident）/ スコープ（グローバル or コンポーネント固有）/ API 的カスタムプロパティの要否
6. **中断時の挙動**: 逆再生 / スキップ / 不要
7. **reduced-motion 対応**: 無効化 / 簡素化 / 短縮 / 維持
8. **リスク**: アクセシビリティ、繰り返し利用時の摩擦、視覚的不整合、パフォーマンス

### 既存コードの修正提案時

1. **判断**: 維持 / 修正 / 削除
2. **理由**: UX 上の目的と利用頻度
3. **修正内容**: 具体的な変更箇所とコード例
4. **リスク**: 修正による副作用

### 性能レビュー時

1. **分類**: layout / paint / composite
2. **リスク**: 低 / 中 / 高
3. **理由**: invalidation の経路と関与スレッド
4. **より安全な代替案**: `transform` / `clip-path` / observer / ローカル変数 / `@property` など
5. **ブラウザ注意点**: Chrome 固有最適化、Safari / Firefox の差異

## 参考資料

- [TAK - Animations Skill](https://gist.github.com/tak-dcxi/b1870cfe73e3089a1e4aa7da19c3374a)
