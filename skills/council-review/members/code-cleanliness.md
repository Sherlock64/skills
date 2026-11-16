# Code cleanliness

## Commands

If `tree-id.sh` matches the evidence `tree:`, take the recorded format, lint and type-check results as given. Otherwise run the project's format-check, lint and type-check commands; every failure, error or warning is a finding. Don't ask for linters or formatters the project doesn't use; adding them means new dependencies.

## Rubric

1. **Project coding rules.** Every rule in the project instructions that no other member owns (for example where types live, how money or time is represented, naming) is yours. Honour the exemptions the instructions grant, such as generated or vendored code; never report them.
2. **Errors.** Errors follow the project's error type and mapping conventions. Bad input gets the project's validation error. No panics, `unwrap`, bare `except`, or equivalent outside tests and startup. No errors swallowed silently.
3. **Established patterns.** New code matches how the codebase already does the same thing: import style, file naming, module layout, how handlers wrap logic, how the UI calls the backend. Generated files are never hand-edited.
4. **Readability.** Names say what things are. Functions do one thing. Nesting stays shallow. No commented-out code, stray debug prints or TODOs. Comments explain why, never what.
5. **Language idioms.** Use the language's idiomatic forms (error propagation, iteration, borrowing or immutability, narrow visibility) where they read better than the hand-rolled version.

Out of your dimension: whether code should exist at all and duplication (`minimalism`), security, tests, visuals, UX, accessibility and requirements.
