- Never commit directly to the original PR's branch or to main — always a new branch
  ("documentation/update-pr-<N>") + a new pull request, reviewed by a human before merge.
- Name doc files after the module/feature they document (e.g. "documentation/db_utils.md"),
  never a generic "notes.md".
- Carry forward any hard constraint from the CAF context (e.g. a decision ID) into the doc
  file itself, with a concrete correct/incorrect example — don't just link back to .cwf.
