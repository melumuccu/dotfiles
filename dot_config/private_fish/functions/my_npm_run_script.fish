function my_npm_run_script
    set -l script (jq -r '.scripts | keys[]' package.json | sort | fzf)
    or return 1

    npm run $script
end
