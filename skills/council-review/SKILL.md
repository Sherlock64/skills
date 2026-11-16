---
name: council-review
description: Convene a review council on a change. Picks the reviewers (security, tests, requirements, cleanliness, minimalism, UI, UX, accessibility) that the change's risk calls for, runs them as parallel read-only subagents, merges their severity-rated findings into one deduped table, and decides PASS (nothing critical, high or blocking medium) or FAIL. Use when a version's or fix's dev work is done and needs review, or when the user asks for a council review.
---

# Council review

Each member is a read-only subagent that follows `member-contract.md` plus its own rubric in `members/<member>.md`, both in this folder. "Project instructions" means the project's `AGENTS.md`, `CLAUDE.md`, or both. A project can add rubric items per member under a "Review" heading there; members apply them.

## Members and dimensions

Each member owns one dimension. Every project-instruction rule should have exactly one owner; when one has none, give it to the closest member in the prompt.

| Member | Dimension |
|---|---|
| `code-cleanliness` | Readability, structure, idioms, lint/format/type-check clean, consistency with established patterns, project coding rules |
| `minimalism` | Unneeded code, abstraction, scope creep, duplication, dependencies |
| `security` | Secrets, crypto, external interfaces, injection, input validation, data integrity |
| `test-quality` | Tests run and pass, cover the change, and are meaningful |
| `requirements` | Every task and acceptance criterion, one by one, against the coverage map and tests; checkpoints and branch rule |
| `ui-design` | Visual consistency: components, design tokens, layout, typography |
| `ux-design` | Flows, states, feedback, copy |
| `accessibility` | WCAG 2.1 AA: semantics, keyboard, focus, names, contrast |

## Steps

1. Build the scope:
   - The changed files: `changed_files` in the evidence file (`snapshots/<version>/evidence.md`).
   - A summary of the change in a few lines.
   - The requirements: the PRD path, or for a hotfix the task brief.
   - The coverage map `snapshots/<version>/coverage.md`.
   - The contracts path, or "none".
   - The UI screenshots: one per distinct state of the changed components only (in a re-review, only the retaken ones), with route and state, or "none". Only `ui-design`, `ux-design` and `accessibility` get them.
   - The dependencies the user approved, or "none".
   - For each member, the findings you rejected in earlier rounds, with reasons.
2. Select the members. In a re-review round, take the set the caller gives. Otherwise classify the change by its files and behaviour, including the transitive callers of changed code (grep them), and take the union of every row that applies:

   | Risk | Applies when | Members |
   |---|---|---|
   | docs-only (record as `routine`) | Only prose changed | None required; optionally `requirements` as a spot check |
   | `routine` | Code outside the sensitive paths, no new external interface | `requirements`, `code-cleanliness`, plus `minimalism` when code, files or abstractions were added |
   | `ui` | UI code changed | `requirements`, `ux-design`, `accessibility`, plus `ui-design` when visuals changed |
   | `sensitive` | A sensitive path, a new or changed external interface (API, command, file format, permission), or a change to how data is stored, imported, exported or deleted | `security`, `test-quality`, `requirements`, `code-cleanliness`, plus the `ui` members when UI changed |
   | `cross-cutting` | A major redesign across layers, or members contradicting each other across rounds | All eight |

   Sensitive paths are the ones the project instructions list. Where they list none, take: auth, crypto, secrets and key handling, persistence and migrations, parsers of external input, request handlers and their registration, permission or security config, and dependency manifests.

   Escalate one row on a critical unknown, a security-sensitive dependency, or a blast radius you can't bound. A risk row only picks reviewers: every project rule still applies, and a change touching what a security rule covers is `sensitive` whatever its paths.

   Append a `review:` block to the evidence file: `requirements`, `risk`, `snapshots`, `reviewers_required`, and `reviewers_skipped` with one `"<member>: <reason>"` per member not selected.
3. Spawn the selected members in parallel, as read-only subagents where the harness offers them. Give each this prompt, filled in with absolute paths:
   ```
   You are the <member> member of the review council.
   Follow <skill dir>/member-contract.md and <skill dir>/members/<member>.md.
   Requirements: <PRD path, or "Task brief:" and the brief>
   Round: <k>
   Evidence: snapshots/<version>/evidence.md
   Scope:
   <changed files>
   Summary: <summary>
   Contracts: <path or "none">
   Coverage: snapshots/<version>/coverage.md
   Snapshots:
   <path - route, state; or "none">
   Approved dependencies: <list or "none">
   Previously rejected findings: <list with reasons, or "none">
   ```
4. If a reply breaks the output format in `member-contract.md`, send it back to that member once to reformat. A member that still gives no valid verdict counts as `FAIL`.
5. Recompute each member's verdict from its findings with the rule in `member-contract.md`, whatever its verdict line says.
6. Verify each surprising finding in the cited code before rating it. Change a rating only when it plainly contradicts the scale, and record the old rating and why. Never lower a rating because fixing it is inconvenient.
7. Dedupe: merge findings with the same `file:line` and fix, keep the highest severity, credit every member that raised it. When two findings conflict, keep both and mark them `CONFLICT` for the organizer.
8. Reject a finding only if it contradicts the requirements or project instructions, or cites code that doesn't exist. Record the reason.
9. Report. The council passes when nothing left after steps 6-8 is `CRITICAL`, `HIGH` or blocking `MEDIUM`:
   ```
   COUNCIL: PASS | FAIL (round <k>)
   | Member | Verdict | Critical | High | Medium (blocking) | Medium | Low |
   |---|---|---|---|---|---|---|
   | code-cleanliness | FAIL | 0 | 1 | 0 | 1 | 2 |
   ...
   BLOCKING (deduped, most severe first):
   F1. [HIGH] [code-cleanliness, minimalism] <path>:<line> - Problem: ... Fix: ...
   NON-BLOCKING:
   F4. [LOW] [ui-design] <path>:<line> - Problem: ... Fix: ...
   RE-RATED:
   - F2 [member] MEDIUM non-blocking -> HIGH - <reason>
   REJECTED:
   - [member] <finding> - <reason>
   ```
10. Append the report to `snapshots/<version>/council-findings.md` (gitignored; what may reach GitHub is the `build-version` publication rule), and set `review.blocking_findings` in the evidence file to the `BLOCKING` IDs as `R<k>-F<n>`.
