── STEP T2/3 — F086 R22 ──────────────────────────────────────

Goal:        Record R21's verdict, register R-0588 — a done-when ordered a
             whole-file bound measurable only after the LAST commit while the
             declaration it demanded had to be written into the commit BEFORE it
             — and promote that rule onto §3 item 14, whose reach it extends.

Bundle:      1. `.agent/plan.md` := PLAN22.
             2. `.agent/live_review.md` += FIND0588, then RECORD20.
             3. `docs/agents/planner_reviewer_prompt.md` += the R-0588 clause at
                the end of §3 item 14.
             4. The handback, then the session verdict appended to it.

Change:      C0a `.agent/authored/f086-r22.md` := this block, byte-verbatim, the
                 single top separator line included and nothing after the last
                 slice's END marker.
             C0b `.agent/last_block.md` := a mirror of the COMMITTED C0a, read
                 back from git rather than retyped.
             C1  `.agent/plan.md` := PLAN22, whole file. Alone. This is the round's
                 FIRST substantive commit because the bundle moves the finding
                 ledger (§3 item 23).
             C2  `.agent/live_review.md` += a blank line, FIND0588, a blank line,
                 RECORD20. Pure append; nothing already in the file changes.
             C3  `docs/agents/planner_reviewer_prompt.md`: apply the single pair
                 CHECK14FROM → CHECK14TO. Nothing else in that file changes.
             C4  `.agent/handoff.md` := your rewrite, in the COMPACT commits form
                 constraint 7 fixes.
             C5  `.agent/handoff.md` += the VERDICT slice, appended verbatim.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r22.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`, and
   `.agent/handoff.md` at C4 and C5. NOT `tests/test_install_smoke.py`, not
   `tests/conftest.py`, not `pyproject.toml`, not
   `packages/orchestration/ci_stages.py`, not `apps/cli/version_report.py`, and
   nothing else under `apps/`, `packages/`, `tests/`, `docs/roadmap/` or
   `.github/`. Every path this constraint FORBIDS exists at `e7cdae4d`, so the
   prohibition forbids something real (R-0559).
3. THE LANDED RECORD IS NOT REWRITTEN. Neither the duplicate header at
   `4dc7cbdf` nor the handoff at `e7cdae4d` that lacks its DECISION D15 line is
   repaired. §3 item 20 rules that the counter-measure for landed text is a dated
   correction in NEW text, never a rewrite. You append; G7 is written so the
   duplicate left standing is expected rather than forbidden.
4. PLAN22, FIND0588, RECORD20, CHECK14TO and VERDICT are the reviewer's text. Do
   not summarise or reformat them, and do not write a verdict of your own
   anywhere — in the handoff, in a commit message, or in your report. Reporting
   what a gate MEASURED is your job; ruling on a round is not.
5. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback, and `git worktree list` reads one line throughout. This round
   orders NO mutation and NO disposable worktree: it writes no code, so there is
   nothing to red-prove, and inventing a mutation to look thorough would prove
   nothing about a documentation edit.
6. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
7. THE HANDBACK'S LENGTH IS FIXED BY ARITHMETIC THIS BLOCK DOES FOR YOU, which is
   the whole point of R-0588. The VERDICT slice this block ships is 44 lines,
   measured at emission on its final bytes, and C5 appends it by pure
   concatenation, so the file at C5 is exactly C4's length plus 44. Write C4 in
   the COMPACT commits form — ONE table with a per-commit row, the form R18's and
   R19's accepted handbacks used, not one table per commit — and keep C4 at 56
   lines or fewer, which puts the file at C5 at 100 or fewer with no DECISION D15
   overage to declare. If C4 nevertheless lands above 56, do NOT drop a mandated
   section: put the D15 "Deviations, declared" line in C4 itself, naming C4's own
   count and that count plus 44 as the final one, and say which mandated content
   caused it. Both readings are gated by G13.
8. SIZE, measured at emission on the final bytes: this block is 336 lines TOTAL —
   217 prose and 119 slice including its 12 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`;
    `git worktree list` one line throughout, per constraint 5.

