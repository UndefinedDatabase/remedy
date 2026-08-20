── STEP R2 — F255 Teacher role ────────────────────────────────
Goal:        Register R-0601 and R-0602, record the R1 verdict so it is not
             stranded, and MEASURE the five seams F255 depends on into an
             inventory file — every claim carrying a citation that resolves at
             HEAD. Nothing is designed this round and nothing is built: R3 rules
             the shape once the ground is known. No source file, no test and no
             document under docs/ changes.

Bundle:      C0a save this block · C0b mirror it · C1 register R-0601 and
             R-0602 · C2 record the R1 verdict · C3 the inventory · C4 the
             plan · C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r2.md`
             C0b `.agent/last_block.md`
             C1  `.agent/live_review.md`
             C2  `.agent/live_review.md`
             C3  `.agent/f255_inventory.md`   (NEW FILE, worker-authored)
             C4  `.agent/plan.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base and must stay untouched: `hatch_build.py`,
             `pyproject.toml`, `README.md`, `docs/roadmap/STATUS.md`,
             `docs/roadmap/features/T5_F255.md`, `.agent/context.md`,
             `packages/orchestration/role_config.py`,
             `apps/cli/command_catalog.py`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r2.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r2.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. R0601, R0602 and RECORDR1 are APPENDS to
   `.agent/live_review.md`, PLAN255R2 is a WHOLE-FILE replacement of
   `.agent/plan.md`, and the inventory is a NEW file you author yourself. The
   reviewer ran the containment test over this block's slices before emission
   and found no pair to classify, so no FROM count is ordered anywhere below.
4. EVERY APPEND IS BLANK-SEPARATED. Each of R0601, R0602 and RECORDR1 is
   appended preceded by exactly one blank line (R-0578), copied from its
   extracted slice file and never retyped. Nothing already in that file is
   rewritten, reordered or deleted. The registered set moves by exactly +2 and
   the resolved set does not move at all.
5. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH. Nothing is fixed this
   round, only registered, recorded and measured.
6. THE INVENTORY IS MEASURED, NEVER RECALLED. This is the whole point of the
   round. Every factual claim in `.agent/f255_inventory.md` carries a
   `path:line` citation that you resolved AT HEAD by opening the file and
   reading that line — not from memory, not from a feature file, not from this
   block. Where the answer is that something does NOT exist, write it as an
   explicit absence: "Remedy deliberately does not X" is a first-class finding
   and is more valuable here than a plausible guess. Never invent a path to
   make an answer look complete; an honest ABSENT is what R3 needs.
7. NOTHING IS DESIGNED AND NOTHING IS BUILT THIS ROUND. You do not add a role,
   a config key, a CLI command, a test or a doc. If the measurement suggests an
   obvious fix, RECORD the suggestion in the inventory and leave the code alone
   — R3 rules the design as a DECISION and amends the feature file.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
10. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

The inventory answers these six questions, one `##` heading each, in this order.
Each answer is a short paragraph of prose plus a citation table whose rows are
`path:line` · symbol · one line of what it does. Quote the decisive source line
verbatim where a single line settles the question.

Q1 ROLE RESOLUTION. What role names does the vocabulary hold, where is that
   vocabulary declared, and what happens TODAY when a role outside it is
   resolved — warning, error, or silent default? Name EVERY file that carries
   an independent role list, because a fourth role must be taught to each one.
   Record whether the feature file's phrase "the same role_config mechanism as
   orchestrator/worker/reviewer" matches the names actually declared.
Q2 LEDGER EVENT VOCABULARY. Is there a CLOSED, enumerated vocabulary of run-log
   event names, or are event names free strings? Where is an event emitted and
   where, if anywhere, is its name validated? F255's registration names "stable
   ledger event vocabulary (Tier 2)" as a DEPENDENCY: record, measured, whether
   that dependency is satisfied today, and name any partial registries.
Q3 BUDGET POOLS. How is a token charge attributed to its spender, and does a
   "pool" concept exist in the code at all? Record the separation axis that
   actually exists, and where a budget LIMIT is expressed, so R3 can rule
   whether a teacher pool is a new value on an existing axis or a new axis.
