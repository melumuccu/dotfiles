# devcontainer と mise

devcontainer は**オプション**。ルール適用表で **適用** と確定した場合のみ実装する。デフォルトは devcontainer なしで、ローカル + `mise.toml` を正本とする。

## 1. devcontainer（オプション）

- ルール適用表で devcontainer が **適用** のときだけ `.devcontainer/devcontainer.json` を作る。
- **不適用** のときは devcontainer 関連ファイルを作らない。README もローカル + `mise` 前提で書く。
- runtime や package manager の版管理は devcontainer 内に分散させず、原則 `mise.toml` を正本にする。
- devcontainer を使う場合は `mise install` を実行して、PJ が要求する tool 群を揃える。
- `postCreateCommand` や同等の初期化処理は、`mise install` と `mise run` を中心に組む。
- apt, brew, curl などで個別に runtime を入れるのは、mise で扱えない OS パッケージに限る。

## 2. user settings の dev.containers・dotfiles 設定を先に確認する（devcontainer 適用時）

devcontainer を **適用** する場合のみ実施する。

- まず user settings.json の `dev.containers.*`, `dotfiles.*` を確認する。
- 既に user settings にある値は、devcontainer 側へ重複して書かない。
- 特に `dev.containers.defaultExtensions` に含まれる拡張は、PJ 固有の理由がない限り `.devcontainer/devcontainer.json` の `customizations.vscode.extensions` へ重複追加しない。
- `dev.containers.copyGitConfig` のような user 方針も、PJ 側で上書きが必要なときだけ明示する。
- override が必要な場合は、なぜ user 設定ではなく PJ 側に置くのかを説明できる状態にする。
- `dotfiles.repository` で指定されたリポジトリの dotfiles は devcontainer 内で常に効く前提で、PJ 固有の devcontainer 設定を考える。

## 3. mise をフル活用する

`mise.toml` は単なる version 指定ファイルとしてではなく、PJ の開発基盤の中心として扱う。

必須方針:

- `[tools]` で runtime と主要 CLI を管理する。
- `[env]` で PJ 固有の環境変数を管理する。
- `[tasks]` で install / dev / check / test / build / lint / format などの日常コマンドを管理する。
- コマンド実行は `mise run <task>` または `mise exec -- <command>` を優先する。
- README や devcontainer（利用時）の手順も `mise` ベースで統一する。
- CI でもローカルと同じ `mise` task 名を使い、コマンド定義を二重化しない。

活用観点:

- runtime の version は `[tools]` に寄せる。
- `.env` 読み込みが必要なら `[env]` の `_.file` を使う。
- `node_modules/.bin` や独自 bin を通したいなら `[env]` の `_.path` を使う。
- 必須 secret や接続先は `required = true` で明示する。
- OS 依存や install 順依存がある tool は `os` と `depends` を使って `mise.toml` に閉じ込める。

## 4. devcontainer と mise の役割分担（devcontainer 利用時）

- devcontainer は「実行場所」を揃える（利用時のみ）。
- mise は「PJ が必要とする tools / env / tasks」を揃える。
- 同じ version 情報を Dockerfile と `mise.toml` の両方に持たない。
- Dockerfile へ version を直書きするのは、base image の都合で避けられない場合だけにする。
- 日常コマンドは shell script の散在より `mise run` を優先する。

## 5. サンプルファイルを初期ファイルの起点にする

- `references/sample-files/` 配下は、新規 PJ に置く設定ファイルのサンプルとして扱う。
- 生成対象と同じ相対パスや同じファイル名のサンプルがある場合は、まずその内容を読む。
- サンプルがあるファイルは、ゼロから書き起こさず、サンプルを起点に PJ 固有の値だけ調整する。
- サンプルの内容と本文ルールが食い違う場合は、本文ルールを優先し、必要ならサンプル側の更新も検討する。
- サンプルがないファイルは、承認済みルールの参照ファイルに従って新規作成する。
