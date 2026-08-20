── STEP findings + checklist — F086 R27 ──────────────────────
Goal:
Record R26's verdict and register R-0594 — a gate that ordered a reading at a BASE
revision without naming a mechanism that reads it WITHOUT writing, so the only
faithful route left was to overwrite a tracked file in the primary checkout — and
land its counter-measure as checklist item 29, which is the only place a rule in
this repository binds the next block. This round writes no production code and
runs no suite of its own beyond the canary.

SCOPE NOTE, stated because it is a deliberate cut and not an oversight: the
packaging ist-doc and its `docs/README.md` row were drafted for this round and
REMOVED from it. With them the block measured 418 lines against the 400-line cap
of §3 item 1, and DECISION F105 D5 requires the design to change rather than the
wording to be shaved. They are the next session's first work, ahead of closure,
and PLAN27 carries them.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R27 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0594 and RECORD26.
4. `docs/agents/planner_reviewer_prompt.md` gains item 29, appended after item
   28's last line and BEFORE the paragraph beginning "Why this is on disk and
   not a habit", so nothing is renumbered and no existing item moves.
5. The handback, then the reviewer's VERDICT appended to it.

Change:
Exactly these paths:
  `.agent/authored/f086-r27.md`               (C0a)
  `.agent/last_block.md`                      (C0b)
  `.agent/plan.md`                            (C1)
  `.agent/live_review.md`                     (C2)
  `docs/agents/planner_reviewer_prompt.md`    (C3)
  `.agent/handoff.md`                         (C4, then C5)
Nothing else. In particular NOT `docs/roadmap/STATUS.md`, not `README.md`, not
`docs/README.md`, not `docs/roadmap/features/T2_F086.md`, not
`packages/orchestration/release_gate.py`, not `pyproject.toml`, not
`CHANGELOG.md`, and nothing else under `apps/`, `packages/`, `tests/`, `docs/system/`
or `.github/`. Every path this paragraph FORBIDS exists at `788849bb` — resolved
with `git cat-file -e` at emission per §3 item 24 — so the prohibition forbids
something real.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is. §3 item 20 rules
   that the counter-measure for landed text in `.agent/live_review.md` is a dated
   correction in NEW text. You append only. G7 is written so the R19 duplicate is
   EXPECTED rather than forbidden.

4. PLAN27, FIND0594, RECORD26, the CHECK29 pair and VERDICT are the reviewer's
   text. Do not summarise, rewrap or reformat them. Do not write a verdict of
   your own anywhere — not in the handoff, not in a commit message, not in your
   report. Reporting what a gate MEASURED is your job; ruling on a round is not.
   A worker-authored `Done:` paragraph is a finding however honestly it is
   hedged (§4.4).

5. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line throughout.
   NO FILE IN THE WORKING TREE IS OVERWRITTEN TO TAKE A READING — that is
   R-0594's whole subject and this round must not reproduce it. Every reading at
   a non-current revision comes from `git show <sha>:<path>` into memory or into
   a scratch path under `.remedy-wt/`, never onto the tracked path itself.

6. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals (a Python dict literal written inline counts) and
   env-prefix command forms. Route that work through `python3 - <<'PY'` heredocs
   or scripts under `.remedy-wt/`. Capture exit codes with
   `subprocess.run(...).returncode`, never with `$?`.

7. THE CHECK29 PAIR IS APPEND-SHAPED and lands in ONE commit, C3. The containment
   test was run at emission and printed `TO contains FROM: True`, so §4.9's APPEND
   obligation applies, a "FROM 0x" count is unattainable by construction and must
   NOT be attempted, and CHECK29FROM occurs exactly 1x in the file at `788849bb`.

