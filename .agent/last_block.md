── STEP findings + checklist — F086 R25 ──────────────────────
Goal:
Record R24's verdict, register the one defect R24's review exposed — a mandated
handback column that no gate reaches, which carried one commit's diff twice and
got it wrong once — and promote its counter-measure onto the §3 pre-emission
checklist as a new item 28, which is the only place a rule in this repository
binds the next block. This round writes no production code and runs no suite of
its own beyond the canary.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R25 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0592 and RECORD24.
4. `docs/agents/planner_reviewer_prompt.md` gains item 28 in ONE commit, appended
   after item 27's last line and BEFORE the paragraph beginning "Why this is on
   disk and not a habit", so nothing is renumbered and no existing item moves.
5. The handback, then the reviewer's VERDICT appended to it.

Change:
Exactly these paths:
  `.agent/authored/f086-r25.md`            (C0a)
  `.agent/last_block.md`                   (C0b)
  `.agent/plan.md`                         (C1)
  `.agent/live_review.md`                  (C2)
  `docs/agents/planner_reviewer_prompt.md` (C3)
  `.agent/handoff.md`                      (C4, then C5)
Nothing else. In particular NOT `.agent/gate_f086_r23/attribution.txt`, not
`tests/test_install_smoke.py`, not `tests/conftest.py`, not `pyproject.toml`, not
`packages/orchestration/ci_stages.py`, not `docs/roadmap/STATUS.md`, not
`.github/workflows/release.yml`, and nothing else under `apps/`, `packages/`,
`tests/`, `docs/roadmap/` or `.github/`. Every path this paragraph FORBIDS exists
at `e33ba23a` — resolved with `git cat-file -e` at emission per §3 item 24 — so
the prohibition forbids something real.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.
   R23 declared three such problems and was right to; that is the system working.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is, and so does every
   word of `.agent/handoff.md` as committed at `fa9512a8` and `e33ba23a` — the
   very file whose wrong column this round registers. §3 item 20 rules that the
   counter-measure for landed text is a dated correction in NEW text. You append
   only. G7 is written so the R19 duplicate is EXPECTED rather than forbidden,
   and a gate that reported it as a violation would be the defect.

4. PLAN25, FIND0592, RECORD24, the CHECK28 pair and VERDICT are the reviewer's
   text. Do not summarise, rewrap or reformat them. Do not write a verdict of
   your own anywhere — not in the handoff, not in a commit message, not in your
   report. Reporting what a gate MEASURED is your job; ruling on a round is not.
   A worker-authored `Done:` paragraph is a finding however honestly it is
   hedged (§4.4).

5. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line throughout.
   This round orders NO mutation and NO disposable worktree: it edits documents
   and a record, so there is nothing to red-prove, and inventing a mutation to
   look thorough would prove nothing about a documentation edit.

6. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals and env-prefix command forms. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`. Capture
   pytest exit codes with `subprocess.run(...).returncode`, never with `$?`.

7. THE CHECK28 PAIR IS APPEND-SHAPED and lands in ONE commit, C3. The
   containment test was run at emission and printed `TO contains FROM: True`, so
   §4.9's APPEND obligation applies and a "FROM 0x" count is unattainable by
   construction and must not be attempted. CHECK28FROM occurs exactly 1x in the
   file at `e33ba23a`, verified at emission.

8. THE HANDBACK'S ARITHMETIC IS STATED ONCE, HERE, AND NOWHERE ELSE — §3 item
   14's sweep rule, which R-0589 added. The VERDICT slice this block ships is 39
   lines, measured at emission on its final bytes, and C5 appends it by pure
   concatenation, so the file at C5 is exactly C4's length plus 39. KEEP C4 AT 60
   LINES OR FEWER, which puts C5 at 99 or fewer with no DECISION D15 overage to
   declare. Write C4 in the COMPACT form: ONE commits table with a per-commit
   row, ONE LINE PER GATE in the Verification section, the transcript going to
   your round report and not into the file (R-0582). G13 below NAMES this
   constraint instead of restating its numerals, deliberately: measured at
   emission, `39`, `60` and `99` occur in this constraint and in no other clause
   of this block, so there is no second copy to fall out of step. If C4
   nevertheless lands above that bound, do NOT drop a mandated section — exceed
   the cap, write the DECISION D15 "Deviations, declared" line naming the real
   count and the mandated content that caused it, and say so in the report.

9. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION — this is R-0592's own
   counter-measure applied to the block that registers it. Every `+/-` cell you
   write in the handback's `## Commits` table is READ OUT of `git diff --numstat
   <sha>^ <sha>` for that commit and pasted from that reading. Do not derive a
   cell from a file's line count before and after: for a full-file rewrite those
   two numbers differ from the diff columns by exactly the lines the two versions
   share, which is what went wrong at R24.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 5's two
   readings both taken and both reported.

G2 TRANSPORT. `.remedy-wt/f086-r25.md`, the committed `.agent/authored/f086-r25.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN25 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND. The pre-C2 `.agent/live_review.md` blob is a byte-exact PREFIX
   of the post-C2 blob, and the remainder is byte-equal to a blank line, FIND0592,
   a blank line and RECORD24 — both extracted from the committed C0a. Report the
   remainder's sha256 and line count.

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = lines matching `^- R-\d+ — `; resolved = lines matching
   `^Done: R-\d+ — `. Report at `e33ba23a` and at C2: registered count, resolved
   count, duplicate count, unregistered-resolution count, `Landed:` line count and
   open count. The RESOLVED set must be UNCHANGED between the two — this round
   resolves nothing — and the REGISTERED set must gain exactly `R-0592` and
   nothing else. CONTROL, which must MOVE so the reading is not vacuous: the same
   two extractions over `f0b27118..7b84524c` report `[]` registered while the
   resolved set gains exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST — a token a finding QUOTES is not a token it USES
   (R-0584) — then count `\bHEAD\b` in what remains. It must read 0. RED CONTROL,
   same two-step extractor over the lines `fd166295` adds to the same file: it must
   read 3. A control that does not read 3 means the extractor is broken and the 0
   proves nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `e33ba23a` and at C2, and
   the SET of strings occurring more than once at each. That duplicate set must be
   UNCHANGED and must be exactly `Gate: R19 — the R18 entry.` — constraint 3
   forbids repairing it, so it is the expected reading. Then: `Gate: R25 — the R24
   entry.` occurs exactly 1x, it is the LAST such header in the file, and the text
   immediately following it begins `R24 `.

G8 THE CHECK28 PAIR, PROVED IN THE APPEND FORM (§4.9), never as a FROM-zero count.
   Print the containment test's own output, confirm CHECK28FROM occurs exactly 1x
   at `e33ba23a` AND exactly 1x at C3. Then the ORDERED EQUALITY: the file at C3 is
   byte-equal to the `e33ba23a` blob with CHECK28FROM's single occurrence replaced
   by CHECK28TO and nothing else changed. Report C3's sha256 and line count against
   the base's 865.

G9 STRUCTURE, which is what proves nothing was renumbered.
   `grep -c '^  26\. \*\*'`, `grep -c '^  27\. \*\*'` and `grep -c '^  28\. \*\*'`
   over `docs/agents/planner_reviewer_prompt.md` at C3 each read 1. Report the line
   that FOLLOWS CHECK28TO's last line: it is the line beginning
   `  Why this is on disk and not a habit:`.

G10 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md` and
    `docs/agents/planner_reviewer_prompt.md` at C4: each must be 0. Count marker
    LINES, not substrings — this handback quotes gate text, so a substring gate
    over `.agent/handoff.md` would be unmeetable (F086 R5). The `.agent/handoff.md`
    reading can only be taken after C5 and goes in the round report.

G11 SUITES, serially in the PRIMARY checkout, the second started only after the
    first has ENDED and reported its exit code (F085 R64: two concurrent pytest
    processes produce false reds here). First `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, then the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both exit codes
    and both summary lines. NOTE, so the handback does not claim more than it
    proves: no suite in this repository reads
    `docs/agents/planner_reviewer_prompt.md`, so G8 and G9 are C3's whole evidence
    and a green suite says nothing about it.

