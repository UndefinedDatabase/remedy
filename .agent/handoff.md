# Handoff — F036, round 2 (book round 1, record DECISION F036 D3, land T002's first half: the
model-written tour through the summary role, the no-new-claims check, the honest first stop and
the labelled fallback)

## Session

SESSION 1 of feature F036 · round 2 · rounds so far 2. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, the required
source files in full (`result_tour.py` as round 1 left it, `artifact_summary.py`,
`structured_outputs.py`, `intake.py`, `failure_postmortem.py`, `model_routing.py`'s
`ROLE_CONFIG_CALL_SITES` section, `test_model_routing.py`'s call-site test, `conftest.py`'s
`_no_live_ollama_reach`, `pingpong_job.py`'s `TaskEntry`, and `test_artifact_summaries.py`'s stub
pattern), plus DECISION F036 D3 in the booking diff and `docs/agents/handback_template.md`; wrote
the S1–S6 generation code, its 11 new tests and the mutation tool from the specification; ran the
payload-verification script, the G1/G2 byte-equality and hash checks, ruff, the G4 pytest
selection twice (once during authoring, once as the formal gate), `integrity check`, and the G5
mutation tool twice (a preliminary dry run in a throwaway worktree, then the official run at C5).

## Range

Review of `44965328..HEAD` (`HEAD` is this handback's own commit, `F036 R2 C6`, on
`feature/f036-guided-result-tour`).

## Commits

### 7c44acc65 F036 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r2-block.md | 297/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r2-booking.diff | 73/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r2-plan.md | 29/0 | copy of the reviewer's plan.md payload |

### 33a5cd4ec F036 R2 C2: book round 1, record DECISION F036 D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 55/0 | DECISION F036 D3 appended by booking.diff |
| .agent/live_review.md | 2/0 | round 1's `Gate: F036 R1 —` entry appended by booking.diff |
| .agent/plan.md | 6/6 | rewritten to the reviewer's plan.md payload |

### c5d6a8afd F036 R2 C3: generate the result tour through the summary role, no new claims
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/model_routing.py | 1/0 | `ROLE_CONFIG_CALL_SITES` gains `result_tour.py`/`summary`, after the `pingpong_job.py` entry (S6) |
| packages/orchestration/result_tour.py | 335/5 | S1–S6: schema, `tour_source_text`, `tour_claim_problems`, `build_tour_prompt`, `generate_result_tour`, `PROVIDER_CALL_ERRORS`, `tour_call_fn`; `build_fallback_tour` refactored onto a shared `_assemble_fallback_tour` helper (behaviour unchanged) |
| tests/orchestration/test_model_routing.py | 6/5 | the two call-site-count numerals moved 9→10 and 4→5, comment updated (S6) |

### 4bdadd926 F036 R2 C4: test the generated tour, its claim check and its fallbacks
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_result_tour.py | 282/1 | 11 new tests: no-call-fn parity, mechanical-first ordering, the four claim breaches, an unknown-anchor drop, the nine-stop ceiling, the no-sound-stops fallback, provider-error/unparseable fallbacks (never raising, retried once), the prompt's anchors and numeral 7, source-text acceptance/diff-count lines, and `tour_call_fn`'s spy + refused-Ollama behaviour |

### 9321d739a F036 R2 C5: add the round 2 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r2-mutations.py | 147/0 | the G5 red-proof tool: 10 mutations (m1–m10 of the block), all caught |

### <this commit> F036 R2 C6: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f036-r2-worker/dryrun-mut HEAD` — a preliminary,
  non-official dry run of the mutation tool before C5 existed, to validate the tool's own
  correctness. Outcome: worktree created at `4bdadd926` (then C4's tip); tool run passed all 10
  mutations; removed with `git worktree remove --force` (exit 0) immediately after, restoring
  `git worktree list | wc -l` to 64.
- `git worktree add --detach .remedy-wt/f036-r2-mut 9321d739a` — the official G5 worktree, cut
  from C5 per the block. Outcome: worktree created at detached HEAD `9321d739a`.
- `git worktree remove --force .remedy-wt/f036-r2-mut` then `git worktree prune` — the official
  G5 worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 64,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — pending, run immediately after this
  commit per the bundle order. Its real outcome is reported in the round's reply (G6), not here,
  because this file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use):
