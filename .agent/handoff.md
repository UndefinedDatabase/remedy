# Handback — F037 Rendered diff viewer, round 18

## Session

SESSION 5 of feature F037 · round 18 · rounds so far 18

Soft limit not reached: 18 of 25 rounds, session 5 of 7.

## Range

Review of `5a4d5257..HEAD`, where HEAD is the C7 commit that writes this file.

## Commits

### 4b270773 chore(agent): save the F037 R18 step block verbatim

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r18.md | +385/-0 | C0a: the reviewer's block saved byte for byte |

### 7a4b4793 chore(agent): mirror the R18 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +289/-266 | C0b: the same bytes, mirrored from the committed C0a blob |

### a684321e docs(agent): set the plan to R18, the round that mounts the viewer

| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +26/-23 | C1: full rewrite from the PLANF037R18 slice |

### 5efe6e10 docs(agent): record the R17 gate and register finding R-0725

| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +8/-0 | C2: GATER17 then FINDING725, appended in that order |

### ee75a7f4 test(ui-contracts): scope the diff door presence checks to one function

| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_diff_envelope_door.py | +43/-6 | C3, SPEC S1: both presence assertions scoped, plus the vacuity test |
| .agent/live_review.md | +2/-0 | C3, SPEC S2: the `Landed:` line for R-0725 |

### ce3407ef feat(ui): give the detail popover the open diff entry point

| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/components/detail/DetailPopover.tsx | +18/-1 | C4, SPEC S3: the optional `onOpenDiff` prop and its button |

### fdd94580 feat(ui): mount the diff view behind the shell open diff state

| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/components/shell/RemedyShell.tsx | +67/-1 | C5, SPEC S4-S6: state, the cancelling read, the panel |

### a1d08610 test(ui-contracts): gate the diff viewer mount by reading its three files

| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_diff_viewer_mount.py | +363/-0 | C6, SPEC S7: the new mount guard |

### C7 — the commit that writes this file

| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C7: this handback; a handoff cannot table its own commit (R-0149) |

Every insertion count above is the `+` column of `git show --numstat` for that commit,
and every one is under 500. The largest is C6 at 363.

## External actions

- `git worktree add .remedy-wt/g6-r18 a1d08610 --detach` — created for G6. Removed with
  `git worktree remove --force .remedy-wt/g6-r18`.
- `git worktree add .remedy-wt/g6-base 5a4d5257 --detach` — created to measure the
  PRE-repair colour of mutations (a) and (b). Removed the same way.
- `git worktree prune`, then `git worktree list` → the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- `git push -u origin feature/f037-rendered-diff-viewer` after C7.
- No PR created. Nothing merged. No history rewritten. No force push.

## Verification

G1 HYGIENE — exit 0. `.agent/STOP` read from disk before C0a: **ABSENT**. Read again
immediately before C7: **ABSENT**. `git rev-parse HEAD` before C0a =
`5a4d525722532a98e15e10c8db85cf90447bddd4`, which is `5a4d5257`.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` = **0**, measured directly after C0a, C0b, C1 and C6.
For C2 through C5 the reading is 0 by the same chain: the `git diff --stat` taken at the
start of each following step listed only the files that step had just edited, so nothing
was left behind by the commit before it, and the tree reads 0 at C6 with no residue from
any earlier step. Everything else written this round lives under the gitignored
`.remedy-wt/`.

G2 TRANSPORT — one digest comparison, all three readings agree.
`git show 4b270773:.agent/authored/f037-r18.md` → **29389 bytes**, **385 lines**, sha256
**`42f16726baf7983cccab6f0dc17529c69a5f2f0a0dd9a558977792f0fffbb81b`**. The delegation
named 29389, 385 and `42f16726…fffbb81b`: all three MATCH.
`git rev-parse 7a4b4793:.agent/authored/f037-r18.md` and
`git rev-parse 7a4b4793:.agent/last_block.md` are both blob
`3557fd38113682d42b3d9ad3de9868bce5c62022` — the SAME blob.

G3 EXTRACTION AND CAPS — measured on the committed C0a blob. Content lines: PLANF037R18
**49**, GATER17 **5**, FINDING725 **1**. CONTENT = **55**. TOTAL = **385**.
PROSE = 385 − 55 = **330**. TOTAL <= 490: **True**. PROSE <= 400: **True**.

G4 THE PLAN AT C1 — exit 0. PLANF037R18 extracted programmatically from the committed C0a
blob, never retyped. `git show a684321e:.agent/plan.md` is **2630 bytes**, the slice is
**2630 bytes**, and they are byte equal INCLUDING the trailing newline: **True**.
Negative control against the slice minus its trailing newline: **False**.
`wc -l` = **49**, strictly under 50: **True**. Lines exactly `## Goal`: **1**. Lines
exactly `## Next Steps`: **1**.

