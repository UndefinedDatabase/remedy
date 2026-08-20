── STEP R12 — F086 Release capability (embed the build revision; record R11) ──

Goal:
Close the hole T002 left open. `apps/cli/version_report.py` reads a `REVISION`
file out of the installed distribution's metadata and NOTHING WRITES IT, so an
installed wheel reports `dev` exactly as a bare checkout does. This round makes
the wheel carry the revision it was built from and makes the reader look where
the build puts it. It also records the R11 verdict and registers R-0581.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r12.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN12 slice, whole file
  C2  append FIND0581 then RECORD10 to `.agent/live_review.md`, in that order
  C3  `hatch_build.py` := the HATCH slice, whole file
  C4  apply the VER FROM/TO pair to `apps/cli/version_report.py`
  C5  create `tests/test_build_revision.py` := the TESTS slice
  C6  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. C2 appends the finding BEFORE the
gate paragraph, the order already on disk for R8's finding and R9's gate entry.

The HATCH docstring states the two facts the reviewer measured on a real wheel
built at `ee22186c`. The hook class is renamed because the old name no longer
fits; it is referenced nowhere outside `hatch_build.py` and hatchling resolves it
by scanning, so `pyproject.toml` stands unchanged.

Base:
This round starts from `ee22186c`, the tip of `feature/f086-release-capability`.
Every range gate below names that SHA. Stay on the existing branch — do NOT
create one, do NOT run the Open PR Gate, do NOT open a PR. The branch stays
pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN12, HATCH
and TESTS are COMPLETE files, each including its single trailing newline.
FIND0581 and RECORD10 are EOF-APPENDS: pure concatenation, each slice's own
leading blank line INSIDE the slice, nothing prepended, nothing stripped.
VERFROM/VERTO are a FROM/TO pair — VERFROM occurs EXACTLY once and is replaced.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `ee22186c`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r12.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r12.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r12.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN12 slice, byte-verbatim, whole file. Commit
   alone.

3. C2 — append FIND0581 and then RECORD10 to `.agent/live_review.md` under the
   append convention, FIND0581 first, one commit for both. FIND0581 registers
   R-0581; RECORD10 is the reviewer's R11 verdict and registers no id.

4. C3, C4, C5 — one commit each, in that order, every slice byte-verbatim and
   nothing else in any of them. C3 `hatch_build.py` := the HATCH slice, whole
   file, replacing the existing 46-line file; `assert_frontend_assets_built` and
   `FRONTEND_DIST_INDEX` keep their names because `tests/test_packaging_smoke.py`
   imports both. C4 replaces the single occurrence of VERFROM in
   `apps/cli/version_report.py` with VERTO. C5 creates
   `tests/test_build_revision.py` := the TESTS slice, a new file at the tests
   root; no package directory and no `__init__.py` is added.

