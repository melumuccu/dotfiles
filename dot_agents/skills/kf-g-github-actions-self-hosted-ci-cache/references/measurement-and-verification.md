# 計測と検証

改修前後を step 単位で比較する。感覚ではなく `gh run view --json jobs` を使う。

## build + deploy workflow

```sh
# build まで（deploy スキップ input がある場合）
gh workflow run <workflow> --ref <branch> -f skip_deploy=true

# 2 回連続で warm run を確認
gh run list --workflow=<workflow-file> --limit 2
gh run view <RUN_ID> --json jobs
```

確認項目:

- 2 回目 `Run jdx/mise-action@v3` ~1s
- `Run mise run install` ~10s 台
- ログに `mise all tools are installed`

## ephemeral deploy workflow（PR トリガー等）

```sh
# 同一ブランチで workflow を 2 回起動（空 commit push 等）
gh run list --workflow=<workflow-file> --limit 2
gh run view <RUN_ID> --json jobs
```

確認項目:

- deploy job 成功
- cleanup job 成功（close / destroy トリガー時）

## 計測サマリの目安

| 対象 | 改修前の典型 | warm 後の典型 |
|------|-------------|--------------|
| build+deploy job | ~140s | ~35–60s |
| cleanup job（軽量化後） | ~130s | ~25–35s |

| step | 改修前の典型 | warm 後の典型 |
|------|-------------|--------------|
| mise-action | ~100s | ~1s |
| pnpm install | ~11–12s | ~11–12s |
| remote deploy | 可変 | 可変（API 待ち） |
| cleanup delete | ~5–6s | ~5–6s |

## warm run の解釈

- **mise**: `RUNNER_TOOL_CACHE` 永続化で劇的短縮。主ボトルネック解消。
- **pnpm install**: store warm でも ~11s は下限（毎 job `node_modules` リンク）。
- **2 回目の追加短縮**: install より remote deploy ステップ（incremental upload 等）の寄与が大きいことがある。

## 次の改善候補（優先度）

1. **cleanup CLI-only 化** — build 不要 job の定番手
2. **remote deploy 内訳計測** — API 呼び出しの切り分け
3. **secret 再投入の条件スキップ** — 値不変時のみ（実装コスト中）
4. **path filter** — docs-only 変更で deploy skip（誤 skip 注意）
5. **build / node_modules cache** — ROI 低、見送り推奨