Q4 ActionClass read_only. Where is `ActionClass` defined, what are its members,
   and what ENFORCES it — a runtime check on a code path, or a declaration
   checked only by tests? Name the enforcing code or record its absence.
Q5 THE WATCH PATH. Does `remedy do watch` exist? Does `remedy teach` exist?
   Record the nearest EXISTING read-only reader of a live run and the mechanism
   by which it stays isolated from the writer.
Q6 DOES `teacher` EXIST ANYWHERE? Search `packages/`, `apps/`, `tests/` and
   `scripts/` and report every hit, or report zero.

<<<SLICE R0601
- R-0601 — Low — A GATE ORDERING THAT EVERY REFLOG ENTRY OF A ROUND READ `commit:` CANNOT BE MET BY ANY ROUND WHOSE BUNDLE OPENS WITH THE OPEN PR GATE, AND THE HANDBACK THEN CARRIES THE OVER-SCOPED SENTENCE INTO THE PERMANENT RECORD. G12 of the F255 R1 block, saved at `903c00ff`, orders "that every `git reflog` entry of this round reads `commit:`" — wording carried across from the F086 R35 block, whose round performed no branch navigation at all. R1's own bundle opens with S0, which AGENTS.md defines as `gh pr merge`, `git checkout main`, `git pull --ff-only` and `git checkout -b`, so that round's reflog necessarily holds `checkout` and `pull --ff-only` entries and the ordered universal is unmeetable by construction. Re-measured by the reviewer at `6c47a490`: of the ELEVEN reflog entries R1 produced, SEVEN read `commit` and FOUR read `checkout` or `pull --ff-only`, so the sentence at line 49 of `.agent/handoff.md` is FALSE under its literal reading and true only under the narrower reading "the entries for this round's commits". The worker met the gate by DECLARING the imprecision in its round report rather than by amending C5 — an amend would itself have added a non-`commit` reflog entry and an eighth, unordered commit — which is the correct response, and the reason this is registered against the block's wording and never against the round. Nothing on disk is wrong: the property the gate exists to protect is the ABSENCE of history rewriting, and re-measured over those same entries BY THEIR OPERATION PREFIX — the text before the first colon of `git reflog --format=%gs`, which is the only place the operation appears — `amend`, `reset`, `rebase` and `cherry` each occur 0 times. The prefix reading is itself load-bearing: two of R1's commit SUBJECTS contain the word "reset", so a naive scan of the whole `%gs` line reports two false history-rewrite hits, and the reviewer's own first measurement did exactly that before being corrected. The counter-measure replaces one unmeetable universal with the two measurable claims it was reaching for, and the R2 block already carries them: every reflog entry that PRODUCED a commit of the round reads `commit`, reported as a count, and no entry of the round — navigation included — has a history-rewriting operation prefix.
<<<END R0601

<<<SLICE R0602
- R-0602 — Low — THE HANDBACK TEMPLATE'S 800-TOKEN HARD CAP HAS BEEN EXCEEDED BY EVERY ROUND FOR AT LEAST TWELVE ROUNDS, SO IT BINDS NOTHING AND NO ROUND HAS EVER BEEN FOUND AGAINST IT. `docs/agents/handback_template.md` states at line 14 "Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit LARGE case (P4 token thrift)". Measured by the reviewer over the twelve most recent commits that rewrote `.agent/handoff.md`, at the chars/4 estimate the worker itself used: EVERY ONE exceeds 800, from 1306 tokens at `3f154c6f` to 2983 at `6c47a490`, a band of 1.6x to 3.7x the cap, with the F086 R35 handback that this reviewer PASSED sitting at 2148. The line-count cap in the SAME document is meanwhile respected — R1's 67 lines sit inside the ≤100 allowance the template grants a table of more than five commits — so two caps in one file disagree about what the same artifact may contain, and only the token one is dead letter. It is registered rather than repaired because it is not this round's regression, it is not fixable by writing a shorter handback while the mandated content stays what it is, and choosing between the two coherent outcomes is an operator-visible DECISION under §4 item 7: either the cap is stale and is restated to a number the mandated sections can actually meet, or the mandated content shrinks and the template says which section gives way. R3 rules it alongside the F255 spec amendments. Until then no round should be failed against a number twelve consecutive rounds have ignored, and no handback should cite compliance with it.
<<<END R0602

