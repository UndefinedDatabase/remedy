── STEP findings + gate repair — F086 R28 ────────────────────
Goal:
Record R27's verdict, and register and fix the two defects the R27 review found by
reading the code rather than the record: R-0595, a false test location in the F086
feature file's `## Built State`, which closure precondition 4 rests on; and R-0596,
a documentation link gate that has never once evaluated the documentation index,
because it parametrises by filename and two of its primary docs are both named
`README.md`. This round writes no production code and runs no suite of its own
beyond the docs suite it repairs, the four state readers and the canary.

SCOPE NOTE, stated because it is a deliberate cut and not an oversight: the
packaging ist-doc and its two `docs/README.md` rows were drafted for this round and
REMOVED from it. With them the block measured 471 lines against the 400-line cap of
§3 item 1, and DECISION F085 D5 requires the design to change rather than the
wording to be shaved. They are R29's work, and PLAN28 carries them. The order is
not arbitrary: R-0596's fix is the gate those rows must be judged by, so it lands
first, in this round.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R28 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0595, FIND0596 and RECORD27.
4. `docs/roadmap/features/T2_F086.md` — the BUILT pair corrects the test location.
5. `tests/docs/test_docs_consistency.py` — the LINK pair repairs the gate.
6. `.agent/live_review.md` gains DONE0595 and DONE0596.
7. The handback.

Change:
Exactly these paths:
  `.agent/authored/f086-r28.md`                   (C0a)
  `.agent/last_block.md`                          (C0b)
  `.agent/plan.md`                                (C1)
  `.agent/live_review.md`                         (C2, then C5)
  `docs/roadmap/features/T2_F086.md`              (C3)
  `tests/docs/test_docs_consistency.py`           (C4)
  `.agent/handoff.md`                             (C6)
Nothing else. In particular NOT `docs/README.md`, not `docs/roadmap/STATUS.md`, not
`README.md`, not `pyproject.toml`, not `hatch_build.py`, not
`apps/cli/version_report.py`, not `packages/orchestration/release_gate.py`, not
`scripts/release_gate_check.py`, not `.github/workflows/release.yml`, not
`CHANGELOG.md`, not `tests/test_packaging_smoke.py`, not
`tests/test_install_smoke.py`, and nothing else under `apps/`, `packages/`,
`docs/system/` or `docs/agents/`. Every path this paragraph FORBIDS exists at
`b86812be` — resolved with `git cat-file -e` at emission per §3 item 24 — so the
prohibition forbids something real. `docs/system/release-capability-v1.md` is NOT
in either list: it does not exist yet and R29 creates it.

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
   ruling on a round is not. A worker-authored `Done:` paragraph is a finding
   however honestly it is hedged (§4.4); DONE0595 and DONE0596 are authored here.

5. COMMIT ORDER IS LOAD-BEARING, and this constraint is what DONE0595 and DONE0596
   name in place of a SHA that cannot exist when they are written (§3 item 20, the
   R-0524 carve-out): C3 and C4 both land before C5. A resolution committed before
   the fix it describes would assert a landed change that had not landed.

6. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback, and `git worktree list` reads ONE line at every
   commit and at the handback. G10's red control is the one exception and it is
   bounded: it runs in a disposable worktree under `.remedy-wt/`, takes no commit
   while it exists, and is removed and pruned before C5. NO FILE IN THE PRIMARY
   CHECKOUT IS OVERWRITTEN TO TAKE A READING (R-0594): every reading at a
   non-current revision is taken with `git show <sha>:<path>` into memory or into a
   scratch path under `.remedy-wt/`, never onto the tracked path itself — §3 item
   29, which landed at `5399dc0b` and binds this block first.

7. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals (a Python dict or set literal written inline counts)
   and env-prefix command forms. Route that work through `python3 - <<'PY'`
   heredocs or scripts under `.remedy-wt/`. Capture exit codes with
   `subprocess.run(...).returncode`, never with `$?`.

8. PAIR SHAPES, each from its own containment test run at emission, one reading
   per pair and neither generalised to the other (§3 item 15):
     BUILT — `TO contains FROM: False` → REWRITE, so FROM 1x at `b86812be` and 0x
             at C3, TO 1x at C3, plus the ordered equality.
     LINK  — `TO contains FROM: False` → REWRITE, the same three readings at C4.
   Each FROM occurs exactly 1x in its own target at `b86812be`, counted at emission.

