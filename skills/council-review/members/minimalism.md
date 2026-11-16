# Minimalism

## Rubric

1. **Dependencies.** Compare every dependency manifest and lockfile against the default branch (`git diff origin/main -- <manifest>`; with no commits, take the whole file as new). Any added dependency or feature flag that is neither in the approved list nor named by the PRD or roadmap is a finding. An approved dependency must be mature and well documented, with no mature alternative already installed.
2. **Scope creep.** Flag any feature, setting, option, route or table the requirements don't ask for, and any item from the PRD's Out of Scope list.
3. **Speculative code.** Flag abstractions, interfaces, generics, wrappers, config or parameters with one use and no requirement behind them, and any "for later" code.
4. **Duplication.** Flag code that re-implements something the repo, the standard library or an installed dependency already has. Name the existing one.
5. **Dead weight.** Flag unused exports, files, components, styles, columns, error variants or parameters.
6. **Length.** Flag code that could be clearly shorter with the same behaviour and readability. Name the shorter form.

Out of your dimension: style of code that should exist (`code-cleanliness`) and missing requirements (`requirements`).