```
booking.diff: 73 lines, 12245 bytes, sha256 4f1d09fd…8f70188b533f  MATCH
plan.md:      29 lines,   992 bytes, sha256 ff10018e…c380f35bb7373bd5474  MATCH
```
Block self-check: 297 lines, sha256 `aa5d7a13…04775e89c4b3` — MATCH on both readings (measured
twice: once before reading the block, once as this section's own re-check).
`.agent/authored/f036-r2-*` copies vs. sources, read back via `git show 7c44acc65:<path>`, all
byte-identical:
```
f036-r2-block.md    vs .remedy-wt/f036-r2/block.md            sha256 match
f036-r2-booking.diff vs .remedy-wt/f036-r2-payloads/booking.diff sha256 match
f036-r2-plan.md      vs .remedy-wt/f036-r2-payloads/plan.md      sha256 match
```

**G2 THE BOOKING** — every file's bytes and sha256 at C2 (`git show 33a5cd4ec:<path>`) MATCHED
the reviewer's table exactly:
```
.agent/decisions.md   2356984 bytes  sha256 3a674224…5180e3cca  MATCH
.agent/live_review.md  313639 bytes  sha256 293c27fd…d4d6b39212 MATCH
.agent/plan.md            992 bytes  sha256 ff10018e…35bb7373bd5474 MATCH
```
`open_finding_ids` over `.agent/live_review.md` TEXT at C2 read `[]`. The ledger's last non-empty
line at C2 begins `Gate: F036 R1 — ` (confirmed verbatim). `git diff --name-only 7c44acc65
33a5cd4ec` named exactly the 3 paths of the G2 table, no more, no fewer.

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/result_tour.py
packages/orchestration/model_routing.py tests/orchestration/test_model_routing.py
tests/orchestration/test_result_tour.py` at C4: `All checks passed!`, REAL_EXIT=0.
`tour_claim_problems`, `PROVIDER_CALL_ERRORS`/`_provider_call_error_types` and
`generate_result_tour` were quoted whole from `git show c5d6a8afd` — see the round's reply for the
full text; behaviour matches S3, S5 exactly.

**G4 THE TESTS** — the full 26-target serial selection:
```
1627 passed, 4 skipped, 1 warning in 103.59s (0:01:43)
REAL_EXIT=0
```
SKIPPED lines (all 4):
```
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
```
— the same 4 skips the block's baseline names, unchanged. Node count of
`tests/orchestration/test_result_tour.py` by `--collect-only -q`: 24 (13 from round 1 plus 11 new
this round). Block's baseline: `1616 passed, 4 skipped` at `44965328` with the round-1 13 nodes
already counted in it. 1616 + 11 (this round's new nodes) = 1627 — no discrepancy.
`python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0, `ok`
true.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r2-mut 9321d739a` then
`python3 -B .agent/authored/f036-r2-mutations.py <worktree>`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1 claim check ignores numbers: exit=1 failed=2 nodes=[test_each_kind_of_new_claim_is_dropped_with_a_naming_reason, test_every_stop_dropped_gives_the_no_sound_stops_fallback]
m2 claim check ignores backtick spans: exit=1 failed=1 nodes=[test_each_kind_of_new_claim_is_dropped_with_a_naming_reason]
m3 claim check ignores paths: exit=1 failed=1 nodes=[test_each_kind_of_new_claim_is_dropped_with_a_naming_reason]
m4 denylist matched case-sensitively, before lower-casing: exit=1 failed=2 nodes=[test_each_kind_of_new_claim_is_dropped_with_a_naming_reason, test_every_stop_dropped_gives_the_no_sound_stops_fallback]
m5 mechanical first stop not put first: exit=1 failed=3 nodes=[test_three_sound_model_stops_follow_the_mechanical_first_stop, test_each_kind_of_new_claim_is_dropped_with_a_naming_reason, test_nine_sound_model_stops_keep_eight_in_all]
m6 PROVIDER_CALL_ERRORS holds no RuntimeError: exit=1 failed=1 nodes=[test_provider_errors_and_unparseable_text_fall_back_without_raising]
m7 a generated tour keeps even one stop, no fallback for fewer than two: exit=1 failed=1 nodes=[test_every_stop_dropped_gives_the_no_sound_stops_fallback]
m8 a not-ok outcome is labelled summary-role: exit=1 failed=1 nodes=[test_provider_errors_and_unparseable_text_fall_back_without_raising]
m9 tour_call_fn binds GeneratedSummaryContent from artifact_summary instead: exit=1 failed=1 nodes=[test_tour_call_fn_asks_resolve_role_config_and_make_structured_call_fn]
m10 the structured call is made with allow_parse_retry=False: exit=1 failed=1 nodes=[test_provider_errors_and_unparseable_text_fall_back_without_raising]
control (after): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
No mutation stayed green; no extra test was needed. A preliminary, non-official dry run against a
throwaway worktree at C4's tip produced the identical result before C5 existed (see External
actions), which is why no correction round was needed between writing the tool and running it
officially. `git worktree remove --force .remedy-wt/f036-r2-mut`, `git worktree prune`,
`git worktree list | wc -l` = 64 (matches step 4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run (both the preliminary dry run and the official run); no extra test needed |

## Authored-text proofs

`booking.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. The two payloads (`booking.diff`, `plan.md`) were verified line count/byte
count/sha256 against the PAYLOADS table before use, and the committed `.agent/authored/f036-r2-*`
copies read back byte-identical to their sources via `git show` (G1, above). `.agent/plan.md` was
REWRITTEN to the payload file by `shutil.copyfile`, never hand-edited; its post-write sha256
equals the payload table's own `ff10018e…` row and C2's resulting file hashes matched the
reviewer's G2 table exactly for all 3 files (see Verification, G2). No reviewer-authored text was
applied outside these two payloads; the S1–S6 generation code, its 11 tests and the mutation tool
are worker-authored against the block's specification, not transcribed from a payload.

## Deviations & assumptions

- **`build_fallback_tour` refactored onto `_assemble_fallback_tour` (not ordered by the block, done
  for reuse).** S5 says `generate_result_tour` "reads the context and `build_report_sources(job)`
  once" before branching, including the `call_fn is None` branch, whose answer must equal
  `build_fallback_tour`'s. Rather than re-reading the job's records a second time inside that
  branch (calling `build_fallback_tour(job)` fresh), a private helper
  (`_assemble_fallback_tour(job, sources, context, generator=...)`) was factored out of the
  existing `build_fallback_tour` and reused by both it and every fallback path of
  `generate_result_tour`. `build_fallback_tour`'s OWN behaviour and every round-1 test's
  assertions against it are unchanged (S7); this is an internal reuse, not a behaviour change, and
  test 13 (`test_generate_with_no_call_fn_matches_build_fallback_tour`) asserts the two stay equal.
- **Claim-check wording is worker-chosen (S3 sets the four breach KINDS, not their exact reason
  text).** The block specifies four kinds of breach and that each earns "one readable line" naming
  the offending number/span/path/word, but not the sentence's exact wording. Reasons were written
  as `"the number {n!r} is not in the records"`, `` "the backtick span `{s}` is not in the
  records" ``, `"the path {p!r} is not in the records"` and `"the claim word {w!r} is not
  allowed"` — each names the offending token, joined by `"; "` per stop as S5 orders, and every
  test asserts by substring containment against these reasons rather than by exact-string match,
  so the choice of wording carries no hidden coupling.
- **A path candidate is read off the stop's OWN text with backtick spans stripped, checked against
  the UNSTRIPPED source text (S3's "read after the backtick spans are removed" is ambiguous about
  which text).** Read as: search for paths in the stop's title+body with any backtick-quoted
  spans blanked out first (so a path already reported as a backtick breach is not reported a
  second time as a path breach), and check what is found against the source text as written.
  Tests exercise the four breach kinds independently, so this reading was never load-bearing
  against an alternative interpretation producing a different observable answer in this round's
  tests.
- **Caught a test bug of this round's own authoring before C4 was committed (permitted under
  constraint 4: "A test this round itself wrote that is wrong may be corrected before C6").**
  `test_nine_sound_model_stops_keep_eight_in_all` originally used digit-suffixed titles
  (`f"Filler {i}"` for `i` in `range(9)`), which made `tour_claim_problems` — which scans title
  AND body together — read the digit in the title itself as an unrecorded-number claim, dropping
  7 of the 9 "sound" stops instead of keeping them. Caught by running the test locally before
  committing C4; corrected to letter-suffixed titles (`"Filler A"`.."Filler I"`) before the first
  commit of this test file, so no red C4 ever landed.
- No other deviation. Every mutation in G5 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit; nothing under AGENTS.md "If Blocked" applies
  this round.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 2). (3) T002's second half —
`tour.json` stored and versioned at the job terminal, the command line's tour, and the fixture
goldens. Open-findings count: 0. Operator-questions count: 1 (Q6).
