── STEP closure preparation — F086 R26 ───────────────────────
Goal:
Record R25's verdict, register R-0593 — two stale ABSENCE claims left in
production text by the rounds that built the thing each one says does not exist —
retire both at their source, and add the feature file's Built State section,
which docs/roadmap/STATUS_closure_protocol.md precondition 4 requires and which
R-0154 forbids the closure commit itself from touching. This round writes no new
behaviour: every edit is a comment or a document.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R26 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0593 and RECORD25.
4. `packages/orchestration/release_gate.py` — the GATE pair retires "nothing
   calls it".
5. `pyproject.toml` — the TOML pair retires "is still owed".
6. `docs/roadmap/features/T2_F086.md` — the BUILT pair appends `## Built State`.
7. The handback, then the reviewer's VERDICT appended to it.

Change:
Exactly these paths:
  `.agent/authored/f086-r26.md`               (C0a)
  `.agent/last_block.md`                      (C0b)
  `.agent/plan.md`                            (C1)
  `.agent/live_review.md`                     (C2)
  `packages/orchestration/release_gate.py`    (C3)
  `pyproject.toml`                            (C4)
  `docs/roadmap/features/T2_F086.md`          (C5)
  `.agent/handoff.md`                         (C6, then C7)
Nothing else. In particular NOT `scripts/release_gate_check.py`, not
`.github/workflows/release.yml`, not `hatch_build.py`, not
`apps/cli/version_report.py`, not `docs/roadmap/STATUS.md`, not `README.md`, not
`docs/README.md`, and nothing else under `apps/`, `tests/` or `.github/`. Every
path this paragraph FORBIDS exists at `8fe709a8` — resolved with `git cat-file -e`
at emission per §3 item 24 — so the prohibition forbids something real. The
packaging ist-doc and its `docs/README.md` row are deliberately NOT in this round:
they are a separate document and belong to the next one.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is. §3 item 20 rules
   that the counter-measure for landed text in `.agent/live_review.md` is a dated
   correction in NEW text. You append only. G7 is written so the R19 duplicate is
   EXPECTED rather than forbidden. This constraint binds the RECORD; it does not
   bind production comments, which is exactly what C3 and C4 exist to correct.

4. PLAN26, FIND0593, RECORD25, the three pairs and VERDICT are the reviewer's
   text. Do not summarise, rewrap or reformat them. Do not write a verdict of
   your own anywhere — not in the handoff, not in a commit message, not in your
   report. Reporting what a gate MEASURED is your job; ruling on a round is not.
   A worker-authored `Done:` paragraph is a finding however honestly it is
   hedged (§4.4).

5. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line throughout.
   This round orders NO mutation and NO disposable worktree: it edits comments
   and documents, so there is nothing to red-prove.

6. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals and env-prefix command forms. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`. Capture
   pytest exit codes with `subprocess.run(...).returncode`, never with `$?`.

7. THE THREE PAIRS HAVE TWO DIFFERENT SHAPES and are proved differently (§4.9),
   measured per pair at emission and never generalised (§3 item 15):
     GATE  — REWRITE. `TO contains FROM: False`. Prove FROM 0x at C3 and TO 1x.
     TOML  — REWRITE. `TO contains FROM: False`. Prove FROM 0x at C4 and TO 1x.
     BUILT — APPEND.  `TO contains FROM: True`.  A FROM-zero count is unattainable
             by construction and must NOT be attempted; prove containment instead.
   Each FROM occurs exactly 1x in its target at `8fe709a8`, verified at emission.
   Each pair lands in its OWN commit, in the order C3, C4, C5.

8. THE HANDBACK'S ARITHMETIC IS STATED ONCE, HERE, AND NOWHERE ELSE — §3 item
   14's sweep rule, which R-0589 added. The VERDICT slice this block ships is 45
   lines, measured at emission on its final bytes, and C7 appends it by pure
   concatenation, so the file at C7 is exactly C6's length plus 45. KEEP C6 AT 54
   LINES OR FEWER, which puts C7 at 99 or fewer with no DECISION D15 overage to
   declare. Write C6 in the COMPACT form: ONE commits table with a per-commit
   row, ONE LINE PER GATE in the Verification section, the transcript going to
   your round report and not into the file (R-0582). G14 below NAMES this
   constraint instead of restating its numerals, deliberately: measured at
   emission, `45`, `54` and `99` occur in this constraint and in no other clause
   of this block. If C6 nevertheless lands above that bound, do NOT drop a
   mandated section — exceed the cap, write the DECISION D15 "Deviations,
   declared" line naming the real count and the mandated content that caused it.

9. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28, which
   R-0592 added last round). Every `+/-` cell you write in the handback's
   `## Commits` table is READ OUT of `git diff --numstat <sha>^ <sha>` for that
   commit and pasted from that reading. Never derive a cell from a file's line
   count before and after.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 5's two
   readings both taken and both reported.

