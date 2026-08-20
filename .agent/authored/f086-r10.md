── STEP R10 — F086 Release capability (T002: `remedy --version`, honest in both modes) ──

Goal:
Give Remedy the version command DECISION F086 D2 rules: `remedy --version` reads
the version back through package metadata so no second literal exists to drift,
prints the build revision, the Python version and the platform, and reports `dev`
for whatever a checkout cannot prove. Record the R9 verdict, which passed clean.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r10.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN10 slice, whole file
  C2  append the RECORD8 slice to `.agent/live_review.md`
  C3  new file `apps/cli/version_report.py`, plus the three `apps/cli/grouped.py`
      pairs that wire the flag
  C4  new file `tests/cli/test_version_report.py`
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. C3 puts the module and its wiring
in ONE commit because a module nothing calls is not a feature; C4 follows because
its tests import both. This round registers NO finding — R9 produced none — so
the open set does not move and no FINDINGS slice exists.

Base:
This round starts from `e7c219cc`, the tip of `feature/f086-release-capability`
and the R9 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

What the reviewer already measured: the whole change set below was applied in a
disposable worktree OUTSIDE this repository at `e7c219cc`, then run, linted and
RED-CONTROLLED before emission. The gates order that dry run's numbers.

What T002 still owes, stated so no later reader mistakes this for the finished
slice: `resolve_build_revision()` reads a `REVISION` file out of the installed
distribution's metadata and NOTHING WRITES THAT FILE YET, so an installed wheel
reports `dev` exactly as a checkout does. The embedding belongs in
`hatch_build.py` and is a later round's work; PLAN10 says so on disk.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. The slices are
PLAN10, RECORD8, VERSIONMOD, TESTMOD and the FROM/TO pair PAIRFROM with PAIRTO.
PLAN10, VERSIONMOD and TESTMOD are COMPLETE files including their single trailing
newline. RECORD8 is an EOF-APPEND, defined as pure concatenation with its own
leading blank line INSIDE the slice. The reviewer ran the containment test on the
pair mechanically, and this is its output — TO contains FROM: true. The pair is
therefore APPEND-shaped, its obligation is the ordered equality G7 states, and NO
"FROM 0x" count is ordered for it (§4.9, finding R-0522).

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `e7c219cc`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r10.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r10.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r10.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN10 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD8 slice to `.agent/live_review.md` under the append
   convention. Commit alone. It is the reviewer's R9 verdict. The paragraph
   begins `Gate:` and registers no finding id, so it moves no ledger set.

5. C3 — THE COMMAND, both edits in ONE commit:
   (a) create `apps/cli/version_report.py`, byte-verbatim from the VERSIONMOD
       slice, whole file. It carries the whole flag: the metadata readers, the
       report renderer, and `handle_version_flag`, which decides whether argv
       asked for a version at all;
   (b) in `apps/cli/grouped.py`, replace the single occurrence of PAIRFROM with
       PAIRTO. PAIRFROM occurs exactly 1x at `e7c219cc` — the reviewer counted
       it — and this calls the flag handler from `main()` BEFORE the help
       pre-scan, so `--version` is not swallowed by `--help` or by argparse.
   The import sits inside `main()` rather than at module scope, the pattern
   `grouped.py` already uses for its local `json` import, which keeps this round
   to ONE pair against that file. Commit both together.

