"""
The agentic loop. This is the highest-weighted single rubric line (20 pts)
-- see GUIDE.md Part 2 before writing this, and read it closely, because
the brief explicitly warns against the most common failure mode: treating
a turn cap as the primary way the loop ends, or trying to parse the
model's natural-language text to decide when to stop.

Required shape (fill in around this skeleton):

    def run_conversation(user_message: str, max_turns: int = 8) -> list[dict]:
        messages = [{"role": "user", "content": user_message}]

        for turn in range(max_turns):
            response = client.messages.create(
                model=...,
                max_tokens=...,
                tools=TOOLS,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                break  # <-- normal termination
            elif response.stop_reason == "tool_use":
                # TODO: find every tool_use block in response.content
                # (there can be MORE THAN ONE -- this is exactly the
                # "multi-concern, single reply" requirement from the
                # brief, see GUIDE.md Part 5), dispatch each to its
                # handler, and append ONE user message containing a
                # tool_result block per tool_use, each carrying the
                # matching tool_use_id.
                pass
            elif response.stop_reason == "max_tokens":
                # TODO: this should be a raised/flagged condition, NOT a
                # silent break -- per the brief, the turn cap is a
                # labelled safety net, and max_tokens is a genuinely
                # different failure than "ran out of turns".
                pass
        else:
            # TODO: loop exhausted max_turns without an end_turn --
            # label this distinctly from a normal completion.
            pass

        return messages

Things to get right:
- Every tool_use block in a response must get exactly one matching
  tool_result (by tool_use_id) -- even if the tool call itself errors.
  Use tools.errors.error(...)'s return value as the tool_result content;
  never let a handler's exception propagate up into the loop (brief:
  "Do not raise errors into the loop").
- The turn cap (max_turns) is a safety net for genuinely stuck
  conversations, not how you expect well-behaved conversations to end.
- Dispatch tool_use blocks by name to the functions in tools/handlers.py.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

from tools.schemas import TOOLS

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"  # adjust if you're targeting a different model


def dispatch_tool_call(name: str, tool_input: dict) -> dict:
    """Route a single tool_use block to its handler. TODO."""
    # TODO: import from tools.handlers and match on `name`
    raise NotImplementedError


def run_conversation(user_message: str, max_turns: int = 8) -> list[dict]:
    """TODO: see the docstring above for the required shape."""
    raise NotImplementedError