G12 CHANGE SET AND HISTORY, AND THE TABLE ITSELF. Print the range's path set and
    confirm it equals the Change list above, with no path on either side alone.
    Confirm every path the Change section FORBIDS is PRESENT at `e33ba23a`.
    Confirm the range is linear — every commit at exactly one parent — and that
    the round's `git reflog` entries are all `commit:`. Then, per constraint 9:
    for every commit BEFORE C4 print `git diff --numstat <sha>^ <sha>` and confirm
    each `+/-` cell of the handback's `## Commits` table is byte-identical to the
    numstat pair for that commit, with the insertion column alone checked against
    the 500 cap (DECISION F104 D1). C4's and C5's own rows cannot be measured
    before they exist (§3 item 14) and are reported in the round report instead.

G13 THE HANDBACK, BOTH HALVES, per §3 item 14. Report `wc -l` of
    `.agent/handoff.md` at C4 and again at C5, and confirm each against the bound
    CONSTRAINT 8 states for it — this gate deliberately names that constraint
    rather than restating its numerals. All seven mandated headings of
    docs/agents/handback_template.md are present in the template's order and no
    section is dropped. The prefix-and-remainder equality against VERDICT is
    measurable only after C5 and goes in the round report.

G14 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Then
append VERDICT verbatim as C5. Push the branch once, after C5.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN25>>>
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
R25: record R24's verdict, register R-0592 — the handback's mandated `## Commits`
table carries a `+/-` column no gate reaches, and at R24 one row of it disagreed
with `git diff --numstat` and with the same file's own gate line — and promote its
counter-measure onto the §3 checklist as item 28, where a rule has to live to
bind the next block.

## Next Steps
1. THE INTEGRATION GATE IS DONE and it is GREEN: at R23 the branch full suite ran
   17192 passed / 20 skipped / 0 failed, the branch-only failure set was EMPTY, and
   all 23 base-only ids were attributed to the throwaway worktree's missing build
   artefacts by demonstration at `76661dc1`. Evidence: `.agent/gate_f086_r23/`.
2. CLOSURE is the next substantive round, per docs/roadmap/STATUS_closure_protocol.md
   — evidence job, FRESH review zip, the STATUS line, the PR. The packaging ist-doc
   is written there, when the built state stops moving.
3. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has yet paid
  down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN25>>>

<<<SLICE FIND0592>>>
- R-0592 — Low — A MANDATED HANDBACK COLUMN THAT NO GATE REACHES CARRIED ONE COMMIT'S DIFF TWICE AND GOT IT WRONG ONCE. docs/agents/handback_template.md requires a `## Commits` changed-files table with a `+/-` column for EVERY commit in the range. The R24 handback, committed at `fa9512a8`, filled that column correctly for four of its five measurable commits — `+380/-0`, `+17/-16`, `+8/-0`, `+45/-0`, each byte-identical to `git diff --numstat` — and wrote `+380/-334` for the block-mirror commit `d08af133`, where the real numstat is `270  224`. 380 and 334 are the line COUNTS of `.agent/last_block.md` after and before that commit; the diff columns differ from them by exactly the 110 lines the two versions share, because the R24 block and the R23 block it replaced hold long identical runs. THE SAME FILE ALREADY HELD THE RIGHT NUMBER: its G12 line reports the round's insertions as `380, 270, 17, 8, 45`, using 270 for that very commit, so one handback stated one commit's insertion count twice, by two different derivations, and the two disagreed. WHY LOW: nothing downstream consumed the wrong pair. The cap reading is unaffected — 270 and 380 are both under the 500 of DECISION F104 D1 — the transport proof at G2 is independent and exact, and the round's verdict does not rest on the table. WHY IT IS A FINDING AT ALL: `.agent/handoff.md` is the map AGENTS.md's Session Resume tells the next session to read SECOND, and a wrong `+/-` there is the input to the next round's split-or-not arithmetic; the block-save commit is precisely where it misleads, because `.agent/last_block.md` is the one path in this workflow whose commit is a full-file rewrite rather than an append, and memory of that rule is exactly what R-0399 says cannot be trusted. THE GAP IS THE GATE, NOT THE WORKER: R24's G12 ordered "report each commit's INSERTION count", the worker reported all five correctly in the Verification section, and NO clause of that block, and no item of the §3 checklist, ever named the TEMPLATE's table as a place the same value lands. Item 22 binds a sentence the reviewer writes about a range; item 14 binds a constant the block computes for itself; neither reaches a value the worker derives a second time to fill a section the template mandates. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: a new checklist item 28 requires a block that orders a measurement which docs/agents/handback_template.md independently carries to name that mandated section as where the value lands, and to order the two readings compared.
<<<END FIND0592>>>

