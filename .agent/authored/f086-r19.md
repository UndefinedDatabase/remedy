── STEP R19 — F086 Release capability (record R18; register and fix R-0585) ──

Goal:
Close this session's record. R18 landed exactly as ordered, and the one deviation
its worker had to declare is a defect in the reviewer's own block text: gate G10
said "exactly the four paths of constraint 2 other than `.agent/handoff.md`" while
constraint 2 names five such paths. The worker read the semantics, changed nothing
to fit the numeral, and declared the contradiction — which is the right outcome and
still costs a round. This round registers that as R-0585, records R18's verdict,
and promotes the narrow rule it exposes into the §3 pre-emission checklist, where a
rule has to live to bind anything (finding R-0452 class).

WHY THE RULE MOVES RATHER THAN THE NUMERAL. Item 16 already forbids a sentence that
counts what follows it, and it was obeyed: every heading in the R18 block was swept.
What it does not reach is a sentence counting a list that lives in ANOTHER SECTION
of the same block — the check as written reads "the body beneath it", and the list
that drifted was fifty lines above. That gap is the whole finding.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r19.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN19 slice, whole file
  C2  append FIND0585 then RECORD17 to `.agent/live_review.md`
  C3  apply the CHECKFROM → CHECKTO pair to
      `docs/agents/planner_reviewer_prompt.md`
  C4  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C5  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 item 23 requires the plan to advance before any commit
touching the finding ledger. C2 precedes C3 because §4 item 4 requires findings to
persist BEFORE their repair. No `Landed:` line is ordered this round: the repair is
a documentation amendment whose effect the NEXT block demonstrates by obeying it,
not a code change whose landing a line could assert.

Base:
This round starts from `7b84524c`, the tip of `feature/f086-release-capability`
and the R18 handback commit. Every range gate names that SHA. Stay on the branch:
do NOT create one, merge, or open a PR — F086's PR belongs to its closure round.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN19 is a
COMPLETE file including its single trailing newline. FIND0585, RECORD17 and VERDICT
are EOF-APPENDS: pure concatenation, each slice's own leading blank line INSIDE the
slice, nothing prepended, nothing stripped. CHECKFROM and CHECKTO are a multi-line
replacement pair, each line carrying its own six-space indentation and its trailing
newline.

PAIR SHAPE, from the containment test run on these exact bytes at emission:
  CHECKFROM → CHECKTO   TO contains FROM: true → APPEND-shaped. The §4.9 append
  obligation is therefore what G7 orders — CHECKFROM exactly 1x before AND after,
  plus each TO-ONLY line exactly 1x among the lines C3's diff ADDS — and a
  "FROM 0x" reading is NOT orderable for this pair and is not ordered anywhere.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `7b84524c`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r19.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r19.md`; copy that file rather than retyping it. Commit alone.
   C0b then copies the COMMITTED `.agent/authored/f086-r19.md` over
   `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN19 slice, byte-verbatim, whole file. Alone.

3. C2 — append FIND0585 and then RECORD17 to `.agent/live_review.md`, in that
   order, under the append convention. Commit alone.

4. C3 — in `docs/agents/planner_reviewer_prompt.md`, replace CHECKFROM with
   CHECKTO. CHECKFROM occurs exactly 1x in that file at `7b84524c`; count it before
   replacing it. CHECKTO is CHECKFROM plus seven lines appended after it, so the
   edit adds text at the end of §3 item 16 and touches nothing else — item 17's
   line must still follow immediately, and no other item may be renumbered,
   reflowed or re-indented. Commit alone.

5. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 7b84524c..<HEAD>`; write the literal token `HEAD`, this
   branch's convention from R10 onward, because a handoff cannot name the SHA of
   the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT — one line per gate:
   its number, what it measured in a clause, and its real colour or value (the
   R-0582 repair; G11 measures it). The FULL transcript goes in your ROUND REPORT,
   which no cap binds.
   THE BUDGET IS ARITHMETIC: the VERDICT slice C5 appends is 42 lines, measured by
   the reviewer, so 58 of the 100 remain for your text. Measure it yourself from
   the COMMITTED C0a file before writing C4, and state the FINAL line count of
   `.agent/handoff.md` in your Deviations section. Do NOT trim after C5.
   `Next` names, in order, the next session's first three actions: re-read
   `.agent/STOP` from disk (Phase 1 rule 1), run the Open PR Gate (rule 2), then
   review `7b84524c..HEAD` and record R19's verdict (rule 4).

6. C5 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C4 must be a byte-exact PREFIX of the file at HEAD.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY the paths listed here and nothing else:
   `.agent/authored/f086-r19.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`, and
   `.agent/handoff.md` at C4 and C5. The round writes NO production code and NO
   test: not `tests/orchestration/test_release_workflow.py`, not
   `.github/workflows/release.yml`, not `scripts/release_gate_check.py`, not
   `packages/orchestration/ci_stages.py`, not `pyproject.toml`, and nothing under
   `apps/`, `packages/`, `tests/` or `docs/roadmap/`. Each of those five named
   files exists at `7b84524c`, so the prohibition forbids something real (R-0559).
   G9 states this set by NAMING it rather than by counting it, which is the rule
   this round is registering.
3. FIND0585, RECORD17, CHECKTO and VERDICT are the reviewer's text. Do not
   summarise or reformat them, and do not write a verdict of your own anywhere —
   in the handoff, in a commit message, or in your report. Reporting what a gate
   MEASURED is your job; ruling on a round is not. No worker-authored text lands
   in a tracked file this round.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback, and `git worktree list` reads one line throughout. This round
   orders NO mutation and NO disposable worktree: it changes one prose paragraph
   in a convention document and three state files, and a mutation red-proof over
   prose measures nothing.
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
6. SIZE, measured at emission on the final bytes: this block is 359 lines TOTAL —
   245 prose and 114 slice including its 12 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`;
    `git worktree list` one line.

