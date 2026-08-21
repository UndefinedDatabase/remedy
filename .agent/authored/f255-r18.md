── STEP R18 — F255 Teacher role · INTEGRATION GATE ─────────────
Goal:        Run the FULL suite twice — once on this branch, once at the merge
             base — compare the failure sets, attribute every difference, and
             commit the evidence. This is the tier-3 gate of
             docs/agents/planner_reviewer_prompt.md §3, performed exactly as
             docs/agents/integration_gate.md prescribes. It also persists the R17
             verdict: R17 PASSED with NO finding. This round changes NO source
             file and NO test file; it measures.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2 record
             the R17 verdict · C3 the gate evidence · C4 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r18.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/gate_f255_r18/` — NINE files, named exactly:
                 `branch_meta.txt`, `branch_run_tail.txt`, `branch_failed.txt`,
                 `base_parity.txt`, `base_failed.txt`,
                 `comm_branch_only_failures.txt`,
                 `comm_base_only_failures.txt`, `attribution.txt`,
                 `full_log_provenance.txt`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged in the tracked
             tree. NO source file and NO test file is touched this round. These
             paths are PRESENT at the base `b3146e91` and must stay untouched:
             `apps/cli/commands/teach_cmd.py`, `apps/cli/command_catalog.py`,
             `tests/cli/test_teach_cmd.py`,
             `packages/orchestration/teacher_model.py`, `.agent/decisions.md`,
             `docs/roadmap/features/T5_F255.md`.
             EVERY evidence file is `.txt` and NEVER `.log` (R-0169): `.gitignore`
             drops `*.log` silently and the review-zip guard rejects any member
             ending `.log`, so a log-named artifact vanishes from the record
             without a word.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback. Marker lines never reach a target file.
2. TRANSPORT. `.remedy-wt/f255-r18.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r18.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated.
3. THE PLAN COMES FIRST (R-0377, R-0491, R-0548). Only C0a and C0b may precede
   the `.agent/plan.md` update.
4. THE VERDICT PERSISTS BEFORE THE MEASURING BEGINS. C2 lands before C3, so a
   session that dies inside a 2-minute suite run still leaves R17's verdict on
   disk. This round registers NO finding and resolves NONE: registered stays 186,
   resolved stays 3.
5. RECORDR17 IS SINGLE-PARAGRAPH — the reviewer measured it for an interior blank
   line and found none — so the LAST-UNIT paragraph reading G5 orders is exact.
6. TWO PYTEST PROCESSES NEVER RUN AT ONCE. The branch run finishes before the
   base run starts, and every serial re-run happens after both. Runtime suites in
   this repository leak port-bound supervisors, so an overlap manufactures false
   reds that would then be attributed to the feature.
7. THE ENVIRONMENT VARIABLE IS PASSED AS AN ARGUMENT, NOT AS A SHELL PREFIX. This
   session's guard rejects the `VAR=value cmd` form, so set
   `REMEDY_UI_NO_AUTO_BUILD=1` for the BASE run through the `env=` parameter of
   `subprocess.run` — a copy of `os.environ` with that key added — and record
   that you did. Do NOT set it for the branch run.
8. THIS ROUND CONTAINS NO FROM/TO PAIR (§4.9, R-0207). The evidence files are
   generated from the runs, not authored here; only the two slices are authored.
9. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
    handback instead.
11. `git status --porcelain` is EMPTY after every commit. The base worktree is
    created under the gitignored `.remedy-wt/` and REMOVED before the handback.
12. YOU DO NOT WAIT ON ANY CI RUN and you create NO pull request: on this project
    the PR is created by the closure round, which is the round after this one.
13. A BLOCKER STOPS THE ROUND. If any branch-only failure reproduces serially AND
    is coupled to this feature's code, do NOT fix it here: commit the evidence
    you have, write the handback naming the id and the coupling, and END. The fix
    is its own reviewer-gated round (integration_gate.md step 4).

