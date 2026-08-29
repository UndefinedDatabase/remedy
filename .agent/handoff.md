# Handback — F033 Hunk-level diff approval · ROUND 5 · T001 CLOSED

## Session

SESSION 2 of feature F033 · round 5 · rounds so far 5

## Range

Review of `7434f54632e75e9d1e86044d8edc7f96c0ef0ae6`..`HEAD` on branch
`feature/f033-hunk-approval-v2`.

## Commits

### 12f255fc chore(f033): save the round 5 block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r5.md` | +340 / -0 | C0a, the block saved with `shutil.copyfile`, never retyped |

### 7bc8e1b3 chore(f033): mirror the round 5 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +259 / -168 | C0b, byte-identical mirror of the C0a blob |

### 203806ab docs(f033): retarget the plan on T001 closure
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16 / -16 | C1, slice `PLANF033R5` applied whole-file |

### 935c3cf7 docs(f033): book the round 4 verdict, R-0739 and DECISION F033 D3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6 / -0 | C2, slice `RECORDF033R5` appended after one newline |

### d96988c8 docs(f033): repair two comments that still describe the pre-wiring world
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/diffViewModel.ts` | +7 / -6 | C3, the `buildDiffRowModels` KEYS note |
| `packages/orchestration/hunk_identity.py` | +16 / -14 | C3, the module docstring's opening paragraphs |

### d1faf70e docs(f033): record amendment A1 on the feature file
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T5_F033.md` | +23 / -0 | C4, slice `FEATUREF033A1` appended, no separator |

### 8c594ef1 docs(f033): book the landed repair for R-0739
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C5, the worker-authored `Landed: R-0739` line naming C3's real SHA |

### C6 (this commit) docs(f033): hand back the round 5 T001 closure
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | this file | C6, the handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Action | Outcome |
|--------|---------|
| `git push -u origin feature/f033-hunk-approval-v2` | run immediately after this commit, per AGENTS.md Push Discipline |
| worktree add / remove | NONE — this round ordered no mutation red-proof and none was invented |
| `gh` commands | NONE — no PR created, none touched |
| force-push / history rewrite / branch deletion / merge | NONE |

## Verification

