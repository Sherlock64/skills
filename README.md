# skills

My personal collection of reusable AI agent skills in the `SKILL.md` format. Each skill is a folder you can drop into any project so Claude Code, Codex, Cursor, or another agent that reads `SKILL.md` files can use it. None of them assume a programming language.

## Skills

| Skill | Purpose | Source / author |
| --- | --- | --- |
| [grill-me](skills/grill-me/SKILL.md) | Interview you relentlessly to sharpen a plan or design (run it with `/grill-me`). | [Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me), MIT |
| [grilling](skills/grilling/SKILL.md) | The interview procedure that `grill-me` calls. Included because `grill-me` doesn't work without it. | [Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling), MIT |
| [unslop](skills/unslop/SKILL.md) | Remove AI writing patterns from text (run it with `/unslop`). | [Lauren Tan, Cursor pstack plugin](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md), MIT |
| [yap-better](skills/yap-better/SKILL.md) | Rewrite a rough prompt to be clearer and more specific without changing its intent. | Sherlock64 (original) |
| [write-prd](skills/write-prd/SKILL.md) | Interview you into a versioned PRD (`plans/PRD-V<n>.md`) of user stories with buildable `S#-T#` tasks. | Sherlock64 (original) |
| [build-version](skills/build-version/SKILL.md) | Organizer playbook: build one PRD with parallel dev subagents, review it with `council-review`, open a PR. | Sherlock64 (original) |
| [council-review](skills/council-review/SKILL.md) | Risk-selected review by up to eight read-only reviewer subagents (security, tests, requirements, cleanliness, minimalism, UI, UX, accessibility). | Sherlock64 (original) |
| [fix-bug](skills/fix-bug/SKILL.md) | Hotfix playbook: reproduce, failing regression test, smallest fix, council review, PR. | Sherlock64 (original) |
| [investigate](skills/investigate/SKILL.md) | Answer a question about the codebase with `file:line` evidence and no changes. | Sherlock64 (original) |
| [retrospective](skills/retrospective/SKILL.md) | Local HTML retro of a Claude Code or Codex session with a token tally, then file its defects as issues. | Sherlock64 (original) |
| [factory-cleanup](skills/factory-cleanup/SKILL.md) | Bundle open `factory-bug` issues into one minor version and build it. | Sherlock64 (original) |

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # YAML frontmatter (name, description) + instructions
    *.md, *.py ...  # optional supporting files the skill reads or runs
    agents/openai.yaml  # optional Codex metadata (display name, invocation policy)
```

Skill folder names are kebab-case and match the `name` field in the frontmatter. The `description` field tells the agent when to use the skill; keep it under 500 characters, Codex's limit.

## Using a skill in another project

Clone this repo once:

```bash
git clone https://github.com/Sherlock64/skills.git ~/skills
```

Claude Code reads skills from `.claude/skills/` (per project) or `~/.claude/skills/` (every project). Codex reads them from `.agents/skills/` (per project) or `~/.agents/skills/` (every project). Cursor uses `.cursor/skills/`.

Symlink a skill into a project (stays in sync with this repo), for both Claude Code and Codex:

```bash
for d in .claude/skills .agents/skills; do mkdir -p $d && ln -s ~/skills/skills/yap-better $d/yap-better; done
```

Or copy it (a frozen snapshot you can commit with the project):

```bash
for d in .claude/skills .agents/skills; do mkdir -p $d && cp -r ~/skills/skills/yap-better $d/; done
```

Or install every skill for every project:

```bash
for d in ~/.claude/skills ~/.agents/skills; do mkdir -p $d && ln -s ~/skills/skills/* $d/; done
```

In Claude Code, run a skill with `/<name>`; in Codex, with `$<name>`. Both also pick one on their own when your request matches its description.

When you install `grill-me`, install `grilling` alongside it.

The workflow skills (`write-prd`, `build-version`, `council-review`, `fix-bug`, `factory-cleanup`, `retrospective`) call each other and read each other's files, so install them together.

## Setting up a project for the workflow skills

The workflow skills hold no project facts. They read them from the project's agent instructions: `AGENTS.md` (Codex), `CLAUDE.md` (Claude Code), or both (keep them in sync, or make `CLAUDE.md` say `@AGENTS.md`). Put these there:

- **Coding rules and layout:** what lives where, conventions reviewers should enforce.
- **Check commands:** how to build, format, lint, type-check and run tests, for the whole project and for one module or file.
- **Branch rule:** how to name version and hotfix branches, for example `v<n>-<slug>` and `v<n>.<m>.<p>-<slug>`.
- **Sensitive paths:** files that make a change `sensitive` for `council-review` (auth, crypto, migrations, handlers). Without a list, the skill uses a generic default.
- **Screenshots (UI projects):** a command that captures a page in a given state to a PNG. Without one, UI review works from code only.
- **Review (optional):** extra rubric items per council member, under a `Review` heading.

The skills write their working files to `snapshots/` and `retros/`; add both to `.gitignore`. PRDs go in `plans/`, unless the instructions name another folder.

## Third-party skills

`grill-me`, `grilling`, and `unslop` are copied verbatim from their upstream repos. Their files are not edited here. Each of those folders includes the upstream `LICENSE` with the original copyright notice:

- `grill-me`, `grilling`: copyright (c) 2026 Matt Pocock, MIT License. From [mattpocock/skills](https://github.com/mattpocock/skills) at commit `59db609`.
- `unslop`: copyright (c) 2026 Lauren Tan, MIT License. From [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack) (pstack) at commit `1ba91fc`.

To update one, copy the upstream folder over the local one again rather than editing it here.

## License

The original content in this repo is under the [MIT License](LICENSE). Vendored skills keep their own licenses, as listed above.
