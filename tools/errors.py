"""
Small helpers for building the lean, uniform result shape every tool should
return. This part is mechanical (just a dict shape) so it's provided --
what's graded is HOW you use these categories inside each tool's business
logic in handlers.py.

Result shape (always the SAME shape whether it succeeded or failed -- this
is what lets the agent loop append it as a tool_result without special-
casing):

    {
        "ok": bool,
        "data": <only on success -- only the fields Claude needs next turn>,
        "errorCategory": <only on failure -- one of the 4 below>,
        "isRetryable": <only on failure>,
        "message": <only on failure -- customer-facing, not a stack trace>,
    }

The four error categories (from the assignment brief):
- "transient"   -- e.g. a downstream service timeout. isRetryable=True.
- "validation"  -- e.g. malformed order id, missing required field.
                   isRetryable=False (the caller needs to fix the input,
                   not just retry the same call).
- "business"    -- e.g. refund exceeds ceiling, order already refunded,
                   customer not found. isRetryable=False, and the message
                   should be something you could show a customer directly.
- "permission"  -- e.g. identity not verified yet, order belongs to a
                   different customer. isRetryable=False.

Think about *isRetryable* as the field that would drive different agent
behavior -- what should Claude actually do differently for a transient
error vs a business error? That's the judgment the rubric is looking for
in handlers.py, not in this file.
"""

def ok(data: dict) -> dict:
    return {"ok": True, "data": data}


def error(category: str, message: str, retryable: bool) -> dict:
    assert category in {"transient", "validation", "business", "permission"}, (
        f"unknown errorCategory: {category!r}"
    )
    return {
        "ok": False,
        "errorCategory": category,
        "isRetryable": retryable,
        "message": message,
    }