9. THE FROM-ZERO GATES ARE SCOPED TO THEIR OWN TARGET FILE and to no other (§3
   item 2). FIND0595 QUOTES the sentence BUILTFROM removes and FIND0596 quotes the
   expression LINKFROM removes, but both land in `.agent/live_review.md`, which is
   neither pair's target. G8's count runs over
   `docs/roadmap/features/T2_F086.md` and G9's over
   `tests/docs/test_docs_consistency.py`, each alone.

10. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28). Every
    `+/-` cell you write in the handback's `## Commits` table is READ OUT of
    `git diff --numstat <sha>^ <sha>` for that commit and pasted from that
    reading. Never derive a cell from a file's line count before and after.

11. THE HANDBACK'S SIZE IS STATED ONCE, HERE, AND NOWHERE ELSE (§3 item 14's sweep
    rule). This round appends NO verdict slice, so C6 is the only commit that
    writes `.agent/handoff.md` and a whole-file reading is honest at it. KEEP C6 AT
    60 LINES OR FEWER, the AGENTS.md cap, with no DECISION D15 overage to declare.
    Write it in the COMPACT form: ONE commits table with a per-commit row, ONE LINE
    PER GATE in the Verification section, the transcript going to your round report
    and not into the file (R-0582). G13 NAMES this constraint instead of restating
    its numeral, deliberately: measured at emission, `60` occurs in this constraint
    and in no other clause of this block. If C6 nevertheless lands above that
    bound, do NOT drop a mandated section — exceed the cap and write the DECISION
    D15 "Deviations, declared" line naming the real count and the mandated content
    that caused it.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 6's readings all
   taken and reported, including the explicit statement that no path in the primary
   checkout was overwritten to take a reading.

