---
name: build-version
description: Organizer playbook for building one version of a project from its PRD. Turns the PRD's S#-T# tasks into a task graph, runs parallel dev subagents wave by wave with strict file ownership, then docs and prompt maintenance where needed, then loops a risk-selected review council until nothing blocking remains, then opens a PR. Use when the user says "build V<n>", "implement PRD-V<n>", or asks to run the version workflow.
argument-hint: V<n>
---

# Build version

You are the organizer. You plan, delegate, verify and decide. Leave all code and docs edits to dev subagents.

Flow: plan → code waves (parallel devs) → integration → docs and prompts (only where needed) → council (risk-selected) → blocking findings go back to the code waves; otherwise PR and hand-off.

**Project instructions** means the project's `AGENTS.md`, `CLAUDE.md`, or both. They hold the coding rules, layout, check commands, branch rule and anything else project-specific. This skill never restates them. Where they are silent, use the defaults given here.

**Skill files.** This folder holds `dev-contract.md` and `roles/`. The `council-review`, `write-prd` and `retrospective` skills sit in sibling folders. Resolve their absolute paths once and pass absolute paths in every subagent message; a subagent can't find them on its own.

**Subagents.** "Spawn" means start a subagent with your harness's subagent tool; "message" means send a follow-up to a running or idle one instead of spawning a new one. Spawn the tasks of one wave together so they run in parallel, then wait for all of them. Resume an agent that was cut off; never respawn it.

**Usage.** If your harness reports usage limits, check them before every phase. Near a limit, start no new agents: let in-flight ones finish, tell the user which limit and when it resets, and wait.

## 0. Scope

1. Read the project instructions, `plans/ROADMAP.md` and `plans/PRD-V<n>.md` (or the paths the project instructions name). Read earlier PRDs only when V<n> builds on something they define.
2. Build only V<n>. Never start V<n+1> or pull in a later version's items.
3. If the PRD has open questions, or a decision the PRD and project instructions don't settle, ask the user before you assign work.
4. Find the checkpoints the PRD marks. Stop at each one and wait for the user's decision.
5. Run `git status`. If the tree isn't clean, ask the user. Then `git fetch origin` and create the branch from `origin/main` (or the default branch) by the project's branch rule, else `v<n>-<one or two words>`. All work for V<n> happens on it.

## Design check

Run it, also inside `fix-bug`, only when the work involves encryption or key handling, schema architecture or a data-rewriting migration, sync or concurrency, a new external interface that is hard to reverse, or a design deadlock. Not for routine changes.

1. Spawn 2-3 read-only planning subagents, each told to design a structurally different approach.
2. Compare them against the PRD (or task brief) and the project instructions, and pick one.
3. Record the surprising or hard-to-reverse choice as an ADR task for the docs writer (`docs/adr/NNNN-<slug>.md`, or where the project keeps ADRs).
4. For a high-risk claim, demand proof where feasible: a failing test, a reproducer or a concrete code path.

## 1. Plan the task graph

1. The PRD's tasks (`S<k>-T<m>`) are the task graph: each is one complete behaviour slice with criteria and deps already set. Keep their IDs. To each task add the exact files it may create or edit, its acceptance proof (the tests or screenshots that show each criterion holds), and the exact interfaces it provides or consumes. Split a task (`S1-T2a`, `S1-T2b`) or add a dep only when file ownership forces it. A UI task lists at least one screenshot when the project can take them.
2. Give every file exactly one task. Two tasks that must edit the same file merge or run in sequence. Watch the hub files every feature touches (route tables, command or handler registries, shared type modules, navigation, fixtures); find them with `git log --stat` on recent features. A task that adds a field to a type that tests build as literals also owns every file with such a literal (grep for it).
3. Split along files, not layers: put each backend feature in its own module and each page in its own files, so tasks run side by side.
4. Run the Design check if it applies. Then write the cross-boundary contracts to `snapshots/V<n>/contracts.md` before anyone starts: each new endpoint, command or public function with its request and response types, field names and error kinds. For every UI mutation, state the success message and the error's next step. Quote every PRD formula or rule verbatim and add one worked example per edge it names. Re-read the contracts once for self-contradictions.
5. Add a dependency only where a task truly needs another's output. A contract is enough for UI work to proceed against an interface that doesn't exist yet. When the UI can't compile without generated or shared types, make the first wave one contract task that adds those types and the client wrappers with their tests.
6. Group tasks into waves: wave 1 is every task with no deps; each later wave is every task whose deps are all in earlier waves. At most five agents per wave; split a larger one.
7. If the plan needs a dependency (library or package) the PRD doesn't name, ask the user before you assign it. Their answer is the approved-dependencies list.
8. Show the user the graph as one table (ID, area, covers, files, deps, wave) plus the contracts, then start. Don't wait for approval unless step 0 or 1.7 left a question open.

`snapshots/` is local working state: make sure it is gitignored before writing to it.

## 2. Code waves

1. Before the first wave with a UI task, start the project's dev server in the background if its screenshots need one, and confirm it answers. Keep it running until step 6.
2. Spawn every task of a wave in parallel, one agent per task. Each task message contains: the task ID, the story and task with its acceptance criteria, the allowed files, the contracts path, the snapshot folder `snapshots/V<n>/` for UI tasks, a note when dead-code warnings are expected until a named later task lands, and "Follow `<absolute path>/dev-contract.md`." Pass paths, not file contents. Never call existing code "untested" in a task message.
   For a follow-up on a file, message its idle owner; spawn fresh with a narrow brief only when the owner's context is large or the files span owners.
