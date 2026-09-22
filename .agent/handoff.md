# Handback — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 21 · T002's sweep: every `--json` command answered under test, and the one gap it found (D13)

## Session

SESSION 5 of feature F283 · round 21 · rounds so far 21

This round booked round 20's PASS, appended a correction that restates round
19's verdict in the canonical `VERDICT <TOKEN>` form (finding R-1032),
registered R-1033 and R-1034, recorded DECISION F283 D13, landed T002's
`--json` sweep and the catalog-to-dispatch parity check in a new
`tests/cli/test_json_contract.py`, and converted `stats report --json`'s
success answer from a bare document to the envelope (`emit_ok(**document)`,
R-1033), updating its readers in `tests/cli/test_stats_report.py` in the same
commit. Every gate ran clean; no deviation from the block's ordered sequence
was needed and no extra commit was required.

Context self-assessment: the large majority of the working budget remained
at the point this handoff was written.

## Range

Review of `a100a48a`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 193 | 193 | True |
| sha256 | `b610bc56442713770c362dd16fe66d30e347ed205f585bd0d4794e77d7e0d34e` | `b610bc56442713770c362dd16fe66d30e347ed205f585bd0d4794e77d7e0d34e` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `a100a48a`, matching the delegation message.
- The branch tip's one expected red,
  `tests/orchestration/test_final_audit_evidence.py::TestReviewStateExtraction::test_the_manifest_reads_the_real_ledger_as_the_canonical_reader_does`,
  confirmed present at `a100a48a` before C1: `1 failed, 14 passed` on the
  file alone. No other failure was seen at any reading in this round.

## Commits

### c9916adf F283 R21 C1: copy round 21 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r21-block.md | +193/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r21-decisions.md | +53/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r21-ledger.md | +12/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r21-plan.md | +35/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r21-prose_slips.md | +1/-0 | byte-for-byte copy of prose_slips.md |

Measured insertions (`git show --numstat`): **294** (193+53+12+35+1).

### 5680f0ac F283 R21 C2: book round 20's PASS, correct round 19's verdict token, register R-1033 and R-1034
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +53/-0 | append decisions.md payload: DECISION F283 D13 |
| .agent/live_review.md | +12/-0 | append ledger.md payload: round 20's `Gate:` entry, the round 19 verdict-token correction, R-1032/R-1033/R-1034 registrations, and R-1032's `Done:` paragraph |
| .agent/plan.md | +14/-12 | rewrite to plan.md payload, byte-identical |
| .agent/prose_slips.md | +1/-0 | append prose_slips.md payload: the round 20 allowlist-slot slip |

Measured insertions: **80** (53+12+14+1); 12 deletions from the plan.md rewrite.

### e2d1278c F283 R21 C3: sweep every --json command's envelope and the catalog-dispatch parity (D13)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_json_contract.py | +163/-0 | NEW: `INVALID_CANDIDATES` (every `supports_json` catalog entry, 144) and `SUCCESS_CANDIDATES` (D13 (1)'s narrower set — no positional, `read_only`, no mutation/execution, not excluded, 33 after excluding `ui.stop` under finding R-1034); `_call` runs the grouped CLI's own `main(argv)` in process and reads the real exit code (`SystemExit` or the implicit 0 a `read_only` success returns with); `_assert_one_envelope_matching_its_exit_code` pins D13 (2)'s three properties (one JSON object, `schema_version` 1 + boolean `ok`, exit code 0 iff `ok`); `TestInvalidArgumentSweep` (144 cases, `ok` false), `TestSuccessSweep` (33 cases), `TestCatalogDispatchParity` (2 tests, D13 (5)) |

Measured insertions: **163**.

