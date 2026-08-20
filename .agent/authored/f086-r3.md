── STEP R3 — F086 Release capability (record + packaging inventory) ──

Goal:
Record the R2 verdict in the review ledger, then MEASURE the packaging shape
Remedy actually has today: build a real wheel in a disposable virtualenv and read
what is inside it, rather than inferring it from `pyproject.toml`. The inventory
this produces is what fixes the T001 order; nothing is repaired this round.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r3.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN3 slice, whole file
  C2  append the RECORD slice to `.agent/live_review.md`
  C3  `.agent/f086_inventory.md` — the measured packaging inventory, NEW file
  C4  rewrite `.agent/handoff.md` (the handback)

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger, and the RECORD slice touches it.

Base:
This round starts from `9e855296`, the tip of `feature/f086-release-capability`
and the R2 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN3 and RECORD. PLAN3 is the COMPLETE file including its single
trailing newline; RECORD is an EOF-APPEND into `.agent/live_review.md`, defined
as pure concatenation with its own leading blank line INSIDE the slice, so
nothing is prepended and nothing is stripped. No FROM/TO pair exists in this
block. `.agent/f086_inventory.md` is NOT authored here: it is the round's
MEASUREMENT OUTPUT and you write it from what you actually observe.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `9e855296`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r3.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r3.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r3.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN3 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD slice to `.agent/live_review.md` under the append
   convention. Commit alone. Nothing else in that file changes: the RECORD
   paragraph begins `Gate:` and registers no finding id, so the ledger sets are
   unchanged by this commit and gate G4 requires exactly that.

5. C3 — MEASURE, then write `.agent/f086_inventory.md`. Everything below is a
   reading you take, never a value you carry over from this block. Where a
   command fails, the failure IS the measurement: record the real command, the
   real exit code and the real message, and continue to the next item.

   THE BUILD IS ISOLATED. Create a disposable virtualenv under the gitignored
   `.remedy-wt/` — for example `.remedy-wt/f086r3-venv` — and install the build
   front-end into THAT venv only. Never install into the system interpreter and
   never modify the primary checkout's environment. The reviewer measured at
   `9e855296` that neither `build` nor `hatchling` is importable from the system
   python3, and that `https://pypi.org/simple/hatchling/` answered 200, so the
   install is expected to be reachable; if it is not, record the failure and
   carry on with the static half.

   Build from a PRISTINE tree, not from the working checkout, so that gitignored
   files present on this machine cannot change the answer: `git worktree add` a
   disposable worktree at `9e855296` under `.remedy-wt/`, and build THAT. State
   in the inventory which tree you built and whether `apps/ui/dist` existed in
   it. Remove and prune every worktree and delete the venv before the handback.

   Measure and record, each with the command that produced it:
   a. `python -m build --wheel` (or `pip wheel --no-deps .`) run against the
      pristine worktree: exit code, wall time, and the resulting wheel filename
      and byte size.
   b. The wheel's full member list — `python -c "import zipfile; ..."` — and
      from it: the total member count; how many members are under `apps/`; how
      many under `apps/ui/dist/`; how many under `apps/ui/node_modules/`; how
      many under `packages/`. Report the counts, and list the first ten members
      under `apps/` verbatim.
   c. Whether the wheel contains `apps/ui/dist/index.html`. This is the question
      T001 exists to answer; report it as the literal True or False your run
      produced, and do not soften it either way.
   d. The console entrypoint actually recorded in the wheel: the contents of the
      `entry_points.txt` member, verbatim.
   e. The version string the wheel metadata carries, read from its `METADATA`
      member, and the version literal in `pyproject.toml` at `9e855296`.
   f. Static facts, each with `path:line`: the `[tool.hatch.build.targets.wheel]`
      table in `pyproject.toml`; whether any `artifacts`, `force-include`,
      `exclude` or `include` key exists under `[tool.hatch...]`; the `.gitignore`
      lines that ignore `apps/ui/dist` and `apps/ui/node_modules`; and whether
      `apps/ui/dist` is tracked by git (`git ls-files`).
   g. How the serve command resolves the UI directory: the enclosing symbol and
      the resolution expression in `packages/orchestration/ui_server.py`, and
      the honest "assets not built" message the feature file expects to already
      exist — quote it and give its symbol, or record that you could not find
      one.
   h. Whether `apps/cli` defines a `--version` flag anywhere: the command you
      grepped with and its real result.
   i. Whether the npm spawn that builds the UI goes through the F085
      `exec_guard` seam or a bare subprocess: name the symbol and the call.

   Write the inventory with a `# ` title naming F086, a `## Method` section
   naming every command you ran and the tree each ran in, one `## ` section per
   item a-i above, and a closing `## Open questions for T001` section. State
   readings only. Do NOT propose a design, do NOT edit any file the inventory
   describes, and do NOT register a finding — a defect you notice is written as
   an open question here and the reviewer decides whether it becomes an R-id.

6. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~2 % (F086 beansprucht · R1/R2 gegated · Inventar gemessen · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table with items
   a-i each appearing exactly once, every gate reading below with its real exit
   code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. PLAN3 and RECORD are applied BYTE-VERBATIM. If either cannot be applied
   as-is, stop and declare it — never adjust the bytes to make a gate pass.
3. No production code, no test file, no `docs/` file and no `pyproject.toml`
   change this round. This round MEASURES the packaging shape and changes
   nothing about it. If a measurement seems to require an edit, it does not:
   record the reading and hand back.
4. The build, the venv and every worktree live under the gitignored
   `.remedy-wt/`. Nothing is installed into the system interpreter. Every
   worktree is removed and pruned and the venv deleted before the handback, so
   `git status --porcelain` is EMPTY and `git worktree list` is ONE line.
5. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch, and do not create one.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
7. A failed measurement is a RESULT, not a red gate: record it and continue. A
   red GATE below is different — record the real command, the real exit code and
   the real output, and hand back without repairing the thing it measures.
8. The inventory reports what it observed and never what this block expects. If
   a reading contradicts something stated in this block — including the
   reviewer's own readings quoted in item 5 — the READING wins and the
   contradiction is called out in the inventory in plain words.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed
unless the step names another tree, every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent. Branch is still
    `feature/f086-release-capability`. No venv directory remains under
    `.remedy-wt/`.
G2  TRANSPORT: `.remedy-wt/f086-r3.md`, the committed `.agent/authored/f086-r3.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN3 slice extracted from the
    COMMITTED `.agent/authored/f086-r3.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  LEDGER UNCHANGED BY THIS ROUND. Using a PARAGRAPH extraction — split on runs
    of blank lines into blocks; a finding paragraph is any block whose FIRST
    line matches `^- R-\d+ — `, the whole block and never its first line —
    report at HEAD and at `9e855296`: registered, resolved, `Landed:`,
    duplicate ids, resolutions naming an unregistered id, and the OPEN set.
    REQUIRED as set comparisons, reporting both sides: the registered set, the
    resolved set and the OPEN set are IDENTICAL at the two SHAs. The reviewer
    measured 156 registered, 1 resolved and 155 open at `9e855296`.
G5  CARRY STILL INTACT — the R2 property must not regress. For every id carried
    at the F086 claim, its paragraph at HEAD is byte-equal to its paragraph in
    the blob at `76661dc1`. Report compared and equal; they must agree, and the
    reviewer measured 152 of 152 at `9e855296`. NEGATIVE CONTROL, read-only, no
    checkout: the SAME comparison against the blob at `25f7a5af` MUST report
    strictly fewer equal than compared — the reviewer measured 113 of 152. If
    both halves agree, the check cannot fail; report that and hand back.
G6  The RECORD paragraph is present verbatim at HEAD, begins `Gate:`, and does
    NOT match `^- R-\d+ — `. `.agent/live_review.md` contains `Steps` and `<<<`
    occurs 0x in it.
G7  `.agent/f086_inventory.md` exists at HEAD, is a NEW file in this round, has
    a `## Method` section and an `## Open questions for T001` section, and names
    every one of the items a-i. Report its line count and the section headings
    it actually carries.
G8  `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `9e855296`, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`,
    which spawns `npx vitest run` and cannot resolve `apps/ui/node_modules`,
    absent from every fresh worktree because it is gitignored. That red is the
    known R-0480 mechanism, not a base red.
G9  `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at `9e855296`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no
    path under `docs/` changes.
G10 `git diff --name-only 9e855296..HEAD` lists exactly:
    `.agent/authored/f086-r3.md`, `.agent/f086_inventory.md`,
    `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`. Report the real list and flag any difference rather than
    editing to match. In particular `pyproject.toml` must NOT appear.
G11 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3. None may exceed 500 unless it is the verbatim rewrite of
    a SINGLE `.agent/**` state file, which is exempt under AGENTS.md DECISION
    F104 D1; if you invoke that exemption, name it and the file. C4's own count
    cannot exist while C4 is being written, so report it in your FINAL MESSAGE.
G12 `git log --format=%p 9e855296..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.
G13 No build artefact is committed: `git diff --name-only 9e855296..HEAD`
    contains no path matching `\.whl$`, `\.tar\.gz$`, `dist/`, `build/` or
    `\.egg-info`. Report the check.

The two pytest gates run SERIALLY, never two at once: concurrent pytest
processes here produce false reds through port-bound supervisors (R-0518 class).

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN3>>>
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
R3, this round: record the R2 verdict in the review ledger, then MEASURE the
packaging shape by building a real wheel in a disposable virtualenv from a
pristine worktree and reading what is inside it. Nothing about the packaging is
changed this round; the inventory is what fixes the T001 order.

## Next Steps
1. R4 — rule the packaging shape and the version single-source as a DECISION in
   `.agent/decisions.md`, from what the R3 inventory actually measured rather
   than from the feature file's assumptions, and author the T001 order against
   it. The open question the inventory exists to settle is whether a wheel built
   from a pristine tree carries `apps/ui/dist` at all: that directory is
   gitignored at `.gitignore:13` and untracked, while the wheel target is a bare
   `packages = ["packages", "apps"]` with no artifacts or force-include rule.

## Risks
- If the wheel omits the UI assets, T001 is not a small packaging tweak: it needs
  a build step that produces the assets and a package-data rule that carries
  them, plus the dual-mode resolver, and the feature file's "fail loudly if
  assets are missing" line becomes the acceptance test.
- `apps/ui/node_modules` is 305 MB and sits under a path the wheel target names.
  Whether it reaches the wheel is measured by R3, not assumed, and the answer
  sets the wheel-size budget T003 wants.
- Building a wheel spawns npm. That spawn is what F085's guard bounds, so a
  packaging round that bypasses the seam would silently undo stage-1
  containment.
<<<END PLAN3>>>

<<<SLICE RECORD>>>

Gate: R3 — the R1 and R2 entries. R1 FAILED and R2 PASSED, and both verdicts are recorded here rather than only in a handoff, because finding R-0571 registered this round's own predecessor for exactly that gap. R1 claimed F086, reset this record carrying the F085 open set forward and registered R-0570 and R-0571; its transport, its slice equality, its STATUS pair and its path set were all re-verified by the reviewer and were sound. It FAILED on the carry: of the 152 ids carried, the 113 whose pre-reset paragraph occupies a single physical line survived byte-equal and the 39 that span several were each truncated to their first physical line, destroying 52917 characters of this record. The mismatched set and the multi-line set were the same set. The cause was the reviewer's own R1 wording — "a finding paragraph is a line matching `^- R-\d+ — `" literally defines the paragraph as the line — and the worker applied it literally and reported honestly under it; R-0572 carries that defect and R-0573 carries the reason no gate caught it, R1's G4 having compared both sides with the same broken extractor and so reported 152 of 152 equal over a record in which 39 paragraphs had lost their bodies. R2 repaired it and the reviewer re-took every gate over `25f7a5af..9e855296` with an extraction written independently of the block's, rather than reading the handback. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form, not the digest fallback: the reviewer's scratch original, the committed `.agent/authored/f086-r2.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 87aa80c9cfe85916490ef1e516b960e6a24d4398a182d15b9fb742d9e48f4abf, 24675 B, 319 lines. THE RESTORATION HELD AND ITS CHECK CAN FAIL: all 152 carried paragraphs at `9e855296` are byte-equal to their originals in the blob at `76661dc1`, while the same comparison against `25f7a5af` reports 113 of 152 — the negative control R1's G4 lacked, and the half that makes the required reading mean anything. The carried set's character volume is 263073 at both `76661dc1` and `9e855296`, a difference of 0 against the 52917 lost at `25f7a5af`; all 39 repaired paragraphs span more than one line again; and the count of carried paragraphs closing with `OPEN.` is 86 at both SHAs, that marker being a convention of 86 of the 152 rather than of all of them. THE ARITHMETIC HELD: 154 registered and 0 resolved at `25f7a5af` against 156 and 1 at `9e855296`, the registered difference exactly R-0572 and R-0573, the resolved set exactly R-0572, the open set moving 154 to 155 by exactly R-0573, with 0 duplicate ids, 0 resolutions naming an unregistered id and 0 `Landed:` lines at both. THE REPAIR COMMIT IS PURE: `0ac027da` is +589/-0 over one file, and among its added lines none begins `- R-`, none is a `Done:` line, none carries a slice marker and none is blank — 628 restored paragraph lines replacing the 39 present. R-0570, R-0571 and the file header are byte-unchanged from `25f7a5af`. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout at `9e855296`: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: five paths, all under `.agent/`, over seven single-parent commits inserting 319, 217, 13, 4, 589, 2 and 73 lines, of which only the 589 exceeds no cap it is subject to, being the single-state-file rewrite AGENTS.md DECISION F104 D1 exempts. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the constraint-9 ordering that G5 ran between C3 and C4, and the absence of `.agent/STOP` at the two points the block names; every claim the applied `Done:` text makes about the record is true at `9e855296` independently of when it was written.
<<<END RECORD>>>
