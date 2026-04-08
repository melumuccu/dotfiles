function my_git_stash_drop_fzf
    set -l selected (git stash list | fzf)
    or return 1

    set -l stash_ref (string split -m1 ':' -- $selected)[1]
    test -n "$stash_ref"
    or return 1

    git stash drop $stash_ref
end