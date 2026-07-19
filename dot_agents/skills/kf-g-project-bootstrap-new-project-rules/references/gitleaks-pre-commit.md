# gitleaks と pre-commit

## secret scan は gitleaks で標準化する

- GitHub Action と pre-commit の設定は、`gitleaks/gitleaks` の README を参照して組む。
- `pre-commit` と `gitleaks` は brew ではなく `mise` で入れる。`mise install` を導入の基準にする。
- `GITLEAKS_LICENSE` は個人アカウント利用を前提に不要とし、既定では設定しない。Organization 向け要件が明確な場合だけ別途検討する。
- local の macOS でも `mise install` を前提にし、devcontainer 環境でも同じ `mise` の導線で入るように整える。

## pre-commit framework の運用

- commit 前の検査と push 前の検査は分ける。
- `.pre-commit-config.yaml` では、gitleaks hook を `pre-commit` 専用にする。
- push 前に実行する hook は `pre-push` 専用にする。
- 各 hook の `stages` を明示し、`pre-push` で同じ gitleaks が 2 回走らないようにする。
- gitleaks hook は `stages: [pre-commit]` を基本にする。
- push 用 hook は `stages: [pre-push]` を基本にする。
- local hook の導入は、`pre-commit install` と `pre-commit install --hook-type pre-push` の両方を実行する。
- hook 導入手順は `mise run hooks-install` にまとめる。
- hook 設定の検証は `pre-commit validate-config` と `pre-commit run --hook-stage pre-push` で行う。
