"""
Thin CLI entry point. Not graded on its own -- just wiring so you can
actually run the thing while you build it. Extend as you like (e.g. to
print a nicely formatted transcript for the transcripts/ deliverable).
"""

import sys
from agent.loop import run_conversation


def main():
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = input("Customer: ")

    messages = run_conversation(user_message)
    for m in messages:
        print(f"--- {m['role']} ---")
        print(m["content"])
        print()


if __name__ == "__main__":
    main()
