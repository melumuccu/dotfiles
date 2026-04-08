function my_git_rebase_interactive_head
    if test (count $argv) -ne 1
        echo 'Usage: grih <count>'
        return 1
    end

    git rebase -i HEAD~$argv[1]
end