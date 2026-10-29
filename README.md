# skills

My personal collection of reusable AI agent skills in the `SKILL.md` format. Each skill is a folder you can drop into any project so Claude Code, Cursor, or another agent that reads `SKILL.md` files can use it.

## Skills

| Skill | Purpose | Source / author |
| --- | --- | --- |
| [grill-me](skills/grill-me/SKILL.md) | Interview you relentlessly to sharpen a plan or design (run it with `/grill-me`). | [Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me), MIT |
| [grilling](skills/grilling/SKILL.md) | The interview procedure that `grill-me` calls. Included because `grill-me` doesn't work without it. | [Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling), MIT |
| [unslop](skills/unslop/SKILL.md) | Remove AI writing patterns from text (run it with `/unslop`). | [Lauren Tan, Cursor pstack plugin](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md), MIT |
| [yap-better](skills/yap-better/SKILL.md) | Rewrite a rough prompt to be clearer and more specific without changing its intent. | Sherlock64 (original) |

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # YAML frontmatter (name, description) + instructions
    references/     # optional supporting files
```

Skill folder names are kebab-case and match the `name` field in the frontmatter. The `description` field tells the agent when to use the skill.

## Using a skill in another project

Clone this repo once:

```bash
git clone https://github.com/Sherlock64/skills.git ~/skills
```

Then either symlink a skill into the project (stays in sync with this repo):

```bash
mkdir -p .claude/skills && ln -s ~/skills/skills/yap-better .claude/skills/yap-better
```

Or copy it (a frozen snapshot you can commit with the project):

```bash
mkdir -p .claude/skills && cp -r ~/skills/skills/yap-better .claude/skills/
```

For Cursor, use `.cursor/skills/` instead of `.claude/skills/`. To make a skill available in every project, put it in `~/.claude/skills/` instead.

When you install `grill-me`, install `grilling` alongside it.

## Third-party skills

`grill-me`, `grilling`, and `unslop` are copied verbatim from their upstream repos. Their files are not edited here. Each of those folders includes the upstream `LICENSE` with the original copyright notice:

- `grill-me`, `grilling`: copyright (c) 2026 Matt Pocock, MIT License. From [mattpocock/skills](https://github.com/mattpocock/skills) at commit `59db609`.
- `unslop`: copyright (c) 2026 Lauren Tan, MIT License. From [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack) (pstack) at commit `1ba91fc`.

To update one, copy the upstream folder over the local one again rather than editing it here.

## License

The original content in this repo is under the [MIT License](LICENSE). Vendored skills keep their own licenses, as listed above.
