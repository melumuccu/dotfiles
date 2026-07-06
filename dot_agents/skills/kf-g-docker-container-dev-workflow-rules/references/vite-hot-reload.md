# Vite の hot reload

frontend を Docker 開発環境で動かす場合は、Vite の dev server と hot reload を使う。
production build や static preview を開発用の主経路にしない。

## Compose の基本形

```yaml
services:
  web:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    command: pnpm dev --host 0.0.0.0
```

## Vite 設定ルール

- source directory を container の Vite 実行 directory へ bind mount する
- dev command は Vite dev server を起動する
- container 外の browser からアクセスできるように `--host 0.0.0.0` または `server.host` を設定する
- Vite の dev server port を Compose の `ports` に出す
- source 編集時は Vite HMR で自動反映させる
- proxy、Tailscale、custom domain などで HMR 接続先がずれる場合だけ `server.hmr.host`, `server.hmr.clientPort`, `server.hmr.protocol` を調整する
- file watch が Docker 環境で効かない場合だけ `server.watch.usePolling` や `CHOKIDAR_USEPOLLING=true` を検討する
- 通常の source 編集で container restart や image rebuild を要求しない

## 最終チェック

- frontend 開発では Vite dev server を使っているか
- source directory が container の Vite 実行 directory へ bind mount されているか
- Vite の host、port、HMR が container 外の browser から使えるか
- source 変更だけで rebuild が不要な構成になっているか
