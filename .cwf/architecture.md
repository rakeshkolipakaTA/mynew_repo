> **What this file is:** Human-owned description of *this* project's architecture — not structural detail (routes, functions, call graphs belong in the code itself, which an AI assistant should read directly). This file is for what the code can't tell you: why it's shaped this way, and what to preserve when someone proposes changing it. Same as `instructions.md`, there's no framework-provided default here — "why is this system shaped this way" is project-specific by definition, so this file is entirely user-defined. (For what the AI itself discovers exploring the code, see the separate, AI-owned `architecture.observed.md` instead.)
>
> **Example:** `## Design Goals` → "Optimize for readability over cleverness. No premature multi-tenancy." — a fact no amount of code-reading would reveal on its own.
>
> **AI assistant:** if you're reading this file directly without having read `.cwf/AGENT.md` first this session, stop and read that first — it's the router that decides whether this file even applies to the current task.

# Start from Here.

## Architecture

### System Vision

<!-- One paragraph: why this system is shaped the way it is. -->

### Design Goals

<!-- e.g. "Optimize for readability over cleverness." "No premature multi-tenancy." -->

### High-Level Components

<!-- e.g. Frontend, Backend, Database, Cache, major cloud services -->

### Major Services

<!-- e.g. Authentication, Payments, Notifications, Monitoring -->

### External Dependencies

<!-- Third-party APIs, managed services this system relies on -->

### Decisions to preserve

<!-- Cross-reference memory/decisions/ for the full history; note here
anything an AI assistant should specifically not "helpfully" undo. -->
