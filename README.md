# dotfiles

[chezmoi](https://www.chezmoi.io/) + `GitHub CLI` + `VS Code` を組み合わせた dotfiles 管理リポジトリ

## 🚀 特徴
- **自動同期**: `chezmoi edit` で保存し VS Code を閉じると、自動で `apply` & `git push` されます。

## 🛠 セットアップ (新環境での復元手順)

### 1. GitHub CLI のインストールと認証
各 OS のパッケージマネージャで `gh` をインストール後、以下を実行：

```bash
# SSH で GitHub にログイン
gh auth login
# 1. What account do you want to log into? → GitHub.com
# 2. What is your preferred protocol for Git operations? → SSH (重要！)
# 3. Generate a new SSH key to upload to your GitHub account? → Yes
# 4. Enter a passphrase for your new SSH key → (空のままEnter またはパスフレーズを入力)
# 5. Title for your new SSH key → (そのままでOK)
# 6. How would you like to authenticate GitHub CLI? → Login with a web browser
```

```bash
# GitHubとのSSH接続テスト
ssh -T git@github.com

# 成功すれば "Hi [ユーザー名]! You've successfully authenticated..." と出ます
```
