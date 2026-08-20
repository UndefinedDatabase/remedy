── STEP R15 — F086 Release capability (the DATA and the CALLER) ──

Goal:
Make the release gate refuse something real. R13 landed `refuse_release` and its
seeded-failure tests, and said so plainly: nothing calls it, so it refuses
nothing. This round supplies the two missing halves — the DATA (`CHANGELOG.md`,
carrying a section for the version `pyproject.toml` declares) and the CALLER
(`scripts/release_gate_check.py`, observing a release from the built wheel's own
filename, the changelog on disk and the wheel's real size) — plus tests driving
both over THIS repository's values rather than over fixtures. DELIBERATELY LEFT
OUT, so no reader mistakes a bounded round for a finished one: the manual-trigger
workflow, which is R16's, for block budget and not for doubt. PLAN15 says so.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r15.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN15 slice, whole file
  C2  append FIND0583 and then RECORD13 to `.agent/live_review.md`
  C3  `CHANGELOG.md` := the CHANGELOG slice, a NEW file
  C4  `scripts/release_gate_check.py` := the RUNNER slice, a NEW file
  C5  `tests/orchestration/test_release_gate_wiring.py` := the TESTS slice, NEW
  C6  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 item 23 requires the plan to advance before any commit
touching the finding ledger; C2 puts the finding on disk before the work per §4
item 4(a); C3 and C4 precede C5 because the tests read both files.

Base:
This round starts from `6f5a589a`, the tip of `feature/f086-release-capability`
and the commit that appended R14's session verdict. Every range gate names that
SHA. Stay on the branch: do NOT create one, merge, or open a PR.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers
and apply it byte-verbatim; no marker line ever reaches a target file. PLAN15,
CHANGELOG, RUNNER and TESTS are COMPLETE files, each including its single trailing
newline. FIND0583 and RECORD13 are EOF-APPENDS to `.agent/live_review.md`: pure
concatenation, each slice's own leading blank line INSIDE the slice, nothing
prepended, nothing stripped. No FROM/TO pair exists in this block, so no pair
shape is claimed and no FROM-count is orderable.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `6f5a589a`, `git branch --show-current`
   is `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r15.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r15.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r15.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN15 slice, byte-verbatim, whole file. Alone.

3. C2 — append FIND0583 to `.agent/live_review.md`, then append RECORD13, in
   that order, under the append convention. ONE commit. FIND0583 registers
   R-0583; RECORD13 is the reviewer's R14 verdict and registers no id.

4. C3 — create `CHANGELOG.md` at the repository root := the CHANGELOG slice.
   Commit alone. Do not register it in `docs/README.md`, which indexes `docs/`.

5. C4 — create `scripts/release_gate_check.py` := the RUNNER slice. Commit
   alone. Do not make it executable, do not add a `[project.scripts]` entry, and
   do not import it from any production module: the workflow calls it, nothing
   else does.

6. C5 — create `tests/orchestration/test_release_gate_wiring.py` := TESTS. Alone.

7. C6 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 6f5a589a..<HEAD>`; write the literal token `HEAD`, this
   branch's convention from R10 onward, because a handoff cannot name the SHA of
   the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT — one line per gate:
   its number, what it measured in a clause, and its real colour or value. This
   is the R-0582 repair that R14 proved works; G15 measures it. The FULL
   transcript goes in your ROUND REPORT, which no cap binds.
   `Next` names, in order, the next session's first two actions: re-read
   `.agent/STOP` from disk (Phase 1 rule 1), then the Open PR Gate (rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r15.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `CHANGELOG.md`, `scripts/release_gate_check.py`,
   `tests/orchestration/test_release_gate_wiring.py`, and `.agent/handoff.md` at
   C6. Not `pyproject.toml`, not `hatch_build.py`, not
   `packages/orchestration/release_gate.py`, not `.github/workflows/ci.yml`, and
   nothing under `apps/` or `docs/`.
3. Do not write a verdict of your own anywhere — in the handoff, in a commit
   message, or in your report. RECORD13 is the reviewer's text. Reporting what a
   gate MEASURED is your job; ruling on a round is not.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback. This round adds exactly ONE disposable worktree, for G9, G10
   and G11's control; it is removed and pruned before the handback, where `git
   worktree list` reads one line. Every other gate command runs in the PRIMARY
   checkout, and suites run SERIALLY — the second starts only after the first
   has ENDED (R-0518).
   The fake wheel G10 needs is written under that WORKTREE's `dist/`, which
   `.gitignore` matches, so its porcelain stays empty too.
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
6. SIZE, measured at emission on the final bytes: this block is 489 lines TOTAL
   — 244 prose and 245 slice including its 12 marker lines — against DECISION
   F085 D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED
   C0a file and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r15.md`, the committed
    `.agent/authored/f086-r15.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN15 slice extracted
    from the COMMITTED `.agent/authored/f086-r15.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains
    `## Goal`, `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to FIND0583
    followed by RECORD13, in that order. Report its full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and
    `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and
    the two registered id SETS must be EQUAL. Expected at HEAD: 166 registered,
    2 resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:`, 164 open.
    Report the symmetric difference of the HEAD registered set against the
    `6f5a589a` set AS THE SET; it must be `['R-0583']`. CONTROL: the SAME
    extractor over `3351878d..a662abcc` must read `['R-0582']`.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md`, `CHANGELOG.md`, `scripts/release_gate_check.py` and
    `tests/orchestration/test_release_gate_wiring.py` at HEAD each contain 0
    lines beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<`.

G7  THE THREE NEW FILES ARE THEIR SLICES, AND THEY ARE NEW. `CHANGELOG.md`,
    `scripts/release_gate_check.py` and
    `tests/orchestration/test_release_gate_wiring.py` at HEAD are byte-equal to
    CHANGELOG, RUNNER and TESTS respectively, extracted from the COMMITTED C0a
    file. Report each one's full sha256, byte count and line count. Confirm with
    `git ls-tree 6f5a589a -- <path>` that each is ABSENT at the base, so each of
    those commits is a creation and not an edit.

G8  THE WIRING SUITE AND THE GATE SUITE, in the PRIMARY checkout:
    `python3 -m pytest tests/orchestration/test_release_gate_wiring.py
    tests/orchestration/test_release_gate.py -q -rf` → exit 0, 21 passed.

G9  RED PROOF — THE TESTS READ THE REAL CHANGELOG. In the disposable worktree at
    the round's HEAD, in `CHANGELOG.md` and in that file only, first count the
    exact line `## [0.1.0] - 2026-08-20`, which must be 1; replace that one line
    with `## [0.1.0-broken] - 2026-08-20`; run `python3 -m pytest
    tests/orchestration/test_release_gate_wiring.py -q -rf` THERE. It must report
    exactly 3 failed and 6 passed, naming
    `test_the_declared_version_has_a_non_empty_section`,
    `test_this_repository_is_refused_for_no_reason_at_all` and
    `test_a_sound_release_exits_zero`. Revert, re-run, report 9 passed at exit 0
    and that worktree's porcelain EMPTY. Report the names you actually saw.

G10 THE CALLER RUNS AS A PROGRAM. In the worktree, write a file of 2040197 bytes
    at `dist/remedy-0.1.0-py3-none-any.whl`, then run `python3
    scripts/release_gate_check.py --tag v0.1.0 --wheel
    dist/remedy-0.1.0-py3-none-any.whl --ci-status success` → exit 0, stdout
    exactly `release v0.1.0 may proceed`. Then the same command with `--tag
    v9.9.9 --ci-status failure` → exit 1 and exactly two stderr lines, each
    beginning `REFUSED: `, one naming CI and one the tag. Report both
    invocations' real exit codes and real output.

G11 RUFF, SCOPED TO WHAT THIS ROUND ADDS. `python3 -m ruff check
    scripts/release_gate_check.py
    tests/orchestration/test_release_gate_wiring.py` in the PRIMARY checkout →
    exit 0 with an EMPTY rule-code multiset. There is no base reading to compare
    against, both paths being absent at `6f5a589a` (G7 measures that); say so
    rather than inventing one. CONTROL, in the worktree only: insert the line
    `import json` directly after the line `import argparse` in
    `scripts/release_gate_check.py`, counted 1x in that file first; re-run the
    same ruff command there, report exit 1 naming `F401`, revert, report exit 0.

G12 CANARY AND THE STATE READERS, in the PRIMARY checkout, serially: `python3 -m
    pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed;
    then `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed. State that they did not overlap.

G13 HISTORY AND COMMIT SIZE. Every commit in `6f5a589a..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Report the chain, and
    with it the INSERTION count — the `+` column of `git show --numstat` — for
    every commit BEFORE C6, one each; none over 500. C6's own goes in the report.

G14 PATH SET. `git diff --name-only 6f5a589a..HEAD`, measured before C6, is
    exactly the seven paths constraint 2 lists other than `.agent/handoff.md`.
    Report the post-C6 set in the round report. Confirm `pyproject.toml`,
    `hatch_build.py`, `packages/orchestration/release_gate.py` and
    `.github/workflows/ci.yml` are ABSENT from the range and all four EXIST at
    `6f5a589a` under `git ls-tree`, so the clause forbids something real.
    Report separately that `.github/workflows/release.yml` is absent from the
    range AND at `6f5a589a`: it is R16's work, and saying so keeps the clause
    from reading as a guard over a live file (R-0559).

G15 THE HANDBACK STAYS UNDER ITS CAP. Report the line count of
    `.agent/handoff.md` at HEAD. It must be AT MOST 100, the AGENTS.md cap, with
    NO DECISION D15 overage declared, and hold all seven mandated headings of
    docs/agents/handback_template.md in the template's order. R14 reached 98 by
    moving the transcript to the round report; if yours exceeds 100, declare the
    overage plainly rather than hiding it.

G16 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report it verbatim; merge nothing.

Handback:
A FULL completion report — every gate, its real command, its real exit code, its
output and every digest at 64 characters — plus the SHORT `.agent/handoff.md` C6
writes. Push after C5 and again after C6. "Green" as a word is a finding; a red
gate is reported plainly, with its raw output, and the round hands off.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN15>>>
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
R15, this round: the DATA and the CALLER. `CHANGELOG.md` with a section for the
version `pyproject.toml` declares, `scripts/release_gate_check.py` observing a
release from the built wheel's filename, the changelog on disk and the wheel's
own size, and tests driving both over this repository's real values. From here
the gate refuses something real.

## Next Steps
1. R16 — the TRIGGER: a manual-trigger `.github/workflows/release.yml` that
   builds the wheel, reads the CI run's conclusion for the commit and calls
   `scripts/release_gate_check.py`, with text guards of the kind
   `tests/orchestration/test_ci_workflow.py` already applies to `ci.yml`. R15
   left it out for block budget, not doubt: DECISION F085 D6 caps a block at
   490 lines and that slice did not fit beside the caller's.
2. Then the install smoke, the integration gate, and closure. The packaging
   ist-doc is written at closure, when the built state stops moving.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so the round that writes it must name its
  execution host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
<<<END PLAN15>>>

<<<SLICE FIND0583>>>

- R-0583 — Low — A ROUND THAT ENDS A SESSION IS NOT A ROUND THAT ENDS A BRANCH, AND R14's OWN RECORD CONFLATED THEM. The reviewer's session verdict appended to `.agent/handoff.md` at `6f5a589a` rules R14 `terminator; §4 item 13 gives it no ledger entry`. That item of docs/agents/planner_reviewer_prompt.md governs THE LAST ROUND OF A BRANCH, and R14 was the last round of a SESSION: the same file at the same commit names R15's work under `Next`, and `.agent/plan.md` at `fbfddb0a` names it under `## Next Steps`, so the branch demonstrably continued. WHY IT MATTERS rather than being a wording slip: the sentence asserts that R14 will NEVER receive a ledger entry, and a later reader who believed it would leave the finding ledger a permanent hole at exactly the round that repaired R-0582 — the R-0228 class, a round line positively claiming a review cannot happen, arriving inverted. It also handed R14 to the next session with no verdict at all, neither PASS nor FAIL but a classification, which is the stranding DECISION F085 D9 exists to prevent. Nothing was ultimately lost, because Phase 1 rule 4 of docs/agents/self_drive_protocol.md forces the next session to review an ungated handback before planning new work, and it did. COUNTER-MEASURE, and it is narrow: the terminator carve-out is claimed only by a round whose own bundle CREATES the branch's pull request, because that is the only round after which no further round can record anything; every other session-closing round issues a PASS or a FAIL and leaves it to be recorded, exactly as D9 already requires. REGISTERED AGAINST THE REVIEWER, not the worker: constraint 3 of the R14 block forbade the worker to write any verdict of its own, and it wrote none.
<<<END FIND0583>>>

<<<SLICE RECORD13>>>

Gate: R15 — the R14 entry. R14 PASSED, with ONE finding — R-0583, against the reviewer, registered by this round's own FIND0583 slice. Every gate its block ordered was re-executed by the reviewer over `a662abcc..6f5a589a` rather than read from the handback, and every reading reproduces. THE R-0582 REPAIR WORKED AND ITS GATE COULD HAVE FAILED: `.agent/handoff.md` is 98 lines at `6f5a589a`, under the 100-line AGENTS.md cap with no DECISION D15 overage declared, against 113 at `dea9dc2f`, 165 at `ee22186c`, 223 at `3351878d` and 222 at `a662abcc` — all four re-derived by the reviewer from each commit's own blob rather than copied from the handback — and all seven mandated headings of docs/agents/handback_template.md are present in the template's order, so the transcript moved out and no section was dropped. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r14.md`, the committed `.agent/authored/f086-r14.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 8960302f4ce113011a0157dd8f191ef43c7cc35c99ea2e9952520c03f50bf420, 23468 B, 330 lines, which is the size the block declares of itself. EVERY SLICE LANDED BYTE-EXACT: `.agent/plan.md` equals PLAN14 at 165f3a3ecf00f0080b27504fbbeca4d3c3b4137d6d8fd29cc450bd6fc4dc82b9 over 43 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 2-line remainder equals RECORD12 at afa1fe5da0e8580ffd4ef0c3b7c37bc2bf908bdc91a17386315be4be367b86e6; and `.agent/handoff.md` as committed by C3 is a byte-exact PREFIX of the file at HEAD whose 43-line remainder equals VERDICT at 242d697684d2a85af5689baaa3fc0caef1a53ca5473e2d931e68289d177364c9. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` or `.agent/handoff.md`. THE LEDGER DID NOT MOVE, WHICH IS WHAT THE ROUND CLAIMED: both extractions agree at 165 registered / 2 resolved / 0 duplicate ids / 0 unregistered resolutions / 0 `Landed:` / 163 open at `6f5a589a` with the two registered SETS equal, the symmetric difference against `a662abcc` is empty, and the reviewer's control over `3351878d..a662abcc` reads exactly `['R-0582']`, so the extractor can see a difference rather than being blind. THE `Gate: ` PARAGRAPHS go from 11 to 12 and the added one names R14. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the primary checkout: 160 passed for the four state readers and 42 for the canary, each exit 0. THE HYGIENE HELD: five paths, all under `.agent/`, over six single-parent commits inserting 330, 221, 10, 2, 34 and 43 lines, none over 500 and no DECISION F104 D1 exemption invoked; `pyproject.toml` and `hatch_build.py` are absent from the range and both exist at `a662abcc`, and no path under `apps/`, `packages/`, `tests/`, `docs/` or `scripts/` appears in it. WHERE R14 WENT WRONG is in none of that: it is the one sentence in its own appended verdict that rules itself a branch terminator, which R-0583 records and to which this entry is the counter-example.
<<<END RECORD13>>>

<<<SLICE CHANGELOG>>>
# Changelog

All notable changes to Remedy are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Remedy follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is DATA the release gate reads: `packages/orchestration/release_gate.py`
refuses any release whose version has no section here, or whose section is empty.
Bumping the version in `pyproject.toml` without adding a section below therefore
fails the gate rather than shipping an unexplained release.

## [Unreleased]

## [0.1.0] - 2026-08-20

### Added
- Remedy installs like a normal tool: a `pip install` of the wheel puts the
  `remedy` CLI on PATH with the built UI assets bundled (T2_F086 T001).
- `remedy --version` reports the distribution version, the revision embedded at
  build time, the Python version and the platform. A checkout with no embedded
  revision reports `dev` rather than inventing a sha (T2_F086 T002).
- A release gate that refuses on red CI, on a tag that does not match the
  distribution version, on a missing or empty changelog section, and on a wheel
  over its size budget (T2_F086 T003).
<<<END CHANGELOG>>>

<<<SLICE RUNNER>>>
#!/usr/bin/env python3
"""Observe a proposed release and refuse it for every reason it must be refused.

`release_gate.refuse_release` DECIDES; this script OBSERVES. It reads the version
out of the built wheel's own FILENAME, the changelog off disk and the wheel's
size from the file itself, so every value the gate judges comes from the artifact
being released rather than from a second declaration that could drift out of sync
with it (DECISION F086 D2). Remedy deliberately does not upload anything here and
holds no credential: publishing stays a HUMAN command (T2_F086 Orchestrator).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[1])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from packages.orchestration.release_gate import ReleaseRequest, refuse_release  # noqa: E402

DEFAULT_CHANGELOG = Path(_REPO_ROOT) / "CHANGELOG.md"
CI_SUCCESS_CONCLUSION = "success"


def version_from_wheel_name(wheel: Path) -> str:
    """Return the distribution version encoded in a wheel's filename.

    A wheel is named `<name>-<version>-<python>-<abi>-<platform>.whl`, so the
    version is its second hyphen-separated field. Reading it HERE ties the gate to
    the artifact under release: a wheel built from some other version cannot pass
    by agreeing with a declaration the build never read.
    """
    fields = wheel.name.split("-")
    if not wheel.name.endswith(".whl") or len(fields) < 5:
        raise ValueError(f"not a wheel filename: {wheel.name}")
    return fields[1]


def observe_release(tag: str, wheel: Path, changelog: Path, ci_status: str) -> ReleaseRequest:
    """Build the request the gate judges out of what is really on disk."""
    return ReleaseRequest(
        tag=tag,
        version=version_from_wheel_name(wheel),
        changelog=changelog.read_text(encoding="utf-8"),
        wheel_bytes=wheel.stat().st_size,
        ci_green=ci_status == CI_SUCCESS_CONCLUSION,
    )


def main(argv: list[str] | None = None) -> int:
    """Print every refusal reason; return 1 when there is one and 0 when there is none."""
    parser = argparse.ArgumentParser(description="Refuse a release that is not fit to ship.")
    parser.add_argument("--tag", required=True, help="the tag being released")
    parser.add_argument("--wheel", required=True, type=Path, help="the built wheel")
    parser.add_argument("--ci-status", required=True, help="the CI run's conclusion")
    parser.add_argument("--changelog", type=Path, default=DEFAULT_CHANGELOG)
    args = parser.parse_args(argv)
    reasons = refuse_release(
        observe_release(args.tag, args.wheel, args.changelog, args.ci_status)
    )
    for reason in reasons:
        print(f"REFUSED: {reason}", file=sys.stderr)
    if not reasons:
        print(f"release {args.tag} may proceed")
    return 1 if reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
<<<END RUNNER>>>

<<<SLICE TESTS>>>
"""The release gate is WIRED to this repository's own values (T2_F086 T003).

`test_release_gate.py` proves the gate's DECISIONS against seeded requests. These
prove the other half: that those decisions are reached over the real changelog,
the real declared version and a real wheel's real size. A gate nothing calls
refuses nothing, which is the state R13 left behind on purpose.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration.release_gate import changelog_section, refuse_release
from scripts.release_gate_check import main, observe_release, version_from_wheel_name

REPO_ROOT = Path(__file__).resolve().parents[2]
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
ABSENT_VERSION = "0.0.0"


def declared_version() -> str:
    """The version `pyproject.toml` declares — the one place it is written (D2)."""
    found = re.search(r'^version = "([^"]+)"', PYPROJECT_PATH.read_text(), re.MULTILINE)
    assert found is not None, "pyproject.toml declares no version"
    return found.group(1)


def build_wheel(directory: Path, version: str, size: int) -> Path:
    """A file named like a real wheel of `version` and exactly `size` bytes long."""
    wheel = directory / f"remedy-{version}-py3-none-any.whl"
    wheel.write_bytes(b"x" * size)
    return wheel


@pytest.mark.unit
class TestTheRealChangelogCoversTheRealVersion:
    def test_the_declared_version_has_a_non_empty_section(self):
        assert CHANGELOG_PATH.is_file(), CHANGELOG_PATH
        version = declared_version()
        body = changelog_section(CHANGELOG_PATH.read_text(), version)
        assert body is not None, f"CHANGELOG.md has no section for {version}"
        assert body.strip(), f"the CHANGELOG.md section for {version} is empty"

    def test_this_repository_is_refused_for_no_reason_at_all(self, tmp_path):
        version = declared_version()
        request = observe_release(
            f"v{version}", build_wheel(tmp_path, version, 1024), CHANGELOG_PATH, "success"
        )
        assert refuse_release(request) == ()


@pytest.mark.unit
class TestTheCallerObservesTheArtifact:
    def test_the_version_comes_from_the_wheel_filename(self, tmp_path):
        assert version_from_wheel_name(build_wheel(tmp_path, "9.9.9", 3)) == "9.9.9"

    def test_a_file_that_is_not_a_wheel_is_refused_rather_than_guessed(self, tmp_path):
        with pytest.raises(ValueError):
            version_from_wheel_name(tmp_path / "remedy-1.2.3.tar.gz")

    def test_the_wheel_size_is_read_from_the_file_not_declared(self, tmp_path):
        request = observe_release(
            "v1.2.3", build_wheel(tmp_path, "1.2.3", 4321), CHANGELOG_PATH, "success"
        )
        assert request.wheel_bytes == 4321


@pytest.mark.unit
class TestTheCallerExitsNonZeroSoAWorkflowStops:
    def _run(self, tmp_path, version, tag, ci_status):
        wheel = build_wheel(tmp_path, version, 1024)
        return main(["--tag", tag, "--wheel", str(wheel), "--ci-status", ci_status])

    def test_a_sound_release_exits_zero(self, tmp_path):
        version = declared_version()
        assert self._run(tmp_path, version, f"v{version}", "success") == 0

    def test_red_ci_exits_non_zero(self, tmp_path):
        version = declared_version()
        assert self._run(tmp_path, version, f"v{version}", "failure") == 1

    def test_a_version_with_no_changelog_section_exits_non_zero(self, tmp_path):
        assert self._run(tmp_path, ABSENT_VERSION, f"v{ABSENT_VERSION}", "success") == 1

    def test_every_reason_is_printed_not_only_the_first(self, tmp_path, capsys):
        assert self._run(tmp_path, ABSENT_VERSION, "v9.9.9", "failure") == 1
        assert capsys.readouterr().err.count("REFUSED: ") == 3
<<<END TESTS>>>