<<<SLICE RECORD24>>>
Gate: R25 — the R24 entry. R24 PASSED with ONE finding, R-0592, and that finding is against the reviewer's gate coverage rather than against the worker's execution. Every gate R24's block ordered was RE-EXECUTED by the reviewer over `39bfc199..e33ba23a` rather than read from the handback, and every reading reproduces to the byte. THE TRANSPORT HELD in the primary three-way form: the scratchpad, the committed `.agent/authored/f086-r24.md` at `abc56562` and the committed `.agent/last_block.md` at `d08af133` are byte-EQUAL at sha256 4c044d5ef995da602dcb9d20493e25371f2e2785a30ac6a167902a50bfcd7bc2, 33340 B over 380 lines. EVERY SLICE LANDED BYTE-EXACT, each checked disk-to-disk against an extraction from the COMMITTED C0a by an extractor the reviewer wrote independently: `.agent/plan.md` at `5d48bb86` equals PLAN24 at sha256 39c58c704bdcd5cdda26b429fa1d4b76545118447a11cc1f14aaa0fef3692956 over 45 lines, under the AGENTS.md cap of 50 and carrying `## Goal`, `## Next Steps` and `F086`; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 8-line remainder equals a blank line, FIND0589, a blank line, FIND0590, a blank line, FIND0591, a blank line and RECORD22 at sha256 b88bbb56c685f7885b3190c2fbae27b499d513b6fbbf25a078d582c5605f786f over 10781 B; and the three checklist pairs satisfy the ORDERED EQUALITY in the append form — `docs/agents/planner_reviewer_prompt.md` at `f33ac247` is byte-equal to the `39bfc199` blob with each of CHECK14FROM, CHECK18FROM and CHECK27FROM replaced by its TO and nothing else changed, 820 lines to 865 at sha256 15b6332a1422d83d302a7b538e8ef7b11779c72bfea52da9b610cffe59fe2eb4. NOTHING WAS RENUMBERED: items 14, 15, 18, 19, 26 and 27 each match exactly once, and each TO is followed by the line the block named. THE LEDGER MOVED ONLY ON THE REGISTERED SIDE: both extractions AGREE at each end — 171 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 167 open at `39bfc199`, and 174 / 4 / 0 / 0 / 0 / 170 at `0434d7bb` — the resolved set is equal, the registered set gains exactly `R-0589`, `R-0590` and `R-0591`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. R-0586'S SCAN HELD WITH ITS CONTROL BITING: over the lines `0434d7bb` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0, while the same two-step extractor over `fd166295`'s added lines reads 3. R-0587'S CHECK HELD IN THE FORM THAT LETS A LANDED DEFECT STAND: the duplicated-header set is unchanged and is exactly `Gate: R19 — the R18 entry.`; `Gate: R24 — the R23 entry.` occurs 1x, is the LAST such header, and the text after it begins `R23 `. THE SUITES ARE GREEN ON THE REVIEWER'S OWN RUNS, taken serially: 160 passed at exit 0, then the canary 42 passed at exit 0, matching the worker's two runs. THE HYGIENE HELD: six paths over seven single-parent commits, all seven paths the block FORBIDS present at `39bfc199` and none touched, nothing under `apps/`, `packages/`, `tests/`, `docs/roadmap/` or `.github/` in the range, every `git reflog` entry of the round `commit:`, no marker LINE in any target, `git worktree list` one line, the tree clean and `origin` holding the same commit. THE HANDBACK IS 52 LINES AT C4 AND 99 AT C5, the first a byte-exact prefix of the second with a 47-line remainder byte-equal to VERDICT, all seven mandated headings present in the template's order, and constraint 8's own arithmetic — the R-0589 counter-measure applied to the block that registered it — held exactly. WHERE R24 FELL SHORT IS IN ONE PLACE AND IT IS THE REVIEWER'S: the `+/-` cell for `d08af133` reads `+380/-334` where the numstat is `270  224`, the file's line counts standing in for the diff columns, while the same handback's G12 line reports 270 for that commit — a mandated template column that no gate of that block and no item of the checklist ever named (R-0592).
<<<END RECORD24>>>