3. Handle each report's `NEEDS`. Route a change in someone else's file to that file's task, and send dependency requests to the user. Start the next wave only when every task it depends on reports `STATUS: DONE`. Append each report's `COVERS` under its task ID to `snapshots/V<n>/coverage.md`; a criterion with no test and no `RUNTIME` note goes back to its task.
4. Look at one screenshot per changed page yourself; leave the rest to the UI council members. Send wrong or missing states back to the task. Keep the screenshot list for the council.

## 3. Integration

Run the project's full checks (build, format, lint, type-check, every test suite) once, from its instructions. Write `snapshots/V<n>/evidence.md`:

```
tree: <output of council-review/tree-id.sh>
changed_files:
<git diff --name-only origin/main, plus untracked files>
checks:
- `<command>`: pass | fail
```

Route each failure to the task that owns the file, and rerun only after a fix changed the tree. Don't rerun while `tree-id.sh` still matches `tree:`.

## 4. Docs and prompts

Start only after step 3 is green. Spawn the docs writer (`roles/docs-writer.md`) only if user-facing behaviour, commands, layout or facts the project instructions describe changed, and the prompt engineer (`roles/prompt-engineer.md`) only if the stack, conventions or workflow changed. Spawn the needed ones together. Record each skipped one and why in `snapshots/V<n>/metrics.md`.

## 5. Council loop

1. Run the `council-review` skill yourself; don't delegate it. Give it the PRD path (or, for a hotfix, the task brief), the round number, the contracts, coverage and evidence paths, the screenshot list and the approved dependencies. `tree-id.sh` must match the evidence `tree:` first; otherwise rerun step 3.
2. If the council passes, go to step 6.
3. If it fails, turn each `BLOCKING` finding into a fix task for the owner of the cited file. Decide every `CONFLICT` yourself first. Keep each finding's severity, `file:line`, Problem and Fix verbatim. Build a small task graph for the fixes with the step 1 rules and run it through steps 2 and 3, updating `coverage.md` from the fix reports. Each UI fix names the screenshots to retake; the next round gets only those. Run the docs writer or prompt engineer only if a finding targets their files.
4. Leave `NON-BLOCKING` findings as follow-ups, unless a fix task already edits that exact code. They are in `snapshots/V<n>/council-findings.md`; the `retrospective` skill triages them. While a round is already failing, also fold in a non-blocking `MEDIUM` from security or requirements on a sensitive path.
5. Re-review only what the fixes can affect. If a fix changed a contract, a migration, auth or secrets handling, a sensitive path or semantics other code shares, let `council-review` select members from scratch. Otherwise convene only the members with a blocking finding, plus each member whose dimension the fixes touch, plus `requirements` every round. Pass along rejected findings and their reasons.
6. If the same blocking finding survives three rounds, or two members still contradict each other after a full round, stop and ask the user.

## 6. Pull request and hand-off

1. Stop any background server you started, through the harness's own task control, never `pkill -f`.
2. Stage only the files listed in the dev reports' `CHANGED`. Ask the user about anything else `git status` shows. Never stage `snapshots/`. Commit once as `V<n>: <PRD title>`, push with `-u`, and open the PR against the default branch (`gh pr create`). The body has:
   - A summary of what V<n> adds, in a few lines.
   - The task checklist from the `requirements` member's last report.
   - The final council table: verdicts and counts only.
   - Every `RUNTIME` acceptance criterion as a manual check.

   For an `SB-<n>` fix, replace the checklist with one neutral line ("Hardening fix; reviewed privately"), show only verdicts, and make the manual check "verify the app works as before".

   **Publication rule.** In a public repo a listed weakness is a guide to attacking it. Council findings reach GitHub text (PR, commits, issues) only as `factory-bug` issues, and only after triage:
   - Always private, whatever the triage says: blocking findings, what earlier rounds failed on, and every `security` finding.
   - The `security` member sorts every other non-blocking finding, and each retrospective item that is a concrete defect, into `public` or `private`. When unsure: private.
   - `public` becomes a `factory-bug` issue, with the user's yes. `private` goes only to `snapshots/security-bugs.md` (gitignored) as `SB-<n>`. Everything committed or pushed for an `SB-<n>` fix (branch, test names, comments, docs, commit message, PR body) uses neutral wording ("Harden restore validation") and never names the weakness or the SB number.
   - Process ideas are never filed; they stay retro recommendations.

   In a private repo the user may relax this; ask once and record the answer in the project instructions.
3. If the project is an app, start it the way its instructions say, in the background, and watch the output until it is up with no errors. If it fails, go back to section 2 with the error.
4. Tell the user: the PR link (and that the app is running, if it is), the final council table with the path to `council-findings.md` and the top follow-ups, one screenshot per changed page, and every `RUNTIME` criterion as a step they can check.
5. Run the `retrospective` skill's tally (its steps 1.1 and 1.2); the HTML write-up is optional. Append to `snapshots/V<n>/metrics.md`: weighted tokens per phase, agent launches, council member launches, full integration runs, and fix and review rounds.
6. Stop. Don't merge. The next version gets its own session.
