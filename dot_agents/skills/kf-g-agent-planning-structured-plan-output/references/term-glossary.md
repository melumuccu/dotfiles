# フットノート語彙リスト

基準: **標準的 IT エンジニアなら初出説明不要** かどうか。

迷ったら「読者がその計画のドメイン外か」で判断。ドメイン外なら初出フットノート。

## 判定早見

| 信号 | フットノート |
|------|-------------|
| 汎用言語 / FW / ツール名 | 不要 |
| HTTP / DB / Git / CI の一般語 | 不要 |
| ベンダー製品の固有名詞・独自概念 | 推奨 |
| 同一ベンダー内でもニッチな内部用語 | 推奨 |
| 計画の主題ドメインの専門語 | 推奨 |

## フットノート不要 (例)

ユーザー指定 + 拡張。初出でも平文。

### 開発基盤

`git`, `branch`, `merge`, `rebase`, `commit`, `PR`, `issue`, `worktree`, `monorepo`, `semver`

### 言語 / FW / ランタイム

`JavaScript`, `TypeScript`, `Node.js`, `React`, `Svelte`, `SvelteKit`, `Vue`, `Next.js`, `pnpm`, `npm`, `ESM`, `CJS`

### Web / API

`HTTP`, `HTTPS`, `REST`, `GraphQL`, `WebSocket`, `SSE`, `JSON`, `YAML`, `OpenAPI`, `CORS`, `cookie`, `session`, `JWT`, `OAuth`, `middleware`, `webhook`

### データ

`SQL`, `PostgreSQL`, `SQLite`, `MySQL`, `Redis`, `ORM`, `migration`, `upsert`, `snapshot`, `storage`, `cache`, `index`, `transaction`, `CRUD`, `WAL`

### インフラ / 運用 (一般)

`Docker`, `container`, `CI/CD`, `GitHub Actions`, `deploy`, `build`, `runtime`, `environment variable`, `load balancer`, `TLS`, `DNS`, `CDN`

### アーキテクチャ (一般)

`frontend`, `backend`, `SSR`, `CSR`, `SSG`, `API gateway`, `microservices`, `idempotency`, `retry`, `timeout`, `circuit breaker`

### 品質

`unit test`, `integration test`, `E2E`, `linter`, `formatter`, `ESLint`, `Prettier`, `refactoring`, `dependency`

## フットノート推奨 (例)

製品固有・ニッチ・計画外読者向け。初出に footnote。

### Cloudflare

| 用語 | 補足の方向性 |
|------|-------------|
| Durable Object | 状態付きシングルインスタンス実行 |
| Workers KV | エッジ KV、 eventual consistency |
| R2 | S3 互換オブジェクトストレージ |
| D1 | エッジ SQLite |
| Queues | メッセージキュー |
| Cron Triggers | Workers 定期実行 |
| Smart Placement | バックエンド近接実行 |
| isolation group | DO 配置単位 |
| hibernation | DO アイドル退避 |
| eviction | インスタンス / キャッシュ破棄 |
| Durable Objects alarm | DO 内スケジュールコールバック |

### AWS / GCP / Azure (代表)

| 用語 | 補足の方向性 |
|------|-------------|
| Lambda@Edge | CloudFront 連動エッジ関数 |
| Fargate Spot | 中断可能タスク課金 |
| ECS task definition | コンテナ起動定義 |
| IAM permission boundary | 権限上限 |
| Cloud Run request-based billing | リクエスト課金モデル |
| Azure Functions consumption plan | 従量プラン |

### データ / 分散 (ニッチ)

| 用語 | 補足の方向性 |
|------|-------------|
| MVCC | 多版同時実行制御 |
| serializable isolation | 最強分離レベル |
| advisory lock | アプリ協調ロック |
| outbox pattern | イベント配信整合 |
| saga pattern | 分散トランザクション補償 |
| CRDT | 衝突自由複製データ型 |
| hot row | 更新集中行 |

### セキュリティ / ネットワーク

| 用語 | 補足の方向性 |
|------|-------------|
| mTLS | 相互 TLS |
| Zero Trust | 境界less 認可モデル |
| WAF custom rule | アプリ層フィルタ |
| split-horizon DNS | 内部外部で異なる解決 |

### SvelteKit / ランタイム (ややニッチ)

| 用語 | 補足の方向性 |
|------|-------------|
| remote function | SvelteKit 2.20+ RPC 的関数 |
| `+page.server.ts` load | サーバ専用データ取得 (初出のみ、SvelteKit 計画なら省略可) |
| `$app/server` | サーバ専用 import |

### GitHub / 運用 (ややニッチ)

| 用語 | 補足の方向性 |
|------|-------------|
| ruleset bypass actor | 保護ルール例外主体 |
| merge queue | 順次マージキュー |
| required reviewers | 必須レビュア設定 |

### アーキテクチャ / 運用 (計画の主題)

| 用語 | 補足の方向性 |
|------|-------------|
| cold start | サーバレス / エッジ初回起動遅延 |
| connection pooling | DB 接続再利用 |
| CQRS | コマンドとクエリの責務分離 |
| event sourcing | 状態をイベント列で保持 |
| backpressure | 下流処理能力に合わせた流量制御 |
| sticky session | LB 配下で同一クライアントを固定サーバへ |
| blue-green deployment | 2 環境切替による無停止デプロイ |
| canary release | 一部トラフィックのみ新版本へ |