Eight gates, every one run, every exit code real.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again before
  C6: `ls` exit 2, "No such file or directory", both times. `git status
  --porcelain` empty after every one of the seven commits. Branch
  `feature/f033-hunk-approval-v2` throughout. `git rev-parse
  feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
  unmoved. No force-push, no rewrite, no branch deletion, no `gh` command.
- **G2 TRANSPORT — PASS.** `<C0a>:.agent/authored/f033-r5.md` is 27281 bytes at
  sha256 `02e77e6f9308ba7a11a18731035bbb2e8db9c055f183d46d1a295f565fc809b6`;
  `.remedy-wt/f033-r5-block.md` is 27281 bytes at the same digest; EQUAL = True.
  `git rev-parse <C0b>:.agent/authored/f033-r5.md` and `git rev-parse
  <C0b>:.agent/last_block.md` both print `62b275daa5d600a667299168d225bce6c68c7506`
  — ONE blob id. Exit 0.
- **G3 THE RECORD APPENDS — PASS, exit 0.** (a) BASE blob 1446287 bytes as
  ordered; `base + one newline + RECORDF033R5` (8354 bytes) == the C2 blob
  (1454642 bytes, sha256 `8f33bb85…01dc2`) byte for byte; BASE is a byte PREFIX =
  True; ends in exactly one newline = True. (b) N COUNTED by the script in
  `RECORDF033R5` = 3. The last 3 blank-line units of the C2 blob equal the
  slice's three paragraphs IN ORDER = True. NEGATIVE CONTROL: the first appended
  paragraph is proved by span arithmetic to run `[1446288, 1449890)`; offset
  1448089 lies inside it (`1446288 <= 1448089 < 1449890`); the byte there, `52`,
  was flipped to `20`; reader 1 (byte concatenation) REJECTS = True and reader 2
  (paragraph-wise) REJECTS = True. (c) `C2 + one newline + the Landed line` == the
  C5 blob (1456716 bytes, sha256 `c5b68a31…40f108`) byte for byte = True; C2 is a
  byte PREFIX = True; C5 ends in exactly one newline = True. C5's diff adds 2
  lines total — 1 BLANK separator and 1 CONTENT line — and the single content line
  matches `^Landed: R-0739 — `; 0 removed. See deviation 1: the block's
  byte-formula clause and its "adds exactly one line" clause disagree by one
  blank line, and the byte formula was followed.
- **G4 THE LEDGER at C5 — PASS, exit 0.** Registered `^- R-\d+ — ` 299 -> 300,
  distinct at both (299/299 and 300/300); the ADDED id is exactly `{R-0739}`.
  `^Done: R-\d+ — ` 44 lines over 42 distinct ids at BASE and 44 over 42 at C5 —
  UNMOVED. `^Landed: R-` 11 -> 12. `^Gate: F\d+ R\d+ — ` 121 -> 122. Open set
  257 -> 258. `^Gate: F033 R4 — ` reads 0 at BASE and exactly 1 at C5.
- **G5 THE STALENESS REPAIR at C3 — PASS, exit 0.** Over the RAW text of both
  files, BASE via `git show <BASE>:<path>` against C3. Must VANISH, each printed
  as BASE -> C3: in `packages/orchestration/hunk_identity.py` `currently names
  hunks` 1 -> 0, `The parser is not wired to` 1 -> 0, `values are PROVISIONAL`
  1 -> 0, `will share this same function` 1 -> 0; in
  `apps/ui/src/api/diffViewModel.ts` `Those ids are PROVISIONAL` 1 -> 0 and
  `<fileIndex>:<hunkIndex>` 1 -> 0. All six were confirmed to sit on a SINGLE line
  at BASE, so none of them is a needle that could never have matched. Must
  SURVIVE at C3: `Nothing here depends on the id's SHAPE` = 1 in the client and
  `DELIBERATE ABSENCE` = 1 in `hunk_identity.py`. COMMENT-ONLY, determined by
  CANONICALISATION rather than by eyeballing the diff — Python: both revisions
  parsed with `ast`, every docstring blanked, `ast.dump` compared; comments never
  reach an AST at all, so the equal dump says no executable or structural element
  moved, and a control that changes `HUNK_ID_LENGTH = 16` to `17` is REJECTED.
  TypeScript: both revisions passed through the repository's OWN scoper,
  `tests/ui_contracts/test_diff_view_model.strip_ts_comments` — the same function
  the shipped contract guards read the module through — giving 13233 of 42483
  characters at BASE and 13233 of 42526 at C3, so the scoper is not vacuous, and
  the two stripped sources are EQUAL; a control that changes
  `DIFF_VIRTUAL_OVERSCAN_ROWS = 8` to `9` is REJECTED. Per-file counts for C3
  alone (`git diff --numstat C3^ C3`): `apps/ui/src/api/diffViewModel.ts` +7/-6,
  `packages/orchestration/hunk_identity.py` +16/-14. `git diff <BASE> <C3>` over
  the whole range additionally carries the four `.agent/**` state paths of C0a,
  C0b, C1 and C2, which are markdown state files rather than production code; the
  comment-only claim is about the two production files and is proved above.
- **G6 THE SUITES — PASS.** Serially, one pytest process at a time, each a REAL
  exit code from `subprocess.run` rather than a piped tail:
  `tests/orchestration/test_hunk_identity.py` 10 passed, exit 0;
  `tests/orchestration/test_diff_parser.py` 50 passed, exit 0;
  `tests/ui_contracts/` 664 passed and 4 skipped, exit 0; `tests/docs/` 295
  passed, exit 0; the canary `tests/cli/test_golden_path.py` 42 passed, exit 0.
  Then from `apps/ui` through Python's `subprocess.run`, never `npm run`:
  `npx tsc --noEmit` exit 0 with no output, and
  `npx vitest run --reporter=basic src/api/diffViewModel.test.ts` 1 test file
  passed, 95 tests passed, exit 0. NO MUTATION RED-PROOF WAS RUN, and none was
  invented: C3 changes comment text only, no mutated branch is reachable by any
  test, and a colour ordered here could only have been green. The block says so
  explicitly and this handback says so rather than manufacturing a colour.