G2 TRANSPORT. `.remedy-wt/f086-r28.md`, the committed `.agent/authored/f086-r28.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN28 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPENDS, both of them, each proved in the prefix-and-remainder form
   against slices extracted from the committed C0a. The pre-C2 blob is a byte-exact
   PREFIX of the post-C2 blob whose remainder is a blank line, FIND0595, a blank
   line, FIND0596, a blank line and RECORD27; the pre-C5 blob is a byte-exact
   PREFIX of the post-C5 blob whose remainder is a blank line, DONE0595, a blank
   line and DONE0596. Report each remainder's sha256 and line count. The blank line
   between entries is mandatory (R-0578).

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = `^- R-\d+ — `; resolved = `^Done: R-\d+ — `. Report at `b86812be`,
   at C2 and at C5: registered, resolved, duplicate, unregistered-resolution,
   `Landed:` and open counts. The registered set gains exactly `R-0595` and
   `R-0596` at C2 and nothing further at C5; the resolved set is UNCHANGED at C2
   and gains exactly those same two ids at C5, so no resolution is unregistered at
   any point. CONTROL, which must MOVE so the reading is not vacuous: the same two
   extractions over `f0b27118..7b84524c` report `[]` registered while the resolved
   set gains exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, and again over
   the lines C5 adds, delete every backtick-quoted span FIRST — a token a finding
   QUOTES is not one it USES (R-0584) — then count `\bHEAD\b` in what remains: each
   must read 0. RED CONTROL, the same two-step extractor over the lines `fd166295`
   adds to the same file: it must read 3, or the extractor is broken and the two
   zeros prove nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `b86812be` and at C2 and the
   SET occurring more than once at each: that set must be UNCHANGED and exactly
   `Gate: R19 — the R18 entry.`, which constraint 3 preserves. Then `Gate: R28 —
   the R27 entry.` occurs exactly 1x, is the LAST such header, and the text
   immediately following it begins `R27 `.

G8 THE BUILT PAIR, proved in the REWRITE form constraint 8 fixes. Print the
   containment test's own output. BUILTFROM occurs 1x in
   `docs/roadmap/features/T2_F086.md` at `b86812be` and 0x at C3; BUILTTO occurs 1x
   at C3. Then the ORDERED EQUALITY: the file at C3 is byte-equal to the `b86812be`
   blob with BUILTFROM's single occurrence replaced by BUILTTO and nothing else
   changed. Report C3's sha256 and line count against the base's 90. Also confirm
   `tests/test_packaging_smoke.py` is ABSENT from this round's change set, because
   the correction NAMES that file and must not touch it — a claim made true by
   editing the code it describes would be the opposite of this fix.

G9 THE LINK PAIR, the same REWRITE form, over `tests/docs/test_docs_consistency.py`.
   Print the containment output; LINKFROM 1x at `b86812be` and 0x at C4, LINKTO 1x
   at C4; then the ordered equality against the `b86812be` blob. Report C4's sha256
   and line count against the base's 2029. Then lint that path at `b86812be` and at
   C4 by feeding each blob to `python3 -m ruff check --stdin-filename
   tests/docs/test_docs_consistency.py -` on stdin — the non-writing mechanism §3
   item 29 requires, and the one that keeps `per-file-ignores` resolving by path —
   and report the rule-code MULTISET at each end. COMPARE the two multisets and
   report whether C4's is a subset of the base's; do NOT demand exit 0, because
   ruff is red repo-wide and this path may carry pre-existing findings.

G10 THE GATE REPAIR IS REAL, which is this round's central claim and the one no
    byte-equality can reach. First, at C4, `python3 -m pytest
    tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve --collect-only
    -q` — report the collected test IDs VERBATIM: exactly five, one of them
    `[docs/README.md]`, and NEITHER `[README.md0]` NOR `[README.md1]` present.
    Second, the RED CONTROL, in a disposable worktree at C4 under `.remedy-wt/` and
    never in the primary checkout (§4.10): append the single line
    `| [no-such-doc-v0.md](system/no-such-doc-v0.md) | red control |` to
    `docs/README.md` THERE, run `python3 -m pytest tests/docs/ -q -rf`, and report
    that it FAILS naming `docs/README.md has broken links`. Third, the SAME control
    in a second disposable worktree at `b86812be`, where it must PASS — that is
    what makes the second reading evidence of the repair rather than of the row.
    Remove both worktrees and run `git worktree prune`, then re-read `git worktree
    list` and `git status --porcelain` before C5.

G11 SUITES, serially in the PRIMARY checkout, each started only after the previous
    has ENDED and reported its exit code (F085 R64: two concurrent pytest processes
    produce false reds here). At C4: `python3 -m pytest tests/docs/ -q -rf`, which
    is the §3 docs-round gate this change set requires and the gate this round
    repaired — it must be GREEN, and report its passed COUNT against the 295 the
    reviewer measured at `b86812be`, since the repair changes which files are read
    without changing how many cases run. Then `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, then the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q`. Report all three exit
    codes and summary lines. NOTE, so the handback does not claim more than it
    proves: no suite in this repository reads
    `docs/roadmap/features/T2_F086.md` for the sentence C3 corrects, so G8 is that
    commit's whole evidence and a green suite says nothing about it.

G12 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/features/T2_F086.md`
    and `tests/docs/test_docs_consistency.py` at C6: each must be 0. Count marker
    LINES, not substrings — this handback quotes gate text, so a substring gate
    over `.agent/handoff.md` would be unmeetable (F086 R5).

G13 CHANGE SET, HISTORY AND THE HANDBACK. Print the range's path set and confirm it
    equals the Change list, with no path on either side alone. Confirm every path
    the Change section FORBIDS is PRESENT at `b86812be` and untouched, that
    `docs/system/release-capability-v1.md` is absent at BOTH ends, that the range is
    linear, and that the round's `git reflog` entries are all `commit:`. Per
    constraint 10, for every commit BEFORE C6 print `git diff --numstat <sha>^
    <sha>` and confirm each `+/-` cell of the handback's `## Commits` table is
    byte-identical to that pair, insertion column alone against the 500 cap
    (DECISION F104 D1); C6's own row is measurable only after C6 and goes in the
    round report (§3 item 14). Then report `wc -l` of `.agent/handoff.md` at C6
    against the bound CONSTRAINT 11 states — this gate names that constraint rather
    than restating its numeral — and confirm all seven mandated headings of
    docs/agents/handback_template.md are present in the template's order with no
    section dropped.

G14 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Push the
branch once, after C6. This round appends no verdict: R28's verdict is recorded by
R29's own ledger commit.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN28>>>
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
R28: record R27's verdict, and register and fix R-0595 — a false test location in
the F086 feature file's Built State — and R-0596 — the documentation link gate
never evaluated the documentation index, because it parametrised by filename and
two primary docs are both named README.md. The gate is repaired HERE so that R29's
index rows are judged by a gate that works.

