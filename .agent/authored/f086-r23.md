── STEP integration gate — F086 R23 ──────────────────────────
Goal:
Record R22's verdict and R-0588's resolution in the finding ledger, then run
F086's INTEGRATION GATE — the tier-3 full-suite run of
docs/agents/planner_reviewer_prompt.md §3, executed exactly as
docs/agents/integration_gate.md prescribes — and commit its evidence. This round
writes no production code and changes no behaviour: it MEASURES the branch
against its merge base and records what it found.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R23 (§3 item 23 — this round touches the ledger,
   so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains RECORD21 and DONE0588.
4. The integration gate: branch run, base run, comparison, attribution, all of it
   committed under `.agent/gate_f086_r23/`.
5. The handback, then the reviewer's VERDICT appended to it.

Change:
Exactly these paths:
  `.agent/authored/f086-r23.md`   (C0a)
  `.agent/last_block.md`          (C0b)
  `.agent/plan.md`                (C1)
  `.agent/live_review.md`         (C2)
  `.agent/gate_f086_r23/**`       (C3, a new directory)
  `.agent/handoff.md`             (C4, then C5)
Nothing else. In particular NOT `tests/test_install_smoke.py`, not
`tests/conftest.py`, not `pyproject.toml`, not
`packages/orchestration/ci_stages.py`, not `packages/orchestration/ui_server.py`,
not `apps/cli/version_report.py`, and nothing else under `apps/`, `packages/`,
`tests/`, `docs/` or `.github/`. Every path this paragraph FORBIDS exists at
`43e7f1e0` — checked with `git ls-tree` at emission, per §3 item 24 — so the
prohibition forbids something real.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.

2. The change set is the path list above and nothing else. A gate run that
   modifies a tracked file is a STOP, not a fix.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is; §3 item 20 rules
   that the counter-measure for landed text is a dated correction in NEW text.
   You append only. G7 below is written so that duplicate is EXPECTED rather than
   forbidden, and a gate that reported it as a violation would be the defect.

4. PLAN23, RECORD21, DONE0588 and VERDICT are the reviewer's text. Do not
   summarise, rewrap or reformat them. Do not write a verdict of your own
   anywhere — not in the handoff, not in a commit message, not in your report.
   Reporting what a gate MEASURED is your job; ruling on a round is not. A
   worker-authored `Done:` paragraph is a finding however honestly it is hedged
   (§4.4).

5. WORKTREE HYGIENE, stated in two halves because this round DOES create a
   worktree and a blanket "one line throughout" would contradict its own bundle.
   (a) `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit
   and at the handback. (b) `git worktree list` reads ONE line at the start of
   the round and ONE line at the handback; between the base worktree's `add` and
   its `remove` it reads two, which is the round working as designed. The
   throwaway branch `tmp/base-gate-r23` is deleted with it. Neither exists at
   `43e7f1e0` — checked at emission — so neither `add` can collide.

6. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`,
   brace-with-quote literals and ENV-PREFIX command forms. That last one binds
   this round directly: `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest ...` will be
   REFUSED. Set that variable through a copied `os.environ` passed to
   `subprocess.run(..., env=...)` inside a `python3 - <<'PY'` heredoc, and route
   every loop the gate needs the same way.

7. SUITE LOGS ARE WRITTEN OUTSIDE THE TRACKED TREE while a run is in flight, to
   the gitignored scratch dir `.remedy-wt/.cache/gate_r23/` (`git check-ignore`
   confirms `.remedy-wt` is ignored, checked at emission). This is R-0176: a log
   growing inside the repo during a run changes the worktree digest mid-run and
   turns the manifest-identity ids into FALSE failures. Only derived evidence is
   committed, it is named `.txt` and never `.log` (R-0169: `.gitignore` drops
   `*.log` silently and the review-zip guard rejects any `\.log$` member), and
   each raw log's identity is pinned in `full_log_provenance.txt` by line count
   and sha256.

8. RUN THE TWO SUITES SERIALLY. The second starts only after the first has ENDED
   and reported its exit code. Two concurrent pytest processes produce false reds
   in this repository because the runtime suites bind ports (F085 R64).

9. THE HANDBACK'S LENGTH IS FIXED BY ARITHMETIC THIS BLOCK DOES FOR YOU, which is
   what §3 item 14 now requires of any file more than one commit builds. The
   VERDICT slice this block ships is 44 lines, measured at emission on its final
   bytes, and C5 appends it by pure concatenation — so the file at C5 is exactly
   C4's length plus 44. Write C4 in the COMPACT form: ONE commits table with a
   per-commit row, ONE LINE PER GATE in the Verification section with the
   transcript going to your round report and not into the file (R-0582). Keep C4
   at 56 lines or fewer, which puts C5 at 100 or fewer with no DECISION D15
   overage to declare. If C4 nevertheless lands above 56, do NOT drop a mandated
   section: exceed the cap, write the D15 "Deviations, declared" line naming the
   real count and the mandated content that caused it, and say so in the report.

10. IF THE GATE FINDS A BLOCKER — a branch-only failure that reproduces serially
    and is coupled to this feature's code — STOP after C3. Commit the evidence,
    write the handback naming the blocker, and end. Do not fix it: per
    docs/agents/integration_gate.md step 4 that repair is its own reviewer-gated
    round, and a worker who fixes and certifies in one round voids both. An empty
    branch-only set is a RESULT, not a requirement — this block does not order
    the gate's colour, and reporting a red one honestly is a PASS-shaped outcome
    for the round even though it blocks the feature.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 5's two
   readings both taken and both reported.

G2 TRANSPORT. `.remedy-wt/f086-r23.md`, the committed `.agent/authored/f086-r23.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN23 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND. The pre-C2 `.agent/live_review.md` blob is a byte-exact PREFIX
   of the post-C2 blob, and the remainder is byte-equal to a blank line, RECORD21,
   a blank line, DONE0588 — both extracted from the committed C0a. Report the
   remainder's sha256 and line count.

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = lines matching `^- R-\d+ — `; resolved = lines matching
   `^Done: R-\d+ — `. Report at `43e7f1e0` and at C2: registered count, resolved
   count, duplicate count, unregistered-resolution count, `Landed:` line count and
   open count. The REGISTERED set must be UNCHANGED between the two — this round
   registers nothing — and the RESOLVED set must gain exactly `R-0588` and nothing
   else. CONTROL, which must MOVE so the reading is not vacuous: the same two
   extractions over `f0b27118..7b84524c` report `[]` registered while the resolved
   set gains exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST — a token a finding QUOTES is not a token it USES
   (R-0584) — then count `\bHEAD\b` in what remains. It must read 0. RED CONTROL,
   same two-step extractor over the lines `fd166295` adds to the same file: it
   must read 3. A control that does not read 3 means the extractor is broken and
   the 0 proves nothing.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `43e7f1e0` and at C2, and
   the SET of strings occurring more than once at each. That duplicate set must be
   UNCHANGED and must be exactly `Gate: R19 — the R18 entry.` — constraint 3
   forbids repairing it, so it is the expected reading. Then: `Gate: R23 — the R22
   entry.` occurs exactly 1x, it is the LAST such header in the file, and the text
   immediately following it begins `R22 `.

G8 THE BRANCH RUN. In the PRIMARY checkout, from the repo root:
   `python3 -m pytest -n auto -q`, its log written to
   `.remedy-wt/.cache/gate_r23/branch_run.txt`. Record into
   `.agent/gate_f086_r23/branch_meta.txt`: checkout path, revision, the exact
   command, EXIT_CODE, WALL_SECONDS, the summary line and FAILED_COUNT. Write the
   sorted FAILED list to `branch_failed.txt` and the raw tail to
   `branch_run_tail.txt`.

G9 THE BASE RUN AND THE PARITY READING. Merge base is `76661dc1` — verified at
   emission as `git merge-base main HEAD`, and identical to both `main` and
   `origin/main`. Add the worktree ON THE THROWAWAY BRANCH
   (`git worktree add -b tmp/base-gate-r23 .remedy-wt/base-r23 76661dc1`): the
   self-dogfood guard refuses a detached HEAD by design (DECISION D3), so a
   detached base worktree would fail the guard-dependent ids for the wrong reason.
   COPY `apps/ui/node_modules` and `apps/ui/dist` in with `shutil.copytree` —
   NEVER symlink: the UI auto-build writes THROUGH a symlink into the primary
   checkout (F053 R3). Both are untracked build outputs, so they resolve on the
   FILESYSTEM and not in `git ls-tree`; both were confirmed present and not
   symlinks at emission. Set `REMEDY_UI_NO_AUTO_BUILD=1` per constraint 6, and do
   NOT trust it alone. READ FOUR VALUES: the sha256 over `apps/ui/dist` and the
   mtime_ns of `apps/ui/dist/index.html`, BEFORE the base run and AFTER it.
   A MOVED DIGEST **OR** A MOVED MTIME VOIDS THE PARITY CLAIM — the digest is
   blind to a byte-identical rebuild while `_frontend_is_stale()` in
   `packages/orchestration/ui_server.py` decides staleness by MTIME (R-0565; at
   F085 R72 the digest held still and the mtime moved). Record all four readings
   and the verdict in `base_parity.txt`, then the run's own records in
   `base_failed.txt` and `base_run_tail.txt`. Remove the worktree, delete
   `tmp/base-gate-r23`, prune, and print `git worktree list`.

G10 THE COMPARISON, then ATTRIBUTION. `comm -13 base_failed.txt branch_failed.txt`
    → `comm_branch_only_failures.txt`; `comm -23` → `comm_base_only_failures.txt`;
    report both line counts and commit both files even when empty. Then
    `attribution.txt`, WITH EVERY ID IN BOTH COMM OUTPUTS PRESENT
    AND NONE SILENTLY ABSENT. For every BRANCH-ONLY id: re-run that exact node id
    SERIALLY and classify — serial-pass is the xdist-flake class and is recorded
    rather than blocking; serial-fail is reproduced at `76661dc1` before the
    feature is blamed; a reproducible branch-only failure coupled to feature code
    is a BLOCKER and constraint 10 applies. For every BASE-ONLY id: if the parity
    claim went VOID, attribute it to its environment class BY DIRECT EVIDENCE,
    naming the missing or rebuilt artifact PER ID — an unattributed base-only id
    counts as a genuine base failure and blocks the gate verdict. If a comm output
    is empty, say so explicitly and say why it is empty by construction.

G11 LOG PROVENANCE. `full_log_provenance.txt` lists every raw log under
    `.remedy-wt/.cache/gate_r23/` with its line count and sha256, and states that
    the worktree and its branch were removed after the readings were taken.

G12 THE CANARY, run in the PRIMARY checkout after the gate runs have ended:
    `python3 -m pytest tests/cli/test_golden_path.py -q` → report exit code and
    the summary line.

G13 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md`, `.agent/live_review.md` and every file under
    `.agent/gate_f086_r23/` at C4: each must be 0. Count marker LINES, not
    substrings — this handback quotes gate text, so a substring gate over
    `.agent/handoff.md` would be unmeetable (F086 R5). The `.agent/handoff.md`
    reading can only be taken after C5 and goes in the round report.

G14 CHANGE SET AND HISTORY. Print the range's path set and confirm it equals the
    Change list above other than `.agent/handoff.md`, with no path on either side
    alone. Confirm every path the Change section FORBIDS is PRESENT at `43e7f1e0`.
    Confirm the range is linear — every commit at exactly one parent — that the
    round's `git reflog` entries are all `commit:`, and report each commit's
    INSERTION count (the `+` column only, per DECISION F104 D1), none over 500.

G15 THE HANDBACK, BOTH HALVES, per §3 item 14. (a) `wc -l` of `.agent/handoff.md`
    at C4 is at most 57. (b) at C5 it is exactly (a) plus 43, at most 100. All
    seven mandated headings of docs/agents/handback_template.md are present in the
    template's order and no section is dropped. The prefix-and-remainder equality
    against VERDICT is measurable only after C5 and goes in the round report.

G16 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing, merge nothing.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. Then
append VERDICT verbatim as C5. Push the branch once, after C5.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN23>>>
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
R23, the INTEGRATION GATE: record R22's verdict, resolve R-0588 — whose
counter-measure landed at `72640273` and which R22's own G13 then met — and run
the tier-3 full suite twice per docs/agents/integration_gate.md, branch and merge
base, with `apps/ui/node_modules` and `apps/ui/dist` parity restored by COPY, then
attribute every id in both comm outputs.

## Next Steps
1. CLOSURE per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH
   review zip, the STATUS line, the PR. The packaging ist-doc is written there,
   when the built state stops moving.
2. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- A branch-only failure the gate reproduces serially and couples to feature code
  is a BLOCKER whose repair is its own reviewer-gated round, never this one's.
- The base worktree lacks build outputs, so parity is restored by COPY and never
  by symlink; `apps/ui/dist` is read by DIGEST AND BY MTIME before and after that
  run, because at F085 R72 the digest held still while the mtime moved (R-0565).
  Either reading moving voids the parity claim and forces per-id attribution.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN23>>>

<<<SLICE RECORD21>>>
Gate: R23 — the R22 entry. R22 PASSED, with NO finding — the first round of this feature in four to produce none, and the round in which a rule authored one round earlier was demonstrated WORKING rather than merely landed. Every gate R22's block ordered was RE-EXECUTED by the reviewer over `e7cdae4d..43e7f1e0` rather than read from the handback, and every reading reproduces. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form, not the digest fallback: `.remedy-wt/f086-r22.md`, the committed `.agent/authored/f086-r22.md` at `787a1141` and the committed `.agent/last_block.md` at `39ab54ef` are byte-EQUAL at sha256 d4d00dfbf05f263c2c4f3b5a94eab14ab9533a84dcbcfeadcd46771741a5f4bf, 27444 B over 336 lines. EVERY SLICE LANDED BYTE-EXACT, each checked disk-to-disk against an extraction from the COMMITTED C0a and never against a retype: `.agent/plan.md` at `f6bafbdc` equals PLAN22 at sha256 1955bfe2937ae46ef5e3c7c5f10e8cc6973391936c535629b64d8b781a206ac7 over 44 lines, under the AGENTS.md cap of 50 and carrying `## Goal`, `## Next Steps` and `F086`; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0588, a blank line and RECORD20 at sha256 51cae6480f0be3fe54cda0b91134d1bd23ab8b04b8bd6cf31769f7707cceb132; and `docs/agents/planner_reviewer_prompt.md` at `72640273` is byte-equal to the `e7cdae4d` blob with CHECK14FROM's single occurrence replaced by CHECK14TO and nothing else changed, at sha256 1df716cdff9b2e290f43e311787a31bdfcde80483a9f37ec53bfc845b9aef12c over 820 lines against 805. THE PAIR WAS APPEND-SHAPED AND WAS PROVED IN THE APPEND FORM: the containment test prints `TO contains FROM: true`, CHECK14FROM occurs 1x at both ends, and the ordered-equality reading above is strictly stronger than the per-line count it replaces because it fixes position as well as multiplicity (§4.9, R-0531). THE CLAUSE LANDED INSIDE ITEM 14 AND RENUMBERED NOTHING: `grep -c '^  14\. \*\*'` and `grep -c '^  15\. \*\*'` each read 1, and the line following the last of the fifteen added lines is item 15's own heading line. R-0586'S SCAN HELD WITH ITS CONTROL BITING: over the lines `79dbd1d4` adds, backtick-quoted spans deleted first, `\bHEAD\b` reads 0, while the same two-step extractor over `fd166295`'s added lines reads 3. R-0587'S CHECK HELD IN THE FORM THAT LETS A LANDED DEFECT STAND: the duplicated-header SET is unchanged across the round and is exactly `Gate: R19 — the R18 entry.`, which constraint 3 forbade repairing; `Gate: R22 — the R21 entry.` occurs 1x, is the LAST such header, and the text after it begins `R21 `. The reviewer's own extractor reads one header more at each end than the handback does, because it also matches the combined `— the R1 and R2 entries.` form that the block's stricter pattern excludes; the two disagree on the DEFINITION of the set and on none of its load-bearing properties. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end — 170 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 167 open at `e7cdae4d`, and 171 / 3 / 0 / 0 / 0 / 168 at `79dbd1d4` — the registered SETS are equal, the symmetric difference is exactly `['R-0588']`, and the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`. THE SUITES WERE RE-RUN BY THE REVIEWER, NOT READ, serially and non-overlapping in the PRIMARY checkout: 160 passed for the four state readers, then 42 passed for the canary, both exit 0. THE HYGIENE HELD: six paths over seven single-parent commits inserting 336, 185, 11, 4, 15, 30 and 44 lines, none over 500 and no DECISION F104 D1 exemption invoked; all five paths the block FORBIDS exist at `e7cdae4d` and none is touched in the range; every `git reflog` entry of the round is `commit:`; no marker line reached any target; and the tree is clean at `43e7f1e0` with one worktree. FINALLY, THE FACTS INSIDE THE SLICES WERE CHECKED AND NOT ONLY THEIR BYTES, because a shape gate never fails on a false sentence (R-0561): FIND0588's arithmetic is exact — the handoff blob at `88bf8e7d` is 80 lines, `e7cdae4d` is 120, the first is a prefix of the second and the remainder is 40 — R21's G14 really does read "at the commit C5 creates is AT MOST 100 lines", and the R18 and R19 handbacks it cites as the compact form really are 97 and 96 lines.
<<<END RECORD21>>>

<<<SLICE DONE0588>>>
Done: R-0588 — RESOLVED, and resolved in the strong form: the counter-measure is not merely on disk, it was DEMONSTRATED WORKING by the very next block. Commit `72640273` extended §3 checklist item 14 from the per-commit reading to the whole-file one, ruling that a bound on a file MORE THAN ONE COMMIT builds is stated per commit and never once over the final state, and that the block computes any constant its own appended slices contribute. R22's own G13 then applied exactly that: it shipped a 44-line VERDICT slice, fixed C4's bound at 56 — the 100-line cap minus that constant — and bounded C5 at 100. The round landed at 52 lines for C4 and 96 for C5, so the content obligation and the arithmetic were BOTH satisfiable and no DECISION D15 "Deviations, declared" line was needed or written. Verified by the reviewer over `e7cdae4d..43e7f1e0`: the handoff blob at `6c8a0ede` is 52 lines, the blob at `43e7f1e0` is 96, the first is a byte-exact PREFIX of the second, and the 44-line remainder is byte-equal to the VERDICT slice extracted from the committed `.agent/authored/f086-r22.md`. The defect R-0588 named — a gate demanding a declaration in a commit that could not yet know the number it must declare — is unreachable under the item as it now reads.
<<<END DONE0588>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued; appended so the next handback rewrite cannot silently
destroy it. Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md,
resuming the branch at `43e7f1e0` and declaring a three-round cap up front per guardrail
G7. The reviewer wrote nothing in the work tree, one delegated worker per round made
every commit, and every verdict below rests on gates the reviewer RE-EXECUTED over the
committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R22 | e7cdae4d..43e7f1e0 | PASS — no finding |
| R23 | 43e7f1e0..HEAD | verdict not yet on disk; see the last paragraph |

R22 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was
planned. It is the first round of this feature in four to produce NO finding, and the
reason is worth recording: R21 registered R-0588 against the reviewer, R22 landed the
counter-measure into §3 item 14 at `72640273`, and R22's OWN handback was then bounded
by the rule it had just written — C4 at 56 lines because the block shipped a 44-line
VERDICT and 100 minus 44 is 56, landing at 52 and 96. A rule proved on its author beats
a rule merely filed, and this one closed R-0588 in the same round it was written.

The reviewer re-ran both suites rather than reading their colours — 160 passed for the
four state readers, then 42 for the canary, serially in the primary checkout — and
every transport digest, slice equality, ledger set and scan control reproduces. The
facts INSIDE the slices were checked as well as their bytes per R-0561, a shape gate
never failing on a false sentence.

R23 IS THE INTEGRATION GATE, whose result is not knowable when this text is authored,
so this block orders no colour for it and claims none. WHAT THIS FEATURE STILL OWES
after it is closure. NO INSTALL HAS BEEN PROVEN in this session or any other and no
round of this workflow can prove one — DECISION F086 D4 records that with its
measurement — and the release workflow has never been dispatched; both are human
actions, named at closure as unproven rather than counted as coverage.

R23 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict
to be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `43e7f1e0..HEAD` and record R23's verdict in
`.agent/live_review.md` as `Gate: R24 — the R23 entry.`, the header shape §3 item 26
binds. Its first substantive work is closure — unless R23's gate found a blocker, in
which case that repair is the next round and closure waits behind it.
<<<END VERDICT>>>