### d63c48ff F283 R21 C4: stats report answers --json success in the envelope (R-1033)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/stats_ledger_cmd.py | +20/-4 | `_cmd_stats_report`'s `--json` branch now builds the document with `cost_report_json` (the dict `cost_report_json_bytes` serialises) and answers `emit_ok(**document)`, keeping every key the old bare document carried; the text branch keeps calling `render_cost_report_markdown` unchanged; `cost_report_json_bytes` is no longer imported here (still exported by `packages/orchestration/cost_report.py`, untouched); docstring gains one paragraph naming the fix and the deliberate absence |
| tests/cli/test_stats_report.py | +17/-0 | NEW `test_the_json_success_answer_is_the_envelope_over_a_real_ledger` in `TestReportRendering`: runs `_cmd_stats_report(..., json_output=True)` against `report_ledger` (a real ledger, not an empty data root) and asserts `schema_version` 1, `ok` true, and that `total`/`buckets`/`segments` — keys the old document carried — are still present |

Measured insertions: **37** (20+17); 4 deletions.

### C5 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |
| .agent/live_review.md | +1/-0 | one line: `Landed: R-1033 — <what changed, and C4's sha>` (the worker's mark for a fix the reviewer has not yet authored a resolution for; no `Done:` paragraph) |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r21-worker d63c48ff`, used for G5's
  control and all three named mutation red-proofs, each reverted with
  `git checkout --` before the next, confirmed clean
  (`git -C .remedy-wt/f283-r21-worker status --porcelain` empty) before
  removal.
- `git worktree remove .remedy-wt/f283-r21-worker` immediately after the
  final control re-run; `git worktree list` shows the primary checkout alone
  (repeated in the session reply).
- `git push origin feature/f283-machine-contracts-part-two` after C5 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in
  the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- `git stash` was **not** used at any point this round.

## Verification

### G1 — PAYLOADS transport, then five authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 12/12 | 11354/11354 | True |
| decisions.md | 53/53 | 4272/4272 | True |
| plan.md | 35/35 | 1512/1512 | True |
| prose_slips.md | 1/1 | 303/303 | True |

**All readings equal: True.**

Five `.agent/authored/f283-r21-*` copies (the block copy plus four
payloads), each read back from the committed tree with
`git show c9916adf:<path>` and compared byte-for-byte with its source:

| copy | equal to source |
|---|---|
| f283-r21-block.md | True |
| f283-r21-decisions.md | True |
| f283-r21-ledger.md | True |
| f283-r21-plan.md | True |
| f283-r21-prose_slips.md | True |

**Copies compared: 5. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`a100a48a`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 543665 | 11354 | 555019 | True |
| .agent/decisions.md | 1834490 | 4272 | 1838762 | True |
| .agent/prose_slips.md | 362989 | 303 | 363292 | True |

Matches the block's stated composition exactly (555019, 1838762, 363292).

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R20 — ` = **1**,
`^Gate: F283 R19 correction — ` = **1**, `^Done: R-1032 — ` = **1**, and one
`^- R-103[234] — ` line each (`R-1032`, `R-1033`, `R-1034`, each = **1**).
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `a100a48a` | **24** |
| C2 (`5680f0ac`) | **26** |

Added: `['R-1033', 'R-1034']`. Removed: `[]`. Matches the block's stated
24 → 26, ADDED `R-1033`/`R-1034`, REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`850a578badeab646c381a760ad585d116d997a201238cee7a73b7536ccc3cc6d`
both). Line count: **35**, under the AGENTS.md 50-line rule.

**(d)** `python3 -m pytest tests/orchestration/test_final_audit_evidence.py -q`
after C2: **15 passed**, exit 0 — the whole file, including the test
R-1032 names.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `5680f0ac`→`e2d1278c` | `tests/cli/test_json_contract.py` | 163 |
| C4 `e2d1278c`→`d63c48ff` | `apps/cli/commands/stats_ledger_cmd.py`, `tests/cli/test_stats_report.py` | 37 |

Sweep candidate counts, measured by importing `CATALOG` directly: **INVALID
144** (every `supports_json` entry), **SUCCESS 33** (34 candidates before
exclusion, minus `ui.stop` — the one exclusion, under finding R-1034,
written as `EXCLUDED_FROM_SUCCESS_SWEEP = {"ui.stop": "..."}` in the test).
Both match the reviewer's dry-run reading at `a100a48a` (144, 33) exactly.

`python3 -m pytest tests/cli/test_json_contract.py --collect-only -q`:
**179 tests collected** (144 + 33 + 2 parity tests).

`git diff --name-only a100a48a d63c48ff -- packages/` prints **nothing**.

### G4 — TARGETED SELECTION, ruff, integrity, golden path

`.remedy-wt/f283-r21-scratch/selection.txt` under `-n auto`. The reviewer's
`a100a48a` reading: `1 failed, 11752 passed, 13 skipped`, exit 1, over 308
paths (the one failure being R-1032's). This round's own three readings
(309 paths throughout, since `tests/cli/test_json_contract.py` already
existed on disk from C3's work before each run — the selection script joins
it by file existence, not by commit):

| when | exit | summary | BAD |
|---|---|---|---|
| after C2 | 0 | 11933 passed, 13 skipped | none |
| after C3 | 0 | 11933 passed, 13 skipped | none |
| after C4 | 0 | 11933 passed, 13 skipped | none |

**Zero failed and zero errors at all three readings**, as constraint 4
requires; the reading after C2 is the first clean one, matching the block's
statement that C2 repairs the tip's one known failure.

`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/commands/stats_ledger_cmd.py`, `tests/cli/test_json_contract.py`,
`tests/cli/test_stats_report.py` — 3 paths): **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C4:
`"passed": true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C4:
**42 passed**, exit 0.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r21-worker` at C4 (`d63c48ff`), never
committed. Files: `tests/cli/test_json_contract.py`,
`tests/cli/test_stats_report.py`, run together as the control:

| step | exit code | result |
|---|---|---|
| control (initial) | 0 | 191 passed |
| control (final, post-revert confirmation) | 0 | 191 passed |

| mutation | exit code | result | failing test(s) |
|---|---|---|---|
| (a) C4's `emit_ok` in `_cmd_stats_report` prints the old renderer's text again | 1 | 6 failed, 6 passed | C4's own `test_the_json_success_answer_is_the_envelope_over_a_real_ledger`, plus `test_the_json_parses_and_carries_its_version_and_comparison`, `test_the_handler_resolves_and_dispatches_from_a_namespace`, and all three `TestPriorPeriodComparison` tests (collateral: every reader of the `--json` success shape breaks once it stops parsing as JSON) |
| (b) `apps/cli/grouped.py`'s `_usage_refusal` prints its prose line instead of calling `emit_error` under `--json` | 1 | 47 failed, 97 passed, 35 deselected | 47 of the 144 `TestInvalidArgumentSweep` cases — every command whose refusal in this exact argv shape reaches `_usage_refusal` rather than the earlier "missing required argument" branch inside `main` (`self.report`, `dev.smoke-help`, `dev.status`, `roadmap.status`, `roadmap.next`, `ci.run`, `integrity.check`, `data.usage`, `data.reclaim`, `config.list`, `config.show`, `config.sources`, `config.init`, `config.validate`, and 33 more of the same shape) |
| (c) `stats.report`'s handler is removed from `stats_ledger_cmd.COMMAND_HANDLERS` | 1 | 1 failed, 1 passed | `TestCatalogDispatchParity::test_every_catalog_command_id_has_exactly_one_handler`, naming `['stats.report']` |

Each mutation reddened its named target and nothing unexpected beyond the
collateral (a) and (b) explain. Each mutation was reverted with
`git checkout --` (byte-for-byte back to the committed text) and confirmed
clean (`git -C .remedy-wt/f283-r21-worker status --porcelain`, empty) before
the next. `git worktree remove .remedy-wt/f283-r21-worker` afterward.
`git worktree list` (post-removal): the primary checkout alone.

## Authored-text proofs

- The five copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r21-payloads/` and `.remedy-wt/f283-r21-block.md`: **five
  readings, all True** (G1).
- The three APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md,
  543665+11354=555019), `.agent/decisions.md` (decisions.md,
  1834490+4272=1838762), and `.agent/prose_slips.md` (prose_slips.md,
  362989+303=363292), all equal to the block's own stated composition (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and four payload copies
  at C1 were made with `shutil.copyfile`; the three appends by reading each
  payload's bytes and writing base+payload back to disk; the plan.md
  rewrite by `shutil.copyfile`, then verified sha256-equal.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC, DECISION F283 D13 (C3) and finding R-1033's fix clause
  (C4) — there is no reviewer-authored diff to compare against for those
  files; G3/G4/G5 above are the proof they meet the SPEC.

