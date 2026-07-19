#!/usr/bin/env bash

set -u

# fail-open: trap で常に exit 0 し、編集フローを止めない

# ログ出力先を決め、log() でタイムスタンプ付き追記する

# hook 入力から file_path を解決する
# - CLI 引数
# - stdin JSON の file_path / path / filePath

# file_path が空、ファイル不在、非対象拡張子なら no-op

# mise 不在なら no-op

# PJ 固有の対象拡張子と mise task 名を定義する
# - TARGET_EXTENSIONS
# - FORMAT_TASK
# - LINT_TASK

# mise run "${FORMAT_TASK}" -- "${FILE_PATH}" を実行する
# - 編集ファイル単位のみ。全体一括 format はしない
# - 失敗しても編集フローを止めない

# mise run "${LINT_TASK}" -- "${FILE_PATH}" を実行する
# - 編集ファイル単位のみ。全体一括 lint はしない
# - 失敗しても編集フローを止めない

# 開始・skip・失敗・完了を log() で記録する
