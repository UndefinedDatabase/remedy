── STEP R8 — F255 Teacher role ────────────────────────────────
Goal:        Register R-0605 against the R7 block, record the R7 verdict, and
             finish T001 by declaring the `teacher.model` config key with its
             pin in the SAME commit. T001 is complete when this round lands:
             the role name, the conventions document and the routing surface.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST, ahead of
             the ledger and ahead of the work · C2 register R-0605 · C3 record
             the R7 verdict · C4 the config key and its pin, together · C5 the
             handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r8.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `packages/orchestration/config.py` AND
                 `tests/orchestration/test_config.py` — ONE commit, both files,
                 because a declared key and the pin that freezes its spec may
                 never be separated (R-0151).
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base `3812d625` and must stay untouched:
             `packages/orchestration/role_config.py`,
             `packages/orchestration/role_conventions.py`,
             `docs/agents/teacher_conventions.md`,
             `tests/orchestration/test_role_conventions.py`,
             `docs/README.md`, `docs/roadmap/features/T5_F255.md`,
             `.agent/decisions.md`, `.agent/context.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r8.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r8.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST, as it did at R7. Findings R-0377, R-0491 and R-0548 are
   OPEN and all rule that the `.agent/plan.md` update is the FIRST substantive
   commit of a round with substance to record.
4. TWO PAIRS, AND THEIR SHAPES DIFFER. The reviewer ran the containment test
   over each before emission and quotes each result as the test printed it.
   PINFROM→PINTO: `TO contains FROM: True` — APPEND-shaped. CFGFROM→CFGTO:
   `False` — REWRITE. G7 orders the FROM-zero count for the REWRITE ONLY, and
   never for the append, whose FROM the applied file necessarily still carries
   (§4.9, R-0207).
5. THE KEY AND ITS PIN LAND IN ONE COMMIT. C4 changes two files at once for the
   R-0151 reason: `test_teacher_model_key_is_declared` asserts the spec's env
   var, type and default by EXPECTED LITERAL, so the pin without the key is RED
   and the key without the pin is unguarded. The reviewer measured the red —
   see G8.
6. EVERY FROM IS UNIQUE IN ITS TARGET. The reviewer measured both FROM texts at
   exactly 1 occurrence in their file at the base. Apply each by a count-checked
   replacement: assert the FROM occurs exactly once BEFORE replacing, and stop
   if it does not.
7. THE LEDGER APPENDS ARE BLANK-SEPARATED. R0605 at C2 and RECORDR7 at C3 are
   each appended preceded by exactly one blank line (R-0578). This round
   registers one finding and resolves none: the registered count moves 180 to
   181 and the resolved count stays 3.
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. NOTHING ELSE IS BUILT. No reader for the new key, no narration code, no CLI
   surface. The key is DECLARED here and first READ by T004; that is the design
   the slice states, not an omission.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
11. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran every destructive control G8 reports.
12. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R8
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
R8: register R-0605 against the R7 block, record the R7 verdict, and finish T001
by declaring the `teacher.model` config key with its pin in the same commit.
T001 is complete when this round lands.

## Next Steps
1. R9 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
2. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real. It is also the round that gives `teacher.model` its first
   reader.
3. The integration gate and the closure round follow T004, per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- THE NEW CONFIG KEY HAS NO READER UNTIL T004. That is deliberate and stated in
  the key's own description, so a later reader finds a decision rather than a
  forgotten wiring — but if T004 slips, the key ships unread and the feature
  file's T001 claim outruns the code.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- FIVE ROLE LISTS EXIST AND T001 TOUCHED TWO. DECISION F255 D1 rules that the
  CLI-override and token-cost lists are deliberately NOT extended.
<<<END PLAN255R8

<<<SLICE R0605
- R-0605 — Low — A GATE ORDERED A ROUND'S COMMIT COUNT AS AN EQUALITY THE HANDBACK COMMIT CANNOT REACH, SO THE PERMANENT RECORD UNDERSTATES ITS OWN ROUND BY ONE. G13 of the F255 R7 block, saved at `db54b5f2`, orders the reflog reported as two measured claims and requires the count of entries that produced a commit to "equal the number of commits the round makes". R7 makes SEVEN commits, and `.agent/handoff.md` at `3812d625` reads "entries of this round reading exactly `commit` = 6, equal to the 6 commits the round makes". THE GATE IS UNMEETABLE RATHER THAN THE WORKER CARELESS: that sentence lands in the handback which C5 itself writes, so at most six of the round's seven reflog entries can exist at the moment the text is composed, and a worker obeying the gate literally must either state a number it cannot yet observe or state the number it can. The same block carved C5 out of the OTHER half of the very same gate — "C5's own cell and the complete change set belong to the round report" — and left the reflog half uncarved, so one gate carried one carve-out where it needed two. THE PROPERTY THE GATE EXISTS TO PROTECT HOLDS, and was re-measured by the reviewer at `3812d625`: `git reflog --format=%gs` holds SEVEN entries for this round, every one reading `commit` in the operation prefix before the first colon, and ZERO whose prefix contains amend, reset, rebase or cherry — so no history was rewritten and the absence claim is true; only the count sentence is short by one. THE RECORD CONTRADICTS ITSELF, which is how a later reader meets it: the same handback's `## Commits` section tables six commits and then a seventh row for C5, and its item-status table lists seven items C0a through C5, all done. THE CLASS IS CHECKLIST ITEM 14 of docs/agents/planner_reviewer_prompt.md, "a per-commit gate names the commits it can honestly reach", whose own R-0489 instance is the same arithmetic one feature earlier — a handback that reported five insertion counts and called its range five single-parent commits while that range held six. NO DUPLICATE ID WAS MINTED, and the open set was searched for the DEFECT before this id was written, as item 30 requires: R-0494 is OPEN and covers the neighbouring problem that under self-drive a reading routed to the ephemeral round report dies with the session, which is an ABSENT reading rather than a false one; R-0601 is OPEN and covers the reflog universal quantified over entry TYPES, which is what G13's two-claim wording already fixed and is not a count at all. Neither describes a sentence that is false on disk, so this is a third symptom of item 14 rather than a second id for either. WHY LOW: no gate was weakened, no work is wrong, nothing consumed the number, and the round's real subject — a conventions document, its vocabulary and its pins — verified byte for byte. THE LANDED SENTENCE IS NOT REWRITTEN: item 20 rules that the counter-measure is a dated correction in NEW text and never an overwrite of the record, and this paragraph is that correction. COUNTER-MEASURE, applied by the block that carries this finding rather than merely described by it: a whole-round count gate names the commits it can reach — the ones BEFORE the handback commit — states the reading together with the commit it was taken at, and never states a total for the round; the handback commit's own contribution is measured by the reviewer at the next gate and recorded in that round's record paragraph, which is exactly what R-0494's counter-measure already established for insertion counts. G12 of this block orders that shape.
<<<END R0605

