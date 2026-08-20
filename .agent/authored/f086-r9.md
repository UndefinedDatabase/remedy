── STEP R9 — F086 Release capability (T001 part (b): the packaging guard, and the kept two-mode resolver test) ──

Goal:
Land the guard DECISION F086 D1 part (b) still owes: a wheel build whose
`apps/ui/dist/index.html` is absent must FAIL LOUDLY instead of exiting 0 and
shipping a wheel with zero UI files, which is what it does today. Land with it
the two-mode resolver TEST that DECISION F086 D3 keeps after withdrawing the
two-mode resolver CODE. Register R-0580 and record the R8 verdict.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r9.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN9 slice, whole file
  C2  append the FINDINGS3 slice to `.agent/live_review.md`
  C3  append the RECORD7 slice to `.agent/live_review.md`
  C4  THE GUARD — new file `hatch_build.py` plus the `pyproject.toml` hooks entry
  C5  THE TESTS — new file `tests/test_packaging_smoke.py`
  C6  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because docs/agents/planner_reviewer_prompt.md §3 pre-emission
item 23 requires the plan to advance before any commit touching the finding
ledger. C2 precedes C3 because §4 item 4 requires findings to persist in their
own commit before anything else, so nothing is lost if the session dies. C4
precedes C5 because the test file imports `hatch_build`, and a commit whose test
cannot import its subject is not independently checkable.

Base:
This round starts from `419fb683`, the tip of `feature/f086-release-capability`
and the R8 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

What the reviewer already measured, so you are not rediscovering it: the whole
change set below was written into a disposable worktree OUTSIDE this repository
at `419fb683`, then built, tested, linted and RED-CONTROLLED before this block
was emitted. The numbers the gates order are that dry run's numbers. The build
toolchain is already installed at `.remedy-wt/f086r9-pylib` (hatchling 1.32.0,
build 1.5.0) and you may reuse it rather than re-installing it.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim; no marker line ever reaches a target file.
The slices are PLAN9, FINDINGS3, RECORD7, HOOK, TESTS, TOMLFROM and TOMLTO.
PLAN9, HOOK and TESTS are COMPLETE files including their single trailing
newline. FINDINGS3 and RECORD7 are EOF-APPENDS, defined as pure concatenation
with each slice's own leading blank line INSIDE the slice, so nothing is
prepended and nothing is stripped. TOMLFROM and TOMLTO are a FROM/TO pair, and
the reviewer ran the containment test on it mechanically, with this output —
TO contains FROM: true. That pair is therefore APPEND-shaped, its obligation is
the ordered equality G7 states, and NO "FROM 0x" count is ordered for it,
because that count is unattainable by construction for an append (§4.9, finding
R-0522).

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `419fb683`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r9.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r9.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r9.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN9 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the FINDINGS3 slice to `.agent/live_review.md` under the append
   convention. Commit alone. It registers R-0580, a defect in the REVIEWER's own
   R8 gate text and not a defect of your predecessor's work.

5. C3 — append the RECORD7 slice to `.agent/live_review.md` under the append
   convention. Commit alone. It is the reviewer's R8 verdict. The paragraph
   begins `Gate:` and registers no finding id, so it moves no ledger set.

6. C4 — THE GUARD, both its paths in ONE commit because a hook file no
   `pyproject.toml` registers is dead code, and a registration pointing at no
   file breaks every build:
   (a) create `hatch_build.py` at the repository root, byte-verbatim from the
       HOOK slice, whole file;
   (b) in `pyproject.toml`, replace the single occurrence of the TOMLFROM slice
       with the TOMLTO slice. TOMLFROM occurs exactly 1x at `419fb683` — the
       reviewer counted it — and the pair is APPEND-shaped, so the surrounding
       bytes are untouched and nothing else in that file moves.
   Commit both together.

7. C5 — THE TESTS. Create `tests/test_packaging_smoke.py`, byte-verbatim from
   the TESTS slice, whole file. This is the path F086's own feature file suggests
   by name. Commit alone.