5. C6 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of ee22186c..<HEAD>`. Over the 100-line cap, declare the
   overage under AGENTS.md DECISION D15 and name its cause; drop no mandated
   section to meet it. Report your own C6 insertion count and the post-C6 path
   set in the ROUND REPORT, not in the file, because a handoff cannot measure the
   commit that writes it (§3 item 14). `Next` names, in order, the next session's
   first two actions: re-read `.agent/STOP` (Phase 1 rule 1), then the Open PR
   Gate (rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r12.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `hatch_build.py`, `apps/cli/version_report.py`,
   `tests/test_build_revision.py`, and `.agent/handoff.md` at C6.
   `pyproject.toml` is NOT in it: the hook path and the target config are
   unchanged and hatchling resolves the hook class by scanning, not by name.
3. `git status --porcelain` in the primary checkout is EMPTY at every commit and
   at the handback, and `git worktree list` is exactly one line at the handback.
   The gates add worktrees and remove them; a higher count while they exist is
   expected. Never build inside the primary checkout.
4. EVERY WHEEL PROBE ROOT LIVES OUTSIDE THIS REPOSITORY. hatchling's
   `load_vcs_exclusion_patterns()` returns `[]` — dropping every VCS exclusion
   for the whole build — when the build root's own path is gitignore-matched, and
   `.gitignore` carries a `.remedy-wt/` line, so a probe tree there measures a
   file selection no real build has (finding R-0574). Use `git worktree add
   --detach <path> <sha>` with `<path>` outside `/home/decodeux/Repos/remedy`.
5. The toolchain is vendored at `.remedy-wt/f086r9-pylib` (hatchling 1.32.0,
   build 1.5.0 and dependencies). Put it on `PYTHONPATH` and drive it with
   `.remedy-wt/r9_build_runner.py`, which runs `build --wheel --no-isolation
   --outdir <outdir> <srcdir>`; wheels and outdirs stay under `.remedy-wt/`. Do
   NOT pip-install and do NOT create a virtualenv — the permission layer refuses
   to execute an interpreter under `.remedy-wt/`.
6. The asset guard refuses a build with no `apps/ui/dist/index.html`, so write
   one into every probe tree first or the build fails for an unrelated reason.
7. Suite commands run in the PRIMARY checkout, never in a worktree, and SERIALLY
   — each starts only after the previous has ENDED (finding R-0518).
8. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
9. SIZE, measured at emission: 490 lines TOTAL — 267 prose, 223 slice including
   14 marker lines — against DECISION F085 D6's 490 total and D5's 400 prose.
   Re-measure both from the COMMITTED C0a file and report your readings; a
   disagreement with these numbers is what makes drift visible.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `git worktree list` exactly 1 line at the
    handback; `.agent/STOP` absent, re-read from disk before C0a and again at the
    handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r12.md`, the committed
    `.agent/authored/f086-r12.md` and the committed `.agent/last_block.md` are
    all three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters,
    never elided — plus the byte count and the line count. An elided digest
    cannot be re-derived and a mistranscribed one is invisible: that is finding
    R-0581, and every digest ordered below is reported in full for that reason.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN12 slice extracted
    from the COMMITTED `.agent/authored/f086-r12.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to FIND0581
    followed immediately by RECORD10, concatenated in that order. Report the
    remainder's full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST AGREE. Extract twice — once by
    PARAGRAPH (split on blank lines; a paragraph counts when it STARTS with
    `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and
    `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Report the symmetric difference of the
    HEAD registered set against the `ee22186c` set as the SET itself; it must be
    exactly `['R-0581']`. The reviewer measured 163 / 2 / 161 at `ee22186c` under
    both, so HEAD must read 164 registered / 2 resolved / 162 open under both.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md`, `hatch_build.py`, `apps/cli/version_report.py` and
    `tests/test_build_revision.py` at HEAD each contain 0 lines beginning
    `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<` substrings.

G7  THE LEDGER CARRIES A VERDICT FOR EVERY REVIEWED ROUND OF THIS BRANCH. Count
    the paragraphs in `.agent/live_review.md` beginning `Gate: ` and report the
    count with the round each names. At `ee22186c` the reviewer measured 9,
    naming R3 through R11; C2 adds the tenth, so HEAD must read 10 and the added
    one must name R12. R12's OWN entry is absent by construction and that absence
    is the terminator, not a gap — do NOT add one.

G8  THE CODE IS THE SLICE. `hatch_build.py` and `tests/test_build_revision.py` at
    HEAD are each byte-equal to their slice; report both full sha256s and line
    counts, and confirm `tests/test_build_revision.py` is ABSENT at `ee22186c` by
    `git ls-tree`. For `apps/cli/version_report.py` prove ORDERED EQUALITY: the
    file at HEAD equals the blob at `ee22186c` with its single occurrence of
    VERFROM replaced by VERTO — construct the expected bytes and compare, do not
    count occurrences. Report that VERFROM occurs 1x in the base blob and 0x at
    HEAD, and VERTO 0x at the base and 1x at HEAD.

G9  THE WHEEL CARRIES THE REVISION AND THE READER FINDS IT — GREEN. In a worktree
    at HEAD sited OUTSIDE this repository, with `apps/ui/dist/index.html` written
    in, build a wheel per constraints 4-6 and report the build's real exit code.
    From the wheel report its total member count, the FULL list of members whose
    name contains `REVISION` — exactly
    `['remedy-0.1.0.dist-info/extra_metadata/REVISION']` — and that member's
    exact bytes alongside the worktree's own `git rev-parse HEAD`, so the reader
    can compare them and not only you. Then unpack the wheel and build
    `importlib.metadata.PathDistribution(<dir>/remedy-0.1.0.dist-info)`: report
    `read_text(apps.cli.version_report.REVISION_METADATA_FILE)`, which must be
    that revision, and `read_text("REVISION")`, which must be None — the control
    making C4 necessary rather than cosmetic, the bare name being what the base
    reads and what a real wheel does not answer.

