# Handoff — F112 Prompt budget per task class, round 26 (session-ending handoff: book RECORD25, register R-0792, NO code changes)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-25 carried forward unresolved — "6 (or 7)") ·
round 26 · rounds so far 26.

**SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.** Round 26
is the 26th delegated round on this feature, which has now REACHED AND
PASSED the amend0827-process-diet rule 6 soft limit of 25 rounds per
feature (the alternative "7 sessions" leg of that same limit is not
separately resolvable given the "6 or 7" ambiguity above, but the round
count alone is unambiguous and sufficient to trigger the obligation on
its own). Per that rule, this handoff carries a SCOPE REPORT instead of
more work:

- **What is finished.** F112's own product code is complete and green:
  T001 (per-class cap config, validation, floor + shared class
  vocabulary), T002 (compiler cap enforcement + `cannot_fit` arithmetic),
  T003/T003b2a/T003b2b2a/T003b2b2b1/T003b2b2b2/T003c (the decision
  wiring, dispatch-loop integration, `TaskEntry.files_hint`/`inputs`/
  `task_class` round-trips) — all per
  `docs/roadmap/features/T3_F112.md`'s task slicing and Built State
  section. Of the six closure preconditions this repository's closure
  protocol requires, FIVE are satisfied. `R-0790` (the `ABS_PATH_RE`
  false positive on a punctuation-only commit-subject tail) is fixed,
  mutation-red-proofed and independently re-verified (F112 R24/R25).
  `R-0791` (a whitespace-only transport defect in
  `tests/orchestration/test_failure_postmortem.py`) is fixed and
  independently re-verified (F112 R25). This round additionally books
  round 25's PASS verdict and registers one further finding, `R-0792`
  (below) — real, confirmed, but explicitly NOT shown to bear on the
  remaining blocker.
- **What is missing.** Closure precondition/algorithm step 2 — the
  mandatory review-zip build to a commit-ready, authoritative package —
  is BLOCKED. The zip now builds (exit 0, a real archive, a verified
  SHA-256) with R-0790's specific `ReviewSubjectError` crash gone, but it
  packages as `PACKAGE_STATUS=BLOCKED_EVIDENCE` /
  `EVIDENCE_AUTHORITATIVE=false`. Two full investigation passes (F112
  R25's own worker, then the R25 gate's independent reviewer
  re-verification) have NOT isolated a confirmed root cause: every
  individual gate file read directly out of the packaged zip via
  `zipfile` reads clean, so the failure is somewhere in the
  `package_status` decision logic itself (seven booleans plus
  `_check_bundle_integrity`, `scripts/build_review_manifest.py:3290-3296`
  and `:3323-3325`) rather than in any gate's own JSON. Full detail is in
  RECORD25 below and in this file's Verification section. Closure
  (STATUS `[x]`, README capability sync, `scripts/self_use_queue.json`
  SU-007 `consumed_by=F112`) cannot proceed while this precondition is
  unmet.
