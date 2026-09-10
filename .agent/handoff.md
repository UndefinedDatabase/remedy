# Handback — F275 round 29

## Session

SESSION 14 of feature F275 · round 29 · rounds so far 29

## Range

Review of `99e677f0`..`HEAD`.

## Commits

### 4e9ed17d F275 R29 C0a: save the round 29 block verbatim as the authored original.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r29.md` | +317 / -0 | the round 29 block saved byte-verbatim as the authored original, by `shutil.copyfile` |

### fd07d29a F275 R29 C0b: mirror the committed round 29 block into the last-block slot.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +259 / -258 | the COMMITTED C0a blob mirrored in, written from `git cat-file blob` and never retyped |

### 72b9994d F275 R29 C1: retarget the plan at round 29, R-0872 finished and the ratchet deleted.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -20 | PLAN29, applied byte-for-byte from the committed C0a blob |

### b881f25b F275 R29 C2: book the round 28 PASS verdict and resolve R-0872 in the record.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | LEDGER29's two paragraphs appended — the round 28 `Gate:` record and the `Done: R-0872` resolution |

### 60c96b5c F275 R29 C3: rename every flat pre-Step-38 command example in the architecture page to its shipped group-first successor, and stop spelling F263 plan as runnable, discharging the second half of R-0872.
| Path | +/- | Reason |
|---|---|---|
| `docs/system/architecture.md` | +38 / -38 | pair V1 applied FIRST, then the 22-mapping rename table over 37 occurrences |
| `docs/system/vocabulary.md` | +1 / -1 | pair V2 — DECISION F259 D1 keeps the name `absorb`, loses the runnable spelling |

### 047972e5 F275 R29 C4: delete the known-dead advertisement allowlist, its ceiling, its ratchet test and the subtraction it fed, now that R-0872 backlog reads zero.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_advertised_commands.py` | +2 / -76 | items (a)-(d): the allowlist and its comment block, `_ALLOWLIST_CEILING` and its comment, `test_the_known_dead_doc_advertisement_list_only_ever_shrinks`, and the `remainder` subtraction — the operator-facing assertion now reads directly against `unresolved` |

### <this commit> F275 R29 C5: the round 29 handback.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | a handback cannot table the commit that writes it (R-0149 pattern) |

Per-commit insertions, against the DECISION F104 D1 cap of 500: 317, 259, 17, 4,
39, 2. C3 and C4 together are 41 insertions against 115 deletions over three
files, exactly the figure the block predicted.

## External actions

- `git worktree add .remedy-wt/r29-redproof 047972e5 --detach` — exit 0, created at C4.
- `git worktree remove .remedy-wt/r29-redproof --force` — exit 0.
- `git worktree prune` — exit 0; `git worktree list` back to ONE entry.
- `git push -u origin feature/f275-one-world-completion-part-three` — see below.
- No PR created, edited or merged. No `gh` command run.

## Verification

One line per gate, real exit codes, real numbers.

- **G1 TRANSPORT (at C0b) — REAL_EXIT=0.** ONE comparison over three readings:
  the scratch original `.remedy-wt/f275-r29-block.md`, the committed
  `.agent/authored/f275-r29.md` and the committed `.agent/last_block.md` are all
  26767 bytes at
  `11b8bb509713cd02bd9fa7d604b909805ad5bf0bd7a9d7ec769fe64d18652b3e`, and the two
  committed BLOBS re-read through `git show` give the same digest — EQUAL.
- **G2 THE PLAN (at C1) — REAL_EXIT=0.** `written == slice: True`, 2268 bytes,
  42 lines against the AGENTS.md cap of 50, `^## Goal$` == 1, `^## Next Steps$` == 1.
- **G3 THE RECORD (at C2) — REAL_EXIT=0.** pre 775926, slice 7723, post 783650;
  `post == pre + ONE newline + slice` True; the joining byte read back at offset
  775926 is `b'\n'`. INDEPENDENT structural reader: N counted BY THE SCRIPT from
  the slice = 2, and the last 2 blank-line units of the file match the slice's 2
  paragraphs IN ORDER (unit 1 True, unit 2 True). NEGATIVE CONTROL: one byte
  flipped at offset 776127, inside the FIRST appended paragraph (which spans
  775927..780118), `b'N'` -> `b'X'` — arithmetic reader False, structural reader
  False (unit 1 False), while both accept the truth. `^Gate: F275 R28 ` == 1,
  `^Done: R-0872 — ` == 1. OPEN SET BY DISTINCT ID: 102 distinct registrations
  minus 14 distinct resolutions = 88, down from 89 at the base, correct for a
  round that registers none and resolves one.