G2 TRANSPORT. `.remedy-wt/f086-r26.md`, the committed `.agent/authored/f086-r26.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN26 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND. The pre-C2 `.agent/live_review.md` blob is a byte-exact PREFIX
   of the post-C2 blob, and the remainder is byte-equal to a blank line, FIND0593,
   a blank line and RECORD25 — both extracted from the committed C0a. Report the
   remainder's sha256 and line count.

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = lines matching `^- R-\d+ — `; resolved = lines matching
   `^Done: R-\d+ — `. Report at `8fe709a8` and at C2: registered count, resolved
   count, duplicate count, unregistered-resolution count, `Landed:` line count and
   open count. The RESOLVED set must be UNCHANGED between the two — this round
   resolves nothing — and the REGISTERED set must gain exactly `R-0593` and
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
   `.agent/live_review.md`. Report the header count at `8fe709a8` and at C2, and
   the SET of strings occurring more than once at each. That duplicate set must be
   UNCHANGED and must be exactly `Gate: R19 — the R18 entry.` — constraint 3
   forbids repairing it, so it is the expected reading. Then: `Gate: R26 — the R25
   entry.` occurs exactly 1x, it is the LAST such header in the file, and the text
   immediately following it begins `R25 `.

G8 THE THREE PAIRS, each proved in ITS OWN shape per constraint 7. For GATE at C3
   and TOML at C4: print the containment test's own output, then FROM 0x and TO 1x
   in the target file at that commit. For BUILT at C5: print the containment test's
   own output and confirm FROM occurs exactly 1x at `8fe709a8` and exactly 1x at
   C5 — do NOT count FROM as zero. Then, for EACH of the three, the ORDERED
   EQUALITY: the target at its commit is byte-equal to its `8fe709a8` blob with
   that FROM's single occurrence replaced by its TO and nothing else changed.
   Report each target's sha256 and line count at its commit.

G9 THE CLAIM THE PAIRS MAKE IS TRUE AT `8fe709a8`, not merely well-formed — the
   R-0561 obligation, because a shape gate never fails on a false sentence. Show,
   with the command output beside each: `scripts/release_gate_check.py` exists and
   imports `refuse_release` from `packages.orchestration.release_gate`;
   `.github/workflows/release.yml` exists and its only trigger is
   `workflow_dispatch`; `hatch_build.py` exists and `pyproject.toml` declares
   `[tool.hatch.build.targets.wheel.hooks.custom]` pointing at it. Confirm with
   `git merge-base --is-ancestor` that `8cdecc5b`, `25336879` and `f754228e` are
   all ancestors of `8fe709a8`, and that `3b738f6d` is an ancestor of `f754228e` —
   which is what makes "the comment went stale when the guard landed" a measurement
   rather than a story.

G10 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/release_gate.py`,
    `pyproject.toml` and `docs/roadmap/features/T2_F086.md` at C6: each must be 0.
    Count marker LINES, not substrings — this handback quotes gate text, so a
    substring gate over `.agent/handoff.md` would be unmeetable (F086 R5). The
    `.agent/handoff.md` reading can only be taken after C7 and goes in the round
    report.

