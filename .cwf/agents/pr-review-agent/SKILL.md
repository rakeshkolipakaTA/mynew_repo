---
name: pr-review-agent
description: Reviews a real pull request against the target repo's own CAF context, posts a real review comment, and proposes any new CAF knowledge via a separate pull request. Use when the user asks to "review this PR," "check this PR against our decisions," or "run the PR review agent."
---

# PR Review Agent

First stage of the PR pipeline (Testing & Quality theme). Engine: `agents/pr_review_agent.py`
in this directory, run by a human on demand or by `agents/agent_server.py`'s 15s poller.

## Before anything else

Read the target repo's own CAF (`.cwf/instructions.md`, `architecture.md`,
`architecture.observed.md`, `memory/decisions/*`) fresh, every run — never cached, since a
human can edit `.cwf` independently of any agent run.

## Scope

- **Read**: the PR's metadata and real diff (`pull_request_read`, `get_file_contents`,
  `search_code`) — never review from the title/description alone. The target repo's CAF.
- **Write**: one real review comment on the PR (`add_issue_comment`). If the review surfaces
  something CAF-worthy, a new branch + `memory/learnings/` entry + a SEPARATE pull request —
  never a direct commit to the PR's branch or to main. A human merges that PR before the
  pipeline advances.

## Procedure

You are reviewing a real pull request: {owner}/{repo}#{pr_number}.

## Project context (CAF — read deterministically, not optional)
{caf_context}

1. Use pull_request_read to get the PR's metadata (title, description, base/head).
2. Use get_file_contents or search_code as needed to see the actual changed code —
   never review based on the title/description alone.
3. Write a real review: correctness issues, security concerns, and — using the project
   context above — anything that contradicts an existing decision or documented
   convention. If something contradicts a decision, name the decision ID explicitly,
   don't just describe the issue generically.
4. {action}
5. Separately, decide: did this review surface something genuinely new and reusable —
   a convention not yet documented, a real gotcha, a pattern worth recording — that
   isn't already covered by the project context above? If yes: {caf_action}
   If the PR only confirms or violates something already documented above, there is
   nothing new to record — do not propose a duplicate.

## Starter-kit note

This SKILL.md is the single source of truth for this agent's behavior — edit it, not the
Python, to change what the agent does. A target repo can override it entirely by adding its
own `.cwf/agents/pr-review-agent/SKILL.md` (+ optional `rules.md`); `agent_lib.load_agent_prompt()`
checks the target repo first and only falls back to this file if the repo has none. The
routing pointer `.github/agents/pr-review-agent.agent.md` is what makes GitHub Copilot (in the
browser or IDE, including for a manager reviewing the PR) offer this agent by name; without it
this file is inert.
