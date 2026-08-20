── STEP R6 — F086 Release capability (T001 part a: the wheel carry, measured) ──

Goal:
Record the R5 verdict, then land the first substance of T001: make the built UI a
declared wheel artifact. DECISION F086 D1 (a) requires the carry mechanism to be
chosen by MEASUREMENT rather than by documentation, so this round BUILDS a wheel
each way, counts what each carries, and applies the one that works. The same
round takes one reading the R3 inventory left as an open question — what
`_get_frontend_dist()` actually returns from an INSTALLED layout — and records it
without acting on it.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r6.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN6 slice, whole file
  C2  append the RECORD4 slice to `.agent/live_review.md`
  C3  write `.agent/f086_r6_inventory.md` — the measurement, worker's own words
  C4  `pyproject.toml` := the FROM/TO pair, using the variant C3 measured to work
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance before
any commit touching the finding ledger, and RECORD4 touches it. C3 precedes C4
because C4's content is CHOSEN by C3's reading; authoring an edit before the
measurement that selects it is the defect D1 (a) exists to prevent.

Base:
This round starts from `91459dc1`, the tip of `feature/f086-release-capability`
and the R5 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN6, RECORD4, PYFROM, PYTO-A and PYTO-B. PLAN6 is the COMPLETE
file including its single trailing newline. RECORD4 is an EOF-APPEND, defined as
pure concatenation with its own leading blank line INSIDE the slice, so nothing
is prepended and nothing is stripped. PYFROM with PYTO-A, and PYFROM with
PYTO-B, are the two candidate FROM/TO pairs for C4; exactly ONE of them is
applied.

Pair shape, measured not asserted (§3 pre-emission items 4 and 15). The
containment test was run mechanically on the final bytes of this block, one
reading per pair, and this is its output:
  PYTO-A contains PYFROM: true   -> APPEND
  PYTO-B contains PYFROM: true   -> APPEND
Both pairs are therefore APPEND-shaped, and G7 orders the §4.9 append obligation
— FROM exactly 1x in the file at `91459dc1`, and each TO-ONLY line exactly 1x
among the lines C4's diff ADDS — and never a "FROM 0x" count, which is
unattainable by construction for a pair whose TO contains its FROM.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `91459dc1`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r6.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r6.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r6.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN6 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD4 slice to `.agent/live_review.md` under the append
   convention. Commit alone. The paragraph begins `Gate:` and registers no
   finding id, so the ledger sets are unchanged by this commit; G4 requires it.

5. C3 — run the measurement described under "The measurement" below and write
   `.agent/f086_r6_inventory.md` in YOUR OWN words. It is a readings file, not an
   authored slice: no wording of it is prescribed here. It states, for every
   command, the command line, the exit code and the literal value produced, and
   where a reading contradicts this block it says so in plain words. Commit
   alone. Nothing else changes in this commit.

