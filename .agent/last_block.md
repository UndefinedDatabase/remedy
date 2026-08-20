── STEP the packaging ist-doc — F086 R29 ─────────────────────
Goal:
Record R28's verdict, and write the one document this feature owes: a
`docs/system/` page for what F086 BUILT. AGENTS.md requires an ist-doc when a
feature introduces behaviour that is not yet documented, and F086 has introduced
packaging, a version report and a release gate without one. The page lands with
its two `docs/README.md` index rows in the SAME commit as the file they point at,
which makes it the first change ever judged by the documentation link gate R28
repaired. This round writes no production code and registers no finding.

WHY THIS IS ITS OWN ROUND, stated because it looks like a deferral and is not:
the page was drafted into R27's block and again into R28's, and both times the
combined block measured over the cap, so DECISION F085 D5's instruction — change
the design rather than shave the wording — was applied and the page was given a
round. R28 went first on purpose: an index row pointing at a new file is exactly
the reading the old gate could not make, so the fix had to precede the rows.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R29 (§3 item 23 — this round appends to the
   ledger, so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains RECORD28.
4. `docs/system/release-capability-v1.md` created, and `docs/README.md` gains its
   two rows, in ONE commit.
5. The handback.

Change:
Exactly these paths:
  `.agent/authored/f086-r29.md`                   (C0a)
  `.agent/last_block.md`                          (C0b)
  `.agent/plan.md`                                (C1)
  `.agent/live_review.md`                         (C2)
  `docs/system/release-capability-v1.md`          (C3, created)
  `docs/README.md`                                (C3)
  `.agent/handoff.md`                             (C4)
Nothing else. In particular NOT `docs/roadmap/STATUS.md`, not `README.md`, not
`docs/roadmap/features/T2_F086.md`, not `tests/docs/test_docs_consistency.py`, not
`pyproject.toml`, not `hatch_build.py`, not `apps/cli/version_report.py`, not
`packages/orchestration/release_gate.py`, not `scripts/release_gate_check.py`, not
`.github/workflows/release.yml`, not `CHANGELOG.md`, not
`tests/test_packaging_smoke.py`, not `tests/test_install_smoke.py`, and nothing
else under `apps/`, `packages/`, `tests/` or `docs/agents/`. Every path this
paragraph FORBIDS exists at `05c6e012` — each resolved with `git ls-tree` at
emission per §3 item 24 — so the prohibition forbids something real.
`docs/system/release-capability-v1.md` is in the ALLOWED list only: it does not
exist at `05c6e012` and C3 creates it.

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

4. EVERY SLICE IS THE REVIEWER'S TEXT. Do not summarise, rewrap or reformat one.
   Do not write a verdict of your own anywhere — not in the handoff, not in a
   commit message, not in your report. Reporting what a gate MEASURED is your job;
   ruling on a round is not (§4.4).

5. THE DOCUMENT AND ITS INDEX ROWS SHARE ONE COMMIT, and this is the constraint
   RECORD28 and the round both rest on: C3 writes
   `docs/system/release-capability-v1.md` and both `docs/README.md` rows
   together. A commit in which a row exists and its target does not is precisely
   the state R28's repaired gate now fails on, and splitting C3 would put that
   state into the history on purpose.

6. C1 IS THE FIRST SUBSTANTIVE COMMIT, after C0a and C0b which write nothing but
   the block itself (§3 item 23).

7. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line at every
   commit and at the handback. G10's red control is the one exception and it is
   bounded: it runs in a disposable worktree under `.remedy-wt/`, takes no commit
   while it exists, and is removed and pruned before C4. NO FILE IN THE PRIMARY
   CHECKOUT IS OVERWRITTEN TO TAKE A READING (§3 item 29, finding R-0594): every
   reading at a non-current revision is taken with `git show <sha>:<path>` into
   memory or into a scratch path under `.remedy-wt/`, never onto the tracked path.

8. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals (a Python dict or set literal written inline counts)
   and env-prefix command forms. Route that work through `python3 - <<'PY'`
   heredocs or scripts under `.remedy-wt/`. Capture exit codes with
   `subprocess.run(...).returncode`, never with `$?`.

9. PAIR SHAPES, each from its own containment test run at emission, one reading
   per pair and neither generalised to the other (§3 item 15):
     QUICK — `TO contains FROM: True` → APPEND-shaped.
     SYS   — `TO contains FROM: True` → APPEND-shaped.
   Both are APPEND, so §4.9 forbids a FROM-zero count for either: the obligation
   is FROM exactly 1x at both ends plus each TO-ONLY line exactly 1x AMONG THE
   LINES C3'S DIFF ADDS, and G9 orders exactly that and no zero. Each FROM occurs
   exactly 1x in `docs/README.md` at `05c6e012`, counted at emission.

10. THE IST-DOC IS A NEW FILE, so its proof is ordered equality and not a pair:
    the file C3 creates is byte-equal to the DOC slice, and the lines C3's diff
    adds for that path are exactly the slice's lines in order (§4.9, R-0531).

11. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28). Every
    `+/-` cell you write in the handback's `## Commits` table is READ OUT of
    `git diff --numstat <sha>^ <sha>` for that commit and pasted from that
    reading. Never derive a cell from a file's line count before and after.

