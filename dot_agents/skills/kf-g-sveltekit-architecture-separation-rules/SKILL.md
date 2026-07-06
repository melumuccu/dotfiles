---
name: kf-g-sveltekit-architecture-separation-rules
description: Use this skill when designing, reviewing, or editing SvelteKit route architecture, separation of concerns, UI component placement, +page.svelte/+page.server.ts responsibilities, or $lib/server service/model layering. Apply it whenever the user mentions SvelteKit component splitting, route-local components, shared components, load/actions, database access, external APIs, auth checks, business logic placement, frontend/backend boundaries, or MVC-like layering.
---

# SvelteKit 関心分離ルール

この skill は、SvelteKit の画面、ルート処理、サーバ処理を混ぜないための設計規約。
`kf-g-sveltekit-docs` を公式仕様の参照元にし、この skill では repo で使う責務分離の判断を固定する。

## 使う場面

- SvelteKit の画面構成を設計する
- `+page.svelte` と `+page.server.ts` の責務を分ける
- `load` や `actions` に書く処理量を判断する
- DB アクセス、外部 API、認証、ビジネスロジックの置き場所を決める
- route-local component と shared component の配置を決める
- SvelteKit の既存実装をレビューし、責務の混線を直す

## 読み進め方

1. SvelteKit のファイル規約、`load`、`actions`、server-only modules の仕様が絡むなら、先に `../kf-g-sveltekit-docs/SKILL.md` を読む
1. `.svelte` component や Svelte 5 の書き方が絡むなら、`../svelte-core-bestpractices/SKILL.md` も読む
1. CSS layout や UI 用語の責務境界が主論点なら、該当する CSS / design-system 系 skill を併用する
1. この skill では、公式仕様そのものではなく、実装上の責務分離を判断する

## 黄金律

SvelteKit のファイル名は責務境界として扱う。
迷ったら、`+page.server.ts` を薄い仲介役にし、実処理を `$lib/server` へ寄せる。

| 場所 | 位置づけ | やること | 避けること |
| --- | --- | --- | --- |
| `+page.svelte` | View | データ表示、フォームやボタンなどのユーザー操作の検知、局所 UI state | API 通信、DB アクセス、認証判定、長い計算、ビジネスルール |
| `+page.server.ts` | Controller | `load`、`actions`、入力の受け取り、サービス呼び出し、`redirect` / `error` / `fail`、画面へ返す形への整形 | DB クエリ直書き、外部 API 直叩き、重いビジネスロジック、複数画面で再利用される処理 |
| `$lib/server/` | Model / Service | DB アクセス、外部 API 連携、認証チェック、ビジネスルール、永続化、トランザクション境界 | browser から使う component や client module への依存 |

## `+page.svelte` のルール

- 画面は `data`、props、局所 state を表示する場所
- ユーザー操作は検知してよい
- フォーム送信は SvelteKit の `actions` へ流す
- 複雑な加工は、`load` 前の service か小さな pure helper に寄せる
- `$lib/server`、private env、DB client を import しない
- fetch や外部 API 呼び出しを直接書かない

許容する処理:

- 表示用の軽い整形
- 入力欄の開閉、選択状態、ソート表示などの UI state
- `use:enhance` などの progressive enhancement
- 子 component への props 受け渡し

## `+page.server.ts` のルール

`+page.server.ts` は、画面と server service の交通整理に徹する。
長くなったら「処理をここで実行している」のではなく「ここから呼んでいる」形に戻す。

書いてよい処理:

- `load` と `actions`
- `params`、`locals`、`request`、`formData` の受け取り
- 最低限の入力検証と型変換
- `$lib/server` の service 呼び出し
- `redirect`、`error`、`fail` による SvelteKit 境界処理
- 画面が必要とする戻り値への薄い整形

避ける処理:

- SQL や ORM query の直書き
- 外部 API client の直書き
- 認可ルールや料金計算などの業務判断
- 複数 route で再利用されそうな処理
- テストしたい中心ロジック
- 巨大な `actions` 分岐

判断基準:

