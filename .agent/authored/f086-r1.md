── STEP R1 — F086 Release capability ─────────────────────────

Goal:
Claim F086 in the ledger, reset the live-review record while carrying the F085
open set forward, and register the two closure candidates the reviewer's R74
closure review of F085 produced. No production code, no packaging change, no
inventory yet — R2 is the packaging-shape inventory.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r1.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN slice, whole file
  C2  reset `.agent/live_review.md`: authored header + Steps + Findings, then
      R-0570, then R-0571, then the F085 open set carried forward verbatim
  C3  claim: `docs/roadmap/STATUS.md` pair + `.agent/context.md` +
      `.agent/candidates.md`, whole-file for the two `.agent` files
  C4  rewrite `.agent/handoff.md` (the handback)

C1 writes `.agent/plan.md` before any commit that touches the finding ledger,
which is what docs/agents/planner_reviewer_prompt.md §3 pre-emission item 23
requires of a round that registers a finding: only the two block-save commits
may precede the plan update.

Base:
This round starts from `76661dc1`, the tip of `main` and the merge commit of
PR #206, which the OPERATOR merged manually at 2026-08-20T07:34:53Z. Every range
gate below names that SHA. The branch is `feature/f086-release-capability`, cut
from `main` at that commit.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are LIVEREVIEW-HEADER, R0570, R0571, STATUSLINE-FROM, STATUSLINE-TO,
CONTEXT, PLAN and CANDIDATES. Every slice's bytes end with a single trailing
newline, and every whole-file slice is the COMPLETE file including that newline.

Pair shape, tested mechanically at emission rather than by eye:
STATUSLINE-FROM → STATUSLINE-TO reads `TO contains FROM: false`, so it is a
REWRITE and the proof is FROM 0x and TO 1x over the whole file after the edit.
It is the only FROM/TO pair in this block; every other slice is a whole-file
replacement or an append into a file this round rebuilds.

──────────────────────────────────────────────────────────────

Change:

0. Open PR Gate, before any branch is created. Run
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   record the raw output in the handback. The reviewer measured `[]` at
   authoring time, after PR #206 was merged by the operator; if it is still `[]`
   nothing is merged and you continue. If it is NOT `[]`, stop and hand off — do
   not merge and do not create the branch. Then confirm `git rev-parse HEAD`
   equals `76661dc1`, and `git checkout -b feature/f086-release-capability`.
   Do NOT delete the local `feature/f085-closeout-state` branch if it still
   exists; it is merged and left alone (self-drive protocol G2).

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r1.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r1.md`; copy that file rather than retyping it (`cp` may be
   denied — `shutil.copyfile` is an acceptable substitute; the gate names the
   byte property, not the tool). Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r1.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN slice, byte-verbatim, whole file. Commit
   alone. This is the round's first substantive commit.

4. C2 — rebuild `.agent/live_review.md` in this exact order, then commit:
   a. the LIVEREVIEW-HEADER slice, byte-verbatim;
   b. the R0570 slice, byte-verbatim;
   c. the R0571 slice, byte-verbatim;
   d. the F085 open set, carried forward VERBATIM and never retyped. Extract it
      programmatically from the PRE-RESET file — the blob at `76661dc1` —
      like this: a finding paragraph is a line matching `^- R-\d+ — `; a
      resolution is a line matching `^Done: R-\d+ — `; the open set is every
      finding paragraph whose id has no resolution line anywhere in that file.
      Append those paragraphs in the order they appear in the pre-reset file,
      each separated from the next by exactly one blank line, each byte-equal to
      its pre-reset original. The reviewer measured the pre-reset file at
      `76661dc1` as 184 registered ids, 32 resolved, 0 `Landed:` lines, 0
      duplicate ids and 0 resolutions naming an unregistered id, so the carried
      set is 152 paragraphs.

5. C3 — the claim, one commit, three files:
   a. `docs/roadmap/STATUS.md`: replace the single line STATUSLINE-FROM with
      STATUSLINE-TO.
   b. `.agent/context.md`: whole file := the CONTEXT slice.
   c. `.agent/candidates.md`: whole file := the CANDIDATES slice.
   README.md is NOT touched. Its line 19 already reads
   `51 of 255 registered items accepted. Next: F086 (Release capability).`, and
   the reviewer measured the ledger's accepted count as 51 at `76661dc1`, so both
   halves of that sentence are already correct and only move at closure. That the
   Tier 2 LIST beneath it is incomplete is registered as R-0570 and is NOT
   repaired here.

6. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~1 % (F086 beansprucht · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table, every
   gate reading below with its real exit code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. No production code, no test file, and no `docs/` file other than
   `docs/roadmap/STATUS.md` is touched this round. If the work seems to require
   one, stop and hand off.
4. Destructive or red-proof verification runs only inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout, which
   satisfies `git status --porcelain` == empty at the handback.
5. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch. Do not create the PR this round — the branch is pushed and
   the PR is created at closure.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.
8. The two registered findings are recorded, NOT fixed. R-0570 edits `README.md`
   and a test in `tests/docs/test_docs_consistency.py`; R-0571 edits
   `docs/agents/planner_reviewer_prompt.md` or the integrity gate. Both are
   outside F086's ownership and both route to a paydown branch. Touching either
   this round is a scope violation.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent.
G2  TRANSPORT: `.remedy-wt/f086-r1.md`, the committed `.agent/authored/f086-r1.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/live_review.md` at HEAD: recompute the sets with the same two
    regexes named in C2. Report registered, resolved, `Landed:`, duplicate ids
    and resolutions naming an unregistered id. REQUIRED: the set of OPEN ids at
    HEAD equals the set of OPEN ids in the blob at `76661dc1` PLUS exactly
    `R-0570` and `R-0571`, as a set comparison — report the two counts rather
    than predicting them, and report the max id and the next free id.
G4  Every carried paragraph is byte-equal to its pre-reset original: for each
    carried id, compare the paragraph at HEAD against the paragraph extracted
    from the blob at `76661dc1`. Report the number compared and the number
    equal; those two numbers must agree.
G5  `.agent/live_review.md` contains the substring `Steps`.
G6  `docs/roadmap/STATUS.md` at HEAD: STATUSLINE-FROM occurs 0x, STATUSLINE-TO
    occurs 1x, `^- \[~\]` occurs exactly 1x, `^- \[x\] F\d{3} — ` still occurs
    51x, and `<<` occurs 0x. The reviewer measured FROM 1x, TO 0x, `[~]` 0x and
    `[x] F` 51x at `76661dc1`.
G7  `.agent/context.md` at HEAD contains `## Active Branch`, the substring
    `feature/`, the substring `Steps`, a match of `\bF\d{3}\b`, and `resource`
    or `pytest` case-insensitively.