- **Proposal to the operator** (documented only; NOT executed on this
  session's own authority, per amend0827 rule 6): the `BLOCKED_EVIDENCE`
  defect lives entirely inside shared evidence/packaging infrastructure
  (`scripts/build_review_manifest.py`, `packages/orchestration/
  job_evidence.py`) rather than in any F112-specific code path, and
  nothing about it is unique to this feature's own task-splitting logic.
  Two options, per the rule's own wording:
  (a) **Split remaining scope off as a DECISION** — record that F112's
  own product code is complete and closure is deferred pending a
  separately-scoped investigation into the review-zip packaging defect,
  picked up with a fresh round budget rather than continuing to spend
  F112's own count against it; or
  (b) **Split into two STATUS lines** — keep F112's STATUS line pointed
  at its now-complete code, and open a second, differently-scoped STATUS
  line for the review-zip/evidence-packaging `BLOCKED_EVIDENCE`
  investigation, since a defect in shared packaging machinery is plausibly
  a blocker for OTHER features' closures too, not only F112's, and a
  feature-scoped round budget is an awkward fit for a cross-cutting
  infrastructure bug. This session recommends (b) as the better shape
  given where the defect actually lives, but leaves the choice to the
  operator, exactly as amend0827 rule 6 requires.

**A separate, mechanical problem in this round's own step block is
declared here per constraint 1** (apply byte-for-byte, declare rather
than silently correct): constraint 4's own closing bullet is internally
contradictory — it first states the SITZUNGS-LIMIT banner is "NOT owed
here (this is not a soft-limit round-count situation — 26 rounds is
under the 25-round soft limit's...)" (a factually false premise: 26 is
not under 25, it is over it), then immediately breaks off with "actually
reconfirm" and states the correct rule that the round count is what
governs. This handoff follows the block's own final, corrective clause
(round count ≥ 25 → name it plainly, apply the scope-report obligation)
rather than its earlier, self-contradicted premise, since the corrective
clause is both later in the text and arithmetically the only one of the
two that is true.

## Range

`138f616e..ee4b9a22` (base is F112 R25's handback commit; this handoff
itself lands as commit C3 on top of `ee4b9a22`).

## Commits

### 39fd60a1 F112 R26 C0a: save the round 26 step block verbatim to .agent/authored/f112-r26.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r26.md` | 236/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 97f955d8 F112 R26 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 175/263 | Byte-identical mirror of the authored file (whole-file overwrite; numstat reflects a partial-line-overlap diff against the prior round's block content, not a size mismatch). Confirmed with `git rev-parse HEAD:.agent/authored/f112-r26.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id, `42a613fc8c867eb3566e71bb41e4154286b58c33`, re-confirmed at the current HEAD (`ee4b9a22`) after C1/C2 landed. |

### 1704be71 F112 R26 C1: append RECORD25 to live_review.md (books R25 PASS, registers R-0792)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 4/1 | Appended RECORD25 via `content_bytes + b"\n" + RECORD25_bytes` (one-newline formula), extracted programmatically from the committed authored file. RECORD25 carries one internal blank line (Gate paragraph / `R-0792` finding paragraph), preserved exactly. |

### ee4b9a22 F112 R26 C2: apply PLAN26 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 22/20 | Whole-file replacement with PLAN26, extracted programmatically from the committed authored file, not retyped. No trailing newline. |

4 commits, 437 insertions total across C0a-C2 (largest single commit
236, well under the 500 cap; no oversize declaration needed — and every
one of these is a whole-file `.agent/**` state-file save exempt from the
churn reading regardless). This handback is commit C3 (per the block's
own numbering) — its own diff is the `.agent/handoff.md` rewrite only,
exempt from the churn reading as a single-state-file save.

## External actions

None yet at the time this file is written. `git push -u origin
feature/f112-prompt-budget-per-task-class` runs after this commit lands;
its outcome is reported in the completion report per the write-once rule
(not re-written into this file). No PR created, nothing merged, per
constraint 6.

## Verification

**G1 TRANSPORT** — sha256 of the committed `.agent/authored/f112-r26.md`:
`84424ad7677f5a8be08f0fe9d0df189d5a30ebf11032c079ed40fcb6d485f94e`, length
**20490 bytes**. `git rev-parse HEAD:.agent/authored/f112-r26.md` and
`git rev-parse HEAD:.agent/last_block.md` BOTH print
`42a613fc8c867eb3566e71bb41e4154286b58c33` — ONE blob id, confirmed
immediately after C0b and re-confirmed at the current HEAD. PASS.

**G2 THE PLAN** — PLAN26 extracted by delimiter from the committed
authored file (2006 bytes) compared byte-for-byte against the written
`.agent/plan.md` at C2: **equal**. `wc -l .agent/plan.md` = **42** (under
50). File ends WITHOUT a trailing newline (confirmed: last byte is
`.`). `## Goal` count = **1**. `## Next Steps` count = **1**. (`##
Current Step` and `## Risks` also each occur exactly once, matching the
file's required shape.) PASS.

**G3 THE RECORD APPEND** — RECORD25 extracted from the committed
authored file measured **7531 bytes**, matching the block's own pinned
figure exactly. `.agent/live_review.md` measured **2316649 bytes**
immediately before the append (matches the block's pinned pre-C1 figure
exactly, and matches this file's own last-committed size from round 25's
handback). Arithmetic: `2316649 + 1 + 7531 = 2324181` — matches the real
post-append size exactly, confirmed directly, and matches the block's
own predicted total exactly. Old-file-is-prefix check (first 2316649
bytes of the new file compared byte-for-byte against the pre-C1 file,
read from the prior commit): **True**. Post-append file still ends
WITHOUT a trailing newline: **True**. The seam reads
`...attempting anything.\nGate: F112 R25...` — exactly one newline
between the old tail and the new record, no extra blank line, and
exactly one blank line survives INSIDE the appended record between its
Gate paragraph and its `- R-0792 —` finding paragraph (confirmed: zero
occurrences of a triple newline anywhere in the appended span). NEGATIVE
CONTROL: flipping the single last byte of the post-append file breaks
the byte-for-byte match between the file's tail and the extracted
RECORD25 slice (confirmed False where the unmutated check reads True),
so the equality check is sensitive rather than vacuous. HEADER SHAPE:
lines matching `^Gate: F\d+ R\d+ — ` — before C1 **272**, after **273**.
Lines matching `^Gate: F112 R25 — ` — before **0**, after **1**. Lines
matching `^- R-0792 — ` — before **0**, after **1**. OPEN SET recomputed
mechanically directly against `.agent/live_review.md`: registered
(unique `^- R-\d+` ids) — before **352**, after **353**. `Done:`
(unique `^Done: R-\d+` ids, DISTINCT from the raw `Done:` LINE count) —
before **72**, after **72**. One verification note earned its own
sub-check here: a naive raw-line count of `^Done:` reads **74**, not
72, because two ids (`R-0721`, `R-0725`) each carry a SECOND `Done:`
paragraph from an earlier correction round — the block's own "72" figure
is the UNIQUE-id reading and is confirmed correct once de-duplicated;
this is a verification detail, not a deviation from the block, since the
block's own arithmetic already used the correct reading. Open total
(registered minus unique done) — before **280**, after **281**. MOVED
exactly as the block predicted. `git status --porcelain` immediately
before C3 was staged: **empty**. `git diff --stat 138f616e..ee4b9a22 --
packages/ apps/ tests/ docs/`: **empty** — no file under any of those
four trees appears anywhere in this round's four commits. PASS, no
deviation.

## Authored-text proofs

Both reviewer-authored texts applied this round were extracted
PROGRAMMATICALLY from the committed `.agent/authored/f112-r26.md` (never
retyped) and compared disk-to-disk against the file each was applied to:

- **RECORD25** (7531 bytes) — the bytes appended to `.agent/live_review.md`
  at C1 are byte-identical to the extracted slice; confirmed by direct
  tail comparison (see G3 above).
- **PLAN26** (2006 bytes) — the bytes written to `.agent/plan.md` at C2
  are byte-identical to the extracted slice; confirmed by direct
  whole-file comparison (see G2 above).

## Deviations & assumptions

1. **The constraint-4 self-contradiction on the SITZUNGS-LIMIT banner**,
   declared in full in the Session section above: the block's own text
   asserts both "not owed" and a false premise ("26 is under 25") before
   correcting itself mid-sentence. Resolved by following the block's own
   later, arithmetically-true correction. Not a registered finding
   (nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is
   affected; this is reviewer/worker-prose territory per
   amend0827-process-diet rule 2) — logged here per constraint 1's own
   instruction to declare rather than silently resolve.
2. **No code file anywhere was touched**, exactly as ordered: `git diff
   --stat 138f616e..ee4b9a22 -- packages/ apps/ tests/ docs/` is empty
   (G3 above). No evidence job was re-run, no zip was rebuilt, no fix was
   attempted for `BLOCKED_EVIDENCE` or for `R-0792` — all per constraint
   4's explicit prohibition on guessing at a fix this round.
3. **No new `R-` id was minted for `BLOCKED_EVIDENCE` itself.** Only
   `R-0792` (the independently-confirmed `output_hash`/`stdout_summary`
   mismatch, on its own terms) is registered this round, exactly as
   RECORD25 and the block's constraint 4 both specify.
4. **`.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T3_F112.md` were NOT touched**, per constraint 5.
5. **The "6 (or 7)" session-number ambiguity from round 20 is carried
   forward unresolved**, not invented or silently picked one way — the
   round count (26, unambiguous) is what this handoff relies on to
   trigger the soft-limit obligation, precisely because the session count
   is not resolvable from the record as it stands.
6. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a, re-confirmed at current HEAD |
| C1 append RECORD25 (books R25 PASS, registers R-0792) | done | byte length matched pinned figure exactly (7531); arithmetic, prefix, no-trailing-newline, header/open-set counts, and a negative control all confirmed; open set correctly MOVED (280→281) |
| C2 apply PLAN26 | done | byte-equal, 42 lines (under 50), no trailing newline, `## Goal`/`## Next Steps` present exactly once each |
| C3 this handoff | done | comprehensive session-ending handoff per docs/agents/handback_template.md and self_drive_protocol.md's "Ending a session"; scope report included per the soft-limit trigger |
| G1 transport | done | blob ids match, sha256 + length reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | done | arithmetic matches; open set correctly MOVED; negative control confirmed sensitive |
| RECORD25 booked | done | applied verbatim at C1 |
| R-0792 registered | done | applied verbatim at C1, as part of RECORD25's own text |
| PLAN26 applied | done | applied verbatim at C2 |
| Constraint-4 SITZUNGS-LIMIT self-contradiction | deviated | declared in Session section and Deviations item 1; resolved by following the block's own corrective clause |
| No code/docs/tests/packages change | done | confirmed empty diff over those four trees between 138f616e and ee4b9a22 |
| No new fix or zip rebuild attempted | done | per constraint 4's explicit prohibition |

## Next

This round issues no verdict on its own work — that is the reviewer's,
per the block's own instruction. No `Done: R-0790`, `Done: R-0791`, or
any `Done:`/`Gate:` line for THIS round's own work is written here; the
reviewer books this round's own verdict, if any, into
`.agent/live_review.md` in the first commit of whatever round follows.

**Next expected action, in order:**

1. **The operator decides the scope-report proposal above** (split as a
   DECISION, or split into two STATUS lines) before continuing — this is
   the amend0827 rule 6 obligation this handoff exists to raise, and
   nothing below should proceed on the session's own authority ahead of
   that decision.
2. Once that is settled, whichever session picks this up next should
   read `scripts/build_review_manifest.py` roughly lines 3150-3340 in
   FULL — further back than either the round-25 worker or this round's
   reviewer got to — to find exactly which of the seven `package_status`
   booleans (`evidence_valid`, `alignment_ok`, `containment_ok`,
   `gate_matrix["ok"]`, `fv_ok_for_ready`, `git_status_ok`,
   `tt_ok_for_ready`) or `_check_bundle_integrity` actually reads false
   AT BUILD TIME, and whether that reading happens before or after the
   "Evidence refresh completed for staged copy" console line — printing
   each boolean's value at the point of the `package_status` decision (a
   one-line debug print, or a direct call to the relevant helper
   functions against the SAME evidence dir still on disk,
   `remedy-job-evidence-f112-closure/`, job id `cee206d7881e4699`) will
   answer this far faster than re-reading the packaged JSON files after
   the fact, which is what led both this round's and round 25's
   investigation to first (correctly) rule out every individual gate
   file without yet finding which upstream boolean actually flips.
3. Do NOT attempt another zip rebuild or another fix before that reading
   is done — the cause is not yet confirmed and guessing again would
   repeat exactly the mistake G8 exists to prevent.

Open findings count: **281** (353 registered, 72 `Done:`) — MOVED from
280 by this round's C1 append (G3 above), because this round both books
RECORD25's PASS verdict and registers `R-0792` in the same commit.

Before starting the next round: re-check `.agent/STOP` from disk (absent
as of this round, confirmed at both the round's start and immediately
before this handback, per constraint 2). Phase 0's state probe (git
status, branch, log, `gh pr list`) should be re-run fresh at that
round's own start, per `docs/agents/self_drive_protocol.md` — not
assumed carried over from this handoff.
