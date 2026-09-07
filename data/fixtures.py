"""
Mock data store for the assignment. This is fixture/test data only -- not
part of what's graded -- so it's provided for you rather than left as a TODO.

Two customers, two orders. Notice the numbers are chosen on purpose:
- ORD-123 (Alice) is UNDER the $500 refund ceiling -> should succeed.
- ORD-456 (Bob) is OVER the $500 refund ceiling -> should trigger your
  code-level gate and escalate, not get auto-refunded.

Feel free to add more customers/orders/edge cases as you test (e.g. an
order that's already been refunded, an unverified customer, a customer
asking about an order that isn't theirs).
"""

CUSTOMERS = {
    "alice@example.com": {
        "customer_id": "CUST-001",
        "name": "Alice Nguyen",
        "email": "alice@example.com",
        "verification": {
            # whatever fields your identity check needs, e.g. last4 of
            # payment method, zip code, order number, etc.
            "zip_code": "94110",
        },
    },
    "bob@example.com": {
        "customer_id": "CUST-002",
        "name": "Bob Martinez",
        "email": "bob@example.com",
        "verification": {
            "zip_code": "95814",
        },
    },
}

ORDERS = {
    "ORD-123": {
        "order_id": "ORD-123",
        "customer_id": "CUST-001",
        "item": "Wireless Headphones",
        "amount": 89.99,
        "status": "delivered",
        "refunded": False,
    },
    "ORD-456": {
        "order_id": "ORD-456",
        "customer_id": "CUST-002",
        "item": "Standing Desk",
        "amount": 649.00,
        "status": "delivered",
        "refunded": False,
    },
}