<<<SLICE PLAN255R18
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
R18 is the INTEGRATION GATE, per docs/agents/integration_gate.md: the full suite
on this branch and again at the merge base b35d350b, the two failure sets
compared, every difference attributed by direct evidence, and the whole record
committed under `.agent/gate_f255_r18/`. It also persists the R17 verdict. It
changes no source file and no test file.

## Next Steps
1. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, FRESH review zip, the STATUS line authored by the reviewer and
   committed last, and the pull request — which is created there and merged at
   the NEXT feature's Open PR Gate, never in the session that creates it.

## Risks
- A BRANCH-ONLY FAILURE COUPLED TO FEATURE CODE IS A BLOCKER, not a repair to
  fold into this round: it ends the gate and earns its own reviewed round.
- BASE PARITY CAN BE VOIDED BY A REBUILD THE DIGEST CANNOT SEE. F085 R72 measured
  a byte-identical `apps/ui/dist` whose mtime had moved, and `_frontend_is_stale`
  decides by mtime, so this round reads BOTH and claims parity only if neither
  moved (finding R-0565).
- THE OPEN SET IS 183 AND NONE OF IT IS PAID DOWN HERE. R-0607, R-0608 and R-0609
  are reviewer-process findings; R-0610's code half landed at R17 and only the
  reviewer's own text may resolve it.
