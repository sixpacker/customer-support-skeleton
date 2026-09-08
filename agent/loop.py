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

import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv

from tools.schemas import TOOLS
from tools.errors import error
from tools.handlers import get_customer, lookup_order, process_refund, escalate_to_human

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"  # adjust if you're targeting a different model


def dispatch_tool_call(name: str, tool_input: dict) -> dict:
    """Route a single tool_use block to its handler."""
    if name == "get_customer":
        email = tool_input["email"]
        zip_code = tool_input["zip_code"]
        try:
            return get_customer(email, zip_code)
        except Exception as e:
            return error("business", str(e), False)
    elif name == "lookup_order":
        order_id = tool_input["order_id"]
        customer_id = tool_input["customer_id"]
        try:
            return lookup_order(order_id, customer_id)
        except Exception as e:
            return error("business", str(e), False)
    elif name == "process_refund":
        order_id = tool_input["order_id"]
        customer_id = tool_input["customer_id"]
        # NOTE: the schema's field is "refund_amount" (see tools/schemas.py),
        # but the handler's stub parameter is named "amount" -- translate
        # here, or rename the handler param to match when you write Part 3.
        amount = tool_input["refund_amount"]
        try:
            return process_refund(order_id, customer_id, amount)
        except Exception as e:
            return error("business", str(e), False)
    elif name == "escalate_to_human":
        # required per the schema:
        customer_id = tool_input["customer_id"]
        customer_name = tool_input["customer_name"]
        reason = tool_input["reason"]
        # optional per the schema -- .get() so a missing key doesn't KeyError:
        order_id = tool_input.get("order_id")
        order_amount = tool_input.get("order_amount")
        requested_refund_amount = tool_input.get("requested_refund_amount")
        try:
            # NOTE: tools/handlers.py's current stub signature only takes
            # (customer_id, order_id, reason) -- it needs to be extended in
            # Part 3 to accept customer_name/order_amount/
            # requested_refund_amount too, so the ticket is actually
            # self-sufficient per what you designed in Part 1.
            return escalate_to_human(
                customer_id=customer_id,
                customer_name=customer_name,
                order_id=order_id,
                order_amount=order_amount,
                reason=reason,
                requested_refund_amount=requested_refund_amount,
            )
        except Exception as e:
            return error("business", str(e), False)
    else:
        return error("validation", f"unknown tool: {name}", False)


def run_conversation(user_message: str, max_turns: int = 8) -> list[dict]:
    """Run the agentic loop until Claude signals end_turn, max_tokens is
    hit, or max_turns is exhausted -- see module docstring for the shape."""
    messages = [{"role": "user", "content": user_message}]

    for turn in range(max_turns):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break
        elif response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = dispatch_tool_call(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
            messages.append({"role": "user", "content": tool_results})
        elif response.stop_reason == "max_tokens":
            messages.append({"role": "assistant", "content": "[SYSTEM: max_tokens limit hit]"})
            break
    else:
        messages.append({"role": "assistant", "content": "[SYSTEM: max_turns exhausted without resolution]"})

    return messages
