# Issue 選択

「issue 実装開始」や「issue プランニング開始」など、特定のタスクを明示せずに指示を受けた時は以下のルールに従って作業を進める。

1. GitHub issues を参照し、status が Ready になっている issue を確認する。
1. Ready になっている issue の中で、start date プロパティが最も早い issue を選択する。
1. 選択した issue の内容を確認し、作業を開始する。
1. 作業中は、随時 issue の description の更新・status 更新・comment 追記など、記録できるものは常に記録する。

作業の着手順は依存関係を考慮する。依存関係は start date プロパティで管理する。

- ロードマップ上で日付順に並べた時に同日なら並行作業可能。
- より早い日付が設定されている issue (A) が、より後の issue (B) をブロックしているものとみなし、A が完了するまで B は着手しない。