G8  `.agent/plan.md` at HEAD contains `## Goal`, `## Next Steps` and a match of
    `\bF\d{3}\b`, and is under 50 lines. Report the line count.
G9  Each of `.agent/context.md`, `.agent/plan.md`, `.agent/candidates.md` is
    byte-equal to its slice as extracted from the COMMITTED
    `.agent/authored/f086-r1.md`, not from any retype. Report each file's
    sha256 and line count.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. These four files are the readers of the state files this round
    rewrites. Report the passed count and the exit code. RUN THIS IN THE PRIMARY
    CHECKOUT, not in a worktree: the reviewer measured `160 passed`, exit 0, in
    the primary checkout at the base tree, and the SAME command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`,
    which spawns `npx vitest run` and cannot resolve `apps/ui/node_modules`
    because that path is gitignored and therefore absent from every fresh
    worktree by construction. That red is the known R-0480 mechanism and not a
    base red.
G11 `python3 -m pytest tests/docs/ -q` → exit 0. The reviewer measured
    `295 passed` at the base tree. This round changes `docs/roadmap/**`, which is
    what makes this gate mandatory.
G12 `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → exit 0.
    The reviewer measured `30 passed` at the base tree. This is the half that
    actually parses the STATUS grammar C3 edits; `tests/docs/` does not.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at the base tree.
G14 `git diff --name-only 76661dc1..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f086-r1.md`, `.agent/candidates.md`,
    `.agent/context.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`.
    Report the real list and flag any difference rather than editing to match.
G15 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3 only. None may exceed 500, except that C2 is the verbatim
    rewrite of a SINGLE `.agent/**` state file and is exempt by AGENTS.md
    DECISION F104 D1; report its number anyway. C4's own insertion count cannot
    exist while C4's text is being written, so it is reported in your FINAL
    MESSAGE — the round report, written after C4 exists — and not in this file.
G16 `git log --format=%p 76661dc1..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.

The four pytest gates run SERIALLY, never two at once: concurrent pytest
processes in this repository produce false reds through port-bound supervisors
(finding R-0518 class), and a false red costs the round.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push the branch with
`git push -u origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE LIVEREVIEW-HEADER>>>
# Live Review — F086 Release capability

> Round-by-round review record for the F086 branch, reset at the feature claim.
> The F085 record closed with PR #204, merged 2026-08-20, and two state-only
> pull requests followed it on `main`: the operator amendment PR #205 and the
> state refresh PR #206. That branch's closing verdict lives in its handoff and
> in the PR, per docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids
> continue the monotonic R-XXXX series across the reset.
> Next free id: R-0572.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when
> the F085 record closed are reproduced verbatim at the end of this file,
> extracted by id out of the previous record and never retyped. The pre-reset
> record held no `Landed:` line.

## Steps
R1 claim F086, reset this record carrying the F085 open set forward, and
register the two closure candidates out of the reviewer's R74 closure review of
F085 → R2 the packaging-shape inventory: what `pyproject.toml` declares, what a
built wheel actually carries, how the served UI asset directory is resolved
today, and where a version string would have to come from — each MEASURED from a
real build rather than read off the metadata → R3 record R2 and rule the
packaging shape and the version single-source as a DECISION → R4 T001 package
data plus the dual-mode asset resolver, checkout and installed wheel, with a
test for each mode → R5 T001 the fresh-venv install smoke as a subprocess marker
→ R6 record R4 and R5 → R7 onward T002 the version single-source and the build
info behind `remedy --version`, with a checkout mode that reports "dev" honestly
→ then T003 the release CI stage, the changelog and tag gate, the wheel-size
budget and the seeded-failure tests → then the integration gate → then closure.
The map from R4 on is planned rather than measured: the inventory R2 produces is
what fixes it, and a round that changes this map records the change as a
DECISION in this file. Each round marks the PREVIOUS one done and never itself;
the FULL map is stated here ONLY. Another file may name at most the NEXT round —
`.agent/plan.md` must, because AGENTS.md mandates its Next Steps section — and
naming one round is not restating the map (R-0447, R-0455).

## Findings
<<<END LIVEREVIEW-HEADER>>>

<<<SLICE R0570>>>
- R-0570 — Low, THE ROOT README'S ACCEPTED-FEATURE LIST IS PINNED IN ONE DIRECTION ONLY, SO AN INCOMPLETE LIST PASSES EVERY TEST THAT READS IT. Raised by the reviewer's closure review of F085 R74, carried in `.agent/candidates.md` as a closure candidate per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings", and registered here because this is F086's first reviewed round. Measured by the reviewer at 76661dc1: `README.md` line 58 opens "Accepted in Tier 2 so far:" and the list beneath it names F254, F103, F104, F105 and F107 — five ids — while the Tier 2 block of `docs/roadmap/STATUS.md` carries thirteen lines matching `^- \[x\] F\d{3} — `, namely F103, F104, F105, F107, F111, F115, F045, F057, F077, F082, F083, F085 and F254. Eight accepted features are therefore absent from the list that claims to enumerate them, and the README already contradicts itself on the same page: its tier table at line 25 reads `| 2 | Minimal Self-Build Runtime | 13 | 14 |`. The reason nothing catches it is structural rather than accidental. `test_the_readme_reports_the_accepted_foundation_and_no_later_feature` in `tests/docs/test_docs_consistency.py` iterates the ids the README LISTS and asserts each one is accepted in the ledger; that is the list→ledger direction only, so removing an id from the list, or never adding it, can never fail that test. Its two neighbours are pinned in the other direction and are both green for exactly that reason: `test_the_readme_accepted_count_equals_the_status_count` compares the prose "51 of 255 registered items accepted" against the ledger's `[x]` count, which the reviewer measured as 51 at the same commit, and `test_the_readme_tier_table_done_column_matches_the_ledger` pins the Done column, which is why the TABLE says thirteen while the PROSE LIST says five. Low, because nothing false is asserted anywhere — every count that is pinned is correct, and no unaccepted feature is claimed as accepted — and the whole cost is that a reader of the list under-counts Tier 2 by eight. This is not F085's defect: the same list was already incomplete when F082 and F083 closed, neither of which added itself, which is precisely why it needed a carrier rather than a repair inside that feature. The fix edits `README.md` and one test in `tests/docs/test_docs_consistency.py`, neither of which F086 owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.
<<<END R0570>>>

<<<SLICE R0571>>>
- R-0571 — Medium, A LAST ROUND WHOSE VERDICT WAS WRITTEN AND ONE WHOSE VERDICT WAS NEVER WRITTEN ARE INDISTINGUISHABLE ON DISK. Raised by the reviewer's gate of F085 R74, carried in `.agent/candidates.md` as a closure candidate, and registered here because this is F086's first reviewed round. A branch's LAST round has no on-disk gate entry by construction: docs/agents/planner_reviewer_prompt.md §4 item 13 states that every reviewed round records its verdict in `.agent/live_review.md`, that the round writing that record cannot record the gate on itself, and that every branch therefore ends with one round whose verdict lives only in `.agent/handoff.md`, the completion report and the PR. Both states consequently present the identical disk signature — a handback with no `Gate:` paragraph naming that round, and no verdict anywhere in the record — so on disk a terminated round and an abandoned one cannot be told apart. The F085 session reported finding exactly that state at e950e8af: R74's handback present, `.agent/live_review.md` correctly silent about R74, no verdict in `.agent/handoff.md`, and no comment on PR #204 when its gate began; it had to re-run the entire round gate to establish which of the two states it was looking at, because nothing cheaper distinguishes them. Item 13 does tell the reviewer to write the closing verdict into the handoff and the PR, but nothing on disk goes red when that write does not happen, and the preconditions of docs/roadmap/STATUS_closure_protocol.md do not check for it either, so the omission is silent at exactly the moment the record becomes permanent. Medium rather than Low, because the failure mode is a feature closing with no verdict on record and no gate able to say so, and because the recovery cost is a full re-run of a round gate rather than a read. Two counter-measures, for whoever takes this: have the closure round's own block order the verdict slice as a named unit the way every other authored text is ordered, or give `.agent/handoff.md` a terminator marker the integrity gate can look for. This is not F085's defect — it is a hole in the terminator rule itself, which is why it needed a carrier rather than a repair inside that feature. The fix edits docs/agents/planner_reviewer_prompt.md or the integrity gate, neither of which F086 owns, so it routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.
<<<END R0571>>>

<<<SLICE STATUSLINE-FROM>>>
- [ ] F086 — Release capability
<<<END STATUSLINE-FROM>>>

<<<SLICE STATUSLINE-TO>>>
- [~] F086 — Release capability
<<<END STATUSLINE-TO>>>

<<<SLICE CONTEXT>>>
# Context — F086 Release capability

## Active Branch
feature/f086-release-capability, cut from `main` at 76661dc1, the merge commit
of PR #206, which the operator merged manually at the Open PR Gate. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round
makes every commit.

## Scope
In: shipping Remedy as a normal installable tool — a single wheel with the
console entrypoint `remedy`, the built UI carried as package data, asset
resolution that works from an installed wheel as well as from a checkout, a
single-sourced version with build info behind `remedy --version`, a release CI
stage gated on tag/version agreement and on a changelog section, a wheel-size
budget, and a fresh-virtualenv install smoke.

Out, per the feature file's Do-not-touch: auto-publishing, installers beyond
pip, update mechanisms and the license choice. Publishing to an index stays a
HUMAN command in v1; automating the final upload is explicitly rejected for this
feature. No wording anywhere may claim the wheel ships assets it does not.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state live:
  tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- Repository-wide `ruff check` is RED at the claim and is NOT a gate (R-0364):
  the reviewer measured 26 errors at 76661dc1 — 20 I001, 4 F401, 1 F821 and 1
  UP035. Ruff is gated scoped to the files a round touches, measured against the
  SAME files at 76661dc1 so a pre-existing error is not read as a new one.
- A wheel build runs npm. Every such spawn goes through the F085 `exec_guard`
  seam rather than a bare subprocess, and a round that adds one says so.
- 152 findings are open at the claim, carried forward into the reset record per
  DECISION F057 D1. R-0403, R-0448, R-0482, R-0487, R-0490, R-0567, R-0568,
  R-0569, R-0570 and R-0571 are routed to a paydown branch and are deliberately
  not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXT>>>

<<<SLICE PLAN>>>
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
R1, this round: the STATUS claim `[ ]` → `[~]`, the live-review reset carrying
the F085 open set forward, and the registration of the two closure candidates
F085's R74 closure review produced. No production code and no packaging change.

## Next Steps
1. R2 — the packaging-shape inventory in `.agent/f086_inventory.md`, MEASURED
   from a real `python -m build` rather than read off the metadata: what the
   built wheel actually contains, whether the UI assets are in it, how the serve
   command resolves that directory, and where a version string could be
   single-sourced from. The reviewer read four starting facts at 76661dc1 —
   `pyproject.toml` declares `version = "0.1.0"` literally, its wheel target
   lists `packages = ["packages", "apps"]` with no package-data rule,
   `apps/cli` defines no `--version` flag, and `ui_server._get_frontend_dist`
   resolves `apps/ui/dist` by walking three parents up from its own `__file__`.
   R2 confirms or refutes each rather than inheriting it.

## Risks
- `packages = ["packages", "apps"]` collects `apps/ui` wholesale, and
  `apps/ui/node_modules` lives under that path. Whether a built wheel already
  carries that tree is a MEASUREMENT R2 must take; it is not a conclusion this
  file draws, and the wheel-size budget T003 wants depends on the answer.
- The feature file requires dual-mode asset resolution, checkout and installed
  wheel, and the resolver has one mode today. Adding the second is T001's
  substance and the reason T001 is the largest slice.
- Building a wheel spawns npm. That spawn is exactly what F085's guard now
  bounds, so a packaging round that bypasses the seam would silently undo
  stage-1 containment.
<<<END PLAN>>>

<<<SLICE CANDIDATES>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty. Both candidates F085's R74 closure review produced were
registered in `.agent/live_review.md` at F086 R1 — the README accepted-list
asymmetry as R-0570, and the last-round terminator hole as R-0571 — which is
what the closure protocol asks the next feature's first reviewed round to do.
<<<END CANDIDATES>>>
