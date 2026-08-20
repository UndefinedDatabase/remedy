── STEP closure — F086 R31 ───────────────────────────────────
Goal:
Close F086. Register the one finding R30's review produced, record R30's verdict,
then make the closure commit the protocol fixes: the `[x]` STATUS line carrying
the values R30 measured, the README capability sync in that SAME commit, and the
final handback — after which the pull request is created and NOT merged. This is
the branch terminator: §4 item 13's carve-out belongs to the round whose own
bundle CREATES the pull request, which is this one, so R31's own verdict lives in
`.agent/handoff.md`, in the PR and in the reviewer's report rather than in a later
gate entry.

THE FOUR CLOSURE VALUES were MEASURED at R30 and are quoted here verbatim; they
are not re-derived, and a value that disagrees with this list is a stop:
  evidence job   f086-closure
  package        remedy-review-20260820-200318-READY_FOR_REVIEW.zip
  SHA-256        bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855
  accepted HEAD  f5fa19c368ed15d14ee6067fc69fde4fbc7863a6
The accepted HEAD is R30's C2, which is the head the package's manifest records
as `committed_review_subject.head_commit`; the reviewer read that value out of the
package itself. This round's own commits come AFTER it, which is what the closure
protocol's build order requires and not a defect.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R31 (§3 item 23 — this round registers a finding,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains FIND0597 and RECORD30.
4. THE CLOSURE COMMIT: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md` together, and nothing else.
5. The pull request, created and left unmerged.

Change:
Exactly these paths:
  `.agent/authored/f086-r31.md`                   (C0a)
  `.agent/last_block.md`                          (C0b)
  `.agent/plan.md`                                (C1)
  `.agent/live_review.md`                         (C2)
  `docs/roadmap/STATUS.md`                        (C3)
  `README.md`                                     (C3)
  `.agent/handoff.md`                             (C3)
Nothing else. In particular NOT `.agent/candidates.md` — the carrier is already
correct and empty, and this closure produced no candidate that is not being
registered here with a real id — not `.agent/context.md`, not
`docs/system/release-capability-v1.md`, not `docs/README.md`, not
`docs/roadmap/features/T2_F086.md`, not `CHANGELOG.md`, not `pyproject.toml`, not
`docs/agents/planner_reviewer_prompt.md`, and nothing under `apps/`, `packages/`
or `tests/`. Every path this paragraph FORBIDS exists at `d1889132`, each resolved
with `git ls-tree` at emission per §3 item 24.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` stays exactly as it is (§3 item 20). You append only.

4. EVERY SLICE IS THE REVIEWER'S TEXT. Do not summarise, rewrap or reformat one.
   Do not write a verdict of your own anywhere. The PR body is a slice: write
   PRBODY byte-verbatim to `.remedy-wt/f086_pr_body.md` and pass it with
   `--body-file`; do not compose a description of your own.

5. RULE A4 — THE STATUS EDIT IS THE LAST COMMIT ON THE BRANCH. C3 is the final
   commit and carries STATUS.md, README.md and the handback TOGETHER. The README
   sync may not land in a separate commit from the `[x]` line: R-0154 requires
   that README and STATUS never disagree in any committed state, and a split
   would create exactly that state. The pull request is created AFTER C3 and adds
   no commit.

6. THE HANDBACK CANNOT NAME THE PR NUMBER, and must not pretend to. C3 is written
   before `gh pr create` runs, so the number does not exist yet — ordering it
   would be the R-0371 defect this round exists to avoid repeating. The handback
   states that the PR is created immediately after C3; you report its number and
   URL to the reviewer in your round report.

7. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit and at the handback; `git worktree list` reads ONE line throughout —
   this round runs no destructive check. NO FILE IN THE PRIMARY CHECKOUT IS
   OVERWRITTEN TO TAKE A READING (§3 item 29). The review package
   `remedy-review-20260820-200318-READY_FOR_REVIEW.zip` sits in the repository
   root and is gitignored; leave it exactly where it is and do not add it.

8. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals (an inline Python dict or set literal counts) and
   env-prefix command forms. Route that work through `python3 - <<'PY'` heredocs
   or scripts under `.remedy-wt/`.

9. PAIR SHAPES, each from its own containment test run at emission, one reading
   per pair and none generalised to the others (§3 item 15):
     STATUSLINE — `TO contains FROM: False` → REWRITE: FROM 1x at `d1889132` and
                  0x at C3, TO 1x at C3, plus the ordered equality.
     RMCOUNT    — `TO contains FROM: False` → REWRITE, the same three readings.
     RMTIER     — `TO contains FROM: False` → REWRITE, the same three readings.
     RMLIST     — `TO contains FROM: False` → REWRITE, the same three readings.
   RMLIST LOOKS like an append and is NOT one: its TO ends the F107 entry with a
   comma where the FROM ends it with a period, and a TO that edits the FROM line
   at all is a REWRITE (§3 item 4). All four pairs are therefore rewrites and all
   four carry the FROM-zero reading; no pair in this block takes the §4.9 append
   obligation. Each FROM occurs exactly 1x in its own target at `d1889132`,
   counted at emission.

10. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28). Every
    `+/-` cell is READ OUT of `git diff --numstat <sha>^ <sha>` and pasted.

11. THE HANDBACK'S SIZE IS STATED ONCE, HERE, AND NOWHERE ELSE (§3 item 14's
    sweep rule). C3 is the only commit that writes `.agent/handoff.md`. KEEP C3'S
    HANDBACK AT 60 LINES OR FEWER, the AGENTS.md cap, in the COMPACT form: one
    commits table, ONE LINE PER GATE, the transcript in your round report
    (R-0582). G13 NAMES this constraint rather than restating its numeral:
    measured at emission, `60` occurs in this constraint and in no other clause of
    this block. If it lands above the bound, do NOT drop a mandated section —
    exceed it and write the DECISION D15 "Deviations, declared" line.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 7's readings all
   taken and reported.

G2 TRANSPORT. `.remedy-wt/f086-r31.md`, the committed `.agent/authored/f086-r31.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN31 extracted programmatically
   from the COMMITTED C0a. Report its sha256 and line count, which must be under
   50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps` and `F086`.

G4 LEDGER APPEND. The pre-C2 blob is a byte-exact PREFIX of the post-C2 blob whose
   remainder is a blank line, FIND0597, a blank line and RECORD30. Report the
   remainder's sha256 and line count. The blank separators are mandatory (R-0578).

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = `^- R-\d+ — `; resolved = `^Done: R-\d+ — `. Report at `d1889132`
   and at C2: registered, resolved, duplicate, unregistered-resolution, `Landed:`
   and open counts. The registered set gains EXACTLY `R-0597` and the resolved set
   is UNCHANGED, so no resolution is unregistered at any point. CONTROL, which
   must MOVE: the same two extractions over `f0b27118..7b84524c` report `[]`
   registered gained and exactly `R-0584` resolved gained.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST (R-0584), then count `\bHEAD\b` in what remains: it
   must read 0. RED CONTROL, the same extractor over the lines `fd166295` adds to
   the same file: it must read 3.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `d1889132` and at C2 and
   the SET occurring more than once at each: UNCHANGED and exactly `Gate: R19 —
   the R18 entry.`. Then `Gate: R31 — the R30 entry.` occurs exactly 1x, is the
   LAST such header, and the text following it on the same line begins `R30 ` once
   its leading space is stripped.

G8 THE STATUS LINE. Print the containment output. STATUSLINEFROM occurs 1x in
   `docs/roadmap/STATUS.md` at `d1889132` and 0x at C3; STATUSLINETO occurs 1x at
   C3. Then the ORDERED EQUALITY: the file at C3 equals the `d1889132` blob with
   that single occurrence replaced and nothing else changed. Report C3's sha256
   and line count against the base's 342. Then confirm, by literal count in the
   file at C3, that `- [x] F086 — Release capability (` occurs 1x and `- [~] F086`
   occurs 0x, and that the four closure values in the Goal above each occur in
   that line exactly as spelled there.

