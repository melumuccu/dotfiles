set -gx HOMEBREW_NO_AUTO_UPDATE 1

set -gx PNPM_HOME /Users/fujisawakoki/Library/pnpm

# fish_add_path の既定は prepend で、--append と混在させると
# 記述順と実際の PATH 優先順がずれやすい。
# さらに fish_user_paths は universal 変数として順序が残るため、
# 起動のたびにグローバル値を組み直してファイル順をそのまま優先順にする。
set -g fish_user_paths
fish_add_path -g --append /opt/homebrew/bin
fish_add_path -g --append $PNPM_HOME
fish_add_path -g --append /Users/fujisawakoki/.cache/lm-studio/bin
fish_add_path -g --append /Users/fujisawakoki/.antigravity/antigravity/bin

if status is-interactive
    if command -q mise
        mise activate fish | source
    end
end
