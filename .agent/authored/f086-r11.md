── STEP R11 — F086 Release capability (record the R10 verdict; close the session) ──

Goal:
Close this session on disk. Record the R10 verdict in the finding ledger, and
write the reviewer's own session verdict into `.agent/handoff.md` so that no
verdict this session issued exists only in a transcript — which is finding
R-0571, registered by this feature. This is the LAST round of the session. No
code, no test, no PR.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r11.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN11 slice, whole file
  C2  append the RECORD9 slice to `.agent/live_review.md`
  C3  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C4  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. This round registers NO finding —
R10 produced none — so the open set does not move and no FINDINGS slice exists.

Why C4 exists and why it APPENDS. A branch's last round has no on-disk gate entry
by construction (docs/agents/planner_reviewer_prompt.md §4 item 13), so a session
that ends after its final verdict leaves that verdict nowhere. C4 APPENDS rather
than rewrites because a rewrite of `.agent/handoff.md` is precisely what destroys
a verdict already written into it.

Base:
This round starts from `dea9dc2f`, the tip of `feature/f086-release-capability`
and the R10 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. The slices are
PLAN11, RECORD9 and VERDICT. PLAN11 is a COMPLETE file including its single
trailing newline. RECORD9 and VERDICT are EOF-APPENDS, defined as pure
concatenation with each slice's own leading blank line INSIDE the slice, so
nothing is prepended and nothing is stripped. No FROM/TO pair exists in this
block.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `dea9dc2f`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r11.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r11.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r11.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN11 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD9 slice to `.agent/live_review.md` under the append
   convention. Commit alone. It is the reviewer's R10 verdict. The paragraph
   begins `Gate:` and registers no finding id, so it moves no ledger set.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of dea9dc2f..<HEAD>`.
   BEFORE writing it, measure the VERDICT slice's own line count from the
   COMMITTED `.agent/authored/f086-r11.md`, because C4 appends exactly those
   lines to this file. Your `Deviations & assumptions` section states the FINAL
   line count of `.agent/handoff.md` as it will stand after C4 — your own lines
   plus the slice's — and, if that total exceeds the cap, declares the overage
   under AGENTS.md DECISION D15 naming its cause: this round carries the
   reviewer's authored session verdict, which is mandated content for the round
   that closes a session, and no section is dropped to meet the cap. Do NOT trim
   after C4. Report your own C3 insertion count and the post-C3 path set in the
   ROUND REPORT rather than in the file, because a handoff cannot measure the
   commit that writes it (§3 item 14).
   The `Next` section names, in this order, the next session's first two actions:
   re-read `.agent/STOP` from disk (Phase 1 rule 1), then run the Open PR Gate
   (Phase 1 rule 2).

6. C4 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C3 must be a byte-exact PREFIX of the file at HEAD, and G8 measures
   exactly that.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r11.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, and `.agent/handoff.md` at C3 and C4. No path under
   `apps/`, `packages/`, `tests/`, `docs/` or `scripts/` is in it, and neither
   `pyproject.toml` nor `hatch_build.py` is: this round changes no behaviour and
   ships no code.
3. The VERDICT slice is the reviewer's text. Do not summarise it, do not
   reformat it, and do not write a verdict of your own anywhere — in the handoff,
   in a commit message, or in your report. Reporting what a gate MEASURED is your
   job; ruling on a round is not.
4. `git status --porcelain` in the primary checkout is EMPTY at every commit and
   at the handback, and `git worktree list` is exactly one line throughout. This
   round adds no worktree: it has nothing destructive to check.
5. Both suite commands run in the PRIMARY checkout, never in a worktree, and
   SERIALLY — the second starts only after the first has ENDED (finding R-0518).
6. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs; helper scripts under the gitignored
   `.remedy-wt/` are expected.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout; `git
    worktree list` exactly 1 line; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r11.md`, the committed
    `.agent/authored/f086-r11.md` and the committed `.agent/last_block.md` are
    all three byte-EQUAL. Report the sha256, the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN11 slice extracted
    from the COMMITTED `.agent/authored/f086-r11.md`. Report its sha256 and line
    count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob and the remainder is byte-equal to RECORD9. Report
    the sha256 of the remainder.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST AGREE AND MUST NOT MOVE. Extract
    twice — once by PARAGRAPH (split the file on blank lines; a paragraph counts
    when it STARTS with `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED
    (`^- R-\d+ — ` and `^Done: R-\d+ — `). At HEAD report registered / resolved /
    duplicate ids / unregistered resolutions / anchored `Landed:` lines / open,
    for BOTH, and the two registered id SETS must be EQUAL. Expected at HEAD:
    163 registered, 2 resolved, 0 duplicates, 0 unregistered resolutions,
    0 `Landed:`, 161 open. Report the symmetric difference of the HEAD registered
    set against the `dea9dc2f` set as the SET itself; it must be EMPTY, because
    this round registers nothing. The control proving the extractor can see a
    difference at all is already on disk in RECORD8, where the same extractor
    read `['R-0580']` added across R9.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md` and
    `.agent/handoff.md` at HEAD each contain 0 lines beginning `<<<SLICE ` or
    `<<<END `. Count marker LINES, not `<<<` substrings — this block's own text
    quotes those markers, and a handback quoting them is normal (finding from
    F086 R5).

G7  THE LEDGER CARRIES A VERDICT FOR EVERY REVIEWED ROUND OF THIS BRANCH. Count
    the paragraphs in `.agent/live_review.md` that begin `Gate: ` and report the
    count with the round each one names. At `dea9dc2f` the reviewer measured 8,
    naming R3 through R10; C2 adds the ninth, so HEAD must read 9 and the added
    one must name R11. R11's OWN entry is absent by construction and that absence
    is the terminator, not a gap (docs/agents/planner_reviewer_prompt.md §4 item
    13) — do NOT add one.

G8  THE VERDICT LANDED AND NOTHING ELSE MOVED. `.agent/handoff.md` as committed
    by C3 is a byte-exact PREFIX of the file at HEAD, and the remainder is
    byte-equal to the VERDICT slice. Report the remainder's sha256 and line
    count. Confirm the seven mandated headings of docs/agents/handback_template.md
    are present in order.

G9  ROUND GATE SUITE. `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` in the PRIMARY checkout →
    exit 0, 160 passed. These are the readers of the `.agent/` state files this
    round rewrites.

G10 CANARY. `python3 -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY
    checkout → exit 0, 42 passed. Run it only after G9 has ENDED; state that the
    two runs did not overlap.

G11 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `dea9dc2f..HEAD` BEFORE C3, one line each.
    None may exceed 500. Report C3's own count and C4's in the round report.

G12 HISTORY. Every commit in `dea9dc2f..HEAD` has exactly one parent and the
    chain is linear from `dea9dc2f`. `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, or force-push. Report the chain.

G13 PATH SET. `git diff --name-only dea9dc2f..HEAD`, measured before C3, is
    exactly `.agent/authored/f086-r11.md`, `.agent/last_block.md`,
    `.agent/live_review.md` and `.agent/plan.md`. Report the post-C3 set in the
    round report. Confirm that `pyproject.toml`, `hatch_build.py` and every path
    under `apps/`, `packages/`, `tests/`, `docs/` and `scripts/` are ABSENT, and
    confirm with `git ls-tree dea9dc2f` that all of those EXIST at the base, so
    the clause forbids something real.

G14 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report its output verbatim. Merge
    nothing whatever it says; this round opens and merges no PR.

Handback:
Completion report plus a rewritten `.agent/handoff.md`. Push after C2 and again
after C4. Report every gate above with its REAL exit code and output — "green" as
a word is a finding. If any gate is red, say so plainly with the raw output and
hand off; never repair a red gate by changing what it measures.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN11>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs
to its closure round. `.agent/live_review.md` is the source of truth for the open
set, for the next free finding id and for the round map; this file repeats none
of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R11, this round: close the session. Record the R10 verdict and write the
reviewer's own session verdict to disk, so that no verdict this session issued
exists only in a transcript (finding R-0571). No code, no test, no PR.

## Next Steps
1. R12 — the REVISION embedding T002 still owes. `resolve_build_revision()` in
   `apps/cli/version_report.py` reads a `REVISION` file out of the installed
   distribution's metadata and NOTHING WRITES THAT FILE, so an installed wheel
   reports `dev` exactly as a checkout does. `hatch_build.py` is where it gets
   written, beside the asset guard that already lives there.
2. Then T003 — the release CI stage, the changelog and tag gate, the wheel-size
   budget and the seeded-failure tests.
3. Then the install smoke, the integration gate, and closure. The packaging
   ist-doc is written at closure, when the built state stops moving.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is itself gitignore-matched, so any
  packaging probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
<<<END PLAN11>>>

<<<SLICE RECORD9>>>

Gate: R11 — the R10 entry. R10 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `e7c219cc..dea9dc2f` rather than read from the handback, and every reading reproduces. THE COMMAND EXISTS AND ANSWERS: `python3 -m apps.cli.grouped --version` exits 0 in the primary checkout and prints four lines whose prefixes are `remedy   `, `build    `, `python   ` and `platform `, and the `build` line reads `dev` — which is the reading DECISION F086 D2 requires while nothing writes the REVISION file, and the one reading that proves no revision was invented. THE TESTS ARE NOT VACUOUS: `tests/cli/test_version_report.py` is 8 passed at HEAD, and under the reviewer's own mutations in a worktree OUTSIDE this repository — the two-line `embedded is None or not embedded.strip()` guard deleted, then `    if handle_version_flag(argv):` replaced by `    if False:`, each byte string counted 1x in its named file first — it reads 4 failed / 4 passed and then 2 failed / 6 passed, returning to 8 passed once reverted, with that worktree's `git status --porcelain` empty to prove the restoration rather than assume it. THE WIRING IS REAL, which is what control (ii) measures: unwire the call and the CLI-level tests go red, so the module is not a feature that exists only in its own unit tests. THE ENTRY POINT DID NOT REGRESS: 601 passed across `tests/test_grouped_cli.py`, `tests/cli/test_cli_ux.py` and both command-catalog suites, and `ruff check` over the two new files and `apps/cli/grouped.py` exits 0 — the third of those being the only one that exists at the base, where the reviewer had measured it exit 0 as well, so the gate compared like with like. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r10.md`, the committed `.agent/authored/f086-r10.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 769c36fe3738134b140ecf30bbf7c64e19da39de26a60424e2b9ca43a35a2710, 28100 B, 490 lines; `.agent/plan.md` is byte-equal to its PLAN10 slice at 45 lines; both new files are byte-equal to their slices and both are measured ABSENT at `e7c219cc`; and `apps/cli/grouped.py` at HEAD equals the base blob with its single PAIRFROM occurrence replaced by PAIRTO, by ordered equality rather than by a count no append can meet. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the six written files. THE LEDGER DID NOT MOVE, which is what a round registering nothing must show: paragraph and line-anchored extractions AGREE at `e7c219cc` and at `dea9dc2f`, both reading 163 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 161 open, and the symmetric difference of the two registered sets across the range is EMPTY under both. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout: 160 passed for the four state readers and 42 passed for the canary, each exit 0. THE HYGIENE HELD: eight paths over seven single-parent commits inserting 490, 339, 12, 2, 74, 83 and 70 lines, none over 500 — the block-save commit at 490 being the reason DECISION F085 D6 budgets a block at 490 lines rather than leaving it unbounded. THE ONE DEVIATION WAS DECLARED AND IS NOT A FINDING: `.agent/handoff.md` stands at 113 lines over the 100-line cap, declared under AGENTS.md DECISION D15 with its cause named and every mandated section present.
<<<END RECORD9>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

This section exists because finding R-0571, registered by this feature, is that a
verdict issued and never written to disk cannot be told apart from one never
issued. It is appended rather than written into the sections above so that the
next handback rewrite cannot silently destroy it.

Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md, and the
THIRD session on this branch. The reviewer wrote nothing in the work tree; one
delegated worker per round made every commit; every verdict below rests on gates
the reviewer re-executed itself over the committed diff, never on a handback's
summary.

| Round | Range | Verdict |
|---|---|---|
| R8 | b769ccd7..419fb683 | PASS — one finding, R-0580, against the reviewer |
| R9 | 419fb683..e7c219cc | PASS — no finding |
| R10 | e7c219cc..dea9dc2f | PASS — no finding |

R8 was inherited unreviewed: the previous session ended immediately after issuing
its own verdict, which is exactly the stranding DECISION F085 D9 warns about, so
reviewing it first was Phase 1 rule 4. It passed on every gate, and its one defect
was in the reviewer's own G6, which named a range one commit too wide — three of
that gate's four clauses hold only ACROSS the repair commit, and the worker
recorded both readings and declared the contradiction instead of reconciling it.
That is R-0580, and it is registered against the reviewer, not the worker.

R9 closed T001. `hatch_build.py` now refuses to build a wheel whose
`apps/ui/dist/index.html` is absent, and the reviewer proved both colours itself
from a worktree sited OUTSIDE this repository, because hatchling drops every VCS
exclusion when the build root is gitignore-matched (finding R-0574): with assets
present the build exits 0 and ships a 417-member wheel carrying 3 UI files, and
without them it exits non-zero and produces no wheel at all. The red control is
what makes that worth stating — the same removal at the base exits 0 and ships a
414-member wheel with 0 UI files, so the defect DECISION F086 D1 part (b) names
reproduces at the base and is closed at HEAD.

R10 landed T002's reporting surface. `remedy --version` reads the version back
through package metadata per DECISION F086 D2, so no second literal exists to
drift, and reports `dev` for what a checkout cannot prove rather than inventing
it. Unwiring the call turns the CLI-level tests red, which is how this record
knows the module is wired rather than merely present.

WHAT THIS FEATURE STILL OWES, stated plainly so the next session does not have to
infer it: T002's REVISION embedding. `resolve_build_revision()` reads a `REVISION`
file out of the installed distribution's metadata and nothing writes that file, so
an installed wheel reports `dev` exactly as a checkout does. Then T003 — the
release CI stage, the changelog and tag gate, the wheel-size budget — then the
install smoke, the integration gate and closure. No release may be cut before the
embedding exists, because the release gate compares a tag against a number the
artifact reports.

Every round of this session passed, and the only finding it registered is a defect
in the reviewer's own gate text. By docs/agents/planner_reviewer_prompt.md §4 item
13 the LAST round of a session has no on-disk gate entry, so R11's own verdict is
the terminator and lives in this handoff and in the reviewer's closing report
rather than in the ledger. That absence is the rule, not an omission.
<<<END VERDICT>>>
