#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title LOGIN TO LINE !!
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🟩

#================================================

# Bitwardenを起動
open -a "bitwarden"

# BitwardenでLINEを検索
osascript -e 'tell application "System Events" to keystroke "f" using command down' # ⌘F で検索バーにフォーカス
osascript -e 'tell application "System Events" to keystroke "a" using command down' # ⌘A で全選択
osascript -e 'tell application "System Events" to key code 51' # Backspaceキーで検索バーをクリア
osascript -e 'tell application "System Events" to keystroke "LINE"' # LINEを検索
osascript -e 'tell application "System Events" to key code 36' # Enterキー

# LINEのパスワードをコピー
osascript -e 'tell application "System Events" to key code 48' # Tabキー
osascript -e 'tell application "System Events" to key code 48' # Tabキー
osascript -e 'tell application "System Events" to key code 36' # EnterキーでLINEを選択
osascript -e 'tell application "System Events" to keystroke "p" using command down' # ⌘Pでパスワードコピー

# LINEを起動
open -a "LINE"

# ペースト
osascript -e 'tell application "System Events" to keystroke "v" using command down' # ⌘V
osascript -e 'tell application "System Events" to key code 36' # Enterキー