G10 THE DEFECT REPRODUCES AT THE BASE — RED CONTROL. Repeat G9 in a SECOND
    worktree at `ee22186c`, unmodified, same asset stand-in and toolchain. Report
    its build exit code, member count, the full list of members whose name
    contains `REVISION` — which must be the EMPTY list — and that
    `read_text("REVISION")` over that wheel is None. A base build that produced a
    REVISION member, or that failed to build, means the control did not run: say
    so and hand off. Remove both worktrees and report `git worktree list` after.

G11 THE TESTS PASS AND THEY CAN FAIL. Run `python3 -m pytest
    tests/test_build_revision.py tests/test_packaging_smoke.py
    tests/cli/test_version_report.py -q -rf` in the PRIMARY checkout → report the
    real exit code and pass count. Then in a THROWAWAY worktree only, take these
    two mutations one at a time, each reverted before the next, reporting the
    pass/fail counts for each: (i) in `hatch_build.py` replace the two lines
    `    if revision is None:` / `        return {}` with `    if False:` /
    `        return {}`; (ii) in `apps/cli/version_report.py` set
    `REVISION_METADATA_FILE` back to `"REVISION"`. Each must turn at least one
    test RED. Before each edit report that the replaced byte string occurs 1x in
    its named file; after the last revert report that worktree's `git status
    --porcelain`, so the restoration is measured and not assumed.

G12 NO REGRESSION, ROUND GATE SUITE AND CANARY. Three runs in the PRIMARY
    checkout, each started only after the previous ENDED; state that none
    overlapped, and report each real exit code and pass count. (a) `python3 -m
    pytest tests/test_grouped_cli.py tests/cli/test_cli_ux.py -q`, the entry
    point this round's reader is wired into. (b) `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed.
    (c) `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.

G13 LINT DID NOT GET WORSE. Run `python3 -m ruff check hatch_build.py
    apps/cli/version_report.py tests/test_build_revision.py` at HEAD, and the
    same over the two paths that exist at `ee22186c` in a worktree. Report both
    exit codes and the MULTISET of rule codes each reported. The HEAD multiset
    may not contain any code more often than the base multiset does; a path new
    at HEAD contributes to HEAD only and must contribute 0 codes. Do not demand
    exit 0 of the base.

G14 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `ee22186c..HEAD` BEFORE C6, one line each;
    none may exceed 500. Report C6's own count in the round report.

G15 HISTORY. Every commit in `ee22186c..HEAD` has exactly one parent, the chain
    is linear, and `git reflog` over this round shows only `commit:` entries — no
    amend, rebase, reset, force-push. Report the chain.

G16 PATH SET. `git diff --name-only ee22186c..HEAD`, measured before C6, is
    exactly the paths constraint 2 lists other than `.agent/handoff.md`. Report
    the post-C6 set in the round report. Confirm `pyproject.toml` and every path
    under `packages/`, `docs/` and `scripts/` are ABSENT, and confirm with
    `git ls-tree ee22186c` that all four EXIST at the base, so the clause forbids
    something real.

G17 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report it verbatim; merge nothing.

Handback:
Completion report plus a rewritten `.agent/handoff.md`. Push after C5 and again
after C6. Report every gate with its REAL exit code and output — "green" as a
word is a finding. If a gate is red, say so plainly with the raw output and hand
off; never repair a red gate by changing what it measures.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN12>>>
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
R12, this round: close T002. The wheel now embeds the revision it was built
from, and `apps/cli/version_report.py` reads it back at the path hatchling
actually writes. Also records the R11 verdict and registers R-0581.

## Next Steps
1. T003 — the release CI stage, the changelog and tag gate, the wheel-size
   budget and the seeded-failure tests.
2. Then the install smoke, the integration gate, and closure. The packaging
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
<<<END PLAN12>>>

<<<SLICE FIND0581>>>

- R-0581 — Medium — AN ELIDED DIGEST IS AN UNCHECKABLE DIGEST, AND ONE OF THEM WAS WRONG. F086 R11's G2 ordered the transport property proved and its sha256 REPORTED; the handback at `ee22186c` reports it as `c76d6b4f…f9ff257fc2`, while the real sha256 of the three byte-equal files is `c76d6b4feef8870cb1b65284662cb0da375cfbf84baa14ba99ef63f1fa257fc2`, whose last ten characters are `f1fa257fc2` and not `f9ff257fc2`. The property itself HOLDS — the reviewer re-derived it at R12 and the three files are byte-equal at 21640 B over 320 lines — so this is a defect in the evidence record, not in the transport. It matters because a digest exists only to let the next reader re-derive it: a reader who recomputes and gets a different tail cannot tell a transcription slip from a real transport failure, and must re-open a question that was actually settled. TWO CAUSES, BOTH THE REVIEWER'S. First, the gate is a SHAPE gate — "report the sha256" is satisfied by any 64-character string, so no reading of it can fail on a wrong one, which is the R-0561 class again. Second, the block's own convention writes digests ELIDED with a `…`, and an elided digest cannot be re-derived at all: 54 of the 64 characters are simply gone, so even a diligent reader has nothing to compare. The other two digests in the same handback, `…72648680` and `…dbea9d0f`, do match, which is what makes this a slip rather than a systematic error and is exactly why no human reading could have caught it. FIX, and it is in this block: every gate that orders a digest orders it IN FULL, all 64 hex characters, never elided — R12's G2, G3, G4 and G8 all say so. The stronger form, for a gate that can afford it, is to order the equality property rather than the value, since an equality can be red. OPEN.
<<<END FIND0581>>>

<<<SLICE RECORD10>>>

Gate: R12 — the R11 entry. R11 PASSED, with one finding, R-0581, registered against the reviewer's own gate text. Every gate its block ordered was re-executed by the reviewer over `dea9dc2f..ee22186c` rather than read from the handback, and every reading reproduces. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original `.remedy-wt/f086-r11.md`, the committed `.agent/authored/f086-r11.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 c76d6b4feef8870cb1b65284662cb0da375cfbf84baa14ba99ef63f1fa257fc2, 21640 B, 320 lines — and that full digest is the point of R-0581, because the handback reports its tail as `f9ff257fc2` where the true tail is `f1fa257fc2`. THE SLICES LANDED BYTE-EXACT: `.agent/plan.md` equals PLAN11 at sha256 cc7fefe26153cb0662ccbb06b5f5178c6e0f6d38e3dbcc3e72e5b66372648680 over 43 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob with the 2-line remainder equal to RECORD9 at sha256 34a16d52c183c4d905d14b4ea63042bb4257cbf3683a61339d4d609fdbea9d0f; and the C3 handoff blob is a byte-exact PREFIX of the file at HEAD whose 58-line remainder is exactly the VERDICT slice at sha256 0ef26000679d3b5eafcfed0a0f211f92969b90e1e16fc0449269e7f85e0278f0. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the three written state files. THE LEDGER DID NOT MOVE, which is what a round registering nothing must show: paragraph and line-anchored extractions AGREE at `dea9dc2f` and at `ee22186c`, both reading 163 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 161 open, and the symmetric difference of the two registered sets across the range is EMPTY under both — while the same extractor reads `['R-0580']` across `419fb683..e7c219cc`, the negative control that proves it can see a difference at all. THE VERDICT LANDED WHERE R-0571 SAYS IT MUST: the ledger's `Gate: ` paragraphs go from 8 at `dea9dc2f` naming R3 through R10 to 9 at HEAD, the added one naming R11, and the seven mandated handback headings are present in order at lines 6, 10, 37, 44, 87, 94 and 104 — measured line-anchored, because a substring search for `## Next` matches the quoted `## Next Steps` inside G3's own text and reports the headings out of order. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout: 160 passed for the four state readers, exit 0, ending 13:05:05, and 42 passed for the canary, exit 0, starting 13:05:08. THE HYGIENE HELD: five paths, all under `.agent/`, over six single-parent commits inserting 320, 201, 12, 2, 68 and 58 lines, none over 500; `pyproject.toml`, `hatch_build.py` and every path under `apps/`, `packages/`, `tests/`, `docs/` and `scripts/` are absent from the range and all seven exist at the base. THE ONE DECLARED DEVIATION IS NOT A FINDING: `.agent/handoff.md` stands at 165 lines over the 100-line cap, declared under AGENTS.md DECISION D15 with its cause named — the mandated session verdict — and every section present.
<<<END RECORD10>>>