## Next Steps
1. THE PACKAGING IST-DOC is R29's work and its FIRST work: `docs/system/` has no
   page for what F086 built and AGENTS.md requires one. It was drafted for R27 and
   again for R28, and cut each time on the block cap; DECISION F085 D5 requires the
   design to change, so it now gets a round of its own. It lands with its two
   `docs/README.md` rows in the SAME commit as the file they point at, and it must
   land BEFORE the closure commit, whose path set R-0154 fixes at STATUS.md,
   README.md and `.agent/`.
2. CLOSURE then follows, per docs/roadmap/STATUS_closure_protocol.md — evidence
   job, FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precondition 4 is met: `## Built State` landed at `d420e8e5` and
   R28 corrects one sentence of it. The open set closes PASS_WITH_RISKS, as F083
   and F085 both did. That round CREATES the PR, so it is the branch terminator §4
   item 13 describes and its verdict lives in the handoff and the PR.
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
<<<END PLAN28>>>

<<<SLICE FIND0595>>>
- R-0595 — Low — A `## Built State` SENTENCE NAMES THE WRONG TEST FILE FOR THE DUAL-MODE ASSET RESOLUTION, AND EVERY GATE THAT ROUND ORDERED WAS BLIND TO IT BECAUSE ALL OF THEM MEASURED BYTES. The F086 feature file's Built State, landed at `d420e8e5`, reads "Dual-mode asset resolution and the install smoke live in `tests/test_install_smoke.py`". The second half is true; the first is false. Measured at `b86812be`: `tests/test_install_smoke.py` contains the classes `TestInstallSmokeOptIn`, `TestBuildRootLiesOutsideTheRepository` and `TestVersionReportReading` plus the opt-in-gated install test, and NO test of the frontend resolver; the dual-mode property is pinned by `TestFrontendDistResolution` in `tests/test_packaging_smoke.py`, whose three cases assert the wheel-root mode, the checkout mode and the missing-index case. THE CLASS IS R-0561: the R26 block gated that slice for byte equality, for marker leakage and for its pair shape, and a slice can satisfy every one of those while stating a falsehood, because none of them reads the sentence against the tree it describes. ONE WRITER MAKES THE CLAIM AND ONLY ONE, checked rather than assumed (R-0391): `grep -rn 'test_install_smoke' docs/ .agent/*.md README.md` at `b86812be` returns five hits, of which the other four — the same file's SKIP sentence, DECISION F086 D4, `.agent/plan.md` and `.agent/last_block.md` — say only that the install smoke lives there, which is true. WHY LOW: nothing executable depends on the sentence and no measurement rests on it. WHY IT IS FIXED NOW RATHER THAN AT CLOSURE: closure precondition 4 is this very section, so the closure round would otherwise enter the permanent record citing a section with a false line in it. The correction is applied by this round's C3 to the feature file, which is a document and not an append-only record, so item 20's dated-correction rule does not reach it.
<<<END FIND0595>>>

<<<SLICE FIND0596>>>
- R-0596 — Medium — THE DOCUMENTATION LINK GATE HAS NEVER ONCE EVALUATED THE DOCUMENTATION INDEX: TWO PRIMARY DOCS ARE BOTH NAMED `README.md`, THE TEST PARAMETRISES BY FILENAME, AND ITS LOOKUP RESOLVES BOTH TO THE FIRST. `tests/docs/test_docs_consistency.py` declares `PRIMARY_DOCS` as the repository `README.md`, `AGENTS.md`, `docs/README.md`, `docs/roadmap/STATUS.md` and `docs/roadmap/ROADMAP.md`, then parametrises `TestPrimaryDocLinksResolve` over `[p.name for p in PRIMARY_DOCS]` and recovers the path with `next(p for p in PRIMARY_DOCS if p.name == doc)`. Measured at `b86812be`, that list of names is `['README.md', 'AGENTS.md', 'README.md', 'STATUS.md', 'ROADMAP.md']`; pytest disambiguates the collision into the ids `[README.md0]` and `[README.md1]`, but `next` cannot, so BOTH resolve to the repository root `README.md` and `docs/README.md` is read by no case. THE GATE IS VACUOUS AND WAS PROVED SO, not argued: in a disposable worktree at `b86812be` a row whose link target does not exist was appended to `docs/README.md`, and `python3 -m pytest tests/docs/ -q` still reported `295 passed` at exit 0. WHY MEDIUM rather than Low: AGENTS.md requires every new or renamed doc to be registered in `docs/README.md`, so that file accumulates links faster than any other primary doc, and it is the one primary doc whose links nothing checks — the R-0438 vacuous-gate class, arriving through a parametrisation id rather than through a missing path. THE FIX IS THIS ROUND'S C4 and it is one expression: parametrise by the repo-relative PATH, which is unique by construction, and index by it directly. Measured in that same worktree with the fix applied: the collected ids become five distinct ones including `[docs/README.md]`, the same broken row then FAILS naming `docs/README.md has broken links`, and the unmodified tree stays at `295 passed` — so the repair adds a real reading without turning any existing link red.
<<<END FIND0596>>>