## Deviations & assumptions

None. The block's five commits landed in order with no extra, dropped or
reordered commit; every constraint held; every gate read clean at every
required point.

1. **Constraint 1** (no payload edited or retyped): held — `shutil.copyfile`
   for C1's five copies and the plan.md rewrite; byte-read-then-write for
   C2's three appends.
2. **Constraint 2** (every commit under 500 insertions by `git show
   --numstat`): held — 294, 80, 163, 37; this handoff exempt as a single
   `.agent/**` state file (plus one `Landed:` line in `.agent/live_review.md`
   in the same commit, per the block's own C5 instruction).
3. **Constraint 3** (the round's tracked path set is at most the block's
   enumeration): held — the round's whole path set (12 distinct paths before
   this commit, listed below) is a SUBSET of the enumeration, using none of
   the two discretionary allowances (`import_reachability_allowlist.txt`,
   a selection-guard test file) because neither was needed this round: no
   new module joined the D11 (c) reachable closure, and no existing test's
   guard went red from this round's own work.
4. **Constraint 4** (every commit from C2 on leaves selection A at zero
   failed/errors): held — see G4, all three readings (after C2, C3, C4)
   read zero failed and zero errors.
5. **Constraint 5** (STOP on an out-of-scope red): not invoked — no gate
   went red outside the round's own editable scope at any point.
