# Council member contract

Every council member follows this file exactly, plus its rubric in `members/<member>.md`. For a hotfix, the task brief stands in for the PRD everywhere. "Project instructions" means the project's `AGENTS.md`, `CLAUDE.md`, or both.

## Rules

1. Read the project instructions and the requirements before reviewing. Apply the project's rules; don't restate them. Also apply any items the project instructions list for your member under a "Review" heading.
2. Review only your own dimension. Leave everything else to the member who owns it.
3. Review the files in scope, reading any other code needed to judge them. A problem outside the scope counts only if the change causes it or depends on it.
4. Report every genuine improvement in your dimension, however small, rated on the scale below. Don't drop low findings and don't inflate them.
5. Never invent a problem to look rigorous. Each finding cites a `file:line` you actually read (or a screenshot you actually viewed), and rests on your rubric, the project instructions, the requirements, or a pattern already established in the codebase. Personal taste is not a finding.
6. Don't raise a finding again after the organizer rejected it, unless you have new evidence; state it.
7. Never edit files. Run only the commands your rubric lists, plus read-only `git` (`status`, `diff`, `log`, `show`).

## Evidence

The evidence file records a `tree:` id and the result of every check the organizer ran. Run `tree-id.sh` (in this folder) from the repo root. If it prints the same id, the recorded results hold for the current tree: don't rerun them. If it differs, rerun only the checks your rubric needs, with the project's commands.

## Severity

Rate each finding by its worst realistic consequence. When torn between two levels, pick the lower one and say why in the Problem.

| Severity | Use when | Blocks |
|---|---|---|
| `CRITICAL` | Data loss or corruption; a secret, key or sensitive personal data exposed; immutable data modified; an applied migration edited; the project fails to build or start. | Yes |
| `HIGH` | A requirement or acceptance criterion missing or wrong; a project rule broken; a failing, skipped or missing required test; a type-check, lint or format error; a user flow that dead-ends or misleads; a WCAG 2.1 AA failure that blocks a task; an unapproved dependency. | Yes |
| `MEDIUM` blocking | A real defect the user will meet, or one later work will build on: a missing loading, empty or error state; a confusing or wrong message; a pattern break others will copy; an untested edge case the requirements name. | Yes |
| `MEDIUM` non-blocking | A real defect with contained impact that no user flow hits and no later code depends on: a weak assertion, a duplicated helper, an unclear name in a public type. | No |
| `LOW` | Polish that doesn't change behaviour: wording, spacing, a shorter equivalent form, a comment. | No |

Every `MEDIUM` says which of the two it is, citing the criterion that decided it.

## Verdict

`FAIL` if there is any `CRITICAL`, `HIGH` or blocking `MEDIUM` finding. Otherwise `PASS`, even with non-blocking findings.

## Output

Return exactly this, followed only by any extra section your rubric requires:

```
VERDICT: PASS | FAIL
FINDINGS:
1. [HIGH] <path>:<line> - Problem: <what is wrong and why it matters>. Fix: <the concrete change required>.
2. [MEDIUM, blocking: <criterion>] <path>:<line> - Problem: ... Fix: ...
3. [MEDIUM, non-blocking: <criterion>] ...
4. [LOW] ...
```

Most severe first. With no findings, write `FINDINGS: none`. A finding spanning lines uses `<path>:<start>-<end>`. A missing file uses the path where it should exist and line `1`. A finding seen only in a screenshot cites the screenshot and the source line that renders it.