12. THE HANDBACK'S SIZE IS STATED ONCE, HERE, AND NOWHERE ELSE (§3 item 14's
    sweep rule). This round appends NO verdict slice, so C4 is the only commit
    that writes `.agent/handoff.md` and a whole-file reading is honest at it.
    KEEP C4 AT 60 LINES OR FEWER, the AGENTS.md cap, with no DECISION D15 overage
    to declare. Write it in the COMPACT form: ONE commits table with a per-commit
    row, ONE LINE PER GATE in the Verification section, the transcript going to
    your round report and not into the file (R-0582). G13 NAMES this constraint
    instead of restating its numeral: measured at emission, `60` occurs in this
    constraint and in no other clause of this block. If C4 nevertheless lands
    above that bound, do NOT drop a mandated section — exceed the cap and write
    the DECISION D15 "Deviations, declared" line naming the real count and the
    mandated content that caused it.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 7's readings all
   taken and reported, including the explicit statement that no path in the
   primary checkout was overwritten to take a reading.

G2 TRANSPORT. `.remedy-wt/f086-r29.md`, the committed `.agent/authored/f086-r29.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN29 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND, proved in the prefix-and-remainder form against RECORD28
   extracted from the committed C0a. The pre-C2 blob is a byte-exact PREFIX of the
   post-C2 blob whose remainder is a blank line followed by RECORD28. Report the
   remainder's sha256 and line count. The blank line between entries is mandatory
   (R-0578).

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = `^- R-\d+ — `; resolved = `^Done: R-\d+ — `. Report at `05c6e012`
   and at C2: registered, resolved, duplicate, unregistered-resolution, `Landed:`
   and open counts. This round registers and resolves NOTHING, so assert the
   EQUALITY of the sets rather than predicting their sizes: the registered set at
   C2 equals the registered set at `05c6e012` and the resolved set at C2 equals
   the resolved set at `05c6e012`, and both counts are REPORTED. CONTROL, which
   must MOVE so an all-equal reading is not vacuous: the same two extractions over
   `f0b27118..7b84524c` report `[]` registered gained while the resolved set gains
   exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST — a token a finding QUOTES is not one it USES
   (R-0584) — then count `\bHEAD\b` in what remains: it must read 0. RED CONTROL,
   the same two-step extractor over the lines `fd166295` adds to the same file: it
   must read 3, or the extractor is broken and the zero proves nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `05c6e012` and at C2 and the
   SET occurring more than once at each: that set must be UNCHANGED and exactly
   `Gate: R19 — the R18 entry.`, which constraint 3 preserves. Then `Gate: R29 —
   the R28 entry.` occurs exactly 1x, is the LAST such header, and the text that
   follows it on the same line begins `R28 ` once its leading space is stripped —
   the entry is one paragraph on one line, so that space is the separator and not
   a defect.

G8 THE IST-DOC. `docs/system/release-capability-v1.md` does NOT exist at
   `05c6e012` and DOES exist at C3 — report both `git ls-tree` readings. Its bytes
   at C3 are byte-equal to the DOC slice extracted from the committed C0a; report
   its sha256 and line count. Then the ordered equality constraint 10 fixes: the
   lines C3's diff adds for that path are exactly the slice's lines, in order.

G9 THE INDEX PAIRS, both APPEND-shaped per constraint 9, and NO FROM-zero count is
   ordered or reported for either. Print each pair's containment output on its own
   line. QUICKFROM occurs 1x in `docs/README.md` at `05c6e012` and 1x at C3, and
   QUICKTO occurs 1x at C3; the same three readings for SYSFROM and SYSTO. Then
   the ORDERED EQUALITY: the file at C3 is byte-equal to the `05c6e012` blob with
   QUICKFROM's single occurrence replaced by QUICKTO and SYSFROM's by SYSTO and
   nothing else changed. Report C3's sha256 and line count against the base's 228.
   Finally, over the lines C3's diff ADDS to `docs/README.md`, each of the two
   TO-ONLY rows occurs exactly 1x and the added-line count is 2.

G10 THE NEW ROWS ARE JUDGED, which is the payoff of R28 and the reason the two
    rounds are in this order. First, at C3 in the PRIMARY checkout, run
    `python3 -m pytest "tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve::test_every_relative_markdown_link_exists[docs/README.md]" -q -rf`
    and report that it PASSES — that case exists only because R28 repaired the
    parametrisation, and it is now reading the rows C3 added. Second, the RED
    CONTROL, in a disposable worktree at C3 under `.remedy-wt/` and never in the
    primary checkout (§4.10): in that worktree replace, in `docs/README.md` and in
    no other file, both occurrences of `system/release-capability-v1.md` with
    `system/release-capability-v0.md`, a file that does not exist. That byte
    string occurs exactly 2x in that file at C3 and 0x at `05c6e012`, both of them
    rows C3 adds — counted at emission per §3 item 25 — so "both" is exact. Run the
    SAME single-case command THERE and report that it FAILS naming
    `docs/README.md has broken links`. A gate that cannot fail on a broken row
    proves nothing about a row that resolves. Remove the worktree, run
    `git worktree prune`, then re-read `git worktree list` and
    `git status --porcelain` before C4.

G11 SUITES, serially in the PRIMARY checkout, each started only after the previous
    has ENDED and reported its exit code (F085 R64: two concurrent pytest
    processes produce false reds here). At C3: `python3 -m pytest tests/docs/ -q
    -rf`, which is the docs gate this change set requires — it must be GREEN, and
    report its passed COUNT beside the 295 the reviewer measured at `05c6e012`.
    The count is REPORTED, not predicted: no test in this repository enumerates
    `docs/system/*.md`, so a new page there adds no case, and if the number moves
    anyway that is a finding and not something to reconcile. Then `python3 -m
    pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, then the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q`. Report all three exit
    codes and summary lines.

G12 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md`,
    `docs/system/release-capability-v1.md` and `docs/README.md` at C4: each must
    be 0. Count marker LINES, not substrings — this handback quotes gate text, so
    a substring gate over `.agent/handoff.md` would be unmeetable (F086 R5).

G13 CHANGE SET, HISTORY AND THE HANDBACK. Print the range's path set and confirm
    it equals the Change list, with no path on either side alone. Confirm every
    path the Change section FORBIDS is PRESENT at `05c6e012` and untouched, that
    the range is linear, and that the round's `git reflog` entries are all
    `commit:`. Per constraint 11, for every commit BEFORE C4 print
    `git diff --numstat <sha>^ <sha>` and confirm each `+/-` cell of the
    handback's `## Commits` table is byte-identical to that pair, insertion column
    alone against the 500 cap (DECISION F104 D1); C4's own row is measurable only
    after C4 and goes in the round report (§3 item 14). Then report `wc -l` of
    `.agent/handoff.md` at C4 against the bound CONSTRAINT 12 states — this gate
    names that constraint rather than restating its numeral — and confirm all
    seven mandated headings of docs/agents/handback_template.md are present in the
    template's order with no section dropped.

G14 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing: the PR belongs to
    the closure round.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Push the
branch once, after C4. This round appends no verdict: R29's verdict is recorded by
the closure round's own ledger commit.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN29>>>
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
R29: record R28's verdict and write the packaging ist-doc. `docs/system/` has had
no page for what F086 built and AGENTS.md requires one; it was drafted for R27 and
again for R28 and cut both times on the block cap, so DECISION F085 D5 gives it a
round of its own. It lands with its two `docs/README.md` rows in the SAME commit
as the file they point at, which is the first change R28's repaired link gate
judges.

## Next Steps
1. CLOSURE is the next round and the last, per docs/roadmap/STATUS_closure_protocol.md
   — evidence job, FRESH review zip, the STATUS line, the README capability sync in
   that SAME commit, the PR. Precondition 4 is met: `## Built State` landed at
   `d420e8e5` and R28 corrected one sentence of it. The open set closes
   PASS_WITH_RISKS, as F083 and F085 both did. That round CREATES the PR, so it is
   the branch terminator §4 item 13 describes, and its verdict lives in the handoff
   and the PR rather than in a later gate entry.
2. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN; no
   round of this workflow can do either. Both are human actions, and closure names
   them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; this round
  touches no Python at all, so it gates ruff nowhere.
- `remedy integrity check` is denied to this session class, so closure precondition
  3 is met through the underlying module or declared unmet — never assumed.
<<<END PLAN29>>>

<<<SLICE RECORD28>>>
Gate: R29 — the R28 entry. R28 PASSED with NO finding, the second such round in a row, and the reviewer re-executed every gate R28's block ordered over `b86812be..05c6e012` rather than reading the handback. Every byte-level reading reproduces exactly: the transport at sha256 6bdf7e7d5d41c9018724b9e560c71d1c1d62c898f86183fc5ce3f178a622a3b5 over 30770 B and 353 lines, with the `.remedy-wt/` scratchpad still present and equal so the PRIMARY cmp form held rather than the digest fallback; PLAN28 at 277c0482644efd2b53f26b8a79443d3f00a5abd6baaf12611e8929b7e505233e over 49 lines, under the 50-line cap and carrying `## Goal`, `## Next Steps` and `F086`; the 6-line C2 remainder at 509fb277956a124fb0973d4b9db3d1ba264f01c6430557ca199023d0b3731342 and the 4-line C5 remainder at e5185e15320b506a1f9c2e912c97b04e9618ce0d48b127a41b0941ecc2e66022, each blank-separated as R-0578 requires and each a byte-exact suffix of a prefix-preserving append. BOTH PAIRS HELD IN THE REWRITE FORM THEIR CONTAINMENT TESTS DICTATED — `TO contains FROM: False` for each, FROM 1x at the base and 0x after, TO 1x after, and the ordered equality satisfied at ec119ea594eb021f741dffc9cc815da8c9bef4c7065a78ce11630f149e9bbfa2 over 92 lines for the feature file and c763e230f26e5e95e867fa10e93fa132d2f22254bf9f078db54380cdd8a65ff1 over 2033 lines for the test. THE LEDGER MOVED ON BOTH SIDES AND IN THE RIGHT ORDER: both extractions AGREE at all three ends — 177 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 173 open at `b86812be`, 179 / 4 / 0 / 0 / 0 / 175 at C2, 179 / 6 / 0 / 0 / 0 / 173 at C5 — the registered set gains exactly `R-0595` and `R-0596` at C2 and nothing at C5, the resolved set is unchanged at C2 and gains exactly those two at C5, and the control over `f0b27118..7b84524c` reads `[]` registered gained with exactly `R-0584` resolved gained. THE SCANS HELD WITH THEIR CONTROL BITING: over C2's 6 added lines and C5's 4, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 and 0 while the same extractor over `fd166295`'s added lines reads 3; the duplicated-header set is unchanged at exactly `Gate: R19 — the R18 entry.`; and `Gate: R28 — the R27 entry.` occurs 1x, is the LAST such header, and the text after it begins `R27 `. R-0596'S REPAIR IS REAL AND THE REVIEWER PROVED IT INDEPENDENTLY RATHER THAN ACCEPTING THE HANDBACK'S WORD, which is the one claim in this round no byte-equality could reach: the collected ids of `TestPrimaryDocLinksResolve` are five distinct paths including `[docs/README.md]` with neither `[README.md0]` nor `[README.md1]` among them; and with ONE identical broken row appended to `docs/README.md` in two disposable worktrees, the tree at `05c6e012` FAILS with `AssertionError: docs/README.md has broken links: ['system/no-such-doc-v0.md']` at 1 failed and 294 passed while the tree at `b86812be` PASSES at 295 — the same row, opposite colours, which is what makes the second reading evidence of the repair rather than of the row. THE FIX IS ALSO THE FILE'S OWN IDIOM, checked rather than assumed: `str(p.relative_to(REPO))` is how the two sibling tests at that file's `test_no_doc_still_claims_150_feature_files` and `test_no_doc_references_a_missing_roadmap_ledger` already spell a primary doc at `b86812be`, and neither was ever affected because both iterate the whole list instead of parametrising by a key, so `TestPrimaryDocLinksResolve` was the lone outlier and no sibling defect of the same class survives. R-0595'S CORRECTION IS TRUE AGAINST THE TREE, which is the reading its own finding says every R27 gate lacked: at `05c6e012` `tests/test_packaging_smoke.py` defines `TestFrontendDistResolution` with its wheel-root, checkout and missing-index cases, while `tests/test_install_smoke.py` defines `TestInstallSmokeOptIn`, `TestBuildRootLiesOutsideTheRepository` and `TestVersionReportReading` and mentions no frontend resolver at all — and G8's confirmation that `tests/test_packaging_smoke.py` is absent from the change set is what distinguishes moving the claim to the code from moving the code to the claim. THE SUITES ARE GREEN ON THE REVIEWER'S OWN SERIAL RUNS: `tests/docs/` 295 passed at exit 0, then the four-file state-reader selection 160 passed at exit 0, then the canary 42 passed at exit 0. THE HYGIENE HELD: seven paths over eight single-parent commits, all twelve forbidden paths present at `b86812be` and none touched, `docs/system/release-capability-v1.md` absent at both ends, every `git reflog` entry `commit:`, no marker LINE in any target, `git worktree list` one line and the tree clean after the reviewer's own two control worktrees were removed and pruned; item 28 bound for the third round running, with all seven measurable `+/-` cells byte-identical to `git diff --numstat` and a maximum insertion column of 353 under the 500 cap; and the handback is 57 lines, inside the 60-line cap with no DECISION D15 overage owed, all seven mandated headings present in the template's order.
<<<END RECORD28>>>

<<<SLICE DOC>>>
# Release Capability v1

> How Remedy ships: what the wheel carries, what `remedy --version` reports, and
> every reason the release gate refuses a release. Built by F086 — T001 packaging
> and the asset carry, T002 the version report, T003 the gate. The target plan is
> [T2_F086.md](../roadmap/features/T2_F086.md); this page describes what is BUILT,
> and its last section states what is NOT proven.

## Overview

Six files carry this capability and no seventh. `pyproject.toml` declares the
distribution, the console entrypoint and the carry that puts the built UI into the
wheel. `hatch_build.py` is the build hook: it refuses a wheel with no UI and
embeds the revision that wheel was built from. `apps/cli/version_report.py` reads
that revision back for `remedy --version`.
`packages/orchestration/release_gate.py` decides whether a release may proceed,
`scripts/release_gate_check.py` observes the real artifact and asks it, and
`.github/workflows/release.yml` runs that pair on a manual trigger. The split is
deliberate: the gate DECIDES and runs nothing, the script OBSERVES, so every value
judged comes from the artifact under release rather than from a second declaration
that could drift away from it.

## The wheel

`[project.scripts]` maps `remedy` to `apps.cli.grouped:main`, so installing the
wheel puts the CLI on PATH. The wheel target packages `packages` and `apps`.

The built UI is carried explicitly by `artifacts = ["apps/ui/dist/**"]`, and it
has to be named: `apps/ui/dist` is build output, untracked, and matched by the
generic `dist/` entry in `.gitignore`, so a VCS-aware backend omits it otherwise.
DECISION F086 D3 chose that mechanism by measurement at `72e07381`, from a probe
worktree outside the repository — `pyproject.toml` as committed produced 414
members and no files under `apps/ui/dist/`; `artifacts` produced 417 members,
2155470 bytes and 3 UI files; a `force-include` table produced 417 members,
2155479 bytes and the same 3. `artifacts` won because it needs no
source-to-target path mapping and is the smaller of the two.

The carry is NOT a guard. Measured at that same commit, a build with `artifacts`
applied and no `apps/ui/dist` present exits 0 and ships the same 414-member wheel
with no UI in it at all. That is what the build hook exists for.

## The build hook

`hatch_build.py` declares ONE hook class, `RemedyBuildHook`, because hatchling's
`load_plugin_from_script` refuses a script defining two. Its `initialize` does two
things. It calls `assert_frontend_assets_built`, which raises `ValueError` naming
`apps/ui/dist/index.html` and telling the caller to build the frontend first — so
DECISION F086 D1 part (b), never ship an empty UI silently, is enforced at build
time instead of discovered by a user. And it merges `build_revision_metadata`
into the build's `extra_metadata`.

Both rules live in plain module-level functions, so the test suite exercises them
without the build backend installed. The revision is written to a temporary
staging directory and never into the source tree: a generated file there would
survive the build and report a revision nobody built.

## Asset resolution has one mode, deliberately

Remedy deliberately does NOT carry a two-mode asset resolver. DECISION F086 D3
withdrew the one that was planned, after measurement: three `.parent` hops from
`packages/orchestration/ui_server.py` land on the wheel ROOT, and `apps/` is a
sibling of `packages/` at that root — the identical geometry a checkout has, so a
single expression already satisfies both modes. A second resolution path would
have been untested surface added to satisfy a premise that turned out false.

The property is still pinned per mode, because a regression would otherwise stay
invisible until a user's first serve: `TestFrontendDistResolution` in
`tests/test_packaging_smoke.py` asserts wheel-root mode, checkout mode, and that a
layout with no `index.html` resolves to `None`.

## Version and build info

DECISION F086 D2 keeps ONE version number, in `pyproject.toml`, and reads it back
through package metadata, so no second literal exists to drift out of sync.
`remedy --version` prints four lines — the distribution version, the build
revision, the Python version and the platform — and `handle_version_flag` runs
before the help pre-scan, so `--version` answers from anywhere in the command tree
rather than being swallowed by `--help` or by argparse.

In a checkout the distribution is usually not installed and no revision was
embedded at build time, and both fields then report `dev`. That is a requirement
and not a fallback: a version command reporting a fabricated revision is worse
than one that admits it is looking at a working tree. For the same reason Remedy
deliberately does not generate a `_version.py` at build time — a stale generated
file in a checkout would outrank the metadata.

The revision is read from `extra_metadata/REVISION` rather than `REVISION`,
because hatchling prefixes every hook-supplied extra-metadata entry with
`extra_metadata/` inside `.dist-info`. That was measured on a built wheel, not
inferred from the API.

## The release gate

`release_gate.py` decides and runs nothing, which is what makes each refusal
testable without a tag, a wheel or a CI run existing. `refuse_release` evaluates
every rule and returns ALL the reasons rather than the first, so a release broken
four ways is fixed once rather than four times.

| Refusal | The rule behind it |
|---|---|
| CI is not green | the observed conclusion is not `success` |
| the tag does not match the version | `normalise_tag` drops a leading `v`, then compares |
| there is no changelog section | `changelog_section` finds no `## [<version>]` heading |
| the changelog section is empty | the heading exists and its body is blank |
| the wheel is too big | its size exceeds `WHEEL_SIZE_BUDGET_BYTES` |

A missing section and an empty one are distinguished on purpose: a caller refuses
on both but must be able to say which. The budget is 8 MiB, measured rather than
guessed — a wheel carrying a stand-in `index.html` was 2040197 B at F086 R12 and
one carrying the built `apps/ui/dist` was 2155470 B at F086 R7 — so it is roughly
four times the real artifact. It admits a UI bundle's growth while still refusing
what it exists to catch: a wheel that swallowed `node_modules`, `.git` or the test
corpus.

`scripts/release_gate_check.py` supplies the values the gate judges. It reads the
version out of the built wheel's own FILENAME, the changelog off disk and the size
from the file itself, so a wheel built from some other version cannot pass by
agreeing with a declaration the build never read. It prints one
`REFUSED: <reason>` line per reason to stderr and exits 1, or reports that the
release may proceed and exits 0.

`.github/workflows/release.yml` fires on `workflow_dispatch` only — cutting a
release is a human decision, so nothing there runs on a push, a tag or a schedule.
It holds `contents: read` and `actions: read` and writes nothing back. It builds
the UI, builds the wheel, reads the conclusion of THIS commit's `ci.yml` run and
hands both to the checker. When no such run exists the step reports `missing`,
which is not `success`, so an absent answer is refused rather than counted as a
green one. The tag reaches the runner through the environment and is never
interpolated into a shell line, so a crafted tag cannot become a command.

Remedy deliberately does not publish from CI. That workflow has no upload step and
holds no index credential, because T2_F086's Do-not-touch keeps the final upload a
HUMAN command in v1.

## CHANGELOG.md is data

The changelog is not decoration — the gate parses it. Bumping the version in
`pyproject.toml` without adding a section for it fails the release rather than
shipping an unexplained one. The format follows Keep a Changelog, and the gate
reads only enough of it to check that the version's section exists and is not
empty.

## What is NOT proven

Two of this feature's DONE conditions are human actions, and no round of the build
workflow has performed either. They are listed here rather than left to be
inferred from a passing suite.

- No wheel has been installed into a fresh virtualenv.
  `tests/test_install_smoke.py` self-skips unless `REMEDY_INSTALL_SMOKE` is set,
  so its install coverage is zero wherever it currently runs (DECISION F086 D4).
  Its unit-level coverage of the surrounding helpers is real.
- `.github/workflows/release.yml` has never been dispatched, so the hosted gate
  has never judged a real release.
<<<END DOC>>>

<<<SLICE QUICKFROM>>>
| quickstart | [simple-operator-quickstart-v0.md](guides/simple-operator-quickstart-v0.md) | guide |
<<<END QUICKFROM>>>

<<<SLICE QUICKTO>>>
| quickstart | [simple-operator-quickstart-v0.md](guides/simple-operator-quickstart-v0.md) | guide |
| release / packaging | [release-capability-v1.md](system/release-capability-v1.md) | system |
<<<END QUICKTO>>>

<<<SLICE SYSFROM>>>
| [real-test-execution-v1.md](system/real-test-execution-v1.md) | Real test execution service |
<<<END SYSFROM>>>

<<<SLICE SYSTO>>>
| [real-test-execution-v1.md](system/real-test-execution-v1.md) | Real test execution service |
| [release-capability-v1.md](system/release-capability-v1.md) | What the wheel carries, what `remedy --version` reports, every reason the release gate refuses, and what F086 leaves unproven |
<<<END SYSTO>>>
