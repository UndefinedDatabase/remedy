# Handback — F314 "Findings paydown v10," round 9 (closing round)

## Session

SESSION 1 of feature F314 · round 9 · rounds so far 9

Context self-assessment: this session verified every prepared file's bytes against the manifest
before use, applied C1 through C3 byte-for-byte with the ledger rotation's output matching the
simulation exactly, ran all five closing gates to the exact readings expected, and is about to
commit C4 with this handback and open the branch's pull request with ample context remaining.

The session ends here because F314 is closed and the next feature starts in a fresh session.

State block:
Feature F314 (accepted `[x]`), branch `feature/f314-findings-paydown-v10`, base `aa9900968`.
Fortschritt: 100 % (F314 is accepted; its pull request waits for the next session's Open PR Gate)
— Schätzung

## Range

Review of `aa9900968`..HEAD.

## Commits

### add31060c F314 R9 C1: book round 8, re-assign the open findings to F316, the Built State, the block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r9-pr_body.md` | +44/-0 | NEW FILE; byte copy of the reviewer-authored PR body |
| `.agent/authored/f314-r9.md` | +143/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/live_review.md` | +10/-0 | round 8's PASS verdict booked; the eight open findings re-assigned from F314 to F316 |
| `.agent/plan.md` | +6/-6 | rewritten for F314 round 9, the closing round |
| `docs/roadmap/features/T2_F314.md` | +24/-0 | the Built State section added |

All five paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct byte-equality check (see Authored-text proofs) confirm each equality.

### d6cc7aeb7 F314 R9 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-66 | the rotation moved 6 gate records, 12 finding pairs (24 records) and 2 resolved-text records out to the archive |
| `.agent/live_review_archive.md` | +66/-0 | the same records received |

Produced by one run of `scripts/rotate_live_review.py` (see Verification); both resulting files
proved byte-equal to the reviewer's prepared `c2-*` files before being staged.

### c36418b00 F314 R9 C3: register F316 — Findings paydown v11 under amend0911-feedback rule B: feature file, STATUS line, pin 316, README counters
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F316.md` | +53/-0 | NEW FILE; F316's feature file |
| `docs/roadmap/STATUS.md` | +7/-0 | F316's `- [ ]` line added under its own Tier 2 heading, Tier 8 re-opened after it |
| `tests/docs/test_docs_consistency.py` | +5/-1 | `TOTAL_FEATURES` moved 315 → 316 with the registration comment |
| `README.md` | +2/-2 | the registered-items denominator 315 → 316 and the Tier 2 total row 49 → 50 |

All four paths are byte copies of the reviewer's prepared `c3-*` files; gate 1's `verify.py` and a
direct byte-equality check (see Authored-text proofs) confirm each equality.

### this commit — F314 R9 C4: accept F314 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F314's line `[~]` → `[x]`, carrying the Built State summary (measured before this commit joined; see Authored-text proofs) |
| `README.md` | +14/-3 | the accepted-items numerator 161 → 162, the Tier 2 accepted row 48 → 49, F314's entry added to the Tier 2 list after F307's (measured before this commit joined) |
| `scripts/self_use_queue.json` | +1/-1 | SU-080's `consumed_by` set to `F314` (measured before this commit joined) |
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `add31060c`, exactly the five named paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `d6cc7aeb7`, exactly the two ledger files, rotation output matching `sim-rotation.txt` apart from the `written:` path |
| C3 | done | `c36418b00`, exactly the four named paths, each byte-equal to its prepared `c3-*` file |
| C4 | done | this commit, the three named paths plus this handback |
| Gate 1 (`verify.py`) | done | every line `True`, `C4` read `absent` before this commit, last line `ALL True` |
| Gate 2 (STATUS line) | done | occurs exactly once in `docs/roadmap/STATUS.md`, no line starts `- [~]` |
| Gate 3 (pytest selection) | done | exit 0, `680 passed` (matches `sim-gate3.txt`'s passed count; seconds differ), no FAILED/ERROR/SKIPPED line |
| Gate 4 (integrity) | done | `integrity exit 0`, `"fail_count": 0`, matching `sim-gate3.txt` |
| Gate 5 (open ids) | done | `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']`, the exact list required |
| Push | pending | ordered to run immediately after this commit; see this session's reply for the result |
| Pull request | pending | ordered to run after the push; see this session's reply for the number and URL |

## External actions

- No push, `gh` command or worktree action has run yet at the moment this file is written: the
  block orders the push and the pull request to follow this commit, and Rule A4 requires the
  handback to be this branch's last commit before them. Their outcomes are reported in this
  session's final reply, not rewritten into this file (write-once rule, PH v3).
- One scratch directory used, `.remedy-wt/f314-r9-worker/` (created this round), holding the
  copy-and-verify scripts for C1, C3 and C4, the rotation runner, and the gate-2/gate-5 readers.
  `.remedy-wt/f314-r9/` (the reviewer's prepared tree) was only read, never written.

## Verification

Gate order per the block, run once each after C4's three files were copied and before this commit.

1. `git status --porcelain` → exactly the three C4 files modified (`README.md`,
   `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`).
   `python3 .remedy-wt/f314-r9/prep/verify.py .` → every line `True` (`C4` read `absent`, with the
   three working-tree equality checks also `True`), last line `ALL True`.

2. STATUS line: the content of `status_line.txt` without its trailing newline occurs exactly once
   in `docs/roadmap/STATUS.md` (count 1), and no line of it begins `- [~]`.

3. `python3 .remedy-wt/f314-r9/prep/gate3.py .`, run once:
   ```
   exit 0
   680 passed in 94.61s (0:01:34)
   NOTICE ... R-1411: 3 entries of the configured data root ... changed in the folders a
   supervisor this run did not start and its clients write; not counted: [...]
   integrity exit 0 6 pass; ['{"check_count": 6, "checks": [{"message": "handlers=201",
   "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS",
   "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0,
   context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message":
   "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
   "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene",
   "status": "pass"}, {"message": "no open blocker/high findings", "name":
   "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}']
   ```
   `exit 0` matches `sim-gate3.txt`'s first line; `680 passed` matches its second line's passed
   count (the simulation read `91.63s`, this run `94.61s`, which the block permits to differ); no
   `FAILED`, `ERROR` or `SKIPPED` line appeared. The `NOTICE` line names the data root per the
   conftest's own wording, but because the exit code was already 0 with the matching passed count
   and no FAILED/ERROR line, DECISION F151 D6's one-more-run exception does not apply (it binds
   only an exit-1 reading) and no second run was made.

4. Gate 3's integrity line, read from the same run above: `integrity exit 0` and
   `"fail_count": 0`, matching `sim-gate3.txt` exactly, including all six check messages.

5. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']` — the exact
   list required.

The rotation's own run (C2, before the gates), in full:
```
exit 0
gate records moved: 6
finding pairs moved: 12 (24 records)
resolved-text records moved: 2
old ledger size: 178365 bytes
new ledger size: 144769 bytes
old archive size: 7286732 bytes
new archive size: 7320328 bytes
open findings before: 8
open findings after: 8
gate headers matching neither known form (left in place): 1
written: .agent/live_review.md and .agent/live_review_archive.md
```
Ledger size: 178365 bytes before, 144769 bytes after. Archive size: 7286732 bytes before,
7320328 bytes after. Every line but `written:` equals `sim-rotation.txt`'s corresponding line; the
`written:` line differs only in the tree root, as the block anticipates, and is quoted here with
the machine path removed.

## Authored-text proofs

- `digests.txt` was checked against its own stated sha256
  (`77772417faa7da48e57021404e66905226bacfd7b88d869c136adeaacfdb432a`, matched), then every one of
  its seven listed entries was checked with a Python sha256 reader and every one read `OK`, then
  every one of `manifest.tsv`'s fourteen prepared files was checked against its listed sha256 and
  every one read `OK` — all before any prepared file was copied, run or read.
- `.agent/authored/f314-r9.md` against `block.md`: identical sha256
  (`e4f8b063af9a7f08920aed095f30f17a55b0e365d368d578b708a14c3af06587`). Byte-identical.
- All five C1 paths, both C2 paths, and all four C3 paths proved byte-identical to their `c1-*`,
  `c2-*` and `c3-*` prepared files respectively, each with its own read-only comparison script,
  before staging.
- The three C4 paths (`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`)
  proved byte-identical to their `c4-*` prepared files before staging.
- The STATUS-line proof the block names specifically: `status_line.txt` without its trailing
  newline occurs exactly once in `docs/roadmap/STATUS.md` (count 1). That line, with its package
  folder written as `~` per the block's instruction:
  `- [x] F314 — Findings paydown v10 (T001–T008 complete; R-1246, R-1281, R-1351, R-1353, R-1426,
  R-1428, R-1448 and R-1450 open — owned by F316; accepted 2026-10-24 · live review
  PASS_WITH_RISKS — ACCEPTED · Evidence job f314r8e1001 · package
  remedy-review-20261024-030553-READY_FOR_REVIEW.zip · SHA-256
  cbcf7163ae8ffa580d6ea95e572df6e29b2260b71129ab428280f7a96687fec3 · package path ~ · accepted
  HEAD 7e02a9110f3253ff93ece51a2ba3dbc0c408373f)`.

## Deviations & assumptions

None. C1 through C4 landed in the block's exact order, on the one branch, with no extra, dropped
or reordered commit; every prepared byte was copied verbatim and proved equal before being staged;
every `git diff --cached --numstat` reading equalled `manifest.tsv`'s lines for its commit; the
rotation's exit code and output matched `sim-rotation.txt` apart from the one line the block
excepts; all five gates read exactly what the block and the simulation required, and gate 3's
`NOTICE` line did not trigger DECISION F151 D6's re-run exception because the run's exit code was
already 0. The push and the pull request have not run yet at the time this file is written, which
is the block's own ordering (THEN, after C4) rather than a deviation from it.

## For the operator, in plain sentences

This clean-up repaired twelve written-down problems and carries eight of them to the next
clean-up. The practice queue no longer offers work that needs the internet, and it no longer
offers error handlers that are meant to catch everything. A project can now name its builder and
its reviewer once, in its own settings. The test campaign opens its orders the same way a
person's own order is opened. The paid practice run repaired the planner's half of those settings,
on its own branch, and that repair was never applied to this branch; the next clean-up will read
it. The whole test collection passed on the code that ships, and the computer time it used was a
little above the limit, which the next clean-up will watch. This session could not start the test
run on GitHub and asks the operator to start it once. The review package is named
remedy-review-20261024-030553-READY_FOR_REVIEW.zip and sits in the package folder quoted above as
`~`. A pull request is open and will be merged at the start of the next session unless the
operator merges it earlier.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: this branch's pull request merges in the NEXT session, never in this
   one.
3. The booking of this round's verdict happens in the next feature's first commit.
4. Rule A5: the next feature is the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 2. Open findings: 8 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428,
R-1448 and R-1450, owned by F316).