G2  TRANSPORT. `.remedy-wt/f086-r22.md`, the committed
    `.agent/authored/f086-r22.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at the commit C1 creates is byte-equal to the PLAN22
    slice extracted from the COMMITTED `.agent/authored/f086-r22.md`. Report its
    full sha256 and line count, confirm the count is under 50, and confirm it
    contains `## Goal`, `## Next Steps` and `F086`.

G4  THE LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to a blank line,
    FIND0588, a blank line, RECORD20, in that order. Report the remainder's own
    full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At the commit C2 creates report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Expected there: 171 registered, 3
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:` lines, 168
    open. Report the symmetric difference of that registered set against the
    `e7cdae4d` set AS THE SET; it must be exactly `['R-0588']`.
    CONTROL: the SAME extractor over `f0b27118..7b84524c` must read `[]` for the
    registered symmetric difference while its RESOLVED set gains exactly `R-0584`.

G6  THE ITEM-20 SCAN, now that it is on disk. Take the lines C2's diff ADDS to
    `.agent/live_review.md`. FIRST delete every backtick-quoted span — the regex
    `` `[^`]*` `` — THEN count `\bHEAD\b` in what remains; the count must be 0.
    RED CONTROL: the SAME two-step extractor over the lines `fd166295`'s diff ADDS
    to that same file reads 3. Report both numbers. This gate binds the ledger
    commit only: VERDICT lands in `.agent/handoff.md`, which this workflow
    REWRITES every round, and its range row names `e7cdae4d..HEAD` by the
    R10-onward convention that a handoff cannot name the SHA of the commit that
    writes it. Do not "fix" that row and do not report it as a violation.

G7  THE ITEM-26 CHECK, WITH THE LANDED DUPLICATE LEFT STANDING. Collect every
    header matching `(?m)^Gate: R(\d+) — the R(\d+) entry\.` in
    `.agent/live_review.md`. At `e7cdae4d` exactly one header string occurs more
    than once, and it is `Gate: R19 — the R18 entry.` — report that reading first,
    because it is the RED CONTROL proving the extractor sees a duplicate at all.
    At the commit C2 creates the set of header strings occurring more than once
    must be UNCHANGED — still exactly that one string, because constraint 3
    forbids repairing it — and additionally: `Gate: R22 — the R21 entry.` occurs
    exactly 1x, it is the LAST such header in the file, and the text immediately
    following it begins `R21 `. Report all four readings.

G8  THE PAIR, classified by a containment test whose OUTPUT you print (§3 item
    15). In `docs/agents/planner_reviewer_prompt.md` print the literal words
    `TO contains FROM: true` or `TO contains FROM: false`, and derive the APPEND
    or REWRITE label from that output on the same line — never write the label on
    its own. It is expected APPEND-shaped, so the obligation is §4.9's append form
    and NOT a FROM-zero count: report CHECK14FROM occurring exactly 1x at
    `e7cdae4d` AND exactly 1x at the commit C3 creates — that is what an append
    means — and each CHECK14TO-ONLY line occurring exactly 1x among the lines C3's
    diff ADDS. Then the ORDERED-EQUALITY reading over the whole file: at the
    commit C3 creates the file is byte-equal to the `e7cdae4d` blob with
    CHECK14FROM's single occurrence replaced by CHECK14TO and nothing else
    changed. Report the file's full sha256 and line count there, and the line
    count at `e7cdae4d`, which is 805.

G9  THE EDIT LANDED INSIDE ITEM 14 AND RENUMBERED NOTHING. At the commit C3
    creates: `grep -c '^  15\. \*\*' docs/agents/planner_reviewer_prompt.md` reads
    1, `grep -c '^  14\. \*\*' ...` reads 1, and the line immediately following
    CHECK14TO's last line is
    `  15. **Pair shapes are classified by a containment test, never by eye.** Finding`.
    Report all three readings verbatim. This is the structural check the pair
    proof cannot give: ordered equality would also hold for text that landed in
    the wrong item if the bytes happened to match, and this one names where.

G10 NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md` and
    `docs/agents/planner_reviewer_prompt.md` at the commit C4 creates each contain
    0 lines beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<`.
    `.agent/handoff.md` can only be counted after C5, and that fourth reading goes
    in the round report.

G11 SUITES, in the PRIMARY checkout, serially, the second starting only after the
    first has ENDED and reported its code: `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed; then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.
    These four readers parse the state files this round rewrites, so they are the
    gate that can fail on a bad state text. NOTE, so the handback does not claim
    more than it proves: NO suite in this repository reads
    `docs/agents/planner_reviewer_prompt.md` — its one occurrence under `tests/`
    is inside the `reason=` string of a `@pytest.mark.skip` decorator in
    `tests/test_agent_tooling.py`, whose test reads a different file — so no test
    can go red on C3, and G8 plus G9 are that commit's entire evidence.

G12 CHANGE SET AND HISTORY. `git diff --name-only e7cdae4d..HEAD` before C4 prints
    the paths constraint 2 NAMES other than `.agent/handoff.md`; report the list
    it prints and the list constraint 2 names, and compare them AS SETS — state no
    numeral for either. Confirm with `git ls-tree e7cdae4d -- <path>` that every
    path constraint 2 FORBIDS exists at that base. Then: every commit in
    `e7cdae4d..HEAD` has exactly one parent, the chain is linear, and `git reflog`
    over this round shows only `commit:` entries. Walk the range with `git
    rev-list --reverse` and report the INSERTION count — the `+` column of `git
    show --numstat`, never insertions+deletions (DECISION F104 D1) — for every
    commit BEFORE C4, one reading each; none over 500. C4's and C5's own go in the
    round report (§3 item 14).

G13 THE HANDBACK, MEASURED IN BOTH HALVES BECAUSE ONE NUMBER CANNOT REACH BOTH
    COMMITS. This gate is R-0588's counter-measure demonstrated in the round that
    registers it. Report, separately: (a) the `wc -l` reading of `.agent/handoff.md`
    at the commit C4 creates, which constraint 7 bounds at 56 or fewer; and
    (b) the `wc -l` reading at the commit C5 creates, which must equal (a) plus 44
    and be 100 or fewer. If (a) exceeded 56 then C4 carries the DECISION D15
    "Deviations, declared" line and you quote it here; if (a) held, confirm that no
    D15 line was needed and none was written. Then confirm all seven mandated
    headings of docs/agents/handback_template.md are present in the template's
    order, and that no section was dropped. The blob C4 commits is a byte-exact
    PREFIX of the file at C5 and the remainder is byte-equal to VERDICT; that
    measurement can only be taken after C5, so it goes in the round report — which
    is exactly the split this gate exists to teach.

G14 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft`. Report its output. Create nothing,
    merge nothing.

Handback: your completion report with the FULL transcript — every gate's real
command, exit code and output, which is where the transcript belongs (R-0582) —
plus C4's rewrite of `.agent/handoff.md` carrying ONE line per gate, and C5's
append of VERDICT.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN22>>>
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
R22, this session's last: record R21's verdict, register R-0588 — a done-when that
bounded a file measurable only after the last commit while demanding the
declaration be written into the commit before it — and promote that rule onto the
§3 pre-emission checklist, item 14, where a rule has to live to bind the next block.

## Next Steps
1. THE INTEGRATION GATE is the next substantive round and belongs to a session
   with room for it: the full suite per docs/agents/integration_gate.md, branch
   run and base run with `apps/ui/node_modules` and `apps/ui/dist` parity
   restored by COPY, then per-id attribution of every branch-only failure.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH
   review zip, the STATUS line, the PR. The packaging ist-doc is written there,
   when the built state stops moving.
3. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- The base worktree of the integration gate lacks build outputs, so parity is
  restored by COPY and never by symlink, and `apps/ui/dist` is hashed before and
  after that run or the parity claim is void.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN22>>>

<<<SLICE FIND0588>>>
- R-0588 — Low — A DONE-WHEN BOUNDED A FILE AT THE LAST COMMIT WHILE DEMANDING THE DECLARATION BE WRITTEN INTO THE COMMIT BEFORE IT, SO NO HONEST WORKER COULD SATISFY BOTH HALVES. The R21 block, committed at `7f82ad08`, ordered in G14 that `.agent/handoff.md` "at the commit C5 creates is AT MOST 100 lines" and that an overage be declared with a DECISION D15 "Deviations, declared" line rather than by dropping a section. But C5 appends only the reviewer's VERDICT slice; the file's text is written at C4, and at C4 the post-C5 total does not yet exist. Measured over the landed round: the blob `88bf8e7d` commits is 80 lines, VERDICT is 40, `e7cdae4d` is 120, the prefix-and-remainder equality holds exactly, and all seven mandated headings are present in the template's order with no section dropped — so the content obligation was met and only the arithmetic was unreachable. The worker declared the overage with its cause in the round report, noted that the on-disk handoff carries no D15 line, and named amending as forbidden by the same block's history gate; that is the correct handling of a contradiction internal to the reviewer's text. WHAT THE BLOCK SHOULD HAVE DONE, and what this round's own G13 does instead: bound C4 and C5 SEPARATELY, compute the constant the append adds — the block ships VERDICT, so the block knows its length — and fix C4's bound so the sum lands under the cap, which R18's and R19's accepted handbacks achieved at 97 and 96 lines by writing the commits section as ONE table with a per-commit row rather than one table per commit. WHY LOW: nothing false reached disk and nothing was dropped; the cost was one declared deviation and a handoff whose length is stated in the round report instead of in the file. §3 item 14 already forbids a per-commit gate from reaching the handback commit, for exactly this reason — a value that cannot exist while the text is written — and this is the same shape one level up, at the WHOLE-FILE reading rather than the per-commit one, which is why item 14 as worded did not reach it. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: item 14 gains the clause that a bound on a file BUILT BY MORE THAN ONE COMMIT is stated per commit, with the block computing any constant its own appended slices contribute.
<<<END FIND0588>>>

<<<SLICE RECORD20>>>
Gate: R22 — the R21 entry. R21 PASSED, with ONE finding — R-0588, against the reviewer, registered by this round's own FIND0588 slice. Every gate R21's block ordered was re-executed by the reviewer over `e7cdae4d`'s range `a7373e00..e7cdae4d` rather than read from the handback, and every reading reproduces. BOTH OF THE SESSION'S RULES ARE NOW ON DISK IN THE CHECKLIST, which is the round's point: `docs/agents/planner_reviewer_prompt.md` at `e1af7921` is byte-equal to the `a7373e00` blob with CHECK20FROM's single occurrence replaced by CHECK20TO and CHECK26FROM's by CHECK26TO and nothing else changed, at sha256 085c6c830b898e7c3d37590430c943b007e5772b3735c37e5d62b42244c80461 over 805 lines against 773 — and that digest was PREDICTED by the reviewer's pre-emission dry run and matched on landing, which is what makes the transport claim evidence rather than assertion. Each pair is APPEND-shaped with its FROM occurring 1x at both ends, the thirty-two added lines are exactly the two TOs' TO-ONLY lines each once, `grep -c '^  21\. \*\*'` and `grep -c '^  26\. \*\*'` each read 1, the line after CHECK20TO is that item-21 line and the line after CHECK26TO is the checklist's closing paragraph — so item 26 landed between item 25 and that paragraph and nothing was renumbered. R-0586'S OWN GATE HELD WITH ITS CONTROL BITING: over the lines `a4fba89b` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 — 0 before the strip as well — while the same two-step extractor over `fd166295`'s added lines reads 3. R-0587'S GATE HELD IN THE FORM THAT LETS A LANDED DEFECT STAND: at `a7373e00` seventeen headers match `^Gate: R(\d+) — the R(\d+) entry\.` and exactly one string occurs twice, `Gate: R19 — the R18 entry.`; at `a4fba89b` there are eighteen headers, that duplicate SET is unchanged because constraint 3 forbade repairing it, `Gate: R21 — the R20 entry.` occurs once, it is the last such header, and the text after it begins `R20 `. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 169 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 166 open at `a7373e00` and 170 / 3 / 0 / 0 / 0 / 167 at `a4fba89b`, the registered SETS equal, the symmetric difference exactly `['R-0587']`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains `R-0584`. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r21.md`, the committed `.agent/authored/f086-r21.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 7c28f5c828d665ee5c10a52371ce5448c25e1efd24f57a7ee02d0de2aa5c807a, 29051 B over 351 lines — 351 total, 215 prose, 136 slice including 16 marker lines, which is what constraint 7 of that block declares of itself. `.agent/plan.md` equals PLAN22's predecessor PLAN21 over 42 lines, and the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0587, a blank line and RECORD19 at 837f39fd87b59a52fbedc4a6078b4b79e216b3b8b96bde0a0037e9950048263f. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md` or `.agent/handoff.md`. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: exit 0 and 160 passed for the four state readers, then exit 0 and 42 passed for the canary. THE HYGIENE HELD: five paths over seven single-parent commits inserting 351, 256, 16, 4, 32, 41 and 40 lines, none over 500 and no DECISION F104 D1 exemption invoked; `tests/test_install_smoke.py`, `tests/conftest.py`, `pyproject.toml`, `packages/orchestration/ci_stages.py` and `apps/cli/version_report.py` are absent from the range and all five exist at `a7373e00`. WHERE R21 WENT WRONG is in none of the worker's work but in its block's G14, which bounded a file at a commit that only appends while requiring the declaration in the commit that writes; that is R-0588, and this round's G13 measures the same file in the two halves that gate should have had.
<<<END RECORD20>>>

<<<SLICE CHECK14FROM>>>
      and called the range "five single-parent commits" while HEAD held six.
<<<END CHECK14FROM>>>

<<<SLICE CHECK14TO>>>
      and called the range "five single-parent commits" while HEAD held six.
      Finding R-0588 raises this item from the PER-COMMIT reading to the WHOLE-FILE
      one. A bound on a file that MORE THAN ONE commit builds — the handback this
      workflow writes at one commit and appends the reviewer's verdict to at the
      next — is stated per commit and never once over the final state, because the
      final state does not exist when the text that must respect it is written. The
      block computes any constant its own appended slices contribute: it SHIPS that
      slice, so it knows the length, and it fixes the earlier commit's bound as the
      cap minus that constant. The R21 instance: G14 ordered the handoff "at the
      commit C5 creates" to be at most 100 lines AND ordered a DECISION D15 line
      declaring any overage, while C5 appended only the 40-line VERDICT and C4 wrote
      the 80-line text — so the worker met every content obligation, could not have
      known the sum in time to declare it, and had to record the arithmetic in the
      round report instead of in the file. The counter-measure is two readings, not
      a bigger cap: bound the writing commit, bound the appending commit, and state
      which is which.
<<<END CHECK14TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming the branch at `bc85e5f7` and ending
at its declared three-round cap. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on
gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R19 | 7b84524c..bc85e5f7 | PASS — one finding, R-0586, against the reviewer |
| R20 | bc85e5f7..a7373e00 | PASS — one finding, R-0587, against the reviewer |
| R21 | a7373e00..e7cdae4d | PASS — one finding, R-0588, against the reviewer |
| R22 | e7cdae4d..HEAD | verdict not yet on disk; see the last paragraph |

R19 was inherited ungated, so Phase 1 rule 4 reviewed it first. R20 is the round
this feature needed: `tests/test_install_smoke.py` exists, its helpers and its
opt-in skip go red when the code under them is mutated, and its install path is
declared unproven rather than dressed as coverage. R21 put both of the session's
rules into the checklist as mechanical scans, and the reviewer's pre-emission dry
run PREDICTED the edited file's digest, which then matched on landing.

EVERY DEFECT THIS SESSION FOUND WAS THE REVIEWER'S OWN TEXT, and none was in the
workers' execution. R-0586 the reviewer caught by re-reading a landed record;
R-0587 and R-0588 the WORKERS caught, each applying a flawed slice verbatim as its
constraints required and then declaring the problem instead of quietly repairing
it. Three rounds, three reviewer defects, three honest handbacks — the split is
doing the job it exists for, and the checklist is three items richer for it.

WHAT THIS FEATURE STILL OWES: the integration gate, then closure. NO INSTALL HAS
BEEN PROVEN in this session or any other, and no round of this workflow can prove
one — DECISION F086 D4 records that with the measurement behind it, and closure
names it as unproven rather than counting a skipped test as coverage. The release
workflow has likewise never been dispatched.

R22 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `e7cdae4d..HEAD` and record R22's verdict in
`.agent/live_review.md` as `Gate: R23 — the R22 entry.`, the header shape §3 item
26 binds. Its first substantive work is the integration gate.
<<<END VERDICT>>>
