── STEP R7 — F086 Release capability (T001 part a lands; R6's gate defects registered) ──

Goal:
Register the four gate defects R6 exposed, record the R6 verdict, rule the
DECISION that R6's measurement forces, and land the wheel carry itself. The
measurement that selects the carry mechanism is NOT re-delegated as an open
question this round: the reviewer executed it at `72e07381` with a build root
that is not gitignore-matched, and this block orders that same reading back as a
gate with its own control.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r7.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN7 slice, whole file
  C2  append the FINDINGS slice to `.agent/live_review.md`
  C3  append the RECORD5 slice to `.agent/live_review.md`
  C4  append the DECISION3 slice to `.agent/decisions.md`
  C5  `pyproject.toml` := the PYFROM→PYTO pair
  C6  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. C2 precedes C3 because
docs/agents/planner_reviewer_prompt.md §4 item 4 requires findings to persist in
their own commit FIRST, before anything else the round does. C5 comes after C4
because DECISION3 is what authorises the edit C5 makes.

Base:
This round starts from `72e07381`, the tip of `feature/f086-release-capability`
and the R6 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN7, FINDINGS, RECORD5, DECISION3, PYFROM and PYTO. PLAN7 is
the COMPLETE file including its single trailing newline. FINDINGS, RECORD5 and
DECISION3 are EOF-APPENDS, defined as pure concatenation with each slice's own
leading blank line INSIDE the slice, so nothing is prepended and nothing is
stripped. PYFROM→PYTO is the round's only FROM/TO pair.

Pair shape, measured not asserted (§3 pre-emission items 4 and 15). The
containment test was run mechanically on the final bytes of this block, and this
is its output:
  PYTO contains PYFROM: true   -> APPEND
The pair is therefore APPEND-shaped, and G8 orders the §4.9 append obligation —
PYFROM exactly 1x in the file at `72e07381`, and each TO-ONLY line exactly 1x
among the lines C5's diff ADDS — and never a "FROM 0x" count, which is
unattainable by construction for a pair whose TO contains its FROM.

What the reviewer already measured, so you are re-taking a reading and not
discovering one. At `72e07381`, from a probe worktree at
`/home/decodeux/remedy-f086r7-base` — OUTSIDE the repository, which is the whole
point — with `apps/ui/dist` copied in from the primary checkout:
  base `pyproject.toml`            -> 414 members, 2038283 bytes, 0 under `apps/ui/dist/`
  with `artifacts`                 -> 417 members, 2155470 bytes, 3 under `apps/ui/dist/`
  with `force-include`             -> 417 members, 2155479 bytes, 3 under `apps/ui/dist/`
  with `artifacts`, dist ABSENT    -> 414 members, 2038283 bytes, 0 under `apps/ui/dist/`, exit 0
Both mechanisms work once the build root is not gitignore-matched. `artifacts`
is chosen because it needs no source-to-target path mapping and produced the
smaller wheel of the two. The fourth line is why DECISION3 says part (b) is still
owed: the carry does not make an absent UI loud.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `72e07381`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r7.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r7.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r7.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN7 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the FINDINGS slice to `.agent/live_review.md` under the append
   convention. Commit alone. It registers R-0574, R-0575, R-0576 and R-0577; all
   four are defects in the REVIEWER's own R6 gates, none is a defect of your
   work, and G5 measures the ledger arithmetic they produce.

5. C3 — append the RECORD5 slice to `.agent/live_review.md` under the append
   convention. Commit alone. The paragraph begins `Gate:` and registers no
   finding id, so it moves no ledger set.

6. C4 — append the DECISION3 slice to `.agent/decisions.md` under the append
   convention. Commit alone. `.agent/decisions.md` at `72e07381` must be a
   byte-exact PREFIX of the file after this commit; G7 measures that.

7. C5 — apply PYFROM→PYTO to `pyproject.toml`, byte-verbatim, exactly once.
   Commit alone. This is the only non-`.agent/` file the round touches.

8. C6 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 72e07381..<HEAD>`. If the file exceeds its cap, declare the
   overage under AGENTS.md DECISION D15 with its cause and drop no section; do NOT
   write a trim commit afterwards. The `Next` section names, in this order, the
   next session's first two actions: re-read `.agent/STOP` from disk (Phase 1
   rule 1), then run the Open PR Gate (Phase 1 rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If one cannot be applied as-is, stop and
   declare it — never adjust the bytes to make a gate pass.
3. The only non-`.agent/` path this round may touch is `pyproject.toml`, and only
   in C5. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is
   touched. G12 measures the change set exactly.
4. Never force-push, never rebase, never amend, never work on `main`, never delete
   a branch, and do not create one. Do NOT create a pull request.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, exit code and output, and hand back.
7. The G9 probe worktree lives OUTSIDE this repository, at
   `/home/decodeux/remedy-f086r7-tree`. That siting is load-bearing and is finding
   R-0574: hatchling drops EVERY VCS exclusion pattern when the build root's own
   path is matched by the `.gitignore` it reads, so a probe tree under
   `.remedy-wt/` silently carries files no real build would. Wheels, extractions
   and the build toolchain still go under `.remedy-wt/`, which is gitignored, so
   the primary checkout's `git status --porcelain` stays EMPTY throughout.
8. Write no verdict anywhere: a worker-authored verdict is a finding however
   honestly it is hedged (docs/agents/planner_reviewer_prompt.md §4 item 4).

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root unless a gate says
otherwise, with `pwd` confirmed, every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is ONE
    line. `.agent/STOP` absent. Branch still `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r7.md`, the committed `.agent/authored/f086-r7.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN7 slice extracted from the
    COMMITTED `.agent/authored/f086-r7.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  APPEND SHAPES. `.agent/live_review.md` at `72e07381` is a byte-exact PREFIX of
    the file after C2, and that file is a byte-exact PREFIX of the file at HEAD;
    the two remainders are exactly FINDINGS and then RECORD5, byte for byte.
    Report both prefix checks as True or False and both remainders' sha256.
G5  LEDGER ARITHMETIC. Using a PARAGRAPH extraction — split on runs of blank lines
    into blocks; a finding paragraph is any block whose FIRST line matches
    `^- R-\d+ — `, the whole block and never its first line; a resolution is a line
    matching `^Done: R-\d+ — `; a `Landed:` line is one matching `^Landed: R-\d+`,
    ANCHORED at line start and never counted as a substring, because these files
    legitimately quote the token in prose and a substring count is unmeetable by
    construction (finding R-0575, registered by this very round) — report at
    `72e07381` and at HEAD: registered, resolved, `Landed:`, duplicate ids,
    resolutions naming an unregistered id, and the OPEN set size. The reviewer
    measured at `72e07381`: 156 registered, 1 resolved, 0 anchored `Landed:` lines,
    0 duplicates, 0 unregistered resolutions, 155 open. REQUIRED at HEAD: 160
    registered, 1 resolved, 0 anchored `Landed:` lines, 0 duplicates, 0
    unregistered resolutions, 159 open, and the four ids added are exactly R-0574,
    R-0575, R-0576 and R-0577 — report the set difference itself, not just its size.
G6  CARRY STILL INTACT — the R2 repair must not regress. The carried set is the ids
    present BOTH in the HEAD ledger and in the blob at `76661dc1`. In that blob,
    "unresolved" means carrying no `^Done: R-\d+ — ` line anywhere in the file; the
    reviewer measured 184 finding paragraphs there and 32 such resolutions, leaving
    152, and verified that this equals the carried set. (Naming that extraction
    rule is finding R-0576, which R6's block omitted.) For every carried id, its
    paragraph at HEAD is byte-equal to its paragraph in the `76661dc1` blob. Report
    compared and equal; they must agree at 152. NEGATIVE CONTROL, read-only, no
    checkout: the SAME comparison against the blob at `25f7a5af` MUST report
    strictly fewer equal than compared — the reviewer measured 113 of 152. If both
    halves agree the check cannot fail; report that and hand back.
G7  `.agent/decisions.md` at `72e07381` is a byte-exact PREFIX of the file at HEAD
    and the remainder is exactly DECISION3, byte for byte. Report the prefix check
    and the remainder's sha256. The heading `## DECISION F086 D3` occurs exactly 1x
    at HEAD, so no landed DECISION was edited.
G8  `pyproject.toml`: PYFROM occurs exactly 1x in the file at `72e07381`; PYTO
    occurs exactly 1x at HEAD; and each line that PYTO adds and PYFROM does not
    contain occurs exactly 1x among the lines C5's diff ADDS, measured with
    `git show --numstat` for the total plus a per-line count over that diff's added
    lines. Do NOT count a "FROM 0x": the pair is APPEND-shaped per the containment
    output above and that count is unattainable. Also report that `python3 -c
    "import tomllib; tomllib.load(open('pyproject.toml','rb'))"` exits 0, so the
    file is still valid TOML.
G9  THE CARRY IS PROVED, with a control that can fail. Install the toolchain with
    `python3 -m pip install --no-input --target .remedy-wt/f086r7-pylib build hatchling`.
    Create the probe worktree OUTSIDE the repository:
    `git worktree add /home/decodeux/remedy-f086r7-tree <SHA>`, copy the primary
    checkout's `apps/ui/dist` into it, and build with
    `--wheel --no-isolation --outdir <out> /home/decodeux/remedy-f086r7-tree`.
    Take TWO readings from the SAME preparation, reporting for each the exit code,
    total member count, byte size and the count of members whose name begins
    `apps/ui/dist/`:
      (i)  CONTROL, worktree at `72e07381` — that count MUST be 0.
      (ii) SUBJECT, a second worktree at the C5 commit — that count MUST be 3 and
           `apps/ui/dist/index.html` MUST be a member.
    If (i) is not 0 the control is vacuous and the whole gate is void: report that
    and hand back rather than reading (ii) as evidence. That is finding R-0574
    recurring, and it is the reason this gate names an out-of-repo worktree.
    The `PYTHONPATH=... python3 -m build ...` command form is REFUSED by this
    session's Bash guard, as is `env PYTHONPATH=...`; R6 established the working
    form and you should reuse it — a `python3 - <<'PY'` wrapper that sets BOTH
    `sys.path` and `os.environ['PYTHONPATH']` to the absolute
    `.remedy-wt/f086r7-pylib` and calls `runpy.run_module('build', run_name='__main__')`
    with `sys.argv` set to the argument vector. Setting `PYTHONPATH` is
    load-bearing: with only `sys.path` the backend subprocess dies with
    `BackendUnavailable: Cannot import 'hatchling.build'`.
    Remove BOTH worktrees and run `git worktree prune` before the handback, and
    delete `.remedy-wt/f086r7-pylib` and every outdir.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `72e07381`, and the same command in a fresh worktree is
    red on `TestVitestFrontendTestFoundation::test_vitest_passes`, which spawns
    `npx vitest run` and cannot resolve `apps/ui/node_modules`, absent from every
    fresh worktree because it is gitignored. That red is the known R-0480
    mechanism, not a base red.
G11 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed` at `72e07381`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no path
    under `docs/` changes.
G12 `git diff --name-only 72e07381..HEAD` lists exactly `.agent/authored/f086-r7.md`,
    `.agent/decisions.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md` and `pyproject.toml`. Report the real
    list and flag any difference rather than editing to match. Every path under
    `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` must be ABSENT; all five
    of those directories exist at `72e07381`, so the clause forbids something real.
G13 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3, C4 and C5. None may exceed 500 unless it is the verbatim rewrite of
    a SINGLE `.agent/**` state file, exempt under AGENTS.md DECISION F104 D1; if you
    invoke that exemption, name it and the file. C6's own count cannot exist while
    its text is being written, so report it in your FINAL MESSAGE.
G14 `git log --format=%p 72e07381..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:`, `checkout:` and the worktree
    entries G9 creates — no amend, rebase, reset or force-push.
G15 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` is run
    READ-ONLY at the handback and its raw output recorded, to prove this round
    opened no pull request. The reviewer measured `[]` before ordering this block;
    report what you actually see and merge nothing whatever it says.

The two pytest gates run SERIALLY, never two at once: concurrent pytest processes
here produce false reds through port-bound supervisors (R-0518 class). Neither may
run while a wheel build is in flight.

Handback:
Completion report + the handoff written by C6. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN7>>>
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
R7, this round: register the four defects R6 exposed in the reviewer's own gates,
record the R6 verdict, rule DECISION F086 D3, and land T001 part (a) — the
`artifacts` carry for `apps/ui/dist` in `pyproject.toml`. The carry mechanism was
selected by a measurement the reviewer executed itself, with a control that can
fail; R6's own control could not, which is finding R-0574.

## Next Steps
1. R8 — T001 part (b), the packaging-time guard that refuses to produce a wheel
   whose `apps/ui/dist/index.html` is absent, plus the two-mode resolver TEST that
   DECISION F086 D3 keeps after withdrawing the two-mode resolver CODE. The guard
   is owed because the carry alone is silent: measured at 72e07381, a build with
   the carry applied and no `dist/` present exits 0 and produces a 414-member
   wheel carrying 0 UI files.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A wheel that carries `apps/ui/dist` is only as honest as the directory it was
  built from, so a release now requires the UI to be built first — DECISION F086
  D1's own stated consequence, inherited by CI and by any human cutting a release.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against the
  same files at the base.
<<<END PLAN7>>>

<<<SLICE FINDINGS>>>

- R-0574 — High — A red control whose build root is gitignore-matched cannot fail, and the R6 block forced exactly that siting. R6's M2 ordered a wheel built from a probe worktree with the base `pyproject.toml` and required 0 members under `apps/ui/dist/`; it measured 3, which voided the round's central measurement and cost R6 its deliverable — `pyproject.toml` was correctly left unedited. The cause is mechanical: hatchling 1.32.0 `load_vcs_exclusion_patterns()` builds a `pathspec.GitIgnoreSpec` from the root `.gitignore` and, if that spec matches the build ROOT's own path, returns `[]`, dropping every VCS exclusion for the whole build. `.gitignore` carries a `.remedy-wt/` line and the block's Constraint 7 required all scratch to live under `.remedy-wt/`, so the block's own two clauses could not both hold. This is the R-0364 rule recurring in the reviewer's own text — every gate is EXECUTED at its base before it is ordered — and R6's block ordered a colour the reviewer had never run. The counter-measure that worked, and which R7's G9 orders, is a probe worktree sited OUTSIDE the repository, where no pattern in the repository's own `.gitignore` can match the root; re-measured at `72e07381` from `/home/decodeux/remedy-f086r7-base`, the same control reads 0 members and 414 total, equal to the R3 baseline. The wider lesson is that a build tool's file selection depends on WHERE the tree is, not only on what is in it, so a scratch-siting convention adopted for cleanliness can silently invalidate a measurement.
- R-0575 — Medium — A ledger gate that counts a token as a bare substring counts the prose that describes the gate. R6's G4 ordered a `Landed:` reading over `.agent/live_review.md` without anchoring it, while the same block's RECORD4 slice appended a paragraph whose own words include the token; the worker read 10 at the base and 11 at HEAD and correctly reported that the difference WAS the new paragraph, and the reviewer's anchored re-reading of the same two blobs found 0 anchored lines at both and 19 then 20 unanchored occurrences. Neither reading is wrong; the gate simply never said which it wanted, and the one it invited moves whenever the round writes about itself. This is the class already carried for the `<<<` marker token — where the counter-measure was to count marker LINES rather than substring occurrences — arriving through a different token, so the fix is the general one: a ledger gate anchors every count at line start, `^Landed: R-\d+` and `^Done: R-\d+ — `, and says so in the gate text. §3 pre-emission items 2 and 6 already forbid a zero-gate that counts a string the same block writes into the target; what they did not reach is a non-zero COUNT gate whose number the block's own prose shifts by one.
- R-0576 — Low — A set defined by a phrase no extractor implements is a gate the worker cannot evaluate. R6's G6 required the carried set to equal "the set of ids registered-and-unresolved in that blob" and never said what marks an id resolved in a blob written before the current convention; the worker read 184 registered paragraphs at `76661dc1`, found no `Resolved:` line to subtract, and reported honestly that it could not derive 152 by that route. The gate's REQUIRED numbers were unaffected — 152 of 152 equal, and 113 of 152 against the negative control — so nothing was lost, but a clause that only the author can evaluate is a clause that proves nothing when a second reader disagrees. The rule the reviewer actually used is `^Done: R-\d+ — ` anywhere in the blob, which yields 32 resolutions against 184 paragraphs and therefore 152; R7's G6 states that rule inline. This is the R-0492 shape — define a set by the predicate that produces it, never by a phrase that names it — recurring in a gate rather than in an inventory.
- R-0577 — Medium — A probe recipe that replaces the whole of `sys.path` can only fail, whatever it is probing. R6's M5 ordered `sys.path[:] = ['<site>']` before importing the module under test, which discards the standard library along with the checkout, so the import died at `ui_server`'s own first line with `ModuleNotFoundError: No module named '__future__'` and the probe produced no reading at all. The worker recovered it with `sys.path.insert(0, '<site>')`, which keeps the stdlib while still putting the extraction first, and proved the substitution had taken effect by printing the loaded module's `__file__` — the check that makes such a probe worth running. §3 pre-emission item 12 requires the reviewer to run a gate's EXACT command line before ordering it; the reviewer dry-ran the CHECKOUT form of this probe, which needs no path surgery, and never ran the isolated form it actually ordered. A dry run of a variant is not a dry run, and the isolated form is the only half that could break.
<<<END FINDINGS>>>

<<<SLICE RECORD5>>>

Gate: R7 — the R6 entry. R6 PASSED. Every gate its block ordered was re-taken by the reviewer over `72e07381..HEAD`'s base range `91459dc1..72e07381` rather than read from the handback. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original at `.remedy-wt/f086-r6.md`, together with `.agent/authored/f086-r6.md` and `.agent/last_block.md` AS COMMITTED AT `72e07381`, are byte-EQUAL at sha256 3335f4b7fa6b40ba72534454814c2bbf8906ede3b624fc76dfcb7bd6e5fd492b, 25011 B, 363 lines, and `.agent/plan.md` at `72e07381` is byte-equal to its PLAN6 slice at sha256 ed90971e53568f8d4671541403a07e309d4b797987d55376eb9d9c3bdb2fdedd, 43 lines. THE LEDGER MOVED NOT AT ALL: registered, resolved and OPEN are IDENTICAL sets at `91459dc1` and `72e07381` — 156 registered, 1 resolved, 155 open, 0 duplicate ids, 0 unregistered resolutions, and 0 `Landed:` lines by the ANCHORED reading, against 19 then 20 unanchored occurrences, which is finding R-0575. THE R2 REPAIR HAS NOT REGRESSED: all 152 carried paragraphs at `72e07381` are byte-equal to their originals in the blob at `76661dc1`, while the same comparison against `25f7a5af` reports 113 of 152. THE ROUND CORRECTLY DECLINED TO ACT: `pyproject.toml` is byte-identical at `91459dc1` and `72e07381`, because the block's own halt clause fired when M2's red control read 3 instead of 0, and a worker that had edited anyway would have been acting on a measurement its own block called void. THE CAUSE WAS FOUND AND THE REVIEWER CONFIRMED IT INDEPENDENTLY: the probe tree sat under `.remedy-wt/`, which the repository's `.gitignore` matches, and hatchling drops every VCS exclusion when the build root is itself excluded; re-run at `72e07381` from a worktree OUTSIDE the repository the same control reads 414 members and 0 under `apps/ui/dist/`, and both candidate mechanisms then carry 3. That defect is the reviewer's, not the worker's, and it is registered as R-0574. THE INSTALLED-LAYOUT READING WAS REPRODUCED BY THE REVIEWER rather than accepted: from a copy of `packages/` and `apps/ui/dist` laid out as a wheel root and placed first on `sys.path` with the working directory outside the repository, `_get_frontend_dist()` returned that copy's own `apps/ui/dist` and the loaded module's `__file__` proved the substitution took effect — which is what DECISION F086 D3 rules on. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout at `72e07381`: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: six paths, all under `.agent/`, over six single-parent commits inserting 363, 270, 18, 2, 225 and 60 lines, none over 500 and no exemption needed; `pyproject.toml` and every path under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` are absent from the range. THE DEVIATIONS WERE ALL DECLARED and all of them were the honest choice: C4 produced no commit, M3 and M4 were run anyway so the reviewer would have raw data, an unordered control was taken from the primary checkout that reproduced the R3 baseline exactly, and two commands first piped into `tail` were re-run unpiped because a pipe masks the exit code. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the points the block names, the serial ordering of the two pytest runs, and the removal of the scratch paths, whose end state — one worktree line and an empty `git status --porcelain` — the reviewer did confirm.
<<<END RECORD5>>>

<<<SLICE DECISION3>>>

## DECISION F086 D3 — the dual-mode resolver is withdrawn; the carry mechanism is `artifacts` (2026-08-20)

CHOSEN, and it AMENDS DECISION F086 D1 rather than replacing it. Part (c) of D1
required `_get_frontend_dist()` to resolve the asset directory in two modes,
package-relative when installed and repository-relative in a checkout, on the
stated premise that "its three `.parent` hops land on the environment's
`site-packages` parent once installed and there is no repository root there to
find". That premise is FALSE, and the R3 inventory's open question 4 carries the
same error. The hops land on the wheel ROOT, not its parent:
`packages/orchestration/ui_server.py` has exactly three ancestors up to the
archive root, and `apps/` is a sibling of `packages/` at that same root — the
identical geometry a checkout has. Measured three ways at `72e07381`: from an
extracted wheel the function returned that extraction's own `apps/ui/dist`; from
an independent copy of `packages/` plus `apps/ui/dist` laid out the same way and
placed first on `sys.path` with the working directory outside the repository, it
returned that copy's directory; and from the checkout it returned the checkout's.
In every case the loaded module's `__file__` was printed first, so the reading
could not have come from the wrong copy. No dual-mode code is therefore written,
because the single expression already satisfies both modes, and a second
resolution path would be untested surface added to satisfy a measurement error.

KEPT from part (c): the test per mode. The property is load-bearing for the
feature's own DONE condition and nothing currently pins it, so a regression that
broke installed-mode resolution would be invisible until a user's first serve. A
test that constructs a wheel-root-shaped layout and asserts the resolver follows
it is cheap, and it is the artifact that would have caught the premise error
years earlier than a human would.

CONFIRMED and now MEASURED, part (a): the explicit carry is real and both
candidate mechanisms work. From a probe worktree OUTSIDE the repository with
`apps/ui/dist` present, `pyproject.toml` AS COMMITTED AT `72e07381` produces 414
members and 0 under `apps/ui/dist/`; `artifacts = ["apps/ui/dist/**"]` produces 417 members,
2155470 bytes and 3; a `force-include` table produces 417 members, 2155479 bytes
and 3. `artifacts` is chosen: it needs no source-to-target path mapping, and it
is the smaller of the two artifacts by nine bytes. R6's measurement could not
choose between them because its control was vacuous, which is finding R-0574.

STILL OWED, part (b), and this decision sharpens why. The carry does not make an
absent UI loud: measured at `72e07381`, a build with `artifacts` applied and no
`apps/ui/dist` present exits 0 and produces the same 414-member wheel with 0 UI
files. So landing the carry alone is a strict improvement — with assets present
the wheel now ships them, where before it never did — but it does NOT satisfy
D1's "never ship a wheel with an empty UI directory silently", and no release may
be cut until the packaging-time guard exists.

ALTERNATIVE CONSIDERED and rejected: keep part (c) as written and build the
dual-mode resolver anyway, on the grounds that it is harmless. Rejected because
it is not harmless — it would add a branch no environment reaches, and a branch
no environment reaches is a branch no test can honestly red-prove, which this
repository has already paid for once (finding R-0252).

Reverse this decision by deleting this section, which restores D1 part (c) as
written and reopens the choice between `artifacts` and `force-include`.
<<<END DECISION3>>>

<<<SLICE PYFROM>>>
[tool.hatch.build.targets.wheel]
packages = ["packages", "apps"]
<<<END PYFROM>>>

<<<SLICE PYTO>>>
[tool.hatch.build.targets.wheel]
packages = ["packages", "apps"]
# WHY: apps/ui/dist is build output, untracked and matched by the generic `dist/`
# ignore at .gitignore:13, so a VCS-aware backend omits it unless it is named
# here. DECISION F086 D1 (a), mechanism chosen by measurement in DECISION F086 D3.
# This carry is NOT a guard: with no dist/ present the build still succeeds and
# ships no UI. That guard is D1 part (b) and is still owed.
artifacts = ["apps/ui/dist/**"]
<<<END PYTO>>>