G2  TRANSPORT. `.remedy-wt/f086-r19.md`, the committed
    `.agent/authored/f086-r19.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN19 slice extracted
    from the COMMITTED `.agent/authored/f086-r19.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  THE LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob and the remainder is byte-equal to FIND0585
    followed by RECORD17. Report the remainder's own full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At HEAD report registered / resolved / duplicate ids / unregistered
    resolutions / anchored `Landed:` lines / open, for BOTH, and the two
    registered id SETS must be EQUAL. Expected at HEAD: 168 registered, 3
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:` lines, 165
    open. Report the symmetric difference of the HEAD registered set against the
    `7b84524c` set AS THE SET; it must be exactly `['R-0585']`.
    CONTROL: the SAME extractor over `f0b27118..7b84524c` must read `[]` for the
    registered symmetric difference while its RESOLVED set gains exactly `R-0584`,
    so the extractor is measured on a range that moved a resolution and not a
    registration.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md` and `docs/agents/planner_reviewer_prompt.md` at HEAD each
    contain 0 lines beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not
    `<<<`.

G7  THE APPEND-SHAPED PAIR, under the §4.9 obligation its shape carries. In
    `docs/agents/planner_reviewer_prompt.md`: CHECKFROM occurs exactly 1x at
    `7b84524c` AND exactly 1x at HEAD — that is what an append means and it is not
    a defect — and each of CHECKTO's seven TO-ONLY lines occurs exactly 1x among
    the lines C3's diff ADDS. Report all nine counts one by one. Then the
    ORDERED-EQUALITY reading: the file at HEAD is byte-equal to the `7b84524c`
    blob with the single CHECKFROM occurrence replaced by CHECKTO and nothing else
    changed. Report the file's full sha256 and line count at HEAD, and confirm the
    line count grew by exactly 7.

G8  THE EDIT LANDED INSIDE ITEM 16 AND MOVED NOTHING ELSE. At HEAD,
    `grep -c '^  17\. \*\*' docs/agents/planner_reviewer_prompt.md` reads 1, and
    the line immediately following CHECKTO's last line is that item-17 line.
    Report both readings verbatim. This is the structural check the pair proof
    cannot give: ordered equality would also hold for an insertion that landed in
    the wrong item if the bytes happened to match, and this one names where.

G9  CHANGE SET. `git diff --name-only 7b84524c..HEAD` before C4 is the paths
    constraint 2 names, other than `.agent/handoff.md`. Report the list it prints
    and the list constraint 2 names, and compare them AS SETS — state no numeral
    for either. Confirm with `git ls-tree 7b84524c -- <path>` that every path
    constraint 2 FORBIDS exists at the base, and report those readings.

G10 SUITES, in the PRIMARY checkout, serially, the second starting only after the
    first has ENDED: `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed; then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.
    These four readers parse the state files this round rewrites, so they are the
    gate that can fail on a bad state text. NOTE, so the handback does not claim
    more than it proves: NO suite in this repository reads
    `docs/agents/planner_reviewer_prompt.md`, so no test can go red on C3. The
    pair proof and G8 are that commit's entire evidence, and saying so is the
    point — a suite run beside a docs edit proves the docs edit nothing.

G11 HISTORY AND COMMIT SIZE. Every commit in `7b84524c..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Report the chain and
    the INSERTION count for every commit BEFORE C4, one each; none over 500. C4's
    and C5's own go in the round report (§3 item 14).

