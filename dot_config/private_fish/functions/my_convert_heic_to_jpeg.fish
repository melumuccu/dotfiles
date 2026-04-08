function my_convert_heic_to_jpeg
    if test (count $argv) -ne 1
        echo 'Usage: ch <path_to_file>'
        return 1
    end

    set -l input_file $argv[1]
    set -l dirname (dirname "$input_file")
    set -l basename (basename "$input_file")
    set -l filename (path change-extension '' "$basename")
    set -l extension (string lower -- (path extension "$basename" | string trim -l -c '.'))

    if test "$extension" != 'heic'
        echo 'The file is not a HEIC format.'
        return 1
    end

    set -l output_file "$dirname/$filename.jpeg"

    magick convert "$input_file" "$output_file"
    or begin
        echo "Failed to convert $input_file to jpeg."
        return 1
    end

    echo "$input_file has been converted to"
    echo "$output_file"
end