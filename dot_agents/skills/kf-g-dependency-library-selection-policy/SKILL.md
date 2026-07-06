---
name: kf-g-dependency-library-selection-policy
description: Use this project skill whenever adding, replacing, evaluating, or reviewing third-party libraries or package dependencies in this repository. It prioritizes trusted vendor-backed packages, screens out low-adoption or individual-maintained libraries, and requires documented justification for unavoidable exceptions.
---

# 依存ライブラリ選定規約

この skill は、このリポジトリでライブラリやパッケージ依存を追加、置換、レビューするときに使う。

## 基本方針

依存ライブラリは、信頼性と継続保守の見込みを優先して選ぶ。

まず標準ライブラリ、既存依存、利用中フレームワークの公式機能で足りるかを確認する。新しい依存を増やす場合は、用途に対して必要十分な範囲に絞る。

## 優先する依存

次のような依存を優先する。

- Microsoft、Meta、Google、Apple、Amazon、Cloudflare、OpenJS Foundation など、信頼性のある組織やベンダーが提供しているもの
- 利用中フレームワークやランタイムの公式パッケージ
- 既にこのリポジトリで採用され、保守状態に問題がないもの
- その用途で広く使われ、代替候補と比べてデファクトスタンダードと説明できるもの

## 基本的に避ける依存

次の依存は基本的に利用対象から外す。

- 個人開発者が単独で保守しているライブラリ
- GitHub stars が 1000 未満のライブラリ
- 直近の保守状況、issue 対応、リリース頻度が弱いライブラリ
- trivial な処理を置き換えるだけの小さな便利ライブラリ
- 依存ツリーが大きく、用途に対して過剰なライブラリ

## 例外として許可できる条件

個人開発や stars 1000 未満でも、次の裏付けがある場合は候補にできる。

- その用途ではデファクトスタンダードとして扱われている
- 主要フレームワーク、公式ドキュメント、大規模プロジェクトで採用例がある
- 代替の公式・大手ベンダー製ライブラリが存在しない
- 実装を自前で持つほうが、保守性、セキュリティ、互換性のリスクを大きくする

例外採用する場合は、採用理由をコメントに残す。コメントは WHAT ではなく WHY を書く。

```ts
// HEIC 変換では公式の軽量実装がなく、この用途では sharp が事実上の標準として保守されているため採用する。
import sharp from "sharp";
```

## 調査手順

依存追加の前に、次を確認する。

1. 標準機能、既存依存、公式 API で代替できないか。
1. パッケージの提供元が組織か個人か。
1. GitHub stars が 1000 以上か。
1. 最終リリース、issue、pull request、セキュリティ advisory の状態。
1. 主要プロジェクトや公式ドキュメントでの採用実績。
1. 依存ツリー、バンドルサイズ、ライセンスが用途に対して妥当か。

stars、保守状況、採用実績は変わるため、依存を新しく入れる判断では現在の情報を確認する。

## レビュー時の扱い

依存追加や置換のレビューでは、次を確認する。

- 公式機能や既存依存で済む処理を新規依存にしていないか
- 信頼できるベンダーや公式パッケージを優先しているか
- 個人開発または stars 1000 未満の依存を採用していないか
- 例外採用の場合、デファクトスタンダードである裏付けがあるか
- 例外採用の場合、WHY のコメントが残っているか

`package.json` などコメントを書けないファイルだけで依存が見える場合は、その依存を直接使う実装箇所、または近い設計メモに WHY を残す。
