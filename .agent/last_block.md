── STEP R4 — F086 Release capability (record + the packaging DECISIONs) ──

Goal:
Record the R3 verdict in the review ledger, then rule — from what R3 MEASURED
and not from the feature file's assumptions — how the wheel comes to carry the
UI it serves, and where a single version string lives. Two DECISIONs, no code:
this round fixes the T001 and T002 orders without writing either.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r4.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN4 slice, whole file
  C2  append the RECORD2 slice to `.agent/live_review.md`
  C3  append the DECISION1 slice, then the DECISION2 slice, to
      `.agent/decisions.md`
  C4  rewrite `.agent/handoff.md` (the handback)

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger, and RECORD2 touches it.

Base:
This round starts from `0cabd17e`, the tip of `feature/f086-release-capability`
and the R3 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN4, RECORD2, DECISION1 and DECISION2. PLAN4 is the COMPLETE
file including its single trailing newline. RECORD2, DECISION1 and DECISION2 are
EOF-APPENDS, defined as pure concatenation with each slice's own leading blank
line INSIDE the slice, so nothing is prepended and nothing is stripped. No
FROM/TO pair exists in this block.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `0cabd17e`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r4.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r4.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r4.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN4 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD2 slice to `.agent/live_review.md` under the append
   convention. Commit alone. The paragraph begins `Gate:` and registers no
   finding id, so the ledger sets are unchanged by this commit; G4 requires it.

5. C3 — append DECISION1, then DECISION2, to `.agent/decisions.md`, in that
   order, under the append convention. Commit alone. Nothing else in that file
   changes: this is an append to the end, never an edit of a landed DECISION.

6. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~3 % (F086 beansprucht · R1-R3 gegated · Paketform entschieden · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table, every
   gate reading below with its real exit code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If one cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. This round writes NO code and NO test. `pyproject.toml`,
   `packages/orchestration/ui_server.py`, `apps/**` and `tests/**` are NOT
   touched. The DECISIONs RULE what T001 and T002 will do; they do not do it. If
   applying a slice seems to require a code change, it does not — stop and
   declare.
4. No `docs/` file changes: no path under `docs/` is in this round's change set.
5. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch, and do not create one.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, exit code and output, and hand back.
8. A landed DECISION is never edited. DECISION1 and DECISION2 are appended after
   the last existing section of `.agent/decisions.md`; no existing byte of that
   file changes, and G7 measures exactly that.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent. Branch still
    `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r4.md`, the committed `.agent/authored/f086-r4.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN4 slice extracted from the
    COMMITTED `.agent/authored/f086-r4.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  LEDGER UNCHANGED BY THIS ROUND. Using a PARAGRAPH extraction — split on runs
    of blank lines into blocks; a finding paragraph is any block whose FIRST
    line matches `^- R-\d+ — `, the whole block and never its first line —
    report at HEAD and at `0cabd17e`: registered, resolved, `Landed:`, duplicate
    ids, resolutions naming an unregistered id, and the OPEN set. REQUIRED as
    set comparisons, reporting both sides: the registered, resolved and OPEN
    sets are IDENTICAL at the two SHAs. The reviewer measured 156 registered, 1
    resolved and 155 open at `0cabd17e`.
G5  CARRY STILL INTACT — the R2 property must not regress. For every id carried
    at the F086 claim, its paragraph at HEAD is byte-equal to its paragraph in
    the blob at `76661dc1`. Report compared and equal; they must agree, and the
    reviewer measured 152 of 152 at `0cabd17e`. NEGATIVE CONTROL, read-only, no
    checkout: the SAME comparison against the blob at `25f7a5af` MUST report
    strictly fewer equal than compared — the reviewer measured 113 of 152. If
    both halves agree the check cannot fail; report that and hand back.
G6  The RECORD2 paragraph is present verbatim at HEAD, begins `Gate:`, and does
    NOT match `^- R-\d+ — `. `.agent/live_review.md` contains `Steps` and `<<<`
    occurs 0x in it.
G7  `.agent/decisions.md` at HEAD: the file's content at `0cabd17e` is a
    byte-exact PREFIX of the file at HEAD, and the appended remainder is exactly
    DECISION1 followed by DECISION2, byte for byte. Report the prefix check as
    True or False and report both slice digests. Report also that `## DECISION
    F086 D1` occurs exactly 1x and `## DECISION F086 D2` exactly 1x in the file,
    and that `<<<` occurs 0x.
G8  `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `0cabd17e`, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`,
    which spawns `npx vitest run` and cannot resolve `apps/ui/node_modules`,
    absent from every fresh worktree because it is gitignored. That red is the
    known R-0480 mechanism, not a base red.
G9  `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at `0cabd17e`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no
    path under `docs/` changes.
G10 `git diff --name-only 0cabd17e..HEAD` lists exactly:
    `.agent/authored/f086-r4.md`, `.agent/decisions.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`.
    Report the real list and flag any difference rather than editing to match.
    In particular `pyproject.toml`, `packages/orchestration/ui_server.py` and
    any path under `tests/` or `docs/` must be ABSENT.
G11 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3. None may exceed 500 unless it is the verbatim rewrite of
    a SINGLE `.agent/**` state file, exempt under AGENTS.md DECISION F104 D1; if
    you invoke that exemption, name it and the file. C4's own count cannot exist
    while C4 is being written, so report it in your FINAL MESSAGE.
G12 `git log --format=%p 0cabd17e..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.

The two pytest gates run SERIALLY, never two at once: concurrent pytest
processes here produce false reds through port-bound supervisors (R-0518 class).

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN4>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1, the merge
commit of PR #206. `.agent/live_review.md` is the source of truth for the open
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
R4, this round: record the R3 verdict, and rule as DECISIONs how the wheel comes
to carry the UI it serves and where the single version string lives — both from
what R3 measured rather than from the feature file's assumptions. No code and no
test this round.

## Next Steps
1. R5 — T001 begins: the packaging change DECISION F086 D1 rules, in its own
   commits — the wheel-side asset carry, the packaging-time guard that refuses
   to build a wheel with no UI, and the dual-mode resolver in
   `_get_frontend_dist()` with a test for each mode. The measured baseline it
   must move is a wheel of 414 members and 2038283 bytes carrying 0 members
   under `apps/ui/dist/`.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the
  wheel's console script. R3 measured that THIS session's permission layer
  refuses to execute any interpreter under `.remedy-wt/`, so the smoke cannot
  be proved green from a session with that posture; the round that writes it
  must name its execution host or it will be unverifiable where it matters.
- `_load_frontend()` reacts to a missing `dist/` by spawning npm, and
  `apps/ui/package.json` ships in the wheel, so an installed environment can
  reach the npm path with no `node_modules` present. DECISION F086 D1 rules
  that path off in installed mode; a T001 that carries assets but leaves the
  spawn reachable has fixed only half of it.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against
  the same files at the base.
<<<END PLAN4>>>

<<<SLICE RECORD2>>>

Gate: R4 — the R3 entry. R3 PASSED. Every gate its block ordered was re-taken by the reviewer over `9e855296..0cabd17e` rather than read from the handback, and the round's central measurement was corroborated from git independently of the build the worker ran. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original, the committed `.agent/authored/f086-r3.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 f659fccc1911c491903c2eea2986a9a427da6d7d6163db558b0ec9a65d976c88, 20622 B, 277 lines, and `.agent/plan.md` is byte-equal to its PLAN3 slice at 41 lines. THE LEDGER WAS UNCHANGED, which is what a record round owes: registered, resolved and OPEN are IDENTICAL sets at `9e855296` and `0cabd17e` — 156 registered, 1 resolved, 155 open, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 `Landed:` lines — because the appended paragraph begins `Gate:` and matches no finding pattern. THE R2 REPAIR HAS NOT REGRESSED, and its check still cannot pass vacuously: all 152 carried paragraphs at `0cabd17e` are byte-equal to their originals in the blob at `76661dc1`, while the same comparison against `25f7a5af` reports 113 of 152. THE INVENTORY IS A MEASUREMENT AND NOT A CONCLUSION: `.agent/f086_inventory.md` is 290 lines carrying `## Method`, one section per ordered item a through i, and `## Open questions for T001`, and it registers no finding, proposes no design and edits nothing it describes. ITS HEADLINE WAS CORROBORATED WITHOUT REBUILDING: at `9e855296` git tracks 149 files under `apps/` and 261 under `packages/`, so the reported 414 wheel members are exactly those 410 plus 4 dist-info members; git tracks 0 files under `apps/ui/dist` and 0 under `apps/ui/node_modules`, so a wheel built from a pristine tree carries neither, which is the reported `apps/ui/dist/index.html -> False`; and `apps/ui/package-lock.json` is 182948 bytes at that SHA, the figure the inventory reports. THE ISOLATION HELD AND WAS RE-MEASURED RATHER THAN ASSUMED: no `.remedy-wt/f086r3*` path survives, `git worktree list` is one line, and `import hatchling` still fails in the primary checkout's interpreter, so the `--target` install the worker deviated to never entered the system environment. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout at `0cabd17e`: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: six paths, all under `.agent/`, over six single-parent commits inserting 277, 202, 21, 2, 290 and 89 lines, none over 500 and no exemption needed; no path in the range matches `\.whl$`, `\.tar\.gz$`, `dist/`, `build/` or `\.egg-info`. TWO DEVIATIONS WERE DECLARED AND BOTH ARE ACCEPTED. The ordered venv route could not run: the index was reachable — the reviewer measured `https://pypi.org/simple/hatchling/` at 200 before ordering it — and what refused was this session's permission layer, which declines to execute ANY interpreter under `.remedy-wt/`, including `python -V`. The worker rerouted through `pip install --target` with `--no-isolation`, then re-measured the isolation property instead of asserting it. That is the block's constraint 8 working as intended: the reviewer's reading about WHICH layer would bite was wrong, the worker's reading overrode it, and the contradiction was reported rather than smoothed over. The second deviation is a 126-line handback against the 100-line cap, declared in the file under AGENTS.md DECISION D15 with its mandated cause and no section dropped. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the two points the block names and the serial ordering of the two pytest runs.
<<<END RECORD2>>>

<<<SLICE DECISION1>>>

## DECISION F086 D1 — the wheel carries the built UI explicitly, and installed mode never builds it (2026-08-20)

CHOSEN. T001 makes the built UI a declared wheel artifact rather than a file that
happens to be lying around. Three parts, and the first is useless without the other
two. (a) `pyproject.toml` gains an explicit carry for `apps/ui/dist` under
`[tool.hatch.build.targets.wheel]` — `artifacts` or `force-include`, whichever the
installed hatchling honours, chosen by MEASUREMENT and not by documentation — because
that directory is untracked and matched by the generic `dist/` ignore at
`.gitignore:13`, and a build backend that respects VCS ignores will otherwise omit it
however carefully it was built first. (b) A packaging-time guard REFUSES to produce a
wheel whose `apps/ui/dist/index.html` is absent, so the failure is loud at build time
instead of silent at serve time; the feature file's "never ship a wheel with an empty
UI directory silently" is this clause. (c) `_get_frontend_dist()` in
`packages/orchestration/ui_server.py` resolves the asset directory in BOTH modes —
package-relative when installed, repository-relative in a checkout — with a test per
mode, because its three `.parent` hops land on the environment's `site-packages`
parent once installed and there is no repository root there to find.

Additionally, and rules the hazard R3's inventory surfaced as its open question 4:
in INSTALLED mode the missing-assets path does NOT spawn npm. `_load_frontend()`
today answers a missing `dist/` by running `npm install` and `npm run build`, and
`apps/ui/package.json` IS a wheel member, so that path is reachable from a user's
environment where no `node_modules` exists and no toolchain is promised. Installed
mode degrades to the honest "UI assets not built" message the feature file expects to
already exist; auto-build stays a CHECKOUT-mode convenience. The mode test is the same
one part (c) introduces, so this costs no second mechanism.

ALTERNATIVE CONSIDERED and rejected: ship the UI SOURCE and build on first serve,
which is close to today's accidental behaviour — the wheel already carries 65 files
under `apps/ui/src/` and a 182948-byte `package-lock.json` but no build output. It is
rejected because it makes every installed user's first serve depend on a network, a
node toolchain and an npm lockfile resolution, turning a packaging problem into a
runtime one, and because it cannot satisfy the feature's own DONE condition that the
UI serve work in a fresh virtualenv. Whether the wheel should keep shipping that
source at all is left to T003's wheel-size budget and is NOT ruled here.

CONSEQUENCE. The wheel stops being buildable from a bare `git worktree`: producing a
releasable artifact now requires the UI to be built first, which is a real constraint
on CI and on any human cutting a release, and it is deliberate — it is the only way the
guard in (b) can be honest. The measured baseline T001 must move is a wheel of 414
members and 2038283 bytes carrying 0 members under `apps/ui/dist/`.

Reverse this decision by deleting this section and the explicit carry it rules, which
returns the wheel to whatever the backend's default file selection produces — today,
a wheel with no UI.
<<<END DECISION1>>>

<<<SLICE DECISION2>>>

## DECISION F086 D2 — one version literal, read through package metadata, honest in a checkout (2026-08-20)

CHOSEN. T002 keeps `pyproject.toml` as the single place a version NUMBER is written —
it is `version = "0.1.0"` at `pyproject.toml:7` today, and R3 measured the wheel's
METADATA agreeing with it — and `remedy --version` reads it back through
`importlib.metadata.version("remedy")` rather than through a second literal in Python
source. No `__version__` constant is introduced to be kept in sync, because a second
literal is the defect this decision exists to prevent. There is no `--version` flag
under `apps/` today; T002 adds one, and it prints the version, the git sha embedded at
build time, the Python version and the platform, as the feature file's Design asks.

In a CHECKOUT the distribution is frequently not installed and the embedded sha does
not exist, so the command reports the version it can prove and says `dev` for the build
info rather than inventing a sha or crashing. That is the feature file's "checkout mode
reports dev honestly" and it is a REQUIREMENT, not a fallback: a version command that
reports a stale or fabricated sha is worse than one that admits it is a working tree.

ALTERNATIVE CONSIDERED and rejected: generate a `_version.py` at build time as the
single source. It reads more simply at the call site, but it puts a generated file on
the import path where a stale copy in a checkout outranks the metadata and reports a
version nobody built — the precise failure mode the honest-`dev` clause exists to
avoid.

CONSEQUENCE. `remedy --version` is only fully truthful for an INSTALLED distribution,
which is the mode the release gate cares about, and the checkout mode is deliberately
less informative rather than differently informative. The release gate T003 builds can
then compare a tag against exactly one number, read from the artifact it is about to
publish.

Reverse this decision by deleting this section, which returns the version story to a
single literal with no reader and no `--version` flag.
<<<END DECISION2>>>