8. THE HANDBACK'S ARITHMETIC IS STATED ONCE, HERE, AND NOWHERE ELSE — §3 item
   14's sweep rule, which R-0589 added. The VERDICT slice this block ships is 48
   lines, measured at emission on its final bytes, and C5 appends it by pure
   concatenation, so the file at C5 is exactly C4's length plus 48. KEEP C4 AT 51
   LINES OR FEWER, which puts C5 at 99 or fewer with no DECISION D15 overage to
   declare. Write C4 in the COMPACT form: ONE commits table with a per-commit
   row, ONE LINE PER GATE in the Verification section, the transcript going to
   your round report and not into the file (R-0582). G12 below NAMES this
   constraint instead of restating its numerals, deliberately: measured at
   emission, `48` and `51` occur in this constraint and in no other clause of
   this block. If C4 nevertheless lands above that bound, do NOT drop a mandated
   section — exceed the cap, write the DECISION D15 "Deviations, declared" line
   naming the real count and the mandated content that caused it.

9. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28). Every
   `+/-` cell you write in the handback's `## Commits` table is READ OUT of
   `git diff --numstat <sha>^ <sha>` for that commit and pasted from that
   reading. Never derive a cell from a file's line count before and after.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 5's readings all
   taken and reported, including the explicit statement that no tracked path was
   overwritten to take a reading.

G2 TRANSPORT. `.remedy-wt/f086-r27.md`, the committed `.agent/authored/f086-r27.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN27 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND. The pre-C2 `.agent/live_review.md` blob is a byte-exact PREFIX
   of the post-C2 blob, and the remainder is byte-equal to a blank line, FIND0594,
   a blank line and RECORD26 — both extracted from the committed C0a. Report the
   remainder's sha256 and line count.

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = `^- R-\d+ — `; resolved = `^Done: R-\d+ — `. Report at `788849bb`
   and at C2: registered, resolved, duplicate, unregistered-resolution, `Landed:`
   and open counts. The RESOLVED set must be UNCHANGED — this round resolves
   nothing — and the REGISTERED set must gain exactly `R-0594`. CONTROL, which
   must MOVE so the reading is not vacuous: the same two extractions over
   `f0b27118..7b84524c` report `[]` registered while the resolved set gains
   exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST — a token a finding QUOTES is not one it USES
   (R-0584) — then count `\bHEAD\b` in what remains: it must read 0. RED CONTROL,
   same two-step extractor over the lines `fd166295` adds to the same file: it must
   read 3, or the extractor is broken and the 0 proves nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `788849bb` and at C2 and the
   SET occurring more than once at each: that set must be UNCHANGED and exactly
   `Gate: R19 — the R18 entry.`, which constraint 3 preserves. Then `Gate: R27 —
   the R26 entry.` occurs exactly 1x, is the LAST such header, and the text
   immediately following it begins `R26 `.

G8 THE CHECK29 PAIR, PROVED IN THE APPEND FORM (§4.9), never as a FROM-zero count.
   Print the containment test's own output, confirm CHECK29FROM occurs exactly 1x
   at `788849bb` AND exactly 1x at C3. Then the ORDERED EQUALITY: the file at C3
   is byte-equal to the `788849bb` blob with CHECK29FROM's single occurrence
   replaced by CHECK29TO and nothing else changed. Report C3's sha256 and line
   count against the base's 883.

G9 STRUCTURE, which is what proves nothing was renumbered.
   `grep -c '^  27\. \*\*'`, `grep -c '^  28\. \*\*'` and `grep -c '^  29\. \*\*'`
   over `docs/agents/planner_reviewer_prompt.md` at C3 each read 1. Report the line
   that FOLLOWS CHECK29TO's last line: it is the line beginning
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

G12 CHANGE SET, HISTORY AND THE HANDBACK. Print the range's path set and confirm
    it equals the Change list, with no path on either side alone. Confirm every
    path the Change section FORBIDS is PRESENT at `788849bb` and untouched, that
    the range is linear, and that the round's `git reflog` entries are all
    `commit:`. Per constraint 9, for every commit BEFORE C4 print
    `git diff --numstat <sha>^ <sha>` and confirm each `+/-` cell of the handback's
    `## Commits` table is byte-identical to that pair, insertion column alone
    against the 500 cap (DECISION F104 D1). Then report `wc -l` of
    `.agent/handoff.md` at C4 and at C5 against the bound CONSTRAINT 8 states —
    this gate names that constraint rather than restating its numerals — and
    confirm all seven mandated headings of docs/agents/handback_template.md are
    present in the template's order with no section dropped. C4's and C5's own
    numstat rows and the prefix-and-remainder equality against VERDICT are
    measurable only after C5 and go in the round report.

