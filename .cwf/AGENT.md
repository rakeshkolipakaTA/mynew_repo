> **What this file is:** The router every AI assistant reads first, unconditionally, before touching any other `.cwf/` file. It classifies the task type and tells the assistant exactly which other files to load — it contains no project facts and no project-specific rules; those live in `instructions.md` and `rules.md`. This is framework plumbing, not content you fill in — you'd only edit it to change how CWF itself behaves, which is rare.
>
> **Example:** A request to "fix the 500 error on checkout" gets classified as **Coding**, so the assistant loads only `instructions.md` and `rules.md` — it does not load `architecture.md` or any `memory/` file unless the area being touched has a prior decision or incident attached.

# Start from Here.

## CWF Agent Instructions

You are working inside a project that uses the **Context Workspace Framework (CWF) v2**.

CWF is a lightweight operating system for AI-assisted software development. Its job is to:
- **Route** you to only the context you actually need for this task.
- **Persist** information that cannot be inferred from source code (decisions, incidents, conventions).
- **Standardize** workflows across AI tools (Copilot, Claude Code, Cursor, and future tools).
- **Stay lightweight** by treating source code as the primary source of truth and loading additional context only on demand.

---

### Step -1 — Bootstrap the entry points, so "read .cwf" never has to be said twice (once per project)

You normally reach this file automatically — `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules`, or `AGENTS.md` auto-loads at the start of every session and points here. If instead a human just told you directly to "read `.cwf`" (or `.cwf/AGENT.md`), that itself is a signal: one or more of those entry points is missing, which is why nothing auto-loaded you this time.

**This is a compulsory step, not optional cleanup — do it before anything else, without asking.** Check whether each of these four exists at the repo root. For any that's **missing**, create it with exactly this content, substituting the row's values — **never overwrite a file that already exists at that path**, even if it doesn't mention `.cwf`, since it might be a real, unrelated file someone wrote by hand:

```
# <Tool Name>

This repository uses the **Context Workspace Framework (CWF) v2**.

Read `.cwf/AGENT.md`. That file is the router — it will tell you exactly which other files to load based on the task. Do not pre-load `instructions.md`, `rules.md`, `architecture.md`, or memory before reading AGENT.md and classifying the task first.

See `.cwf/adapters/<adapter file>.md` for tool-specific notes.
```

| File (missing → create) | `<Tool Name>` | `<adapter file>` |
|---|---|---|
| `CLAUDE.md` | Claude Code | `claude` |
| `.github/copilot-instructions.md` | GitHub Copilot | `github-copilot` |
| `.cursorrules` | Cursor | `cursor` |
| `AGENTS.md` | AGENTS.md | `agents-md` |

This content is embedded here, not fetched from `template/root/`, because `template/root/` only exists in the framework repo — it was never copied into this project, so it isn't there to copy from. The `.cwf/adapters/*.md` files referenced in the last line *do* exist here, and are the fuller, tool-specific reference copy each short root file points to — don't paste their full content into the root file itself, just point to them, the same way the framework's own original root files do.

If all four already exist, say nothing about it and continue.

This is what turns "read `.cwf`" from something a human has to remember to say every session into a one-time instruction: once the entry points exist, the *next* session — in Claude Code, Copilot, Cursor, or any tool that supports the `AGENTS.md` convention — auto-loads into `AGENT.md` on its own, no one needing to type anything.

---

### Step 0 — Identify the user (once per machine)

