#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

hook = Path(__file__).with_name("deny-dangerous-shell.py")
proc = subprocess.run(
    ["python3", str(hook)],
    input=json.dumps({"command": "psql -c 'SELECT 1'"}),
    capture_output=True,
    text=True,
    check=True,
)
payload = json.loads(proc.stdout)
assert payload["permission"] == "deny"
msg = payload["agent_message"]
for phrase in (
    "実行しようとした理由",
    "各フラグと引数についての項目別解説",
    "手動で実行するよう指示",
):
    assert phrase in msg, phrase
print("agent_message check OK")
