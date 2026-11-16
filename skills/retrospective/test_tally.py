"""Self-check for tally.py with tiny synthetic transcripts: python3 -I test_tally.py"""

import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tally import tally  # noqa: E402


def write(lines):
    f = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
    f.write("\n".join(json.dumps(line) for line in lines))
    f.close()
    return pathlib.Path(f.name)


usage = {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 20}
claude = tally(write([
    {"type": "user", "timestamp": "t1", "message": {"content": "fix it"}},
    {"type": "user", "message": {"content": "<task-notification>x"}},
    # one request logged twice (two content blocks) must count once
    {"type": "assistant", "requestId": "r1", "message": {"usage": usage, "content": [{"type": "tool_use", "name": "Bash"}]}},
    {"type": "assistant", "requestId": "r1", "timestamp": "t2", "message": {"usage": usage, "content": []}},
]))
assert claude["requests"] == 1 and claude["output_tokens"] == 20, claude
assert claude["weighted"] == 10 + 200 + 100 + 100, claude
assert claude["tools"] == {"Bash": 1} and claude["user_prompts"] == ["fix it"], claude
assert (claude["started"], claude["ended"]) == ("t1", "t2"), claude

total = {"input_tokens": 1000, "cached_input_tokens": 800, "output_tokens": 50}
codex = tally(write([
    {"type": "event_msg", "timestamp": "t1", "payload": {"type": "user_message", "message": "fix it"}},
    {"type": "response_item", "payload": {"type": "function_call", "name": "shell"}},
    {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 1, "output_tokens": 1}}}},
    {"type": "event_msg", "payload": {"type": "token_count", "info": None}},
    {"type": "event_msg", "timestamp": "t2", "payload": {"type": "token_count", "info": {"total_token_usage": total}}},
]))
assert codex["input_tokens"] == 200 and codex["cache_read_input_tokens"] == 800, codex
assert codex["output_tokens"] == 50 and codex["tools"] == {"shell": 1}, codex
assert codex["user_prompts"] == ["fix it"], codex
print("ok")