6. **Constraint 6** (nothing merged): held — no `gh pr merge`, no `gh pr
   create`, no checkout of `main`.
7. **Constraint 7** (a G5 worktree under `.remedy-wt/`, removed last,
   `git worktree list` reported): held — `.remedy-wt/f283-r21-worker`,
   removed immediately after the final control re-run, `git worktree list`
   reported clean afterward (repeated in the session reply for G6).
8. **Constraint 8** (no swept command reaches outside the isolated data
   root, a network or a server): held — every SUCCESS-half candidate ran
   under the suite's autouse `_isolated_data_root` fixture, and the ONE
   command that would not have been safe by the catalog's classification
   alone, `ui.stop`, is excluded BY NAME under finding R-1034, exactly as
   DECISION F283 D13 (3) orders; no other exclusion was needed — the full
   309-path selection reading at every one of C2/C3/C4 shows no network- or
   server-shaped failure.
9. `git stash` was never used this round.

### The round's whole tracked path set (before this commit)

`git diff --name-only a100a48a d63c48ff` — **12** distinct paths; plus
`.agent/handoff.md` from this commit makes **13** — a SUBSET of constraint
3's full enumeration (5 authored copies + 4 `.agent/**` state files + 1
`apps/` module + 2 named test files; the two discretionary slots unused):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r21-block.md | C1 `c9916adf` |
| 2 | .agent/authored/f283-r21-decisions.md | C1 `c9916adf` |
| 3 | .agent/authored/f283-r21-ledger.md | C1 `c9916adf` |
| 4 | .agent/authored/f283-r21-plan.md | C1 `c9916adf` |
| 5 | .agent/authored/f283-r21-prose_slips.md | C1 `c9916adf` |
| 6 | .agent/decisions.md | C2 `5680f0ac` |
| 7 | .agent/live_review.md | C2 `5680f0ac`, touched again by C5 |
| 8 | .agent/plan.md | C2 `5680f0ac` |
| 9 | .agent/prose_slips.md | C2 `5680f0ac` |
| 10 | tests/cli/test_json_contract.py | C3 `e2d1278c` |
| 11 | apps/cli/commands/stats_ledger_cmd.py | C4 `d63c48ff` |
| 12 | tests/cli/test_stats_report.py | C4 `d63c48ff` |
| 13 | .agent/handoff.md | C5 (this commit) |