<<<SLICE RECORDR1
Gate: R2 — the R1 entry. R1 PASSED. Every gate the R1 block ordered was RE-EXECUTED by the reviewer over `b35d350b..6c47a490` rather than read from the handback, and every one holds; two findings are registered this round, R-0601 against the block's own reflog wording and R-0602 against a template cap the whole project has outgrown, and NEITHER is a defect of the round's work. THE OPEN PR GATE RAN AS AGENTS.md ORDERS: `gh pr list` returned exactly one entry, #207 from `feature/f086-release-capability` into `main` and not a draft; `gh pr view 207` now reports `MERGED` at 2026-08-20T20:27:23Z with merge commit `b35d350b`; `git rev-parse main` and `origin/main` both read `b35d350b`; `git merge-base HEAD main` IS that commit, so feature/f255-teacher-role is cut from the merge and no commit of the round sits on `main`; and `gh pr list --state open` now returns the empty list. The merge was authorised because the reviewer watched CI run 32411743463 on `538323e0` to conclusion `success` with #207 MERGEABLE and mergeStateStatus CLEAN. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f255-r1.md`, the committed `.agent/authored/f255-r1.md` at `903c00ff` and the committed `.agent/last_block.md` at `d5437d29` are byte-EQUAL at sha256 c445fb0d6e9b45a98a5523c0fb35292be44289aa91c12dd72d19ca61e10e7d25 over 29472 B and 386 lines — the digest stated at delegation — and both commits carry the identical git blob `74f3dde6`. THE CLAIM IS A REWRITE THAT MOVED ONE LINE: in `docs/roadmap/STATUS.md` the FROM line reads 1x at `b35d350b` and 0x at `c4718364` while the TO line reads 0x then 1x, the containment test prints False so the REWRITE shape the block declared is the shape the slices have, and `git diff --numstat` for that file is `1 1`, so no other ledger line moved and F255 now reads `- [~]`. THE RESET CARRIED THE OPEN SET WITHOUT LOSING A BYTE, WHICH IS THE ROUND'S REAL RISK AND THE ONE R-0572 EXISTS FOR: measured by the reviewer independently of the worker's script, by a line scan alone, the base blob at `b35d350b` holds 182 registered, 7 resolved, 175 open and 0 `Landed:`, and the C2 blob at `7efd78aa` holds 176 registered, 0 resolved, 176 open and 0 `Landed:` — the reading a carry-forward of 175 plus one registration owes; the carried id sequence equals the base open sequence AS AN ORDERED LIST; none of the seven resolved ids leaked in; and `- R-0600 — ` occurs exactly 1x, last. THE CARRY IS VERBATIM UNDER A CONTROL THAT CAN ACTUALLY FAIL: all 175 carried paragraphs are EXACT ELEMENTS of the base record's 226-paragraph set, 175 matched of 175, and three negative controls — one paragraph truncated by 40 B, one word altered, one paragraph dropped — are each REJECTED. That control shape is load-bearing rather than ceremonial: the truncated paragraph IS still a substring of the base blob, so the containment form of the same check accepts it, which the reviewer confirmed by running both forms against the same mutant before the block was emitted. THE R35 ENTRY LANDED AS AN APPEND: the pre-C3 blob, 314805 B over 972 lines, is a byte-exact PREFIX of the post-C3 blob, 319613 B over 974 lines; the 2-line remainder is a blank line followed by RECORD35 at sha256 158079a7f686685eab8455d9d1c21db7a6ef4f01b25075d1cf01cd3a07275308 over 4808 B, separator PRESENT; an independent paragraph split yields 181 units whose LAST is exactly RECORD35, at sha256 818125f7f01a3a55 over 4807 B and 1 line with its trailing newline INCLUDED and at sha256 d336f5e06edd657a over 4806 B with it STRIPPED, both conventions given because R-0600 was registered for omitting exactly that; a one-byte mutant is REJECTED by both readings; and `Gate: R1 — the F086 R35 entry.` occurs 1x, is the only and therefore last line beginning `Gate: R`, with no header key repeated. THE STATE FILES ARE BYTE-EXACT AND SATISFY EVERY READER THE REVIEWER COLLECTED: `.agent/plan.md` at `7f1fc0e0` byte-equals PLAN255 at 40 lines, under the 50-line cap, with `## Goal` 1x, `## Next Steps` 1x and `F255` 3x; `.agent/context.md` at `c4718364` byte-equals CONTEXT255 with `## Active Branch` 1x, `feature/` 1x, `Steps` 1x, `F255` 1x and `pytest` 2x, and carries none of the eight stale strings the dashboard and test-runner contracts forbid; the reset record contains `Steps`. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT, never two pytest processes at once: the four-file state-reader selection exited 0 at `160 passed`, `tests/docs/` with `test_roadmap_index.py` exited 0 at `325 passed`, and the canary exited 0 at `42 passed`, each equal to the count measured at `538323e0` before the round began. THE RANGE IS WHAT THE HANDBACK DECLARES: seven paths over seven single-parent commits, every `+/-` cell of the `## Commits` table byte-identical to `git diff --numstat` at 386/0, 352/154, 28/27 with 1/1, 25/124, 2/0, 31/34 and C5's own 39/27 correctly routed to the round report rather than claimed inside itself; a maximum insertion column of 386, under the 500 cap; all seven paths the Change section names as untouched present at `b35d350b` and absent from the range; zero marker lines in each of the five files the round writes; and a handback of 67 lines, inside the ≤100 allowance its seven-commit table earns, carrying all seven mandated headings in the template's order. R1 IS NOT A TERMINATOR: R-0583 gives that carve-out to the round whose bundle creates the branch's pull request, and on this branch no pull request exists yet.
<<<END RECORDR1

