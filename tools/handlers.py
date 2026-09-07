"""
Business logic for each tool. This is where errors.ok(...) / errors.error(...)
actually get used, and where the two HARD RULES from the assignment get
enforced -- as code, not as instructions to Claude. See GUIDE.md Part 3
and Part 4.

Session state: for this assignment a simple in-memory dict tracking which
customers have been identity-verified this conversation is enough --
you don't need a real auth system. e.g.:

    VERIFIED_CUSTOMERS: set[str] = set()   # customer_ids verified this session

Wire these functions up in agent/loop.py's tool dispatch (name -> function).
"""

from data.fixtures import CUSTOMERS, ORDERS
from tools.errors import ok, error

REFUND_CEILING = 500.00

# TODO: some way to track identity verification for the current
# conversation/session. A module-level set of verified customer_ids is
# fine for this assignment.


def get_customer(email: str) -> dict:
    """
    Look up a customer by email and (per your design) verify their
    identity using the fields in CUSTOMERS[...]["verification"].

    Decide: what does the caller (Claude) need to pass in to prove
    identity, beyond just the email? What error category applies if the
    email doesn't exist vs. if verification fields don't match?

    On success, this is the function that should mark the customer as
    "verified" for the rest of the conversation -- that's the flag your
    identity gate (Rule 1) checks before allowing lookup_order or
    process_refund to run.
    """
    # TODO
    raise NotImplementedError


def lookup_order(order_id: str, customer_id: str) -> dict:
    """
    Read-only order lookup. Must be gated behind identity verification
    (Rule 1) -- decide where that check lives (here, or in a shared
    guardrail called from the dispatch loop -- see agent/guardrails.py
    and GUIDE.md Part 4 for the tradeoff).

    Think about the error categories:
    - order_id not found -> ?
    - order exists but belongs to a different customer_id -> ?
    """
    # TODO
    raise NotImplementedError


def process_refund(order_id: str, customer_id: str, amount: float) -> dict:
    """
    Issue a refund. Must enforce BOTH hard rules:
      1. Identity verification gate (same as lookup_order).
      2. The $500 refund ceiling -- REFUND_CEILING above. This check must
         be unconditional code, not something a system prompt asks Claude
         to "remember" to respect. Think hard about *where* exactly this
         check should live so nothing can call process_refund and skip it
         (see GUIDE.md Part 4 -- there's a stretch goal about trying to
         break your own gate with a hostile system prompt).

    What happens when amount > REFUND_CEILING? Not a silent failure --
    what does the customer/agent need to know, and should this case be
    steering the conversation toward escalate_to_human?
    """
    # TODO
    raise NotImplementedError


def escalate_to_human(customer_id: str, order_id: str, reason: str) -> dict:
    """
    Create a ticket a human agent could act on WITHOUT reading the chat
    transcript. Per the brief: customer, order, and reason, plus a ticket
    id. Think about what "without the transcript" really requires --
    is a raw customer_id/order_id enough, or does a human need the
    customer's name, the order amount, etc. copied into the ticket too?
    """
    # TODO
    raise NotImplementedError
