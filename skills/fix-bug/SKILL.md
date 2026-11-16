---
name: fix-bug
description: Playbook for fixing one bug or making one small fix as a hotfix, from reproduction through a failing regression test, the smallest root-cause fix, checks and a risk-selected council review to a PR. Use when the user reports a bug, wrong behaviour or error, gives a factory-bug issue (#<n> or its URL) or a private security bug (SB-<n>), or asks for a small fix that needs no PRD.
---

# Fix bug

"Project instructions" means the project's `AGENTS.md`, `CLAUDE.md`, or both. This skill uses files from the sibling `build-version` and `council-review` skill folders; resolve their absolute paths first.

1. **Branch.** Run `git status`; if the tree isn't clean, ask the user. `git fetch origin`, then create the branch from `origin/main` (or the default branch) by the project's branch rule, else `fix-<one or two words>`; for `SB-<n>`, neutral words (the `build-version` publication rule, step 6.2). Evidence goes in `snapshots/<version or branch>/` (gitignored).
2. **Reproduce.** Given `#<n>` or an issue URL, `gh issue view <n>` is the report; if it looks security-sensitive after all, stop and ask. Given `SB-<n>`, its entry in `snapshots/security-bugs.md` is the report, and from here on every test name, comment and doc follows the neutral-wording rule; say so in each delegated task. Find the exact input and code path that fail, citing `file:line`. If it won't reproduce, or the fix needs a decision the report doesn't settle, ask the user. A novel or high-risk decision gets the `build-version` Design check. Then write the task brief as story `S1` in the `write-prd` format: one "As a user..." line and tasks `S1-T1`... with acceptance criteria, the first being that the reported input now behaves correctly.
3. **Regression test.** Write the test that fails for this bug at a public seam (dev contract rule 5) and run it to see it fail. Record each criterion's test in `coverage.md` as `COVERS` lines (dev contract rule 10).
4. **Smallest fix.** Fix the root cause once, in the shared code; grep every caller of what you change. Do it yourself under the project instructions and dev contract rules 1-6, or, when the fix spans areas or is more than a small change, delegate each file set to a dev subagent as `build-version` step 2.2 does. UI changes get screenshots when the project can take them.
5. **Task check.** Run the project's checks for the changed code (dev contract rule 9).
6. **Integration.** `build-version` step 3: full checks once, written to `evidence.md`.
7. **Council.** Run the `council-review` skill with the bug report and the `S1` brief as the task brief; it selects members by risk. Fix blocking findings as `build-version` step 5 does.
8. **PR.** `build-version` step 6.2: commit once as `fix: <summary>` (or the project's convention), push, open the PR, publishing findings only as that step allows. For an issue, the commit message and PR body include `Closes #<n>`. For `SB-<n>`, follow the neutral-wording rule and PR body carve-out, then set its entry to `Status: fixed (<branch>)`. Tell the user the PR link and how to check the fix. Don't merge.
