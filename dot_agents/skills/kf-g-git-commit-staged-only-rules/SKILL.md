---
name: kf-g-git-commit-staged-only-rules
description: Enforce staged-only behavior for git commits. Always use this skill whenever the user asks to commit, wants a commit created, asks to run git commit, wants a commit message based on repo changes, or uses short prompts like "commit", "commit plz"; combine it with kf-g-git-commit-japanese-commit-message when creating the message.
---

# Git Commit の staged-only 規約

この skill は、commit 依頼で commit 対象を staged 済み変更だけに限定するための規約。
コミットメッセージ作成時は `kf-g-git-commit-japanese-commit-message` と併用する。

## 基本方針

- commit 対象は、依頼時点ですでに stage されている変更だけにする
- unstaged 変更、untracked ファイル、未 stage の削除は commit 対象に含めない
- commit 依頼の流れで、勝手に `git add` しない
- stage された変更が 1 つもない場合は、ユーザーに stage を促して中断する

## 禁止事項

commit 依頼では、次の操作を厳格に禁止する。

- `git add`
- `git add -A`
- `git add .`
- `git add <path>`
- `git commit -a`
- `git commit --all`
- `git commit <pathspec>`
- `git update-index` など、index を直接変更する操作
- formatter、generator、hook 修復などを理由にした暗黙の stage

ユーザーが stage 操作も必要だと明示した場合でも、commit と同じ流れで勝手に stage しない。
まず stage 対象を確認し、stage 後に commit へ進んでよいかを別途確認する。

## 確認手順

1. `git status --short` で staged、unstaged、untracked の有無を確認する
1. `git diff --cached --name-status` または `git diff --cached --stat` で staged 済み変更だけを確認する
1. staged 済み変更がなければ、その時点で中断する
1. コミットメッセージは `git diff --cached` の内容だけから作る
1. commit する場合は、pathspec や `--all` を付けずに `git commit` する
1. commit 後の報告では、commit 対象が staged 済み変更だけだったことを必要に応じて明記する

## staged 変更がない場合

staged 済み変更が 1 つもない場合は、commit しない。
空コミットで代替しない。
ユーザーへ、対象ファイルを stage してから再依頼するよう短く伝える。

例:

```text
stage 済み変更なし。commit 対象なし。
必要なファイルを `git add <path>` で stage してから再依頼して。
```

## unstaged 変更がある場合

unstaged 変更や untracked ファイルがあっても、commit 対象には含めない。
それらを勝手に stage せず、必要なら「未 stage の変更は commit から除外」とだけ報告する。

コミットメッセージの `概要` と `Why` も、staged 済み変更だけを根拠に書く。
unstaged 変更の内容を混ぜると、実際の commit と message がずれるため。

## commit message skill との併用

`kf-g-git-commit-japanese-commit-message` を使う場合も、この skill の制約を優先する。

- 直近 commit の確認はしてよい
- staged diff の確認はしてよい
- unstaged diff は commit message の根拠にしない
- commit message の作成後も `git add` しない
- `git commit` 実行時は staged index だけを commit する
