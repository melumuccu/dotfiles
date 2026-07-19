# 完了処理

PR 作成後:

1. issue に PR URL を comment する。
1. PR を issue に紐づける。
1. 必要な reviewer を設定する。(gh コマンドでログイン済みのユーザーを reviewer に設定する)
1. issue status を review 待ちへ更新する。
1. local repository に設計資料ディレクトリがある場合は、設計資料への反映要否を確認する。
1. 設計変更や判断が残る作業なら、local 設計資料へ反映する。
1. remote issue の作業記録や議論を整理し、設計資料として必要な情報だけに絞る。
1. なぜその設計に至ったか、どの議論や制約が判断に影響したかを記録する。
1. issue URL と PR URL を設計資料から辿れる形で残す。

local 設計資料の置き場は repository の規約に従う。
例: `docs/`、`design-docs/`、`2_設計前資料/`、`3_設計資料/`。
