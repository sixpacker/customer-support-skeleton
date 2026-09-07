"""
Tool definitions for the Messages API `tools` parameter.

THIS FILE IS YOUR JOB -- it's the single biggest lever in the "Tool
descriptions" rubric line (15 pts) and it's what the loop in agent/loop.py
will pass straight through to the API. See GUIDE.md Part 1 before writing
these.

Each entry needs:
    {
        "name": "...",
        "description": "...",   # <-- this is what Claude routes on. Be
                                 #     explicit about: what it's for, what
                                 #     it is NOT for, input formats, what
                                 #     it returns, and any preconditions
                                 #     (e.g. "call get_customer first").
        "input_schema": {
            "type": "object",
            "properties": {...},
            "required": [...],
        },
    }

You have four tools to define:
    1. get_customer       -- look up / verify a customer's identity
    2. lookup_order       -- read-only order status/details lookup
    3. process_refund     -- actually issue a refund (mutates state, money
                              moves)
    4. escalate_to_human  -- hand off to a person with a self-sufficient
                              ticket

REQUIRED: two of these four are similar enough that a lazily-written
description will cause misrouting (the assignment brief tells you this
directly). Before you write the descriptions, decide for yourself which
pair you think that is and WHY -- you'll need to defend that in the
reflection section of the README. Write the two descriptions so a model
reading only the tool list (no examples, no routing layer) could never
confuse them. Test it: after you've built the loop, deliberately send an
ambiguous message like "I want my money back for my headphones" and check
which tool gets called.

TODO: build TOOLS = [ ... ] below, one dict per tool as described above.
"""

TOOLS = [
    # TODO: get_customer
    # TODO: lookup_order
    # TODO: process_refund
    # TODO: escalate_to_human
]