G13 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Then
append VERDICT verbatim as C5. Push the branch once, after C5.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN27>>>
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
R27: record R26's verdict, register R-0594 — a gate that ordered a reading at a
base revision without naming a non-writing mechanism, so the worker overwrote a
tracked path to take it — and land item 29, where a rule has to live to bind the
next block.

## Next Steps
1. THE PACKAGING IST-DOC is owed and is the next round's FIRST work: `docs/system/`
   has no page for what F086 built and AGENTS.md requires one. It was drafted for
   R27 and cut when the block measured 418 lines against the 400 cap. It must land
   BEFORE the closure commit, whose path set R-0154 fixes at STATUS.md, README.md
   and `.agent/`; an earlier commit in the closure round satisfies that.
2. CLOSURE then follows, per docs/roadmap/STATUS_closure_protocol.md — evidence
   job, FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precondition 4 is already met: `## Built State` landed at
   `d420e8e5`. The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
- `remedy integrity check` is denied to this session class, so closure precondition
  3 is met through the underlying module or declared unmet — never assumed.
<<<END PLAN27>>>

<<<SLICE FIND0594>>>
- R-0594 — Low — A GATE ORDERED A READING AT A BASE REVISION WITHOUT NAMING A MECHANISM THAT READS WITHOUT WRITING, SO THE ONLY FAITHFUL ROUTE LEFT WAS TO OVERWRITE A TRACKED FILE IN THE PRIMARY CHECKOUT. The R26 block, committed at `b674a9cf`, ordered in G11: "`python3 -m ruff check packages/orchestration/release_gate.py` at `8fe709a8` and again at C3, reporting the rule-code MULTISET at each". Ruff resolves `[tool.ruff.lint.per-file-ignores]` by the path it is given, so linting a copy at another path would have answered a different question; the block named no way to present the base bytes AT that path without writing them there. The worker therefore wrote the `8fe709a8` blob over the tracked `packages/orchestration/release_gate.py`, ran ruff, restored the file, verified the restore byte-identical and the tree clean, took no commit while the base blob was in place, and DECLARED the method in its report. THE MEASUREMENT WAS CORRECT AND IS CONFIRMED: the reviewer re-took both readings with `ruff check --stdin-filename packages/orchestration/release_gate.py -`, feeding each blob on stdin, and read an EMPTY rule-code multiset at exit 0 at both ends — the same answer, obtained without touching the working tree. WHY THIS IS A FINDING: docs/agents/self_drive_protocol.md guardrail G5 says mutation "run[s] only inside a disposable `git worktree`, never in the primary checkout", and the gate as written left overwrite-and-restore as the obvious route. Every commit of the round holds the C3 blob and none holds the base blob — the reviewer checked all five — so nothing false reached disk and the guardrail's PURPOSE, a clean tree at every verdict, held; what failed is the gate's duty to make the safe route the stated one. WHY LOW rather than Medium: the breach was transient, self-declared, verified reversed, and the reading it produced is independently reproducible by the non-writing mechanism, so no evidence rests on the mutated state. THE CLASS IS THE R-0590/R-0591 FAMILY — a reviewer ordering an OUTCOME while leaving the ROUTE to the worker — but neither of those items reaches it: item 18 reads a NAMED mechanism against the property it must preserve, and this block named no mechanism at all. COUNTER-MEASURE, applied by this round's C3 rather than asserted here: a new checklist item 29 requires a gate that measures a NON-CURRENT revision to name the non-writing mechanism it is read with.
<<<END FIND0594>>>