<<<END PLAN255R18
<<<SLICE RECORDR17
Gate: R18 — the R17 entry. R17 PASSED with NO finding registered against it, and the worker declared NO deviation because none was owed: the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 ran in exactly that order, none dropped, added or reordered. Every gate the R17 block ordered was RE-EXECUTED by the reviewer over `8f885b4f..b3146e91` rather than read from the handback; every number here is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r17.md`, the committed `.agent/authored/f255-r17.md` at `f0287557` and the committed `.agent/last_block.md` at `cbe83001` are byte-EQUAL at sha256 45fedbdf8ed39f04a92e08678161cb83fe2eb46e39d3bb7dfc4f30c58ca615a4 over 31242 B and 284 lines, the digest stated at delegation. THREE SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count, newline convention NEWLINE-INCLUDED: PLAN255R17 sha256 7f7d6271e0d09f130fabb8b2a8c74a850424614d1263fd43958436bcbb6c09eb over 2125 B and 38 lines; FINDINGS3 sha256 2811b7b659491067cb99b4f427c305268859dbfea8589a679b3de93fc8c2e6ba over 6444 B and 5 lines; RECORDR16 sha256 4bfca993fc0d86e43febcfae5248ce2c8bd0c71e84c9714641b4f38b3814714e over 5940 B and 1 line. THE PLAN LANDED FIRST: `.agent/plan.md` at `0f2b3968` byte-equals PLAN255R17 over 2125 B and 38 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and `git log --reverse 8f885b4f..0f2b3968` opens f0287557, cbe83001, 0f2b3968. THE FINDINGS PERSISTED BEFORE THE VERDICT, which is what §4.4 asks: the `.agent/live_review.md` blob at `8f885b4f` is a byte-exact prefix of the blob at `76d2d941` whose 6445 B remainder equals one newline followed by FINDINGS3, the byte after that newline being `-`; and THAT blob is a byte-exact prefix of the blob at `8729b4d4` whose 5941 B remainder equals one newline followed by RECORDR16, the byte after that newline being `G`. The blank-line paragraph split of the C3 blob gives 210 units whose LAST unit IS RECORDR16, and no paragraph reading was ordered or reported for the multi-paragraph FINDINGS3, which is what R-0606 asks. THE THREE REGISTRATIONS AGREE UNDER BOTH READINGS the block ordered, R-0578's counter-measure: splitting FINDINGS3 on blank lines and collecting the C2 blob's registered lines absent at the base both give R-0608, R-0609 and R-0610, in that order. THE SETS MOVED BY EXACTLY THREE REGISTRATIONS AND NOTHING ELSE: 183 registered / 3 resolved / 180 open / 0 line-anchored `Landed:` at `8f885b4f`, then 186 / 3 / 183 / 0 at BOTH `76d2d941` and `8729b4d4`, the second commit adding a `Gate:` paragraph, which is neither kind of line. Each of `R-0608`, `R-0609` and `R-0610` occurs 0x at `8f885b4f` and exactly 1x as a registered line at `76d2d941`. `Gate: R17 — the R16 entry.` occurs 0x at the base and 1x at `8729b4d4`, sits last among the seventeen lines beginning `Gate: R`, and all seventeen header keys are distinct. R-0610'S CODE HALF IS REAL, and the reviewer read the diff rather than the tests' names: `apps/cli/commands/teach_cmd.py` at `da0ed2d9` gains `--file`, reads that ONE file through `Path.read_text` — reading writes nothing, so the `write_metadata` class of DECISION F255 D10 is untouched — and passes its text as `code` with the path as `code_path` to BOTH the context whose grounding list is printed and the one `ask_teacher` builds, so the two cannot disagree. An unreadable path prints a line naming the path and the reason, leaves `code_path` None rather than asserting a file it never read, and still answers. THE TESTS PIN WHAT THE MODEL WAS SHOWN, not merely what the JSON said: the four tests at `aa3a47c9` capture the prompt the injected seam received and assert the file's text and its path are IN it, that `[code]` is absent without the option, that an unreadable path is said out loud at exit 0, and that the data-root hash map with the ledger excluded by name is unchanged while the source file is byte-identical afterwards. THE CALLER MEASUREMENT THAT R-0610 TURNS ON WAS RE-TAKEN: at `b3146e91` the only caller of `ask_teacher` outside `tests/` is `_cmd_teach_ask`, and it now passes both `code` and `code_path`, where at `8f885b4f` it passed neither. THE SUITES ARE THE REVIEWER'S OWN RUNS, all serial and in the primary checkout at `b3146e91`: `tests/cli/test_teach_cmd.py` with `tests/test_command_catalog.py` exit 0 at 37 passed; the three teacher modules exit 0 at 42 passed; the state-reader four exit 0 at 160 passed; the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed; and `ruff check` 0.15.17 over the three touched paths exit 0, All checks passed. THE RANGE AND THE HISTORY HOLD: eight paths over eight single-parent commits; per-commit insertions 284, 190, 14, 6, 2, 59, 104 and 36, every one under the 500 cap — and C4 and C5 are separate commits because the R17 block ordered them so, which is R-0609's counter-measure working the round it was registered; the change set equals the block's Change list with no path on either side alone; all six paths the block named untouched are PRESENT at `8f885b4f` and ABSENT from the range; zero lines beginning with the slice or end marker prefixes appear in any written file; and at `b3146e91` the round has made 8 commits with 8 reflog entries whose operation prefix reads exactly `commit` and NO entry of any other prefix, so the `reset` carve-out R-0608 introduced was available and not needed. THE HANDBACK MEASURES CLEAN: 82 lines at `b3146e91`, inside the 100-line allowance its bundle earns, no trailing whitespace on any line, all seven mandated headings in the template's order, an item-status table naming C0a through C6 exactly once, and `## Commits` cells byte-identical to `git diff --numstat`. R-0607, R-0608 AND R-0609 REMAIN OPEN and none of them is a code defect: the first is closed only by a docs round promoting its rule into the docs/agents/planner_reviewer_prompt.md §3 checklist, and the other two bind the shape of future blocks, which is why each was answered by this round's own block rather than by an edit.
<<<END RECORDR17

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback. `git worktree list` reports the
   primary checkout ALONE at the handback — the base worktree is removed and
   pruned and its temporary branch deleted before then, and you report the
   command output that proves it.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r18.md`, of `.agent/authored/f255-r18.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r18.md` by its markers; report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R18; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report that C1
   is the FIRST commit other than C0a and C0b, from
   `git log --reverse b3146e91..<C1>`.
G5 THE R17 VERDICT RECORDED. Over `.agent/live_review.md`: the base blob at
   `b3146e91` is a byte-exact PREFIX of the C2 blob; report the remainder's
   sha256, byte and line counts; that it equals one newline followed by
   RECORDR17; and that the byte after that leading newline is not a newline.
   Then a SECOND, INDEPENDENT blank-line paragraph split of the C2 blob whose
   LAST unit is RECORDR17, giving that unit's sha256 under BOTH newline
   conventions with the byte count of each. Re-measure constraint 5 rather than
   trusting it. Run a negative control: one character of the expected remainder
   mutated, rejected by BOTH readings.
G6 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` over `.agent/live_review.md` at `b3146e91` and at C2, the registered
   count being lines matching `^- R-\d+ — ` and the resolved count lines matching
   `^Done: R-\d+ — `: the reviewer measured 186 / 3 / 183 / 0 at `b3146e91`, and
   C2 owes the SAME four numbers because a `Gate:` paragraph adds neither kind of
   line. Report that `Gate: R18 — the R17 entry.` occurs 0x at `b3146e91` and 1x
   at C2, that it is the LAST line beginning `Gate: R`, and that every such
   header key is distinct. COUNT HEADERS LINE-ANCHORED, never as substrings
   (R-0584).
