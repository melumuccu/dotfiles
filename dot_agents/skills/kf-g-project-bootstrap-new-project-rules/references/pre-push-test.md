# pre-push で全テスト実行

## 方針

- push 前に PJ 内の全テストを実行する。
- 1 件でも失敗したら push を止める（hook が非ゼロ終了）。
- pre-commit framework の `pre-push` stage で実行する。gitleaks pre-push と同じ `.pre-commit-config.yaml` に載せる。

## 前提

- `mise.toml` に `test` task があり、`mise run test` で全テストが走ること（[devcontainer-mise.md](devcontainer-mise.md) の mise 日常 task 一式）。
- frontend あり PJ では Vite+ の test コマンドを `test` task に載せる（[frontend-vite-plus.md](frontend-vite-plus.md)）。
- backend のみ PJ では、その言語の test runner を `test` task に集約する。

## `.pre-commit-config.yaml`

- `stages: [pre-push]` の local hook を追加する。
- gitleaks pre-push と並列で登録する。実行順は gitleaks → test を推奨（secret 検出を先に）。
- hook 例:

```yaml
      - id: test-pre-push
        name: Run all tests before push
        entry: mise run test
        language: system
        pass_filenames: false
        always_run: true
        stages:
          - pre-push
```

## 検証

- `pre-commit run test-pre-push --hook-stage pre-push` で手動実行できること。
- 意図的に失敗するテストを置き、`git push` が拒否されることを確認する。

## 不適用

- テストを書かない PJ、または `test` task を定義しない PJ では **不適用**。
