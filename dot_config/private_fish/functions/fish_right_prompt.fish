function fish_right_prompt
    # Gitのブランチ情報を表示 (標準機能を利用)
    # set_color magenta
    # fish_vcs_prompt
    # set_color normal

    if test -n (commandline -b)
        return
    end

    set_color brblack
    echo -n '⌃G AI  ⌃R history'
    set_color normal
end