- **G7 THE FEATURE-FILE APPEND at C4 — PASS, exit 0.** BASE blob of
  `docs/roadmap/features/T5_F033.md` = 5057 bytes as ordered. The slice OPENS
  with a blank line, so no separator was added: `base + FEATUREF033A1` (1301
  bytes) == the C4 blob (6358 bytes, sha256 `59f58361…e806e9`) byte for byte.
  BASE is a byte PREFIX = True; ends in exactly one newline = True. The lines the
  commit ADDS are exactly the slice's 23 lines IN ORDER (23 added, 23 expected,
  0 removed). `^## Amendments$` at C4 = 1.
- **G8 STRUCTURE — PASS, exit 0.** `git rev-list --reverse BASE..C5` walks 7
  commits, each with exactly ONE parent and each under 500 INSERTIONS — the `+`
  column of `git diff --numstat`, never insertions plus deletions:
  `12f255fc` 340, `7bc8e1b3` 259, `203806ab` 16, `935c3cf7` 6, `d96988c8` 23,
  `d1faf70e` 23, `8c594ef1` 2. Path set against the change set in BOTH
  directions: paths touched but not in the change set = NONE; change-set paths
  not touched in the range = `.agent/handoff.md` alone, which is C6 and is the
  expected absence. Delimiter residue at C5, counting the block's SLICE-open and
  END-close transport tags:
  `.agent/plan.md` 0/0, `docs/roadmap/features/T5_F033.md` 0/0,
  `packages/orchestration/hunk_identity.py` 0/0,
  `apps/ui/src/api/diffViewModel.ts` 0/0, against the non-zero CONTROL
  `.agent/authored/f033-r5.md` at 5 and 6. `git ls-files .remedy-wt` = 0.
  C6's own numbers are not measured here, as the block directs.

## Authored-text proofs

Three reviewer-authored slices applied, all three EXTRACTED FROM THE COMMITTED
C0a BLOB by `git show <C0a>:.agent/authored/f033-r5.md` and never retyped. The
extractor anchors to the NAMED delimiter at line start, asserts the tag is not
duplicated, and takes the bytes strictly between the delimiter lines.

| Slice | Bytes | sha256 | Applied to | Result |
|-------|-------|--------|------------|--------|
| `PLANF033R5` | 2102 | `b74000b4…d5b277` | `.agent/plan.md` (whole file) | disk == slice, byte-EQUAL; 40 lines, under the 50-line cap |
| `RECORDF033R5` | 8354 | `4ff3fd31…57c292` | `.agent/live_review.md` (append) | base + newline + slice == C2 blob, byte-EQUAL |
| `FEATUREF033A1` | 1301 | `c03ffce3…6d6b11` | `docs/roadmap/features/T5_F033.md` (append) | base + slice == C4 blob, byte-EQUAL |

The C0a save itself: `.remedy-wt/f033-r5-block.md` and
`<C0a>:.agent/authored/f033-r5.md` are both 27281 bytes at sha256
`02e77e6f9308ba7a11a18731035bbb2e8db9c055f183d46d1a295f565fc809b6`. This
workflow has no paste relay, so that chain proves the worker's own copies agree
and claims nothing about the bytes the reviewer emitted.

The `Landed: R-0739` line at C5 is NOT a slice and was not extracted from the
block: `docs/agents/planner_reviewer_prompt.md` §4 item 4 reserves `Done:` for
the reviewer and gives the worker the `Landed:` line, and it names C3's real SHA
`d96988c8bba7051b773d55db33452334078355db`, a value that did not exist while the
block was being written.

## The repaired comment regions, quoted in full

So the reviewer can read them without the diff.

### `packages/orchestration/hunk_identity.py`, docstring lines 3–18 at C3

    WHY this module exists: approving a hunk is a promise about a piece of CONTENT, and a
    POSITIONAL name cannot keep that promise. An id spelled ``"<file_index>:<hunk_index>"`` —
    both zero-based — is stable only within a single parse of a single diff text: insert one
    hunk near the top of a file and every hunk after it is renumbered, so an operator who
    approved hunk ``0:3`` in one round would be approving a different piece of content in the
    next. An id computed from the hunk's own old-side text does not move when something else
    in the file moves, which is what lets an approval survive an edit above it.

    ``packages/orchestration/diff_parser.py`` CALLS this module for every hunk ``id`` it
    emits, and its own docstring says those ids "are CONTENT-DERIVED and carry no position at
    all"; ``DIFF_VIEW_VERSION`` is 2, the bump that carried the change out to consumers. The
    diff-repair side holds no hunk identity to share with it: ``RepairHunk`` in
    ``packages/orchestration/diff_repair.py`` selects spans of CURRENT source for a repair
    prompt and never names a hunk, so this module has ONE caller by design. A reader who
    expected a second one should read amendment A1 of
    ``docs/roadmap/features/T5_F033.md``.

