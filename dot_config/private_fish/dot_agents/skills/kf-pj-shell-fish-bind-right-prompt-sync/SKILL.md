---
name: kf-pj-shell-fish-bind-right-prompt-sync
description: Keeps fish right-prompt key hints in sync with repo-managed custom bind definitions. Use when adding, changing, or removing fish bind, key assignment, or keybindings files (e.g. fish_user_key_bindings.fish, conf.d/*keybindings*.fish).
---

# fish bind と右プロンプト同期

repo 管理の明示的カスタム bind を変更したら、右プロンプトのキー一覧も同一作業で更新する。

## トリガー

次を追加・変更・削除する作業:

- `functions/fish_user_key_bindings.fish` の `bind`
- `conf.d/*keybindings*.fish` の `bind`
- 上記に相当するキー割当の追加・改名・削除

## 対象外

- fish built-in bind
- fzf / peco 等プラグイン内部 bind
- 上記ソースに無い暗黙 bind

## 同期先

`functions/fish_right_prompt.fish` の空入力時表示行:

```fish
echo -n '⌃G AI  ⌃R history'
```

`commandline -b` が非空なら return する既存挙動は維持。

## 手順

1. **bind 収集** — 対象ソースから `bind` 行を読む
1. **一意キー化** — 同一キー（例: `\cr` が2ファイル）は最終的に有効な定義1件として扱い、表示も1回
1. **ラベル決定** — 関数名・コメント・既存右プロンプトから短い用途ラベル（例: `AI`, `history`）
1. **表記変換** — `\cX` → `⌃X`（`\cg` → `⌃G`）
1. **右プロンプト更新** — 項目を `⌃X label` 形式、項目間スペース2個で連結
1. **ケース別**
   - **追加**: bind 追加 + 右プロンプトに項目追加
   - **変更**: bind キー/関数変更 + 右プロンプトの該当項目更新
   - **削除**: bind 削除 + 右プロンプトから該当項目削除。カスタム bind が0件なら表示行を空または削除方針に合わせる

## 完了条件

bind 変更と `fish_right_prompt.fish` 変更を同一 diff / 同一作業で行う。片側のみは未完了。

## 検証

1. **一意キー整合** — 対象ソースの有効な一意キー集合と右プロンプト表示キーが一致
1. **構文** — `fish -n functions/fish_right_prompt.fish` および変更した bind ファイル
1. **表示** — 新 fish セッションで
   - 空入力: 右プロンプトにキー一覧表示
   - 文字入力後: 右プロンプト非表示（`commandline -b` で return）

## 参照例（現状）

| ソース | bind | 表示 |
| --- | --- | --- |
| `fish_user_key_bindings.fish` | `\cg my_ai_gen` | `⌃G AI` |
| `fish_user_key_bindings.fish`, `300-keybindings.fish` | `\cr my_peco_history_selection` | `⌃R history`（1表示） |