6. C4 — apply ONE of the two candidate pairs to `pyproject.toml`, byte-verbatim,
   chosen by C3's reading:
     - variant A carried the assets and variant B did not → apply PYFROM→PYTO-A
     - variant B carried them and variant A did not → apply PYFROM→PYTO-B
     - BOTH carried them → apply PYFROM→PYTO-A, and say in the handback that the
       tie-break was taken because `artifacts` needs no source-to-target path
       mapping, not because B failed
     - NEITHER carried them → make NO edit, commit nothing for C4, write the
       handback and end the round. That is guardrail G8 of
       docs/agents/self_drive_protocol.md, not a failure of this round.
   Commit alone. Name the chosen variant in the commit body.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 91459dc1..<HEAD>`. If the file exceeds its cap, declare
   the overage under AGENTS.md DECISION D15 with its cause and drop no section;
   do NOT write a trim commit afterwards. The `Next` section names, in this
   order, the next session's first two actions: re-read `.agent/STOP` from disk
   (Phase 1 rule 1), then run the Open PR Gate (Phase 1 rule 2).

──────────────────────────────────────────────────────────────

The measurement (C3) — all of it inside disposable scratch under `.remedy-wt/`:

M0. Build toolchain. R3 recorded that neither `build` nor `hatchling` is
    importable from the system python3, that this session may not EXECUTE any
    interpreter under `.remedy-wt/` — which makes a venv unusable — and that a
    `--target` install works. Re-take the first reading yourself rather than
    trusting it (`python3 -c "import build"`, `python3 -c "import hatchling"`,
    both exit codes recorded), then install with
    `python3 -m pip install --no-input --target .remedy-wt/f086r6-pylib build hatchling`
    and confirm AFTERWARDS that `python3 -c "import hatchling"` in the primary
    checkout still fails — the target install must not have entered the system
    interpreter. Report all four readings.

M1. Probe tree. `git worktree add .remedy-wt/f086r6-tree 91459dc1`. Then copy the
    PRIMARY checkout's `apps/ui/dist` directory into it. State plainly in the
    inventory that the assets were COPIED rather than built: the question this
    round asks is whether the backend carries an existing gitignored directory,
    not whether npm can run. Record what `apps/ui/dist` holds in the probe tree
    (file count and whether `index.html` is among them).

M2. RED CONTROL first, before any pyproject edit. Build a wheel from the probe
    tree with its pyproject UNCHANGED:
    `PYTHONPATH=.remedy-wt/f086r6-pylib python3 -m build --wheel --no-isolation --outdir <out> .remedy-wt/f086r6-tree`
    Report the exit code, the wheel's total member count, its byte size, and the
    count of members whose name begins `apps/ui/dist/`. That last number MUST be
    0 — the assets are present on disk in that tree and the backend still omits
    them. If it is not 0, the whole measurement is void because the check cannot
    fail; report that and hand off without editing `pyproject.toml`.

M3. Variant A. Edit ONLY the probe tree's `pyproject.toml` by applying
    PYFROM→PYTO-A there, rebuild into a FRESH outdir, and report the same four
    numbers plus whether `apps/ui/dist/index.html` is literally a member.

M4. Variant B. Restore the probe tree's `pyproject.toml`, apply PYFROM→PYTO-B
    there instead, rebuild into a FRESH outdir, and report the same five values.

M5. Installed-layout reading — a PROBE, with no expected value ordered. Extract
    the wheel from whichever of M3/M4 carried the assets into
    `.remedy-wt/f086r6-site` with `zipfile`, then run, with the working
    directory OUTSIDE the repository so the checkout cannot shadow the
    extraction:
    `python3 -c "import sys; sys.path[:] = ['<abs path to .remedy-wt/f086r6-site>']; import packages.orchestration.ui_server as m; print(m.__file__); print(m._get_frontend_dist())"`
    Report BOTH printed lines literally. The first line PROVES which copy was
    imported: if it does not begin with the extraction directory, the reading is
    void and says so — a probe that loaded the checkout's module measures
    nothing. If the import raises, report the exception type and message and
    move on; a failed probe is a reading too.
    Then run the same two prints from the PRIMARY checkout with the default
    `sys.path` and report those two lines beside them.
    Do NOT change `_get_frontend_dist()` this round whatever it returns, and do
    NOT register a finding about it — the reviewer rules on the reading next
    round. The R3 inventory's open question 4, whether the missing-assets path
    spawns npm from an installed environment, is likewise NOT touched here.

M6. Remove every scratch path before the handback:
    `git worktree remove .remedy-wt/f086r6-tree`, `git worktree prune`, then
    delete `.remedy-wt/f086r6-pylib`, `.remedy-wt/f086r6-site` and the outdirs.
    `git worktree list` must print ONE line at the handback.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If one cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. The only non-`.agent/` path this round may touch is `pyproject.toml`, and only
   in C4. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is
   touched. G12 measures the change set exactly. The probe tree's `pyproject.toml`
   is a scratch file under `.remedy-wt/` and is not part of the change set.
4. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch, and do not create one. Do NOT create a pull request.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, exit code and output, and hand back.
7. Every build, every wheel and every extraction lives under `.remedy-wt/`, which
   is gitignored, so `git status --porcelain` stays EMPTY in the primary checkout
   at every commit and at the handback (self-drive protocol G5).
8. Write no verdict anywhere: a worker-authored verdict is a finding however
   honestly it is hedged (docs/agents/planner_reviewer_prompt.md §4 item 4). The
   inventory reports readings; it does not rule on them.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root unless M5 says otherwise,
with `pwd` confirmed, every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is ONE
    line. `.agent/STOP` absent. Branch still `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r6.md`, the committed `.agent/authored/f086-r6.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN6 slice extracted from the
    COMMITTED `.agent/authored/f086-r6.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  LEDGER UNCHANGED BY THIS ROUND. Using a PARAGRAPH extraction — split on runs
    of blank lines into blocks; a finding paragraph is any block whose FIRST line
    matches `^- R-\d+ — `, the whole block and never its first line — report at
    HEAD and at `91459dc1`: registered, resolved, `Landed:`, duplicate ids,
    resolutions naming an unregistered id, and the OPEN set. REQUIRED as set
    comparisons, reporting both sides: the registered, resolved and OPEN sets are
    IDENTICAL at the two SHAs. The reviewer measured 156 registered, 1 resolved
    and 155 open at `91459dc1`.
G5  CARRY STILL INTACT — the R2 repair must not regress. The carried set is the
    ids present BOTH in the HEAD ledger and in the blob at `76661dc1`; the
    reviewer measured that set as 152 and verified it equals the set of ids
    registered-and-unresolved in that blob. For every such id, its paragraph at
    HEAD is byte-equal to its paragraph in the `76661dc1` blob. Report compared
    and equal; they must agree at 152. NEGATIVE CONTROL, read-only, no checkout:
    the SAME comparison against the blob at `25f7a5af` MUST report strictly fewer
    equal than compared — the reviewer measured 113 of 152. If both halves agree
    the check cannot fail; report that and hand back.
G6  The RECORD4 paragraph is present verbatim at HEAD, begins `Gate:`, and does
    NOT match `^- R-\d+ — `. `.agent/live_review.md` contains `Steps`, and NO
    LINE of it begins `<<<SLICE ` or `<<<END ` — that is, no marker line leaked.
    The count is of marker LINES and not of the substring `<<<`, because prose in
    these files legitimately quotes the marker syntax when describing this very
    gate, and a whole-file substring count is therefore unmeetable by
    construction (§3 pre-emission items 2 and 6). Report the marker-line count.
G7  `pyproject.toml` — only if C4 made an edit. PYFROM occurs exactly 1x in the
    file at `91459dc1`; the applied TO occurs exactly 1x at HEAD; and each line
    that the chosen TO adds and PYFROM does not contain occurs exactly 1x among
    the lines C4's diff ADDS, measured with `git show --numstat` for the total
    plus a per-line count over that diff's added lines. Do NOT count a "FROM 0x":
    both pairs are APPEND-shaped per the containment output above and that count
    is unattainable. Report which variant was applied and why.
G8  THE CARRY IS PROVED, not asserted. At the C4 commit, create a SECOND
    disposable worktree, copy `apps/ui/dist` into it exactly as M1 did, build a
    wheel the same way, and report the count of members whose name begins
    `apps/ui/dist/` together with the total member count and byte size. That
    count must be greater than 0 and `apps/ui/dist/index.html` must be a member.
    M2's reading at the base pyproject, from the same preparation, is the
    negative control for this gate and must be 0; report the two numbers side by
    side. Remove and prune that worktree too. Skip this gate entirely, and say so,
    if C4 made no edit.
G9  Report M5's four printed lines verbatim — the extraction's `__file__` and
    `_get_frontend_dist()`, and the primary checkout's two. No value is ordered:
    this is a reading, and whatever it says is the correct answer to report.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `91459dc1`, and the same command in a fresh worktree
    is red on `TestVitestFrontendTestFoundation::test_vitest_passes`, which spawns
    `npx vitest run` and cannot resolve `apps/ui/node_modules`, absent from every
    fresh worktree because it is gitignored. That red is the known R-0480
    mechanism, not a base red.
G11 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed` at `91459dc1`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no path
    under `docs/` changes.
