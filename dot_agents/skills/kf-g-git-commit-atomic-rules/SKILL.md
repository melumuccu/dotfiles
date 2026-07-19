---
name: kf-g-git-commit-atomic-rules
description: Enforce frequent atomic commits while doing coding work. Always use this skill at the start of any task that may edit code, configuration, tests, documentation, generated metadata, or other repository files; apply it before implementing features, fixing bugs, refactoring, formatting, or making multi-step changes.
---

# Git Commit Rules / コミットのルール

この skill は、コーディングタスク開始時に必ず参照する commit 粒度の規約。
変更はアトミックな単位に分け、作業中にこまめに commit する。

## 基本方針

You must make frequent, atomic commits for each logical change.
変更は必ず「アトミック（最小単位）」に分割し、こまめにコミットする。

## Commit Granularity / コミットの粒度基準

1. **Single Responsibility / 1つの関心事**
   - 1 commit = 1 logical change. Do not mix unrelated changes.
   - 1つのコミットには1つの修正・機能変更だけを含める。複数の無関係な変更をまとめない。

1. **Keep it Green / 常にビルド可能な状態**
   - Every commit must be in a working state. Code must compile and tests must pass.
   - 小さな単位でも、アプリが起動しない状態やテストが落ちる状態での commit は禁止。

1. **Separate Refactoring from Functional Changes / リファクタリングの分離**
   - Never mix refactoring, formatting, or typo fixes with functional changes or bug fixes.
   - 機能追加・バグ修正と、リファクタリング・タイポ修正・フォーマット変更は必ず別 commit にする。

1. **Reviewable Size / レビューしやすいサイズ**
   - Keep commits small and concise so that reviewers can understand the diff at a glance.
   - 差分を見ただけで何をしたかが一目瞭然な、数行から数十行の小さな単位を意識する。

## Execution Instructions / 実行指示

- Execute `git commit` immediately after completing a small, self-contained task.
- 1つの小さなタスクやファイル修正が完了するたびに、即座に `git commit` を実行する。
- Never bundle multiple issues into a single massive commit. Commit messages like `Fix multiple issues` are strictly prohibited.
- タスク全体の完了を待ってから一括で大きな commit を作ることは禁止。

## 作業開始時の確認

1. `git status --short --untracked-files=all` で既存変更を確認する。
1. 既存の staged / unstaged / untracked 変更がある場合、自分の作業と混ぜない。
1. 既存変更と作業対象が重なる場合、先に扱いを確認する。
1. 作業を、commit 可能な小さい単位へ分割する。
1. それぞれの単位に必要な検証コマンドを決める。

## 作業中の commit 手順

1. 1つの論理変更だけを実装する。
1. その変更に必要なテスト、型検査、lint、差分確認を実行する。
1. 失敗した検証があれば修正し、green な状態に戻す。
1. 自分が変更した対象だけを stage する。ユーザーの既存変更を混ぜない。
1. `git diff --cached --stat` と `git diff --cached --name-status` で commit 対象を確認する。
1. 1つの関心事だけが staged になっている状態で `git commit` を実行する。

## 分離ルール

- 機能変更とリファクタリングを同じ commit に入れない。
- フォーマット、typo、rename、import 整理は機能変更から分ける。
- テスト追加と実装変更は、レビュー容易性が上がる場合だけ同じ commit にしてよい。
- generated file や index file 更新は、対応する source 変更と同じ論理変更なら同じ commit にしてよい。
- 複数ファイル変更でも、1つの論理変更なら1 commit でよい。
- 1ファイル内でも無関係な修正が複数あるなら commit を分ける。

## サンプル

- CLI ツールによりコードベースに何かしらの変更が加えられた時 → 1 commit
  - commit メッセージ例:
     ```
     feat_: `sv create` コマンド実行

     {...(選択したオプションを詳細に記載)}
     ```

- 機能変更と typo 修正が同時に見つかった時 → 2 commit
  - 先に機能変更だけを commit する
  - その後に typo 修正だけを別 commit にする

- 生成ファイルと元コード更新が同じ論理変更に属する時 → 1 commit
  - 変更元と生成先の差分が 1 つの対応関係なら、別 commit に分けない

## staged-only commit skill との関係

この skill は、エージェントがコーディング作業を進めるときの commit 粒度を扱う。
ユーザーが単に `commit` と依頼した場合は、`kf-g-git-commit-staged-only-rules` を優先し、依頼時点ですでに staged 済みの変更だけを commit 対象にする。

## 禁止事項

- `Fix multiple issues` のような大きい commit。
- 動作しない、compile できない、テストが落ちる状態の commit。
- unrelated change の混入。
- refactor / format / typo fix と functional change / bug fix の混在。
- ユーザーの既存変更を自分の commit に混ぜること。

## 完了報告

完了時は、作成した commit、検証内容、未 commit 変更の有無を短く報告する。