<<<SLICE HATCH>>>
"""Packaging-time guard and build-info embedding for the remedy wheel.

THE GUARD: `artifacts = ["apps/ui/dist/**"]` carries the built UI but is SILENT
when that directory is absent — measured at 419fb683, such a build exits 0 and
ships zero UI files, which DECISION F086 D1 part (b) forbids.

THE EMBEDDING: `remedy --version` reports the revision a wheel was built from
(DECISION F086 D2). hatchling prefixes every hook-supplied extra-metadata entry
with `extra_metadata/` inside `.dist-info`, so a hook CANNOT produce
`<dist-info>/REVISION`; the wheel carries `<dist-info>/extra_metadata/REVISION`
and `apps/cli/version_report.py` reads back there. ONE hook class, because
`load_plugin_from_script` refuses a script defining two subclasses. Both rules
live in plain functions so the suite can exercise them without the build backend,
and the revision never touches the source tree — a generated file there survives
the build and reports a revision nobody built.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

try:  # the build backend supplies hatchling; the test environment need not
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # pragma: no cover - only the real wheel build takes this path
    BuildHookInterface = object  # type: ignore[assignment,misc]

FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"
REVISION_WHEEL_NAME = "REVISION"


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


def resolve_source_revision(root: str | Path) -> str | None:
    """Return the git revision of the tree at `root`, or None when it has none.

    None is not a failure: an sdist unpacked outside version control has no
    revision, and DECISION F086 D2 requires an honest `dev` over an invented sha.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def build_revision_metadata(root: str | Path, staging: str | Path) -> dict[str, str]:
    """Write the revision under `staging` and return its extra-metadata map.

    The map is EMPTY when no revision resolves, so the wheel carries no REVISION
    member at all and `remedy --version` reports `dev` rather than a guess.
    """
    revision = resolve_source_revision(root)
    if revision is None:
        return {}
    written = Path(staging) / REVISION_WHEEL_NAME
    written.write_text(f"{revision}\n", encoding="utf-8")
    return {str(written): REVISION_WHEEL_NAME}