8. C6 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 419fb683..<HEAD>`. Report your own C6 insertion count and
   the post-C6 path set in the ROUND REPORT rather than in the file, because a
   handoff cannot measure the commit that writes it (§3 item 14). If the file
   exceeds the cap, declare the overage under AGENTS.md DECISION D15 naming its
   cause; drop no section to meet it. The `Next` section names, in this order,
   the next session's first two actions: re-read `.agent/STOP` from disk
   (Phase 1 rule 1), then run the Open PR Gate (Phase 1 rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r9.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `hatch_build.py`, `pyproject.toml`,
   `tests/test_packaging_smoke.py`, and `.agent/handoff.md` at C6.
   `packages/orchestration/ui_server.py` is NOT in it: DECISION F086 D3 withdrew
   the resolver code change and kept only its test, so the resolver is exercised
   as it stands and never modified. No file under `docs/` is in it either — the
   packaging ist-doc is written at closure, when the built state stops moving,
   and PLAN9 says so on disk.
3. Every destructive check — each red control in G8 and G9 — runs ONLY inside a
   disposable `git worktree` sited OUTSIDE this repository, and every such
   worktree is removed before the handback. hatchling drops every VCS exclusion
   when the build root is itself gitignore-matched, so a probe under
   `.remedy-wt/` reads the wrong file set (finding R-0574); that is why the
   siting is outside and not merely off to one side. `git status --porcelain` in
   the primary checkout is EMPTY at every commit and at the handback, and `git
   worktree list` is back to one line before you write C6.
4. Both suite commands run in the PRIMARY checkout, never in a worktree, and
   SERIALLY — the second starts only after the first has ENDED. Two concurrent
   pytest processes produce false reds in this repository, and a fresh worktree
   has no `apps/ui/node_modules`, so a suite run there is red for a reason that
   has nothing to do with your change (finding R-0518).
5. Never weaken a test, delete an assertion, or relax the guard to make anything
   green. If a gate below is red, report the red with its raw output and hand
   off; a red gate is the round's result, not an obstacle to route around.
6. The `PYTHONPATH=... python3 -m build` shell form is REFUSED by this session's
   Bash guard, as are shell loops, `$( )` and `${arr[0]}`. Set `os.environ` and
   drive `build` inside a `python3 - <<'PY'` heredoc, as G8's recipe says.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout; `git
    worktree list` exactly 1 line; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r9.md`, the committed
    `.agent/authored/f086-r9.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256, the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN9 slice extracted
    from the COMMITTED `.agent/authored/f086-r9.md`. Report its sha256 and line
    count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPENDS. For C2 and C3 separately: the pre-commit blob of
    `.agent/live_review.md` is a byte-exact PREFIX of the post-commit blob, and
    the remainder is byte-equal to FINDINGS3 and to RECORD7 respectively. Report
    both sha256 values.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST AGREE. Extract twice — once by
    PARAGRAPH (split the file on blank lines; a paragraph counts when it STARTS
    with `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — `
    and `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids
    / unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and
    the two registered id SETS must be EQUAL. Expected at HEAD: 163 registered,
    2 resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:`, 161 open.
    Report the ids added over the `419fb683` set as the SETS themselves and not
    only their sizes; expected `['R-0580']` under both. As the control that
    proves this check can fail, report the same readings at `419fb683`, where the
    two agree at 162 registered / 2 resolved / 160 open — a round in which they
    disagreed at HEAD would be a red gate, not a rounding difference.

G6  NEW FILES ARE BYTE-EXACT. `hatch_build.py` and
    `tests/test_packaging_smoke.py` at HEAD are byte-equal to the HOOK and TESTS
    slices extracted from the COMMITTED block. Report both sha256 values and both
    line counts. Both files are NEW at `419fb683` — confirm with `git ls-tree
    419fb683 -- <path>` that each returns EMPTY, so "new file" is measured rather
    than assumed.

G7  THE TOML PAIR, BY ORDERED EQUALITY. `pyproject.toml` at HEAD is byte-equal to
    the blob at `419fb683` with its single occurrence of TOMLFROM replaced by
    TOMLTO. Compute that expected text programmatically and compare; report the
    sha256 of both sides and that they match. Report also that TOMLFROM occurs
    exactly 1x in the `419fb683` blob. Because the pair is APPEND-shaped, do NOT
    report a "TOMLFROM 0x at HEAD" count: it is 1x at HEAD by construction, and
    ordering that count would put a false line into the permanent record.

G8  THE GUARD, BOTH COLOURS, FROM OUTSIDE THE REPOSITORY. Add a disposable
    worktree at HEAD outside this repository (`git worktree add
    /home/decodeux/remedy-f086r9-check HEAD`) and a second one at the base
    (`git worktree add /home/decodeux/remedy-f086r9-basechk 419fb683`). With
    `os.environ['PYTHONPATH']` set to the ABSOLUTE path of
    `.remedy-wt/f086r9-pylib`, run `build --wheel --no-isolation --outdir <out>
    <worktree>` via `runpy.run_module('build', run_name='__main__')` inside a
    heredoc, and report for EACH run below the exit code, whether a wheel was
    produced, its member count, and the number of members whose name starts
    `apps/ui/dist/`:
      (a) HEAD worktree, `apps/ui/dist` COPIED IN from the primary checkout →
          exit 0, 417 members, 3 UI members;
      (b) HEAD worktree, `apps/ui/dist` REMOVED → NON-ZERO exit, NO wheel
          produced, and the captured error text contains
          `apps/ui/dist/index.html`;
      (c) THE RED CONTROL, base worktree at `419fb683`, dist REMOVED → exit 0,
          414 members, 0 UI members. This is the defect the round closes; without
          it (b) proves nothing, because a build that cannot succeed is not a
          guard;
      (d) base worktree, dist COPIED IN → exit 0, 417 members, 3 UI members,
          which shows the guard costs the good path nothing.
    Remove both worktrees and prune afterwards.

G9  THE NEW TESTS. `python3 -m pytest tests/test_packaging_smoke.py -q -rf` in
    the PRIMARY checkout → exit 0, 6 passed. Then, in a disposable worktree
    OUTSIDE the repository and never in the primary checkout, take the RED
    CONTROLS below and report the colour AND the counts for each:
      (i)   in that worktree's `packages/orchestration/ui_server.py` replace the
            single occurrence of the byte string
            `.resolve().parent.parent.parent / "apps" / "ui" / "dist"` with
            `.resolve().parent.parent / "apps" / "ui" / "dist"` — the reviewer
            counted that string and it occurs exactly 1x in that file at
            `419fb683` — and re-run: expect 2 failed, 4 passed;
      (ii)  revert (i), then in that worktree's `hatch_build.py` replace the
            single occurrence of the line `    if not index.is_file():` with
            `    if False:` and re-run: expect 2 failed, 4 passed;
      (iii) revert (ii) and re-run: expect 6 passed, so the worktree is PROVED
            restored rather than assumed restored.
    A control that stays green is a red gate.

G10 ROUND GATE SUITE. `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` in the PRIMARY checkout →
    exit 0, 160 passed. These are the readers of the `.agent/` state files this
    round rewrites.

G11 CANARY. `python3 -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY
    checkout → exit 0, 42 passed. Run it only after G10 has ENDED; state that the
    two runs did not overlap.