<<<SLICE RECORDR7
Gate: R8 — the R7 entry. R7 PASSED. One finding is registered this round, R-0605, against the R7 BLOCK's own gate wording and not against the round's work, which was clean; nothing is resolved. Every gate the R7 block ordered was RE-EXECUTED by the reviewer over `eb8aa9ae..3812d625` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r7.md`, the committed `.agent/authored/f255-r7.md` at `db54b5f2` and the committed `.agent/last_block.md` at `b208d57d` are byte-EQUAL at sha256 326180ada7d1cb7e65e5c19fc845ef7f77b8a37135dfdb1eb88265ca42414b6c over 29581 B and 445 lines, the digest stated at delegation. TWENTY-THREE SLICES, a count the reviewer took from its own ordered extraction of the committed blob rather than from the handback, and the worker's independent count agrees. THE PLAN LANDED FIRST, WHICH IS ITSELF THE FIX: `.agent/plan.md` at `cd2bc66c` byte-equals PLAN255R7 at sha256 6a5548d7a831748738fb707abe5396f856795cda9772dd5a95c35668faf42c8a over 2353 B and 42 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255; and `cd2bc66c` is the first commit of the round after the two block-save commits, so R-0377, R-0491 and R-0548 were obeyed rather than restated for the first time on this branch. THE LEDGER APPEND IS PREFIX-CLEAN: the blob at `eb8aa9ae` is a byte-exact prefix of the blob at `5f0ae785`, the 5720 B two-line remainder equals one newline followed by RECORDR6, and an independent paragraph split of the `5f0ae785` blob yields 194 units whose LAST unit is RECORDR6 byte for byte. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 180 registered / 3 resolved / 177 open / 0 line-anchored `Landed:` at BOTH `eb8aa9ae` and `5f0ae785`; `Gate: R7 — the R6 entry.` occurs 1x, sits last among the seven lines beginning `Gate: R`, and all seven header keys are distinct. THE SOURCE COMMITS WERE RECONSTRUCTED RATHER THAN READ: applying the ten authored pairs to the blobs at `eb8aa9ae` in the block's own order reproduces `packages/orchestration/role_conventions.py` and `tests/orchestration/test_role_conventions.py` at `349a458c` and `docs/README.md` at `3bffaaab` BYTE FOR BYTE, so no edit reached those files that the block did not order. The shapes held as declared: ENUMFROM→ENUMTO printed `TO contains FROM: True` and reads FROM 1x at BOTH ends, which is why no FROM-zero count was ordered or reported for it, while the nine REWRITE pairs each read FROM 1x then 0x and TO 0x then 1x. THE DOCUMENT IS THE AUTHORED BYTES AND IT FITS: `docs/agents/teacher_conventions.md` is ABSENT at `eb8aa9ae` and PRESENT at `349a458c`, byte-equal to the TEACHERDOC slice at sha256 f172231301d701fb7865bb320244668fa35c411a2d11fadf823beffee181e682 over 1982 B, 1972 characters and 46 lines, and `estimate_text_tokens` returns 493 against `CONVENTIONS_TOKEN_CAP` 800 — the character count and the token count both re-measured by the reviewer, and the character count differs from the byte count because the document holds exactly five non-ASCII characters, all of them em dashes, each costing three bytes and one character — the estimator divides CHARACTERS by four, so the byte count is not the number the cap is read against. THE SUITES WERE RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT, never two pytest processes at once: `tests/orchestration/test_role_conventions.py` exits 0 at 35 passed where the base measured 26, `tests/docs/` exits 0 at 295 passed, `python3 -m ruff check` over the two Python files C3 touches exits 0 at `All checks passed!`, the four state-reader files exit 0 at 160 passed, `tests/orchestration/test_role_config.py` exits 0 at 33 passed and the canary exits 0 at 42 passed. THE THREE RED CONTROLS BEHIND G9 WERE RUN BY THE REVIEWER BEFORE DELEGATION, in a disposable worktree since removed: deleting the document gives 7 failed / 28 passed, renaming its `## Isolation` heading gives 1 failed / 34 passed, and pushing it 4000 characters over the cap gives 5 failed / 30 passed — so the document's presence, its headings and its size are each a real tripwire rather than an unfalsifiable assertion. THE RANGE AND THE HISTORY HOLD: nine paths over SEVEN single-parent commits, per-commit insertions 445, 361, 14, 2, 58, 5 and C5's own 38, every one under the 500 cap, and every `+/-` cell in the handback's `## Commits` table byte-identical to `git diff --numstat`; all ten paths named untouched are PRESENT at `eb8aa9ae` and ABSENT from the range; zero lines beginning `<<<SLICE ` or `<<<END ` in any written file; and the handback at `3812d625` is 83 lines carrying all seven mandated headings in the template's order, inside the ≤100 its commit count earns. THE BASE RUFF READING WAS TAKEN BY A ROUTE THE PROTOCOL ALLOWS AND THE WORKER DECLARED IT: constraint 12 forbade a worktree, so the base half of G10 went through `ruff check --stdin-filename <real path> -`, which preserves the per-file-ignores the real path resolves, and the worker shipped a red control with it — two unused imports on stdin return exit 1 and 2x F401 — rather than letting a green reading stand unproven. That is checklist item 29's mechanism named and evidenced, and it is the correct answer to a gate this reviewer left without a stated route. THE ONE DEFECT IS THE BLOCK'S, IT IS R-0605, and it is registered above.
<<<END RECORDR7

