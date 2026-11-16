---
name: investigate
description: Read-only playbook for answering a question about a codebase's code, data model, behaviour or history with cited evidence and no code change. Use when the user asks how something works, why it behaves a way, where something lives, or whether something is true, and wants an answer rather than a fix.
---

# Investigate

1. **Scope.** Restate the question in one line and name what would answer it (a code path, a schema, a test, a commit). Ask the user only if the question is ambiguous.
2. **Evidence.** Read the code, schema, tests and docs that bear on it, starting from the project's `AGENTS.md` or `CLAUDE.md` and `docs/`. Run read-only commands (`grep`, `git log`, `git show`, a single focused test run) when they settle a point. Record each fact with its `file:line`. Use a search subagent only when the search spans many files or naming conventions.
3. **Answer.** Give the direct answer first, then the evidence as `file:line` citations. Mark anything you inferred rather than read. If the answer points to a bug, say so and offer the `fix-bug` skill.

Never edit files, change git state or spawn dev agents.
