# Handoff — F258 Self-use track v2

## Session

SESSION 2 of feature F258 · round 5 · rounds so far 5.

## State

Branch `feature/f258-self-use-v2`, cut from `main` at
`18ae71293cde9b1157aca35d3d02c3a8f4265813` (the merge commit of pull request
225, F040's closure). Last commit on this branch before the handback write is
`11c006b851c1d1eaee01935bcc6a1f87a83cc517` (`feat(f258): add self_use_runner
(T002 consumed means executed)`). This round books round 4's own PASS verdict
(`Gate: F258 R4`) into `.agent/live_review.md` per amend0827 rule 1, then
builds T002: `packages/orchestration/self_use_runner.py`, which composes
`packages.orchestration.self_use_job.plan_next_self_use_item` with
`packages.orchestration.pingpong_job.run_job` under a small
`packages.core.models.JobBudgets`, stopping at whatever status `run_job`
returns (`JOB_COMPLETED` or `JOB_BLOCKED`) — never calling
`packages.orchestration.job_promote.promote_job` anywhere. Ships with
`tests/orchestration/test_self_use_runner.py` (7 tests). Two docs are wired
the same way T001's generator was wired: `docs/roadmap/STATUS_closure_protocol.md`
precondition 6 now describes the queue item as RUN through
`run_next_self_use_item`, never promoted, before `consumed_by` is set;
`docs/system/self-use-track-v1.md`'s banner, "Why it exists", module table
and consumption section now name the runner instead of only "taken to the
approval gate". T002 is now feature-complete against the feature file's own
text. Open findings count in `.agent/live_review.md`: 317 registered, 55
distinct resolved (`Done:`), 262 open — unchanged this round (no new R-id
minted or resolved). `DECISION F258` ids: `['D1', 'D2']`, unchanged this
round (none minted). `Gate: F258 R` lines: `['Gate: F258 R1', 'Gate: F258 R2',
'Gate: F258 R3', 'Gate: F258 R4']`, `Gate: F258 R4` newly booked this round
(this round records no verdict on itself — round 6 books that one, per
amend0827 rule 1). R-0570 stays OPEN (0 `Done: R-0570` lines), routed away,
unrelated to this branch.

## Range

Review of `453d1beb..11c006b8`
(HEAD before the C6 handback commit; see the Commits table below for the
exact short SHAs, which are what this handback actually verified against).

## Item status

Every bundle item and every gate, each appearing exactly once:

| Item | Status | Reason |
|------|--------|--------|
| C0a save block to `.agent/authored/f258-r5.md` | done | `shutil.copyfile`, sha256-verified |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`, sha256-verified |
| C1 rewrite `.agent/plan.md` from PLAN5 | done | byte-equal, 41 lines, trailing `\n` confirmed |
| C2 append RECORD5 to `.agent/live_review.md` | done | append-only, whole-file reconstruction AND paragraph-order reading both hold this round (no inherited quirk) |
| C3 apply PAIR-STATUSPROTO2 to `STATUS_closure_protocol.md` | done | FROM 1→0, TO 0→1; byte-identical to reviewer's own pre-verified after-file |
| C4 apply PAIR-BANNER2/PAIR-WHYEXISTS/PAIR-MODULES/PAIR-CONSUMPTION to `self-use-track-v1.md` | done | all four pairs match spec exactly; byte-identical to reviewer's own pre-verified after-file |
| C5 add `self_use_runner.py` and `test_self_use_runner.py` | done | `shutil.copyfile`, sha256-verified against both scratch originals |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | done | both new files sha256-equal to `.remedy-wt/f258-r5/` originals, exact byte counts |
| G2 the plan | done | byte-equal to PLAN5, 41 lines, `## Goal`/`## Next Steps` present, ends with `\n` |
| G3 the record append | done | whole-file reconstruction `base + b"\n" + record5 == committed` True; paragraph-order reading also True this round (no quirk); negative control (flipped byte) correctly rejected in a disposable worktree |
| G4 the ledger | done | R-ids/Done-ids ADDED/REMOVED empty at C1 and C2; DECISION F258 stays `['D1','D2']`, ADDED `[]`; `Gate: F258 R` lines `[...,'F258 R3']`→`[...,'F258 R4']`, ADDED exactly `['F258 R4']` |
| G5 the five prose pairs and the docs suites | done | all five pairs match FROM/TO expectations exactly; `tests/docs/` 295 passed, `test_roadmap_index.py` 30 passed |
| G6 the new module, its test, and the suites | done | ruff clean ("All checks passed!"); four self-use suites 68 passed (7 new); three sanity suites 69 passed |
| G7 the mutation red-proof | done | in a disposable worktree, removing the `JOB_BLOCKED` guard reddened exactly `test_a_blocked_plan_raises_rather_than_running` (6 passed, 1 failed, exit 1); restore from scratch original returned 7 passed, exit 0; worktree removed |
| G8 the state readers and canary | done | five suites 515/52/21/16/42 passed; tree clean; single worktree; every commit's insertion total under 500 |

## Commits

All `+/-` figures are `git diff --numstat`/`git log --numstat` against each
commit's own parent.

### 3a6ce56d docs(f258): save round 5 block to authored/f258-r5.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f258-r5.md` | 248/0 | C0a — verbatim copy of the round's step block, `shutil.copyfile` |

### 1cef9541 docs(f258): mirror round 5 block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 248/285 | C0b — verbatim copy of the same block, `shutil.copyfile`, into the mirror slot |

### da96dbb6 docs(f258): rewrite plan.md for round 5 (T002 consumed means executed)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | 15/15 | C1 — rewritten from slice PLAN5, byte-equal, 41 lines |

### 2846304a docs(f258): append round 4 verdict (Gate F258 R4) to live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 45/0 | C2 — RECORD5 appended verbatim (one paragraph: round 4's Gate F258 R4 verdict); nothing earlier revised |

### 72ff6c13 docs(f258): wire self_use_runner into closure protocol precondition 6
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS_closure_protocol.md` | 4/2 | C3 — PAIR-STATUSPROTO2: precondition 6 now describes the queue item as RUN through `run_next_self_use_item`, never promoted, before `consumed_by` is set |

### 13690776 docs(f258): wire self_use_runner into self-use-track-v1.md
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/self-use-track-v1.md` | 15/5 | C4 — PAIR-BANNER2, PAIR-WHYEXISTS, PAIR-MODULES and PAIR-CONSUMPTION: the banner, "Why it exists", the module table and the consumption section all now describe the runner |

### 11c006b8 feat(f258): add self_use_runner (T002 consumed means executed)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_runner.py` | 107/0 | C5 — new module, `shutil.copyfile` from the reviewer-verified scratch original |
| `tests/orchestration/test_self_use_runner.py` | 183/0 | C5 — new test file (7 tests), `shutil.copyfile` from the reviewer-verified scratch original |

Not tabled per the template's self-reference exception: the commit that
writes this handback (C6, `.agent/handoff.md`) — its own numbers are the
reviewer's to measure at the next gate.

## External actions

- `git worktree add --detach .remedy-wt/g3-negctl-r5 HEAD` — disposable
  worktree for the G3 negative control, detached at `da96dbb6` (post-C1,
  pre-C2).
- `git worktree remove .remedy-wt/g3-negctl-r5 --force` — removed after the
  negative control ran; `git worktree list` afterward showed only the
  primary checkout.
- `git worktree add --detach .remedy-wt/g7-mutation-r5 HEAD` — disposable
  worktree for the G7 mutation red-proof, detached at `13690776` (post-C4,
  pre-C5), per constraint 3 (re-run the mutation red-proof before applying
  the real module/test files).
- `git worktree remove .remedy-wt/g7-mutation-r5 --force` — removed after
  the red-proof ran; `git worktree list` afterward showed only the primary
  checkout.
- `git push -u origin feature/f258-self-use-v2` — to be run immediately
  after this handback's commit. The push's own outcome (new remote SHA) is
  necessarily outside this file's own content, since the push happens after
  this commit is written; it is reported in this round's session report
  instead. No pull request opened — the PR is created only at closure.
- No `gh pr` command run this round (the Open PR Gate does not apply — this
  round stays on the existing `feature/f258-self-use-v2`, per the block's
  own instruction to open no PR).

## Verification

Every gate below ran with a REAL exit code, in the PRIMARY checkout unless
stated otherwise.

**G1 — TRANSPORT.** `python3 -c "..."` byte-compare, both files:
- `packages/orchestration/self_use_runner.py`: sha256
  `77036196d3e31fdd22320b95174395c70d05d455fcfd8f6ddbeeca06dddcb0cb`, 5079
  bytes — equal to `.remedy-wt/f258-r5/self_use_runner.py`.
- `tests/orchestration/test_self_use_runner.py`: sha256
  `1172f6cae620f6dba4266d3b0ec1e03c6ae08993e272f6ada4de55c64d6e288d`, 7110
  bytes — equal to `.remedy-wt/f258-r5/test_self_use_runner.py`.

**G2 — THE PLAN, at C1.** `.agent/plan.md` sha256
`2bee9077ba14d65ce3f19fc1872b16e1054dbd2c8101dd98a6a4d96f2acb350e`, 1935
bytes, 41 lines — equal to PLAN5 on all three counts. Carries `## Goal` and
`## Next Steps`. Ends with `\n` (`open(path,'rb').read().endswith(b'\n')` →
`True`).

**G3 — THE RECORD APPEND, at C2.** Base (re-measured immediately before C2,
fresh) was 1771908 bytes, matching the block's stated expectation exactly,
ending in exactly one `\n` (confirmed: `data.endswith(b'\n') and not
data.endswith(b'\n\n')` → `True`). RECORD5 is 3401 bytes.
1771908 + 1 + 3401 = 1775310, and the committed `.agent/live_review.md`
after C2 is 1775310 bytes — equal, and byte-identical (sha256
`cc07f8dd95eed7cd00488855f962f1185e67d7ea7809a0e12f78e7affc059a41`) to the
reviewer's own pre-verified `.remedy-wt/f258-r5/expected_live_review.md`.
(a) WHOLE RECONSTRUCTION: `base + b"\n" + record5 == committed` → `True`.
(b) LAST `\n\n`-DELIMITED UNIT: `committed.split(b"\n\n")[-1] == record5` →
**`True`** — unlike round 4, this round's base ended cleanly in `\n`, so no
inherited-quirk merge occurred; both readings agree.
NEGATIVE CONTROL, run inside the disposable worktree `.remedy-wt/g3-negctl-r5`
(detached at `da96dbb6`, post-C1/pre-C2): flipped one printable byte inside a
copy of RECORD5 (byte index 100). Reconstruction on the flipped variant vs.
the committed file: `False` — correctly rejects the flip. Reconstruction on
the true RECORD5 vs. the committed file: `True` — correctly accepts the
original. Worktree removed after; `git worktree list` then showed only the
primary checkout.

**G4 — THE LEDGER, at C1 and at C2.**
- Before C1 / after C1 (identical — C1 does not touch `.agent/live_review.md`
  — measured against `git show HEAD:.agent/live_review.md` at `da96dbb6`):
  317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+` ids,
  `DECISION F258` ids `['D1', 'D2']`, `Gate: F258 R` lines
  `['F258 R1', 'F258 R2', 'F258 R3']`.
- After C2: 317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+` ids,
  `DECISION F258` ids `['D1', 'D2']`, `Gate: F258 R` lines
  `['F258 R1', 'F258 R2', 'F258 R3', 'F258 R4']`.
- ADDED registered: `[]`. ADDED resolved: `[]`. `DECISION F258` ADDED: `[]`.
- `Gate: F258 R` lines newly booked: exactly `Gate: F258 R4`.
- `^Done: R-0570` count: 0 before, 0 after (throughout).

**G5 — THE FIVE PROSE PAIRS AND THE DOCS SUITES, at C4.**
- PAIR-STATUSPROTO2: FROM count 1 before / 0 after; TO count 0 before / 1
  after. Committed `STATUS_closure_protocol.md` sha256
  `73a3c967dd78da3c9c5317efbf8ea5b47c5a59f38899fa7162a2e50a9afbd4a0`, equal
  to the reviewer's own pre-verified after-file.
- PAIR-BANNER2: FROM count 1 before / 1 after (survives as the new
  sentence's prefix, as specified); TO count 0 before / 1 after.
- PAIR-WHYEXISTS, PAIR-MODULES, PAIR-CONSUMPTION: each FROM count 1 before
  / 0 after; TO count 0 before / 1 after.
- Committed `self-use-track-v1.md` sha256
  `9a01e2123c06526a61f55d5a3ba363ff373a69de8a8798a4d9f44e01ba681ecc`, equal
  to the reviewer's own pre-verified after-file.
- `python3 -m pytest tests/docs/ -q` → REAL exit 0, `295 passed`.
- `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → REAL
  exit 0, `30 passed`.

**G6 — THE NEW MODULE, ITS TEST, AND THE SUITES, at C5.**
- `python3 -m ruff check packages/orchestration/self_use_runner.py
  tests/orchestration/test_self_use_runner.py` → REAL exit 0, `All checks
  passed!`.
- `python3 -m pytest tests/orchestration/test_self_use_runner.py
  tests/orchestration/test_self_use_generator.py
  tests/orchestration/test_self_use_queue.py
  tests/orchestration/test_self_use_job.py -q` → REAL exit 0, `68 passed`
  (7 new).
- `python3 -m pytest tests/test_data_paths.py
  tests/orchestration/test_development_artifact_boundary.py
  tests/test_path_utils.py -q` → REAL exit 0, `69 passed`.

**G7 — THE MUTATION RED-PROOF, in the disposable worktree
`.remedy-wt/g7-mutation-r5` (detached at `13690776`, before C5's files
existed in the primary checkout), `__pycache__` purged before each run
(0 dirs found each time, consistent with `python3 -B` never writing one),
`python3 -B` throughout.**
- Baseline (module/test copied in from the scratch originals): `python3 -B
  -m pytest tests/orchestration/test_self_use_runner.py -q` → REAL exit 0,
  `7 passed`.
- Mutated (removed the five-line `if plan.status == JOB_BLOCKED: raise
  SelfUseRunError(...)` block): `python3 -B -m pytest
  tests/orchestration/test_self_use_runner.py -q` → REAL exit 1, `1 failed,
  6 passed` — the one failure is exactly
  `TestRunNextSelfUseItem::test_a_blocked_plan_raises_rather_than_running`
  (`Failed: DID NOT RAISE <class
  'packages.orchestration.self_use_runner.SelfUseRunError'>`).
- Restored (`shutil.copyfile` from `.remedy-wt/f258-r5/self_use_runner.py`;
  sha256-confirmed equal to the scratch original before re-running):
  `python3 -B -m pytest tests/orchestration/test_self_use_runner.py -q` →
  REAL exit 0, `7 passed` again.
- `git worktree remove .remedy-wt/g7-mutation-r5 --force`; `git worktree
  list` afterward showed only the primary checkout.

**G8 — THE STATE READERS AND CANARY, at C6 (run before the C6 commit, since
C6 changes only `.agent/handoff.md`, which none of these suites' own
contracts name).**
- `python3 -m pytest tests/ui_server/ -q` → REAL exit 0, `515 passed`.
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → REAL exit
  0, `52 passed`.
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → REAL
  exit 0, `21 passed`.
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → REAL
  exit 0, `16 passed`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL exit 0,
  `42 passed`.
- `git status --porcelain` → empty.
- `git worktree list` → primary checkout only.
- Per-commit insertion totals (`git log --numstat` against each commit's own
  parent), C0a through C5: 248, 248, 15, 45, 4, 15, 290 (107+183) — every
  one under 500. No oversize-commit exception needed or used this round.

## Authored-text proofs

Two authored slices (PLAN5, RECORD5), five FROM/TO pairs, and two whole new
files were applied this round, all via disk-to-disk `shutil.copyfile` or
exact-string FROM/TO matching against the scratch originals under
`.remedy-wt/f258-r5/`, never retyped:

- C0a/C0b: the whole block, sha256
  `9ac5c74ea0dec38c15b4b6a1c76e51c814c307b18478dbdedb3b20946d5dca6d`, 13944
  bytes — three-way equal (scratch original `.remedy-wt/f258-r5/block.md`,
  `.agent/authored/f258-r5.md`, `.agent/last_block.md`).
- PLAN5 → `.agent/plan.md`: sha256
  `2bee9077ba14d65ce3f19fc1872b16e1054dbd2c8101dd98a6a4d96f2acb350e` both
  sides.
- RECORD5 → appended to `.agent/live_review.md`: proved by whole-file
  reconstruction AND by the last `\n\n`-delimited unit equaling RECORD5
  exactly (both readings agree this round).
- PAIR-STATUSPROTO2 → `docs/roadmap/STATUS_closure_protocol.md`: proved by
  exact-string FROM/TO occurrence counts (1→0, 0→1) and by whole-file
  sha256 equality against the reviewer's own pre-verified after-file.
- PAIR-BANNER2, PAIR-WHYEXISTS, PAIR-MODULES, PAIR-CONSUMPTION →
  `docs/system/self-use-track-v1.md`: each proved by exact-string FROM/TO
  occurrence counts, and by whole-file sha256 equality against the
  reviewer's own pre-verified after-file.
- MODULE → `packages/orchestration/self_use_runner.py`: sha256
  `77036196d3e31fdd22320b95174395c70d05d455fcfd8f6ddbeeca06dddcb0cb` both
  sides.
- TEST → `tests/orchestration/test_self_use_runner.py`: sha256
  `1172f6cae620f6dba4266d3b0ec1e03c6ae08993e272f6ada4de55c64d6e288d` both
  sides.

## Deviations & assumptions

None. Every authored slice, pair and whole file matched the block's stated
hashes/byte counts exactly; both the reviewer's own pre-verified
`expected_live_review.md`, `status_closure_protocol_after.md` and
`self_use_track_v1_after.md` scratch files were used as an additional
cross-check and matched byte-for-byte in every case. The G3 paragraph-order
reading, which round 4 could not satisfy literally due to an inherited
dropped-newline defect, holds cleanly this round with no quirk. Nothing in
the block looked wrong; nothing required declaring under constraint 1.

## Next

T003 (findings flow back): a self-use run's outcome (a defect the run
surfaces) flows back into the standard finding ledger under the normal
`.agent/live_review.md` rules — the concrete wiring point (likely the
closure round itself, since that is where a self-use run's outcome is
already recorded) is round 6's own first design decision. Round 6 also owes
the ledger this round's own `Gate: F258 R5` verdict, per amend0827 rule 1
(booked in round 6's first commit, not this round's). Push and Open PR Gate
housekeeping apply as usual; no PR is open on this branch yet (none is
created before closure).

## Reviewer verdict on round 5 (independent re-verification, 2026-08-30)

VERDICT PASS. The reviewer re-ran every gate independently against the real
diff `453d1beb..11c006b8`, not against the worker's own report, and additionally
re-derived every FROM/TO pair and every sha256 from the reviewer's own
pre-verified `.remedy-wt/f258-r5/` scratch originals (prepared and dry-run
tested, including a full end-to-end integration run in a disposable worktree,
BEFORE the block was authored). G1 TRANSPORT: `packages/orchestration/self_use_runner.py`
sha256 `77036196d3e31fdd22320b95174395c70d05d455fcfd8f6ddbeeca06dddcb0cb`
(5079 bytes) and `tests/orchestration/test_self_use_runner.py` sha256
`1172f6cae620f6dba4266d3b0ec1e03c6ae08993e272f6ada4de55c64d6e288d` (7110
bytes), both equal to the scratch originals and to the block's stated
digests. G2 THE PLAN: `.agent/plan.md` sha256
`2bee9077ba14d65ce3f19fc1872b16e1054dbd2c8101dd98a6a4d96f2acb350e`, 1935
bytes, 41 lines, `## Goal` and `## Next Steps` present, ends with `\n`. G3
THE RECORD APPEND: base re-measured at 1771908 bytes ending in exactly one
`\n`; `base + b"\n" + RECORD5 (3401 bytes) == committed (1775310 bytes)` is
TRUE; the last `\n\n`-delimited unit of the committed file equals RECORD5
exactly — unlike round 4, this round's base already ended cleanly, so no
inherited dropped-newline quirk recurred and both the whole-file and the
paragraph-order readings agree. A negative control in a disposable worktree
(byte flipped at index 100 of a RECORD5 copy) was correctly rejected while
the true original was accepted. G4 THE LEDGER: `DECISION F258` unchanged at
`['D1','D2']` (ADDED `[]`); `Gate: F258 R` lines ADDED exactly `['F258 R4']`;
317 distinct `R-` ids and 55 distinct `Done:` ids unchanged before and after
C2; `Done: R-0570` stays 0. G5 THE FIVE PROSE PAIRS: PAIR-STATUSPROTO2,
PAIR-WHYEXISTS, PAIR-MODULES and PAIR-CONSUMPTION each measured FROM 1→0,
TO 0→1; PAIR-BANNER2 (append-shaped) measured FROM 1→1 (survives as the new
sentence's prefix) and TO 0→1 — all five independently re-measured against
the committed files, matching the block exactly. `python3 -m pytest
tests/docs/ -q` (295) and `tests/orchestration/test_roadmap_index.py` (30)
both independently re-run, REAL exit 0, matching the worker's reported
counts. G6 THE NEW MODULE, ITS TEST, AND THE SUITES: `ruff check` on both
new files REAL exit 0, all checks passed; the four self-use suites together
REAL exit 0, 68 passed (7 new); the three repo-wide sanity guards
(`test_data_paths.py`, `test_development_artifact_boundary.py`,
`test_path_utils.py`) REAL exit 0, 69 passed — this module touches none of
their guarded paths, confirmed by reading the diff directly. G7 THE
MUTATION RED-PROOF, independently reproduced by the reviewer in the
reviewer's OWN disposable worktree, `__pycache__` purged, `python3 -B`:
removing the `JOB_BLOCKED` guard block gave REAL exit 1, exactly one
failure (`test_a_blocked_plan_raises_rather_than_running`), 6 passed;
restoring from the scratch original gave REAL exit 0, 7 passed again. G8
THE STATE READERS AND CANARY, all REAL exit 0, matching every prior round's
base exactly: 515, 52, 21, 16, 42. THE TREE: clean, single worktree,
per-commit insertions 248/248/15/45/4/15/290 from `git log --numstat`,
every one under 500 — no oversize exception needed. THE ROUND PASSES: the
change set matches the block's fixed eight paths exactly (plus the handback
commit), the branch is pushed and matches `origin` exactly at `cc373ca3`,
the tree was clean, no `tmp/*` branch or extra worktree survived. No new
finding is raised by this review; the worker's own report matched the
reviewer's independent re-measurement in every particular, with zero
discrepancies.

This verdict (`Gate: F258 R5`) is PENDING — per amend0827 rule 1 it is
booked into `.agent/live_review.md` in the FIRST COMMIT of the next round
that is happening anyway, which is round 6. It is persisted now by being
written into this pushed, committed handoff, which is the durable carrier
amend0827 rule 1 names for exactly this gap.