G5 THE RECORD AT C2 — exit 0. Both slices extracted from the committed C0a blob.
Reader (a): `git show 5a4d5257:.agent/live_review.md` + one newline + GATER17 + one
newline + FINDING725 equals `git show 5efe6e10:.agent/live_review.md` → **True**.
Reader (b): N counted by the script across both slices = **4** blank-line-separated units
(3 from GATER17, 1 from FINDING725); the committed file's last 4 units equal those 4 units
IN ORDER → **True**. Negative control for each reader, flipping `the round that opened
T003` → `T004` inside GATER17's FIRST paragraph: reader (a) **False**, reader (b)
**False**. The pre-round blob is a byte PREFIX of the committed one: **True**.
Line-anchored counts over the committed file, with the figure at `5a4d5257` beside each:
`^- R-\d+ — ` **286** (285 at base), `^Done: R-\d+ — ` **34** (34), `^Landed: R-` **1**
(1), `^Gate: F\d+ R\d+ — ` **88** (87), open set as registered ids minus ids named by a
`Done:` line **253** (252 at base), every registered id distinct **True**. The only id
this round registers is **R-0725**. `^Landed: R-` becomes **2** at C3 as the block
predicts, and is still 1 at C2.

G6 THE RED-PROOFS — all runs in the disposable worktree `.remedy-wt/g6-r18` at the C6
tree, `__pycache__` purged before every run, `python3 -B` throughout, one pytest process
at a time. Test set:
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_view_render.py`.

- UNMUTATED CONTROL before any mutation: **exit 0**, `39 passed in 0.26s`.
- UNMUTATED CONTROL after the last restore: **exit 0**, `39 passed in 0.26s`.

UNIQUENESS READINGS, taken by me per finding `R-0629`. Counted in the named file BEFORE
editing; where the natural string read 2, it was EXTENDED until it read 1 and the extended
string is what was mutated:

| Case | File | String counted | Count | Mutated string | Count |
|------|------|----------------|-------|----------------|-------|
| (a) | remedyApi.ts | `/diff?` | 2 | `/api/jobs/${job}/diff?` | 1 |
| (b) | remedyApi.ts | `readDiffEnvelope(` | 2 | `    return readDiffEnvelope(payload);` | 1 |
| (c) | DetailPopover.tsx | `type="button"` | 2 | `<button type="button" onClick={() => onOpenDiff(task.id)}>` | 1 |
| (d) | DetailPopover.tsx | `task.id` | 2 | `onOpenDiff(task.id)` | 1 |
| (e) | RemedyShell.tsx | `<DiffView envelope={diffEnvelope} />` | 1 | same | 1 |
| (f) | RemedyShell.tsx | `if (!cancelled) setDiffEnvelope(envelope);` | 1 | same | 1 |

One at a time, each restored byte-identically to its pre-mutation sha256 before the next
(every restore verified equal):

| Case | Mutation | Exit | Summary | Failing node id |
|------|----------|------|---------|-----------------|
| (a) | job template → `/diffs?` | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_envelope_door.py::TestTheJobScopeRouteAgrees::test_the_client_addresses_the_diff_endpoint` |
| (b) | try-branch reader call → bare cast | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_envelope_door.py::TestTheDoorNormalizesThroughOneFunction::test_every_payload_leaves_the_door_through_the_reader` |
| (c) | `type="button"` → `type="submit"` | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_viewer_mount.py::TestThePopoverOffersTheEntryPoint::test_the_entry_point_is_a_real_button` |
| (d) | passes `selectedNode.nodeId` | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_viewer_mount.py::TestTheEntryPointPassesTheTaskId::test_the_button_passes_the_task_id_and_not_the_node_id` |
| (e) | `<DiffView` element deleted | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_viewer_mount.py::TestTheShellReallyMountsTheViewer::test_the_shell_really_renders_the_diff_view` |
| (f) | stale-response guard removed | **1** RED | `1 failed, 38 passed in 0.28s` | `test_diff_viewer_mount.py::TestALateResponseIsDiscarded::test_the_effect_checks_the_flag_before_storing_the_envelope` |

All six are exit 1. None came back green. (e) was applied by replacing the element with
`null` rather than by deleting the characters, because deleting them alone leaves the
ternary syntactically broken and the mutation must isolate "the panel renders nothing",
not "the file no longer parses"; the guard's subject, the `<DiffView` element, is gone
either way.

(a) AND (b) ARE THE FINDING'S OWN PROOF, so I measured their PRE-REPAIR colour myself
rather than inheriting it. In a second disposable worktree `.remedy-wt/g6-base` at
`5a4d5257`, over `tests/ui_contracts/test_diff_envelope_door.py` alone: control **exit 0**
`12 passed`, mutation (a) **exit 0 — GREEN**, mutation (b) **exit 0 — GREEN**, control
after **exit 0** `12 passed`. Both were GREEN before C3 and both are RED after it, which
is the repair of `R-0725` doing exactly what the finding says it should.

G7 SUITES, TYPES, LINT AND CANARY AT C6 — primary checkout, ONE pytest process at a time,
every one exit 0:

| Command | Exit | Summary | Base figure |
|---------|------|---------|-------------|
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | `630 passed, 4 skipped in 5.59s` | 616 passed, 4 skipped |
| `python3 -m pytest tests/ui_server/ -q` | 0 | `495 passed in 31.58s` | 495 passed |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | `52 passed in 5.27s` | 52 passed |
| `python3 -m pytest tests/regression/test_named_bugs.py -q` | 0 | `64 passed, 6 skipped in 1.30s` | 64 passed, 6 skipped |
| `python3 -m pytest tests/docs/ -q` | 0 | `295 passed in 0.44s` | 295 passed |
| `python3 -m ruff check tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_envelope_door.py` | 0 | `All checks passed!` | — |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 20.56s` | 42 passed |

`tests/ui_contracts/` is 630 against 616 at base, a difference of exactly 14: the 13 tests
of the new `test_diff_viewer_mount.py` and the one vacuity test C3 added to
`test_diff_envelope_door.py` (12 → 13). Nothing else moved.

THE TYPESCRIPT NODE INSIDE `tests/ui_server/` **PASSED — it did not skip.**
`python3 -m pytest tests/ui_server/ -q -k test_typescript_compiles` → exit 0,
`1 passed, 494 deselected in 2.03s`. `apps/ui/node_modules/.bin/tsc` is present, so
`tsc --noEmit` really type-checked this round's two `.tsx` edits.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6 — exit 0.
`git diff --name-only 5a4d5257..a1d08610` returns eight paths:
`.agent/authored/f037-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `apps/ui/src/components/detail/DetailPopover.tsx`,
`apps/ui/src/components/shell/RemedyShell.tsx`,
`tests/ui_contracts/test_diff_envelope_door.py`,
`tests/ui_contracts/test_diff_viewer_mount.py`.
ACTUAL MINUS EXPECTED = `[]` (empty). EXPECTED MINUS ACTUAL = `['.agent/handoff.md']`
alone, which C7 writes.
`git diff --stat 5a4d5257..a1d08610 -- packages/` → **EMPTY**.
`git diff --stat 5a4d5257..a1d08610 -- apps/ui/src/api/` → **EMPTY** — constraint 3 made
mechanical: the api client, the view model and `DiffView.tsx` are untouched.
Per-commit insertions from `git show --numstat`: 385, 289, 26, 8, 45, 18, 67, 363 — each
under 500, and each matches the `+/-` column of the `## Commits` table above cell by cell
(C3's 45 is its two rows, 43 + 2).
Marker leakage, lines matching `^<<<SLICE ` or `^<<<END `: `.agent/plan.md` **0**,
`.agent/live_review.md` **0**, `apps/ui/src/components/shell/RemedyShell.tsx` **0**,
`tests/ui_contracts/test_diff_viewer_mount.py` **0**; CONTROL over the C0a blob
`.agent/authored/f037-r18.md` **6**, which is non-zero as required.
`git ls-files .remedy-wt | wc -l` → **0**.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

- **C0a.** `.remedy-wt/f037-r18-block.md` copied with `cp`, never retyped. The committed
  blob at `4b270773` is 29389 bytes / 385 lines / sha256
  `42f16726baf7983cccab6f0dc17529c69a5f2f0a0dd9a558977792f0fffbb81b`, equal on all three
  readings to the ones the delegation named and to the scratch original on disk.
- **C0b.** `.agent/last_block.md` written from `git show 4b270773:.agent/authored/f037-r18.md`,
  so its bytes come from the COMMITTED blob rather than from the scratch file. At `7a4b4793`
  both paths resolve to the one blob `3557fd38113682d42b3d9ad3de9868bce5c62022`.
- **C1.** PLANF037R18 extracted from the committed C0a blob by script and written
  unchanged. Byte equal including the trailing newline; the minus-trailing-newline control
  is False.
- **C2.** GATER17 and FINDING725 extracted from the same committed blob and appended in
  that order. Reader (a) and reader (b) both True; both negative controls False; the base
  blob is a byte prefix.
- The `Landed:` line at C3 and all production code are MY wording, per SPEC S2 and
  constraint 2, and are not reviewer-authored text.

## Deviations & assumptions

1. **NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE.** Eight commits landed in exactly the
   order C0a, C0b, C1, C2, C3, C4, C5, C6, C7 — nothing added, nothing dropped, nothing
   reordered.

2. **SPEC S1(b) NEEDED A TIGHTER SCOPE THAN ITS OWN WORDING, and I wrote the tighter one.**
   S1(b) asks that the assertion read `loadDiffEnvelope`'s BODY so the `import` line can no
   longer satisfy it. But G6(b) mutates the try branch's reader call while leaving the
   CATCH branch's `readDiffEnvelope(null)` in place — and that call is inside the body, so
   a body-wide `in` check would have come back GREEN and failed the gate. The assertion I
   wrote reads the body and then splits it at `} catch`, requiring `readDiffEnvelope` on
   BOTH exits. That is strictly inside what S1(b) orders and is what makes G6(b) red;
   flagging it because a reviewer diffing SPEC against code will see more than "the body".

3. **THE ENTRY POINT INHERITS THE "Changed files" SECTION'S OWN CONDITION.** SPEC S3 orders
   the button placed in that section, and the section already renders only when
   `changedFilesSafe` is a non-empty list. So the button's real condition is
   `changedFilesSafe && task && onOpenDiff`, not the two S3(b) names. Both S3(b) conditions
   hold as stated — they are necessary, and the button is never a dead control — but a task
   run with a diff and no safe file list shows no way in. I did not widen the section's
   condition, because that would change an element the change set does not authorise me to
   change and which `tests/ui_server/test_dashboard_contract.py` reads. Raising it here
   rather than deciding it.

4. **THE BUTTON AND THE PANEL WRAPPER CARRY NO CLASS.** Constraint 6 forbids a new CSS file
   and a layout class for the panel, and `DetailPopover.module.css` is not in the change
   set, so neither the entry-point button nor the panel `<section>` has one. Both are bare
   landmarks, as `DiffView`'s own root is, and each says so in a comment beside it.

5. **THE DIFF PANEL IS A SIBLING OF THE POPOVER, NOT A CHILD OF `<main>`.**
   `tests/ui_contracts/test_main_layout_guard.py::test_shell_main_has_four_children` holds
   the main column to exactly four components. Putting the panel there would have broken a
   guard this round is not repairing.

6. **THE CANCELLATION FLAG IS PINNED BY NAME (`cancelled`).** SPEC S7(e) permits this and
   asks that it be said; the guard's own class docstring says it, and so does this line.

7. **THE EFFECT'S DEPENDENCY ARRAY IS `[openDiffTaskId, dashboard.jobId, serverToken]`,**
   not the open task id alone. S5 says "keyed on the open task id", which it is; the two
   extra entries are the other values the effect reads and are what React's
   exhaustive-deps rule requires.

8. **G6(e) WAS APPLIED AS A REPLACEMENT WITH `null`,** not a raw deletion — reasoned in the
   G6 section above.

9. **NO TYPESCRIPT MUTATION RED-PROOF WAS ATTEMPTED,** per constraint 10. The `.tsx` layer
   is covered by `tsc --noEmit` (measured PASSED, not skipped) and by the text guards.

10. **The `remedy` CLI is denied to subagents here,** so no step used it. Nothing in this
    block needed it.

11. **Assumption on the slice join.** The Slice convention says "join with exactly one
    newline" and G5 reader (a) restates it. I read a slice's bytes as its content lines
    each INCLUDING its terminator, which G4's own wording settles — it asks for byte
    equality "INCLUDING the trailing newline" and a negative control against the slice
    "minus its trailing newline". Under that reading both G5 readers pass, the record keeps
    its blank-line-separated paragraph convention and the file keeps its trailing newline.
    Under the other reading reader (b) could not pass. No other reading was applied.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the plan | done | |
| C2 the R17 gate and R-0725 | done | |
| C3 the R-0725 repair | done | scope tightened past S1(b)'s wording, deviation 2 |
| C4 the entry point | done | placement caveat in deviation 3 |
| C5 the mount | done | |
| C6 the mount guard | done | |
| C7 the handback | done | this file |
| G1 hygiene | done | STOP ABSENT twice; base SHA, branch and clean tree all confirmed |
| G2 transport | done | all three readings match; C0b is one blob |
| G3 extraction and caps | done | TOTAL 385, CONTENT 55, PROSE 330 |
| G4 the plan at C1 | done | byte equal; control False; 49 lines |
| G5 the record at C2 | done | both readers True, both controls False, counts as predicted |
| G6 the red-proofs | done | 6 of 6 RED at exit 1; (a) and (b) GREEN at base, RED now |
| G7 suites, types, lint, canary | done | seven commands, every one exit 0; tsc PASSED |
| G8 structure and artifacts | done | change set exact; packages/ and api/ both empty |

## Next

The reviewer reads `git diff 5a4d5257..HEAD` and re-runs G1 through G8 itself, in
particular the G6 (a) and (b) pair, which is the repair of `R-0725` proving itself. On
PASS, the next round takes the file sidebar over `buildDiffFileSummaries`, which
`diffViewModel.ts` already exports and nothing yet draws. The next session's first action
is Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — read `.agent/STOP` — before
rule 2.