G12 `git diff --name-only 91459dc1..HEAD` lists exactly `.agent/authored/f086-r6.md`,
    `.agent/f086_r6_inventory.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md` and `pyproject.toml` — the last of
    these only if C4 made an edit. Report the real list and flag any difference
    rather than editing to match. Every path under `packages/`, `apps/`, `tests/`,
    `docs/` and `scripts/` must be ABSENT; all five of those directories exist at
    `91459dc1`, so the clause forbids something real.
G13 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3 and C4. None may exceed 500 unless it is the verbatim rewrite of a
    SINGLE `.agent/**` state file, exempt under AGENTS.md DECISION F104 D1; if you
    invoke that exemption, name it and the file. C5's own count cannot exist while
    its text is being written, so report it in your FINAL MESSAGE.
G14 `git log --format=%p 91459dc1..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:`, `checkout:` and the
    worktree entries M1 and G8 create — no amend, rebase, reset or force-push.
G15 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` is run
    READ-ONLY at the handback and its raw output recorded, to prove this round
    opened no pull request. The reviewer measured `[]` before ordering this block;
    report what you actually see and merge nothing whatever it says.

The two pytest gates run SERIALLY, never two at once: concurrent pytest processes
here produce false reds through port-bound supervisors (R-0518 class). Neither may
run while a wheel build is in flight.

Handback:
Completion report + the handoff written by C5. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN6>>>
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
R6, this round: record the R5 verdict, then land T001 part (a) of DECISION F086
D1 — the explicit wheel carry for `apps/ui/dist` — with the carry mechanism
chosen by building a wheel each way and counting what each one carries. The same
round reads, without acting on it, what `_get_frontend_dist()` returns from an
extracted wheel layout.

## Next Steps
1. R7 — the reviewer rules on R6's installed-layout reading, which bears directly
   on DECISION F086 D1 part (c): the dual-mode resolver is worth building only if
   the current three-parent expression fails from an installed layout. Then T001
   parts (b) and (c) as that ruling leaves them — the packaging-time guard that
   refuses a wheel whose `apps/ui/dist/index.html` is absent, and the
   installed-mode path that never spawns npm.

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
<<<END PLAN6>>>

<<<SLICE RECORD4>>>

Gate: R6 — the R5 entry. R5 PASSED. Every gate its block ordered was re-taken by the reviewer over `655661b0..91459dc1` rather than read from the handback. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original at `.remedy-wt/f086-r5.md`, together with `.agent/authored/f086-r5.md` and `.agent/last_block.md` AS COMMITTED AT `91459dc1`, are byte-EQUAL at sha256 101be7cec956c4fa99009d2c0471c2d1c49e8b4b616fd1b2237d280f6de9e37c, 20909 B, 299 lines, and `.agent/plan.md` at `91459dc1` is byte-equal to its PLAN5 slice at sha256 314b31c39bbf2a11e3a7527b992fe2bb46ae8b0a439733ea0fe575c8fed77923, 44 lines. THE LEDGER WAS UNCHANGED, which is what a record round owes: registered, resolved and OPEN are IDENTICAL sets at `655661b0` and `91459dc1` — 156 registered, 1 resolved, 155 open, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 `Landed:` lines — because the appended paragraph begins `Gate:` and matches no finding pattern. THE VERDICT APPEND WAS AN APPEND, which is the whole point of the round R-0571 asked for: `.agent/handoff.md` as committed by C3 is a byte-exact PREFIX of the file at `91459dc1`, and the remainder is exactly the reviewer's VERDICT slice at sha256 af46e4af4c91c72773285435dc2988bcf0cc7b3f0e870819b4ee849332c5b1a1, 2576 B, 44 lines, so the round that recorded a verdict could not have destroyed one. THE R2 REPAIR HAS NOT REGRESSED and its check still cannot pass vacuously: all 152 carried paragraphs at `91459dc1` are byte-equal to their originals in the blob at `76661dc1`, that carried set was re-derived and again equals the registered-and-unresolved set of that blob, while the same comparison against `25f7a5af` reports 113 of 152. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout at `91459dc1`: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: five paths, all under `.agent/`, over six single-parent commits inserting 299, 189, 22, 2, 49 and 44 lines, none over 500 and no exemption needed; `pyproject.toml` and every path under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` are absent from the range. THE DECLARED D15 OVERAGE WAS TRUE AS WRITTEN: the handback predicted 142 lines for itself after C4 — 98 of its own plus the 44-line slice — and the file at `91459dc1` measures 142, with all seven mandated section headings present and 0 marker lines leaked into either state file. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the points the block names and the serial ordering of the two pytest runs.
<<<END RECORD4>>>

<<<SLICE PYFROM>>>
[tool.hatch.build.targets.wheel]
packages = ["packages", "apps"]
<<<END PYFROM>>>

<<<SLICE PYTO-A>>>
[tool.hatch.build.targets.wheel]
packages = ["packages", "apps"]
# WHY: apps/ui/dist is build output, untracked and matched by the generic `dist/`
# ignore at .gitignore:13, so a VCS-aware backend omits it unless it is named
# here. DECISION F086 D1 (a) — the wheel carries the built UI explicitly.
artifacts = ["apps/ui/dist/**"]
<<<END PYTO-A>>>

<<<SLICE PYTO-B>>>
[tool.hatch.build.targets.wheel]
packages = ["packages", "apps"]
# WHY: apps/ui/dist is build output, untracked and matched by the generic `dist/`
# ignore at .gitignore:13, so a VCS-aware backend omits it unless it is named
# here. DECISION F086 D1 (a) — the wheel carries the built UI explicitly.

[tool.hatch.build.targets.wheel.force-include]
"apps/ui/dist" = "apps/ui/dist"
<<<END PYTO-B>>>
