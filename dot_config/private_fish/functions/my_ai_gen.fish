function __my_ai_gen_sanitize_command -a raw
    set -l cleaned (string trim -- "$raw")
    set -l think_open (string join '' '<' 'think' '>')
    set -l think_close (string join '' '<' '/' 'think' '>')
    set -l think_pattern (string join '' '(?is)' $think_open '.*?' $think_close)
    set -l cleaned (string replace -ra '(?is)<think>.*?</think>' '' -- "$cleaned" | string collect)
    set -l cleaned (string replace -ra $think_pattern '' -- "$cleaned" | string collect)
    if string match -qr '(?s)^```' -- "$cleaned"
        set cleaned (string replace -ra '(?ms)^```(?:fish|bash|sh|zsh)?\s*\r?\n([\s\S]*?)\r?\n```\s*$' '$1' -- "$cleaned" | string collect)
    end
    string trim -- "$cleaned"
end

function __my_ai_gen_build_payload -a model prompt
    if string match -qr 'qwen/' -- "$model"
        jq -n \
            --arg prompt "$prompt" \
            --arg model "$model" \
            '{
                messages: [{role: "user", content: $prompt}],
                model: $model,
                temperature: 0.1,
                max_completion_tokens: 512,
                top_p: 0.95,
                stream: false,
                reasoning_effort: "none"
            }'
    else
        jq -n \
            --arg prompt "$prompt" \
            --arg model "$model" \
            '{
                messages: [{role: "user", content: $prompt}],
                model: $model,
                temperature: 0.1,
                max_completion_tokens: 512,
                top_p: 0.95,
                stream: false,
                include_reasoning: false
            }'
    end
end

function my_ai_gen
    set -l current_buffer (commandline -b)

    if test -z "$current_buffer"
        return
    end

    if test -z "$GROQ_API_KEY"
        __fish_echo echo "my_ai_gen: GROQ_API_KEY 未設定"
        commandline -r -- $current_buffer
        commandline -f repaint
        return 1
    end

    set -l model (set -q GROQ_AI_GEN_MODEL; and echo $GROQ_AI_GEN_MODEL; or echo "openai/gpt-oss-20b")

    set -l prompt "You are a shell command expert. Translate the following natural language request into a single executable macOS fish shell command. Output ONLY one command line. No think tags, no markdown, no explanations, no code fences. Request: $current_buffer"

    set -l payload (__my_ai_gen_build_payload "$model" "$prompt")

    set -l response
    set -l curl_status 0
    set response (curl -sS --max-time 30 "https://api.groq.com/openai/v1/chat/completions" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -d "$payload")
    set curl_status $status

    if test $curl_status -ne 0
        commandline -r -- $current_buffer
        __fish_echo echo "my_ai_gen エラー: Groq API への接続失敗 (curl exit $curl_status)"
        commandline -f repaint
        return 1
    end

    set -l ai_command_raw (printf '%s\n' "$response" | jq -r '.choices[0].message.content // empty' 2>/dev/null | string collect)
    set -l ai_command (__my_ai_gen_sanitize_command "$ai_command_raw")
    set -l ai_error (printf '%s\n' "$response" | jq -r '.error.message // empty' 2>/dev/null | string trim)
    set -l finish_reason (printf '%s\n' "$response" | jq -r '.choices[0].finish_reason // empty' 2>/dev/null | string trim)

    if set -q GROQ_AI_GEN_DEBUG
        __fish_echo echo "my_ai_gen debug: model=$model raw=[$ai_command_raw] cleaned=[$ai_command] reason=$finish_reason"
    end

    if test -n "$ai_command" -a "$ai_command" != "null"
        commandline -r -- $ai_command
        commandline -f repaint
    else
        commandline -r -- $current_buffer
        if test -n "$ai_error"
            __fish_echo echo "my_ai_gen エラー: $ai_error"
        else if test "$finish_reason" = "length"
            __fish_echo echo "my_ai_gen エラー: 出力トークン上限到達 (finish_reason=length)"
        else if test -n "$ai_command_raw"
            __fish_echo echo "my_ai_gen エラー: 応答のサニタイズ後に空になりました"
        else
            __fish_echo echo "my_ai_gen エラー: AIからコマンドを得られませんでした (finish_reason=$finish_reason)"
        end
        commandline -f repaint
        return 1
    end
end
