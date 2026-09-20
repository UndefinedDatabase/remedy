# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 6

## Session

SESSION 2 of feature F277 · round 6 · rounds so far 6

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and the payload `decisions.md` (DECISION F277 D6) in full,
verified the step block's bytes before using it — 241 lines, sha256
`efedf806b797709f9cdc9cfebc1dc481ea4f194a5b098d20339157598f466e19`, matching the block's own
R-0954 reading exactly — found no `.agent/STOP` on disk, verified the branch was already checked
out clean at `91034712`, verified all four state payloads plus the code diff byte-for-byte against
the block's stated line counts and digests, applied C1a through C4, ran G1 through G5 with every
reading executed and recorded, and every one of the six gates read green: this is a full PASS,
written honestly as such and not merely asserted.

## Range

Review of `91034712`..`HEAD` (HEAD is C5, this commit).

## Commits

### 02a215cf F277 R6 C1a: copy round 6 payloads into .agent/authored/ (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r6-block.md | +241/-0 | byte copy of the step block itself |
| .agent/authored/f277-r6-decisions.md | +43/-0 | byte copy of payload decisions.md (DECISION F277 D6) |
| .agent/authored/f277-r6-ledger.md | +4/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r6-plan.md | +45/-0 | byte copy of payload plan.md |

Total insertions (numstat): 333. The block states no expected value for C1a (the count moves with
every edit to the block itself); 333 is well under the 500 cap.

### 1fc97d2f F277 R6 C1b: book round 5's PASS, register R-1014, and rewrite plan for round 6 (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +43/-0 | append payload decisions.md (DECISION F277 D6) |
| .agent/live_review.md | +4/-0 | append payload ledger.md (F277 R5 gate entry PASS-on-what-it-executed, plus the R-1014 registration) |
| .agent/plan.md | +23/-27 | rewrite := payload plan.md |

Total insertions (numstat): 70, matching the block's expected 70 exactly (`git commit`'s own
terminal summary printed 92/-49 due to rename detection on `.agent/plan.md`; the numstat reading
is the one DECISION F104 D1 fixes and the one used here).

### 196e4a3e F277 R6 C2: add the JSON envelope and the dispatch error boundary (C2)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/grouped.py | +47/-1 | bare `handler(args)` replaced by `_dispatch(handler, args, command_id, raw)`; new `_dispatch` wraps the call in `try`/`except (SystemExit, KeyboardInterrupt): raise`/`except Exception as exc` per DECISION F277 D6 |
| apps/cli/json_envelope.py | +98/-0 | new file: `SCHEMA_VERSION`, `RESERVED_KEYS`, `build_ok`/`build_error`/`emit_ok`/`emit_error`, `_reject_reserved`, `_write` |

Total insertions (numstat): 145, matching the block's expected 145 exactly.

### f88940cf F277 R6 C3: add the envelope and boundary tests, including the red proof (C3)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_json_envelope.py | +179/-0 | new file: `TestTheEnvelopeHasOneShape` (envelope shape/sorting/reserved-key tests) and `TestNoTracebackReachesTheOperator` (the Acceptance red proof — a real handler that raises) |

Total insertions (numstat): 179, matching the block's expected 179 exactly.

### e4119319 F277 R6 C4: amend T2_F277.md's T002 for DECISION F277 D6 (C4)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F277.md | +13/-3 | T002's paragraph restated: the boundary routes through `emit_error`/stderr and exits 1, with no claim of a project exception base; new amendment paragraph dated 2026-09-20 explaining why `Exception` is caught rather than a non-existent base, citing DECISION F277 D6 |

Total insertions (numstat): 13, matching the block's expected 13 exactly.

## External actions

- `git worktree add --detach .remedy-wt/f277-r6-g5 e4119319` — created for G5 at C4.
- `git worktree remove .remedy-wt/f277-r6-g5` — removed as G5's last action, after all five
  mutations were restored byte-identically (confirmed by sha256 on both touched files).
- No `gh` command was run. No pull request was opened (the block orders none).
- `git push -u origin feature/f277-machine-contracts` — run after this commit; its outcome is
  reported in the round report, not here, because it necessarily postdates this commit (item 31).

## Verification

G1 TRANSPORT AND STATE — all readings True.
- (a) 4 `.agent/authored/f277-r6-*` files compared byte-for-byte against their source payloads
  (`ledger.md`, `decisions.md`, `plan.md`, `block.md`): all 4 equal.
- (b) Byte forensics on the two appends, both at C1b (`1fc97d2f`):
  - `.agent/live_review.md`: reading (a) byte equality of `91034712` bytes (410263) plus
    `ledger.md` (8368) against the committed post (418631) — True. Reading (b) structural: after
    stripping the payload's leading separator newline, the payload splits into N=2 paragraphs (the
    F277 R5 gate entry, the R-1014 finding); the post file's LAST 2 blank-line-delimited units
    equal those 2 paragraphs in order — True. Negative control: a single bit flipped inside the
    first appended paragraph is rejected by BOTH readings (both False, as required).
  - `.agent/decisions.md`: reading (a) byte equality of `91034712` bytes (1771575) plus
    `decisions.md` (3274) against the committed post (1774849) — True. Reading (b) structural: the
    payload splits into N=6 paragraphs (heading, CONTEXT, CHOSEN, ALTERNATIVES, the
    feature-file-amendment paragraph, REVERSE); the post file's LAST 6 units equal those 6
    paragraphs in order — True. Negative control: a single bit flipped inside the first appended
    paragraph is rejected by both readings (both False, as required).
