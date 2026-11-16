# Requirements

## Method

1. List every task (`S<k>-T<m>`) of every story in the PRD, or of the hotfix brief's story `S1`, and every acceptance criterion under it. Skip none.
2. For each criterion, read the story and task, then its line in the coverage map. Find the code that satisfies it and read the mapped test: it must exercise this criterion, assert its observable result, and have passed in the evidence file. A matching file or test name is not evidence. When you doubt a behaviour, run only its tests.
3. Mark each one:
   - `MET`: fully implemented as written. Cite the evidence.
   - `PARTIAL` or `MISSING`: a finding. Cite the closest code, or where it should go. A criterion with no mapped test, or one that doesn't assert it or didn't pass, is at most `PARTIAL`.
   - `RUNTIME`: can only be confirmed in the running app or on the target platform. Cite the code path that should satisfy it. Not a finding unless that path is wrong or missing.
4. Judge a criterion that restates a project rule under that rule, exemptions included.
5. Read stories and criteria literally. Flag any narrowed meaning: a missing field, a weaker algorithm, a skipped sub-clause.
6. **Checkpoints.** If the PRD marks one, the scope summary must record the user's decision. Work past an unrecorded checkpoint is a finding.
7. **Branch.** Run `git branch --show-current` and `git merge-base --is-ancestor origin/main HEAD`. A name that breaks the project's branch rule, or a branch not based on the latest default branch, is a finding.

Extra features and Out of Scope work belong to `minimalism`.

## Extra output section

After `FINDINGS`, add:

```
CHECKLIST:
| ID | Status | Evidence |
|---|---|---|
| S1-T1: <criterion> | MET | src/db.py:9; test test_db::test_opens_in_temp_dir |
| S2-T1: <criterion> | RUNTIME | src/main.rs:12 |
```
