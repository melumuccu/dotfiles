function my_cd_child_dir
    set -l dir (find . -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null | sed 's#^\./##' | fzf-tmux)
    or return 1

    builtin cd -- $dir
end