- (c) `.agent/plan.md` at C1b equals `plan.md`'s bytes exactly (sha256
  `d1eb87045001157555de2cbde0c973de905f9f05fc882ccb28637a8896bbec1e` both sides) — True.
- (d) Open set by distinct id (`^- R-\d+ — ` minus `^Done: R-\d+ — `) in `.agent/live_review.md`:
  19 at `91034712` (R-1014 absent), 20 at C1b `1fc97d2f` (R-1014 present) — rise of exactly 1, as
  a register-only round must show.
- 23 boolean/count readings taken in total (4 in (a); 8 in (b) — 2 files × (reading-a, reading-b,
  negctrl-a, negctrl-b); 1 in (c); 2 counts plus 2 booleans in (d)), every relevant one True or
  matching its expected value.
- SEPARATELY (R-0954): the saved block reads 241 lines, sha256
  `efedf806b797709f9cdc9cfebc1dc481ea4f194a5b098d20339157598f466e19` — identical to the block's own
  PAYLOADS section reading.

G2 CODE TRANSPORT — at C4 (`e4119319`), `git rev-parse <commit>:<path>` for each path read:
```
apps/cli/json_envelope.py          cfa3aaff802f5228a23965b7a80c2faf2a449cb7   (matches block)
apps/cli/grouped.py                4009a41712a4315619b2c4a38030799347e25fdb   (matches block)
tests/cli/test_json_envelope.py    f631063418bfb8c625214863969e47a2d1c0db59   (matches block)
docs/roadmap/features/T2_F277.md   e709f9462ce09f1e7c21f8e9ee964d3e5da2d1f4   (matches block)
```
All four match the block's rehearsal-script table exactly — no scramble this round.
`git diff --name-only 1fc97d2f e4119319` reads:
```
apps/cli/grouped.py
apps/cli/json_envelope.py
docs/roadmap/features/T2_F277.md
tests/cli/test_json_envelope.py
```
Exactly those four paths, length 4, no extras.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py
tests/test_grouped_cli.py tests/test_command_catalog.py tests/docs
tests/orchestration/test_roadmap_index.py tests/orchestration/test_event_names.py
tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
tests/cli/test_golden_path.py` → `771 passed in 159.90s (0:02:39)`, exit code 0.

G4 LINT — `python3 -m ruff check apps/cli/json_envelope.py apps/cli/grouped.py
tests/cli/test_json_envelope.py` → `All checks passed!`, exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r6-g5` detached at `e4119319`, serial `python3 -B -m
pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py`:
- UNMUTATED CONTROL (first): `15 passed`, exit 0.
- (a) anchor `    _dispatch(handler, args, command_id, raw)` occurs 1 time in
  `apps/cli/grouped.py`. After replacing with `    handler(args)`: `3 failed, 12 passed`, exit 1,
  failing node ids `test_an_undeclared_exception_becomes_a_one_line_message`,
  `test_under_json_it_becomes_a_parseable_envelope`,
  `test_a_declared_project_error_is_caught_the_same_way` — matches expected exactly.
- (b) anchor `    print(json.dumps(envelope, sort_keys=True, default=str), file=stream)` occurs 1
  time in `apps/cli/json_envelope.py`. After replacing with
  `    print(json.dumps(envelope, default=str), file=stream)`: `1 failed, 14 passed`, exit 1,
  failing node id `test_every_level_is_sorted_so_two_runs_are_byte_comparable` — matches expected
  exactly.
- (c) anchor `    clash = [k for k in RESERVED_KEYS if k in payload]` occurs 1 time in
  `apps/cli/json_envelope.py`. After replacing with `    clash = []` plus
  `    _unused = [k for k in RESERVED_KEYS if k in payload]`: `2 failed, 13 passed`, exit 1,
  failing node ids `test_a_payload_may_not_overwrite_the_envelope[schema_version]` and
  `test_a_payload_may_not_overwrite_the_envelope[ok]` — matches expected exactly (both parameters
  of that test).
- (d) anchor `    _write(build_error(error, message, **payload), sys.stdout)` occurs 1 time in
  `apps/cli/json_envelope.py`. After replacing `sys.stdout` with `sys.stderr`: `5 failed, 10
  passed`, exit 1, failing node ids include `test_failure_goes_to_stdout_not_stderr` (plus three
  other tests that read `capsys.readouterr().out` and now see the empty stream, and one boundary
  test whose JSON parse now fails on empty stdout) — `test_failure_goes_to_stdout_not_stderr` named
  among the failures as required.