G12 THE HANDBACK. `.agent/handoff.md` at HEAD is AT MOST 100 lines and carries all
    seven mandated headings of docs/agents/handback_template.md in the template's
    order. Report the `wc -l` reading and the heading list. If it exceeds 100,
    declare the DECISION D15 overage with its cause rather than dropping a
    section.

G13 THE VERDICT APPEND. The `.agent/handoff.md` blob committed by C4 is a
    byte-exact PREFIX of the file at HEAD and the remainder is byte-equal to the
    VERDICT slice. Report the remainder's full sha256 and line count.

G14 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft`. Report its output. Create nothing,
    merge nothing.

Handback: your completion report with the FULL transcript, plus C4's rewrite of
`.agent/handoff.md` and C5's append, exactly as steps 5 and 6 specify.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN19>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R19, this round and this session's last: record R18's verdict, register R-0585 —
a done-when gate of the R18 block counted a path list that lives in another
section of that block — and promote the rule it exposes into the §3 pre-emission
checklist, item 16, where a rule has to live to bind the next block.

## Next Steps
1. R20 writes the install smoke per DECISION F086 D4: one `smoke`-marked,
   `slow`-marked module that SELF-SKIPS unless `REMEDY_INSTALL_SMOKE` is set. What
   it can gate is the skip path and the module's own logic; what it cannot gate is
   the install itself, and it says so rather than implying coverage.
2. Then the smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a 300 s budget
   that AGENTS.md forbids raising by hand.
3. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN, and no round can dispatch it; its
   first real run is a human action.

## Risks
- The install smoke needs network, a venv interpreter and minutes. MEASURED at
  R17: this session's permission layer refuses to execute an interpreter under
  `.remedy-wt/`, so a self-drive round can write that smoke but cannot run it.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN19>>>

<<<SLICE FIND0585>>>

- R-0585 — Low — A DONE-WHEN GATE COUNTED A LIST THAT LIVES IN ANOTHER SECTION OF THE SAME BLOCK, AND ITEM 16'S CHECK DOES NOT REACH IT. The R18 block, committed at `ec618ca1`, states in constraint 2 a change set of five paths — `.agent/authored/f086-r18.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`, plus `.agent/handoff.md` at C5 and C6 — while its gate G10 orders the pre-C5 change set to be "exactly the four paths of constraint 2 other than `.agent/handoff.md`". Four against five, in one block, about one list. The worker measured the real set, found the five paths constraint 2 names, applied the semantic reading, changed nothing to make the numeral true and declared the contradiction, which is the correct handling of a reviewer defect and still costs the round a declared deviation. WHY ITEM 16 DID NOT CATCH IT: that item forbids a heading or a quantifying sentence from counting "the body beneath it", and it was obeyed — the R18 block's headings were swept and none of them counts anything. The list G10 counted sits roughly fifty lines ABOVE it, in a different section, so the check as written never looks at it. The defect is not that the rule was skipped but that its REACH is stated as proximity when the property it protects is reference: a sentence is at risk whenever it counts a list it does not itself contain, and where that list lives is irrelevant. WHY LOW rather than Medium: nothing false reached disk. The block is the permanent record and it carries the contradiction, but every gate that ran measured the real set, the change set was correct, and the cost was one declared deviation rather than a wrong state file — the R-0250 class caught by an honest worker instead of by a reader six rounds later. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: §3 item 16 gains the clause that a counted list need not sit beneath the sentence counting it, together with the standing preference for naming a list — "the paths constraint 2 names" — over counting it, which is the form that cannot drift at all. This round's own G9 is written in that form, so the block demonstrates the rule it lands.
<<<END FIND0585>>>

<<<SLICE RECORD17>>>

Gate: R19 — the R18 entry. R18 PASSED, with ONE finding — R-0585, against the reviewer, registered by this round's own FIND0585 slice. Every gate its block ordered was re-executed by the reviewer over `f0b27118..7b84524c` rather than read from the handback, and every reading reproduces. THE RESOLUTION IS ON DISK AND IT REPLACED THE RIGHT LINE: `LANDEDFROM` occurs 1x at `f0b27118` and 0x at HEAD, DONE0584 0x and then 1x, and the blob C2 committed is byte-equal to the base blob with that single occurrence replaced and nothing else changed — `git show --numstat e4407e7f` reads 1 insertion and 1 deletion, the file's line count unchanged at 997. THE LEDGER MOVED IN THE ONE DIMENSION THE ROUND CLAIMED: both extractions AGREE at each end, 167 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions / 1 `Landed:` / 165 open at `f0b27118` and 167 / 3 / 0 / 0 / 0 / 164 at HEAD with the two registered SETS equal; the REGISTERED symmetric difference is empty, the RESOLVED set gains exactly `R-0584`, and the reviewer's control over `4750383c..f0b27118` reads `['R-0584']` for the registered difference, so an empty reading here is a measured absence rather than a blind extractor. THE APPENDS ARE PURE CONCATENATION: the C2 blob is a byte-exact PREFIX of the C3 blob whose 2-line remainder equals RECORD16, and the pre-C4 `.agent/decisions.md` blob is a byte-exact PREFIX of the post-C4 blob whose 44-line remainder equals DECISION4, taking `^## DECISION F086 D` from 3 to 4. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original `.remedy-wt/f086-r18.md`, the committed `.agent/authored/f086-r18.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 3b37ce276cb5dc9ec36b068d0c98092c5672313255c54b6c0444844cdb0778da, 27390 B over 379 lines — 379 total, 232 prose, 147 slice including 12 marker lines, which is what constraint 6 of that block declares of itself. `.agent/plan.md` equals PLAN18 over 45 lines and the C5 handoff blob is a byte-exact PREFIX of the file at HEAD whose 42-line remainder equals VERDICT. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the four written files. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: 160 passed for the four state readers, then 42 for the canary, each exit 0 — the readers that PARSE the files this round rewrote, so they could have failed on a bad state text. THE HYGIENE HELD: five paths over eight single-parent commits inserting 379, 242, 18, 1, 2, 44, 29 and 42 lines, none over 500 and no DECISION F104 D1 exemption invoked; `.github/workflows/release.yml`, `packages/orchestration/ci_stages.py`, `pyproject.toml`, `scripts/release_gate_check.py` and `tests/orchestration/test_release_workflow.py` are absent from the range and all five exist at the base. THE HANDBACK CAME IN UNDER ITS CAP at 97 lines against 100, all seven mandated headings in the template's order, no DECISION D15 overage — the fifth round running that the R-0582 repair has held. WHERE R18 WENT WRONG is in none of its own work but in the block that ordered it, whose G10 counted four paths where constraint 2 names five; that is R-0585, and the worker's declared deviation is the record of it being caught rather than obeyed.
<<<END RECORD17>>>