- **G4 THE RENAME (at C3) — REAL_EXIT=0.** Containment test: `TO contains FROM`
  False for V1 and False for V2. V1 FROM 1 -> 0, TO 0 -> 1; V2 FROM 1 -> 0, TO
  0 -> 1. All 22 mappings, applied in DESCENDING FROM length with the guard
  `re.escape(FROM) + r"(?![a-z0-9-])"`, measured before and after —
  attach-project-repo 1->0, list-patch-intents 1->0, apply-patch-intent 2->0,
  attach-project-job 1->0, discover-commands 2->0, show-permissions 1->0,
  project-context 3->0, run-tests-local 1->0, create-project 1->0,
  list-projects 1->0, trust-report 1->0, constitution 2->0, show-project 2->0,
  run-contract 2->0, token-policy 2->0, attach-repo 1->0, brain-node 7->0,
  brain-view 1->0, create-job 1->0, timeline 1->0, cockpit 1->0, workers 2->0.
  EVERY before-count equals the block's bracketed number and every after-count
  is ZERO. TOTAL REPLACED 37. Raw sweep over the whole file for `remedy ` plus
  any of the 22 flat spellings: RAW TOTAL 0. `architecture.md` is 3076 lines,
  148708 bytes.
- **G5 THE SWEEP (at C3, allowlist STILL PRESENT) — REAL_EXIT=0** for the reading,
  **REAL_EXIT=1** for the suite, which is the point. Through the worker's own
  import of the guard module as it stands at C3: operator-facing sweep 384 seen,
  ZERO unresolved; `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` == 22 and entries that no
  longer occur == 22, so the allowlist is ENTIRELY STALE. Production sweep 542
  seen, ZERO unresolved. The guard suite is therefore RED between C3 and C4 at
  **1 failed / 5 passed**, and the failure is the ratchet demanding its own
  deletion:
  `FAILED tests/cli/test_advertised_commands.py::test_the_known_dead_doc_advertisement_list_only_ever_shrinks`
  — `AssertionError: the known-dead advertisement list excuses advertisements
  that are no longer there — delete the entry in the commit that repairs the
  site:` followed by all 22 keys, 21 under `docs/system/architecture.md` and
  `docs/system/vocabulary.md: remedy absorb`. Reported as evidence, not treated
  as a failure; C4 is the deletion it demands.
- **G6 THE RATCHET IS GONE (at C4) — REAL_EXIT=0.** `KNOWN_DEAD_DOC_ADVERTISEMENTS`
  0, `_ALLOWLIST_CEILING` 0, `only_ever_shrinks` 0 in the guard module (now 233
  lines). `ruff check tests/cli/test_advertised_commands.py` — REAL_EXIT=0, real
  message `All checks passed!`; this is the check constraint 7 names as the only
  one that can see an incomplete removal, and it saw none.
  `python3 -B -m pytest tests/cli/test_advertised_commands.py -q` — REAL_EXIT=0,
  **5 passed**, one fewer than round 28's 6. RED PROOF, inside the disposable
  worktree `.remedy-wt/r29-redproof` at `047972e5` per guardrail G5, with
  `__pycache__` purged and `python3 -B`: unmutated CONTROL first — REAL_EXIT=0,
  5 passed; then `remedy absorb` restored into `docs/system/vocabulary.md`
  (FROM count 1, one replacement) — REAL_EXIT=1, **1 failed / 4 passed**,
  `FAILED ...::test_every_operator_facing_advertised_command_exists_in_the_catalog`,
  `AssertionError: ... docs/system/vocabulary.md:264: remedy absorb`. Reverted by
  exact path with `git checkout -- docs/system/vocabulary.md`: disk and the
  `047972e5:docs/system/vocabulary.md` blob are both 27306 bytes at
  `834972f6ee872f8e59742430f134d939fe4589efdff114666df78811a8441e05` —
  BYTE-IDENTICAL True, worktree porcelain EMPTY. Worktree removed and pruned.
  The guard did not lose its teeth when it lost its allowlist.
