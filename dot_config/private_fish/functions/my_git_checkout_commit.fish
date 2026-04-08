function my_git_checkout_commit
    set -l selected (git log --pretty=oneline --abbrev-commit --reverse | fzf --tac +s +m -e)
    or return 1

    set -l commit (string split ' ' -- $selected)[1]
    test -n "$commit"
    or return 1

    git checkout $commit
end
