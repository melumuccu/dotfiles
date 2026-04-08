function my_ai_gen
    # 現在の入力内容を取得
    set -l current_buffer (commandline -b)

    # 入力が空なら何もしない
    if test -z "$current_buffer"
        return
    end

    # 「考え中」であることを表示（ユーザー体験のため）
    echo -n " ...AI思考中..."
    # システムプロンプトで「コマンドのみを出力し、解説は一切不要」と厳命するのがコツ
    set -l prompt "You are a shell command expert. Translate the following natural language request into a single executable macOS fish shell command. Output ONLY the command code. Do not output <think> tags, internal reasoning, markdown, explanations, or code fences. Request: $current_buffer"

    # Gemini APIを叩く
    # set -l payload (jq -n --arg prompt "$prompt" '{contents:[{parts:[{text:$prompt}]}]}')
    # set -l response (curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent" \
    #     -H "Content-Type: application/json" \
    #     -H "X-goog-api-key: $GOOGLE_API_KEY" \
    #     -d "$payload")

    # Groq APIを叩く
    set -l payload (jq -n \
        --arg prompt "$prompt" \
        '{
            messages: [
                {
                    role: "user",
                    content: $prompt
                }
            ],
            "model": "qwen/qwen3-32b",
            "temperature": 0.6,
            "max_completion_tokens": 4096,
            "top_p": 0.95,
            "stream": false,
            "reasoning_effort": "default",
            "stop": null
        }')

    set -l response (curl -s "https://api.groq.com/openai/v1/chat/completions" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -d "$payload")

    # JSONからテキスト部分を抽出
    # set -l ai_command (echo $response | jq -r '.candidates[0].content.parts[0].text' | string trim)
    set -l ai_command_raw (printf '%s\n' "$response" | jq -r '.choices[0].message.content // empty' | string collect)
    set -l ai_command_without_think (string replace -r '(?is)<think>.*?</think>' '' -- "$ai_command_raw" | string collect)
    set -l ai_command (string trim -- "$ai_command_without_think")
    set -l ai_error (printf '%s\n' "$response" | jq -r '.error.message // empty' | string trim)

    # 万が一エラーや空だった場合の処理
    if test -n "$ai_command" -a "$ai_command" != "null"
        # 現在の行をAIの回答で置き換え
        commandline -r "$ai_command"
        commandline -f repaint
    else
        if test -n "$ai_error"
            echo " エラー: $ai_error"
        else
            echo " エラー: AIから回答を得られませんでした"
        end
        commandline -f repaint
    end
end
