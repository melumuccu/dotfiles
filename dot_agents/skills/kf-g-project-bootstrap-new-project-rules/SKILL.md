---
name: kf-g-project-bootstrap-new-project-rules
description: Use this skill when starting a new project and defining baseline repository rules, especially for optional devcontainer setup, mise-first tooling, pnpm security settings, Vite+ workflows, kiso.css adoption, and project-local post-edit lint/format hooks that run after AI agent file edits.
---

# 新規プロジェクト立ち上げルール

この SKILL.md は**入口**。詳細は `references` 配下の該当ファイルを読む。

**重要**: 新規 PJ のファイル作成・scaffold は、本 skill の [入口フロー](#入口フロー) を完了し、ユーザがルール適用表を承認するまで開始しない。

## この skill を使う場面

- 新しい PJ を作る
- 新規リポジトリの初期構成を決める
- devcontainer や mise を含む開発基盤を最初から整える
- frontend の標準 toolchain を決める
- pnpm の supply chain 対策を初期設定へ組み込みたい
- secret scan を初期設定へ組み込みたい
- AI エージェント編集後の lint/fmt 自動実行を初期設定へ組み込みたい

## 入口フロー

新規 PJ 立ち上げは、次の 4 フェーズを順に進める。フェーズ 4 の承認前に devcontainer 作成・scaffold・設定ファイル追加などの実 작業を始めない。

### フェーズ 1: PJ 概要の把握

ユーザから PJ 概要をヒアリングする。プロンプトに既に含まれていれば、それを起点に不足分だけ確認する。

最低限、次を把握する（未記載なら選択肢から選択させる形でユーザに質問する）:

| 項目            | 例                                                        |
| --------------- | --------------------------------------------------------- |
| PJ 名 / 目的    | 社内ダッシュボード、CLI ツール、API サーバ                |
| リポジトリ種別  | 新規 / 既存空リポジトリ / monorepo 追加                   |
| 提供形態        | Web UI / API のみ / CLI / ライブラリ / 複合               |
| 主要言語・FW    | TypeScript, Go, Python など                               |
| frontend の有無 | ブラウザ向け UI を提供するか                              |
| frontend FW     | SvelteKit / React / なし など                             |
| devcontainer    | 利用するか（**デフォルト: なし**）                        |
| 開発環境        | CI 先（GitHub Actions 等）、ローカル runtime 管理方針   |
| 特記事項        | monorepo 構成、既存 toolchain 継続、Vite+ 非採用理由 など |

### フェーズ 2: ルール適用表の作成

[ルール一覧](#ルール一覧) を全件走査し、PJ 概要に基づいて各ルールの**推奨**（適用 / 不適用 / 要確認）を決める。

- **適用**: 条件を満たし、標準方針どおり導入する
- **不適用**: 条件を満たさない、または PJ 方針上不要
- **要確認**: 条件付きルールで、ユーザ判断が必要

推奨を決めたら、次の形式で**ルール適用表**を提示する。

```markdown
## ルール適用表（確認用）

| ルール        | 条件 | 推奨 | 理由               |
| ------------- | ---- | ---- | ------------------ |
| devcontainer  | オプション | 不適用 | デフォルトはローカル開発。必要時のみ導入 |
| mise 中心運用 | 汎用 | 適用 | tools / tasks 集約 |
| ...           | ...  | ...  | ...                |

### 要確認項目

- Vite+: frontend あり → 適用推奨。React 採用のため Svelte / SvelteKit は不適用でよいか
```

**要確認** がある場合は、適用表提示と同時にユーザへ質問する。回答を反映して表を更新する。

### フェーズ 3: ユーザ確認・調整

ルール適用表を提示し、次を求める。

1. 推奨どおりでよいか
2. **適用 / 不適用** を変更したいルールがあるか
3. 表にない例外・追加要件があるか

ユーザが変更を示したら表を更新し、再度提示する。**全ルールについて適用 / 不適用が確定するまでフェーズ 3 を繰り返す。**

確認手段:

- 表全体への明示的な承認（「この表で進めて」等）
- 個別ルールの変更指示
- 不明点があれば `AskQuestion` 等で構造化して確認してよい

### フェーズ 4: 承認後に作成開始

ユーザがルール適用表を承認したら、初めて実装作業に入る。

1. 承認済み表の **適用** 行に対応する参照ファイルを読み、実装する（[読み進め方](#読み進め方)）
2. **不適用** とされたルールに該当するファイル・設定は作らない
3. 完了前に [checklist.md](references/checklist.md) を、承認済みルールに合わせて確認する

承認済み表は作業ログとして短く残す（どのルールを適用 / 不適用にしたか）。

---

## ルール一覧

全ルールを列挙する。フェーズ 2 ではこの表をベースに、PJ ごとの適用 / 不適用を決める。

| ルール                 | 条件                        | 参照                                                        | 概要                                                                 |
| ---------------------- | --------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------- |
| devcontainer           | オプション（デフォルト: 不適用） | [devcontainer-mise.md](references/devcontainer-mise.md)     | 利用時のみ `.devcontainer/devcontainer.json` を作成。実行場所を統一  |
| mise 中心運用          | 汎用                        | [devcontainer-mise.md](references/devcontainer-mise.md)     | `mise.toml` に tools / env / tasks を集約                            |
| user settings 確認     | devcontainer 適用時         | [devcontainer-mise.md](references/devcontainer-mise.md)     | `dev.containers.*`, `dotfiles.*` を確認し重複設定を避ける            |
| サンプルファイル起点   | 汎用                        | [devcontainer-mise.md](references/devcontainer-mise.md)     | `references/sample-files/` を初期ファイルの起点にする                |
| gitleaks               | 汎用                        | [gitleaks-pre-commit.md](references/gitleaks-pre-commit.md) | secret scan を GitHub Action と pre-commit の両方で導入              |
| pre-commit / pre-push  | 汎用                        | [gitleaks-pre-commit.md](references/gitleaks-pre-commit.md) | `pre-commit`, `gitleaks` を mise 管理。local hook を有効化           |
| pnpm 固定              | frontend あり               | [frontend-pnpm.md](references/frontend-pnpm.md)             | package manager を pnpm に固定                                       |
| pnpm supply chain      | frontend あり               | [frontend-pnpm.md](references/frontend-pnpm.md)             | `pnpm-workspace.yaml` にセキュリティ設定                             |
| Vite+                  | frontend あり               | [frontend-vite-plus.md](references/frontend-vite-plus.md)   | build / dev / check / test を Vite+ 流儀に寄せる                     |
| Svelte / SvelteKit     | frontend + Svelte 採用      | [frontend-vite-plus.md](references/frontend-vite-plus.md)   | 最新安定版を使用                                                     |
| kiso.css               | frontend UI あり            | [frontend-vite-plus.md](references/frontend-vite-plus.md)   | reset CSS を pnpm で導入し entry で最初に読み込む                    |
| Oxlint / Oxfmt         | frontend あり               | [lint-fmt-hooks.md](references/lint-fmt-hooks.md)           | frontend の linter / formatter。未対応時は代替を調査                 |
| lint / format コマンド | コード編集あり              | [lint-fmt-hooks.md](references/lint-fmt-hooks.md)           | `package.json` scripts と `mise run` task に載せる                   |
| 編集後 lint/fmt hooks  | コード編集あり              | [lint-fmt-hooks.md](references/lint-fmt-hooks.md)           | AI エージェント編集後に project hooks で lint/fmt 実行               |
| Tab 補完後 hook        | コード編集あり + ツール対応 | [lint-fmt-hooks.md](references/lint-fmt-hooks.md)           | 利用ツールが対応していれば設定（任意）                               |
| mise 日常 task 一式    | 汎用                        | [devcontainer-mise.md](references/devcontainer-mise.md)     | install / dev / check / test / build / lint / format / hooks-install |

### 条件の読み方

| 条件                        | 適用判定                                                                |
| --------------------------- | ----------------------------------------------------------------------- |
| 汎用                        | 原則すべての新規 PJ で適用推奨                                          |
| オプション（デフォルト: 不適用） | 標準では不適用。ユーザが明示的に利用を選んだ場合のみ適用           |
| devcontainer 適用時         | devcontainer ルールが **適用** と確定している場合のみ適用               |
| frontend あり               | ブラウザ向け UI または frontend パッケージを含む                        |
| frontend UI あり            | ユーザー向け画面・スタイルを提供する frontend                           |
| frontend + Svelte 採用      | frontend があり、Svelte / SvelteKit を採用する                          |
| コード編集あり              | ソースコードをリポジトリで管理・編集する                                |
| コード編集あり + ツール対応 | 編集後 lint/fmt hooks を適用し、かつ Cursor 等が Tab 補完後 hook を提供 |

frontend なし PJ では pnpm / Vite+ / kiso.css / Oxlint・Oxfmt 等 frontend 向けルールは**不適用**。lint / format コマンド・編集後 hooks は backend 言語に合わせて選定して適用する。

## 読み進め方

承認後の実装手順は `references` 側が正本。SKILL.md は入口とルール選定のみ担う。

1. [入口フロー](#入口フロー) を完了する。
2. [ルール一覧](#ルール一覧) で **適用** となった各行の「参照」列のファイルを読み、実装する。
3. 完了前に [checklist.md](references/checklist.md) を、承認済みルールに合わせて確認する。

## 出力方針

- 入口フロー完了前は、方針説明とルール適用表の提示に留める。ファイル作成は始めない。
- 承認後は方針説明だけで止めず、承認済みルールに対応するファイルを作る。
- 承認済みルール適用表を短く残す。
