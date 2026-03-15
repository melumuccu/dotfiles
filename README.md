# dotfiles

[chezmoi](https://www.chezmoi.io/) + `GitHub CLI` + `VS Code` を組み合わせた dotfiles 管理リポジトリ

## 🚀 特徴

- **自動同期**: `chezmoi edit` で保存し VS Code のタブを閉じると、自動で `apply` & `git commit` が走ります。
  - `git push` は手動で行うことで、テンプレート管理しているファイルの内容を誤って公開するリスクを回避しています。
- **マルチプラットフォーム対応**: Mac, Linux, Windows (WSL) で同一のリポジトリを使用可能。
- **テンプレート管理**: OSごとの差異（エディタのパスやエイリアス）をテンプレート機能で吸収します。

---

## 🛠 新環境でのセットアップ手順

新しいマシンを手に入れたら、以下の手順で数分以内に環境が復元されます。

### GitHub CLI のインストールと認証

1. 各OSのパッケージマネージャ（brew, apt, scoop等）で `gh` をインストール
1. GitHub にログイン (SSH)

   ```bash
   gh auth login
   ```

   1. What account do you want to log into? → GitHub.com
   1. What is your preferred protocol for Git operations? → SSH (重要！)
   1. Generate a new SSH key to upload to your GitHub account? → Yes
   1. Enter a passphrase for your new SSH key → (空のままEnter またはパスフレーズを入力)
   1. Title for your new SSH key → (そのままでOK)
   1. How would you like to authenticate GitHub CLI? → Login with a web browser

1. ブラウザで表示されたURLにアクセスし、ターミナルに表示されたコードを入力して認証を完了させる
1. GitHubとのSSH接続テスト
1. 成功すれば "Hi [ユーザー名]! You've successfully authenticated..." と出ます

   ```bash
   ssh -T git@github.com
   ```

### Bitwarden CLI のインストールと認証

[公式Docs](https://bitwarden.com/help/cli/)

1. 公式サイトから `bw` をインストール
   1. see: https://bitwarden.com/help/cli/#download-and-install
1. checksum を検証
   1. see: https://bitwarden.com/help/security-faqs/#q-how-do-i-validate-the-checksum-of-a-bitwarden-app

   ```
   sha256sum {ダウンロードした zip のpath}
   ```

   1. 出力されたハッシュ値が、公式サイトで公開されている SHA256 チェックサムと一致することを確認する
      1. `bw` は `https://github.com/bitwarden/clients/releases` で SHA256 チェックサムが公開されている

1. zip展開
1. 展開された `bw` バイナリをパスの通った適当な場所に移動（例: `/usr/local/bin`）

   ```bash
   sudo mv {`bw` バイナリのPATH} /usr/local/bin/
   ```

1. `bw` バイナリの権限許可

   ```bash
   chmod +x /usr/local/bin/bw
   ```

1. Bitwarden CLI でログイン

   ```bash
   $ bw login
   ```

   > Could not find dir, "/Users/fujisawakoki/Library/Application Support/Bitwarden CLI"; > creating it instead.
   > Could not find data file, "/Users/fujisawakoki/Library/Application Support/Bitwarden > CLI/data.json"; creating it instead.
   > ? Email address: [hidden]
   > ? Master password: [hidden]
   > ? Two-step login code: [hidden]
   > You are logged in!

1. 払い出されたセッションを環境変数に保存

   ```bash
   export BW_SESSION=$(bw unlock --raw)
   ```

> [MEMO]
>
> - node 環境整ったら pnpm などで -g で `bw` をインストールし直しておくのが吉

### memo: Bitwarden CLI の Util commands

- `bw sync`: Vault の最新状態を取得する
- `bw list items --search "{__search_word__}" | jq`: アイテムの一覧を表示する (IDの取得に便利)

### chezmoi のインストール

- Mac

```bash
brew install chezmoi
```

- Linux/Windows(WSL)

```bash
sh -c "$(curl -fsLS get.chezmoi.io)"
```

### 初期化と適用

これにより GitHub から設定が落とされ、~/.config/chezmoi/chezmoi.toml も自動生成されます

```bash
chezmoi init --apply --ssh melumuccu/dotfiles
```

---

## 📝 日常の操作

### ファイルを編集する

```bash
# 例: zshrc を編集
chezmoi edit ~/.zshrc
```

1. VS Code が立ち上がります。
1. 編集して保存し、**VS Code のタブを閉じます**。
1. 自動的に実ファイルへ反映 (`apply`) され、`commit` されます。
   1. `git push` は手動で行う必要があります。テンプレート管理しているファイルの内容を誤って公開するリスクを回避するためです。

### 他のマシンでの変更を取り込む

```bash
chezmoi update
```

### 管理ファイルを追加する

- テンプレートとして追加（推奨）

```bash
chezmoi add --template ~/.zshrc
```

### シンボリックリンクの管理

シンボリックリンク（例：`~/.vimrc`）を追加する場合、用途に合わせて以下のオプションを使い分けます。

#### 実体ファイルとして管理する（推奨）

リンクを解除し、その中身（テキスト）を `chezmoi` の管理下に置く方法です。テンプレート機能がフルに活用できます。

```bash
chezmoi add --follow ~/.vimrc
```

- **挙動**: `chezmoi apply` 実行時、ホームディレクトリのリンクは「実ファイル」に置き換わります。

#### リンクそのものを管理する

「常に特定のパスを指すリンクであってほしい」という状態を維持したい場合に使用します。

```bash
chezmoi add ~/.vimrc
```

- **挙動**: ソース内に `symlink_` プレフィックスが付いたファイルが作成され、リンク先のパスが記録されます。

#### ホームディレクトリ側にリンクを張る

実体は `chezmoi` のソースディレクトリ内に置き、ホームディレクトリ側にはそこへのシンボリックリンクを配置したい場合に使用します。

```bash
chezmoi add --symlink ~/.vimrc
```

---

## 💡 テンプレート管理戦略（使い分けのガイドライン）

`chezmoi` ではファイルをテンプレート（`.tmpl`）として管理することで柔軟性が上がりますが、特性を理解して使い分けるのがベストです。

### テンプレート化すべきファイル（`--template` を使う）

- **主要な設定ファイル**: `.zshrc`, `.gitconfig`, `.ssh/config` など。
- **理由**: OS ごとのパスの違い、ユーザー名、メールアドレスなどの変数を埋め込む必要があるため。

### テンプレート化を避けるべきファイル（通常通り `add` する）

- **プログラミングコード**: Python, Go などのソースファイル。
- **特定のツール設定**: `fzf` の設定など、ファイル自体が `{{ }}` 記法を使用しているもの。
- **理由**: `chezmoi` のテンプレート記法と衝突してパースエラーが発生するため。

### 既存ファイルをテンプレートに変更する方法

後からテンプレート化したくなった場合は、ソースディレクトリでリネームするだけで OK です。

```bash
chezmoi cd
mv dot_zshrc dot_zshrc.tmpl
```

---

## ⚙️ 核心の設定構造

本リポジトリでは `chezmoi` 自体の設定も管理しています。

### 設定ファイルの更新方法

```bash
code ~/.local/share/chezmoi/.chezmoi.toml.tmpl
```

### 動作設定 (`.chezmoi.toml.tmpl`)

ソースディレクトリの直下に配置されているこのファイルが、`chezmoi` の挙動を制御します。

- `edit.apply = true`: 編集完了時に即座に反映。
- `git.autoCommit = true`: 自動コミット。

### OSごとの出し分け

`.chezmoi.toml.tmpl` 内で以下のような条件分岐を使用し、OS間の差異を吸収しています。

```toml
{{- $editor := "code" -}}
{{- if eq .chezmoi.os "windows" -}}
    {{- $editor = "code.cmd" -}}
{{- end -}}
```

---

## 💡 トラブルシューティング

- **Git Push が失敗する場合**:
  `chezmoi cd` でソースディレクトリに入り、`ssh -T git@github.com` で認証が通っているか確認してください。
- **設定が反映されない場合**:
  `chezmoi.toml` 自体の設定を変更した後は、`chezmoi init` を実行して設定ファイルを再生成してください。
