function my_git_checkout_branch_peco
    set -l branch (git branch --format='%(refname:short)' | peco)
    or return 1

    test -n "$branch"
    or return 1

    git checkout -- $branch
    or return 1

    git pull
end