G9 THE README SYNC, three pairs, each with its own containment output printed on
   its own line. All three are REWRITES per constraint 9, so each takes the SAME
   three readings: FROM 1x in `README.md` at `d1889132` and 0x at C3, and TO 1x at
   C3. Then the ORDERED EQUALITY over the whole file: `README.md` at C3 equals the
   `d1889132` blob with each FROM's single occurrence replaced by its TO and
   nothing else changed. Report C3's sha256 and line count against the base's 124.

G10 THE LEDGER CROSS-CHECK, which is the gate that proves the sync is RIGHT rather
    than merely applied, and the reason R-0154 puts README and STATUS in one
    commit. At C3, serially in the PRIMARY checkout: `python3 -m pytest
    tests/docs/ -q -rf`. It must be GREEN. Three of its cases read exactly what
    this round changed — the accepted-id cross-check, the accepted-COUNT pin and
    the tier-table Done pin — so a wrong numeral here is a RED suite and not a
    silent drift. Report the passed count beside the 295 measured at `d1889132`.
    Then, after it has ENDED, `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, and after THAT the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q`. Report all three exit
    codes and summary lines. Never two pytest processes at once (F085 R64).

G11 RULE A4 AND THE CLOSURE COMMIT'S PATH SET. Print
    `git diff --name-only C3^ C3` and confirm it is EXACTLY
    `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md` — three paths,
    no more and no fewer. Confirm C3 is the LAST commit on the branch at the
    handback, and that no commit follows it.

G12 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md` and
    `README.md` at C3: each must be 0.

G13 CHANGE SET, HISTORY AND THE HANDBACK. Print the range's path set over
    `d1889132..HEAD` and confirm it equals the Change list with no path on either
    side alone. Confirm every path the Change section FORBIDS is PRESENT at
    `d1889132` and untouched, that the range is linear, and that the round's
    `git reflog` entries are all `commit:`. Per constraint 10, for every commit
    print `git diff --numstat <sha>^ <sha>` and confirm each `+/-` cell of the
    handback's `## Commits` table is byte-identical, insertion column alone
    against the 500 cap. Report `wc -l` of `.agent/handoff.md` at C3 against the
    bound CONSTRAINT 11 states, and confirm all seven mandated headings of
    docs/agents/handback_template.md are present in the template's order.

G14 THE PULL REQUEST, created LAST and NOT merged. Push the branch after C3, then
    write PRBODY byte-verbatim to `.remedy-wt/f086_pr_body.md` and run
    `gh pr create --base main --head feature/f086-release-capability --title "F086 Release capability — closure" --body-file .remedy-wt/f086_pr_body.md`.
    Report the PR number and URL. Then re-read
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
    report its literal output: it must now show exactly this one PR, from
    `feature/f086-release-capability` into `main`, `isDraft` false. DO NOT MERGE
    IT. The merge is the operator's manual-review window and happens at the next
    feature's start (STATUS_closure_protocol.md step 6, guardrail G1).

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report. It lands INSIDE
C3 together with STATUS.md and README.md, per constraint 5.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN31>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. R31 is the
closure round and the branch terminator; its pull request is created by this round
and merged by the NEXT feature's Open PR Gate, never here.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R31: register R-0597, record R30's verdict, then the closure commit — the `[x]`
STATUS line with the values R30 measured, the README capability sync in that SAME
commit (R-0154), and the handback — followed by the pull request, unmerged.

## Next Steps
1. THE PR IS NOT MERGED BY THIS SESSION. It merges at the next feature's start
   through the AGENTS.md Open PR Gate, which is the operator's manual-review
   window; the operator may merge it manually at any time instead.
2. THE NEXT FEATURE is selected by Rule A5 from `docs/roadmap/STATUS.md` — the
   first `[ ]` in ledger order — in a FRESH session. Its first reviewed round
   reads `.agent/candidates.md`, which this closure leaves empty and correct.