G11 THE TOUCHED PYTHON STILL PARSES AND STILL LINTS, AND THE TOML STILL LOADS.
    `python3 -c "import packages.orchestration.release_gate as g;
    print(g.refuse_release.__module__)"` -> exit 0. `pyproject.toml` at C4 loads
    under `tomli` — this interpreter is 3.10 and has no `tomllib`, measured at
    emission — and the loaded document still carries
    `tool.hatch.build.targets.wheel.hooks.custom.path == "hatch_build.py"` and
    `tool.hatch.build.targets.wheel.artifacts == ["apps/ui/dist/**"]`, so the
    comment edit provably changed no setting. Then
    `python3 -m ruff check packages/orchestration/release_gate.py`
    at `8fe709a8` and again at C3, reporting the rule-code MULTISET at each rather
    than only the exit code (the F086 preview-lint rule): the multiset must be
    UNCHANGED. It is EMPTY at the base — measured at emission, `All checks
    passed!` — so an empty multiset at C3 is the expected reading and any code
    appearing is a finding.

G12 SUITES, serially in the PRIMARY checkout, each started only after the previous
    has ENDED and reported its exit code (F085 R64: two concurrent pytest processes
    produce false reds here). First the packaging and release set, which is what
    C3 and C4 touch: `python3 -m pytest tests/orchestration/test_release_gate.py
    tests/orchestration/test_release_gate_wiring.py
    tests/orchestration/test_release_workflow.py tests/test_packaging_smoke.py
    tests/test_build_revision.py tests/cli/test_version_report.py -q -rf`. Then the
    canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both exit
    codes and both summary lines, and report the SKIP count of the first:
    `tests/test_install_smoke.py` is NOT in this selection and its install coverage
    remains zero either way, which this round does not change and must not imply.

G13 CHANGE SET AND HISTORY, AND THE TABLE ITSELF. Print the range's path set and
    confirm it equals the Change list above, with no path on either side alone.
    Confirm every path the Change section FORBIDS is PRESENT at `8fe709a8` and
    untouched. Confirm the range is linear — every commit at exactly one parent —
    and that the round's `git reflog` entries are all `commit:`. Then, per
    constraint 9: for every commit BEFORE C6 print `git diff --numstat <sha>^
    <sha>` and confirm each `+/-` cell of the handback's `## Commits` table is
    byte-identical to the numstat pair for that commit, with the insertion column
    alone checked against the 500 cap (DECISION F104 D1). C6's and C7's own rows
    cannot be measured before they exist (§3 item 14) and go in the round report.

G14 THE HANDBACK, BOTH HALVES, per §3 item 14. Report `wc -l` of
    `.agent/handoff.md` at C6 and again at C7, and confirm each against the bound
    CONSTRAINT 8 states for it — this gate deliberately names that constraint
    rather than restating its numerals. All seven mandated headings of
    docs/agents/handback_template.md are present in the template's order and no
    section is dropped. The prefix-and-remainder equality against VERDICT is
    measurable only after C7 and goes in the round report.

G15 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Then
append VERDICT verbatim as C7. Push the branch once, after C7.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN26>>>
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
R26: closure PREPARATION. Record R25's verdict, register R-0593 — two stale
absence claims left in production text by the very rounds that built the thing
each says does not exist — retire both at their source, and add the feature
file's `## Built State` section, which the closure protocol's precondition 4
requires and which R-0154 forbids the closure commit from touching.

## Next Steps
1. THE PACKAGING IST-DOC is still owed: `docs/system/` has no page for what F086
   built, and AGENTS.md requires one. It plus its `docs/README.md` row is the
   next round's first work, and it must land BEFORE the closure commit, whose
   path set R-0154 fixes at STATUS.md, README.md and `.agent/`.