<<<SLICE CFGFROM
        value_type=int,
        default=10,
    ),
    ConfigKeySpec(
        key="watchdog.no_progress_repeats",
<<<END CFGFROM

<<<SLICE CFGTO
        value_type=int,
        default=10,
    ),
    ConfigKeySpec(
        key="teacher.model",
        env_var="REMEDY_TEACHER_MODEL",
        description=(
            "Model for the teacher role (F255). The teacher reads and explains "
            "and never writes, so this key buys explanation quality and nothing "
            "else. Unset means the role resolves exactly like every other one. "
            "Stage 1 narration is deterministic and spends nothing, so nothing "
            "reads this key until the Stage 2 question path exists (T004) — a "
            "declared key with no reader yet, not a forgotten wiring."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="watchdog.no_progress_repeats",
<<<END CFGTO

<<<SLICE PINFROM
    def test_get_unknown_key(self):
        assert get_key_spec("nonexistent.key") is None
<<<END PINFROM

<<<SLICE PINTO
    def test_get_unknown_key(self):
        assert get_key_spec("nonexistent.key") is None

    # F255: the teacher's own routing surface. Pinned by EXPECTED LITERAL
    # because a test that reads the spec it is meant to freeze cannot fail.
    def test_teacher_model_key_is_declared(self):
        spec = get_key_spec("teacher.model")
        assert spec is not None
        assert spec.env_var == "REMEDY_TEACHER_MODEL"
        assert spec.value_type is str
        assert spec.default is None
<<<END PINTO

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r8.md`, of `.agent/authored/f255-r8.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r8.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R8; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 R-0605 REGISTERED AND R7 RECORDED. C2 appends R0605 and C3 appends RECORDR7,
   each preceded by exactly one blank line. For EACH of the two commits report
   the PREFIX property, the remainder's sha256, byte and line counts, and that
   the separator is present. For C3 report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR7, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base, at C2 and at C3: the reviewer measured
   180 / 3 / 177 / 0 at `3812d625`; C2 owes 181 / 3 / 178 / 0 and C3 the same,
   because a `Gate:` paragraph adds neither kind of line. Report that
   `- R-0605 — ` occurs 1x and that `Gate: R8 — the R7 entry.` occurs 1x, is the
   LAST line beginning `Gate: R`, and repeats no header key.
G6 THE FROM TEXTS WERE UNIQUE BEFORE THEY WERE REPLACED. For each of the two
   FROM slices report its occurrence count in its target file at the base
   `3812d625`. The reviewer measured each at exactly 1. A count other than 1
   stops the round.
G7 THE TWO PAIRS, BY THEIR OWN SHAPES. For the REWRITE pair CFGFROM→CFGTO
   report FROM's count at the base and at C4 and TO's count at both ends; it
   owes FROM 0x and TO 1x after C4. For the APPEND-shaped pair PINFROM→PINTO
   report FROM 1x at BOTH ends and TO 0x then 1x, and do NOT report a FROM-zero
   count for it: that count is unreachable by construction (§4.9, R-0207).
   PINTO is a CODE append that lands in the MIDDLE of its file, so neither the
   per-line count §4.9 writes for prose (R-0531) nor a whole-file PREFIX reading
   applies to it. The reviewer ran both before ordering anything: the prefix
   reading is FALSE by construction here, and the ordered line-by-line reading
   fails too, because git attributes the pair's blank separator to the END of
   the hunk while the slice carries it at the START — nine added lines either
   way, the same file, a different attribution. Report instead the
   RECONSTRUCTION, which fixes position and multiplicity together and does not
   depend on how a hunk is attributed: for EACH of the two files C4 touches, the
   blob at C4 byte-EQUALS the blob at the base with that file's single FROM
   occurrence replaced once by its TO. Report `git diff --numstat` for both
   files at C4.
G8 THE KEY IS DECLARED AND ITS PIN IS A TRIPWIRE. Report the exact command,
   exit code and tail of
     `python3 -m pytest tests/orchestration/test_config.py -q -rf`
   at C4. The reviewer measured exit 0 at 62 passed at the base and exit 0 at
   63 passed with both pairs applied — the one new case is
   `test_teacher_model_key_is_declared`. Report also, from a short `python3 -c`
   you run yourself, that `get_key_spec("teacher.model")` is not None and that
   its `.env_var`, `.value_type` and `.default` read `REMEDY_TEACHER_MODEL`,
   `str` and `None`. Do NOT run a mutation red-proof: the reviewer already ran
   three in a disposable worktree before emitting this block — deleting the
   whole `teacher.model` spec while the pin stands gives 1 failed / 62 passed at
   `tests/orchestration/test_config.py:78`, renaming the env var to
   `REMEDY_TEACH_MODEL` gives 1 failed / 62 passed at line 79, and giving the
   key a non-None default gives 1 failed / 62 passed at line 81 — and
   constraint 11 forbids you creating a worktree.
G9 RUFF, SCOPED TO THE TWO FILES C4 TOUCHES. Report the exact command, exit
   code and output of
     `python3 -m ruff check packages/orchestration/config.py tests/orchestration/test_config.py`
   at C4. The reviewer measured `All checks passed!` for those two paths at the
   base and again with both pairs applied, so a pre-existing error cannot be
   read as a new one (R-0364).
G10 THE NEIGHBOURS T001 ALREADY BUILT STAY GREEN. Report the exact command,
   exit code and tail of
     `python3 -m pytest tests/orchestration/test_role_config.py tests/orchestration/test_role_conventions.py -q -rf`
   at C4. The reviewer measured exit 0 at 68 passed with both pairs applied.
G11 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state, so the four state-reader files
   gate alongside the canary. Report the exact command, exit code and tail of
   each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `3812d625` in the primary checkout.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 3812d625..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the nine paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table (checklist item 28). C5's own cell and the
   complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601),
   AND NEITHER OF THEM IS A TOTAL FOR THE ROUND (R-0605): report the count of
   this round's reflog entries whose OPERATION PREFIX — the text before the
   first colon of `git reflog --format=%gs` — reads exactly `commit`, TOGETHER
   WITH the commit that count was taken at and the number of commits the round
   has made AT THAT MOMENT, and state that those two numbers are equal. Do NOT
   state a total for the round: C5 is not written when this text is composed, so
   its own reflog entry cannot be counted here, and the reviewer measures it at
   the next gate (R-0494). Report also the count whose prefix contains `amend`,
   `reset`, `rebase` or `cherry`, which must be 0. Read the prefix, never the
   whole line.
G13 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C3,
   `packages/orchestration/config.py` and `tests/orchestration/test_config.py`
   at C4, and `.agent/handoff.md` at C5. Every count must be 0.
G14 THE PUSH. After C5, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C5 bundle, the `## Commits` table
             G12 pins, and one LINE per gate rather than its transcript
             (R-0582). The LINE cap your commit count earns is the bound. Its
             `## Next` section names the next session's FIRST action as Phase 1
             rule 1, the `.agent/STOP` re-read, and its SECOND as R9, T002 and
             T003 together — Stage 1 narration over an enumerated event set and
             the behavioural read-only proof — and states that R8 awaits review
             and that T001 is complete. There is no open pull request. The full
             transcripts go in the round report you return, never in the file.
             The handback also carries this Fortschritt line verbatim, because
             with no relay you never see the operator brief that would otherwise
             state it (R-0418):
             Fortschritt: ~35 % (F086 merged · F255 claimed · six DECISIONs
             ruled · the spec written · T001 COMPLETE: the teacher has a role
             name, a reviewed conventions document, a capped prompt segment and
             its own model key · T002-T004 open) — Schätzung
──────────────────────────────────────────────────────────────
