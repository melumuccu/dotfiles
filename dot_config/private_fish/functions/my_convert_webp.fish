function my_convert_webp
    if test (count $argv) -ne 1
        echo '使い方: cw <path_to_file>'
        return 1
    end

    set -l input $argv[1]

    if test -d "$input"
        find "$input" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' \) -exec bash -c '
            for file; do
                dirname=$(dirname "$file")
                basename=$(basename "$file")
                filename="${basename%.*}"
                output="$dirname/$filename.webp"

                if [ "${file##*.}" = "webp" ]; then
                    echo "$file は既にwebp形式です。"
                else
                    cwebp "$file" -o "$output"
                    if [ $? -eq 0 ]; then
                        rm "$file"
                        echo "$file をwebpに変換しました。"
                    else
                        echo "$file のwebp変換に失敗しました。"
                    fi
                fi
            done
        ' _ {} +
        return $status
    end

    set -l dirname (dirname "$input")
    set -l basename (basename "$input")
    set -l filename (path change-extension '' "$basename")
    set -l extension (string lower -- (path extension "$basename" | string trim -l -c '.'))

    if test -z "$extension"
        echo 'ファイルの拡張子が特定できませんでした。'
        return 1
    end

    if test "$extension" = 'webp'
        echo "$input は既にwebp形式です。"
        return 1
    end

    set -l output "$dirname/$filename.webp"

    cwebp "$input" -o "$output"
    or begin
        echo "$input のwebp変換に失敗しました。"
        return 1
    end

    rm "$input"
    echo "$input をwebpに変換しました。"
end