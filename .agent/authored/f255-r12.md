── STEP R12 — F255 Teacher role ───────────────────────────────
Goal:        Persist the R11 verdict to the finding ledger and advance the plan.
             This round BUILDS NOTHING: the session that reviewed R11 reached its
             limit, and a PASS that lives only in a chat window is a verdict this
             project cannot audit later (DECISION F085 D9).

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             record the R11 verdict · C3 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r12.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source file
             and NO test file is touched this round. These paths are PRESENT at
             the base `da8c2e3f` and must stay untouched:
             `packages/orchestration/teacher_qa.py`,
             `tests/orchestration/test_teacher_qa.py`,
             `packages/orchestration/teacher_narration.py`,
             `apps/cli/commands/teach_cmd.py`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r12.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r12.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all
   rule that the `.agent/plan.md` update is the FIRST substantive commit of a
   round with substance to record.
4. THIS ROUND CONTAINS NO FROM/TO PAIR and creates no file outside `.agent/`, so
   no containment reading and no FROM-zero count is owed (§4.9, R-0207).
5. THE LEDGER APPEND IS BLANK-SEPARATED. RECORDR11 at C2 is appended preceded by
   exactly one blank line (R-0578). This round registers NO finding and resolves
   none: the registered count stays 181 and the resolved count stays 3.
6. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
7. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
8. `git status --porcelain` is EMPTY after every commit. No worktree is created.
9. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R12
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R12: a RECORD round. It persists the R11 verdict to `.agent/live_review.md` and
advances this plan, and it builds nothing — the session that reviewed R11 reached
its limit, and a verdict that lives only in a chat window is a verdict this
project cannot audit.

## Next Steps
1. R13 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and spend recorded under the role name `teacher`.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- R13 IS WHERE THE COST STORY IS PROVEN OR LOST. Nothing built so far spends a
  token; R13 makes the first teacher model call, and its spend must land under
  the role name `teacher` or DECISION F255 D3 is unmet.
- THE LEDGER'S ONE ROW IS A TASK RUN. `token_ledger.record_call` is documented
  as one row per finalized task run, keyed `<job_id>:<task_id>`, and a teacher
  question is neither. R13 must settle that shape before it writes a row.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own.
