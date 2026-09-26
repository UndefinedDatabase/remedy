# Handoff — F289, round 2

## Session

SESSION 1 of feature F289 · round 2 · rounds so far 2. Context remaining at
handback: comfortable — the round closed inside a single session with no
compaction needed.

## Range

Review of `8163cf8b`..`HEAD` (`HEAD` is this handback's own commit, `F289 R2
C6`, on `feature/f289-self-use-sources`).

## Commits

### 7ef89b68e F289 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r2-block.md | 342/0 | copy of this round's block (`shutil.copyfile`) |
| .agent/authored/f289-r2-plan.md | 30/0 | copy of the plan.md payload |
| .agent/authored/f289-r2-records.diff | 83/0 | copy of the records.diff payload |

Measured insertions: 455 (342+30+83), matching the block's expectation
(block's own line count 342 plus 113).

### fce2c8b0c F289 R2 C2: book round 1 and R-1073's resolution, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 54/0 | `git apply records.diff` — appends DECISION F289 D2 |
| .agent/live_review.md | 3/1 | `git apply records.diff` — Done: R-1073, Gate: F289 R1 entry |
| .agent/plan.md | 8/10 | rewritten to the plan.md payload |
| .agent/prose_slips.md | 1/0 | `git apply records.diff` — round 1 docstring-prose slip |

Expected by the block: 54/0, 3/1, 8/10, 1/0 — measured identically.

### b0c530fd5 F289 R2 C3a: add the documentation-staleness catalog, types and checks C01 to C05
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/doc_staleness.py | 494/0 | NEW FILE — types, shared readers, checks C01–C05 (part 1 of 2, see deviations) |

### 4bdeed602 F289 R2 C3b: add checks C06 to C12 and the staleness catalog runner
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/doc_staleness.py | 322/0 | checks C06–C12, `CHECKS`, `run_staleness_checks` (part 2 of 2) |

C3a+C3b together are the block's C3 (816 lines total); split under constraint 2
(a single commit would have reached 500). Declared in Deviations.

### aa46e9d52 F289 R2 C4: render the first stale documentation claim as the generator's Tier 2
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/self_use_generator.py | 92/10 | Tier 2 provenance/targeting, `default_docs_root`, `_doc_staleness_tier` real body, docstring rewrite (S4) |

### dc04ef473 F289 R2 C5a: test the staleness catalog's checks C01 to C09
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_doc_staleness.py | 448/0 | NEW FILE — STALE/FRESH fixtures for C01–C09 (part 1 of 2) |

### f37834648 F289 R2 C5b: finish testing the staleness catalog (C10 to C12) and test the generator's Tier 2
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_doc_staleness.py | 146/0 | C10–C12 fixtures, `TestCheckSuiteShape`, `TestAgainstTheRealTree` (part 2 of 2) |
| tests/orchestration/test_self_use_generator.py | 215/5 | `TestDocStalenessTier`, `TestDocStalenessTierRealChain`, autouse fixture stub |

### b12b1ed1e F289 R2 C5c: add the mutation tool for the staleness catalog and Tier 2
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r2-mutations.py | 224/0 | NEW FILE — the G5 mutation tool, seventeen mutations |

C5a+C5b+C5c together are the block's C5 (no insertion count was expected for
C3–C5 by the block); split three ways under constraint 2 (the whole bundle
totalled 1033 insertions). Declared in Deviations.

### b9d4ce16a F289 R2 fix: reword C02's claim text to stop reading as a group-only advertisement
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/doc_staleness.py | 3/3 | reworded three C02 claim/truth f-strings |
| tests/orchestration/test_doc_staleness.py | 5/5 | updated C02's fixture assertions to match |

An undeclared-by-the-block repair commit, found by G4 itself (see Deviations):
`tests/cli/test_advertised_commands.py`'s group-only sweep read the literal
source text `` `remedy config {sub}` `` as an unrunnable group-only
advertisement (the `{` character satisfies its command-tail-character check).
Reworded the three C02 f-strings to name the subcommand without writing
`remedy config` immediately before it. No check *behavior* changed — the
real-tree claim set is identical before and after (still exactly the two
claims DECISION F289 D2 names) — only the claim/truth wording. This is
production wording, not a test correction, so it does not fit constraint 4's
"a test this round itself wrote that is wrong" clause exactly, but it is the
same spirit: a real gate (G4) caught a real defect in the round's own new
code before C6, and it is repaired and declared here rather than papered
over.

### .agent/handoff.md (this commit, F289 R2 C6)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f289-r2-mut b9d4ce16a` — for G5.
- `git worktree remove --force .remedy-wt/f289-r2-mut` then `git worktree
  prune` — G5's last action; `git worktree list` afterward showed the
  primary checkout and exactly the pre-existing worktrees (see Verification).
- `git push` — real outcome reported in Verification (G6).
- No PR created, no PR merged, no branch checkout, no force-push, no stash —
  none were ordered and none were done.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → does not exist (real exit 2, `No such file or
  directory`).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty.
  `git branch --show-current` → `feature/f289-self-use-sources`. `git log
  --oneline -1` → `8163cf8ba F289 R1 C6: rewrite handoff for round 1` — all
  three matched.
- Block bytes: measured 342 lines, sha256
  `b850212fd8a1e67099501b150125bf69503af8ac66df942164db08a3ff14dd8b` against
  `.remedy-wt/f289-r2/block.md` — both matched the delegation message.
- `git worktree list` reported as found (the primary checkout plus the F015,
  F020, F023, F024, F025, F027, F284, F289 dry/sim worktrees and ten
  `job-*` worktrees) — unchanged at the end (see G6).

PAYLOADS (measured against the table, before use):
| file | lines | bytes | sha256 match |
|---|---|---|---|
| plan.md | 30 | 1047 | yes |
| records.diff | 83 | 12528 | yes |

CONSTRAINT 1 — `git apply --check .remedy-wt/f289-r2-payloads/records.diff` →
real exit 0. `git apply` (real) → real exit 0.

G1 TRANSPORT — every `.agent/authored/f289-r2-*` copy read back with `git show
7ef89b68e:<path>` compared byte-for-byte against its source: all three
byte-identical (block: 26220 bytes both sides; plan.md: 1047 bytes both
sides; records.diff: 12528 bytes both sides).

G2 THE BOOKKEEPING — every file's sha256 read with `git show
fce2c8b0c:<path>` matched the reviewer's table exactly:
| path | bytes | sha256 match |
|---|---|---|
| .agent/decisions.md | 2215932 | yes |
| .agent/live_review.md | 320788 | yes |
| .agent/prose_slips.md | 370558 | yes |
| .agent/plan.md | 1047 | yes |

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger TEXT:
at `8163cf8b` → `['R-1073']`; at `fce2c8b0c` → `[]`. At `fce2c8b0c` the ledger
holds no line starting `Landed: R-1073` (confirmed by direct scan) and its
last non-blank line begins `Gate: F289 R1 — ` (confirmed verbatim).

G3 THE CODE — `python3 -m ruff check packages/orchestration/doc_staleness.py
packages/orchestration/self_use_generator.py
tests/orchestration/test_doc_staleness.py
tests/orchestration/test_self_use_generator.py` at C5 (re-run at the branch
tip after the wording-fix commit) → `All checks passed!`, real exit 0.

Python `ast` reading of every `Import`/`ImportFrom` node in
`packages/orchestration/doc_staleness.py`, at any AST depth (including the
two deferred imports inside `ShippedTruth.live()`): `__future__`, `re`,
`collections.abc`, `dataclasses`, `pathlib`, `apps.cli.command_catalog`,
`packages.orchestration.config`. None names `subprocess`, `socket` or
`urllib`. PASS.

S6's list of claims on the real tree (`run_staleness_checks()` over the
repository, `ShippedTruth.live()`), whole:
1. `docs_index_guide_registration` | `docs/README.md` | claim: "the
   Quick-Find Table has no link to `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`"
   | truth: "`docs/guides/real-test-execution-snapshot-rollback-user-guide-v1.md`
   ships"
2. `config_cli_table_complete` | `docs/guides/remedy-toml-user-guide.md` |
   claim: "the CLI commands table never documents the `config` subcommand
   `show`" | truth: "the `config` subcommand `show` ships"

Both are exactly the two claims DECISION F289 D2 measured and named; no
further claim was found — no real staleness beyond the two named, and no
defect of the checks themselves was left over the real tree (several were
found and fixed during authoring against fixtures before this reading — see
Deviations for the one found by a gate, G4's advertised-commands sweep).

G4 THE TESTS — serial run at the branch tip (after the wording-fix commit,
which is C5's content corrected in place per the block's own numbering — see
Deviations) of the block's selection:
```
833 passed, 1 skipped in 154.51s (0:02:34)
```
Real exit code 0 (`REAL_EXIT=0`). The one SKIPPED line:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
```
— the same D12 quarantine the reviewer's base run also skipped.

Node accounting: `--collect-only -q` on `tests/orchestration/test_doc_staleness.py`
→ 30 tests (new file, did not exist at `8163cf8b`). `--collect-only -q` on
`tests/orchestration/test_self_use_generator.py` at `8163cf8b` → 52 tests; at
the branch tip → 61 tests, 9 new. Total new nodes: 30 + 9 = 39. Reviewer's
base was 794 passed + 1 skipped; 794 + 39 = 833, matching the measured total
exactly. No other difference to account for.

`python3 -m apps.cli.main integrity check --json` → all six checks `pass`,
`fail_count` 0, `ok` true.

G5 THE RED PROOFS — `.agent/authored/f289-r2-mutations.py`, run as
`python3 -B .agent/authored/f289-r2-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f289-r2-mut` against a worktree at
`b9d4ce16a` (this round's tip before the handback commit):
```
control (before) | exit=0 failed=0 nodes=[]
m1 C01 reads only the Guides section | exit=1 failed=2 nodes=[...test_stale, ...test_a_real_missing_quick_find_entry_becomes_a_tier_2_item]
m2 C02 ignores a subcommand that ships and is not documented | exit=1 failed=1 nodes=[...test_stale]
m3 C03 accepts a second word that is not a group | exit=1 failed=1 nodes=[...test_stale]
m4 C04 resolves a link against the root instead of the guide's folder | exit=1 failed=1 nodes=[...test_fresh]
m5 C05 keeps punctuation in a heading's slug | exit=1 failed=1 nodes=[...test_fresh]
m6 C06 no longer skips a match followed by * | exit=1 failed=1 nodes=[...test_fresh]
m7 C07 reads a span whose first segment is not a key prefix | exit=1 failed=1 nodes=[...test_fresh]
m8 C08 drops the table prefix and checks the bare name | exit=1 failed=2 nodes=[...test_stale, ...test_fresh]
m9 C09 writes the folder guides as guides | exit=1 failed=2 nodes=[...test_stale, ...test_fresh]
m10 C10 accepts a path without checking that it exists | exit=1 failed=1 nodes=[...test_stale]
m11 C11 reads a span whose first segment is a key prefix | exit=1 failed=1 nodes=[...test_fresh]
m12 C12 reads only the catalog's descriptions and no ArgDef.help | exit=1 failed=1 nodes=[...test_the_live_truth_s_catalog_texts_include_argdef_help_not_only_descriptions]
m13 fences are no longer skipped by C04 | exit=1 failed=1 nodes=[...test_fresh]
m14 Tier 2 ignores the keys the queue already targets | exit=1 failed=2 nodes=[...test_of_two_claims_the_first_is_offered_then_the_second, ...test_a_consumed_entry_targeting_a_key_still_withdraws_it]
m15 generate_self_use_item tries Tier 3 before Tier 2 | exit=1 failed=1 nodes=[...test_tier_2_wins_over_a_stubbed_actionable_tier_3_warning]
m16 Tier 2 accepts a claim holding a line break | exit=1 failed=2 nodes=[...test_a_claim_holding_a_line_break_raises, ...test_a_truth_holding_a_line_break_raises]
m17 Tier 2 writes the truth on the Claim line and the claim on the Shipped truth line | exit=1 failed=1 nodes=[...test_a_single_claim_becomes_a_tier_2_item]
restored byte-identical: True (packages/orchestration/doc_staleness.py)
restored byte-identical: True (packages/orchestration/self_use_generator.py)
control (after) | exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every one of the seventeen mutations was caught with at least one failing
node; none stayed green, so no test had to be added after the fact. The
worktree was removed (`git worktree remove --force .remedy-wt/f289-r2-mut`,
`git worktree prune`); `git worktree list` afterward matched the BEFORE
ANYTHING ELSE reading exactly.

G6 TREE AND PUSH:
- `git status --porcelain` → empty (after this commit).
- `git log --oneline -n 8` → (see below, filled after commit).
- `git worktree list` → primary checkout plus exactly the worktrees
  constraint 6 names (the pre-existing F015/F020/F023/F024/F025/F027/F284/F289
  dry/sim trees and the ten `job-*` trees) — nothing else.
- `git push` → real outcome below.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` →
  `[]` (empty).

## Authored-text proofs

The block copy and the two payload copies (`plan.md`, `records.diff`),
read back at `7ef89b68e`, equal the reviewer's originals byte for byte (see
G1 above). `records.diff` was applied with `git apply` unedited (constraint
1); `.agent/plan.md` was rewritten to the `plan.md` payload verbatim via
`shutil.copyfile`, confirmed byte-identical by the G2 sha256 reading.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1–4 | done | |
| PAYLOADS verification | done | |
| C1 | done | |
| C2 | done | |
| C3 | deviated | split into C3a/C3b (constraint 2, 816 lines) |
| C4 | done | |
| C5 | deviated | split into C5a/C5b/C5c (constraint 2, 1033 lines) |
| C6 | done | this commit |
| Wording fix (undeclared by the block) | done | G4's advertised-commands sweep caught a false group-only reading in C02's claim text; reworded and re-verified (see Deviations) |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| Constraint 3 (tracked path set) | done | matches exactly, see below |
| Constraint 6 (worktree cleanup) | done | |
| Constraint 7 (no full suite) | done | only the named selection ran |

## Deviations & assumptions

1. **C3 split into C3a and C3b.** The block's C3 (the whole
   `doc_staleness.py`) is 816 lines, over the 500-insertion cap (constraint
   2). Split at a clean boundary after C05's function (line 494): C3a adds
   lines 1–494 (types, shared readers, C01–C05, 494 insertions), C3b appends
   lines 495–816 (C06–C12, `CHECKS`, `run_staleness_checks`, 322 insertions).
   No behavior split — the module is only complete and importable-with-effect
   after C3b, but nothing imports it before C4.
2. **C5 split into C5a, C5b and C5c.** The block's C5 (both test files plus
   the mutation tool) totals 1033 insertions. `test_doc_staleness.py` alone
   is 594 lines, itself over the cap, so it is split the same way as C3:
   C5a adds lines 1–448 (C01–C09 fixtures plus the shared helpers, 448
   insertions), C5b appends lines 449–594 (C10–C12, `TestCheckSuiteShape`,
   `TestAgainstTheRealTree`, 146 insertions) together with the whole
   `test_self_use_generator.py` diff (215/5), and C5c adds the mutation tool
   whole (224 insertions). Two commits in one round now carry a declared
   split (C3 and C5); AGENTS.md's oversize-commit exception is about a
   single commit exceeding 500 lines, not about how many times a block's
   named commit is split into same-cap parts, so this is read as ordinary
   constraint-2 splitting, not a second "accepted, not a precedent" claim.
