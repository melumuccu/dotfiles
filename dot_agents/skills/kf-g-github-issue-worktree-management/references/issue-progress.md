# 作業中の issue 更新

issue と local 設計資料は用途を分ける。

- remote の GitHub Issues / GitHub Projects は、作業進行を管理する場所。
- local repository の設計資料は、後から見返す設計判断を残す場所。
- issue の作業メモを、そのまま設計資料へコピーしない。
- 設計資料には、完了後も参照する決定事項、背景、議論の要点だけを整理して残す。

remote issue では、メンバーや AI agent 間のタスク状況共有と進捗管理を行う。
GitHub Projects がある場合は、repository の既定に従い `Backlog`、`Ready`、`In Progress`、`In review`、`Done` などの status を更新する。

## プランニング内容の description 転記

Cursor チャットや Plan モードなどで作成した実装計画を基に作業を始める場合、**実装着手前**にその計画を issue の description へ転記する。

- description: 作業の仕様・計画を置く場所。
- comment: 作業ログ、判断、進捗、PR URL を残す場所（`SKILL.md` 基本方針参照）。
- 既存 description がある場合は上書きせず、計画節を追記または整理して統合する。
- 転記時のフォーマットは `kf-g-agent-planning-structured-plan-output` に従う。GitHub 投稿前にフットノート記法を変換する。

作業中は issue に随時記録を残す。

記録する内容:

- 着手開始
- 方針、調査結果、判断理由
- blocked / waiting / review など状態変化
- description 更新
- status 更新
- 議論、保留、未決事項
- PR URL
- 完了時の要約

AI agent がコメントする場合は `kf-g-github-operations-bot-workflow` の skill に従う。