2. CLOSURE follows, per docs/roadmap/STATUS_closure_protocol.md — evidence job,
   FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precedent for the open set: F083 and F085 both closed
   PASS_WITH_RISKS.
3. THE INTEGRATION GATE IS DONE and GREEN: at R23 the branch full suite ran
   17192 passed / 20 skipped / 0 failed, the branch-only failure set was EMPTY,
   and all 23 base-only ids were attributed by demonstration at `76661dc1`.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN26>>>

<<<SLICE FIND0593>>>
- R-0593 — Low — TWO PRODUCTION COMMENTS STILL DENY THE EXISTENCE OF CODE THIS FEATURE HAD ALREADY BUILT, EACH LEFT BEHIND BY THE COMMIT THAT BUILT IT. Both are deliberate ABSENCE notes of the kind AGENTS.md's Code Discoverability Conventions require — "Deliberate absences are documented where a reader would search for them" — and both went false without being swept. FIRST, `packages/orchestration/release_gate.py`, whose module docstring landed at `24ad9e9d` and which has exactly ONE commit in its history, still reads "The caller — a manual-trigger workflow, not yet written — supplies the real values" and "Until that caller exists this gate refuses nothing, because nothing calls it". The caller `scripts/release_gate_check.py` landed at `8cdecc5b` and imports `refuse_release` directly; the manual-trigger workflow `.github/workflows/release.yml` landed at `25336879` and invokes that script; both are ancestors of `8fe709a8`. The gate is WIRED, and its own docstring — the WHY comment AGENTS.md places "directly above the definition, that is where searches land" — tells a reader looking for exactly this that it is not. SECOND, `pyproject.toml` reads "That guard is D1 part (b) and is still owed" at the line that entered at `3b738f6d`, four lines above the `[tool.hatch.build.targets.wheel.hooks.custom]` stanza that IS D1 part (b), landed at `f754228e` together with `hatch_build.py`, whose own docstring correctly claims the guard. One file therefore states in one comment that a guard is owed and in the next that the same guard is delivered. WHY LOW: no behaviour is wrong, no gate is weakened and no test is affected — both are comments, and the code they describe is correct and covered. WHY IT IS A FINDING AT ALL: these two comments are the search target for the exact question "is the release gate wired, and does the wheel build refuse an empty UI", and both answer it wrongly in the safe-sounding direction, which is how a later round re-builds something that already exists or trusts a guard it thinks is missing. THE CLASS IS R-0417's, retire-a-claim-everywhere, which F082 R9 solved for AUTHORED SLICES by making every block carry a standing staleness gate over its own text; that gate never reached PRODUCTION comments a round leaves behind in files it is not editing. COUNTER-MEASURE, applied by this round's C3 and C4 rather than asserted here: both comments are retired at their source, each naming the commit that falsified it, and the next block that adds a capability an existing comment calls absent is the one that owes the sweep.
<<<END FIND0593>>>

