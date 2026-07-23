# dotfiles

[chezmoi](https://www.chezmoi.io/) + `GitHub CLI` + `VS Code` dotfiles 管理リポジトリ

## Bitwarden シークレット管理 例

-> see: `dot_gitconfig.tmpl`

## 📝 日常操作

### Bitwarden

#### Vault 最新状態取得

```bash
bw sync
```

#### アイテム一覧表示 (ID取得)

```bash
bw list items --search "___KEYWORD___" | jq 'map({
      id,
      name,
      notes,
      login: {
        username: .login.username,
        password: .login.password
      },
      fields
    })'
```

#### アイテム表示 (ID逆引き)

```bash
bw get item ___ID___ | jq 'map({
      id,
      name,
      notes,
      login: {
        username: .login.username,
        password: .login.password
      },
      fields
    })'
```

#### セッション更新

```bash
export BW_SESSION=$(bw unlock --raw)
```

#### セッション破棄 (作業終了毎回)

```bash
bw lock
```

### chezmoi

#### ファイル編集

```bash
# 例: zshrc 編集
chezmoi edit ~/.zshrc

-> alias: `czed`
```

1. VS Code 起動
1. 編集 → 保存 → **VS Code タブ閉じ**
1. 自動 実ファイル反映 (`apply`) + `commit`
   1. `git push` 手動必須 → テンプレート管理ファイル 誤公開リスク回避

#### 管理対象追加

```bash
chezmoi add <PATH>

-> alias: `czad`
```

#### 既存管理対象の変更commit

```bash
chezmoi re-add

-> alias: `czre`
```

#### 他マシン 変更取込

```bash
chezmoi update

-> alias: `czpl`
```

#### テンプレートファイル追加

```bash
chezmoi add --template ~/.zshrc
```

## シンボリックリンク管理

シンボリックリンク（例：`~/.vimrc`）追加 → 用途別 オプション使い分け

### 実体ファイル管理（推奨）

リンク解除 → 中身（テキスト）を `chezmoi` 管理下へ。テンプレート機能 フル活用

```bash
chezmoi add --follow ~/.vimrc
```

- **挙動**: `chezmoi apply` → ホームディレクトリ リンク → 実ファイル置換

### リンク自体 管理

常に特定パス指すリンク 維持

```bash
chezmoi add ~/.vimrc
```

- **挙動**: ソース内 `symlink_` プレフィックス付きファイル作成 + リンク先パス記録

### ホームディレクトリ側 リンク張り

実体 → `chezmoi` ソースディレクトリ内。ホーム側 → そこへのシンボリックリンク

```bash
chezmoi add --symlink ~/.vimrc
```

---

## 💡 テンプレート管理戦略

`chezmoi` ファイル テンプレート（`.tmpl`）管理 → 柔軟性向上。特性理解 + 使い分け 推奨

### テンプレート化 推奨（`--template`）

- **主要設定ファイル**: `.zshrc`, `.gitconfig`, `.ssh/config` 等
- **理由**: OS別パス差異 / ユーザー名 / メールアドレス → 変数埋込 必要

### テンプレート化 回避（通常 `add`）

- **プログラミングコード**: Python, Go 等ソース
- **特定ツール設定**: `fzf` 設定等、ファイル自体 `{{ }}` 記法使用
- **理由**: `chezmoi` テンプレート記法 衝突 → パースエラー

### 既存ファイル → テンプレート化

ソースディレクトリ リネームのみ

```bash
chezmoi cd
mv dot_zshrc dot_zshrc.tmpl
```

### テンプレート 実行結果確認

[例]

```bash
chezmoi execute-template < ~/.local/share/chezmoi/.chezmoiignore.tmpl
```

---

## ⚙️ chezmoi 設定

本リポジトリ `chezmoi` 自体設定 も管理

### 設定ファイル 更新

```bash
code ~/.local/share/chezmoi/.chezmoi.toml.tmpl
```

### 動作設定 (`.chezmoi.toml.tmpl`)

ソースディレクトリ直下 → `chezmoi` 挙動制御

- `edit.apply = true`: 編集完了 → 即反映
- `merge.command` / `merge.args`: `chezmoi merge` 競合解決 → VS Code
- `git.autoCommit = true`: 自動コミット

### OS別 出し分け

`.chezmoi.toml.tmpl` 条件分岐 → OS間差異 吸収

```toml
{{- $editor := "code" -}}
{{- if eq .chezmoi.os "windows" -}}
    {{- $editor = "code.cmd" -}}
{{- end -}}
```

---

## 🛠 新環境 セットアップ

### GitHub CLI インストール・認証

1. `gh` インストール

   ```bash
   brew install gh
   ```

1. GitHub ログイン (SSH)

   ```bash
   gh auth login
   ```

   1. What account do you want to log into? → GitHub.com
   1. What is your preferred protocol for Git operations? → SSH (重要！)
   1. Generate a new SSH key to upload to your GitHub account? → Yes
   1. Enter a passphrase for your new SSH key → (空Enter or パスフレーズ入力)
   1. Title for your new SSH key → (そのままOK)
   1. How would you like to authenticate GitHub CLI? → Login with a web browser

1. ブラウザ URL アクセス → ターミナル表示コード入力 → 認証完了
1. GitHub SSH接続テスト
1. 成功 → "Hi [ユーザー名]! You've successfully authenticated..." 表示

   ```bash
   ssh -T git@github.com
   ```

### Bitwarden CLI インストール・認証

[公式Docs](https://bitwarden.com/help/cli/)

1. 公式サイトから `bw` インストール
   1. see: https://bitwarden.com/help/cli/#download-and-install
1. checksum 検証
   1. see: https://bitwarden.com/help/security-faqs/#q-how-do-i-validate-the-checksum-of-a-bitwarden-app

   ```
   sha256sum {ダウンロードした zip のpath}
   ```

   1. 出力ハッシュ = 公式公開 SHA256 チェックサム 一致確認
      1. `bw` SHA256 → `https://github.com/bitwarden/clients/releases` 公開

1. zip展開
1. 展開 `bw` バイナリ → PATH通った場所へ移動（例: `/usr/local/bin`）

   ```bash
   sudo mv {`bw` バイナリのPATH} /usr/local/bin/
   ```

1. `bw` バイナリ 権限許可

   ```bash
   chmod +x /usr/local/bin/bw
   ```

1. Bitwarden CLI ログイン

   ```bash
   bw login
   ```

   > Could not find dir, "/Users/fujisawakoki/Library/Application Support/Bitwarden CLI"; > creating it instead.
   > Could not find data file, "/Users/fujisawakoki/Library/Application Support/Bitwarden > CLI/data.json"; creating it instead.
   > ? Email address: [hidden]
   > ? Master password: [hidden]
   > ? Two-step login code: [hidden]
   > You are logged in!

1. 払い出しセッション → 環境変数保存

   ```bash
   export BW_SESSION=$(bw unlock --raw)
   ```

### chezmoi インストール

- Mac

```bash
brew install chezmoi
```

- Linux/Windows(WSL)

```bash
sh -c "$(curl -fsLS get.chezmoi.io)"
```

### 初期化・適用

→ GitHub 設定取得 + `~/.config/chezmoi/chezmoi.toml` 自動生成

```bash
chezmoi init --apply --ssh melumuccu/dotfiles
```

### (任意) 特定ディレクトリ シンボリックリンク

- Why?: Raycast 等ランチャー アクセス容易化
- ex. projects ディレクトリ リンク

```bash
ln -s ~/.local/share/chezmoi ~/projects/chezmoi
```

---

## 💡 トラブルシューティング

- **Git Push 失敗**:
  `chezmoi cd` → ソースディレクトリ → `ssh -T git@github.com` 認証確認
- **設定 反映されない**:
  `chezmoi.toml` 設定変更後 → `chezmoi init` → 設定ファイル再生成
