---
name: kf-g-agent-planning-structured-plan-output
description: Formats AI agent planning output with concise Japanese, mermaid diagrams, tables, and footnotes for niche terms. Use when planning implementation, architecture, migration, rollout, phased work, design proposals, or when SwitchMode enters plan mode; also when drafting plans for GitHub issues or PR comments.
---

# プランニング出力フォーマット

AI agent が設計・実装・移行・段階投入などの**計画**を書くときに適用する。

## 発火条件

次のいずれかなら本 skill を読む。

| 状況        | 例                                                 |
| ----------- | -------------------------------------------------- |
| 計画作成    | 実装計画、移行計画、ロールアウト計画、フェーズ分割 |
| 設計提案    | アーキテクチャ案、技術選定、トレードオフ整理       |
| Plan モード | `SwitchMode` で plan へ切替後の出力                |
| GitHub 転記 | issue / PR コメントへ計画を貼る前後                |

## 読み進め方

1. 専門用語の要否は [references/term-glossary.md](references/term-glossary.md) で判定
1. フットノート記法は [references/footnote-formats.md](references/footnote-formats.md) に従う
1. **GitHub 転記前**に [references/plan-footnote-checklist.md](references/plan-footnote-checklist.md) を実行

## 構成方針

- 計画の目的・規模に合わせて見出しとブロックを選ぶ。固定テンプレート強制なし

## 文体

- 簡潔。体言止め可
- 長文羅列より **表** と **mermaid** を優先
- 同じ情報を段落と表の両方に書かない

### mermaid 図種

| 目的               | 図種              | 例                       |
| ------------------ | ----------------- | ------------------------ |
| コンポーネント関係 | `flowchart`       | サービス分割、データ流   |
| 時系列             | `sequenceDiagram` | API 呼び出し、認可フロー |
| 状態遷移           | `stateDiagram-v2` | ジョブ状態、デプロイ段階 |
| 並行フェーズ       | `gantt`           | マイルストーン           |

### アンチパターン

- フェーズを番号付き長文だけで書く
- 同一内容を概要表と本文段落に重複
- 全見出し下に 1 行説明だけ置く (表に統合)
- 未検証の mermaid を詳細すぎる粒度で描く
- `spoof 対策` / `改ざん対策` / `内部ヘッダ` 等、**計画の主題となるセキュリティパターン名**を footnote なしで初出する

## フットノート方針

| 区分                       | 扱い                             |
| -------------------------- | -------------------------------- |
| 標準 IT 用語               | フットノート不要。初出でも平文   |
| 製品固有・ニッチ | 初出のみフットノート             |
| GitHub 投稿                | 記法を GitHub フットノート `[^n]` へ変換 |

判定の詳細と語彙リストは `references/term-glossary.md`。記法・変換・出力先別ルールは `references/footnote-formats.md`。

## 最終チェック

- [ ] 表または mermaid が計画の中心か
- [ ] 標準用語に不要なフットノートが無いか
- [ ] 製品固有用語に初出フットノートがあるか
- [ ] `term-glossary.md` の「フットノート推奨」語で、計画本文に出たものを漏れなく footnote 化したか
- [ ] セキュリティ / 認可 / 信頼境界のラベル（例: spoof 対策、内部ヘッダ）を初出 footnote したか
- [ ] 出力先に合った記法か (Cursor=HTML / ローカル MD=`[^label]` / GitHub=`[^n]`)
- [ ] GitHub 転記前にフットノート変換済みか
