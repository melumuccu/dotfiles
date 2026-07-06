# Dockerfile のレイヤー見出し

Dockerfile は multi-stage build を前提にする。
各 `FROM ... AS ...` の直前に、次の形式でレイヤー見出しを置く。

```dockerfile
#============================
# Base Layer
#============================
FROM node:24-slim AS base

#============================
# Dependencies Layer
#============================
FROM base AS dependencies
```

## 見出しルール

- `FROM` ごとに見出しを置く
- 見出しは `#============================` で上下を挟む
- 見出し名は `# Base Layer` のように `Layer` で終える
- stage alias は `base`, `dependencies`, `development`, `build`, `runtime` などの小文字名にする
- 必要な stage だけを作る
- build graph と Dockerfile 上の並びを揃える
- 通常の命令ごとには見出しを増やさない

## 標準レイヤー名

- `Base Layer`
- `Dependencies Layer`
- `Development Layer`
- `Build Layer`
- `Runtime Layer`
- `Test Layer`

`Test Layer` は、test 専用 image や CI 用 target が必要な場合だけ使う。

## 最終チェック

- Dockerfile の各 `FROM` にレイヤー見出しがあるか
- Dockerfile が multi-stage build 前提になっているか
- layer 見出しが指定形式に揃っているか
- stage alias が小文字で、役割を表す名前になっているか
