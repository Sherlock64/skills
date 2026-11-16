---
name: write-prd
description: Write one versioned PRD (plans/PRD-V<n>.md) with the user through a grilling interview that settles every decision, checked against the code, as user stories with S#-T# build tasks in the house format. Use when the user says "write PRD-V<n>", "plan V<n>", "next PRD", or asks to turn a roadmap item into a PRD. Writes the PRD only; building it is the build-version skill.
argument-hint: V<n>
---

# Write PRD

"Project instructions" means the project's `AGENTS.md`, `CLAUDE.md`, or both. Paths below are defaults; use the ones the project instructions name.

## 1. Read

1. Read the project instructions, `plans/ROADMAP.md`, the glossary if there is one (`docs/glossary.md`), and the PRDs this version builds on.
2. Read the code, schema and fixtures the version touches. Check every environment or file-format fact a question depends on (running services, format limits, what the database allows) before you ask it.

## 2. Grill

1. Walk the version's decision tree depth-first: scope, then each story, then each task's behaviour, errors and edges. Walk each answer's follow-up branches before moving on.
2. Ask in rounds of at most four independent questions, each with your recommended answer and why. Use the harness's question tool if it has one.
3. Answer from the roadmap, the code and the project instructions whatever you can; ask only what they leave open. Stop only when no branch is open.
4. Use glossary terms exactly. Settle a name for every new domain term.
5. If an answer moves scope to another version, update `plans/ROADMAP.md` to match.

## 3. Confirm

Write a one-page summary of the decisions and the stories with their tasks to `snapshots/V<n>/prd-summary.html` (plain HTML, print styles; `snapshots/` gitignored). If a headless Chrome or Chromium is available, also print it to PDF (`<chrome> --headless --print-to-pdf=snapshots/V<n>/prd-summary.pdf --no-pdf-header-footer snapshots/V<n>/prd-summary.html`) and share that. Otherwise give the user the HTML path.

Get one yes before writing the PRD. A change goes back to step 2 for the branches it opens.

## 4. Write `plans/PRD-V<n>.md`

About 70-120 lines:

- `# <Project> — V<n> PRD: <title>`, then one paragraph saying what V<n> adds, ending "Builds on PRD-V1.md to PRD-V<prev>.md; see ROADMAP.md."
- `## User Stories`: one `### S<k>: <title>` per story. Each is a thin vertical slice, testable end to end, opening with "As a <user>, I want ..., so that ...". Under it, its tasks:
  `- **S<k>-T<m>** (backend | UI; deps: S<j>-T<i>, or none): <what it delivers>`, then its acceptance criteria as indented bullets.
- `## Decisions`: the choices the user made, one line each.
- `## New Terms`: each new domain term with a one-line definition, for the glossary at build time; or "None".
- `## Out of Scope`, and `## Checkpoint` only if the user sets one.

Rules:

- A task is one side's piece of its story (backend or UI) that one agent can build. A story spanning both has a backend task and a UI task, the UI task depending on the backend one. Projects without a UI use `backend` (or another one-word area) throughout. Name no files; `build-version` assigns them.
- Each acceptance criterion is an observable result a test or the running app can check: what the user sees, or what an interface returns or stores, never how the code does it. Each edge case is a criterion of its task.
- Mark criteria only the running app can check as `RUNTIME`.
- Name every dependency the user approved inline, for example "`requests` (approved dependency)", so `build-version` doesn't ask again.
- State every formula or rule once, exactly, with one worked example per edge case.
- Name the migration shape when the database limits it (for example a table rebuild).
- No implementation detail beyond what the user decided.

## 5. Stop

Work on a branch named by the project's branch rule. Show the user the PRD path and a summary, then stop. Don't build; that is `build-version`, in its own session.