3. R-0597 IS OPEN AND ROUTED, not fixed here: the closure commit's path set is
   fixed by R-0154 at STATUS.md, README.md and `.agent/`, and the finding's
   counter-measure already exists as checklist item 8 — it was not run, rather
   than missing — so nothing is owed to `docs/agents/`.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
- The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
<<<END PLAN31>>>

<<<SLICE FIND0597>>>
- R-0597 — Low — A REVIEWER GATE ORDERED A VALUE THE PRODUCER DOES NOT EMIT, AND THE ROUND HAD TO SPEND A DECLARED DEVIATION PROVING IT. R30's G10 ordered the worker to "confirm the summary's final verdict is READY" for the closure evidence bundle. No producer in that bundle emits `READY` as a value: measured by the reviewer at `d1889132` over the 27-entry directory `.remedy-wt/f086_closure_evidence/remedy-job-evidence-f086-closure`, `create_manual_completion_bundle` returned `"verdict": "PASS_WITH_RISKS"`, `final_verifier_report.json` reads `verdict: PASS_WITH_RISKS`, `final_job_review.json` and `fresh_evidence_gate.json` each read `verdict: PASS`, and a scan of every `.json` file in the bundle for a bare `"READY"` value returns NONE. `READY` is the ZIP's vocabulary rather than the bundle's — `make_review_zip.sh` reports `PACKAGE_STATUS=READY_FOR_REVIEW`, which R30's G11 already ordered and which passed — so the gate asked the right question of the wrong artifact. THE CLASS IS CHECKLIST ITEM 8, "gates whose expected VALUE the code contradicts", and the counter-measure therefore already exists on disk and was simply not run: item 8 requires the reviewer to READ THE CODE THAT PRODUCES THE VALUE before asserting it, and the reviewer instead derived `READY` from what the field ought to be called — the exact derivation item 8 names and forbids. Nothing new is owed to `docs/agents/planner_reviewer_prompt.md`, and this finding deliberately proposes no new item: a checklist that grows an entry every time an existing entry is skipped protects nothing. WHY LOW: no false green was produced and no artifact is wrong. The bundle is sound, the package is `READY_FOR_REVIEW`, and the gate's real subject — that a complete closed-schema bundle exists and the final verifier ran over it — was met and separately evidenced. The whole cost is one declared deviation. WHY IT IS REGISTERED AT ALL: R-0590 and R-0591 are the same shape one feature earlier, all three are defects in the REVIEWER's own text rather than the worker's work, and the round that finds such a defect is the only round that can record it. WHAT SAVED IT was the worker, which applied the script byte-verbatim, ran it unedited, reported the real verdicts, proved the absence of `READY` by scanning the bundle, and declared the clause rather than reinterpreting it into something satisfiable — which is precisely the behaviour the split-writer rule exists to produce. OPEN, routed to a paydown branch with the other reviewer-process findings; the closure commit's path set (R-0154) cannot reach `docs/agents/`.
<<<END FIND0597>>>

