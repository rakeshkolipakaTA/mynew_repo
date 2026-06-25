> **What this file is:** The AI assistant's own running summary of this project's *actual* structure, written and updated by the AI as it explores the codebase — distinct from `architecture.md`, which is the human-authored vision and decisions to preserve. This file is **AI-owned**: update it freely, without asking, whenever you learn something about the real system not yet reflected here. Edit it in place to stay current — it's a summary, not an append-only log. If it ever conflicts with `architecture.md`, that's a real signal worth surfacing to a human, not something to silently resolve.
>
> **Example:** After tracing how requests flow through the system, the AI adds: "Routes in `src/main.py` call directly into `_orders` (an in-memory dict) — there is no service layer. `architecture.md` doesn't mention this directly, but `memory/decisions/` DEC-legacy-1 explains why."

# Start from Here.

## Observed Architecture

*(Empty until the AI assistant explores the codebase for the first time — see `AGENT.md`'s Step 3 for when to update this. Each note should be specific and falsifiable — "the orders route uses an in-memory dict, not a database" — not vague restatements of `architecture.md`.)*
