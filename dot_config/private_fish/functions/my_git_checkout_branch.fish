function my_git_checkout_branch
    set -l selected (git for-each-ref refs/heads --sort=refname --format='%(refname:short)\t%(objectname:short)\t%(upstream:short)\t%(subject)' | fzf +m)
    or return 1

    set -l branch (printf '%s\n' "$selected" | cut -f1)
    test -n "$branch"
    or return 1

    git checkout -- $branch
end
