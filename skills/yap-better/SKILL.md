---
name: yap-better
description: Rewrite a rough prompt so it is clearer and more specific without changing its intent or scope. Use when the user says "yap better", "improve this prompt", or "reword this prompt", or hands over a draft prompt and asks for it to be tightened up.
---

# Yap better

Turn the user's rough prompt into one another model (or person) can act on without guessing. The rewrite says the same thing as the original, only more precisely.

## Rules

1. **Keep the intent and scope.** The rewritten prompt asks for exactly what the original asked for. Do not add features, steps, deliverables, or quality bars the user didn't mention. If you think something is missing from the scope, raise it as a question instead of writing it in.
2. **Fill in what's implied, not what's invented.** Make explicit the context, constraints, and expected output format that the original already implies or that the conversation makes clear. If a detail isn't implied and isn't essential, leave it out.
3. **Ask before guessing on essentials.** If something essential is ambiguous (who the audience is, what the output should be, a constraint that changes the whole approach), ask the user 1 to 3 short, specific questions before rewriting. Don't ask about things that only affect polish. If nothing essential is ambiguous, skip the questions and rewrite straight away.
4. **Keep the user's voice where it carries meaning.** Keep their terms, names, and examples. Fix vagueness, not style.

## What a good rewrite usually has

Include only the parts the prompt needs:

- **Goal:** what the result is for, in one or two sentences.
- **Context:** the background the reader needs and wouldn't otherwise have.
- **Task:** what to do, stated concretely.
- **Constraints:** limits the user stated or clearly implied (length, tools, tone, things to avoid).
- **Output format:** what the answer should look like (structure, file type, length, sections).

## Output

If you need to ask questions, ask them (numbered, at most 3) and stop. Rewrite after the user answers.

Otherwise, reply with:

1. The rewritten prompt in a single fenced code block, ready to copy.
2. A short bullet list headed **What changed**, one bullet per meaningful change, each saying what changed and why. Keep it to the changes that matter; skip trivial wording fixes.
