#!/usr/bin/env python3
"""beforeShellExecution hook: deny-list + deny patterns (default allow)."""

import json
import re
import shlex
import sys

DENY_CMDS = frozenset(
    {
        # privilege escalation
        "sudo",
        "su",
        "doas",
        # shell interpreters
        "bash",
        "sh",
        "dash",
        "zsh",
        "fish",
        "ksh",
        # network clients
        "curl",
        "wget",
        "http",
        "httpie",
        "nc",
        "netcat",
        "nmap",
        # remote access
        "ssh",
        "scp",
        "sftp",
        "telnet",
        # disk / system destruction
        "dd",
        "mkfs",
        "mkfs.ext4",
        "mkfs.xfs",
        "wipefs",
        "parted",
        "fdisk",
        "diskutil",
        # system power / services
        "shutdown",
        "reboot",
        "halt",
        "poweroff",
    }
)

DB_CLIENT_CMDS = frozenset(
    {
        "psql",
        "mysql",
        "mariadb",
        "mongosh",
        "mongo",
        "redis-cli",
        "sqlite3",
    }
)

SQL_PAYLOAD_FLAGS = frozenset(
    {
        "-c",
        "-e",
        "--execute",
        "--eval",
        "-q",
        "--query",
    }
)

DANGEROUS_SQL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bDROP\s+(DATABASE|SCHEMA|TABLE)\b", re.I), "SQL DROP"),
    (re.compile(r"\bTRUNCATE(\s+TABLE)?\b", re.I), "SQL TRUNCATE"),
    (re.compile(r"\bALTER\s+(DATABASE|TABLE)\b.*\bDROP\b", re.I), "SQL ALTER DROP"),
    (re.compile(r"\bdropDatabase\s*\(", re.I), "MongoDB dropDatabase"),
    (re.compile(r"\bdb\.[A-Za-z_][\w$]*\.drop\s*\(", re.I), "MongoDB collection drop"),
    (re.compile(r"\bFLUSH(ALL|DB)\b", re.I), "Redis flush"),
]

DENY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f|rm\s+-[a-zA-Z]*f[a-zA-Z]*r"), "recursive rm"),
    (re.compile(r"\brm\s+-rf\b"), "rm -rf"),
    (re.compile(r"find\s+.*-delete"), "find -delete"),
    (re.compile(r"xargs\s+rm\b"), "xargs rm"),
    (re.compile(r"git\s+push\s+.*(-f|--force)"), "git force push"),
    (re.compile(r"git\s+reset\s+--hard"), "git reset --hard"),
    (re.compile(r"git\s+clean\s+-f"), "git clean -f"),
    (re.compile(r"git\s+branch\s+-D"), "git branch -D"),
    (re.compile(r"git\s+filter-(branch|repo)"), "git history rewrite"),
    (re.compile(r"git\s+push\b.*\b(main|master)\b.*(-f|--force)"), "force push to main/master"),
    (re.compile(r"--no-verify|--no-gpg-sign"), "hook bypass flag"),
    (re.compile(r"curl\s+.*\|\s*(ba)?sh\b"), "curl pipe to shell"),
    (re.compile(r"wget\s+.*\|\s*(ba)?sh\b"), "wget pipe to shell"),
    (re.compile(r"curl\s+.*\|\s*(python|python3|node)\b"), "curl pipe to interpreter"),
    (re.compile(r"wget\s+.*\|\s*(python|python3|node)\b"), "wget pipe to interpreter"),
    (
        re.compile(r"bash\s+<\(curl|bash\s+<\(wget|source\s+<\(curl|source\s+<\(wget"),
        "process substitution remote exec",
    ),
    (re.compile(r"(?<![-\w])eval\s+", re.I), "eval"),
    (re.compile(r"docker\s+system\s+prune", re.I), "docker system prune"),
    (re.compile(r"docker\s+volume\s+(rm|prune)", re.I), "docker volume delete"),
    (re.compile(r"docker\s+compose\s+down\s+.*-v", re.I), "docker compose down -v"),
    (re.compile(r"docker\s+rm\s+-f", re.I), "docker rm -f"),
    (re.compile(r"kubectl\s+delete", re.I), "kubectl delete"),
    (re.compile(r"helm\s+uninstall", re.I), "helm uninstall"),
    (re.compile(r"terraform\s+destroy", re.I), "terraform destroy"),
    (re.compile(r"terraform\s+apply\s+.*-auto-approve", re.I), "terraform auto-approve"),
    (re.compile(r"aws\s+s3\s+rm\s+.*--recursive", re.I), "aws s3 recursive delete"),
    (re.compile(r"wrangler\s+delete", re.I), "wrangler delete"),
    (re.compile(r"gcloud\s+.*\sdelete", re.I), "gcloud delete"),
    (re.compile(r"az\s+group\s+delete", re.I), "az group delete"),
    (re.compile(r"npm\s+publish\b"), "npm publish"),
    (re.compile(r"npm\s+install\s+-g\b"), "npm global install"),
    (re.compile(r"pip\s+install\s+.*--break-system-packages"), "pip break-system-packages"),
    (re.compile(r"cargo\s+publish\b"), "cargo publish"),
    (re.compile(r"\bsudo\s+"), "sudo"),
    (re.compile(r"\bsu\s+-"), "su"),
    (re.compile(r"dd\s+if=.*of=/dev/", re.I), "dd to device"),
    (re.compile(r"\b(mkfs|wipefs|parted)\b"), "disk format tool"),
    (re.compile(r"chmod\s+-R\s+777"), "chmod 777 recursive"),
    (re.compile(r"chown\s+-R\s+(/|~|\$HOME)"), "chown recursive system path"),
    (re.compile(r":\(\)\s*\{"), "fork bomb"),
    (re.compile(r"while\s+true\s*;"), "infinite loop"),
    (re.compile(r"\b(shutdown|reboot|halt|poweroff)\b"), "system power"),
    (re.compile(r"kill\s+-9\s+1\b"), "kill init"),
    (re.compile(r"killall\s+-9\b"), "killall -9"),
    (re.compile(r"launchctl\s+unload", re.I), "launchctl unload"),
    (re.compile(r"systemctl\s+(stop|disable)", re.I), "systemctl stop/disable"),
    (re.compile(r"crontab\s+-r"), "crontab remove all"),
    (re.compile(r"~\/.ssh\/id_(rsa|ed25519)"), "SSH private key read"),
    (re.compile(r"cat\s+.*\.aws/credentials"), "AWS credentials read"),
    (re.compile(r"printenv\s*\|"), "env dump pipe"),
    (re.compile(r"env\s*\|"), "env dump pipe"),
    (re.compile(r"prisma\s+migrate\s+reset", re.I), "prisma migrate reset"),
    (re.compile(r"rails\s+db:drop", re.I), "rails db:drop"),
    (re.compile(r"django-admin\s+flush", re.I), "django flush"),
]