Line 1, the summary, the DELIBERATE ABSENCE paragraph, the totality paragraph
and every purity sentence are UNTOUCHED, as are both pointers — to
`diff_parser.py` and to `diff_repair.py` — inside the absence paragraph.

### `apps/ui/src/api/diffViewModel.ts`, the `buildDiffRowModels` KEYS note, lines 380–389 at C3

     *  KEYS. Every row carries a `key` that is unique across the whole array and
     *  STABLE under collapse — collapsing a hunk removes line rows but renumbers
     *  nothing, so React reuses the rows that did not change. The hunk-derived keys
     *  are built from the server's own hunk `id`, which `diff_parser.py` derives
     *  from the hunk's CONTENT — its path and its normalised old side — so a row
     *  survives a re-parse of a changed diff. Where a payload carries no usable id,
     *  `readDiffHunk` above supplies one of the client's own bearing
     *  `UNIDENTIFIED_HUNK_ID_PREFIX`, which is what keeps such an id out of the
     *  server's id space. Nothing here depends on the id's SHAPE, only on the
     *  server assigning distinct ones.

Nothing else in the file changed: the constant, the fallback expression and
`readDiffHunk`'s contract note — round 4's work — are byte-untouched. The
CONSTRAINT was respected: no number was written into any comment this round
touched, and `tests/ui_contracts/test_diff_view_model.py`'s raw-text count of
the collapse-threshold literal still reads exactly 1 (that suite is green at
664 passed, 4 skipped).

## T002 seam inventory

A READING taken at this round's HEAD, not a design. Nothing is proposed here.

**The write door's dispatch, `packages/orchestration/ui_server.py`.** The two
ids it dispatches today are named constants, not inlined strings:
`packages/orchestration/ui_server.py:3270` `JOB_STOP_COMMAND_ID = "job.stop"`
and `:3271` `DECISION_RESOLVE_COMMAND_ID = "decision.resolve"`, under a comment
at `:3268` that calls them "The two ids this door dispatches". The two dispatch
clauses that consume them are `:3666` (`if payload["command"] ==
JOB_STOP_COMMAND_ID:`) and `:3689` (`… == DECISION_RESOLVE_COMMAND_ID:`). The
line that answers an EXPOSED-BUT-UNDISPATCHED command is
`packages/orchestration/ui_server.py:3722`,
`self._send_json(*_safe_error(501, COMMAND_NOT_DISPATCHED_MESSAGE))`, reached at
`:3717` under the comment "An id `_command_is_ui_exposed` admitted that no
clause above dispatches"; the message itself is
`packages/orchestration/ui_server.py:3262`,
`COMMAND_NOT_DISPATCHED_MESSAGE = "command is exposed but not dispatched"`. So
exposure and dispatch are two separate gates, and adding an id to the exposed
set alone yields a 501 rather than a silent pass.

**How a command becomes UI-exposed.** `_command_is_ui_exposed` at
`packages/orchestration/ui_server.py:3916` is the whole test; its body at `:3924`
is the function-scoped import `from apps.cli.command_catalog import
UI_EXPOSED_COMMANDS` and at `:3925` `return command_id in UI_EXPOSED_COMMANDS`.
The set is declared at `apps/cli/command_catalog.py:4810` as
`UI_EXPOSED_COMMANDS: frozenset[str] = frozenset({"job.stop",
"decision.resolve"})`, under a comment at `:4806` calling it "The whole surface
of the UI write door" and recording that plan approval arrives as
`decision.resolve` with an `fp:`-prefixed id rather than as a command of its own
(DECISION F009 D4). It is listed in that module's own Public API docstring at
`apps/cli/command_catalog.py:17`. `tests/ui_server/test_command_channel.py:1557`
`TestUiExposedCommands` pins the set at exactly those two ids.

