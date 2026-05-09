---
name: kf-g-git-commit-japanese-commit-message
description: Create and format commit messages with a fixed 5-character prefix and a Japanese subject. Always use this skill whenever the user wants a commit or a commit message, even if they ask briefly or casually in Japanese or English, such as "commit", "commit plz", "git commitして", "コミットして", "コミットお願いします", "コミットメッセージ考えて", or "コミットメッセージ作って". When executing a commit, only already staged files may be included unless the user explicitly instructs staging.
---

# 5文字プレフィックスの日本語コミットメッセージ

この skill は、コミット実行とコミットメッセージ作成を同じ規約で扱うための入口です。

## 最優先ルール

- stage するかどうかはユーザーが決める。エージェントが自分で commit 対象を広げたり絞ったりしない。
- 実際に commit するときも、コミットメッセージを考えるときも、対象は現在 stage 済みの差分だけに限定する。
- stage 済み差分が 1 つも無い場合は、自分で `git add` せず、その状態を伝えて止まる。
- ユーザーが明示的に stage を依頼した場合だけ、その指示範囲で stage を行う。

## この skill を使う場面

- コミットしてください
- commit
- commit plz
- git commitして
- コミットして
- コミットお願いします
- コミットメッセージ考えて
- コミットメッセージ作って
- prefix を決めてほしい

## 手順

1. まず [権限と commit 対象](./references/authority-and-staging.md) を読む。
1. 次に [メッセージ形式](./references/message-format.md) を読む。
1. prefix 選定が必要なら [prefix 選択ガイド](./references/prefix-selection.md) を読む。
1. wording や最終確認が必要なら [文体・チェック・例](./references/writing-and-checks.md) を読む。
1. stage 済み差分だけを確認してメッセージを作る。
1. ユーザーが実際の commit も求めている場合だけ、その stage 済み差分を commit する。

## 出力方針

- コミットメッセージだけを求められた場合は、規約に沿ったメッセージだけを返す。
- commit 実行を求められた場合は、stage 済み差分だけを commit し、コミット ID を伝える。
- stage 済み差分が無い場合は、勝手に stage せず、その状態を短く伝える。
