#!/usr/bin/env python3
"""Cursor hook stdin/stdout helpers."""

from __future__ import annotations

import json
import sys


def allow() -> None:
    print("{}")
    sys.exit(0)


def empty() -> None:
    print("{}")
    sys.exit(0)


def followup(message: str) -> None:
    print(json.dumps({"followup_message": message}, ensure_ascii=False))
    sys.exit(0)


def deny_payload(user_message: str, agent_message: str) -> dict[str, str]:
    return {
        "permission": "deny",
        "user_message": user_message,
        "agent_message": agent_message,
    }


def deny(user_message: str, agent_message: str) -> None:
    print(json.dumps(deny_payload(user_message, agent_message), ensure_ascii=False))
    sys.exit(0)
