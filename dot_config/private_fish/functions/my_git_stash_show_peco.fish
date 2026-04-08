function my_git_stash_show_peco
    set -l selected (git stash list | peco)
    or return 1

    set -l stash_ref (string split -m1 ':' -- $selected)[1]
    test -n "$stash_ref"
    or return 1

    git stash show $stash_ref
end