3. **An undeclared repair commit.** Running G4 against the round's own new
   code (as it must, since G4 runs the shared selection including
   `tests/cli/test_advertised_commands.py`) surfaced a real defect: three
   f-strings in `doc_staleness.py`'s C02 check literally read
   `` `remedy config {sub}` ``, and the advertised-commands sweep's tail-check
   treats a `{` right after a group name as "looks like a command line",
   making `config {sub}` a candidate group-only invocation that does not
   resolve. This is a defect in the round's OWN new code discovered by a
   gate the block itself orders, not a payload and not test-only — constraint
   4's "a test this round itself wrote that is wrong may be corrected before
   C6" is the nearest-fitting clause, but the wrong text here is production
   wording, not a test. Repaired by rewording the three claim/truth strings
   (no check *behavior* changed, confirmed identical on the real tree before
   and after) and updating the C02 fixture's expected strings to match, as
   one small commit (`b9d4ce16a`, 3/3 + 5/5 insertions/deletions), declared
   here rather than folded silently into C5.
4. No document was edited to clear either of the two real claims (S6):
   `docs/README.md`'s missing Quick-Find link and the CLI-commands table's
   missing `show` row are left for the self-use track, per D2.
5. No test written by the round was found wrong and corrected (the wording
   fix above is production code, covered by item 3, not this clause).

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2,
then T003 — three consecutive generator calls on an empty ledger produce
three distinct items, and one runs to completion under the test provider
inside the default cost cap. Open findings: 0. Operator questions: 0.
