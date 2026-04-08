if status is-interactive
    # README の Homebrew 前提に合わせて、fish 向け shell integration を
    # `fzf --fish | source` で読み込む。
    # ローカルの fzf 0.60.3 では FZF_CTRL_R_COMMAND を空にしても
    # Ctrl-R の生成を止められないため、最終的な Ctrl-R は
    # 300-keybindings.fish 側で peco ベースに上書きする。
    if command -q fzf
        set -lx FZF_CTRL_R_COMMAND ''
        fzf --fish | source
    end
end