<<<SLICE RECORD27>>>
Gate: R28 — the R27 entry. R27 PASSED with NO finding — the first round of this feature to do so since R25, and the reviewer looked for one. Every gate R27's block ordered was RE-EXECUTED by the reviewer over `788849bb..b86812be` rather than read from the handback, and every reading reproduces to the byte, including the four digests the handback states: the transport at sha256 94f81b70d17c0135444c666b7efb432fc5f6ea3b07826d2adb01b247a2813e8e over 26606 B and 332 lines, with the `.remedy-wt/` scratchpad still present and equal, so the PRIMARY cmp form held rather than the digest fallback; PLAN27 at e69c3b53cbc1c2effa7a2b2bda0175bef8818c170c9e4d121974bf23db5e224f over 44 lines, under the 50-line cap and carrying `## Goal`, `## Next Steps` and `F086`; the 4-line ledger remainder at afb559abfc836b65eae1200cc469de75b3895455169835979d57da2332b0ec5c, blank-separated as R-0578 requires; and `docs/agents/planner_reviewer_prompt.md` at a6d4242c91a32dc5c85c987a30bd1ca8fe71c99d3747893f6ae62017f59de854 over 901 lines against the base's 883. THE CHECK29 PAIR HELD IN THE APPEND FORM ITS CONTAINMENT TEST DICTATED — `TO contains FROM: True`, FROM 1x at both ends, no FROM-zero count attempted, and the ordered equality satisfied — and the STRUCTURE reading proves nothing was renumbered: `^  27\. \*\*`, `^  28\. \*\*` and `^  29\. \*\*` each read 1 at C3, and the line following item 29 is the checklist's closing paragraph, so the item landed between item 28 and that paragraph exactly as the bundle said. THE LEDGER MOVED ONLY ON THE REGISTERED SIDE: both extractions AGREE at each end — 176 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 172 open at `788849bb`, and 177 / 4 / 0 / 0 / 0 / 173 at C2 — the resolved set is equal, the registered set gains exactly `R-0594`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. THE SCANS HELD WITH THEIR CONTROLS BITING: over the 4 lines C2 adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 while the same extractor over `fd166295`'s added lines reads 3; the duplicated-header set is unchanged at exactly `Gate: R19 — the R18 entry.`; and `Gate: R27 — the R26 entry.` occurs 1x, is the LAST such header, and the text after it begins `R26 `. R-0594'S OWN SUBJECT WAS RE-MEASURED BY THE MECHANISM ITS COUNTER-MEASURE NAMES, which is the strongest thing this round can say about item 29: feeding the `8fe709a8` and the `b86812be` blobs of `packages/orchestration/release_gate.py` to `ruff check --stdin-filename packages/orchestration/release_gate.py -` returns an EMPTY rule-code multiset at exit 0 at both ends with nothing written to the working tree — and the mechanism itself was RED-CONTROLLED, because the same bytes fed under a path carrying no `per-file-ignores` entry report 1 error where the real path reports none, so `--stdin-filename` demonstrably resolves that configuration and item 29's parenthetical is a measurement rather than a hope. THE SUITES ARE GREEN ON THE REVIEWER'S OWN SERIAL RUNS: the four-file state-reader selection 160 passed at exit 0, then, after it had ended, the canary 42 passed at exit 0. THE HYGIENE HELD: six paths over seven single-parent commits, all seven forbidden paths present at `788849bb` and none touched, nothing under `apps/`, `packages/`, `tests/`, `docs/system/` or `.github/`, every `git reflog` entry `commit:`, no marker LINE in any target, `git worktree list` one line and the tree clean; item 28 bound for the second round running, with all five measurable `+/-` cells byte-identical to `git diff --numstat` and a maximum insertion column of 332 under the 500 cap; and the handback is 50 lines at C4 and 98 at C5, the first a byte-exact prefix of the second whose 48-line remainder is byte-equal to VERDICT, all seven mandated headings present in the template's order. WHERE R27 COULD HAVE FAILED AND DID NOT is its own sweep clause: constraint 8 declared that `48` and `51` occur in that constraint and in no other clause of the block, and a grep of the block's prose finds both numerals only in its three lines — the R-0589 obligation met by a block that stated it about itself. WHAT R27'S GATES COULD NOT SEE, and what this round's two findings come from, is that all of them measured BYTES: the round applied a Built State sentence naming the wrong test file (R-0595) and no gate reads a sentence against the tree, and the documentation gate that should catch such things has never evaluated the documentation index at all (R-0596).
<<<END RECORD27>>>

