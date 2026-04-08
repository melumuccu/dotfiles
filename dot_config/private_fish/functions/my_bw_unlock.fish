function my_bw_unlock
    set -l session (bw unlock --raw)
    or return 1

    set -gx BW_SESSION $session
end
