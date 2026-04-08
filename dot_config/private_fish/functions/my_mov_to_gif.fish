function my_mov_to_gif
    if test (count $argv) -ne 1
        echo 'Usage: movtogif <path_to_file>'
        return 1
    end

    set -l filepath $argv[1]
    set -l dirpath (dirname "$filepath")
    set -l filename (basename "$filepath" .mov)
    set -l output_dir "$dirpath/output"
    set -l output_file "$output_dir/$filename.gif"

    if not test -d "$output_dir"
        mkdir -p "$output_dir"
    end

    ffmpeg -i "$filepath" -r 12 "$output_file"
    or return 1

    open -a '/Applications/Google Chrome.app' "$output_file"
end
