# Test quality

## Commands

If `tree-id.sh` matches the evidence `tree:`, take the recorded test results as given. Otherwise run the project's full test suites. Every failing, skipped, focused (`.only`) or flaky test is a finding; include the failure output in the Problem. Stale generated files (bindings, schemas, clients) that the project checks are a finding against their source.

## Rubric

1. **Coverage of the change.** Every new or changed handler has tests of its success path and each validation rejection, including both sides of every limit, and of each failure it returns (store unavailable, locked, not found). Every query, parser, migration and crypto path has a test. Every new page or component has tests of its loading, empty, error and success states. The error-state rule in the dev contract (rule 6) holds. Every new client wrapper has a test asserting what it sends.
2. **Meaningful assertions.** Tests assert behaviour a user or caller can see. Flag tests that only check nothing threw, snapshot whole trees, or assert implementation details.
3. **Edge cases** the acceptance criteria name are tested: duplicates, empty input, malformed files, boundaries in money, dates and percentages.
4. **Isolation.** Tests use their own temp dirs and clean up, fake external services (keyrings, networks, clocks), call plain functions rather than framework wrappers, mock at the project's established seam, reset mocks between tests, and don't depend on order or wall-clock time.
5. **Fixtures.** Fake data only, never real names, account numbers or credentials. Sample files match any expected-results doc beside them.
6. **UI queries** go by role, label or text before CSS selectors.

Out of your dimension: style of the code under test, and whether the requirement itself is met (`requirements`).
