function my_bw_ensure_session
    my_bw_session_is_valid
    and return 0

    my_bw_unlock
    or return 1

    my_bw_session_is_valid
end