SEGMENT_SPLIT = re.compile(r"\s*(?:;|&&|\|\||\|)\s*")


def basename(token: str) -> str:
    token = token.lstrip("\\")
    return token.rsplit("/", 1)[-1]


def split_segments(command: str) -> list[str]:
    return [part.strip() for part in SEGMENT_SPLIT.split(command) if part.strip()]


def first_command_name(segment: str) -> str | None:
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        return None

    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token == "env":
            index += 1
            while index < len(tokens) and "=" in tokens[index] and not tokens[index].startswith("-"):
                index += 1
            if index < len(tokens):
                return basename(tokens[index])
            return None

        if token == "command" and index + 1 < len(tokens):
            return basename(tokens[index + 1])

        if "=" in token and not token.startswith("-") and not token.startswith("="):
            index += 1
            continue

        return basename(token)

    return None


def extract_db_client_payloads(segment: str, client: str) -> list[str]:
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        return []

    payloads: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token in SQL_PAYLOAD_FLAGS:
            if index + 1 < len(tokens):
                payloads.append(tokens[index + 1])
            index += 2
            continue

        if token.startswith("--execute=") or token.startswith("--eval="):
            payloads.append(token.split("=", 1)[1])
            index += 1
            continue

        index += 1

    if client == "redis-cli":
        for token in tokens[1:]:
            if token.startswith("-"):
                continue
            if token in SQL_PAYLOAD_FLAGS:
                continue
            payloads.append(token)

    if client == "sqlite3":
        positional = [token for token in tokens[1:] if not token.startswith("-")]
        if len(positional) >= 2:
            payloads.append(positional[-1])

    return payloads


def dangerous_sql_reason(segment: str) -> str | None:
    client = first_command_name(segment)
    if client not in DB_CLIENT_CMDS:
        return None

    texts = extract_db_client_payloads(segment, client)
    texts.append(segment)

    for text in texts:
        for pattern, reason in DANGEROUS_SQL_PATTERNS:
            if pattern.search(text):
                return reason

    return None


MANUAL_EXECUTION_AGENT_INSTRUCTIONS = """\
このシェルコマンドはセキュリティフックによってブロックされており再試行は許可されていません。

ユーザーに対し、ブロックされたコマンドを各自のターミナルで手動で実行するよう指示してください。\
指示する際には、以下の情報をすべてメッセージに含める必要があります：

1. 当該コマンドを実行しようとした理由（目的、使用環境、および達成しようとした内容）
2. コマンドの詳細な説明と、実行された場合に生じる影響（副次的効果、対象ファイル/リソース、および変更の可逆性を含む）
3. コマンドで使用されている各フラグと引数についての項目別解説

許可された安全な代替手段で同じ目的を達成できる場合を除き、別のコマンドに置き換えてはなりません。\
安全な代替手段が存在しない場合は、ユーザーがブロックされたコマンドを実行し、その結果を報告するのを待ってください。\
"""


def deny(reason: str, command: str) -> None:
    payload = {
        "permission": "deny",
        "user_message": (
            f"セキュリティポリシーによりシェルコマンドがブロックされました ({reason}). "
            "エージェントから、必要に応じて手動で実行するよう指示があります。"
        ),
        "agent_message": (
            f"コマンドは deny-dangerous-shell.py によってブロックされました ({reason}). "
            f"ブロックされたコマンド: {command!r}\n\n"
            f"{MANUAL_EXECUTION_AGENT_INSTRUCTIONS}"
        ),
    }
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(0)


def allow() -> None:
    print('{"permission":"allow"}')
    sys.exit(0)


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        deny("invalid hook input JSON", raw[:200])

    command = payload.get("command", "")
    if not isinstance(command, str) or not command.strip():
        deny("empty command", str(command))

    command = command.strip()

    for pattern, reason in DENY_PATTERNS:
        if pattern.search(command):
            deny(reason, command)

    segments = split_segments(command)
    if not segments:
        deny("unparseable command", command)

    for segment in segments:
        name = first_command_name(segment)
        if name is None:
            deny("unparseable command segment", segment)
        if name in DENY_CMDS:
            deny(f"command on deny list ({name})", command)
        sql_reason = dangerous_sql_reason(segment)
        if sql_reason is not None:
            deny(sql_reason, command)

    allow()


if __name__ == "__main__":
    main()
