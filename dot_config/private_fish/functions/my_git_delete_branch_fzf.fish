function my_git_delete_branch_fzf
    set -l branch (git branch --format='%(refname:short)' | fzf)
    or return 1

    test -n "$branch"
    or return 1

    git branch -d -- $branch
end