G7 THE BRANCH RUN. In the PRIMARY checkout, at the commit C2 creates, run
   EXACTLY `python3 -m pytest -n auto -q`, writing its output to a log OUTSIDE
   the tracked tree — under `.remedy-wt/.cache/gate_r18/` — because a log growing
   INSIDE the repo during a run changes the worktree digest mid-run and turns the
   manifest-identity tests into false failures (R-0176). Do NOT set
   `REMEDY_UI_NO_AUTO_BUILD` for this run. Record into `branch_meta.txt` the
   checkout, the revision, the exact command, the exit code, the wall seconds,
   the summary line and the FAILED count; the last 40 lines into
   `branch_run_tail.txt`; and the sorted list of lines beginning `FAILED` into
   `branch_failed.txt`. Report the exit code, the summary line and the wall time.
G8 THE BASE RUN, AT PARITY. Create the base worktree ON A BRANCH, never detached
   — `git worktree add -b tmp/base-gate-r18 .remedy-wt/base-r18 b35d350b` —
   because the self-dogfood branch guard refuses a detached checkout by design
   (DECISION D3). `b35d350b` is the merge base, and the reviewer measured it as
   both `git merge-base main HEAD` and the tip of `main` at `b3146e91`.
   RESTORE ARTIFACT PARITY BEFORE THE RUN: copy `apps/ui/node_modules` and
   `apps/ui/dist` from the primary checkout into the base worktree with
   `shutil.copytree(src, dst, symlinks=True)`. THE `symlinks=True` ARGUMENT IS
   THE ORDER, not a detail: `copytree` defaults to `symlinks=False`, which
   DEREFERENCES npm's bin shims and itself CAUSES base-only failures the parity
   exists to prevent (R-0591). Report, per destination, that it is a real
   directory and not itself a symlink.
   Then run the SAME command in that worktree with `REMEDY_UI_NO_AUTO_BUILD=1`
   passed through `env=` (constraint 7), logging outside the tracked tree as in
   G7. VERIFY THE NEUTRALISATION RATHER THAN TRUSTING IT: before and after the
   base run, record the sha256 over `apps/ui/dist` and the file count, AND the
   `st_mtime_ns` of `apps/ui/dist/index.html`. A CHANGED DIGEST **OR** A MOVED
   MTIME VOIDS THE PARITY CLAIM — the digest is blind to a byte-identical
   rebuild while `_frontend_is_stale` in `packages/orchestration/ui_server.py`
   decides staleness by MTIME (R-0565) — and a void claim forces G10's per-id
   attribution of every base-only id. Write all of it, and the verdict
   `PARITY_CLAIM=HELD` or `PARITY_CLAIM=VOID`, into `base_parity.txt`; write the
   sorted `FAILED` lines into `base_failed.txt`. Report the exit code, the
   summary line and the parity verdict.
G9 THE COMPARISON. With both sorted files, write the branch-only failures
   (`comm -13 base_failed.txt branch_failed.txt`) into
   `comm_branch_only_failures.txt` and the base-only failures (`comm -23`) into
   `comm_base_only_failures.txt`. Report the COUNT of each. State plainly that a
   count of 0 branch-only failures is the gate's passing shape and report the
   real number whatever it is.