- **G7 NOTHING ELSE MOVED (at C4, before C5) — REAL_EXIT=0.**
  - `python3 -B -m pytest tests/docs/ tests/cli/ -q -p no:randomly` run SERIALLY
    (never `-n auto`) — REAL_EXIT=0, **1648 passed, 0 failed** in 247.41s. That is
    one fewer than round 28's 1649, and the difference is EXACTLY the deleted
    ratchet test, proved rather than asserted: the range `99e677f0..047972e5`
    touches exactly ONE path under `tests/` — `tests/cli/test_advertised_commands.py`
    — and a `^def (test_\w+)` reading of that file's base blob against its C4 blob
    gives 6 -> 5 with REMOVED
    `['test_the_known_dead_doc_advertisement_list_only_ever_shrinks']` and ADDED
    `[]`. The canary lives inside `tests/cli/` and ran.
  - Through the shipped reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)`
    222, `len(GROUPS)` 44, dangling `related=` 0 over 286 references — resolved on
    the DOTTED `group.subcommand` id, not on a spaced pair, per round 28's declared
    reader error. Unchanged rather than merely valued: the range contains NO
    `apps/` or `packages/` path at all.
  - All 22 TO pairs of the rename table resolve in the shipped `CATALOG`: 22 of
    22, none missing.
  - `.agent/STOP` absent (read from disk, before the first commit and again before
    C4), `git status --porcelain` EMPTY, `git worktree list` exactly ONE entry,
    branch `feature/f275-one-world-completion-part-three`.
  - `git diff --name-only 99e677f0..047972e5` is an EXACT SET MATCH against the
    change set minus `.agent/handoff.md`, over seven paths —
    `.agent/authored/f275-r29.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`, `docs/system/architecture.md`, `docs/system/vocabulary.md`,
    `tests/cli/test_advertised_commands.py`. MISSING: none. EXTRA: none.
    `.agent/prose_slips.md` is correctly absent.
  - Per-commit insertions before the handback commit: 317, 259, 17, 4, 39, 2 —
    every one far under the DECISION F104 D1 cap of 500.

## Authored-text proofs

Every reviewer-authored text was extracted from the COMMITTED C0a blob via
`git cat-file blob HEAD:.agent/authored/f275-r29.md`, never from a retype, and no
marker line reached a target file (constraint 2).

- `.agent/authored/f275-r29.md` vs the scratch original: byte-equal, 26767 bytes,
  `11b8bb50…52b3e` — see G1.
- `.agent/last_block.md` vs the committed C0a blob: byte-equal, same digest.
- PLAN29 -> `.agent/plan.md`: `written == slice` True, 2268 bytes.
- LEDGER29 -> `.agent/live_review.md`: appended, `post == pre + NL + slice` True,
  7723 slice bytes, both readers accepting the truth and rejecting the control.
- V1 -> `docs/system/architecture.md`: FROM 1 -> 0, TO 0 -> 1.
- V2 -> `docs/system/vocabulary.md`: FROM 1 -> 0, TO 0 -> 1.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed
exactly: no extra commit, no dropped commit, no reordering. Every slice was
applied byte for byte and nothing was repaired. What follows is declared doubt,
not deviation, except where marked.

1. **`remedy create-job` reads 2 before V1 and 1 after it — constraint 5 is
   load-bearing and was measured to be so.** Before V1 the guarded raw count of
   `remedy create-job` in `architecture.md` is **2**, not the block's bracketed
   **1**; after V1 it is 1, which is the number the block states and the number
   the table replaced. The second occurrence is the one inside the sentence V1
   rewrites. Had the table run first it would have turned that sentence into
   "restructure the Remedy CLI from flat commands (`remedy job create`, …) to a
   group-first layout (`remedy job create`, …)" — a sentence claiming the
   restructure changed nothing. This is not a deviation from the block; it is the
   block's own bracketed counts being post-V1 readings, and I report the pre-V1
   reading so the ordering's necessity is on the record rather than assumed. All
   other 21 mappings read identically before and after V1.
2. **DOUBT, applied as written and NOT repaired: the mechanical rename made two
   "backward compatibility" sentences read oddly.** `architecture.md` line 1901
   now reads `remedy project show <project_id> [--json]  — show project summary
   (backward-compat)` and line 1909 reads "`remedy project` is the primary
   user-facing alias.  `remedy project show` remains for backward compatibility;
   both call the same implementation." The prose was written when
   `remedy show-project` was the legacy spelling of `remedy project`; renaming the
   legacy spelling to its live successor leaves a sentence calling a live,
   catalogued command a backward-compatibility alias. Both `(project, show)` and
   the `project` group are in the shipped `CATALOG`, so nothing here is a dead
   advertisement and G4/G5/G7 are unaffected — but the *claim* is now questionable
   editorial history rather than a fact. Constraint 1 forbids me repairing a
   reviewer slice, so it stands and is declared. It is a candidate for R-0873's
   page-by-page ruling.
3. **DOUBT, applied as written and NOT repaired: one command block lost its column
   alignment.** In the block at `architecture.md` lines 1896-1901 the em-dash
   comment column was hand-aligned. Twenty-one of the 22 mappings preserve their
   FROM's length exactly, but `remedy list-projects` (20 chars) becomes
   `remedy project list` (19), so that one line's `—` now sits one column left of
   its neighbours. Cosmetic, inside a fenced block, and repairing it would mean
   editing a byte the slice did not order.
4. **DOUBT, applied as written and NOT repaired: `UnresolvedAdvertisement.key` is
   now a readerless property.** C4's four ordered deletions removed both of its
   call sites — the `remainder` filter and the ratchet's `live_keys` comparison —
   and its docstring still opens "The allowlist key: the path and the invocation,
   and NEVER the line number", describing an allowlist that no longer exists. The
   block states in as many words that "Nothing else in the module changes", and
   lists the four deletions exhaustively, so I left it. `ruff check` does not flag
   an unused NamedTuple property, so no gate sees it. This is the R-0855
   "deletion sweeps the neighbourhood" pattern arriving one level down from the
   deletion, and I raise it here rather than acting on it.
5. **`-p no:randomly` was passed to the G7 suite run.** The block orders the suite
   run SERIALLY and does not name a seed flag; this repo's suite is
   order-randomised by default, and pinning collection order is what makes "1648
   passed, one fewer than 1649, and the difference is exactly this test" a
   comparable reading rather than a coincidence. It adds no selection, deselection
   or skip: the collected count is unchanged. Declared because it is a command the
   block did not spell.
6. **Scratch scripts.** Four helper scripts were written under the gitignored
   `.remedy-wt/` (`r29_g3.py`, `r29_c3.py`, `r29_g5.py`, `r29_g7.py`) so that the
   forensics, the transformation and the readings are re-runnable rather than
   typed once into a shell. They are outside the change set by construction —
   `git status --porcelain` is EMPTY — and nothing under version control depends
   on them.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `4e9ed17d`, block saved byte-verbatim |
| C0b | done | `fd07d29a`, mirrored from the COMMITTED C0a blob |
| C1 | done | `72b9994d`, PLAN29 |
| C2 | done | `b881f25b`, LEDGER29 |
| C3 | done | `60c96b5c`, V1 then the table then V2 |
| C4 | done | `047972e5`, all four ratchet deletions |
| C5 | done | this commit |
| V1 | done | FROM 1->0, TO 0->1; applied BEFORE the table per constraint 5 |
| V2 | done | FROM 1->0, TO 0->1; DECISION F259 D1's chosen name untouched |
| rename table | done | 22 mappings, 37 occurrences, every after-count ZERO, every before-count equal to the block's |
| G1 | done | exit 0 — three readings, one digest |
| G2 | done | exit 0 — `written == slice`, 42 lines |
| G3 | done | exit 0 — arithmetic, structural and negative control; open set 88 |
| G4 | done | exit 0 — 37 replaced, raw sweep 0 |
| G5 | done | exit 1 on the suite BY DESIGN — 384/0, allowlist 22 of 22 stale, production 542/0 |
| G6 | done | exit 0 — three names at zero, ruff clean, 5 passed, red proof 1 failed / 4 passed, revert byte-identical |
| G7 | done | exit 0 — 1648 passed, catalog 222/44/0, 22 of 22 TO pairs resolve, exact set match |
| R-0872 | done | RESOLVED — both halves of the fix clause discharged; booked in `.agent/live_review.md` at C2 |

## Open findings

**88** by distinct id at `047972e5` — 102 distinct registrations against 14
distinct resolutions, computed mechanically from `.agent/live_review.md`. Down
from 89 at the base `99e677f0`: this round registers none and resolves one
(R-0872). Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
than this feature's, per DECISION F272 D12.

**Nothing on disk now counts the R-0873 backlog.** The ratchet was the only
mechanism doing so, and deleting it was the correct move for a list at zero, but
the consequence is stated here and in the plan's Risks section: the doc residue
R-0873 names is carried by that finding alone.

## Next

The planner and reviewer re-runs G1 to G7 independently against the committed
range `99e677f0`..`HEAD` and issues the round 29 verdict. Before authoring round
30 it re-reads `.agent/STOP` from disk (Phase 1 rule 1, then rule 2). Round 30's
subject is the first entry of `.agent/plan.md`'s Next Steps: R-0873's declined
ruling — the capability sweep's eighteen pages read one by one and each ruled
DELETE, DATE or LEAVE, recorded as a dated DECISION.