<<<SLICE PLAN255R2
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to ledger events (Stage 1, deterministic
templates, zero tokens) and on-demand Q&A (Stage 2, through the teacher role's
own model) both work, the three grounding sources are never mixed silently,
teacher spend is its own budget pool in the F103 ledger, and the read-only
invariants hold under test.

## Current Step
R2: register R-0601 and R-0602, record the R1 verdict, and MEASURE the five
seams F255 depends on into `.agent/f255_inventory.md`. Nothing is designed and
nothing is built this round.

## Next Steps
1. R3 RULES THE SHAPE AS A DECISION and amends
   `docs/roadmap/features/T5_F255.md` with the Design, Task slicing, Acceptance
   and Do-not-touch sections its registration stub has never carried. R3 also
   rules R-0602, the dead token cap, per §4 item 7.
2. R3 MUST RULE ON EACH SPEC-VS-REALITY GAP R2 MEASURES, rather than building
   around it. A dependency the registration names but the code lacks is a
   planning decision, not a detail for a build round to improvise.
3. R4 ONWARD BUILDS THE T-SLICES that DECISION names, Stage 1 before Stage 2.

## Risks
- THE REGISTRATION MAY NAME GROUND THAT DOES NOT EXIST. F255 depends on a
  "stable ledger event vocabulary" and on the isolation rules of a `watch`
  command; R2 measures whether either is real before R3 designs on top of it.
- READ-ONLY IS AN INVARIANT, NOT AN INTENTION. If `ActionClass` read_only turns
  out to be declarative only, the teacher's hard invariant needs an enforcement
  seam that must be designed rather than assumed.
- THE THREE GROUNDING SOURCES ARE THE WHOLE FEATURE. A teacher that silently
  mixes ledger fact, workspace code and model knowledge is worse than no
  teacher, so their separation is a test obligation and not a prompt wish.
<<<END PLAN255R2

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r2.md`, of `.agent/authored/f255-r2.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Report the command that extracts each slice
   from the COMMITTED `.agent/authored/f255-r2.md` by its markers, and the
   sha256, byte count AND line count of each — every digest you state anywhere
   for an extracted region carries both counts and names its newline convention
   (R-0600).
G4 THE TWO FINDINGS REGISTERED. With `^- R-\d+ — ` as registered and
   `^Done: R-\d+ — ` as resolved, report both counts plus open and `Landed:` at
   the base and at C1. The reviewer measured 176 registered, 0 resolved, 176
   open and 0 `Landed:` at `6c47a490`; C1 owes 178 / 0 / 178 / 0. Report that
   `- R-0601 — ` and `- R-0602 — ` each occur exactly 1x, that each is preceded
   by exactly one blank line, and that the pre-C1 blob is a byte-exact PREFIX
   of the post-C1 blob with the remainder equal to the two slices in order.
