#!/usr/bin/env python3
"""PostToolUse hook: append Agent tool invocations to agent-audit.log."""

import json
import sys
import os
from datetime import datetime

_HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
_CLAUDE_DIR = os.path.dirname(_HOOKS_DIR)
AUDIT_LOG = os.path.join(_CLAUDE_DIR, 'memory', 'agent-audit.log')


def main():
    raw = sys.stdin.read()
    # Debug: always write raw payload to tmp log regardless of tool_name
    try:
        debug_log = os.path.join(_CLAUDE_DIR, 'memory', 'agent-debug.log')
        os.makedirs(os.path.dirname(debug_log), exist_ok=True)
        with open(debug_log, 'a', encoding='utf-8') as f:
            f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] CWD={os.getcwd()} payload={raw[:200]}\n')
    except Exception:
        pass

    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get('tool_name') != 'Agent':
        sys.exit(0)

    tool_input = payload.get('tool_input', {})
    subagent_type = tool_input.get('subagent_type', 'general-purpose')
    description = tool_input.get('description', '(no description)')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(f'[{now}] Agent started: {subagent_type} — {description}\n')

    sys.exit(0)


if __name__ == '__main__':
    main()
