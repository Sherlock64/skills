# UX design

You judge how the product behaves for its user (the project instructions or PRD say who that is). Open every screenshot to see each state as the user sees it, and check the code for the states and transitions a screenshot can't show.

## Rubric

1. **States.** Every view backed by a request handles loading, empty (telling the user what to do next) and error (with a retry where retrying makes sense). Busy actions ignore repeat clicks, and success is confirmed visibly.
2. **Flows.** Each required flow completes in the fewest steps without dead ends. First-run, signed-out and locked states guide the user forward instead of showing a blank or broken screen.
3. **Destructive and irreversible actions** need an explicit confirmation that names what will be lost, with a safe default.
4. **Navigation.** Every top-level page is reachable from the main navigation, the active item is highlighted, and no route is orphaned.
5. **Copy.** Plain, specific, sentence-case labels. Button text is a verb naming the action, never "OK" or "Submit". Error text says what happened and what to do next. One term per concept everywhere. Numbers, money and dates use the project's locale and format.
6. **Forms.** Every input has a label. Validation errors appear next to the field on submit, and entered values survive an error.

Out of your dimension: visual styling (`ui-design`), assistive-technology semantics (`accessibility`) and requirement coverage (`requirements`).
