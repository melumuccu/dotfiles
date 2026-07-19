---
name: kf-g-git-hooks-fix-verify-layering
description: Defines a three-layer quality strategy where editor or AI agent hooks auto-fix and detect issues after edits, pre-commit blocks on verify gates, and pre-push runs heavy checks. Use when setting up or reviewing lint, format, type-check, schema, secret-scan, or test hooks, or when deciding what must block git commit or push versus run only after file edits.
---

# Git hooks と編集後 hooks の Fix / Verify 分担

pre-commit / pre-push で gate できるものは **Git hooks を正** にする。
編集後 hooks（AI エージェント / エディタの project hooks）は **編集直後の Fix + 早期検知** 用。

## 結論

| 層           | 役割         | commit / push を止めるか |
| ------------ | ------------ | ------------------------ |
| 編集直後     | 編集後 hooks | 止めない（fail-open）    |
| `git commit` | pre-commit   | 止める（verify gate）    |
| `git push`   | pre-push     | 止める（重い check）     |

## 3 層モデル

```
編集直後     編集後 hooks   Fix + 早期検知（非ブロック）
    ↓
git commit   pre-commit     Verify gate（ブロック）
    ↓
git push     pre-push       重い check（ブロック）
```

### pre-commit を正にする理由

- 手動 commit / AI エージェント外 editor / CLI にも効く
- commit / push を止められる **唯一の共通層**
- エージェント経由でなくても品質担保できる

### 編集後 hooks の位置

- AI エージェントのファイル書き込み / Tab（インライン補完）編集直後のみ
- commit は止めない → **早期修正ループ** 用
- 利用ツールが `additional_context` 相当を返せる場合、lint / check 結果をエージェントへ返却（post-edit イベントのみ）

編集後 hooks の具体設定は利用ツール依存。Cursor なら `.cursor/hooks.json`、他ツールならその project hooks 仕様に合わせる。正本は **イベント概念**（after agent edit / after tab edit if available）。

## format / lint / check の分担

PJ の task 名（`mise run lint` 等）に合わせて読み替える。

| 種別               | Fix（書き換え）                             | Verify（gate）                   |
| ------------------ | ------------------------------------------- | -------------------------------- |
| **format**         | 編集後 hooks: formatter を編集 1 ファイルへ | pre-commit: format check（全体） |
| **lint**           | 編集後 hooks: lint --fix → lint             | pre-commit: lint（全体）         |
| **type check**     | 編集後 hooks: 対象ファイル種に応じて check  | pre-commit: check（常時）        |
| **db / schema**    | 編集後 hooks: schema / migration 編集時     | pre-commit: 同上条件             |
| **secrets / test** | —                                           | pre-commit / pre-push            |

### 原則

1. **Fix** → 編集後 hooks のみ
2. **Verify（gate）** → pre-commit / pre-push
3. **同じ verify を編集後 hooks で gate 化しない**（早期検知は可）

## 実装指針

### コマンド定義

- lint / format / check の正本は PJ の task（`mise run` 等）に 1 本化
- CI / pre-commit / 編集後 hooks は同じ task 名を呼ぶ。定義を二重化しない
- 編集後 hooks は **編集されたファイルだけ** 処理。初回のリポ全体一括 fix はしない

### pre-commit / pre-push

- pre-commit framework 利用時は `stages: [pre-commit]` と `stages: [pre-push]` を明示
- gitleaks 等は pre-commit 専用、全テスト等は pre-push 専用に分離
- hook 導入は `hooks-install` 系 task にまとめる

### 編集後 hooks

- fail-open（編集フローを止めない）
- hook 入力から `file_path` を取得し、対象外拡張子は no-op
- Fix 用コマンド（format / lint --fix）のみ実行。verify gate は pre-commit へ委譲
- Tab 編集後 hook はツールが提供する場合のみ設定（任意）

### アンチパターン

- 編集後 hooks で `format:check` / 全体 lint を gate 化する
- pre-commit と編集後 hooks で **別コマンド定義** を持つ
- verify 失敗時に編集後 hooks だけで commit を止める設計
- pre-push 相当の重い check を pre-commit に詰め込む

## 関連 skill

- 新規 PJ 初期設定: `kf-g-project-bootstrap-new-project-rules`（`references/lint-fmt-hooks.md` 等）
- commit 操作: `kf-g-git-commit-staged-only-rules`
- skill 命名: `kf-g-skill-naming-creation-organization-rules`
