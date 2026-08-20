# Handback — F086 Release capability, R13 (the release gate; record R12)

Branch `feature/f086-release-capability`, pushed, unmerged, no PR. R13 registers
R-0582; the open set moves 162 → 163. T003's DECISION half lands:
`packages/orchestration/release_gate.py` is a pure function over values a caller
supplies. NOTHING CALLS IT YET, so until R14 the gate refuses nothing — the
changelog DATA and the manual-trigger caller were deliberately left out.

## Range

Review of 3351878d..HEAD.

## Commits

### 9607b2bd chore(agent): save the F086 R13 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r13.md | +490/-0 | C0a, the block saved byte-verbatim |

### 891fc05e chore(agent): mirror the F086 R13 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +305/-305 | C0b, mirror of the COMMITTED C0a file |

### 86a0536d docs(state): advance the F086 plan to R13
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +11/-7 | C1, the PLAN13 slice, whole file |

### ad26358c chore(review): register R-0582 and record the F086 R12 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, FIND0582 then RECORD11, EOF-append |

### 24ad9e9d feat(orchestration): add the release refusal gate
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/release_gate.py | +82/-0 | C3, the GATE slice, new file |

### 27c462d1 test(orchestration): seeded-failure tests for the release gate
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_release_gate.py | +106/-0 | C4, the TESTS slice, new file |

### C5 — this commit (grouped, R-0149: a handoff cannot table itself)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | round report | C5, this rewrite; its own insertion count and the post-C5 path set are reported in the ROUND REPORT, per block step 5 and §3 item 14 |

## External actions

- `git push -u origin feature/f086-release-capability` after C4 → `3351878d..27c462d1`, ok.
- `git worktree add .remedy-wt/mut-r13 27c462d1` → created, detached HEAD, for G10 only.
- `git worktree remove .remedy-wt/mut-r13` → removed; `git worktree list` back to 1 line.
- `git push` after C5 → see round report (it carries this commit).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. Nothing merged, no PR created.

## Verification

G1 HYGIENE. `git status --porcelain` EMPTY (0 lines) in the primary checkout
before and after every one of the six commits and at the handback. `.agent/STOP`
re-read from disk before C0a and again at the handback: ABSENT both times.
`git worktree list` = 1 line at the handback. Branch
`feature/f086-release-capability`.

G2 TRANSPORT. `.remedy-wt/f086-r13.md`, `HEAD:.agent/authored/f086-r13.md` and
`HEAD:.agent/last_block.md` are all three byte-EQUAL at
sha256 85312d57f16691d20c9d33b2186ea5ee6d251e15df3fa8a95a4d864d840c5f5b,
30339 bytes, 490 lines. SIZE re-measured from the COMMITTED C0a file: 490 total,
10 marker lines, 234 slice content lines, 244 slice+markers, 246 prose — equal to
constraint 6's declared 490 / 246 / 244 / 10 on every number.

G3 PLAN. `HEAD:.agent/plan.md` byte-equal to the PLAN13 slice, sha256
cd794e8cc754acb919f312450a0187e4d736118d9a12abe5608191b66d1a648e, 2411 bytes,
42 lines — under 50 — and contains `## Goal`, `## Next Steps` and `F086`.

G4 LEDGER APPEND. The pre-C2 blob (`86a0536d:.agent/live_review.md`) is a
byte-exact PREFIX of `HEAD:.agent/live_review.md`; the remainder is byte-equal to
FIND0582 followed immediately by RECORD11, sha256
049b4b04e6103d2eb077af7551658387f8dd116df42985e6125332beb257ea28, 6164 bytes,
4 lines.

G5 LEDGER SETS. Both extractions run and AGREE at each end. `3351878d`:
164 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions /
0 anchored `Landed:` / 162 open, under BOTH. HEAD: 165 / 2 / 0 / 0 / 0 / 163,
under BOTH. The two registered id SETS are EQUAL at each end. Symmetric
difference of the HEAD registered set against the `3351878d` set is exactly
`['R-0582']` under paragraph AND under line-anchored extraction.

