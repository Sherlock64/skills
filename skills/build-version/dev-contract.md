# Dev contract

Every dev subagent the organizer spawns (code, docs or prompts) follows this file. "Project instructions" means the project's `AGENTS.md`, `CLAUDE.md`, or both.

## File ownership

Your task message names the exact files you may touch. Several devs edit the same working tree at once, so that list is absolute. Nobody edits `plans/`: the user writes PRDs, or the organizer does with the user through the `write-prd` skill.

## Rules

1. Edit only the files your task message allows. If the task needs a change in any other file, stop and report the exact change needed (file, what, why) instead of making it.
2. Follow the project instructions. They are the single source of coding rules; this contract does not restate them.
3. Never add a dependency (library, package, crate, module). If one is needed, report its name, version and reason; the organizer asks the user.
4. Build only what the task asks for. No features, options or abstractions beyond it.
5. For nontrivial logic (parsing, money, validation, state changes, anything security touches), work red-green at a public seam: write the test against a public function, handler or rendered component; see it fail; then make it pass.
6. Done means tested: every new component has one test per error state it renders, and every new backend operation one per failure it returns.
7. A build or test failure in a file you don't own is reported, not fixed. A build tool waiting on a lock means another dev is building: wait, don't kill it. If you edit a hub file, retake every earlier screenshot of the states it changes.
8. Don't commit, push or change git state.
9. Before reporting done, run the checks for what you changed and make them pass: format only your own files, and run the tests for the modules and test files you changed or affected, using the project's commands. Don't run the full suites; the organizer runs them once at integration. Dead-code warnings your task message says are expected may stay; list them in `CHECKS`.
10. Report in this format, and nothing outside these seven fields:
    ```
    STATUS: DONE | BLOCKED
    CHANGED: <every file created, edited or deleted>
    CHECKS: <each command run and its result>
    SNAPSHOTS: <each screenshot path - route, state, what you checked; or "none">
    NEEDS: <changes needed in files you don't own, deps to approve, questions; or "none">
    COVERS: <one line per acceptance criterion: "<task ID> <criterion> -> <test name(s)>", or "-> RUNTIME" when only the running app can show it>
    NOTES: <at most five one-line items, or "none">
    ```
    Story and task IDs go only in the report, never in code, test names or comments.

## UI tasks

- Every data view has loading, empty and error states, and every mutation shows success and ignores repeat presses while busy. Test each async state (loading, error, retry that fails again, cancel).
- Every dialog, and every retry that replaces its button, returns focus to a sensible control.
- Reuse the project's existing components, design tokens and patterns before writing new markup. User-facing labels reuse the PRD's words.
- If an interface you need doesn't exist yet, code against the contract and mock it in tests. Report anything the contract is missing.
- **Screenshots.** Check what you built by looking at it. If the project instructions describe a way to capture the UI (a screenshot script, a fixture page, a headless browser), capture only the states your task changed into the snapshot folder, prefixing file names with your task ID. Open each image and check layout, alignment, spacing, overflow, truncation and contrast against the PRD and the existing pages; fix and recapture until it looks right. If the project has no way to capture the UI, say so in `NOTES` and put `none` in `SNAPSHOTS`. If the dev server the organizer runs isn't answering, report `BLOCKED`.
