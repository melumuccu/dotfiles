---
name: kf-g-sveltekit-docs
description: Use this skill whenever the task involves SvelteKit-specific behavior such as routing, load functions, form actions, hooks, adapters, page options, environment modules, deployment, or file conventions. Because an official SvelteKit skill is not provided, use the official documentation under https://svelte.dev/docs/kit as the primary source before answering or implementing.
---

# SvelteKit 公式 docs 参照ルール

この skill の目的は、SvelteKit 固有仕様を扱うときに参照先をぶらさないこと。

## 背景

- SvelteKit の skills が公式から提供されていないため、SvelteKit 固有情報は `https://svelte.dev/docs/kit` 配下を一次情報として扱う
- 記憶や Svelte 一般論だけで SvelteKit 固有仕様を断定しない

## 使う場面

- `+page` `+layout` `+server` などのファイル規約
- routing `params` `layout` `error` `loading`
- `load` `actions` `redirect` `error`
- hooks `handle` `handleFetch`
- `ssr` `csr` `prerender` `trailingSlash` などの page options
- adapters deploy build env modules
- `$app/*` `$env/*` `@sveltejs/kit` API

## 基本ルール

1. まずローカル実装と設定を確認する
1. SvelteKit 固有仕様や API が絡む場合は、`https://svelte.dev/docs/kit` 配下の該当ページを確認する
1. 回答や実装では、docs の用語とファイル名をそのまま使う
1. Svelte 一般機能の話なら `svelte-code-writer` や `svelte-core-bestpractices` の skill の参照を優先し、SvelteKit 固有部分だけこの skill で補う
1. Svelte と SvelteKit を混同しない

## 確認対象の目安

- ルーティングなら `Routing` `Advanced routing`
- データ取得なら `Loading data`
- フォーム送信なら `Form actions`
- 実行環境や描画方式なら `Page options`
- サーバ処理なら `Hooks` `Server-only modules`
- 配備なら `Adapters` `Node servers` `Static site generation` `Single-page apps`
- API リファレンスなら `Reference` セクション

## URL一覧 (2026/07/06時点)

- /introduction
- /creating-a-project
- /project-types
- /project-structure
- /web-standards
- /routing
- /load
- /form-actions
- /page-options
- /state-management
- /remote-functions
- /environment-variables
- /building-your-app
- /adapters
- /adapter-auto
- /adapter-node
- /adapter-static
- /single-page-apps
- /adapter-cloudflare
- /adapter-cloudflare-workers
- /adapter-netlify
- /adapter-vercel
- /writing-adapters
- /advanced-routing
- /hooks
- /errors
- /link-options
- /service-workers
- /server-only-modules
- /snapshots
- /shallow-routing
- /observability
- /packaging
- /auth
- /performance
- /icons
- /images
- /accessibility
- /seo
- /faq
- /integrations
- /debugging
- /migrating-to-sveltekit-2
- /migrating
- /additional-resources
- /glossary
- /@sveltejs-kit
- /@sveltejs-kit-hooks
- /@sveltejs-kit-node-polyfills
- /@sveltejs-kit-node
- /@sveltejs-kit-vite
- /$app-env
- /$app-env-private
- /$app-env-public
- /$app-environment
- /$app-forms
- /$app-navigation
- /$app-paths
- /$app-server
- /$app-state
- /$app-stores
- /$app-types
- /$env-dynamic-private
- /$env-dynamic-public
- /$env-static-private
- /$env-static-public
- /$lib
- /$service-worker
- /configuration
- /cli
- /types

## 最終チェック

- SvelteKit 固有仕様を記憶だけで断定していないか
- `https://svelte.dev/docs/kit` 配下を参照すべき論点か見落としていないか
- Svelte 一般論と SvelteKit 固有論が分離できているか
