"""
Optional home for the two hard-rule gates, if you decide (per GUIDE.md
Part 4) that they should live as a shared pre-exec hook rather than being
duplicated inline inside each handler in tools/handlers.py.

Either design is acceptable to the rubric ("$500 ceiling inside
process_refund (OR a pre-exec hook)") -- but you must be able to defend
your choice in the README reflection. A hook has the advantage of being
impossible to forget when a 5th tool gets added later; inline is simpler
to read for a 4-tool assignment. Pick one, don't build both half-way.

If you go the pre-exec hook route, this is where you'd intercept a
tool_use block BEFORE calling the handler in agent/loop.py's dispatch,
check its name + input against the rules, and short-circuit with a
tools.errors.error(...) result if a rule is violated.
"""

# TODO (only if you choose the pre-exec hook design)