**`TestCommandDoorImportGuard`, `tests/ui_server/test_command_channel.py:1395`.**
It pins three things about the write door, by AST over the shipped
`ui_server.py` source, scoped to the ten methods listed at `:1415` in
`DOOR_METHODS` (`_handle_command_submission`, `_dispatch_job_stop`,
`_dispatch_decision_resolve`, `_publish_command_result`,
`_emit_command_accepted_event`, `_audit_attempt`, `_command_is_ui_exposed`,
`_replayed_command_result`, `_rate_limit_admits_command`,
`_read_command_payload`). THE EQUALITY GUARD T002 WILL HAVE TO WIDEN is
`test_the_door_imports_exactly_the_allowed_set` at `:1514`, whose docstring
states the rule in its own words — "Equality, not containment: a NEW import is a
finding until it is ruled" — and whose body asserts `found ==
set(self.ALLOWED_IMPORTS)`, reporting `unruled` and `vanished` on failure.
`ALLOWED_IMPORTS` at `:1431` is a frozenset of 15 `(module, name)` pairs, each
annotated with the DECISION that put it there, under a comment saying "Adding an
entry means widening the P3 contract, so it belongs in the same commit as the
decision that widens it". Beside it, `FORBIDDEN_MODULES` at `:1455` names nine
modules the door may never import from — and
`packages.orchestration.source_apply` is the FIRST entry in that set — while
`STORAGE_ALLOWED_NAMES` at `:1472` limits `packages.orchestration.storage` to
`save_job` alone. `test_every_named_method_exists` at `:1503` stops the tuple
emptying itself under a rename, and
`test_the_guard_fails_on_a_handler_that_touches_storage_directly` at `:1533`
runs the same extractor over a synthetic violating handler so the guard has been
watched to fail.

**`packages/orchestration/source_apply.py`'s public entry point.** It is
`apply_structured_patch` at `packages/orchestration/source_apply.py:182`, with
the signature `apply_structured_patch(patch: StructuredPatch, repo_path: Path,
*, data_dir: str | None = None, job_id: UUID | None = None, job: Any,
intent_id: str | None = None) -> ApplyResult`. IT TAKES NO SUBSET OF ANYTHING.
`StructuredPatch` at `packages/orchestration/structured_patch.py:50` is
`(intent_kind, markdown_proposal, file_ops, unified_diffs, target_paths, risk,
applicability, requires_approval)`, and the applier consumes `file_ops` and
`unified_diffs` WHOLE — `_apply_file_op` at `:370`, `_apply_unified_diff` at
`:412` and `_apply_hunks` at `:440` walk every op and every hunk of what they
are handed, with no id, no selection argument and no filter. The nearest thing
to a selector on this module is `intent_id`, which is an APPROVAL reference into
`approval_queue.get_patch_intent` (consumed at `:215`–`:231`), not a choice of
which hunks to land. The other public name is `revert_apply` at `:531`, keyed by
`apply_id`. So an all-or-nothing approved-subset apply is a new seam on this
module rather than a parameter on something that already exists — which is what
`.agent/plan.md`'s risk line already says about `repo_applicator.py`.

**Does anything today read an approved/rejected hunk set?** NONE FOUND. The
search run, case-insensitive over `packages/`, `apps/` and `tests/` restricted
to `*.py`, `*.ts` and `*.tsx`:

    grep -rniE "approve_hunks|approved_hunks|rejected_hunks|hunk_decision|hunk_approval|approved_hunk_ids" \
      --include=*.py --include=*.ts --include=*.tsx packages/ apps/ tests/

It matches ZERO files. The only consumer of a hunk id anywhere is the viewer's
row keying and collapse set in `apps/ui/src/api/diffViewModel.ts`, which reads
ids and never a decision over them. `packages/orchestration/hunk_identity.py`
has exactly one importer, `packages/orchestration/diff_parser.py`, which is the
measurement DECISION F033 D3 rests on.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `12f255fc`, `shutil.copyfile`, digest verified before and after |
| C0b mirror it | done | `7bc8e1b3`, one blob id shared with the C0a path |
| C1 `.agent/plan.md` | done | `203806ab`, `PLANF033R5` byte-equal |
| C2 the verdict, R-0739 and DECISION F033 D3 | done | `935c3cf7`, `RECORDF033R5` appended |
| C3 the staleness repair, both files together | done | `d96988c8`, comment text only in both |
| C4 the feature-file amendment | done | `d1faf70e`, `FEATUREF033A1` appended |
| C5 the `Landed: R-0739` line | done | `8c594ef1`, worker-authored, names C3's real SHA |
| C6 the handback | done | this commit |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS, exit 0 |
| G3 THE RECORD APPENDS | done | PASS, exit 0; see deviation 1 on the (c) line count |
| G4 THE LEDGER at C5 | done | PASS, exit 0 |
| G5 THE STALENESS REPAIR at C3 | done | PASS, exit 0 |
| G6 THE SUITES | done | PASS, every exit code 0 |
| G7 THE FEATURE-FILE APPEND at C4 | done | PASS, exit 0 |
| G8 STRUCTURE | done | PASS, exit 0 |
| the T002 seam inventory | done | the section above |
| a mutation red-proof | skipped | not ordered; the block rules one impossible here and says to say so rather than invent one |

## Deviations & assumptions

1. **G3 (c)'s two clauses disagree by one blank line, and the byte formula was
   followed.** The clause "the C2 blob plus one newline plus LANDEDF033R5 equals
   the C5 blob byte for byte" and the clause "that commit's diff must ADD exactly
   one line" cannot both hold literally: the C2 blob already ends in a newline, so
   "plus one newline" necessarily introduces a BLANK separator line, and git then
   reports 2 insertions. I applied the BYTE FORMULA, which is the primary and
   unambiguous clause, and it is also the repository's own established form —
   all ELEVEN pre-existing `Landed:` lines in `.agent/live_review.md` are
   blank-separated, measured, and the last such commit, `8bb2ab6a`, likewise shows
   `2 0 .agent/live_review.md`. My gate therefore reports both readings: 2 added
   lines TOTAL, of which 1 is blank and exactly 1 is content matching
   `^Landed: R-0739 — `. Nothing on disk differs from what the block intended; only
   the count in one clause does. Declared rather than routed around.
2. **The block's G5 clause "`git diff <BASE> <C3>` must show ZERO changed lines
   that are not inside a comment or docstring" is measured over the two
   PRODUCTION files.** The BASE..C3 range necessarily also contains C0a, C0b, C1
   and C2, which rewrite four `.agent/**` markdown state files; those are not
   code and have no comments, so the clause is unmeetable if read over the whole
   range's path set. I proved the comment-only property where it means something
   — `apps/ui/src/api/diffViewModel.ts` and
   `packages/orchestration/hunk_identity.py`, by canonicalisation with working
   controls, as recorded under G5 — and report the range's other paths openly
   rather than quietly excluding them.
3. **The G5 comment-only determination is a canonicalisation, not a line
   inspection.** The block asked me to "report how you determined that". I did not
   read the diff and judge each line; I removed comments and docstrings from both
   revisions of each file by a mechanical route and compared the remainders, with
   a control mutation in each language proving the route is not blind. That is a
   stronger reading than the block's wording requires and is stated here in case
   the reviewer intended the weaker one.
4. **No unordered work.** No path outside the declared change set was modified.
   `packages/orchestration/diff_parser.py`, `packages/orchestration/diff_repair.py`,
   `apps/ui/src/api/diffViewModel.test.ts` and `docs/roadmap/STATUS.md` are
   untouched, as the block requires. Scratch scripts live under the gitignored
   `.remedy-wt/` and `git ls-files .remedy-wt` reads 0.
5. **No verdict on this round's own work appears anywhere in this file**, and
   none was written. The reviewer gates round 5 and re-runs every gate itself.

## Next

The reviewer gates round 5 at this HEAD. If it passes, T001 is closed on its
three real deliverables with DECISION F033 D3 recorded as amendment A1, and the
next block opens T002 on the seam inventoried above — starting, per
`.agent/plan.md`, with the `approve_hunks` validation core as a pure function
with tests, before any write-door or applicator work.