class RemedyBuildHook(BuildHookInterface):
    """Refuse a wheel with no built UI, and embed the revision it was built from."""

    PLUGIN_NAME = "remedy-build"

    def initialize(self, version, build_data):
        assert_frontend_assets_built(self.root)
        build_data["extra_metadata"].update(
            build_revision_metadata(self.root, tempfile.mkdtemp())
        )
<<<END HATCH>>>

<<<SLICE VERFROM>>>
REVISION_METADATA_FILE = "REVISION"
<<<END VERFROM>>>

<<<SLICE VERTO>>>
# hatchling prefixes every hook-supplied extra-metadata entry with
# `extra_metadata/` inside `.dist-info`, so a real wheel answers here and returns
# None for a bare `REVISION` — measured on a built wheel, not inferred.
# `hatch_build.py` writes the other half of this pair.
REVISION_METADATA_FILE = "extra_metadata/REVISION"
<<<END VERTO>>>

<<<SLICE TESTS>>>
"""Tests for the build revision a wheel carries (F086 T002, DECISION F086 D2).

The wheel-level proof needs the build backend and lives in the round's gates.
These pin what is reachable without hatchling: the revision comes from the tree
being built, an absent revision writes nothing rather than a guess, and reader
and writer name the same path.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apps.cli import version_report
from hatch_build import (
    REVISION_WHEEL_NAME,
    build_revision_metadata,
    resolve_source_revision,
)


def _seed_repository(root: Path) -> str:
    """Make `root` a git repository with one commit; return its HEAD sha."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "seed.txt").write_text("seed\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    git = ["git", "-C", str(root), "-c", "user.name=remedy-test",
           "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
    subprocess.run([*git, "add", "seed.txt"], check=True)
    subprocess.run([*git, "commit", "-qm", "seed"], check=True)
    head = subprocess.run([*git, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True)
    return head.stdout.strip()


@pytest.mark.subprocess
class TestRevisionEmbedding:
    """The embedded revision is the revision of the tree being built, or nothing."""

    def test_a_resolved_revision_is_written_and_mapped(self, tmp_path):
        source = tmp_path / "source"
        head = _seed_repository(source)
        staging = tmp_path / "staging"
        staging.mkdir()
        mapping = build_revision_metadata(source, staging)
        written = staging / REVISION_WHEEL_NAME
        assert mapping == {str(written): REVISION_WHEEL_NAME}
        assert written.read_text() == f"{head}\n"

    def test_no_revision_writes_nothing_and_maps_nothing(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        assert resolve_source_revision(plain) is None
        assert build_revision_metadata(plain, staging) == {}
        assert list(staging.iterdir()) == []


@pytest.mark.unit
class TestReaderAndWriterAgreeOnOnePath:
    """The path the build writes is the path `remedy --version` reads back."""

    def test_the_reader_carries_hatchlings_extra_metadata_prefix(self):
        # Drop the prefix on either side of this equality and an installed wheel
        # reports `dev` forever while every mock in the suite still passes.
        assert version_report.REVISION_METADATA_FILE == (
            f"extra_metadata/{REVISION_WHEEL_NAME}"
        )
<<<END TESTS>>>
