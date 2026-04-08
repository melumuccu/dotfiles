function my_git_checkout_branch_fzf
    set -l branch (git branch --format='%(refname:short)' | fzf)
    or return 1

    test -n "$branch"
    or return 1

    git checkout $branch
    or return 1

    git pull
end
