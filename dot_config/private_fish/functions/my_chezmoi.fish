function my_chezmoi
    my_bw_ensure_session
    or return 1

    chezmoi $argv
end
