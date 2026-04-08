function my_git_delete_branch_peco
    set -l branch (git branch --format='%(refname:short)' | peco)
    or return 1

    test -n "$branch"
    or return 1

    git branch -d -- $branch
end