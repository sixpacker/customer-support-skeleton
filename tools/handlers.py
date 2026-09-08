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

# Module-level, so it persists across separate dispatch_tool_call
# invocations within the same run_conversation() call -- see discussion in
# GUIDE.md Part 4. Reset per process, not per fixture; fine for this
# assignment's scope (a single conversation, no concurrent sessions).
VERIFIED_CUSTOMERS: set[str] = set()


def get_customer(email: str, zip_code: str) -> dict:
    """
    Look up a customer by email and verify identity via zip_code. Requires
    BOTH to match -- email alone proves nothing (see tools/schemas.py's
    description for the same reasoning). Marks the customer verified for
    the rest of this process's VERIFIED_CUSTOMERS set on success.
    """
    customer = CUSTOMERS.get(email)
    if customer is None or customer["verification"]["zip_code"] != zip_code:
        # Same generic message whether the email doesn't exist or the zip
        # doesn't match -- distinguishing them would let a caller enumerate
        # valid emails by trial and error.
        return error("business", "Could not verify identity with the provided email and zip code.", False)

    VERIFIED_CUSTOMERS.add(customer["customer_id"])
    # customer_name is included (not just customer_id) because
    # escalate_to_human's schema requires customer_name as an input, and
    # this is the only tool that ever surfaces customer personal data --
    # lookup_order deliberately does not (see its description).
    return ok({"customer_id": customer["customer_id"], "customer_name": customer["name"]})


def lookup_order(order_id: str, customer_id: str) -> dict:
    """
    Read-only order lookup, gated behind identity verification (Rule 1).

    "Order not found" and "order belongs to a different customer" return
    the SAME customer-facing message -- distinguishing them would let a
    verified customer enumerate other customers' order IDs by trial and
    error (being verified as yourself doesn't authorize learning what
    exists for someone else). errorCategory is still accurate internally
    (business vs permission) even though the message text matches.
    """
    if customer_id not in VERIFIED_CUSTOMERS:
        return error("permission", "Please verify your identity first.", False)

    order = ORDERS.get(order_id)
    if order is None or order["customer_id"] != customer_id:
        category = "business" if order is None else "permission"
        return error(category, "Order not found for this customer.", False)

    return ok({
        "order_id": order["order_id"],
        "item": order["item"],
        "amount": order["amount"],
        "status": order["status"],
        "refunded": order["refunded"],
    })


def process_refund(order_id: str, customer_id: str, amount: float) -> dict:
    """
    Issue a refund. Reuses lookup_order() for the identity gate AND the
    not-found/wrong-owner check (Rule 1) -- since this unconditionally
    calls lookup_order first, there is no code path into the refund logic
    for an unverified customer or someone else's order, by construction.

    Checks run in order: identity/ownership (via lookup_order) -> already
    refunded -> amount exceeds order's original total -> the $500 ceiling
    (Rule 2, REFUND_CEILING, unconditional). Ceiling and already-refunded/
    over-total checks are deliberately ordered so a request that's invalid
    for reasons OTHER than size doesn't get misreported as "too big."
    """
    lookup_result = lookup_order(order_id, customer_id)
    if not lookup_result["ok"]:
        return lookup_result  # propagate as-is: not verified / not found / wrong owner

    order_data = lookup_result["data"]

    if order_data["refunded"]:
        return error("business", "This order has already been refunded.", False)

    if amount > order_data["amount"]:
        return error("business", "Refund amount exceeds the order's original amount.", False)

    if amount > REFUND_CEILING:
        return error("business", "This refund requires additional review. Someone will be with you shortly.", False)

    ORDERS[order_id]["refunded"] = True
    return ok({"order_id": order_id, "refunded_amount": amount, "status": "refunded"})


TICKETS: list[dict] = []
_next_ticket_number = 1


def escalate_to_human(
    customer_id: str,
    customer_name: str,
    reason: str,
    order_id: str = None,
    order_amount: float = None,
    requested_refund_amount: float = None,
) -> dict:
    """
    Create a ticket a human agent can act on without reading the chat
    transcript -- customer_name/order_amount/requested_refund_amount are
    copied in (not just IDs) so nothing needs re-looking-up. Gated behind
    identity verification like the other tools, since even an escalation
    ticket must be tied to a real, verified customer.
    """
    global _next_ticket_number

    if customer_id not in VERIFIED_CUSTOMERS:
        return error("permission", "Please verify your identity first.", False)

    ticket_id = f"TICKET-{_next_ticket_number:06d}"
    _next_ticket_number += 1

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "order_id": order_id,
        "order_amount": order_amount,
        "reason": reason,
        "requested_refund_amount": requested_refund_amount,
    }
    TICKETS.append(ticket)
    return ok(ticket)
