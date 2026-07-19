#!/usr/bin/env bash
# Wrapper kept for compatibility; hooks.json invokes the Python script directly.
exec python3 "$(dirname "$0")/deny-dangerous-shell.py"
