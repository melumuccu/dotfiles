# Issue 選択

「issue 実装開始」や「issue プランニング開始」など、特定のタスクを明示せずに指示を受けた時は以下のルールに従って作業を進める。

コマンド詳細は [issue-reference.md](issue-reference.md) を参照。

1. `gh project item-list 3 --owner melumuccu --format json --limit 100` で Project item 一覧を取得する。
1. `status == "Ready"` の item だけに絞る。
1. Ready item の中で `"start Date"` が最も早い item を選択する。未設定 item は最後尾扱い。
1. 選択した issue の内容を `gh issue view` で確認し、作業を開始する。
1. 作業中は、随時 issue の description の更新・status 更新・comment 追記など、記録できるものは常に記録する。

## 選定中止

Start Date を取得できず選定不能なら、**プランニング・実装着手を中止**する。推測選定・issue 番号順・`projectItems` 代替は禁止。

中止条件:

- `gh project item-list` が失敗（認証エラー、project 不在、`read:project` scope 不足 等）
- 出力に `"start Date"` キー自体がない（`gh issue list --json projectItems` 等の誤コマンド）
- Ready item が 0 件
- Ready item はあるが、全件 `"start Date"` 未設定で最古選定不能

ユーザーへの報告内容:

1. **なぜ選べなかったか** — 上記のどれに該当するか、実行コマンドとエラー/観測結果
2. **解決方針** — 次のいずれかを具体提示
   - `GH_TOKEN` 読み込みと `read:project` scope 確認
   - `gh project item-list 3 --owner melumuccu --format json --limit 100` の再実行（`projectItems` 不使用）
   - GitHub Project 上で Ready issue に Start Date 設定
   - item 数 >100 なら `--limit` 増加
   - project number / owner の見直し

作業の着手順は依存関係を考慮する。依存関係は start date プロパティで管理する。

- ロードマップ上で日付順に並べた時に同日なら並行作業可能。
- より早い日付が設定されている issue (A) が、より後の issue (B) をブロックしているものとみなし、A が完了するまで B は着手しない。