No path outside constraint 3's enumeration was touched:
`tests/orchestration/import_reachability_allowlist.txt`, any other selection
test file, `.agent/candidates.md`, `.agent/context.md`,
`.agent/operator_questions.md`, root `README.md`, `scripts/**`, anything
under `packages/` and no other file under `apps/` appear **0** times.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `a100a48a`; block 193 lines / matching sha256 |
| Tip's one expected red confirmed | done | `test_final_audit_evidence.py` — 1 failed, 14 passed, before C1 |
| C1 copy block + 4 payloads | done | 294 insertions |
| C2 book round 20 PASS, correct R19 token, register R-1033/R-1034 | done | 80 insertions (53+12+14+1, 12 deletions from plan rewrite); open set 24→26, added R-1033/R-1034, removed none |
| C3 the sweep, D13, catalog-dispatch parity | done | 163 insertions; 144 invalid + 33 success candidates, 1 exclusion (`ui.stop`, R-1034); 179 nodes collected |
| C4 stats report answers --json success in the envelope | done | 37 insertions (20+4, 17+0); R-1033's fix clause followed exactly |
| C5 the handback | done | this commit |
| G1 payload transport + authored copies | done | 4/4 payload readings equal; 5/5 authored copies byte-identical |
| G2(a) live_review.md + decisions.md + prose_slips.md append | done | 543665+11354=555019; 1834490+4272=1838762; 362989+303=363292 |
| G2(b) line-anchored gate lines + open set by distinct id | done | 1 each of the 5 named lines; 24→26, added R-1033/R-1034, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 35 lines, under 50 |
| G2(d) test_final_audit_evidence.py after C2 | done | 15 passed, exit 0 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; 144/33 candidate counts and the 1 exclusion reported; 179 collected nodes; nothing under `packages/` |
| G4 targeted selection, ruff, integrity, golden path | done | zero failed/errors at all three readings (after C2/C3/C4); ruff exit 0 over 3 paths; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c) | done | all three go RED, each naming its required test(s); control 191/191 passed at exit 0 |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile` / bytes read+write only |
| Constraint 2 every commit under 500 insertions | done | 294, 80, 163, 37; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 12 paths before this commit (13 after), a SUBSET of the full enumeration; neither discretionary slot needed |
| Constraint 4 selection at zero failed after every commit from C2 | done | zero failed/errors at all three readings |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no such red occurred |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 a G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r21-worker`, removed, `git worktree list` reported after |
| Constraint 8 no swept command reaches outside the data root/network/server | done | `ui.stop` excluded by name under R-1034; no other exclusion needed; no such failure at any selection reading |
| `git stash` used | done (n/a) | never used this round |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk. While it exists, write nothing and end.
2. The review of round 21 — C1 through C5, all six gates re-derived.
3. Then the closure sequence, as `.agent/plan.md` lists it: the Built State
   and Acceptance of `docs/roadmap/features/T2_F283.md`, the evidence job and
   a fresh review zip, the STATUS line, the pull request. Its one full suite
   runs on the merged tree (DECISION amend0921-operator-feedback D1).

Open findings count: **26**. Operator-questions count: **0**.
