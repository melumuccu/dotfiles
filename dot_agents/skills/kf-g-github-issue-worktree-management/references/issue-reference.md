# Issue 参照

GitHub Projects から issue を参照する時は、`.agents/credentials/github/.env` の `GH_TOKEN` (= user token) を環境変数へ読み込んだ状態で `gh` を実行する。
host 側の `gh auth login` 済み状態は前提にしない。
`projectItems` を読むには `read:project` scope が必要。
token 値は出力しない。

コマンド例:

```sh
gh issue list --repo melumuccu/gitdoc-v2 --state open --limit 100 --json number,title,state,url,projectItems,labels,assignees
```
