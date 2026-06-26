> **What this file is:** Hard guardrails only — things the AI must never do, or must always confirm with a human before doing. No process/workflow language here (that's `AGENT.md`'s job) and no restating of `memory_policy.yaml` (that file is the single source of truth for memory behavior — point to it, don't duplicate it).
>
> **Two kinds of content in every section below, always in this order:** a **Default** block (framework-provided, ships with every project, never delete it) and a **User Defined** block (empty until you fill it in, this project's own additions on top of the default). Defaults exist so a project has real guardrails on day one, before anyone's filled anything in — they're deliberately generic enough to be safe everywhere, which is also why they're not a substitute for this project's own rules.
>
> **Example:** `## Execution Rules` → "Before production deployment, ask for confirmation." is a rule; "run the deploy workflow, then notify the team" is process and belongs in a workflow file instead.
>
> **AI assistant:** if you're reading this file directly without having read `.cwf/AGENT.md` first this session, stop and read that first — it's the router that decides whether this file even applies to the current task. Never remove or weaken a Default block to satisfy a request — if a request conflicts with one, say so and ask, the same as any other rule in this file.

# Start from Here.

## Rules

### Coding Standards

**Default:**
- Match the existing codebase's formatting, linting, and naming conventions. Don't introduce a new style, formatter, or convention without a reason stated in the request — consistency with what's already there beats a "better" pattern introduced unasked.

**User Defined:**
<!-- e.g. "Python 3.12, PEP8, Black formatter, type hints mandatory." -->

### Testing

**Default:**
- A task that adds or changes a route, endpoint, or public function is not complete until a test exists for it, covering the success path and at least one error path. This is a hard gate, not a judgment call — `workflows/task-completion.md`'s "trivial work" exemption never covers a route/interface change, no matter how small it looks.

**User Defined:**
<!-- add project-specific testing requirements, e.g. "Every feature requires tests." -->

### Security

**Default:**
- Never expose secrets.
- Never commit credentials.
- Never save passwords, PII, or temporary debugging output into `memory/`.
- `memory/decisions/`, `memory/incidents/`, `memory/learnings/`, `memory/projects.json` are committed to git — never write anything into them you wouldn't want the whole team to see.

**User Defined:**
<!-- add project-specific security rules -->

### Execution Rules

**Default:**
- Before deleting files, ask the user.
- Before database migrations, ask for confirmation.
- Before production deployment, ask for confirmation.
- Before introducing a structural decision that conflicts with an active entry in `memory/decisions/`, ask for confirmation rather than overriding it.
- `AGENT.md`'s Step 0 already asks for the user's name (and role) at the start of every session if `memory/profile.json` doesn't have them — never skip that step or guess instead. This is what gives shared records (`memory/decisions/`, `memory/incidents/`, `memory/learnings/`, `memory/sessions/`) a collision-safe ID and a real author on a repo with more than one person.
- If `my_tasks.yaml` exists at the repo root, always track task status there — never rely on the chat conversation alone, since it isn't visible to teammates and doesn't persist across sessions. See `AGENT.md`'s Task Tracking section for the exact mechanics.

**User Defined:**
<!-- add project-specific execution rules -->