G12 LINT, SCOPED. `python3 -m ruff check hatch_build.py
    tests/test_packaging_smoke.py` from the repository root → exit 0, no
    findings. Both files are new at `419fb683`, so there is no base multiset to
    compare against and none is ordered; ruff is RED repo-wide at 26 pre-existing
    errors and this gate is deliberately scoped to the two files the round adds.

G13 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `419fb683..HEAD` BEFORE C6, one line each.
    None may exceed 500. Report C6's own count in the round report, not here.

G14 HISTORY. Every commit in `419fb683..HEAD` has exactly one parent and the
    chain is linear from `419fb683`. `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, or force-push. Report the chain.

G15 PATH SET. `git diff --name-only 419fb683..HEAD`, measured before C6, is
    exactly the paths constraint 2 names minus `.agent/handoff.md`. Report the
    post-C6 set in the round report. Confirm that no path under `docs/` or
    `scripts/` appears and that the only paths under `apps/` or `packages/` are
    none at all; and confirm with `git ls-tree 419fb683` that `docs/`, `scripts/`,
    `apps/` and `packages/` all EXIST at the base, so the clause forbids
    something real.

G16 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report its output verbatim. Merge
    nothing whatever it says; this round opens and merges no PR.

Handback:
Completion report plus a rewritten `.agent/handoff.md`. Push after C5 and again
after C6. Report every gate above with its REAL exit code and output — "green" as
a word is a finding. If any gate is red, say so plainly with the raw output and
hand off; never repair a red gate by changing what it measures.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN9>>>
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
R9, this round: land T001 part (b) — the packaging-time guard that refuses to
build a wheel whose `apps/ui/dist/index.html` is absent — together with the
two-mode resolver TEST that DECISION F086 D3 keeps after withdrawing the
two-mode resolver CODE. Register R-0580 and record the R8 verdict.

## Next Steps
1. R10 — T002: the version single-source and the build info behind
   `remedy --version`, with a checkout mode that reports "dev" honestly
   (DECISION F086 D2).
2. Then T003 — the release CI stage, the changelog and tag gate, the wheel-size
   budget and the seeded-failure tests; then the integration gate; then closure.
   The packaging ist-doc is written at closure, when the built state stops moving.

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
<<<END PLAN9>>>

<<<SLICE FINDINGS3>>>

- R-0580 — Medium — A gate named a commit range over which three of its own four clauses are false. F086 R8's G6 required the separation repair to change separation and nothing else, and fixed that range as "Between `b769ccd7` and the C3 commit". Three of its clauses — the identical multiset of `^- R-\d+ — ` lines, the byte-identical blank-stripped file, and the exactly-3 byte growth — hold only ACROSS C3, the single commit that performs the repair. C2 sits inside the range the gate names and appends two finding lines, so measured over `b769ccd7..2ea6de4b` the symmetric difference is 2 — exactly `- R-0578 — ` and `- R-0579 — ` — blank-stripped equality is False, and the byte delta is 2575 rather than 3. The reviewer re-measured all six readings itself at R9 and reproduces them. The worker recorded both readings and declared the contradiction rather than reconciling it, which is the correct handling, so this is a defect of the reviewer's text alone. The counter-measure is docs/agents/planner_reviewer_prompt.md §3 item 22 — a sentence quantifying across COMMITS is measured by walking that range — applied to the range a gate NAMES and not only to the values it states, because here every individual clause is sound and only the range is wrong.
<<<END FINDINGS3>>>

<<<SLICE RECORD7>>>

Gate: R9 — the R8 entry. R8 PASSED. Every gate its block ordered was re-executed by the reviewer over `b769ccd7..419fb683` rather than read from the handback, and every reading reproduces. THE LEDGER DEFECT IS REPAIRED AND THE REPAIR IS THE ROUND'S POINT: at `b769ccd7` an independent extractor written by the reviewer reads 157 registered by paragraph against 160 line-anchored, and at `419fb683` it reads 162 and 162 with the two registered id SETS equal, 2 resolved, 160 open, 0 duplicate ids, 0 unregistered resolutions and 0 `Landed:` lines — so the disagreement R-0578 records is gone and the agreement is measured, not asserted. THE REPAIR TOUCHED NOTHING ELSE: across C3 the multiset of finding lines is identical at 162 each side with symmetric difference empty, the blank-stripped file is byte-identical, the byte length grew by exactly 3, and finding lines not preceded by a blank line fall from 3 at `b769ccd7` to 0 — the reviewer's own control value, reproduced. THE TRANSPORT HELD: `.agent/authored/f086-r8.md` and `.agent/last_block.md` at `419fb683` are byte-equal at sha256 4b90e4a1aef0ffe5066bfbb046a6f67422ceef9532545bddbd98f80c71b7d91d, 29943 B, 381 lines; all five slices were re-extracted by their markers and PLAN8 is byte-equal to `.agent/plan.md` at 42 lines, the three ledger appends are exact prefix-plus-remainder, and the C6 handoff blob is a byte-exact prefix of the file at HEAD whose 56-line remainder is exactly the VERDICT slice. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` or `.agent/handoff.md`. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: five paths, all under `.agent/`, over nine single-parent commits inserting 381, 257, 8, 4, 3, 2, 2, 47 and 56 lines, none over 500 and no DECISION F104 D1 exemption invoked; `pyproject.toml` and every path under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` are absent from the range. THE ONE DEFECT IS THE REVIEWER'S and is registered as R-0580: G6's named range is one commit too wide, which the worker declared rather than hid. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the points the block names and the serial ordering of the two pytest runs, whose end state — one worktree line and an empty `git status --porcelain` — the reviewer did confirm.
<<<END RECORD7>>>

<<<SLICE HOOK>>>
"""Packaging-time guard: refuse to build a wheel with no built UI assets.

WHY: `artifacts = ["apps/ui/dist/**"]` in pyproject.toml carries the built UI into
the wheel, but it is silent when that directory is absent — measured at 419fb683,
a build with the carry applied and no `apps/ui/dist` present exits 0 and ships a
414-member wheel with zero UI files. That is exactly the "empty UI directory
shipped silently" DECISION F086 D1 part (b) forbids, and this hook is that guard.

Remedy deliberately keeps the rule in a plain function rather than only in the
hook class: the test suite must be able to exercise it without the build backend
installed, and the class below is a thin adapter that hatchling loads.
"""

from __future__ import annotations

from pathlib import Path

try:  # the build backend supplies hatchling; the test environment need not
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # pragma: no cover - only the real wheel build takes this path
    BuildHookInterface = object  # type: ignore[assignment,misc]

FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"


def assert_frontend_assets_built(root: str | Path) -> Path:
    """Return the frontend entry point under `root`, or raise ValueError if absent."""
    index = Path(root) / FRONTEND_DIST_INDEX
    if not index.is_file():
        raise ValueError(
            f"remedy: refusing to build a wheel without built UI assets. "
            f"{FRONTEND_DIST_INDEX} is missing under {root}. Build the frontend "
            f"first (npm --prefix apps/ui run build); a wheel built without it "
            f"installs a CLI whose UI cannot serve."
        )
    return index


class FrontendAssetsBuildHook(BuildHookInterface):
    """Fail the wheel build when the built frontend entry point is missing."""

    PLUGIN_NAME = "remedy-frontend-assets"

    def initialize(self, version, build_data):
        assert_frontend_assets_built(self.root)
<<<END HOOK>>>

<<<SLICE TESTS>>>
"""Packaging contract tests for the wheel's UI assets.

Covers F086 T001: the packaging-time guard that refuses a wheel with no built
frontend (DECISION F086 D1 part (b)), and the asset resolution that must hold in
BOTH modes — from a checkout and from an installed wheel (DECISION F086 D3, which
withdrew the two-mode resolver CODE and kept this test).
"""

from __future__ import annotations

from pathlib import Path

import pytest

import packages.orchestration.ui_server as ui_server
from hatch_build import FRONTEND_DIST_INDEX, assert_frontend_assets_built


def _wheel_root_layout(root: Path, *, with_index: bool) -> Path:
    """Lay out a wheel root: apps/ is a sibling of packages/, module three deep."""
    module = root / "packages" / "orchestration" / "ui_server.py"
    module.parent.mkdir(parents=True, exist_ok=True)
    module.write_text("# stand-in for the installed module\n")
    dist = root / "apps" / "ui" / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    if with_index:
        (dist / "index.html").write_text("<html></html>")
    return module


@pytest.mark.unit
class TestFrontendDistResolution:
    """`_get_frontend_dist` resolves in both install modes (DECISION F086 D3)."""

    def test_installed_wheel_mode_resolves_under_the_wheel_root(self, tmp_path, monkeypatch):
        module = _wheel_root_layout(tmp_path, with_index=True)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() == tmp_path / "apps" / "ui" / "dist"

    def test_checkout_mode_resolves_under_the_repository_root(self, tmp_path, monkeypatch):
        # A checkout has the SAME geometry as a wheel root: three parents up from
        # the module file, apps/ is a sibling of packages/. That identity is why
        # DECISION F086 D3 withdrew the dual-mode resolver and kept this test.
        checkout = tmp_path / "checkout"
        module = _wheel_root_layout(checkout, with_index=True)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() == checkout / "apps" / "ui" / "dist"

    def test_missing_index_resolves_to_none_in_either_mode(self, tmp_path, monkeypatch):
        module = _wheel_root_layout(tmp_path, with_index=False)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() is None


@pytest.mark.unit
class TestFrontendAssetsBuildGuard:
    """The packaging-time guard refuses a wheel with no built UI."""

    def test_present_assets_return_the_index_path(self, tmp_path):
        index = tmp_path / FRONTEND_DIST_INDEX
        index.parent.mkdir(parents=True)
        index.write_text("<html></html>")
        assert assert_frontend_assets_built(tmp_path) == index

    def test_absent_assets_raise_and_name_the_missing_path(self, tmp_path):
        with pytest.raises(ValueError) as excinfo:
            assert_frontend_assets_built(tmp_path)
        assert FRONTEND_DIST_INDEX in str(excinfo.value)

    def test_a_directory_without_the_index_is_still_refused(self, tmp_path):
        (tmp_path / "apps" / "ui" / "dist").mkdir(parents=True)
        with pytest.raises(ValueError):
            assert_frontend_assets_built(tmp_path)
<<<END TESTS>>>

<<<SLICE TOMLFROM>>>
artifacts = ["apps/ui/dist/**"]
<<<END TOMLFROM>>>

<<<SLICE TOMLTO>>>
artifacts = ["apps/ui/dist/**"]

[tool.hatch.build.targets.wheel.hooks.custom]
# WHY: the carry above is SILENT when apps/ui/dist is absent — the build still
# exits 0 and ships a wheel with no UI. This hook is DECISION F086 D1 part (b).
path = "hatch_build.py"
<<<END TOMLTO>>>