<<<SLICE RECORD25>>>
Gate: R26 — the R25 entry. R25 PASSED with NO finding. Every gate R25's block ordered was RE-EXECUTED by the reviewer over `e33ba23a..8fe709a8` rather than read from the handback, and every reading reproduces to the byte. THE TRANSPORT HELD in the three-way form: the scratchpad, the committed `.agent/authored/f086-r25.md` at `b2751475` and the committed `.agent/last_block.md` at `67fbecb5` are byte-EQUAL at sha256 1b8b5e50f3c473c945dc768ce18b53a7c09418c348f2407b2f32202baa5c9f3b, 26126 B over 329 lines. EVERY SLICE LANDED BYTE-EXACT against an extraction from the COMMITTED C0a: `.agent/plan.md` at `404706f5` equals PLAN25 at sha256 593fb7b6d0e8a9791dd25f08ee62fa6a8b6ffd1d0ab71663a17017f6fce384c7 over 45 lines, under the AGENTS.md cap of 50 and carrying `## Goal`, `## Next Steps` and `F086`; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0592, a blank line and RECORD24 at sha256 a52e460cd4c8e4a8991ceee3cbb440553f61951fa4b765e9c3e0771b5ecc885d over 6499 B; and the CHECK28 pair satisfies the ORDERED EQUALITY in the append form — `docs/agents/planner_reviewer_prompt.md` at `764b5a4a` is byte-equal to the `e33ba23a` blob with CHECK28FROM's single occurrence replaced by CHECK28TO and nothing else changed, 865 lines to 883 at sha256 c41442d8c72fa67b170e2596b457440e3b5375a074159eb65136dc625fcc014f. NOTHING WAS RENUMBERED: items 26, 27 and 28 each match exactly once and item 28's last line is followed by the paragraph beginning `  Why this is on disk and not a habit:`. THE LEDGER MOVED ONLY ON THE REGISTERED SIDE: both extractions AGREE at each end — 174 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 170 open at `e33ba23a`, and 175 / 4 / 0 / 0 / 0 / 171 at `2df326eb` — the resolved set is equal, the registered set gains exactly `R-0592`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. R-0586'S SCAN HELD WITH ITS CONTROL BITING: over the lines `2df326eb` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0, while the same extractor over `fd166295`'s added lines reads 3. R-0587'S CHECK HELD: the duplicated-header set is unchanged and is exactly `Gate: R19 — the R18 entry.`; `Gate: R25 — the R24 entry.` occurs 1x, is the LAST such header, and the text after it begins `R24 `. THE SUITES ARE GREEN ON THE REVIEWER'S OWN SERIAL RUNS: 160 passed at exit 0, then the canary 42 passed at exit 0. ITEM 28 BOUND ON THE VERY ROUND THAT LANDED IT, which is the point of registering it there: all five measurable `+/-` cells of the handback's `## Commits` table — `+329/-0`, `+157/-208`, `+5/-5`, `+4/-0`, `+18/-0` — are byte-identical to `git diff --numstat` for their commits, and the R-0592 instance reproduced live and was caught, `.agent/last_block.md` going 380 lines to 329 while its numstat reads `157 208` and only the numstat pair reaching the table. THE HYGIENE HELD: six paths over seven single-parent commits, all seven forbidden paths present at `e33ba23a` and none touched, nothing under `apps/`, `packages/`, `tests/`, `docs/roadmap/` or `.github/`, every `git reflog` entry `commit:`, no marker LINE in any target including `.agent/handoff.md` at C5, `git worktree list` one line, the tree clean and `origin` at the same commit. THE HANDBACK IS 55 LINES AT C4 AND 94 AT C5, the first a byte-exact prefix of the second with a 39-line remainder byte-equal to VERDICT, all seven mandated headings present in the template's order.
<<<END RECORD25>>>

<<<SLICE GATEFROM>>>
caller — a manual-trigger workflow, not yet written — supplies the real values,
reads the repository's `CHANGELOG.md` and stops on a non-empty result. Until that
caller exists this gate refuses nothing, because nothing calls it. It is
<<<END GATEFROM>>>

<<<SLICE GATETO>>>
caller is `scripts/release_gate_check.py`, added at 8cdecc5b: it supplies the real
values, reads the repository's `CHANGELOG.md` and stops on a non-empty result, and
`.github/workflows/release.yml`, added at 25336879, runs that caller on a manual
trigger only. This gate is therefore WIRED: it refuses real releases, and the
absence note it carried until F086 R26 no longer describes the repository. It is
<<<END GATETO>>>

<<<SLICE TOMLFROM>>>
# ships no UI. That guard is D1 part (b) and is still owed.
<<<END TOMLFROM>>>

<<<SLICE TOMLTO>>>
# ships no UI. That guard is D1 part (b): it is the custom build hook declared
# just below, which landed at f754228e together with hatch_build.py and raises
# when apps/ui/dist/index.html is absent. Retired as owed at F086 R26.
<<<END TOMLTO>>>