<<<SLICE RECORD30>>>
Gate: R31 — the R30 entry. R30 PASSED with ONE finding, R-0597, and that finding is against the REVIEWER's own gate text rather than against any of the worker's work. Every gate R30's block ordered was RE-EXECUTED by the reviewer over `ea4ac5fa..d1889132`, and the two closure artifacts were verified from the artifacts themselves rather than from the handback. THE TRANSPORT HELD IN THE PRIMARY FORM AND AGAIN PROVED THE ROUND'S PROVENANCE: `.remedy-wt/f086-r30.md`, the committed `.agent/authored/f086-r30.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 3902376185df63018b5a60aed27ca8eb8a7e980972863be86fbd84b9e3642492 over 28188 B and 407 lines, and that digest is the one the reviewer computed BEFORE delegating. PLAN30 landed byte-exact at 44 lines under the 50-line cap with `## Goal`, `## Next Steps` and `F086` present; the 2-line C2 remainder is a blank line plus RECORD29 at sha256 76aff925591b36e4108608b373a242845178c5d1ffde191346f003a8db7f623d appended to a byte-exact prefix. THE LEDGER DID NOT MOVE, which is what a round registering nothing owes: both extractions AGREE at 179 registered / 6 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 173 open at both ends, the SETS are equal, and the control over `f0b27118..7b84524c` still MOVES with exactly `R-0584` resolved gained. THE SCANS HELD WITH THEIR CONTROL BITING: `\bHEAD\b` reads 0 over C2's 2 added lines after backtick-quoted spans are deleted, while the same extractor over `fd166295`'s added lines reads 3; the duplicated-header set is unchanged at exactly `Gate: R19 — the R18 entry.`; and `Gate: R30 — the R29 entry.` occurs 1x, is the LAST such header, and its text begins `R29 ` once the separating space is stripped. CLOSURE PRECONDITION 3 WAS RE-RUN BY THE REVIEWER THROUGH THE MODULE, because the `remedy` CLI is denied to this session class and neither actor pretended otherwise: all five checks of `packages.orchestration.integrity_gate` report `pass`, with `relevant_untracked` at `untracked=0, relevant=0` and `high_blockers_open` reporting no open blocker or high findings. CLOSURE PRECONDITION 2 WAS RE-RUN BY THE REVIEWER IN FULL, not read: `python3 -m pytest -n auto -q` in the primary checkout returned exit 0 at `17192 passed, 20 skipped`, which is byte-for-byte the same reading the worker recorded from its own independent run AND the same reading the integration gate took at `39bfc199`, so the suite has not moved across the seven rounds since that gate. THE EVIDENCE BUNDLE IS REAL AND COMPLETE: 27 entries on disk, five verification runs at 6, 12, 9, 7 and 42 passed with ZERO skipped and `len(node_ids) == selected` for each, 76 tests total, `tests/test_install_smoke.py` deliberately excluded because its single skip would have been rejected by the producer's own assertion. THE PACKAGE WAS VERIFIED FROM THE PACKAGE, which is the only reading that could not be taken from the handback: `remedy-review-20260820-200318-READY_FOR_REVIEW.zip` hashes to bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855 under the reviewer's own `sha256sum`, and its `.review_zip_manifest.json` reports `package_status: READY_FOR_REVIEW` with `committed_review_subject.base_commit` 76661dc1ff5ccc7cd4fe15ab88d53cff82d6d9dc — this branch's merge-base with `main` — and `head_commit` f5fa19c368ed15d14ee6067fc69fde4fbc7863a6, which is R30's C2 exactly as constraint 5 required. THE HYGIENE HELD: five `.agent/` paths over five single-parent commits with a maximum insertion column of 407 under the 500 cap and every `+/-` cell byte-identical to `git diff --numstat`; `docs/roadmap/STATUS.md`, `README.md` and `.agent/candidates.md` are all THREE absent from the range, as a round that must not close the feature early requires; all thirteen forbidden paths are present at `ea4ac5fa` and untouched; every `git reflog` entry is `commit:`; no marker LINE reached either state file; `git worktree list` is one line and the tree is clean; and the handback is 60 lines, exactly at its bound, with all seven mandated headings in the template's order. WHERE R30 WENT WRONG IS ENTIRELY IN ITS BLOCK: G10's `READY` clause named a value no producer in that bundle emits, the worker proved the absence by scanning every `.json` in the bundle and declared the clause instead of reinterpreting it, and that is R-0597 — the third consecutive feature in which the reviewer's own gate text is the only thing a round had to declare.
<<<END RECORD30>>>

<<<SLICE STATUSLINEFROM>>>
- [~] F086 — Release capability
<<<END STATUSLINEFROM>>>

<<<SLICE STATUSLINETO>>>
- [x] F086 — Release capability (T001–T003 complete; accepted 2026-08-20 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f086-closure · package remedy-review-20260820-200318-READY_FOR_REVIEW.zip · SHA-256 bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855 · accepted HEAD f5fa19c368ed15d14ee6067fc69fde4fbc7863a6)
<<<END STATUSLINETO>>>

<<<SLICE RMCOUNTFROM>>>
51 of 255 registered items accepted. Next: F086 (Release capability).
<<<END RMCOUNTFROM>>>