- その処理を unit test したいなら `$lib/server` へ移す
- route が変わっても使いそうなら `$lib/server` へ移す
- DB、外部 API、private env、認証状態を読むなら `$lib/server` を第一候補にする
- `+page.server.ts` には「どの service を呼び、SvelteKit とどう接続するか」だけを残す

## `$lib/server/` のルール

`$lib/server/` は server-only なアプリケーション中核。
UI や route file から独立させ、テストしやすい関数として切る。

置くもの:

- DB repository や query helper
- 外部 API client
- 認証、認可、権限チェック
- ビジネスルール
- 保存、更新、削除、トランザクション処理
- 複数 route で共有する server-side use case

分け方の目安:

- `src/lib/server/<domain>/service.ts`: 画面や use case から呼ばれる業務処理
- `src/lib/server/<domain>/repository.ts`: DB の読み書き
- `src/lib/server/<domain>/schema.ts`: server-side の入力検証や永続化用 schema
- `src/lib/server/<provider>/client.ts`: 外部 API client

例外:

- 1 route だけで使う小さな server-only helper は、同じ route 配下の `*.server.ts` でもよい
- ただし、その helper が育ったら `$lib/server` へ移す

## コンポーネント配置ルール

コンポーネントは「どこで使うか」で置き場所を決める。
すべてを `src/lib/components` に集めない。

### Route-local component

配置:

- `src/routes/<route>/ComponentName.svelte`
- 数が増える場合は `src/routes/<route>/components/ComponentName.svelte`

置くもの:

- その route だけで使う表示部品
- その画面固有のフォーム、一覧、ヘッダー、フィルター
- route の `data` 型や画面固有の props に強く依存する UI

避けること:

- 他 route から import しない
- 汎用ボタンやダイアログを route-local に閉じ込めない
- server-only module を import しない

### Shared component

配置:

- `src/lib/components/ComponentName.svelte`
- UI 種別や domain ごとに必要なら `src/lib/components/<group>/ComponentName.svelte`

置くもの:

- 複数 route で使う UI
- Button、Dialog、Navigation、FormField などの再利用部品
- design system に近い component
- route に依存しない表示 component

避けること:

- 特定 route の `data` 前提を持ち込まない
- `src/routes/...` から import しない
- `$lib/server` を import しない
- 画面固有の business workflow を混ぜない

## Import 方向

依存方向は一方向に保つ。

```text
+page.svelte
  -> route-local components
  -> $lib/components

+page.server.ts
  -> $lib/server/<domain>

$lib/server/<domain>
  -> DB / external API / auth / domain rules
```

禁止する依存:

- `$lib/components` から `src/routes/...`
- browser で動く code から `$lib/server`
- `$lib/server` から `.svelte` component
- shared component から route-local component

## レビュー観点

SvelteKit の実装を見たら、次を確認する。

- `+page.svelte` に API 通信、DB、認証、業務判断が混ざっていないか
- `+page.server.ts` が service 呼び出しより実処理で膨らんでいないか
- DB、外部 API、認証、ビジネスルールが `$lib/server` にあるか
- その画面だけの component が route 配下に colocate されているか
- 複数画面で使う component が `$lib/components` にあるか
- shared component が route 固有の型や server-only code に依存していないか
- import 方向が一方向か

## 実装時の出力方針

- 責務分離を直した場合は、何を `+page.svelte`、`+page.server.ts`、`$lib/server`、component へ分けたかを短く説明する
- 公式仕様が論点なら `kf-g-sveltekit-docs` の確認結果に基づいて書く
- 小さな画面では、過剰な抽象化より薄い controller と明確な service 関数を優先する
- 既存のディレクトリ構成がある場合は、その構成を尊重する

## 最終チェック

- `+page.svelte` が View として読めるか
- `+page.server.ts` が Controller として読めるか
- `$lib/server` が server-only の Model / Service として読めるか
- route-local component と shared component の置き場所が用途で分かれているか
- client code から server-only code へ import していないか
- SvelteKit 固有仕様を記憶だけで断定していないか