<<<SLICE CHECKFROM>>>
      rather than synchronise it. A ruled figure that must appear in a heading appears there
      once, in the same words as the body that rules it, so that a later revision cannot
      change one without visibly contradicting the other.
<<<END CHECKFROM>>>

<<<SLICE CHECKTO>>>
      rather than synchronise it. A ruled figure that must appear in a heading appears there
      once, in the same words as the body that rules it, so that a later revision cannot
      change one without visibly contradicting the other.
      Finding R-0585 widens the check's REACH rather than its subject: the list a sentence
      counts need not sit beneath that sentence. The R18 instance is a done-when gate reading
      "exactly the four paths of constraint 2 other than `.agent/handoff.md`" while constraint
      2, fifty lines above it, named five — so "read the numerals against the body beneath it"
      never looked at the list that had drifted, and an honest worker had to spend a declared
      deviation proving the block contradicted itself. Resolve every count to the list it
      NAMES, wherever in the block that list lives, and prefer naming it over counting it.
<<<END CHECKTO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming the branch at `4750383c` and ending
at its declared three-round cap. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on
gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R16 | efc021d9..4750383c | PASS — one finding, R-0584, against the reviewer |
| R17 | 4750383c..f0b27118 | PASS — no finding |
| R18 | f0b27118..7b84524c | PASS — one finding, R-0585, against the reviewer |
| R19 | 7b84524c..HEAD | verdict not yet on disk; see the last paragraph |

R16 was inherited ungated, so Phase 1 rule 4 reviewed it first. Its manual release
trigger is real and every ordered property reproduced; its one defect was invisible
to every gate it ordered, and only a control the block never ordered could find it
— three guards asserting over text that included the workflow's COMMENTS, two of
them satisfied by a comment alone. R17 repaired exactly that, measured from both
sides: the mutation that was green at `4750383c` is red at `f0b27118`, naming only
its own test, while the guard that was already sound stays red at both commits.
R18 resolved R-0584 in the ledger and ruled DECISION F086 D4 — the install smoke is
written here and executed elsewhere, with the permission and network constraints
that force it measured rather than assumed. Its own defect was again the reviewer's:
a gate counting a list it did not contain, which is R-0585 and which R19 promotes
into the checklist.

WHAT THIS FEATURE STILL OWES: the install smoke module per D4, then its wall-clock
measured on a host that can run it, then the CI opt-in, then the integration gate
and closure. NOTHING IN THIS SESSION PROVED AN INSTALL, and no round of this
workflow can; D4 records that with the measurement behind it. The release workflow
has likewise never been dispatched.

R19 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `7b84524c..HEAD` and record R19's verdict in
`.agent/live_review.md` as `Gate: R20 — the R19 entry`.
<<<END VERDICT>>>
