# 開発環境の source mount

開発環境では、source directory をコンテナへ bind mount する。
source を編集するたびに image を再構築する構成にしない。

## Compose の基本形

```yaml
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    command: pnpm dev
```

## mount ルール

- 開発用 service は `development` などの dev target を使う
- repository root または対象 package directory を、container の `WORKDIR` へ bind mount する
- `node_modules` など container 内で install する依存 directory は、anonymous volume か named volume で host 側と分離する
- source だけの変更で `docker compose build` が必要にならない構成にする
- rebuild が必要なのは Dockerfile、base image、package manager 設定、依存関係、OS package を変えた場合に限る

## 最終チェック

- 開発用 service が dev target を使っているか
- source directory が container の作業 directory へ bind mount されているか
- dependency directory が host mount で壊れないよう分離されているか
- source 変更だけで rebuild が不要な構成になっているか
