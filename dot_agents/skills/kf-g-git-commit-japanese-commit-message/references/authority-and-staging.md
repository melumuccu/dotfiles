# 権限と commit 対象

## 非交渉ルール

- stage するかどうかを決める権限はユーザーにある。エージェントが自分で commit 対象を決めない。
- 実際の commit でも、コミットメッセージ作成でも、根拠にしてよい差分は stage 済みのものだけ。
- `commit` のような短い依頼は、stage を許可した意味には解釈しない。
- stage 済み差分が無いときは commit しない。自分で `git add` や `git restore --staged` を打たない。
- unstaged の変更や untracked の未 stage ファイルは、commit 対象として扱わない。

## 実際に確認するもの

commit 実行やメッセージ作成の前には、stage 済み差分だけを見る。

```text
git status --short
git diff --cached --stat
git diff --cached
```

- `git diff` のような unstaged 前提の差分は、commit 内容の判断材料にしない。
- stage 済みと unstaged が混在している場合も、commit 対象は stage 済みだけ。

## ユーザーが stage を明示した場合

次のように、ユーザーが stage の意思を具体的に示した場合だけ、その指示範囲で stage してよい。

- この 2 ファイルを stage してから commit して
- 全部 stage して commit して
- README だけ add してコミットして

この場合でも、stage 後に改めて stage 済み差分を確認し、その差分だけを commit 対象にする。

## 返答ルール

- stage 済み差分が無い場合は、その事実を短く伝えて止まる。
- ユーザーが commit だけを頼んでいて、作業ツリーに unstaged 変更しか無い場合も、自分で stage しない。
- stage 済み差分で commit した結果、他の unstaged 変更が残る場合は、必要なら最後に短く伝える。