<<<END PLAN255R12
<<<SLICE RECORDR11
Gate: R12 — the R11 entry. R11 PASSED with NO finding against its work and none against its block. Every gate the R11 block ordered was RE-EXECUTED by the reviewer over `c6c6fb08..da8c2e3f` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r11.md`, the committed `.agent/authored/f255-r11.md` at `153b78fd` and the committed `.agent/last_block.md` at `b9b1ce9d` are byte-EQUAL at sha256 d4e511dd4060b29e26f1331ee6eeb0c888abec01e04fe7f3681aea4fae07f5de over 31058 B and 490 lines, the digest stated at delegation. FOUR SLICES, a count the reviewer took from its own ordered extraction of the committed blob, agreeing with the worker's independent count: PLAN255R11, RECORDR10, TEACHQA, TEACHQATEST, and NO slice is a FROM or a TO — the round contained no pair, so no containment reading and no FROM-zero count was ordered, owed or reported anywhere in it. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `948f57de` byte-equals PLAN255R11 at sha256 a8d22168cfc33e52a9f488082670cb24348bb203802b2aaef1fa84313057fda5 over 2350 B and 42 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and it is the first commit after the two block-save commits. THE LEDGER APPEND IS PREFIX-CLEAN: the blob at `c6c6fb08` is a byte-exact prefix of the blob at `8271d828` with a 5659 B two-line remainder equal to one newline followed by RECORDR10, an independent paragraph split of the `8271d828` blob yields 199 units whose LAST unit is RECORDR10 byte for byte at newline-INCLUDED sha256 98999ada6035883610f0e52c99835ce7c0446602b5f95b7248d0049b9c8a3d73 and newline-EXCLUDED sha256 cf9e5c517b2643978a81b74e3fd3324ee82266c2c87fffc307f4f46ac60cfcf7, and a one-character mutant of the expected remainder is REJECTED by both readings while the real blob is accepted by both. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at BOTH `c6c6fb08` and `8271d828`; `Gate: R11 — the R10 entry.` occurs 1x, sits last among the eleven lines beginning `Gate: R`, and all eleven header keys are distinct. THE TWO FILES WERE CREATED, NOT EDITED, and each is the authored bytes: `packages/orchestration/teacher_qa.py` and `tests/orchestration/test_teacher_qa.py` are both ABSENT at `c6c6fb08` under `git ls-tree` and both PRESENT at `18083ea7`, and each byte-EQUALS its slice — 151 lines at sha256 abe69cac625362f6067a2e491ced9b6a613cab7c293d2ce0831e905adc126d09 and 113 lines at sha256 208a9417619372ca27d1d07fa1aa0b034c99eb3ad87a15809f06f6c34c00f063, numstat 151/0 and 113/0. STAGE 2'S DETERMINISTIC HALF HOLDS THE THREE PROPERTIES IT WAS BUILT FOR, re-measured by the reviewer rather than read from the report: the suite exits 0 at 19 passed, and in a subprocess with `socket.socket` replaced by a raising stub the module assembles a context, labels every fact with one of `ledger` / `code` / `concept`, groups the prompt under those three headings with each source's honesty rule beside it, and returns a claim set IDENTICAL across all three levels while the depth instruction differs — the acceptance rule that the dial changes depth and not facts, observed rather than asserted. ITS ZERO-TOKEN CLAIM IS STRUCTURAL, not a promise: an AST read of the committed module shows its only imports are `__future__`, `collections.abc`, `dataclasses`, `typing` and `packages.orchestration.teacher_narration`, it calls `open` nowhere, and no network- or process-capable module is among them. THE FIVE RED CONTROLS BEHIND G7 WERE RUN BY THE REVIEWER BEFORE DELEGATION, in a disposable worktree since removed: letting the level leak into `claim_set` gives 2 failed / 17 passed, dropping the source label from the prompt gives 2 failed / 17 passed, building a code fact with no code supplied gives 5 failed / 14 passed, raising on an unknown level gives 1 failed / 18 passed, and dropping the Stage 1 pointer from the refusal gives 1 failed / 18 passed — so the labelling, the dial, the never-invent rule and the honest refusal are each a real tripwire, and the module restored byte-identically to 19 passed afterwards. THE NEIGHBOURS AND THE ROUND GATE HOLD, re-run serially in the primary checkout, never two pytest processes at once: the three repo-wide glob sweeps exit 0 at 132 passed — the same 132 as at the base, so the new file under `packages/` trips none of them — scoped ruff exits 0 at `All checks passed!`, Stage 1's own suite exits 0 at 38 passed, the four state-reader files exit 0 at 160 passed and the canary exits 0 at 42 passed. THE RANGE AND THE HISTORY HOLD: seven paths over six single-parent commits; per-commit insertions 490, 366, 15, 2, 264 and C4's own 33, every one under the 500 cap, with every `+/-` cell of the handback's `## Commits` table byte-identical to `git diff --numstat`; all six paths named untouched are PRESENT at the base and ABSENT from the range; zero marker lines in any written file; no trailing whitespace on any handback line; and the handback at `da8c2e3f` is 74 lines carrying all seven mandated headings in the template's order, within the 100-line allowance its six-commit table earns. C4'S OWN REFLOG ENTRY IS MEASURED HERE, which is what R-0494 asks of the next gate: at `da8c2e3f` the round has made 6 commits and its reflog entries whose operation prefix reads exactly `commit` number 6, with 0 entries whose prefix contains amend, reset, rebase or cherry. ONE DECLARED DEVIATION IS WORTH KEEPING, and it is a worker CORRECTING ITSELF: the worker's first G5 script mislabelled its two newline conventions, because the `re.split` it used retained the document's trailing LF, and it reported the paragraph reading as REJECTING the real blob. It re-measured with an explicit line-wise splitter, reported both conventions correctly, and put only the corrected numbers in the handback while naming the error. The reviewer's own independent extractor reproduces the corrected values exactly. A round that catches its own instrument and says so is the behaviour this record exists to reward.
<<<END RECORDR11

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r12.md`, of `.agent/authored/f255-r12.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r12.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R12; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE R11 VERDICT RECORDED. C2 appends RECORDR11 preceded by exactly one blank
   line. Report the PREFIX property, the remainder's sha256, byte and line
   counts, and that the separator is present. Report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR11, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base and at C2, the registered count being lines matching
   `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `: the
   reviewer measured 181 / 3 / 178 / 0 at `da8c2e3f`, and C2 owes the same four,
   because a `Gate:` paragraph adds neither kind of line. Report that
   `Gate: R12 — the R11 entry.` occurs 1x, is the LAST line beginning `Gate: R`,
   and repeats no header key.
G6 THE ROUND GATE. This round rewrites `.agent/` state and nothing else, so the
   four state-reader files gate alongside the canary. Run them serially in the
   PRIMARY checkout, never two pytest processes at once, and report the exact
   command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `da8c2e3f` in the primary checkout.
G7 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only da8c2e3f..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table (checklist item 28). C3's own cell and the
   complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601),
   AND NEITHER IS A TOTAL FOR THE ROUND (R-0605): report the count of this
   round's reflog entries whose OPERATION PREFIX — the text before the first
   colon of `git reflog --format=%gs` — reads exactly `commit`, TOGETHER WITH
   the commit it was taken at and the number of commits the round has made AT
   THAT MOMENT, and state that those two numbers are equal. State no total: C3
   is unwritten when this text is composed, so its entry cannot be counted here
   and the reviewer measures it at the next gate (R-0494). Report also the count
   whose prefix contains `amend`, `reset`, `rebase` or `cherry`, which must be 0.
G8 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
   `.agent/handoff.md` at C3. Every count must be 0.
G9 THE PUSH. After C3, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 9).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C3 bundle, the `## Commits` table
             G7 pins, and one LINE per gate rather than its transcript (R-0582).
             Its `## Next` section names the next session's FIRST action as
             Phase 1 rule 1, the `.agent/STOP` re-read, and its SECOND as R13,
             which finishes T004 — `remedy teach ask` on the CLI over
             `teacher_qa.build_teacher_context`, the teacher model call, the
             honest refusal with no model configured, and spend under the role
             name `teacher`. It states that R11 PASSED and that its verdict is
             now ON DISK at C2, that R12 itself awaits review, and that there is
             no open pull request. Full transcripts go in the round report,
             never in the file. The handback carries this Fortschritt line
             verbatim (R-0418):
             Fortschritt: ~70 % (T001, T002 and T003 COMPLETE · T004 half done —
             the grounding sources, the level dial and the small context are
             built, red-proofed and REVIEWED · the teacher model call, the
             integration gate and closure remain) — Schätzung
──────────────────────────────────────────────────────────────
