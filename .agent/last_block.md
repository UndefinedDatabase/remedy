── STEP T2/3 — F086 R21 ──────────────────────────────────────

Goal:        Record R20's verdict, register R-0587 — the R20 block's ledger entry
             carried the header of the entry above it — and promote BOTH of this
             session's rules into the §3 pre-emission checklist, where a rule has
             to live to bind the next block.

Bundle:      1. `.agent/plan.md` := PLAN21.
             2. `.agent/live_review.md` += FIND0587, then RECORD19.
             3. `docs/agents/planner_reviewer_prompt.md` += the R-0586 clause at
                the end of §3 item 20, and a new §3 item 26 for R-0587.
             4. The handback, then the session verdict appended to it.

Change:      C0a `.agent/authored/f086-r21.md` := this block, byte-verbatim, the
                 single top separator line included and nothing after the last
                 slice's END marker.
             C0b `.agent/last_block.md` := a mirror of the COMMITTED C0a, read
                 back from git rather than retyped.
             C1  `.agent/plan.md` := PLAN21, whole file. Alone. This is the round's
                 FIRST substantive commit because the bundle moves the finding
                 ledger (§3 item 23).
             C2  `.agent/live_review.md` += a blank line, FIND0587, a blank line,
                 RECORD19. Pure append; nothing already in the file changes.
             C3  `docs/agents/planner_reviewer_prompt.md`: apply BOTH pairs,
                 CHECK20FROM → CHECK20TO and CHECK26FROM → CHECK26TO, in one
                 commit. Nothing else in that file changes.
             C4  `.agent/handoff.md` := your rewrite.
             C5  `.agent/handoff.md` += the VERDICT slice, appended verbatim.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r21.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`, and
   `.agent/handoff.md` at C4 and C5. NOT `tests/test_install_smoke.py`, not
   `tests/conftest.py`, not `pyproject.toml`, not
   `packages/orchestration/ci_stages.py`, not `apps/cli/version_report.py`, and
   nothing else under `apps/`, `packages/`, `tests/`, `docs/roadmap/` or
   `.github/`. Every path this constraint FORBIDS exists at `a7373e00`, so the
   prohibition forbids something real (R-0559).
3. THE LANDED LEDGER IS NOT REWRITTEN. R-0587 is a mislabelled header already on
   disk at `4dc7cbdf`. §3 item 20 rules that the counter-measure for landed text
   is a dated correction in NEW text, never a rewrite, because overwriting the
   record is worse than a dated wrong line. You append; you do not touch that
   paragraph, and G7 is written so that the duplicate it left behind is expected
   rather than forbidden.
4. PLAN21, FIND0587, RECORD19, CHECK20TO, CHECK26TO and VERDICT are the
   reviewer's text. Do not summarise or reformat them, and do not write a verdict
   of your own anywhere — in the handoff, in a commit message, or in your report.
   Reporting what a gate MEASURED is your job; ruling on a round is not.
5. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback, and `git worktree list` reads one line throughout. This round
   orders NO mutation and NO disposable worktree: it writes no code, so there is
   nothing to red-prove, and inventing a mutation to look thorough would prove
   nothing about a documentation edit.
6. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
7. SIZE, measured at emission on the final bytes: this block is 351 lines TOTAL —
   215 prose and 136 slice including its 16 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`;
    `git worktree list` one line throughout, per constraint 5.

G2  TRANSPORT. `.remedy-wt/f086-r21.md`, the committed
    `.agent/authored/f086-r21.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at the commit C1 creates is byte-equal to the PLAN21
    slice extracted from the COMMITTED `.agent/authored/f086-r21.md`. Report its
    full sha256 and line count, confirm the count is under 50, and confirm it
    contains `## Goal`, `## Next Steps` and `F086`.

