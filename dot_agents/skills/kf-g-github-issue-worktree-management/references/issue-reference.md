# Issue 参照

GitHub Projects から issue を参照する時は、`.agents/credentials/github/.env` の `GH_TOKEN` (= user token) を環境変数へ読み込んだ状態で `gh` を実行する。
host 側の `gh auth login` 済み状態は前提にしない。
Projects V2 操作（`gh project item-list` など）には `read:project` scope が必要。
token 値は出力しない。

## Project カスタムフィールド（Status / Start Date 等）— 選定用

Start Date は Project V2 カスタムフィールド。issue 側の `projectItems` では取得できない。project 側 item 一覧で取る。

```sh
gh project item-list 3 --owner melumuccu --format json --limit 100
```

- `--limit 100` 必須（デフォルト 30）。プロジェクト item 数 >30 なら漏れリスク。
- 出力の各 item に `status`, `"start Date"`, `content.number`, `title` 等がフラットに入る。
- JSON キー `"start Date"` は jq で `.["start Date"]` アクセスが必要。
- 取得失敗時は [issue-selection.md](issue-selection.md) の「選定中止」に従い、プランニング・実装着手を止める。

## Issue 詳細（body / labels / assignees）— 選定後の確認用

```sh
gh issue list --repo melumuccu/gitdoc-v2 --state open --limit 100 \
  --json number,title,state,url,labels,assignees
```

- `projectItems` は status と project title のみ。Start Date 非対応。
- 選定後に `gh issue view <n> --repo melumuccu/gitdoc-v2 --json body,...` で詳細確認。

## 非推奨・不可

- `projectCards`: Projects (classic) deprecated。`gh issue view --json projectCards` はエラー。
- `projectItems` からカスタムフィールド値を推測しない。

## フィールド定義確認（任意）

```sh
gh project field-list 3 --owner melumuccu --format json
```
