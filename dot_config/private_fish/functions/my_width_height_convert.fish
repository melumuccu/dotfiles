function my_width_height_convert
    if test (count $argv) -lt 2
        echo 'Usage: wh <path_to_image> <width> [height]'
        return 1
    end

    set -l input_file $argv[1]
    set -l width $argv[2]

    if test (count $argv) -ge 3
        set -l height $argv[3]
        magick convert "$input_file" -resize "$width"x"$height"'!' "$input_file"
        or return 1
        return 0
    end

    set -l aspect_ratio (identify -format '%[fx:h/w]' "$input_file")
    or return 1

    set -l scaled_height (math "$width * $aspect_ratio")
    set -l height (string split -m1 '.' -- $scaled_height)[1]

    magick convert "$input_file" -resize "$width"x"$height" "$input_file"
    or begin
        echo "Failed to resize $input_file."
        return 1
    end
end