<<<SLICE BUILTFROM>>>
  build whose `apps/ui/dist/index.html` is missing (D1 b). Dual-mode asset
  resolution and the install smoke live in `tests/test_install_smoke.py`.
<<<END BUILTFROM>>>

<<<SLICE BUILTTO>>>
  build whose `apps/ui/dist/index.html` is missing (D1 b). Dual-mode asset
  resolution is pinned by `TestFrontendDistResolution` in
  `tests/test_packaging_smoke.py`; the install smoke is
  `tests/test_install_smoke.py`. Corrected at F086 R28, finding R-0595.
<<<END BUILTTO>>>

<<<SLICE LINKFROM>>>
    @pytest.mark.parametrize("doc", [p.name for p in PRIMARY_DOCS])
    def test_every_relative_markdown_link_exists(self, doc):
        path = next(p for p in PRIMARY_DOCS if p.name == doc)
<<<END LINKFROM>>>

<<<SLICE LINKTO>>>
    # R-0596: parametrising by `p.name` collided the repository README.md with
    # docs/README.md and `next` resolved both to the first, so the documentation
    # INDEX — the one file AGENTS.md requires every new doc to be registered in —
    # was checked by no case. The repo-relative path is unique by construction.
    @pytest.mark.parametrize("doc", [str(p.relative_to(REPO)) for p in PRIMARY_DOCS])
    def test_every_relative_markdown_link_exists(self, doc):
        path = REPO / doc
<<<END LINKTO>>>

<<<SLICE DONE0595>>>
Done: R-0595 — Fixed by this round's C3, the commit constraint 5 fixes ahead of this entry. The false half of the sentence is replaced: `docs/roadmap/features/T2_F086.md` now attributes the dual-mode asset resolution to `TestFrontendDistResolution` in `tests/test_packaging_smoke.py` and the install smoke to `tests/test_install_smoke.py`, and names the round and the finding that corrected it. The correction is a REWRITE pair over a document rather than a dated append, because the feature file is not the append-only record item 20 governs. No test file was touched to make the sentence true — G8 confirms `tests/test_packaging_smoke.py` is absent from this round's change set — so the fix moved the CLAIM to the code and not the code to the claim.
<<<END DONE0595>>>

<<<SLICE DONE0596>>>
Done: R-0596 — Fixed by this round's C4, the commit constraint 5 fixes ahead of this entry. `TestPrimaryDocLinksResolve` now parametrises over `str(p.relative_to(REPO))` and indexes by that path, so each primary doc gets its own case and `docs/README.md` is read for the first time. The repair is proved in two readings no byte-equality could give, both ordered by G10: the collected ids at C4 are five distinct paths including `[docs/README.md]` with neither `[README.md0]` nor `[README.md1]` among them, and the red control in a disposable worktree — one row pointing at a file that does not exist — FAILS at C4 naming `docs/README.md has broken links` while the SAME control at `b86812be` passes. The first reading shows the index is now reached; the second shows that reaching it has teeth. R29's index rows for the packaging ist-doc are the first change this gate will judge.
<<<END DONE0596>>>