G6 NO MARKER LEAKED. Marker LINES (lines beginning `<<<SLICE ` or `<<<END `) at
HEAD: `.agent/plan.md` 0, `.agent/live_review.md` 0, `.agent/handoff.md` 0,
`packages/orchestration/release_gate.py` 0,
`tests/orchestration/test_release_gate.py` 0.

G7 VERDICT PER ROUND. `Gate: ` paragraphs: 10 at `3351878d`, naming R3 R4 R5 R6
R7 R8 R9 R10 R11 R12; 11 at HEAD, the added one naming R13. R13's own entry is
absent by construction; none was added.

G8 THE CODE IS THE SLICE. `HEAD:packages/orchestration/release_gate.py` byte-equal
to GATE, sha256 e881d61d647e30ef622bbd85c73bfb365013d4474d1a710e9ef6dec77efc9384,
3467 bytes, 82 lines. `HEAD:tests/orchestration/test_release_gate.py` byte-equal
to TESTS, sha256 e5150cd74f7a237d30ad85df144b3bb900a606f221961d690705cde2fc872454,
3437 bytes, 106 lines. `git ls-tree 3351878d` returns EMPTY for both: ABSENT at
the base.

G9 REFUSALS. `python3 -m pytest tests/orchestration/test_release_gate.py -q -rf`
in the primary checkout → REAL EXIT CODE 0, `12 passed in 0.26s`. Separately and
OUTSIDE pytest, `refuse_release` returned, verbatim:
- (a) unchanged → `()`
- (b) `ci_green=False` → `('CI is not green for this commit',)`
- (c) `tag='v9.9.9'` → `("tag 'v9.9.9' does not match distribution version '1.2.3'",)`
- (d) changelog without a `1.2.3` section → `("CHANGELOG.md has no section for version '1.2.3'",)`
- (e) `wheel_bytes=WHEEL_SIZE_BUDGET_BYTES+1` → `('wheel is 8388609 B, over the 8388608 B budget',)`
(a) is empty; (b) to (e) are each non-empty and each names the rule it was seeded
to trip, not merely some rule.

G10 THE TESTS CAN FAIL. In the throwaway worktree `.remedy-wt/mut-r13` at
27c462d1 only; baseline there exit 0, 12 passed.
(i) `    if request.wheel_bytes > WHEEL_SIZE_BUDGET_BYTES:` counted 1x in the
file, replaced by `    if False:` → exit 1, 2 failed / 10 passed; reverted,
bytes identical to the original.
(ii) `    if not request.ci_green:` counted 1x in the file, replaced by
`    if False:` → exit 1, 2 failed / 10 passed; reverted, bytes identical.
After the last revert: exit 0, 12 passed, and that worktree's
`git status --porcelain` is `''` — measured, not assumed. Worktree then removed.

G11 THE PARSER CAN SAY NO.
`changelog_section("# Changelog\n\n## [1.0.0] - 2026-01-01\n\n- x\n", "0.0.0-absent")`
returned `None`. Without this control G9 (d) would prove nothing.

G12 NO REGRESSION. Three runs in the PRIMARY checkout, each a blocking
`subprocess.run` started only after the previous had ENDED — NONE OVERLAPPED,
and the wall-clock stamps show it.
(a) `pytest tests/orchestration/test_ci_stages.py tests/orchestration/test_ci_stage_selection.py -q`
→ exit 0, `20 passed in 8.89s` (13:52:57 → 13:53:06).
(b) `pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
→ exit 0, `160 passed in 19.87s` (13:53:06 → 13:53:26).
(c) `pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.28s`
(13:53:26 → 13:53:46).

G13 LINT. `python3 -m ruff check packages/orchestration/release_gate.py
tests/orchestration/test_release_gate.py` → exit 0, stdout
`All checks passed!`, stderr empty. Rule-code multiset read from the same command
with `--output-format json`: `{}` — EMPTY. Both paths are new, so there is no
base reading to compare against.

G14 COMMIT SIZE (insertions, the `+` column of `git show --numstat`), every
commit in `3351878d..HEAD` before C5: 9607b2bd 490, 891fc05e 305, 86a0536d 11,
ad26358c 4, 24ad9e9d 82, 27c462d1 106. None exceeds 500. C5's own count is in the
round report.

G15 HISTORY. Linear, every commit exactly one parent:
3351878d → 9607b2bd → 891fc05e → 86a0536d → ad26358c → 24ad9e9d → 27c462d1.
`git reflog` over this round shows only `commit:` entries at HEAD@{0} through
HEAD@{5} — no amend, no rebase, no reset, no force-push.

G16 PATH SET. `git diff --name-only 3351878d..HEAD` before C5 is exactly
`.agent/authored/f086-r13.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `packages/orchestration/release_gate.py`,
`tests/orchestration/test_release_gate.py` — constraint 2's set less
`.agent/handoff.md`. ABSENT from the range and EXISTING at the base per
`git ls-tree 3351878d` (so the clause forbids something real): `pyproject.toml`,
`.github/workflows/ci.yml`, `hatch_build.py`, `apps/cli/version_report.py`,
`packages/orchestration/ci_stages.py`. `CHANGELOG.md`: absent from the range AND
absent at the base — both readings taken, so that clause forbids nothing today
and is recorded as such (finding R-0559).

