# Customer Support Resolution Agent

Week 1, Assignment 1 -- Multi-Tool Agent with Escalation Logic.

## Setup

```
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY
python main.py "hi, I'd like a refund for my headphones"
```

## Architecture

- `data/fixtures.py` -- mock customers/orders
- `tools/schemas.py` -- Messages API tool definitions (the four tools)
- `tools/handlers.py` -- business logic + error handling for each tool
- `tools/errors.py` -- shared `{ok, errorCategory, isRetryable, message}` shape
- `agent/loop.py` -- the agentic loop (stop_reason control flow)
- `agent/guardrails.py` -- (if used) shared pre-exec hook for the two hard rules
- `transcripts/` -- the two required transcripts

## Reflection

### 1. Why does the refund ceiling belong in code, not the system prompt?

TODO

### 2. How did you distinguish the similar tool pair, and how would you detect misrouting in production?

TODO

### 3. Why payload minimization -- what was removed, and what breaks if a summary omits the refund amount?

TODO