<<<SLICE CHECK28FROM>>>
      the round rescuing the reviewer rather than the gate doing its job.
<<<END CHECK28FROM>>>

<<<SLICE CHECK28TO>>>
      the round rescuing the reviewer rather than the gate doing its job.
  28. **A measurement the handback template ALSO carries is gated where the template
      puts it.** Finding R-0592. When a block orders a value that
      docs/agents/handback_template.md independently requires in a mandated section —
      the `+/-` column of the `## Commits` table, a path set, a file's line count —
      the gate NAMES that section as the place the value lands and orders the two
      readings compared, cell by cell, against the tool that produced them. A value
      the worker must write twice will be derived twice, and the second derivation is
      not covered by a gate that only says "report it": the Verification line can be
      exactly right while the table beside it is wrong, and the table is the half a
      later session reads. Item 22 binds a sentence the REVIEWER writes about a range
      and item 14 a constant the BLOCK computes for itself; neither reaches a number
      the WORKER re-derives to fill a section the template mandates, which is the
      third writer of the same value. The R24 instance: G12 ordered each commit's
      insertion count reported, the worker reported all five correctly, and the
      `## Commits` row for the block-mirror commit read `+380/-334` — the file's line
      counts after and before — where `git diff --numstat` reads `270  224`, the two
      differing by exactly the lines the old and new block share. Full-file rewrites
      are where this bites, because only there do the counts and the columns diverge.
<<<END CHECK28TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming at `e33ba23a` under a three-round cap
declared up front per guardrail G7. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and the verdict below rests on gates the
reviewer RE-EXECUTED over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R24 | 39bfc199..e33ba23a | PASS — one finding, R-0592, against the reviewer |
| R25 | e33ba23a..this range | verdict not yet on disk; see the last paragraph |

R24 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was
planned. All fourteen of its gates reproduce to the byte on the reviewer's own runs:
the three-way transport digest, PLAN24, the eight-line ledger remainder, the ordered
equality over the three checklist pairs, both ledger extractions with the control
moving, the item-20 scan with its red control reading 3, the header check, and both
suites green at exit 0 on runs the reviewer took serially and independently.

R-0592 IS A GAP IN THE REVIEWER'S GATE COVERAGE, NOT IN THE WORKER'S EXECUTION. The
worker computed every insertion count R24's G12 ordered and reported all five
correctly; the `## Commits` table beside them carried the same value for one commit a
second time, derived from line counts instead of from the diff, and no clause of that
block and no item of the §3 checklist had ever named that table. R25 registers it and
lands item 28, which closes the class rather than the instance.

WHAT THIS FEATURE STILL OWES: closure alone. NO INSTALL HAS BEEN PROVEN in this session
or any other and no round of this workflow can prove one; DECISION F086 D4 records that
with its measurement, the release workflow has never been dispatched, and closure names
both as unproven rather than counting a skipped test as coverage.

R25 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict to
be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review this round and record R25's verdict as `Gate: R26 — the R25 entry.`,
the header shape §3 item 26 binds. Its first substantive work is closure.
<<<END VERDICT>>>