6. C4 — THE TESTS. Create `tests/cli/test_version_report.py`, byte-verbatim from
   the TESTMOD slice, whole file. The name follows AGENTS.md's discoverability
   convention that a test file is named after the source it covers. Commit alone.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of e7c219cc..<HEAD>`. Report your own C5 insertion count and
   the post-C5 path set in the ROUND REPORT rather than in the file, because a
   handoff cannot measure the commit that writes it (§3 item 14). If the file
   exceeds the cap, declare the overage under AGENTS.md DECISION D15 naming its
   cause; drop no section to meet it. The `Next` section names, in this order,
   the next session's first two actions: re-read `.agent/STOP` from disk
   (Phase 1 rule 1), then run the Open PR Gate (Phase 1 rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r10.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `apps/cli/version_report.py`, `apps/cli/grouped.py`,
   `tests/cli/test_version_report.py`, and `.agent/handoff.md` at C5.
   `pyproject.toml` is NOT in it: DECISION F086 D2 keeps the version literal
   exactly where it already is, at `pyproject.toml:7`, and this round adds a
   READER for it rather than a second place to write it. `hatch_build.py` is not
   in it either — the REVISION embedding is the next round's work, as the Base
   section says.
3. Every destructive check — each red control in G9 — runs ONLY inside a
   disposable `git worktree` sited OUTSIDE this repository, and that worktree is
   removed and pruned before the handback. `git status --porcelain` in the
   primary checkout is EMPTY at every commit and at the handback, and `git
   worktree list` is back to one line before you write C5.
4. Every suite command runs in the PRIMARY checkout, never in a worktree, and
   SERIALLY — each starts only after the previous has ENDED. Two concurrent
   pytest processes produce false reds in this repository, and a fresh worktree
   has no `apps/ui/node_modules`, so a suite run there is red for a reason that
   has nothing to do with your change (finding R-0518).
5. Never weaken a test, delete an assertion, or relax the command to make
   anything green. If a gate below is red, report the red with its raw output and
   hand off; a red gate is the round's result, not an obstacle to route around.
6. Shell loops, `$( )`, `${arr[0]}` and env-prefix command forms are refused by
   this session's Bash guard. Route that work through `python3 - <<'PY'`
   heredocs; helper scripts under the gitignored `.remedy-wt/` are expected.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout; `git
    worktree list` exactly 1 line; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r10.md`, the committed
    `.agent/authored/f086-r10.md` and the committed `.agent/last_block.md` are
    all three byte-EQUAL. Report the sha256, the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN10 slice extracted
    from the COMMITTED `.agent/authored/f086-r10.md`. Report its sha256 and line
    count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob and the remainder is byte-equal to RECORD8. Report
    the sha256 of the remainder.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST AGREE AND MUST NOT MOVE. Extract
    twice — once by PARAGRAPH (split the file on blank lines; a paragraph counts
    when it STARTS with `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED
    (`^- R-\d+ — ` and `^Done: R-\d+ — `). At HEAD report registered / resolved /
    duplicate ids / unregistered resolutions / anchored `Landed:` lines / open,
    for BOTH, and the two registered id SETS must be EQUAL. Expected at HEAD:
    163 registered, 2 resolved, 0 duplicates, 0 unregistered resolutions,
    0 `Landed:`, 161 open. Report the symmetric difference of the HEAD registered
    set against the `e7c219cc` set as the SET itself; it must be EMPTY, because
    this round registers nothing. The control that proves the extraction can see
    a difference at all is R9's own reading, already on disk in RECORD8: the same
    extractor read `['R-0580']` added across that round.

G6  NEW FILES ARE BYTE-EXACT. `apps/cli/version_report.py` and
    `tests/cli/test_version_report.py` at HEAD are byte-equal to the VERSIONMOD
    and TESTMOD slices extracted from the COMMITTED block. Report both sha256
    values and both line counts. Both are NEW at `e7c219cc` — confirm with `git
    ls-tree e7c219cc -- <path>` that each returns EMPTY, so "new file" is
    measured rather than assumed.

G7  THE PAIR, BY ORDERED EQUALITY. `apps/cli/grouped.py` at HEAD is byte-equal to
    the blob at `e7c219cc` with its single occurrence of PAIRFROM replaced by
    PAIRTO. Compute that expected text programmatically and compare; report the
    sha256 of both sides and that they match. Report also that PAIRFROM occurs
    exactly 1x in the `e7c219cc` blob. Because the pair is APPEND-shaped, do NOT
    report a "PAIRFROM 0x at HEAD" count: it is still 1x at HEAD by construction,
    and ordering that count would put a false line into the permanent record.

G8  THE COMMAND ACTUALLY RUNS. In the PRIMARY checkout run
    `python3 -m apps.cli.grouped --version` and report its exit code and FULL
    stdout. Exit 0, first line beginning `remedy   `, later lines beginning
    `build    `, `python   ` and `platform `. The `build` line MUST read `dev`,
    because nothing writes the REVISION file yet; a `build` line reading anything
    else would mean the round invented a revision, which is the one outcome
    DECISION F086 D2 forbids outright.

G9  THE NEW TESTS. `python3 -m pytest tests/cli/test_version_report.py -q -rf` in
    the PRIMARY checkout → exit 0, 8 passed. Then, in a disposable worktree
    OUTSIDE the repository and never in the primary checkout, take the RED
    CONTROLS below and report the colour AND the counts for each:
      (i)   in that worktree's `apps/cli/version_report.py`, delete the two lines
            `    if embedded is None or not embedded.strip():` and
            `        return UNKNOWN_MARKER` that immediately follow the
            `read_text` call in `resolve_build_revision` — the reviewer counted
            that two-line block and it occurs exactly 1x in that file — and
            re-run: expect 4 failed, 4 passed;
      (ii)  revert (i), then in that worktree's `apps/cli/grouped.py` replace the
            single occurrence of the two lines `    if handle_version_flag(argv):`
            and `        return` with `    if False:` and `        return`, and
            re-run: expect 2 failed, 6 passed;
      (iii) revert (ii) and re-run: expect 8 passed, and report that worktree's
            `git status --porcelain` to show it was restored, not assumed.
    A control that stays green is a red gate.

G10 CLI REGRESSION. `python3 -m pytest tests/test_grouped_cli.py
    tests/cli/test_cli_ux.py tests/test_command_catalog.py
    tests/cli/test_command_catalog.py -q -rf` in the PRIMARY checkout → exit 0,
    601 passed. These are the readers of the entry point this round edits, and
    the reviewer measured 601 at `e7c219cc` with the change applied.

G11 ROUND GATE SUITE. `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` in the PRIMARY checkout →
    exit 0, 160 passed. These are the readers of the `.agent/` state files this
    round rewrites.

G12 CANARY. `python3 -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY
    checkout → exit 0, 42 passed. Run it only after G11 has ENDED; state that no
    two suite runs overlapped.

G13 LINT, SCOPED. `python3 -m ruff check apps/cli/version_report.py
    tests/cli/test_version_report.py apps/cli/grouped.py` from the repository
    root → exit 0, no findings. `apps/cli/grouped.py` is the only one that exists
    at the base, and the reviewer ran ruff over it AT `e7c219cc`, where it also
    exits 0 — so this compares like with like rather than demanding a clean file
    that was never clean. Ruff is RED repo-wide at 26 pre-existing errors, so
    this gate is scoped to the paths the round touches.

G14 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `e7c219cc..HEAD` BEFORE C5, one line each.
    None may exceed 500. Report C5's own count in the round report, not here.

G15 HISTORY. Every commit in `e7c219cc..HEAD` has exactly one parent and the
    chain is linear from `e7c219cc`. `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, or force-push. Report the chain.

G16 PATH SET. `git diff --name-only e7c219cc..HEAD`, measured before C5, is
    exactly the paths constraint 2 names minus `.agent/handoff.md`. Report the
    post-C5 set in the round report. Confirm that `pyproject.toml`,
    `hatch_build.py` and every path under `docs/`, `scripts/` and `packages/` are
    ABSENT from it, and confirm with `git ls-tree e7c219cc` that `pyproject.toml`,
    `hatch_build.py`, `docs/`, `scripts/` and `packages/` all EXIST at the base,
    so the clause forbids something real.

G17 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report its output verbatim. Merge
    nothing whatever it says; this round opens and merges no PR.

Handback:
Completion report plus a rewritten `.agent/handoff.md`. Push after C4 and again
after C5. Report every gate above with its REAL exit code and output — "green" as
a word is a finding. If any gate is red, say so plainly with the raw output and
hand off; never repair a red gate by changing what it measures.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN10>>>
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
R10, this round: land T002's reporting surface — `remedy --version` reading the
version back through package metadata per DECISION F086 D2, with the build
revision, the Python version and the platform, and reporting `dev` for whatever
a checkout cannot prove. Record the R9 verdict. T001 is complete and proved: the
wheel carries `apps/ui/dist`, and a build without it now fails loudly.

## Next Steps
1. R11 — close this session: record the R10 verdict and write the reviewer's
   session verdict to disk.
2. Then the REVISION embedding, which T002 still owes: `resolve_build_revision()`
   reads a `REVISION` file out of the installed distribution's metadata, and
   nothing writes that file yet, so an installed wheel reports `dev` exactly as a
   checkout does. The build hook `hatch_build.py` is where it gets written.
3. Then T003 — the release CI stage, the changelog and tag gate, the wheel-size
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
<<<END PLAN10>>>

<<<SLICE RECORD8>>>

Gate: R10 — the R9 entry. R9 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `419fb683..e7c219cc` rather than read from the handback, and every reading reproduces. THE GUARD IS REAL AND THE REVIEWER PROVED BOTH COLOURS ITSELF, from a worktree sited OUTSIDE this repository because hatchling drops every VCS exclusion when the build root is gitignore-matched (finding R-0574): at `e7c219cc` with `apps/ui/dist` present the build exits 0 and produces a 417-member wheel carrying 3 members under `apps/ui/dist/`, and with that directory removed it exits NON-ZERO, produces NO wheel, and names `apps/ui/dist/index.html` in its error. THE RED CONTROL FIRES, which is what makes the preceding sentence worth anything: the same removal at the base `419fb683` exits 0 and produces a 414-member wheel with 0 UI members, so the defect DECISION F086 D1 part (b) describes reproduces at the base and is closed at HEAD, and a build that could not fail would have proved nothing. THE GUARD COSTS THE GOOD PATH NOTHING: the wheel built with assets present is 417 members at both commits. THE TESTS ARE NOT VACUOUS: `tests/test_packaging_smoke.py` is 6 passed at HEAD, and under the reviewer's own mutations — one `.parent` hop removed from the resolver, then the guard's `if not index.is_file():` replaced by `if False:`, each byte string counted 1x in its named file first — it reads 2 failed / 4 passed each time, returning to 6 passed once reverted. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r9.md`, the committed `.agent/authored/f086-r9.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 5e8c7518f8c033812e470d25fd057e1ba18c9c5dc799fb1d236f24ef0c7908a2, 28751 B, 467 lines; `.agent/plan.md` is byte-equal to its PLAN9 slice at 41 lines; both new files are byte-equal to the HOOK and TESTS slices and both are measured ABSENT at `419fb683`; and `pyproject.toml` at HEAD equals the base blob with its single `artifacts` line replaced by the TOMLTO slice, by ordered equality rather than by a count no append can meet. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the six written files. THE LEDGER MOVED BY EXACTLY ONE ID under BOTH extractions, paragraph and line-anchored, which AGREE at 163 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 161 open, the added set being `['R-0580']` under each. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0, and `ruff check` on the two new files exits 0. THE HYGIENE HELD: eight paths over eight single-parent commits inserting 467, 391, 13, 2, 2, 50, 73 and 82 lines, none over 500 and no DECISION F104 D1 exemption invoked. THE ONE DEVIATION WAS DECLARED AND IS NOT A FINDING: `.agent/handoff.md` stands at 127 lines over the 100-line cap, declared under AGENTS.md DECISION D15 with its cause named and every mandated section present, which is what that decision exists to permit.
<<<END RECORD8>>>

<<<SLICE VERSIONMOD>>>
"""`remedy --version` — the version and build info a release is checked against.

WHY here: DECISION F086 D2 keeps `pyproject.toml` as the single place a version
NUMBER is written and reads it back through package metadata, so no second
literal exists to drift out of sync. In a checkout the distribution is often not
installed and no revision was embedded at build time; this module then reports
`dev` rather than inventing a sha, which D2 makes a requirement and not a
fallback — a version command that reports a fabricated revision is worse than
one that admits it is looking at a working tree.

Remedy deliberately does not generate a `_version.py` at build time: a stale
generated file in a checkout outranks the metadata and reports a version nobody built.
"""

from __future__ import annotations

import platform
import sys
from importlib.metadata import PackageNotFoundError, distribution

DISTRIBUTION_NAME = "remedy"
REVISION_METADATA_FILE = "REVISION"
UNKNOWN_MARKER = "dev"


def resolve_distribution_version() -> str:
    """Return the installed distribution's version, or `dev` in a checkout."""
    try:
        return distribution(DISTRIBUTION_NAME).version
    except PackageNotFoundError:
        return UNKNOWN_MARKER


def resolve_build_revision() -> str:
    """Return the revision embedded at build time, or `dev` when none was."""
    try:
        embedded = distribution(DISTRIBUTION_NAME).read_text(REVISION_METADATA_FILE)
    except PackageNotFoundError:
        return UNKNOWN_MARKER
    if embedded is None or not embedded.strip():
        return UNKNOWN_MARKER
    return embedded.strip()


def render_version_report() -> str:
    """Render the `remedy --version` report as the release gate reads it."""
    return "\n".join(
        [
            f"remedy   {resolve_distribution_version()}",
            f"build    {resolve_build_revision()}",
            f"python   {platform.python_version()}",
            f"platform {platform.platform()}",
        ]
    )


def handle_version_flag(argv: list[str] | None) -> bool:
    """Print the version report if argv asks for it; return whether it did.

    Called before the help pre-scan so `remedy --version` answers from anywhere
    in the command tree and is never swallowed by `--help` or by argparse.
    """
    raw = sys.argv[1:] if argv is None else argv
    if "--version" not in raw:
        return False
    print(render_version_report())
    return True
<<<END VERSIONMOD>>>

<<<SLICE TESTMOD>>>
"""Tests for `remedy --version` (F086 T002, DECISION F086 D2).

Both modes are pinned: an INSTALLED distribution reports its version and the
revision embedded at build time, and a CHECKOUT reports `dev` for what it cannot
prove. The checkout half matters most — D2 makes honest `dev` a requirement, so
a regression that invented a revision must turn a test red.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from types import SimpleNamespace

import pytest

from apps.cli import version_report
from apps.cli.grouped import main


def _install(monkeypatch, version: str, revision: str | None) -> None:
    """Make the distribution look installed, carrying `revision` (or none)."""
    dist = SimpleNamespace(
        version=version,
        read_text=lambda name: revision if name == version_report.REVISION_METADATA_FILE else None,
    )
    monkeypatch.setattr(version_report, "distribution", lambda name: dist)


def _uninstall(monkeypatch) -> None:
    """Make the distribution look absent, as it is in a bare checkout."""

    def _raise(name: str):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(version_report, "distribution", _raise)


@pytest.mark.unit
class TestInstalledMode:
    def test_embedded_revision_is_reported(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "abc1234\n")
        assert version_report.resolve_build_revision() == "abc1234"

    def test_report_carries_version_and_revision(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "abc1234")
        report = version_report.render_version_report()
        assert "remedy   1.2.3" in report
        assert "build    abc1234" in report


@pytest.mark.unit
class TestCheckoutMode:
    def test_uninstalled_version_is_dev(self, monkeypatch):
        _uninstall(monkeypatch)
        assert version_report.resolve_distribution_version() == version_report.UNKNOWN_MARKER

    def test_uninstalled_revision_is_dev(self, monkeypatch):
        _uninstall(monkeypatch)
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER

    def test_installed_without_embedded_revision_is_dev(self, monkeypatch):
        _install(monkeypatch, "1.2.3", None)
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER

    def test_blank_embedded_revision_is_dev(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "   \n")
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER


@pytest.mark.unit
class TestVersionFlag:
    def test_version_flag_prints_the_report_and_returns(self, capsys):
        main(["--version"])
        out = capsys.readouterr().out
        assert out.startswith("remedy   ")
        assert "python   " in out
        assert "platform " in out

    def test_version_flag_wins_over_help(self, capsys):
        main(["--version", "--help"])
        out = capsys.readouterr().out
        assert out.startswith("remedy   ")
        assert "Usage" not in out
<<<END TESTMOD>>>

<<<SLICE PAIRFROM>>>
    # Pre-scan for --help to avoid argparse SystemExit on missing required args
    if _pre_scan_help(argv):
        return
<<<END PAIRFROM>>>

<<<SLICE PAIRTO>>>
    # Pre-scan for --version first: it answers from anywhere in the tree and must
    # not be swallowed by --help or by argparse (DECISION F086 D2).
    from apps.cli.version_report import handle_version_flag

    if handle_version_flag(argv):
        return

    # Pre-scan for --help to avoid argparse SystemExit on missing required args
    if _pre_scan_help(argv):
        return
<<<END PAIRTO>>>