<<<SLICE BUILTFROM>>>
choice (human decision). Suggested tests: tests/test_packaging_smoke.py.
<<<END BUILTFROM>>>

<<<SLICE BUILTTO>>>
choice (human decision). Suggested tests: tests/test_packaging_smoke.py.

## Built State
> Written at F086 R26, before closure, per STATUS_closure_protocol.md
> precondition 4. Everything above is the TARGET plan; this section is what is
> BUILT on feature/f086-release-capability.

- **T001 packaging.** `pyproject.toml` carries `apps/ui/dist/**` into the wheel
  (DECISION F086 D1 a, mechanism measured in D3) and `hatch_build.py` refuses a
  build whose `apps/ui/dist/index.html` is missing (D1 b). Dual-mode asset
  resolution and the install smoke live in `tests/test_install_smoke.py`.
- **T002 version.** `apps/cli/version_report.py` reads the version from package
  metadata and the build revision from `<dist-info>/extra_metadata/REVISION`,
  reporting `dev` in a checkout rather than inventing a sha (DECISION F086 D2).
- **T003 release gate.** `packages/orchestration/release_gate.py` returns every
  reason to refuse a release, `scripts/release_gate_check.py` observes a real
  wheel and CI conclusion, and `.github/workflows/release.yml` runs both on a
  manual trigger. Publishing stays a human command, as the brief requires.

NOT PROVEN and NOT CLAIMED: no wheel has been installed into a fresh virtualenv
in any round of this workflow — `tests/test_install_smoke.py` SKIPS unless its
opt-in variable is set, so its install coverage is zero — and
`.github/workflows/release.yml` has never been dispatched. Both are human
actions, and DECISION F086 D4 records the first with its measurement.
<<<END BUILTTO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming at `e33ba23a` under a three-round cap
declared up front per guardrail G7. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on gates the
reviewer RE-EXECUTED over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R24 | 39bfc199..e33ba23a | PASS — one finding, R-0592, against the reviewer |
| R25 | e33ba23a..8fe709a8 | PASS — no finding |
| R26 | 8fe709a8..this range | verdict not yet on disk; see the last paragraph |

R24 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was planned.
R-0592 is a gap in the REVIEWER'S gate coverage, not in the worker's execution: the
handback's mandated `## Commits` table carried one commit's diff a second time, derived
from line counts instead of from the diff, and no clause of that block and no item of the
§3 checklist had ever named that table. R25 registered it and landed checklist item 28,
which then bound the very round that shipped it — all five measurable cells matched
`git diff --numstat`, and the same wrong derivation was available and was not taken.

R25 PASSED WITH NO FINDING. All fourteen of its gates reproduce to the byte on the
reviewer's own runs, including both suites green at exit 0 taken serially.

R26 IS CLOSURE PREPARATION, and it exists because closure cannot legally do this work:
R-0154 fixes the closure commit's path set at STATUS.md, README.md and `.agent/`, while
precondition 4 requires the feature file's Built State to be current already. R-0593,
registered here, is two stale ABSENCE comments in production text — the release gate
saying nothing calls it, and `pyproject.toml` saying a guard four lines below it is still
owed — each left behind by the commit that falsified it.

WHAT THIS FEATURE STILL OWES: the packaging ist-doc under `docs/system/` with its
`docs/README.md` row, then closure. NO INSTALL HAS BEEN PROVEN in this session or any
other and no round of this workflow can prove one; the release workflow has never been
dispatched. Closure names both as unproven rather than counting a skipped test as
coverage, and F083 and F085 are the precedent for closing PASS_WITH_RISKS.

R26 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict to
be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review this round and record R26's verdict as `Gate: R27 — the R26 entry.`,
the header shape §3 item 26 binds.
<<<END VERDICT>>>