<<<SLICE RECORD26>>>
Gate: R27 — the R26 entry. R26 PASSED with ONE finding, R-0594, and that finding is against the reviewer's gate text rather than against the worker's execution. Every gate R26's block ordered was RE-EXECUTED by the reviewer over `8fe709a8..788849bb` rather than read from the handback, and every reading reproduces to the byte. THE TRANSPORT HELD in the three-way form: the scratchpad, the committed `.agent/authored/f086-r26.md` at `b674a9cf` and the committed `.agent/last_block.md` at `5329860b` are byte-EQUAL at sha256 3a01faf9a7b183650e1ef6ec97d505644db511cd80a4586cfba44b149465e3a2, 29011 B over 388 lines. EVERY SLICE LANDED BYTE-EXACT against an extraction from the COMMITTED C0a: `.agent/plan.md` at `8c199616` equals PLAN26 at sha256 5d0503dd3fecf37d9d5c1afbc74d5251410dca45043b0e5486420960f9795d10 over 45 lines, and the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0593, a blank line and RECORD25 at sha256 cf4de522b14a06365e6bf887fbebe8f202531ea2aedf8d129084b65903b94f26. THE THREE PAIRS EACH HELD IN THEIR OWN SHAPE, which is the part of this round that could most easily have gone wrong: GATE and TOML are REWRITES and their FROM reads 1x at base and 0x after with the TO at 1x, while BUILT is an APPEND whose FROM correctly still reads 1x after — the FROM-zero count was NOT attempted for it — and all three satisfy the ORDERED EQUALITY against their `8fe709a8` blobs, at 82 to 84 lines for `packages/orchestration/release_gate.py`, 156 to 158 for `pyproject.toml` and 67 to 90 for `docs/roadmap/features/T2_F086.md`. THE COMMENT EDITS CHANGED NO SETTING, proved rather than argued: `tomli` parses `pyproject.toml` at base and at C4 to EQUAL documents, so the retired absence note moved no key. R-0593'S CLAIMS ARE TRUE AT BASE, checked against the tree and not against the finding's own prose: `scripts/release_gate_check.py` imports `refuse_release`, `.github/workflows/release.yml` has `workflow_dispatch` as its ONLY trigger, `pyproject.toml` carries the `hooks.custom` stanza pointing at `hatch_build.py`, `8cdecc5b`, `25336879` and `f754228e` are all ancestors of `8fe709a8` while `3b738f6d` is an ancestor of `f754228e`, and `packages/orchestration/release_gate.py` had exactly ONE commit in its history before that round — which is what makes "the comment went stale when the guard landed" a measurement rather than a story. THE LEDGER MOVED ONLY ON THE REGISTERED SIDE: both extractions AGREE at each end — 175 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 171 open at `8fe709a8`, and 176 / 4 / 0 / 0 / 0 / 172 at `7d06c6ef` — the resolved set is equal, the registered set gains exactly `R-0593`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. THE SCANS HELD WITH THEIR CONTROLS BITING: over the lines `7d06c6ef` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 while the same extractor over `fd166295`'s added lines reads 3; the duplicated-header set is unchanged at exactly `Gate: R19 — the R18 entry.`; and `Gate: R26 — the R25 entry.` occurs 1x, is the LAST such header, and the text after it begins `R25 `. THE SUITES ARE GREEN ON THE REVIEWER'S OWN SERIAL RUNS: the packaging and release selection 45 passed at exit 0 with 0 skipped, then the canary 42 passed at exit 0. ITEM 28 BOUND AGAIN, one round after it landed: all seven measurable `+/-` cells of the handback's `## Commits` table are byte-identical to `git diff --numstat` for their commits. THE HYGIENE HELD: eight paths over nine single-parent commits, all seven forbidden paths present at `8fe709a8` and none touched, nothing under `apps/`, `tests/` or `.github/`, every `git reflog` entry `commit:`, no marker LINE in any target, `git worktree list` one line, the tree clean and `origin` at the same commit; the handback is 53 lines at C6 and 98 at C7, the first a byte-exact prefix of the second with a 45-line remainder byte-equal to VERDICT and all seven mandated headings in the template's order. WHERE R26 FELL SHORT IS IN ONE PLACE AND IT IS THE REVIEWER'S: G11 ordered a lint reading at a base revision and named no non-writing mechanism for it, so the worker overwrote a tracked path to take it and said so (R-0594).
<<<END RECORD26>>>

