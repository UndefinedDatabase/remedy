# Handoff — F112 Prompt budget per task class, round 27 (evidence-packager verification-run contract fix: R-0792, R-0793)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-26 carried forward unresolved — "6 (or 7)";
see Deviations item 1 below) · round 27 · rounds so far 27.

This round is NOT a fresh loop-session bootstrap — it is a direct
continuation of round 26's own session, executing the operator's ruling
that round 26's handoff (and RECORD26, booked at C1 below) already
carries. Per the session-numbering rule
(docs/agents/planner_reviewer_prompt.md §1 item 3: "this session is that
[carried] number plus one, carried forward in every handback of this
session"), a number only increments at a fresh bootstrap. This is not
one, so the number is unchanged from round 26 — and round 26 itself never
resolved which of 6/7 that carried number is, so this handoff makes the
same honest choice rounds 25 and 26 made rather than guessing.

## Range

Review of `ade5abd4..HEAD` (base is F112 R26's handback commit).

## Commits

### dbba6ca9 F112 R27 C0a: save the round 27 step block verbatim to .agent/authored/f112-r27.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r27.md` | +208/-0 | transport proof — verbatim copy of the supplied step block |

### f9f65916 F112 R27 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +189/-217 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 734ecde8 F112 R27 C1: append RECORD26 to live_review.md (books R26 PASS, registers R-0793)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-1 | append RECORD26 (books round 26's PASS verdict, registers `R-0793`) |

### 091ca97b F112 R27 C2: apply PLAN27 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +31/-26 | whole-file replace with PLAN27 |

### 42eb4342 F112 R27 C3: job_evidence _scrub_paths delegates to shared scrubber, hash follows final summary
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_evidence.py` | +16/-4 | `_scrub_paths` delegates to `packages.common.path_redaction.scrub_paths` after its own repo-root/`$HOME` step (R-0793); `_default_verification_runner` scrubs-then-truncates `stdout_summary`/`stderr_summary` and computes `output_hash` over the FINAL summary, not raw stdout (R-0792) |

### 82c20785 F112 R27 C4: _run_verifications always recomputes output_hash
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_evidence.py` | +6/-7 | normalization loop deletes the caller-supplied-hash handling (`sha256:` strip, empty-hash fallback, dead local `import hashlib as _hl_norm`) and unconditionally recomputes `output_hash` from the final truncated `_stdout_summary`, using the existing module-level `hashlib` import |

### f39ecfef F112 R27 C5: manual_attestation _vt_run_v11 scrubs and rehashes stdout_summary
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/manual_attestation.py` | +9/-7 | imports `scrub_paths`, scrubs `stdout_summary` before truncating (this call site previously applied NO scrubbing at all), unconditionally recomputes `output_hash` from the final summary using the module's existing `hashlib` import |

### 7a1e3095 F112 R27 C6: red proofs for the verification-run contract (R-0792, R-0793)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_evidence_verification_contract.py` | +134/-0 | new file — four red proofs: (a) `_run_verifications` discards a wrong caller-supplied `output_hash` and recomputes from the returned truncated `stdout_summary`; (b) `job_evidence._scrub_paths` redacts a third-party absolute path (pytest platform banner); (c) `_scrub_paths` leaves `"5 +/- 2"` unchanged (R-0790 guard); (d) `manual_attestation._vt_run_v11` scrubs and rehashes, discarding a wrong caller-supplied hash |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) |

## External actions

- `git worktree add .remedy-wt/f112-r27-mutation HEAD --detach` — succeeded, detached at `7a1e3095`.
- `git worktree remove .remedy-wt/f112-r27-mutation --force` — succeeded, removed after the mutation red-proof (see Verification below).
- `git push -u origin feature/f112-prompt-budget-per-task-class` — see Verification below (run after this handback commit, outcome recorded there per the block's own ordering; this file is written once, so the literal push transcript is reported to the operator in the completion message rather than edited back into this section after the fact).

## Verification

Real, trimmed transcripts for every gate this round's block ordered, run in the PRIMARY checkout unless marked worktree:

```
$ python3 -m pytest tests/orchestration/test_job_evidence_verification_contract.py -q
....
4 passed in 0.23s

$ python3 -m pytest tests/orchestration/test_job_evidence.py -q
........................................................................ [ 77%]
.....................                                                    [100%]
93 passed in 17.21s

$ python3 -m pytest tests/orchestration/test_review_verification_tests_strict.py -q
........................                                                 [100%]
24 passed in 0.36s

$ python3 -m pytest tests/orchestration/test_failure_postmortem.py -q
........................................................................ [ 51%]
.....................................................................    [100%]
141 passed in 0.45s

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 20.70s

$ python3 -m ruff check packages/orchestration/job_evidence.py packages/orchestration/manual_attestation.py tests/orchestration/test_job_evidence_verification_contract.py
All checks passed!

$ git status --porcelain
(empty)
```

`.agent/live_review.md` reproduced at exactly `2328447` bytes immediately
after C1 (`2324181 + 1 + 4265`, RECORD26 extracted from the committed
authored file, sha256 `4b46f53311cc1df61bacde454b575e507859401e2de781f62ddf23b7207ed8a6`
matching the marker's stamped hash exactly); the pre-append content is a
byte-exact prefix of the post-append content; the file still ends WITHOUT
a trailing newline (`b'.'`).

`.agent/plan.md` reproduced byte-identical to the extracted PLAN27 span:
`2337` bytes both sides, sha256 `9a4814afc259d1c937c7475fb56480ab4fcc1ebcd667694ba5cdf47ca05194e6`
matching the marker's stamped hash; `wc -l` reads `47` (under 50);
`## Goal`/`## Next Steps` each appear exactly once; no trailing newline.

**Constraints grep (before editing), reported per the block's own
instruction — result NOT empty, but none of the hits are the three call
sites this round touches or depend on the OLD raw-stdout hash surviving
unchanged:**

```
$ grep -rn "output_hash=" packages/ tests/
packages/orchestration/local_candidate_generator.py:557 (unrelated field, candidate-generator record)
packages/orchestration/local_candidate_generator.py:774 (unrelated field, prompt_hash/output_hash pair)
packages/orchestration/builder_bridge.py:130 (unrelated: sha256 of raw builder output, different contract)
tests/orchestration/test_builder_eval.py:434,448,637,649,661 (unrelated: BuilderEvalResult fixture field)
packages/orchestration/builder_eval.py:130,486 (unrelated: BuilderEvalResult plumbing)
packages/orchestration/builder_models.py:119,130,140,151,163 (unrelated: BuilderEvalResult dataclass field)
tests/orchestration/test_f018_authority_integration.py:1755,1765 (tests scripts.build_review_manifest.validate_verification_tests directly — the CONSUMER of the contract this round fixes, not job_evidence/manual_attestation; unaffected by this round's change, still passes: test_output_hash_matches_stdout constructs its own already-consistent hash/summary pair)
tests/orchestration/test_f018_package_pipeline_e2e.py:33 (unrelated: output_hash=None default fixture field)
```
None of these depend on `_default_verification_runner`, `_run_verifications`,
or `_vt_run_v11` returning an unchanged caller-supplied hash.

**C7 mutation red-proof — run ONLY inside a disposable `git worktree`
(`.remedy-wt/f112-r27-mutation`, off `7a1e3095`, removed after), never the
primary checkout. `git status --porcelain` in the primary checkout was
confirmed empty before the worktree was created and again after it was
removed.**

Deviation from the block's literal C7 wording, declared here in full (see
Deviations below for the justification): the block's own text says to
"revert C3c's ordering" and expect test (a) to go RED. Tried literally
first — reverting `_default_verification_runner`'s scrub-then-truncate
order back to `_scrub_paths(stdout[-2000:], repo)` / `hashlib.sha256(stdout...)`
— and reran the full contract test file:

```
$ find . -name __pycache__ -exec rm -rf {} +   # cache purge
$ python3 -B -m pytest tests/orchestration/test_job_evidence_verification_contract.py -v
... 4 passed in 0.27s
```

All 4 stayed GREEN — the literal C3c revert does not reach test (a) at
all, because test (a) injects a `runner=` callable into `_run_verifications`,
which bypasses `_default_verification_runner` entirely (`r = runner(cmd) if
runner is not None else _default_verification_runner(cmd, repo)`). Restored
C3c (`git checkout -- packages/orchestration/job_evidence.py`), confirmed
clean, then mutated the ACTUAL logic test (a) exercises — C4's unconditional
recompute in `_run_verifications` — back to the pre-fix caller-supplied-hash
acceptance:

```
$ python3 -B -m pytest tests/orchestration/test_job_evidence_verification_contract.py -v
FAILED ...TestRunVerificationsOutputHashContract::test_wrong_caller_supplied_hash_is_discarded_and_recomputed
AssertionError: assert 'deadbeef...deadbeef' == '3c5960619e93...962a368458e10'
1 failed, 3 passed in 0.29s
```

Exactly test (a) went RED, the other three stayed GREEN — matching the
block's predicted shape (one targeted test red, the rest unaffected).
Restored (`git checkout --`), reran:

```
$ python3 -B -m pytest tests/orchestration/test_job_evidence_verification_contract.py -v
... 4 passed in 0.32s
```

GREEN restored. As a second, unrequested-but-honest check of the R-0793
half of the fix (since the C7 wording named only the R-0792/C3c half),
also reverted `_scrub_paths`'s `return _shared_scrub_paths(text)` to
`return text` in the same worktree and reran:

```
$ python3 -B -m pytest tests/orchestration/test_job_evidence_verification_contract.py -v
FAILED ...TestScrubPathsCatchesThirdPartyAbsolutePaths::test_third_party_absolute_path_is_redacted
AssertionError: assert '/usr/bin/python3' not in ...
1 failed, 3 passed in 0.29s
```

Exactly test (b) went RED, the other three GREEN. Restored, reran GREEN
(4 passed). Worktree removed (`git worktree remove
.remedy-wt/f112-r27-mutation --force`); `git worktree list` afterward
shows only the pre-existing per-job worktrees from earlier rounds,
untouched; `git status --porcelain` in the primary checkout reproduced
empty throughout and after.

## Authored-text proofs

- `.agent/authored/f112-r27.md` (C0a): `sha256sum` of the source scratchpad
  file and the committed copy both read
  `60fd7980ad29045226901c0c8279bd2e74b3f9805bfa5898224a5f3b75ba219c`
  (16170 bytes, 208 lines) — identical.
- `.agent/last_block.md` (C0b): `git rev-parse HEAD:.agent/authored/f112-r27.md`
  and `git rev-parse HEAD:.agent/last_block.md` both print blob
  `e311d9295e87cbfe411f97f47e17907a33379e1e` — identical.
- RECORD26 (C1) and PLAN27 (C2): byte-exact, hash-verified as reported
  under Verification above.

## Deviations & assumptions

1. **Session-number ambiguity carried forward, not resolved.** Round 20's
   handoff introduced "SESSION 6 (or 7)"; rounds 21-26 all carried it
   forward without resolving it (round 26's own Session section: "Session
   continuing F112 (same numbering as round 24's handoff used)" — itself
   following round 25's identical dodge). This round makes the same
   choice for the same reason: which of 6/7 is correct depends on whether
   an actual fresh Claude Code session bootstrap occurred at some point
   between round 19 and round 20 — information not recoverable from git
   history, `.agent/live_review.md`, or any handoff, all of which were
   checked before writing this section. Per
   `docs/agents/planner_reviewer_prompt.md` §1 item 3, the number only
   increments at a fresh bootstrap; since this round is explicitly a
   continuation of round 26's own session (stated in this round's own
   task framing, not a guess), no increment is warranted here either way
   — the ambiguity is inherited unchanged, not manufactured by this round.
2. **C7 mutation target corrected from "C3c's ordering" to C4's
   unconditional recompute**, fully declared under Verification above
   with both the failed literal attempt (C3c revert leaves all 4 tests
   green — it is inert against test (a), which bypasses
   `_default_verification_runner` via an injected `runner=`) and the
   working mutation (C4's revert turns exactly test (a) red). This is a
   real, reproduced discrepancy in the block's own C7 wording — test (a)
   as the block itself specifies it (bundle item 7a) exercises
   `_run_verifications`'s hash-arithmetic contract (C4), not
   `_default_verification_runner`'s scrub/truncate ordering (C3c) — and
   is reported here rather than silently "corrected" without a trace,
   per the mutation-must-reach-the-test discipline. No block text was
   edited; only the worktree mutation target was chosen to be the one
   that actually reaches the test under proof.
3. **An extra, unrequested mutation check was run** (`_scrub_paths`
   reverted to `return text`) to independently confirm the R-0793 half of
   the fix is real, since the block's C7 item named only the R-0792/C3c
   mutation. This is additive verification, not a deviation from what was
   asked, but is declared here per the "any departure...even when correct"
   rule.
4. No candidate-generator, builder_eval, or builder_models `output_hash=`
   call site was touched — all are unrelated fields on different data
   shapes, confirmed by direct reading (see the constraints-grep report
   under Verification).

## Next

Round 28 (per PLAN27's Next Steps): the reviewer books this round's own
verdict (`Done: R-0792`, `Done: R-0793` if PASS) into
`.agent/live_review.md`, then rebuilds F112's closure evidence job and
review zip, confirming `PACKAGE_STATUS=READY_FOR_REVIEW` /
`EVIDENCE_AUTHORITATIVE=true` by reading `.review_zip_manifest.json` from
inside the built zip (not from builder stdout) — this is the first real
test of whether the R-0792/R-0793 fixes actually clear the
`BLOCKED_EVIDENCE` blocker that triggered this round's work in the first
place. This round does NOT write any `Done:`/`Gate:` line for its own
work — that is the reviewer's job in round 28, per the block's own
instruction and amend0827 rule 1.
