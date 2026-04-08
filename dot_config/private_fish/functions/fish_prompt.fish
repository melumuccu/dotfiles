function fish_prompt
    # 1. 前のコマンドとの間に空行を入れる
    echo ""

    # 2. 上段: パス表示
    set_color magenta
    echo -n "┬─[ "
    set_color cyan
    # echo -n (pwd)
    # $HOME（/Users/xxxxx）を ~ に置き換えて表示
    echo -n (string replace $HOME "~" (pwd))
    set_color magenta
    echo " ]"

    # 3. 中段: Gitブランチ表示 (Gitリポジトリ内のみ)
    # fish_vcs_prompt の出力を取得
    set -l git_info (fish_vcs_prompt | string trim)
    if test -n "$git_info"
        set_color magenta
        echo -n "├─[ "
        set_color yellow  # ブランチ名は目立つイエローに
        echo -n "$git_info"
        set_color magenta
        echo " ]"
    end

    # 4. 下段: 入力欄
    set_color magenta
    echo -n "╰─>"
    set_color normal
    echo -n " "
end