<<<SLICE CHECK29FROM>>>
      are where this bites, because only there do the counts and the columns diverge.
<<<END CHECK29FROM>>>

<<<SLICE CHECK29TO>>>
      are where this bites, because only there do the counts and the columns diverge.
  29. **A gate that measures a NON-CURRENT revision names the mechanism that reads it
      without writing.** Finding R-0594. When a done-when orders a tool run "at <base>"
      as well as at the round's own commit, the block names HOW the base bytes reach
      that tool — `git show <sha>:<path>` into memory, a scratch copy under a
      gitignored directory, or the tool's own stdin flag where its configuration is
      path-sensitive (`ruff check --stdin-filename <path> -`, so `per-file-ignores`
      still resolves). A gate that says only "run X at <base>" leaves overwrite-and-
      restore as the obvious route, and that route mutates the PRIMARY checkout, which
      docs/agents/self_drive_protocol.md guardrail G5 forbids outright. Item 18 reads a
      NAMED mechanism against the property it must preserve and item 27 reads a
      conditional against its false case; neither reaches this one, because here the
      block names no mechanism at all and the defect is the ROUTE the worker is left to
      invent rather than the ORDER itself. The R26 instance: G11 ordered
      `ruff check packages/orchestration/release_gate.py` at the base and at C3, and
      ruff resolves per-file-ignores by the given path, so the worker wrote the base
      blob over the tracked file, linted, restored it byte-identically and declared the
      method — a correct reading taken by a route the protocol forbids, and the same
      reading was available from `--stdin-filename` with nothing written at all.
<<<END CHECK29TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming at `e33ba23a` under a three-round cap
declared up front per guardrail G7. This round is the third and the cap is now spent.
The reviewer wrote nothing in the work tree, one delegated worker per round made every
commit, and every verdict below rests on gates the reviewer RE-EXECUTED over the
committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R24 | 39bfc199..e33ba23a | PASS — one finding, R-0592, against the reviewer |
| R25 | e33ba23a..8fe709a8 | PASS — no finding |
| R26 | 8fe709a8..788849bb | PASS — one finding, R-0594, against the reviewer |
| R27 | 788849bb..this range | verdict not yet on disk; see the last paragraph |

THREE OF THIS SESSION'S FOUR FINDINGS ARE DEFECTS OF THE REVIEWER'S OWN GATE TEXT AND
NONE IS IN A WORKER'S EXECUTION. R-0592: the handback's mandated `## Commits` table
carried a value no gate had ever named, and one cell was derived from line counts
instead of from the diff. R-0594: a gate ordered a lint reading at a base revision and
named no non-writing mechanism, so the worker overwrote a tracked path, declared it, and
restored it verified — a correct measurement by a route guardrail G5 forbids. Each
counter-measure landed on the §3 checklist in the round that registered it, as items 28
and 29, because a rule written only in a finding body binds nothing.

R-0593 IS THE EXCEPTION AND IT IS THE SPLIT WORKING: two stale ABSENCE comments in
production text — the release gate saying nothing calls it, and `pyproject.toml` saying
a guard four lines below it is still owed — each left behind by the commit that
falsified it, and both found by reading the code rather than the record. R26 retired
both at their source, naming the commit that falsified each.

F086'S REMAINING WORK IS THE IST-DOC, THEN CLOSURE. Precondition 4 is already met: the
feature file's `## Built State` landed at `d420e8e5`, which the closure commit itself
may not carry (R-0154). The packaging ist-doc with its `docs/README.md` row was drafted
for R27 and CUT when the block measured 418 lines against the 400-line cap — DECISION
F105 D5 requires the design to change, not the wording to be shaved — so it is the next
session's first work. NO INSTALL HAS BEEN PROVEN in this session or any other and the
release workflow has never been dispatched; closure names both as unproven rather than
counting a skipped test as coverage, and F083 and F085 are the precedent for closing
PASS_WITH_RISKS.

R27 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict to
be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review this round and record R27's verdict as `Gate: R28 — the R27 entry.`,
the header shape §3 item 26 binds.
<<<END VERDICT>>>
