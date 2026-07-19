# gitleaks

commit / push 時に gitleaks で検知された場合:

- commit / push 禁止。
- `--no-verify` 禁止。
- hook 削除、scan 弱体化、除外設定追加による回避禁止。
- まず検知内容を修正する。
- 誤検知に見える場合も、ignore 追加前にユーザへ確認する。
