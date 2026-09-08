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
    {
        "name": "get_customer",
        "description": (
            "Verify a customer's identity and retrieve their customer_id. "
            "Requires BOTH the customer's email AND their account zip code "
            "-- email alone is not sufficient proof of identity, since "
            "email addresses are not secret. Call this FIRST, before "
            "lookup_order or process_refund: both of those require a "
            "verified customer_id from this call and will fail without "
            "one. On failure (email not found OR zip does not match), "
            "returns the same generic 'could not verify identity' failure "
            "for both cases -- do not treat a lookup_order/process_refund "
            "failure as evidence about which emails exist in the system. "
            "This tool does not return order information; use lookup_order "
            "for that after verification."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The customer's email address, e.g. 'alice@example.com'.",
                },
                "zip_code": {
                    "type": "string",
                    "description": (
                        "The zip code on the customer's account, as a string "
                        "(e.g. '94110') to preserve any leading zeros."
                    ),
                },
            },
            "required": ["email", "zip_code"],
        },
    },
    {
        "name": "lookup_order",
        "description": (
            "Look up and return order details, given a customer_id and "
            "order_id. Requires BOTH a non-null customer_id AND a non-null "
            "order_id -- order_id alone is not sufficient; the customer_id "
            "must come from a prior successful get_customer call for this "
            "conversation. On failure (no order found for that "
            "customer_id), returns a generic 'order not found' message. On "
            "failure (invalid/unverified customer_id), returns an 'invalid "
            "customer' message. This is READ-ONLY -- it never issues a "
            "refund or changes order state. If the customer wants their "
            "money back, use process_refund instead. Does not return "
            "customer personal data (name, email, etc.), only order fields."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The verified customer_id from get_customer, e.g. 'CUST-123'.",
                },
                "order_id": {
                    "type": "string",
                    "description": "The order id to look up, e.g. 'ORD-123'.",
                },
            },
            "required": ["customer_id", "order_id"],
        },
    },
    {
        "name": "process_refund",
        "description": (
            "Process a refund for the customer, given customer_id, "
            "order_id, and refund_amount. Requires ALL of: a non-null "
            "customer_id (must come from a prior successful get_customer "
            "call), a non-null order_id, and the refund_amount requested. "
            "On failure (invalid/unverified customer_id), returns an "
            "'invalid customer' message. On failure (no order found for "
            "that customer_id), returns a generic 'order not found' "
            "message. On failure (refund_amount exceeds the order's "
            "original amount), returns an error identifying the request "
            "as not permissible. Refund requests over $500 will be "
            "rejected by a hard limit; if that happens, explain the limit "
            "to the customer and consider escalate_to_human. This CHANGES "
            "STATE -- it issues a partial or full refund and mutates the "
            "order. If the customer just wants order status, use "
            "lookup_order instead; do not call this to check on a refund "
            "that hasn't been requested. Does not return customer "
            "personal data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The verified customer_id from get_customer, e.g. 'CUST-123'.",
                },
                "order_id": {
                    "type": "string",
                    "description": "The order id to refund, e.g. 'ORD-123'.",
                },
                "refund_amount": {
                    "type": "number",
                    "description": "The refund amount in dollars and cents, e.g. 5.00.",
                },
            },
            "required": ["customer_id", "order_id", "refund_amount"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Escalate the conversation out of the agent to a human support "
            "agent. Does not change any order or customer details itself "
            "-- it only creates a ticket for a human to act on. Requires a "
            "non-null customer_id (must come from a prior successful "
            "get_customer call -- even an escalation ticket must be tied "
            "to a verified customer), a non-null customer_name, and a "
            "non-null reason; order_id, order_amount, and "
            "requested_refund_amount are optional but should be included "
            "whenever the escalation relates to a specific order, so the "
            "human agent has everything needed to act without re-looking "
            "anything up. Generates and returns a ticket_id that the "
            "customer or agent can reference. On failure (invalid/"
            "unverified customer_id), returns an 'invalid customer' "
            "message. Does not return customer personal data beyond what "
            "was passed in."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The verified customer_id from get_customer, e.g. 'CUST-123'.",
                },
                "customer_name": {
                    "type": "string",
                    "description": "The customer's name, e.g. 'Bob Martinez'.",
                },
                "order_id": {
                    "type": "string",
                    "description": "The order id this escalation relates to, if any, e.g. 'ORD-123'.",
                },
                "order_amount": {
                    "type": "number",
                    "description": "The order's original amount in dollars and cents, if applicable, e.g. 649.00.",
                },
                "reason": {
                    "type": "string",
                    "description": "The reason for escalation, e.g. 'refund exceeds $500 ceiling'.",
                },
                "requested_refund_amount": {
                    "type": "number",
                    "description": "The refund amount the customer requested, if applicable, e.g. 649.00.",
                },
            },
            "required": ["customer_id", "customer_name", "reason"],
        },
    },
]