G4  THE LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to a blank line,
    FIND0587, a blank line, RECORD19, in that order. Report the remainder's own
    full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At the commit C2 creates report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Expected there: 170 registered, 3
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:` lines, 167
    open. Report the symmetric difference of that registered set against the
    `a7373e00` set AS THE SET; it must be exactly `['R-0587']`.
    CONTROL: the SAME extractor over `f0b27118..7b84524c` must read `[]` for the
    registered symmetric difference while its RESOLVED set gains exactly `R-0584`,
    so the extractor is measured on a range that moved a resolution and not a
    registration.

G6  THE R-0586 RULE, ON THE TEXT THIS ROUND LANDS. Take the lines C2's diff ADDS
    to `.agent/live_review.md`. FIRST delete every backtick-quoted span from them
    — the regex `` `[^`]*` `` — because a token this finding QUOTES is not a token
    it USES (R-0584 class). THEN count `\bHEAD\b` in what remains; the count must
    be 0. RED CONTROL: the SAME two-step extractor over the lines `fd166295`'s
    diff ADDS to that same file reads 3. Report both numbers.
    THIS GATE BINDS THE LEDGER COMMIT AND NOTHING ELSE, deliberately. VERDICT
    lands in `.agent/handoff.md`, a file this workflow REWRITES every round rather
    than appends to, and its range row names `a7373e00..HEAD` by the R10-onward
    convention that a handoff cannot name the SHA of the commit that writes it —
    so neither this gate nor the item-20 clause C3 lands reaches that row, and
    neither is meant to. Do not "fix" it and do not report it as a violation.

G7  THE R-0587 RULE, ON THE ENTRY THIS ROUND LANDS, WITH THE LANDED DUPLICATE
    LEFT STANDING. Collect every header matching `(?m)^Gate: R(\d+) — the R(\d+)
    entry\.` in `.agent/live_review.md`. At `a7373e00` exactly one header string
    occurs more than once, and it is `Gate: R19 — the R18 entry.` — report that
    reading first, because it is the RED CONTROL that proves the extractor sees a
    duplicate at all. At the commit C2 creates, the set of header strings
    occurring more than once must be UNCHANGED — still exactly that one string,
    because constraint 3 forbids repairing it — and additionally: the header
    `Gate: R21 — the R20 entry.` occurs exactly 1x, it is the LAST such header in
    the file, and the text immediately following it begins `R20 `. Report all
    four readings. This gate is R-0587's counter-measure demonstrated in the round
    that registers it, and item 26 is the promotion, which C3 of this same block
    orders (§3 item 11).

G8  THE TWO PAIRS, each classified by a containment test whose OUTPUT you print
    (§3 item 15). For each pair separately, in
    `docs/agents/planner_reviewer_prompt.md`, print the literal words
    `TO contains FROM: true` or `TO contains FROM: false`, and derive the APPEND
    or REWRITE label from that output on the same line — never write the label on
    its own. Both are expected APPEND-shaped, so the obligation is §4.9's append
    form and NOT a FROM-zero count: for each pair report FROM occurring exactly 1x
    at `a7373e00` AND exactly 1x at the commit C3 creates — that is what an append
    means and it is not a defect — and each TO-ONLY line occurring exactly 1x
    among the lines C3's diff ADDS. Then the ORDERED-EQUALITY reading over the
    whole file: at the commit C3 creates the file is byte-equal to the `a7373e00`
    blob with CHECK20FROM's single occurrence replaced by CHECK20TO and
    CHECK26FROM's single occurrence replaced by CHECK26TO, and nothing else
    changed. Report the file's full sha256 and line count there, and the line
    count at `a7373e00`, which is 773.

G9  BOTH EDITS LANDED WHERE THEY WERE AIMED AND RENUMBERED NOTHING. At the commit
    C3 creates: `grep -c '^  21\. \*\*' docs/agents/planner_reviewer_prompt.md`
    reads 1 and `grep -c '^  26\. \*\*' ...` reads 1; the line immediately
    following CHECK20TO's last line is that item-21 line; and the line immediately
    following CHECK26TO's last line is
    `  Why this is on disk and not a habit: item 2 has recurred six times across`.
    Report all four readings verbatim. This is the structural check the pair proof
    cannot give: ordered equality would also hold for text that landed in the
    wrong item if the bytes happened to match, and this one names where.

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

G12 CHANGE SET. `git diff --name-only a7373e00..HEAD` before C4 prints the paths
    constraint 2 NAMES other than `.agent/handoff.md`. Report the list it prints
    and the list constraint 2 names, and compare them AS SETS — state no numeral
    for either. Confirm with `git ls-tree a7373e00 -- <path>` that every path
    constraint 2 FORBIDS exists at that base, and report those readings.

G13 HISTORY AND COMMIT SIZE. Every commit in `a7373e00..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Walk the range with
    `git rev-list --reverse` and report the INSERTION count — the `+` column of
    `git show --numstat`, never insertions+deletions (DECISION F104 D1) — for
    every commit BEFORE C4, one reading each; none over 500. C4's and C5's own go
    in the round report (§3 item 14).

G14 THE HANDBACK, ITS APPEND, AND THE PR GATE. `.agent/handoff.md` at the commit
    C5 creates is AT MOST 100 lines and carries all seven mandated headings of
    docs/agents/handback_template.md in the template's order; report the `wc -l`
    reading and the heading list, and if it exceeds 100 declare the DECISION D15
    overage with its cause rather than dropping a section. The blob C4 commits is
    a byte-exact PREFIX of the file at the commit C5 creates and the remainder is
    byte-equal to VERDICT; that measurement can only be taken after C5, so it goes
    in the round report. Then re-read the Open PR Gate: `gh pr list --state open
    --json number,headRefName,baseRefName,isDraft`. Report its output. Create
    nothing, merge nothing.

Handback: your completion report with the FULL transcript — every gate's real
command, exit code and output, which is where the transcript belongs (R-0582) —
plus C4's rewrite of `.agent/handoff.md` carrying ONE line per gate, and C5's
append of VERDICT.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN21>>>
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
R21, this session's last: record R20's verdict, register R-0587 — a ledger entry
that carried the header of the entry above it — and promote both of this session's
rules into the §3 pre-emission checklist, item 20 and a new item 26.

## Next Steps
1. THE INTEGRATION GATE is the next substantive round: the full suite per
   docs/agents/integration_gate.md, run once before closure. A regression there is
   a normal repair round, not a closure blocker.
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
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN21>>>

<<<SLICE FIND0587>>>
- R-0587 — Medium — AN AUTHORED LEDGER ENTRY CARRIED THE HEADER OF THE ENTRY ABOVE IT, SO `.agent/live_review.md` NOW HOLDS TWO PARAGRAPHS UNDER ONE KEY. RECORD18, committed at `4dc7cbdf`, records R19's verdict and opens `Gate: R19 — the R18 entry. R19 PASSED, with ONE finding — R-0586`. Every other entry in that file follows `Gate: R<this round> — the R<previous round> entry. R<previous round> …`, and the entry immediately above RECORD18 already opens with that identical string, so the correct header was `Gate: R20 — the R19 entry.` and the landed one is both wrong and a byte-for-byte duplicate. Measured at `a7373e00` over the seventeen headers matching `^Gate: R(\d+) — the R(\d+) entry\.`: the convention holds for the sixteen entries R3 through R19 and breaks only on this one, and exactly one header string occurs more than once. THE INSTRUCTION EXISTED AND WAS ON DISK: the `## Next` section of the handback at `bc85e5f7` names the required string, `Gate: R20 — the R19 entry`, so this is not a rule the reviewer had to derive — it is one the reviewer wrote down one round earlier and then did not apply to its own slice. WHY MEDIUM rather than Low, unlike R-0586: a header is the key a later reader and §4.13's terminator reasoning search by, and a duplicated key makes the record ambiguous rather than merely stale — a search for the R19 verdict lands on the R18 entry, and the paragraph that holds the R19 verdict does not announce itself as such. WHY NO GATE CAUGHT IT: the R20 block's G4 gates BYTES and its G5 gates IDS, and the entry is byte-perfect and id-perfect; nothing the block ordered read the slice's SHAPE against the shape of its neighbours. THE WORKER HANDLED IT CORRECTLY and that is worth recording: constraint 1 forbade editing a slice and constraint 3 forbade a worker verdict, so it applied the bytes verbatim, declared the discrepancy in its handback's Deviations section and ruled on nothing — which is exactly what an honest worker does with a reviewer defect. COUNTER-MEASURE, split so neither half overclaims: the landed entry is NOT rewritten, because §3 item 20 rules that overwriting the record is worse than a dated wrong line and this paragraph is that dated correction; this round's own G7 requires the duplicate SET to be unchanged while its new entry is headed `Gate: R21 — the R20 entry.` exactly once and last; and C3 of this same block promotes the rule into the checklist as item 26.
<<<END FIND0587>>>

<<<SLICE RECORD19>>>
Gate: R21 — the R20 entry. R20 PASSED, with ONE finding — R-0587, against the reviewer, registered by this round's own FIND0587 slice. Every gate R20's block ordered was re-executed by the reviewer over `bc85e5f7..a7373e00` rather than read from the handback, and every reading reproduces. THE FEATURE MOVED: `tests/test_install_smoke.py` is created by `724882f2` and is byte-EQUAL to the block's SMOKE slice at sha256 ea84a2f5233b277e7b9fbd0bac3c77447885d4110b8d5e2d9bf668a09ef83f61 over 220 lines, and `git ls-tree bc85e5f7 -- tests/test_install_smoke.py` prints nothing, so the round CREATED it and the §4.9 ordered-equality obligation for a code slice reduces to whole-file equality rather than to a per-line count (R-0531). THE MODULE IS REAL AND ITS SKIP IS REAL: re-run by the reviewer in the primary checkout, `python3 -m pytest tests/test_install_smoke.py -q -rs` exits 0 with 14 passed and 1 skipped, the one skip being the install test, its reason naming `REMEDY_INSTALL_SMOKE`; and both `python3 -m ruff check` and `python3 -m ruff check --preview` exit 0 over that path. THE RED PROOFS REACHED THE CODE, which is what makes the module more than a file: mutating the opt-in helper to `return False` failed only `TestInstallSmokeOptIn::test_any_other_value_enables_it`, and disabling the build-root guard failed only `TestBuildRootLiesOutsideTheRepository::test_a_path_inside_the_repository_is_refused` and `::test_the_repository_root_itself_is_refused`, with the install test still SKIPPING in both — mutations chosen so the logic can go red while no install is ever attempted. NOTHING IN THIS ROUND PROVED AN INSTALL and the block said so before it ran: `REMEDY_INSTALL_SMOKE` stayed unset everywhere, no wheel was built, no venv created, no network reached, and DECISION F086 D4 already records that F086's DONE condition stays UNPROVEN until that variable is set on a host that can honour it. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 168 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 165 open at `bc85e5f7` and 169 / 3 / 0 / 0 / 0 / 166 at `4dc7cbdf`, the registered SETS equal, the symmetric difference exactly `['R-0586']`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains `R-0584`. R-0586'S OWN GATE HELD AND ITS CONTROL BIT: over the lines `4dc7cbdf` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 where 6 occur before the strip, while the same extractor over `fd166295`'s added lines reads 3. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r20.md`, the committed `.agent/authored/f086-r20.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 c88049f01e95e66db81fcbb778cde3a93746525eac864d9264876ff0f30b9231, 32032 B over 482 lines — 482 total, 212 prose, 270 slice including 8 marker lines, which is what constraint 7 of that block declares of itself. `.agent/plan.md` equals PLAN21's predecessor PLAN20 at 2043155c37445fb5ce7823556623299110c56c5da674af789b9a11194ba5453c over 40 lines, and the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0586, a blank line and RECORD18 at 7a4502ccf0774f4d941d77b6aebe98bbd1bc1b1851b564ca6dc9d276417bf23b. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md` or `tests/test_install_smoke.py`. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: exit 0 and 24 passed for the guards a new test FILE could trip, exit 0 and 160 passed for the four state readers, exit 0 and 42 passed for the canary. THE HYGIENE HELD: five paths over six single-parent commits inserting 482, 406, 7, 4, 220 and 60 lines, none over 500 and no DECISION F104 D1 exemption invoked; `tests/conftest.py`, `pyproject.toml`, `packages/orchestration/ci_stages.py`, `apps/cli/version_report.py`, `hatch_build.py` and `tests/test_packaging_smoke.py` are absent from the range and all six exist at `bc85e5f7`. THE HANDBACK CAME IN UNDER ITS CAP at 81 lines against 100, all seven mandated headings in the template's order, one line per gate with the transcript in the round report — the sixth round running that the R-0582 repair has held. WHERE R20 WENT WRONG is in none of its own gates and in none of the worker's work, but in the header of the entry it was told to land; that is R-0587, and this entry is written in the form that finding requires.
<<<END RECORD19>>>

<<<SLICE CHECK20FROM>>>
      copy two commits earlier — four of the five matched, and the sentence claimed five.
<<<END CHECK20FROM>>>

<<<SLICE CHECK20TO>>>
      copy two commits earlier — four of the five matched, and the sentence claimed five.
      Finding R-0586 adds the mechanical scan this item has always described and nothing
      has ever run. Before emission every slice bound for an append-only record is searched
      for the labels this item forbids: delete each backtick-quoted span first — a token a
      finding QUOTES is not a token it USES, and a guard that cannot tell the two apart is
      satisfied by the quotation (R-0584 class) — then require ZERO matches of `\bHEAD\b`
      in what remains. `main` and `origin/main` are INSPECTED rather than counted to zero,
      because both also occur as ordinary prose and a zero-gate over them is unmeetable —
      the R-0563 shape, where a sweep stated too widely protects nothing. Measured at
      `bc85e5f7`, the `Gate:` entries of `.agent/live_review.md` from R10 through R19
      carried 3, 2, 2, 6, 3, 1, 1, 0, 4 and 3 unquoted occurrences in that order, every one
      but R17's carrying at least one: a rule stated for four rounds and broken under
      itself, because nothing measured it. Those landed entries are NOT rewritten — the
      counter-measure above is the dated correction — and this scan binds only text that
      has not yet been written.
<<<END CHECK20TO>>>

<<<SLICE CHECK26FROM>>>
      gate NAMES; this one resolves the BYTES a gate orders CHANGED.
<<<END CHECK26FROM>>>

<<<SLICE CHECK26TO>>>
      gate NAMES; this one resolves the BYTES a gate orders CHANGED.
  26. **A slice joining a file's repeating record format is read against the entries it
      joins.** Finding R-0587. When an authored slice appends an entry to a file whose
      existing entries share a header shape — the `Gate: R<n> — the R<n-1> entry.` lines of
      `.agent/live_review.md`, a changelog's version headings, any keyed series — the
      slice's own header is compared MECHANICALLY against the headers already in that file
      before emission, as a pattern match and never by eye. Items 11 and 16 govern numerals
      a block states about its own text and about a list it names, and item 20 governs a
      fact about a file's CONTENT; none of them reads a slice's SHAPE against the shape of
      its neighbours, which is where R-0587 landed. The R20 instance: RECORD18 was headed
      `Gate: R19 — the R18 entry.` while its body recorded R19 at R20, so the header
      duplicated the entry directly above it byte for byte and the ledger gained two
      paragraphs answering to one key — and the handback of the round before had already
      named the correct string. No gate the block ordered could see it, because those gates
      measured bytes and ids and the entry was perfect in both; the worker applied it
      verbatim, as constraint 1 required, and declared it. A header is the key a later
      reader searches by, so a duplicated one costs more than a stale sentence: order the
      comparison before emission, and never repair it by rewriting the landed entry, which
      item 20 forbids.
<<<END CHECK26TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming the branch at `bc85e5f7` and ending
at its declared round cap. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on
gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R19 | 7b84524c..bc85e5f7 | PASS — one finding, R-0586, against the reviewer |
| R20 | bc85e5f7..a7373e00 | PASS — one finding, R-0587, against the reviewer |
| R21 | a7373e00..HEAD | verdict not yet on disk; see the last paragraph |

R19 was inherited ungated, so Phase 1 rule 4 reviewed it first. Its checklist edit
landed inside item 16 and moved nothing else, and the reviewer re-ran the claim
that commit rests on rather than repeating it. R20 is the round this feature
needed: `tests/test_install_smoke.py` exists, its pure helpers and its opt-in skip
are gated by tests that go red when the code under them is mutated, and its
install path is honestly declared as unproven rather than dressed as coverage.
Both rounds' defects were the reviewer's own text, not the worker's work, and both
were caught — R-0586 by the reviewer re-reading a landed record, R-0587 by the
WORKER, which applied a bad slice verbatim as its constraints required and then
declared it instead of quietly repairing it. That is the split working as designed.

WHAT THIS FEATURE STILL OWES: the integration gate, then closure. NO INSTALL HAS
BEEN PROVEN in this session or any other, and no round of this workflow can prove
one — DECISION F086 D4 records that with the measurement behind it, and closure
names it as unproven rather than counting a skipped test as coverage. The release
workflow has likewise never been dispatched.

R21 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `a7373e00..HEAD` and record R21's verdict in
`.agent/live_review.md` as `Gate: R22 — the R21 entry.`, which is the header
shape §3 item 26 now binds.
<<<END VERDICT>>>