G17 OPEN PR GATE, READ-ONLY.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
verbatim. Nothing merged.

## Authored-text proofs

Five slices, each extracted programmatically by its one-line
`<<<SLICE NAME>>>` / `<<<END NAME>>>` markers from the COMMITTED
`.agent/authored/f086-r13.md` and applied byte-verbatim; none retyped, none
edited. Disk-to-disk equality against that committed original, all full-length:

| Slice | Target | sha256 of the applied bytes | lines | equal |
|---|---|---|---|---|
| PLAN13 | .agent/plan.md | cd794e8cc754acb919f312450a0187e4d736118d9a12abe5608191b66d1a648e | 42 | yes |
| FIND0582+RECORD11 | .agent/live_review.md remainder | 049b4b04e6103d2eb077af7551658387f8dd116df42985e6125332beb257ea28 | 4 | yes |
| GATE | packages/orchestration/release_gate.py | e881d61d647e30ef622bbd85c73bfb365013d4474d1a710e9ef6dec77efc9384 | 82 | yes |
| TESTS | tests/orchestration/test_release_gate.py | e5150cd74f7a237d30ad85df144b3bb900a606f221961d690705cde2fc872454 | 106 | yes |

The block itself: `.remedy-wt/f086-r13.md` ≡ `.agent/authored/f086-r13.md` ≡
`.agent/last_block.md` at
85312d57f16691d20c9d33b2186ea5ee6d251e15df3fa8a95a4d864d840c5f5b.

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: no deviation. Exactly C0a, C0b, C1, C2, C3, C4, C5,
  in the block's order, one commit each, none extra, none dropped, none
  reordered.
- DECLARED OVERAGE, AGENTS.md DECISION D15: this file exceeds the 100-line cap.
  Cause, named: the MANDATED content — a per-commit changed-files table for
  seven commits, a raw Verification transcript for seventeen gates G1–G17, and
  every digest written IN FULL at 64 characters rather than elided as G2
  explicitly orders under finding R-0581. No mandated section is dropped to meet
  the cap. This overage is itself the subject of R-0582, registered by this
  round's C2, which rules on no repair.
- Assumption, stated because the block does not settle it: `Range` names the
  literal token `HEAD`, following the convention of the R10–R12 handbacks on this
  branch, because a handoff cannot name the SHA of the commit that writes it.
- The scratch helpers used this round (`extract_r13.py`, `mutate_r13.py`,
  `gates_r13.py`, the pre-C2 ledger copy, the mutation worktree) all live under
  the gitignored `.remedy-wt/`; none is committed and none is in the path set.
- No verdict on any round is written here. This section, and this file, report
  what was MEASURED.

## Next

1. Re-read `.agent/STOP` from disk (Phase 1 rule 1) — a sentinel that appeared
   mid-session is otherwise invisible.
2. Then the Open PR Gate (Phase 1 rule 2):
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

Then: review R13 over `3351878d..HEAD`, and on a PASS author R14 — the DATA and
the CALLER this round deliberately omitted: `CHANGELOG.md`, a test that the real
changelog covers the version `pyproject.toml` declares, and the manual-trigger
workflow that calls `refuse_release` with the real tag, version, changelog and
wheel size. Until that caller exists the gate refuses nothing.
