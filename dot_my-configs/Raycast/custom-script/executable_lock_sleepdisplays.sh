#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Sleep Display
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖

# ロック(⌘^Qのショートカットキーをエミュレート)
osascript -e 'tell application "System Events" to keystroke "q" using {control down, command down}'

# スクリーンのスリープ
pmset displaysleepnow