<<<SLICE RMCOUNTTO>>>
52 of 255 registered items accepted. Next: F255 (Teacher role).
<<<END RMCOUNTTO>>>

<<<SLICE RMTIERFROM>>>
| 2 | Minimal Self-Build Runtime | 13 | 14 |
<<<END RMTIERFROM>>>

<<<SLICE RMTIERTO>>>
| 2 | Minimal Self-Build Runtime | 14 | 14 |
<<<END RMTIERTO>>>

<<<SLICE RMLISTFROM>>>
F105 cache-optimal prompt ordering, F107 context compiler v2.
<<<END RMLISTFROM>>>

<<<SLICE RMLISTTO>>>
F105 cache-optimal prompt ordering, F107 context compiler v2,
F086 release capability (wheel, `remedy --version`, release gate).
<<<END RMLISTTO>>>

<<<SLICE PRBODY>>>
# F086 — Release capability (closure)

Closes the F086 branch. Remedy can be built as a wheel that carries the built UI,
report its own version and build revision, and refuse a release that is not fit to
ship. Publishing stays a human command, which the feature's Orchestrator brief
requires.

## What changed

- **T001 packaging.** `pyproject.toml` declares the console entrypoint `remedy`
  and carries the built UI with `artifacts = ["apps/ui/dist/**"]`; `hatch_build.py`
  is a build hook that refuses a wheel whose `apps/ui/dist/index.html` is missing
  and embeds the revision the wheel was built from.
- **T002 version.** `apps/cli/version_report.py` reads the version from package
  metadata and the revision from `<dist-info>/extra_metadata/REVISION`, reporting
  `dev` in a checkout rather than inventing a sha.
- **T003 release gate.** `packages/orchestration/release_gate.py` returns every
  reason to refuse a release, `scripts/release_gate_check.py` observes the real
  wheel and CI conclusion, and `.github/workflows/release.yml` runs both on a
  manual trigger only.
- **Documentation.** `docs/system/release-capability-v1.md` describes what was
  built, indexed from `docs/README.md`.

## Key decisions

- **F086 D1/D3** — the wheel carries the UI explicitly, and the planned dual-mode
  asset resolver was WITHDRAWN after measurement: a wheel root and a checkout have
  the identical geometry, so one expression already satisfies both. The test per
  mode was kept.
- **F086 D2** — one version literal, read back through package metadata; `dev` in
  a checkout is a requirement, not a fallback.
- **F086 D4** — the install smoke is written here and executed elsewhere.

## What is NOT proven, and is not claimed

- No wheel has been installed into a fresh virtualenv in any round.
  `tests/test_install_smoke.py` self-skips unless `REMEDY_INSTALL_SMOKE` is set,
  so its install coverage is zero.
- `.github/workflows/release.yml` has never been dispatched.

Both are human actions. The feature closes PASS_WITH_RISKS for exactly this
reason, and the ist-doc says so in its own last section.

## How to review

- Start at `docs/system/release-capability-v1.md`.
- The release gate's rules: `packages/orchestration/release_gate.py` with
  `tests/orchestration/test_release_gate.py`.
- Packaging: `hatch_build.py` with `tests/test_packaging_smoke.py`.
- Full suite at the accepted head: `17192 passed, 20 skipped`, exit 0.
- Review package: `remedy-review-20260820-200318-READY_FOR_REVIEW.zip`,
  SHA-256 `bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855`,
  accepted HEAD `f5fa19c368ed15d14ee6067fc69fde4fbc7863a6`.

## Verdict and runtime actuals

Latest live review PASS_WITH_RISKS. 31 rounds, each with a split worker and
reviewer; the reviewer re-ran every gate rather than reading the handbacks.
Models, wall clock and token cost across the whole feature: not-measured — the
ledger does not carry them per feature, and a guess is worse than the absence.

Not to be merged by the authoring session: this PR merges at the next feature's
start through the AGENTS.md Open PR Gate, which is the operator's manual-review
window.
<<<END PRBODY>>>
