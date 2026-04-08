if status is-interactive
    # README の Homebrew 前提に合わせて、fish 向け shell integration を
    # `fzf --fish | source` で読み込む。
    if command -q fzf
        fzf --fish | source
    end
end
