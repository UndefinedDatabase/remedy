── STEP CLOSE/1 — F112 round 27 ────────────────────────────────
Goal: Fix the evidence-packager verification-run contract (operator
ruling, 2026-09-04): `output_hash` is ALWAYS `sha256` of the exact
`stdout_summary` bytes as stored, in both `job_evidence.py` call sites
and in `manual_attestation.py`; `job_evidence._scrub_paths` catches
non-repo/non-home absolute paths via the shared, already-accepted
scrubber. Book round 26's verdict and register one new finding first.

Bundle:
1. C0a/C0b — save this block verbatim (transport proof).
2. C1 — append RECORD26 (below) to `.agent/live_review.md`: books round
   26's PASS verdict, registers finding `R-0793`.
3. C2 — apply PLAN27 (below) to `.agent/plan.md` (whole-file replace).
4. C3 — fix `packages/orchestration/job_evidence.py`:
   a. Add `from packages.common.path_redaction import scrub_paths as
      _shared_scrub_paths` near the existing imports (top of file, with
      the other `packages.orchestration.*` imports — placement is the
      worker's call, PEP 8 order).
   b. Replace `_scrub_paths` (currently `job_evidence.py:1643-1655`) so
      its body, AFTER the existing `abs_repo`/`home` relativization
      (unchanged, keeps the "rootdir: ." form), returns
      `_shared_scrub_paths(text)` instead of `text`. Do not delete the
      repo-root/`$HOME` step.
   c. In `_default_verification_runner` (currently
      `job_evidence.py:1658-1708`): build the FINAL `stdout_summary` by
      scrubbing the full raw `stdout` first, THEN truncating to the last
      2000 characters (`_scrub_paths(stdout, repo)[-2000:]`, not the
      current `_scrub_paths(stdout[-2000:], repo)` — order matters, a
      path straddling the truncation cut must not survive). Apply the
      same scrub-then-truncate order to `stderr_summary` (keep its
      existing 1000-character length). Compute `output_hash` as
      `hashlib.sha256(stdout_summary.encode("utf-8",
      errors="replace")).hexdigest()` over that FINAL, already
      scrubbed-and-truncated `stdout_summary` string — not over the raw
      `stdout` as today.
5. C4 — fix `_run_verifications`'s normalization loop (currently
   `job_evidence.py:1737-1781`): after computing `_stdout_summary =
   str(r.get("stdout_summary", "") or "")[-2000:]` (unchanged), delete
   the caller-supplied-hash handling (`_output_hash = str(r.get(...))`,
   the `"sha256:"` prefix strip, and the `if not _output_hash:` guard)
   and replace it with an UNCONDITIONAL recomputation:
   `_output_hash = hashlib.sha256(_stdout_summary.encode("utf-8",
   errors="replace")).hexdigest()` (module already imports `hashlib` at
   `job_evidence.py:14`; the loop's own local `import hashlib as
   _hl_norm` becomes dead and should go with it). A caller-supplied
   `output_hash` is NEVER kept — it no longer describes the stored
   bytes once truncation may have changed them.
6. C5 — fix `packages/orchestration/manual_attestation.py`'s
   `_vt_run_v11` (currently lines `182-221`): import `scrub_paths` from
   `packages.common.path_redaction` (module already imports `hashlib` at
   its own top, confirm and reuse). Build `stdout_summary` as
   `scrub_paths(str(run.get("stdout_summary", "") or
   ""))[-2000:]` (scrub the full string, then truncate — same order as
   C3c). Delete the caller-supplied-hash handling (`output_hash =
   str(run.get(...))`, the `"sha256:"` strip, the `if not output_hash:`
   guard) and replace with an UNCONDITIONAL `output_hash =
   hashlib.sha256(stdout_summary.encode("utf-8",
   errors="replace")).hexdigest()`.
7. C6 — red proofs, new file
   `tests/orchestration/test_job_evidence_verification_contract.py`:
   (a) a synthetic pytest-shaped stdout string longer than 2000 chars
   (embed a real multi-line pytest transcript, not a repeated filler
   character, so scrubbing has real path text to act on) passed through
   `_default_verification_runner` via an injected `runner=` callable is
   NOT needed here — call `_scrub_paths`/the hash arithmetic path
   directly by constructing a run dict through `_run_verifications` with
   an injected `runner` lambda returning `{"stdout_summary": <the long
   string>, "output_hash": "deadbeef" * 8, ...other required keys...}`
   and assert the RETURNED run's `output_hash ==
   hashlib.sha256(returned_run["stdout_summary"].encode()).hexdigest()`
   — i.e. the same equality `build_review_manifest.py:2267` checks, and
   assert the deliberately-wrong injected `"deadbeef"*8` hash was
   DISCARDED, not kept; (b) call `_scrub_paths` (job_evidence) directly
   with the literal string `"platform linux -- Python 3.10.12,
   pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python3"` and assert
   `"/usr/bin/python3"` is absent from the result and `"python3"` is
   present; (c) call `_scrub_paths` directly with the literal string
   `"5 +/- 2"` and assert the result is unchanged (R-0790 regression
   guard); (d) call `_vt_run_v11` (manual_attestation) with a `run` dict
   carrying a long `stdout_summary` containing the same
   `/usr/bin/python3` banner text and a deliberately-wrong `output_hash`,
   and assert both the scrub (no absolute path survives) and the hash
   equality (matches `hashlib.sha256(stdout_summary.encode()).hexdigest()`
   on the RETURNED, truncated `stdout_summary`) hold.
8. C7 — mutation red-proof, run ONLY inside a disposable `git worktree`
   (G5; never the primary checkout): temporarily revert C3c's ordering
   (compute `output_hash` from the pre-truncation/pre-scrub `stdout`
   again, i.e. the OLD order) and confirm test (a) from C6 goes RED;
   restore immediately after recording the red result, remove the
   worktree, and confirm `git status --porcelain` is empty in the
   PRIMARY checkout throughout (it never touched it).
9. Handback — completion report + rewrite `.agent/handoff.md`
   (session continues; do not name a soft-limit banner — the operator's
   ruling above is this feature's rule-6 resolution, already booked in
   RECORD26 at C1).

Change: `packages/orchestration/job_evidence.py`,
`packages/orchestration/manual_attestation.py`,
`tests/orchestration/test_job_evidence_verification_contract.py` (new),
`.agent/live_review.md`, `.agent/plan.md`, `.agent/authored/f112-r27.md`
(new), `.agent/last_block.md`, `.agent/handoff.md`. Nothing else.

Constraints:
- Do not touch `docs/roadmap/features/T3_F112.md`,
  `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`,
  `.agent/decisions.md`, `.agent/candidates.md`,
  `.agent/prose_slips.md` this round — closure lands in a later round
  once the evidence job and zip are confirmed clean.
- Do not rebuild the evidence job or the review zip this round — that is
  round 28, after this round's own gates are independently re-verified.
- No `# removed` comments, no backwards-compat shims for the old
  caller-supplied-hash behavior — nothing in this repository's own
  `_default_verification_runner`/`_run_verifications`/`_vt_run_v11`
  callers relies on `output_hash` surviving unchanged (grep
  `tests/` and `packages/` for `output_hash=` call-site literals before
  editing, to confirm no caller depends on the OLD raw-stdout hash
  value; report the grep result in the completion report even if empty).
- `hashlib` import: `job_evidence.py` already imports it at module level
  (`job_evidence.py:14`); do not re-import inside a function after C4's
  cleanup. Check whether `manual_attestation.py` already imports
  `hashlib` at module level before adding a second import.
- Every commit stays under 500 changed lines (AGENTS.md); split C3-C6 if
  needed, but keep the four fixes and the four-part red-proof test in as
  few commits as cleanly separates them logically (a fix commit is not
  required to be one-file-one-commit).

Done when:
- `python3 -m pytest tests/orchestration/test_job_evidence_verification_contract.py -q`
  — all new tests pass, RED under the C7 mutation, GREEN restored after.
- `python3 -m pytest tests/orchestration/test_job_evidence.py -q` — no
  regression.
- `python3 -m pytest tests/orchestration/test_review_verification_tests_strict.py -q`
  — no regression.
- `python3 -m pytest tests/orchestration/test_failure_postmortem.py -q`
  — no regression (shares `packages/common/path_redaction` with the new
  `job_evidence._scrub_paths` delegation).
- `python3 -m pytest tests/cli/test_golden_path.py -q` — canary, every
  round.
- `python3 -m ruff check packages/orchestration/job_evidence.py packages/orchestration/manual_attestation.py tests/orchestration/test_job_evidence_verification_contract.py`
  — clean.
- `git status --porcelain` — empty at handback.
- `.agent/live_review.md` reproduces at exactly `2328447` bytes
  immediately after C1 (pre-append `2324181` + 1 + RECORD26's `4265`
  bytes), and RECORD26 extracted from the committed authored file is a
  byte-exact suffix.
- `.agent/plan.md` reproduces byte-identical to PLAN27 (`2337` bytes,
  no trailing newline, `## Goal`/`## Next Steps` each exactly once,
  `wc -l` under 50) after C2.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD26 sha256=4b46f53311cc1df61bacde454b575e507859401e2de781f62ddf23b7207ed8a6 ---
Gate: F112 R26 — the round 26 handoff entry. VERDICT PASS, over the range `138f616e..ee4b9a22` plus the handback commit `ade5abd4`, independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r26.md` and `HEAD:.agent/last_block.md` both print blob `42a613fc8c867eb3566e71bb41e4154286b58c33`, reproduced directly; `sha256sum .agent/authored/f112-r26.md` reproduced `84424ad7677f5a8be08f0fe9d0df189d5a30ebf11032c079ed40fcb6d485f94e`, `wc -c` reproduced 20490. THE PLAN HELD: `.agent/plan.md` reproduced at 42 lines, `## Goal` and `## Next Steps` each present exactly once, the file ends WITHOUT a trailing newline (last byte `2e` = `.`). THE RECORD APPEND HELD: `.agent/live_review.md` reproduced at 2324181 bytes, matching the round's own pinned post-append figure exactly. NO CODE CHANGED: `git diff --stat 138f616e..ee4b9a22 -- packages/ apps/ tests/ docs/` reproduced empty. `git status --porcelain` reproduced empty. Round 26 correctly filed the amend0827 rule 6 scope report (26 rounds, over the 25-round soft limit) and, per G8, deferred the `BLOCKED_EVIDENCE` fix to the operator rather than guessing. THE OPERATOR HAS NOW RULED (2026-09-04): the `BLOCKED_EVIDENCE` root cause is CONFIRMED, not merely suspected. Two independent contract defects live in shared evidence-packaging infrastructure, neither specific to F112's own task-splitting code: (1) `R-0792` (registered round 26) — `output_hash` is computed over raw/full text while `stdout_summary` is stored scrubbed-and-truncated, so the two can essentially never agree, which is why every run in `evidence/current/verification_tests.json` fails and cascades into `evidence_valid=false`; the same defect is independently present in `packages/orchestration/job_evidence.py`'s `_run_verifications` normalization loop (keeps a caller-supplied `output_hash` after re-truncating the summary) and in `packages/orchestration/manual_attestation.py`'s `_vt_run_v11` (same truncate-keep-foreign-hash pattern, with NO path scrubbing applied at all). (2) `R-0793` (registered below, new) — `job_evidence._scrub_paths` only relativizes the repo root and `$HOME`; it does not catch other absolute paths such as pytest's own platform-banner entry `/usr/bin/python3`, which trips the review manifest's absolute-path scan independently of the hash defect. The operator has selected option (a) from round 26's own proposal: F112's closure continues on ITS OWN round budget, no second STATUS line is opened, and this operator ruling itself is the scope-report resolution amend0827 rule 6 requires — nothing below proceeds on the reviewer's own authority ahead of it, and it did not. `git status --porcelain` immediately before this round's C1 was staged: empty.

- R-0793 — Medium, `JOB_EVIDENCE._SCRUB_PATHS` ONLY RELATIVIZES THE REPO ROOT AND `$HOME`; A THIRD-PARTY ABSOLUTE PATH SURVIVES AND TRIPS THE REVIEW MANIFEST'S ABSOLUTE-PATH SCAN. Found by the operator (2026-09-04), confirmed by the reviewer directly against `packages/orchestration/job_evidence.py:1643-1655`. ROOT CAUSE: `_scrub_paths` does `text.replace(abs_repo + "/", "").replace(abs_repo, ".")` then `text.replace(home, "~")` and returns — no general absolute-path reduction. A pytest stdout banner line such as `platform linux -- Python 3.10.12, pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python3` keeps `/usr/bin/python3` verbatim in the stored `stdout_summary`, which `scripts/build_review_manifest.py`'s absolute-path scan then flags (`runs[i].stdout_summary carries a local absolute path`), contributing to `gate_matrix` failure independently of `R-0792`. FIX (ordered below): `_scrub_paths` delegates to the already-accepted, already-tested `packages/common/path_redaction.scrub_paths` (F007's implementation, reused by F010) after its own repo-root/`$HOME` relativization, and `manual_attestation._vt_run_v11` routes its `stdout_summary` through the same shared scrubber, which it currently does not call at all. CONFIRMED NOT A REGRESSION RISK to the existing `R-0790` "+/-" non-match guard: `packages/common/path_redaction.py`'s own `ABS_PATH_RE` already excludes a bare-punctuation tail by construction (`/(?=[\w.~/])` lookahead), independently re-read by the reviewer at `path_redaction.py:36`.
--- END RECORD26 ---

--- BEGIN PLAN27 sha256=9a4814afc259d1c937c7475fb56480ab4fcc1ebcd667694ba5cdf47ca05194e6 ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green.
Round 26 hit the amend0827 rule 6 soft limit (26 rounds) and filed a
scope report on the review-zip `BLOCKED_EVIDENCE` blocker. The operator
ruled 2026-09-04: the root cause is CONFIRMED (R-0792 output_hash/
stdout_summary contract defect, R-0793 `_scrub_paths` absolute-path gap,
both in shared evidence-packaging infra, neither F112-specific), and
F112's closure continues on its own round budget, no second STATUS line.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 27 fixes the evidence-packager verification-run contract per the
operator's ruling: `output_hash` is always sha256 of the exact stored
`stdout_summary` bytes (`job_evidence.py`'s `_default_verification_runner`
and `_run_verifications`'s normalization loop, `manual_attestation.py`'s
`_vt_run_v11`), and `job_evidence._scrub_paths` delegates to
`packages/common/path_redaction.scrub_paths` for non-repo/non-home
absolute paths. Four red proofs plus one mutation red-proof, all in a
disposable worktree.

## Next Steps

- Round 28: reviewer books round 27's verdict (`Done: R-0792`,
  `Done: R-0793` if PASS), rebuilds F112's closure evidence job and
  review zip, confirms `PACKAGE_STATUS=READY_FOR_REVIEW` /
  `EVIDENCE_AUTHORITATIVE=true` by reading `.review_zip_manifest.json`
  from inside the built zip, not from builder stdout.
- Round 29: closure sequence — STATUS `[x]`, README capability sync,
  `self_use_queue` SU-007 `consumed_by=F112`, final `.agent/` state,
  closure commit, PR opened (not merged that round).
- Round 30: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule.

## Risks

- R-0784, R-0767 (both OPEN, unrelated to F112) carry forward undecided.
- The `scrub_paths` delegation must not regress the R-0790 "+/-"
  non-match guard; the mutation proof below exists to catch exactly that.
--- END PLAN27 ---