- (e) anchor the three lines `    except (SystemExit, KeyboardInterrupt):` /
  `        raise` / `    except Exception as exc:  # noqa: BLE001 - the whole point is the
  catch-all` occurs 1 time (as one contiguous block) in `apps/cli/grouped.py`. After replacing with
  the single line `    except BaseException as exc:  # noqa: BLE001 - the whole point is the
  catch-all`: `2 failed, 13 passed`, exit 1, failing node ids
  `test_a_handler_that_exits_deliberately_is_not_rewritten` and
  `test_a_keyboard_interrupt_is_not_reported_as_a_crash` — matches expected exactly. No narrower
  mutation was tried this round; the block's note that the narrower drop-only-the-re-raise variant
  stayed green in the reviewer's own rehearsal is recorded as context, not re-tested here.
- No mutation stayed green this round. Each was restored byte-identically before the next.
  Post-restoration sha256: `apps/cli/grouped.py`
  `8aa67baef4897fd1eb40d34be447ca5b2b5d9344904d634d2eaaabdd303fe4d4`, `apps/cli/json_envelope.py`
  `3787135c9d3c7b9f551964de41675d1641fad1275e1417aa32f4f865f3e5dc90`, both matching the committed
  (`e4119319`) blobs exactly. The final unmutated control re-run read `15 passed`, exit 0. The
  worktree was removed; `git worktree list` afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f277-r6-dry`, and the two pre-existing job worktrees, and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

20 findings open by distinct id in `.agent/live_review.md` as of C1b/C4 (up from 19 at `91034712`
by exactly 1: `R-1014`, registered this round and left OPEN — no `Done:` paragraph was written for
it, per the block's instruction that its repair belongs to F277's closure-sequence consolidation
pass).

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 241 lines, sha256 match |
| Payload byte verification (4 state payloads + diff) | done | all 5 match block's stated lines/sha256 |
| C1a | done | 333 insertions (numstat), no cap breach |
| C1b | done | 70 insertions (numstat), matches expected 70 |
| R-1014 registration | done | registered by C1b in `.agent/live_review.md`; open count rose 19→20; stays OPEN by design (no `Done:` paragraph written) |
| C2 | done | 145 insertions (numstat), matches expected 145 |
| C3 | done | 179 insertions (numstat), matches expected 179 |
| C4 | done | 13 insertions (numstat), matches expected 13; T2_F277.md T002 amended per DECISION F277 D6 |
| G1 transport and state | done | all readings True; open-set 19→20 with R-1014 as required |
| G2 code transport | done | all four blob ids match the block's table; `diff --name-only` names exactly the four paths |
| G3 targeted suite | done | 771 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green both times; (a)-(e) all red naming the expected tests; byte-identical restoration |
| C5 (this handoff + push) | done | handoff rewritten per template; push follows this commit |
| G6 push and tree | done | reported in round report (necessarily postdates this commit) |

## Authored-text proofs

The four `.agent/authored/f277-r6-*` files (C1a) were compared disk-to-disk against their source
payloads under `.remedy-wt/f277-r6-payloads/` and all four read byte-equal (G1 reading (a)). The
two record appends (`.agent/live_review.md`, `.agent/decisions.md`) and the plan rewrite
(`.agent/plan.md`) at C1b were verified byte-exact against `91034712` bytes plus payload (G1
reading (b)/(c)). The code diff's four applied paths were verified against the block's
rehearsal-script blob-id table at C4 (G2), all four matching. No other reviewer-authored text was
applied this round.

## Deviations & assumptions

- **G1(b)'s structural reader, method stated for the record.** The block specifies the mechanism
  ("splits the post file on blank lines", N counted from the payload after treating its leading
  newline as a separator, not a paragraph) without naming an exact split regex. The worker's
  implementation: strip exactly one leading `\n` from the payload, then split on runs of one-or-more
  blank lines (`\n\n+`) for both the payload and the post file, filtering empty units. This produced
  N=2 for `ledger.md` and N=6 for `decisions.md`, both of which are the visibly correct paragraph
  counts by eye (confirmed against the Read tool's rendering of each payload), and both readings
  agreed with reading (a) and correctly rejected the negative control. Recorded here as an
  assumption rather than a deviation, since no ambiguity changed any reported outcome.
- No other deviation. Every payload was applied byte-exact (verified pre- and post-commit); the
  code diff was applied via `git apply --include=...` in the three ordered slices and never
  retyped; every gate ran for real with its output captured above; no gate went red; no ambiguity
  DECISION F277 D6 leaves unsettled was met.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
2. The review of round 6.
3. T003 — the `fail()` helper and the JSON gaps: a shared `fail(code, message, *, json_output)`
   replacing the `print(...); sys.exit(1)` pairs, one command group per commit and only for groups
   that survive F261; the three commands that accept `--json` and ignore it fixed; the
   read-only-without-`supports_json` set emptied, asserted by a catalog test.
4. Operator questions open: 1
