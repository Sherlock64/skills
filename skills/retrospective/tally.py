"""Token and tool tally for one agent session, for the retrospective skill.

Usage: python3 -I tally.py <session.jsonl> [subagent.jsonl ...]
Reads a Claude Code or Codex transcript and prints JSON. For Claude, subagents in the
<session-id>/subagents/ folder next to it are found automatically; for Codex, pass them.
"""

import collections
import json
import pathlib
import sys

FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
# Rough price weights relative to uncached input: cache write 2x, cache read 0.1x, output 5x.
WEIGHTS = {"input_tokens": 1, "cache_creation_input_tokens": 2, "cache_read_input_tokens": 0.1, "output_tokens": 5}


def weighted(summary):
    return round(sum(summary[field] * weight for field, weight in WEIGHTS.items()))


def tally(path):
    """Usage, tool counts, user prompts and times for one transcript, either format."""
    usage_by_request = {}  # Claude: a request is logged once per content block
    codex_total = None  # Codex: token_count events carry a running total
    tools = collections.Counter()
    user_prompts = []
    first = last = None
    for line in path.open():
        entry = json.loads(line)
        stamp = entry.get("timestamp")
        if stamp:
            first = first or stamp
            last = stamp
        payload = entry.get("payload") or {}
        message = entry.get("message") or {}
        kind = entry.get("type")
        if kind == "assistant":
            usage_by_request[entry.get("requestId") or entry.get("uuid")] = message.get("usage") or {}
            for block in message.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tools[block["name"]] += 1
        elif kind == "user" and not entry.get("isMeta") and isinstance(message.get("content"), str):
            if not message["content"].startswith(("<task-notification>", "<bash-input>")):
                user_prompts.append(message["content"][:300])
        elif kind == "event_msg" and payload.get("type") == "token_count":
            codex_total = ((payload.get("info") or {}).get("total_token_usage")) or codex_total
        elif kind == "event_msg" and payload.get("type") == "user_message":
            user_prompts.append(str(payload.get("message", ""))[:300])
        elif kind == "response_item" and payload.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
            tools[payload.get("name") or payload["type"]] += 1
    if codex_total is not None:
        cached = codex_total.get("cached_input_tokens", 0)
        totals = {
            "input_tokens": codex_total.get("input_tokens", 0) - cached,  # Codex input includes cached
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": cached,
            "output_tokens": codex_total.get("output_tokens", 0),
        }
        requests = None  # Codex logs no per-request ids
    else:
        totals = {field: sum(u.get(field, 0) for u in usage_by_request.values()) for field in FIELDS}
        requests = len(usage_by_request)
    return {
        "requests": requests,
        **totals,
        "weighted": weighted(totals),
        "tools": dict(tools.most_common()),
        "user_prompts": user_prompts,
        "started": first,
        "ended": last,
    }


def subagent(transcript, meta):
    summary = tally(transcript)
    del summary["user_prompts"]  # the organizer's prompt, already in the main transcript
    return {"type": meta.get("agentType"), "description": meta.get("description"), "file": transcript.name, **summary}


def main():
    session = pathlib.Path(sys.argv[1])
    agents = []
    for transcript in sorted((session.parent / session.stem / "subagents").glob("*.jsonl")):
        meta_path = transcript.with_suffix(".meta.json")
        agents.append(subagent(transcript, json.loads(meta_path.read_text()) if meta_path.exists() else {}))
    agents += [subagent(pathlib.Path(p), {}) for p in sys.argv[2:]]
    main_summary = tally(session)
    grand = {field: main_summary[field] + sum(a[field] for a in agents) for field in FIELDS}
    grand["weighted"] = weighted(grand)
    print(json.dumps({"main": main_summary, "subagents": agents, "total": grand}, indent=1))


if __name__ == "__main__":
    main()
