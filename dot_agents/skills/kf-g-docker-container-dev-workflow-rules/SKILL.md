---
name: kf-g-docker-container-dev-workflow-rules
description: Use this skill when creating or reviewing Docker container development setup, Dockerfiles, Compose files, or Vite dev servers in this repository. Apply the local rules for multi-stage layer comment blocks, bind-mounted source directories, and Vite hot reload; use it alongside docker-expert because these conventions supplement docker-expert.
---

# Docker Container 開発ワークフロー規約

この SKILL.md は入口として扱い、詳細は `references` 配下の該当ファイルを読む。
`docker-expert` にある一般的な Docker 最適化、security hardening、Compose 設計は重複して書かない。
この skill は、そこに明記されていないローカル規約だけを補完する。

## 使う場面

- Dockerfile を作成、修正、review する
- Docker Compose の開発環境を作成、修正、review する
- devcontainer や Docker Compose で frontend 開発環境を作る
- Vite の dev server をコンテナ内で動かす
- source 編集がコンテナへ反映されない問題を直す

## 読み進め方

1. Dockerfile を扱うなら [dockerfile-layer-headings.md](references/dockerfile-layer-headings.md) を読む
1. 開発環境の source mount を扱うなら [development-source-mount.md](references/development-source-mount.md) を読む
1. Vite の dev server や hot reload を扱うなら [vite-hot-reload.md](references/vite-hot-reload.md) を読む
1. frontend の Docker 開発環境では、source mount と Vite hot reload の両方を確認する

## 参照ファイル

- [dockerfile-layer-headings.md](references/dockerfile-layer-headings.md): multi-stage Dockerfile のレイヤー見出し規約
- [development-source-mount.md](references/development-source-mount.md): 開発環境の source mount 規約
- [vite-hot-reload.md](references/vite-hot-reload.md): Vite dev server と hot reload 規約

## 共通チェック

- Dockerfile が multi-stage build 前提になっているか
- 開発用 service が dev target を使っているか
- source directory が container の作業 directory へ bind mount されているか
- frontend 開発では Vite dev server を使っているか
- source 変更だけで rebuild が不要な構成になっているか