G10 ATTRIBUTION, FOR EVERY DIFFERING ID, into `attribution.txt`. For EACH
   branch-only id: re-run that exact node id SERIALLY, after both suite runs, and
   classify it — a serial PASS is the xdist-flake class and is recorded, not a
   blocker; a serial FAIL is reproduced at the merge base before the feature is
   blamed; and a reproducible branch-only failure coupled to this feature's code
   is a BLOCKER that ends the round under constraint 13. For EACH base-only id:
   if `PARITY_CLAIM=HELD` say so and name the id; if VOID, attribute that id to
   the environment class BY DIRECT EVIDENCE — the missing or rebuilt artifact
   named per id — because an unattributed base-only id counts as a genuine base
   failure and blocks the gate verdict. If BOTH lists are empty, say exactly that
   and record the two counts; the file is never absent.
   Write `full_log_provenance.txt` naming every raw log's scratch path, its line
   count and its sha256, and stating that the raw logs stay outside the tracked
   tree while only derived `.txt` evidence is committed.
G11 THE CANARY AND THE STATE READERS, UNCONDITIONALLY — R-0607's rule, which
   binds whether or not a round looks harmless. This round rewrites `.agent/`
   state, so both gate. Run them serially in the PRIMARY checkout AFTER the two
   suite runs, never two pytest processes at once, and report the exact command,
   exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed at
   `b3146e91` in the primary checkout.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only b3146e91..<C3>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C4
   itself adds, with no path on either side alone. Report that each path the
   Change section names untouched is PRESENT at the base and ABSENT from the
   range; that every commit in the range has one parent; and each commit's
   insertion column from `git diff --numstat` for C0a through C3, every one under
   500, with the same `+/-` cells appearing byte-identically in the handback's
   `## Commits` table (checklist item 28). C4's own cell and the complete change
   set belong to the round report (R-0149).
   THE REFLOG IS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601), AND NEITHER IS
   A TOTAL (R-0605): report the count of this round's reflog entries whose
   OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — reads exactly `commit`, WITH the commit it was
   taken at and the number of commits the round has made AT THAT MOMENT, and
   state that the two are equal. State no total: C4 is unwritten as this is
   composed (R-0494). HISTORY REWRITING IS GATED AS R-0608 RULES: report the
   count of entries whose prefix contains `amend`, `rebase` or `cherry`, which
   must be 0, and for EVERY entry whose prefix is `reset`, report it together
   with the demonstration that its destination is the commit the branch already
   pointed at. Creating and removing the base worktree adds its own entries;
   those are navigation, not rewriting, and you report them as what they are.
G13 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C2 and `.agent/handoff.md` at C4 — every count 0. Then, after C4,
   `git push` and report its real output. Do NOT create a pull request and do NOT
   wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C4 bundle, the `## Commits` table G12 pins, and
             one LINE per gate rather than its transcript (R-0582). Its
             `## Verification` section carries the gate's four load-bearing
             numbers — branch exit code and summary, base exit code and summary,
             branch-only count, base-only count — plus the parity verdict, and
             says plainly whether this is the ONLY round of this feature entitled
             to the words "full suite". Its `## Next` section names the next
             session's FIRST action as Phase 1 rule 1, the `.agent/STOP` re-read,
             and its SECOND as the CLOSURE round per
             docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review
             zip, the reviewer-authored STATUS line committed last, and the pull
             request, which is created there and merged at the NEXT feature's
             Open PR Gate. It states that R17 PASSED and its verdict is ON DISK
             at C2, that R-0607, R-0608 and R-0609 remain OPEN, and that R18
             ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON DISK. It states that no
             pull request is open. Transcripts go in the round report. The
             handback carries this Fortschritt line verbatim (R-0418):
             Fortschritt: ~95 % (T001 through T004 COMPLETE and REVIEWED · the
             integration gate ran the full suite on both sides at this round ·
             only closure remains — evidence job, review zip, STATUS line and the
             pull request) — Schätzung
──────────────────────────────────────────────────────────────