G5 THE R1 VERDICT ENTRY. C2 appends RECORDR1 preceded by exactly one blank
   line. The pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; report the
   remainder's sha256, byte count and line count and that the blank separator is
   present. Report it a SECOND time by an independent paragraph-level split
   whose LAST unit is RECORDR1, giving that unit's sha256 under BOTH newline
   conventions with the byte count of each. Run a negative control — one
   character of the expected remainder mutated — and report that BOTH readings
   reject it. Report that `Gate: R2 — the R1 entry.` occurs exactly 1x, is the
   LAST line beginning `Gate: R`, and that no `Gate: R` header key repeats.
G6 THE INVENTORY'S CITATIONS RESOLVE AT HEAD. This is the round's central gate.
   Extract every `path:line` citation from `.agent/f255_inventory.md` with a
   script, and for each one report that the path is TRACKED at HEAD
   (`git ls-tree`) and that the file has at least that many lines. Report
   matched and total; they must be equal. Then run a NEGATIVE CONTROL: append a
   citation naming a path that does not exist, and one naming a real path at an
   impossible line, to a COPY of the file, and report that the checker REJECTS
   each. A checker that accepts a bogus citation proves nothing about the real
   ones.
G7 THE INVENTORY ANSWERS EVERY QUESTION. Report that `.agent/f255_inventory.md`
   carries one `##` heading per question Q1..Q6 in that order, and for each the
   number of citation rows beneath it. A question answered by an ABSENCE is
   answered — report it as ABSENT with the search that established it, and give
   the search command, not a conclusion alone.
G8 THE PLAN. `.agent/plan.md` at C4 byte-equals PLAN255R2; report its sha256,
   byte and line counts, that the line count is under 50, and that `## Goal`,
   `## Next Steps` and a roadmap F-id all occur in it.
G9 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches no source file, no
   test and nothing under docs/, so the four state-reader files are the gate,
   plus the canary. Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `6c47a490` in the primary checkout.
G10 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 6c47a490..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the eight paths the Change section names as untouched is PRESENT
   at the base and absent from that range; that every commit in the range has
   one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table. C5's own cell and the complete change set
   belong to the round report, not to C5.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   first, the count of reflog entries of this round that PRODUCED a commit and
   read `commit` — it must equal the number of commits the round makes; second,
   the count of entries of this round, navigation included, whose OPERATION
   PREFIX — the text before the first colon of `git reflog --format=%gs` —
   contains `amend`, `reset`, `rebase` or `cherry`, which must be 0. Read the
   prefix, never the whole line: commit SUBJECTS in this project routinely
   contain the word "reset", and scanning the full line reports false rewrites.
   List every entry of the round with its operation prefix.
G11 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/live_review.md` at C2, `.agent/f255_inventory.md` at C3,
   `.agent/plan.md` at C4 and `.agent/handoff.md` at C5. Every count must be 0.
G12 THE PUSH. After C5, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 10).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C5 bundle, the `## Commits` table
             G10 pins, and one LINE per gate rather than its transcript
             (R-0582). Do NOT cite compliance with the template's 800-token cap:
             R-0602 registers that cap as dead letter this same round, and a
             handback claiming to meet it would be the false sentence that
             finding is about. Stay inside the LINE cap the template grants your
             commit count. Its `## Next` section names the next session's FIRST
             action as Phase 1 rule 1, the `.agent/STOP` re-read, and its SECOND
             as R3 — the DECISION round that rules the shape, rules R-0602 and
             amends the feature file — in that order, and states that R2 awaits
             review. There is no open pull request. The full transcripts go in
             the round report you return, never in the file. The handback also
             carries this Fortschritt line verbatim, because with no relay you
             never see the operator brief that would otherwise state it
             (R-0418):
             Fortschritt: ~5 % (F086 merged · F255 claimed at R1 · R2 measures
             the ground · R3 rules the design next) — Schätzung
──────────────────────────────────────────────────────────────
