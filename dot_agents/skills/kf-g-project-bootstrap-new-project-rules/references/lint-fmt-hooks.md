# linter / formatter と編集後 hooks

本節の焦点は、特定の AI 製品を固定することではない。
**編集後 lint/fmt の自動実行**を新規 PJ の必須要件として組み込むこと。

## linter / formatter の扱い

- frontend では Oxlint / Oxfmt を基本推奨とする。
- Oxlint / Oxfmt が PJ の言語・ライブラリ・フレームワークに未対応の場合は、その時点のデファクトスタンダードを調査して推奨する。
- frontend 以外は PJ ごとに選定する。言語・FW・既存 toolchain に合わせる。
- 設定ファイル名・設定値の固定例は skill 本文に書かない。
- PJ で lint / format コマンドを決め、`package.json` scripts と `mise run` task の両方に載せる。
- lint / format の日常実行入口は `mise run` に集約する。CI でも同じ task 名を使えるようにし、コマンド定義を二重化しない。
- 初回のリポジトリ全体一括 format / lint fix はしない。hooks は編集されたファイルだけを処理する。

## ignore の扱い

- 各 linter / formatter が `.gitignore` を自動尊重する前提で設計する。
- `.gitignore` の内容を hooks や設定へ重複列挙しない。
- hooks 側で `.gitignore` を動的パースする必要は原則なし。
- 追加除外が必要な場合のみ、各ツールの ignore 設定を使う。これは PJ 判断。

## 編集後 lint/fmt hooks

新規 PJ では **project 単位** で編集後 lint/fmt を走らせる。

配置:

- リポジトリ内の project hooks 設定と実行スクリプトを置く。
- user / global 設定への依存は標準にしない。

トリガー:

- 必須: AI エージェントによるファイル編集後（after agent edit）
- 任意: Tab（インライン補完）によるファイル編集後（after tab edit）。利用中ツールが該当 hook を提供する場合のみ設定。未提供なら省略可
- 1 本の共通スクリプトを両トリガーで共用してよい
- 実行 cwd は project root 前提

ツール非依存の要件（実装は PJ が選ぶ AI エディタ / エージェントの hooks 機能に合わせる）:

- hook 入力から編集対象 `file_path` を取得する
- PJ で定義した lint / format コマンドをそのファイルに対して実行する
- 対象外拡張子は no-op
- fail-open（編集フローを止めない）
- 結果はログで確認可能にする

記述方針:

- 特定 AI 製品名は固定しない
- 「利用中の AI エージェント / エディタが提供する project hooks で、編集後イベントに lint/fmt スクリプトを登録する」と書く
- Tab 補完後 hook は「存在すれば設定する（推奨）」に留め、必須要件にしない
- hooks の設定ファイル名・イベント名は参考例として括弧書き可。必須仕様にはしない
- 正本はイベント概念（after agent edit / after tab edit if available）とする。将来ツールが変わっても意図が崩れないようにする

## 既存方針との関係

- mise / pnpm / gitleaks / pre-commit / Vite+ / kiso.css などの既存必須方針は維持する。devcontainer はオプション（デフォルト: 不適用）
- pre-commit / CI への lint/fmt 組み込みは本 skill では必須にしない。主目的は編集後 hooks 実行。将来拡張可能

## 骨格サンプル

- `references/sample-files/scripts/lint-fmt-edited-file.sh`
- `references/sample-files/hooks/project-hooks.example.json`
- 配置先ディレクトリ名と設定ファイル名は、利用ツールの project hooks 仕様に合わせて置き換える