Before anything else, check `memory/profile.json`'s `name` and `role` fields:
- Both already set → continue to Step 1, say nothing about it.
- `name` is `null` → ask for it (just the name — team/email are optional, see `rules.md`'s Execution Rules), in the same question also ask their role (e.g. developer, project manager, scrum master, business analyst, data/finops analyst, technical writer, platform/ML engineer — free text, not a fixed list), then set both fields in `memory/profile.json` directly. Then continue to Step 1 with the actual task.
- `name` is already set but `role` is still `null` (a profile saved before this field existed) → ask for the role alone, once, the next time you'd otherwise stay silent per the first bullet. Don't ask twice if they don't answer.

This exists so a non-coder gets answers calibrated to their role from their very first question in *any* repo with `.cwf/` — not only inside a role-specific starter kit, and not only if they've separately read a by-role guide first. See Step 3 for how `role` actually changes a response.

`memory/profile.json` is gitignored and local to this machine, so this only happens once per machine, not once per session — every session after the first answers from the already-saved name and role.

---

### Step 0.5 — Resume check (every turn, not just session start)

Before classifying the new request, check `my_tasks.yaml` for any task with `status: in_progress` — especially one logged under your own name in `my_tasks_log/<your-name>.yaml`. If one exists:
- State briefly where it stands: what's done, what's left, what (if anything) is blocking it.
- Do this even if the new request looks unrelated. A session can be interrupted and resumed without that context surviving in chat — silently dropping an in-progress task and jumping straight to the new request, with no acknowledgment it exists, is exactly the failure mode this step exists to prevent.

If nothing is `in_progress`, say nothing about it and continue straight to Step 1 with the new request.

---

### Step 1 — Classify the task

Before reading any other file, determine the task type from the user's request:

| Task type | Examples |
|---|---|
| **Coding** | fix bug, add feature, refactor, rename variable, write tests |
| **Architecture** | design a new subsystem, evaluate tradeoffs, change system shape |
| **Documentation** | generate docs, update README, explain a module |
| **Review** | code review, security review, audit |
| **Planning** | roadmap, breakdown, sprint planning |
| **Debugging** | trace an error, explain a failure, diagnose behavior |
| **Deployment** | CI/CD, release, infrastructure |
| **Memory update** | explicitly asked to save a decision, log an incident, record a learning |

If the task is ambiguous, default to **Coding**.

---

### Step 2 — Load only what the task requires

Read the table below. Load **only the files listed for your task type**. Do not load files from other rows unless a later step explicitly requires them.

| Task type | Always load | Load only if needed | Never load unless asked |
|---|---|---|---|
| **Coding** | `instructions.md`, `rules.md` | `memory/decisions/` if the area being changed has prior decisions; `memory/incidents/` if the area being changed (a route, a module, an interface) has a prior incident attached | `architecture.md`, `memory/learnings/`, all workflows |
| **Architecture** | `instructions.md`, `rules.md`, `architecture.md` | `memory/decisions/` to check prior decisions | `memory/incidents/`, `memory/learnings/`, all workflows |
| **Documentation** | `instructions.md` | `architecture.md` if documenting system shape; `memory/decisions/` if documenting why | `rules.md`, all memory types, non-documentation workflows |
| **Review** | `instructions.md`, `rules.md` | `memory/decisions/` for context on reviewed area | `architecture.md` unless reviewing structural code |
| **Planning** | `instructions.md`, `architecture.md` | `memory/decisions/`, `memory/learnings/` | `rules.md`, `memory/incidents/` |
| **Debugging** | `instructions.md`, `rules.md` | `memory/incidents/` for similar past incidents | `architecture.md`, `memory/decisions/`, all workflows |
| **Deployment** | `instructions.md`, `rules.md` | `architecture.md` for infra shape; `memory/decisions/` for deployment choices | `memory/incidents/`, `memory/learnings/` |
| **Memory update** | `memory_policy.yaml` | The specific memory directory being written to | All other files |

#### The rule in plain language

> If you can complete the task without reading a file, don't read it.
> Token budget is real. Architecture is expensive. Memory is expensive. Load them only when the task cannot be done without them.

---

### Step 2.5 — Check connected knowledge sources (MCP), if the task could need one

A tool being connected (Confluence, Jira, an internal wiki, anything else listed in
`instructions.md`'s **Connected Knowledge Sources** section) does not mean it gets called
automatically — an LLM only calls a tool when it judges the question matches that tool's
description, and a generic question ("why does this work this way", "is there a spec for X")
often doesn't obviously match a tool description on its own. Relying on that judgment alone is
why a real connected Confluence server can sit unused on a plain question that it could have
answered.

The fix: before answering any question that could plausibly be answered by a source listed in
`instructions.md`, check that section first. If a listed source is relevant to what's being
asked, call its MCP tool and use the real result — don't answer from training data, memory, or
assumption when a connected source could have the actual, current answer. If no source in that
section is relevant, proceed normally; this step is a check, not a mandate to call every tool
on every question.

---

### Step 3 — Do the work

For **Coding** tasks: search/grep/read the codebase directly for structural questions ("where is X", "what does Y call"). CWF does not maintain a structural index — source code is always the source of truth for structure. Before writing code, do one quick keyword search (grep, not a full read) over `memory/decisions/` and `memory/incidents/` for the file/route/module you're about to touch — load the matching entry only if one turns up. This is a one-line check, not a standing "always read all incidents" rule: it's how a past incident's lesson reaches a task even before it's been promoted into a `rules.md` line.

For **Architecture** tasks: read `architecture.md` before proposing any structural change. Check `memory/decisions/` for prior decisions in the same area. Never introduce a structural choice that conflicts with an active decision without flagging it first.

For **Documentation** tasks: run `workflows/documentation.md`. Read `architecture.md` only if you are documenting system shape. Never document something the code doesn't do — code is the source of truth.

For **Debugging** tasks: search `memory/incidents/` for similar past incidents before starting from scratch. One prior incident entry can save an entire session.

For all tasks: read `rules.md` whenever you are about to do something irreversible (delete, migrate, deploy, override a decision).

For all tasks: check `memory/profile.json`'s `role` and calibrate the *answer*, not the routing above — task classification and file loading stay the same regardless of who's asking, since the facts don't change by role, only how they're explained do.
- **Non-coder role** (project manager, scrum master, business analyst, data/finops analyst, technical writer, or anything else clearly not a hands-on-code role): default to plain-language explanations, no code blocks unless they specifically asked for code, and no offer to "go ahead and implement this" — describe what's true and what it means, don't assume they want a diff. If a question is genuinely ambiguous between "explain this" and "change this," ask which, rather than guessing and producing code for someone who wanted a sentence.
- **Coder role** (developer, platform engineer, ML engineer, or unset/unknown): default to normal technical depth — this is also the safe default when `role` is still `null`, since over-explaining to a developer costs less than under-explaining to a non-coder.
- This calibrates tone and format only. It never changes whether something gets saved to memory, whether a route needs a test, or any other rule in this file — a PM's question that meets the Memory Philosophy bar still gets saved as a learning, same as a developer's would.

For **Coding**, **Architecture**, and **Debugging** tasks: whenever exploring the codebase teaches you something about its real structure that isn't yet in `architecture.observed.md`, update that file before moving on — it's AI-owned, unlike `architecture.md`, so don't wait to be asked. This is the split between the two files: `architecture.md` is what a human decided and wants preserved; `architecture.observed.md` is what you actually found when you looked. They can disagree — if they do, say so rather than picking one silently.

**Loading a memory entry once does not mean trusting it forever.** A `learning`'s `evidence` field exists so it can be re-checked, not just cited — if the current task touches the same file(s) listed in a learning's `evidence`, take the moment to confirm it still says what the learning claims before relying on it. Code moves faster than memory gets updated; an unchecked stale learning is worse than no learning, because it's wrong with the same confidence a correct one would have. If it's stale, update the file in place rather than leaving it to mislead the next person (or your next session) who loads it. This applies to `decisions/` too: if you're about to act on a decision and the area it covers has visibly changed since, that's a real signal to flag, not silently work around.

---

### Step 4 — Produce artifacts

Every significant task produces a fixed artifact set. Run `workflows/task-completion.md` after completing any task you'd call "a task" (not a typo fix or a one-line answer) — **before** telling the user the work is done, not as an afterthought you might get to later:

| Artifact | Condition |
|---|---|
| Code and tests | The work itself |
| `docs/generated/*` | Public interface changed — run `workflows/documentation.md` |
| `architecture.observed.md` update | You learned something about the real system not yet reflected there — see Step 3 |
| Memory entry | Work meets the bar in Memory Philosophy below — gated by `memory_policy.yaml` |
| `CHANGELOG.md` entry | Project has one at its root |
| `my_tasks.yaml` status + a `my_tasks_log/<name>.yaml` entry | The work matches a task there, or is non-trivial enough to add one — see Task Tracking below |
| `memory/sessions/` entry | Always — even if every other artifact was skipped |

Trivial work (a typo fix, or answering a question that's a one-line lookup already sitting in `instructions.md`/`my_tasks.yaml`/an existing memory record) skips this pipeline entirely. **A question is not automatically trivial just because it produced no code change** — see Memory Philosophy below for when an answer itself is worth keeping.

---

### Task Tracking — `my_tasks.yaml`

If `my_tasks.yaml` exists at the repo root, it is the single source of truth for task state — **not the chat conversation**, which doesn't persist across sessions or to teammates. Before starting non-trivial work:

1. Check `my_tasks.yaml`'s `tasks:` list for an entry matching the request. If none exists, add one with `status: backlog`.
2. Set that task's `status` to `in_progress` before starting.
3. On completion, set `status: done`.
4. For every status change, append one entry to **your own log file**, not a shared one: `my_tasks_log/<your-slugified-name>.yaml` (e.g. `my_tasks_log/jane-doe.yaml`), using the name from `memory/profile.json` (see Step 0, never invented). If that file doesn't exist yet, create it — this is the only file under `my_tasks_log/` you should ever create or write to; never write into another person's file there. Each entry: `task_id`, `event` (`added`/`started`/`done`), `by`, `at` (current timestamp).

Never delete a task line in `my_tasks.yaml`, and never edit a past entry in any `my_tasks_log/*.yaml` file — only append. One log file per person means two people logging a change at the same moment never touch the same file, which is stronger than the append-friendly discipline `memory/decisions/` relies on (same idea, taken one step further: different files, not just different lines).

**This is not optional bookkeeping to get to later.** Never report a task as finished, and never move on to a new, unrelated request, without having done steps 1–4 above for the work you just did — "I'll log it afterward" is exactly how task state goes stale and an in-progress task gets silently abandoned (see Step 0.5). If you're unsure whether a request is "non-trivial" enough to track, default to tracking it: the cost of one extra task line is near zero; the cost of an untracked change is a teammate, or your own next session, having no idea it happened.

---

### Memory Philosophy

Memory quality beats memory volume. One accurate entry beats ten vague ones.

**Save:** architecture decisions, incidents, reusable learnings, completed milestones, conventions worth preserving across sessions — **and** anything you discovered, not just decided, while answering a question, if both of these are true:
1. Producing the answer took real exploration or synthesis (reading multiple files, cross-checking memory records) — not a lookup already sitting in one place.
2. The same question is plausible to recur — to you next session, or to someone else (a PM asking "what uses the Payment API," a Scrum Master asking "which incidents repeat").

Save the conclusion as a `learning`, not a transcript of the question — "Payment API is consumed by Order Service and Invoice Service; Refund Service is deprecated" is a learning, "user asked about Payment API" is not.

**Don't save:** every conversation, every prompt, temporary debugging output, speculative ideas that weren't acted on, anything already derivable from the code, a status lookup already answerable from `my_tasks.yaml`/`instructions.md`/an existing memory record without further exploration.

**No learning gets saved without evidence.** `learning.schema.json` requires an `evidence` field — specific file paths, route names, or other memory record IDs the conclusion is actually derived from, at least one. If you can't point to where you actually looked, you're inferring or guessing, not reporting something verified — say so in chat instead, don't write it into committed memory as if it's confirmed. A self-reported confidence score is not evidence and doesn't satisfy this; "I checked `order_service.py` and `invoice_service.py`" does.

The value of CWF memory is not proportional to project size — it's proportional to **session count**. A developer working on a medium project for six months re-explains the same context to the AI every Monday without CWF. With CWF, architecture is read once when needed and reused. Decisions are never re-litigated. Incidents are not repeated. Discoveries aren't re-discovered.

---

### Updating Memory

`memory_policy.yaml` governs whether a record needs approval before saving — don't restate or second-guess it:

- `auto_save.<type>: true` and `approval.<type>: false` → write the file directly (steps below).
- `approval.<type>: true` → show the human what you're about to save and wait for confirmation first, regardless of `auto_save`.
- `quality.merge_duplicates: true` → edit the existing record's file in place (e.g. set its `status` to `superseded`) instead of creating a near-duplicate.
- This should already be a non-issue by the time anything is saved — Step 0 above asks for the user's name at session start. If `memory/profile.json`'s `name` is still `null` when you're about to save, stop and ask first — there's no script enforcing attribution for you, so this is an AI-discipline rule, not a programmatic gate.

**Writing a record — no script involved, CWF has none:**
1. Slugify the name from `memory/profile.json` yourself — there's no script to do it for you, so do it the same way every time: lowercase, spaces and any non-alphanumeric character collapsed to a single hyphen (e.g. `"Jane Doe"` → `jane-doe`, `"O'Brien"` → `obrien`). Getting this wrong is the one thing that can actually break the per-author-ID collision guarantee — `jane-doe` and `Jane-Doe` are different strings to a case-sensitive filesystem and to the schema's `^[a-z0-9-]+$` pattern, so an inconsistent slug for the same person fragments their own ID sequence instead of merging with it.
2. Find your next ID: check `memory/<type>/` for the highest existing number after your slugified name (e.g. `DEC-jane-doe-2` already exists → your next one is `DEC-jane-doe-3`; none yet → start at `-1`).
3. Create `memory/<type>/YYYYMMDDTHHMMSS_<ID>.json` (current timestamp; never overwrite an existing file).
4. Fill in every field marked `required` in `.cwf/schemas/<type>.schema.json` — don't guess a required field's value, ask instead.
5. Before considering the record saved, re-read it against that same schema file one more time: every required field present, the `id` matching the schema's `pattern` exactly. There's no script validating this anymore — that check is now entirely on you, every time, not just when something looks wrong.

Timestamp-prefixed filenames plus per-author IDs mean concurrent additions by different people merge cleanly in Git — each person adds a new file, never touching the same line as anyone else — and two people can never generate the same ID for two different records, even before either has pulled the other's commit (as long as the slug is consistent — see step 1).

---

### Memory Conflicts and Priority

The newest active (non-superseded) entry wins. If two entries genuinely conflict and `memory_policy.yaml`'s `quality.detect_conflicts` is true, don't silently pick one — ask the human which should remain active, then mark the other superseded by editing its file's `status` field directly. Never delete memory records.

---

### File Ownership

- **Human-owned** — never rewrite without being explicitly asked: `AGENT.md`, `adapters/*`, `instructions.md`, `rules.md`, `architecture.md`, `memory_policy.yaml`.
- **AI-owned** — update freely, subject to the policies above: everything under `memory/`, `docs/generated/*`, `architecture.observed.md`.

If `instructions.md`, `rules.md`, or `architecture.md` are still placeholder content (e.g. `<!-- e.g. ... -->` text, never edited from the template) when you first touch this project, say so once and offer to draft them from the codebase — then wait for the human to say yes before writing to any of them. Don't silently treat placeholder content as if it were real project facts, and don't silently fill it in either; both are wrong in different directions. This offer only needs to happen once per project, not every session — if the human declines or ignores it, don't ask again unless they bring it up.

---

### Session End

Before ending a session that did significant work, follow `prompts/session-extraction.md`, which runs `workflows/task-completion.md` for the full artifact set. If nothing meets the Memory Philosophy bar, skip the memory artifact — the others (generated docs, session log) still apply.
