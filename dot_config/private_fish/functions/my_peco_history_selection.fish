function my_peco_history_selection
    set -l selected (history | awk '!seen[$0]++' | peco)
    or return 1

    test -n "$selected"
    or return 1

    commandline -r -- $selected
    commandline -f repaint
end
