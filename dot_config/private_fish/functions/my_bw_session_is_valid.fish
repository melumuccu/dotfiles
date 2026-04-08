function my_bw_session_is_valid
    test -n "$BW_SESSION"
    or return 1

    bw --nointeraction --session "$BW_SESSION" list items --search __bw_session_probe__ >/dev/null 2>/dev/null
end
