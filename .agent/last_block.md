── STEP R13 — F086 Release capability (the release gate; record R12) ──

Goal:
Land T003's decision half: the release gate as a pure, testable module, with one
seeded-failure test per refusal reason the feature's Acceptance names — red CI,
tag/version mismatch, missing or empty changelog section, wheel-size budget
breach. It also records the R12 verdict and registers R-0582.

NOT in this round, and named so the next author does not have to infer the seam:
the repository's own `CHANGELOG.md` and the manual-trigger workflow that calls
this gate. The gate is a pure function over values a caller supplies, so it lands
and is proved on its own; the changelog is DATA the caller reads and belongs with
the caller. Until R14 the gate refuses nothing — stated in the plan, not left to
be discovered.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r13.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN13 slice, whole file
  C2  append FIND0582 then RECORD11 to `.agent/live_review.md`, in that order
  C3  create `packages/orchestration/release_gate.py` := the GATE slice
  C4  create `tests/orchestration/test_release_gate.py` := the TESTS slice
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. C2 appends the finding BEFORE the
gate paragraph, the order already on disk for R8's finding and R9's gate entry.
C4 follows C3 because its tests import the module.

WHY THE MODULE LIVES IN `packages/orchestration/`. That package already exists
and already holds `ci_stages.py`, the sibling piece of release machinery; a new
`packages/release/` would add a package directory and an `__init__.py` question
this round does not need to answer. The gate is NOT added to `CI_STAGES`: that
table is pytest-selection DATA, every entry being a marker expression plus a path
list, and this gate selects no tests at all.

Base:
This round starts from `3351878d`, the tip of `feature/f086-release-capability`.
Every range gate below names that SHA. Stay on the existing branch — do NOT
create one, do NOT run the Open PR Gate, do NOT open a PR. The branch stays
pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN13, GATE
and TESTS are COMPLETE files, each including its single trailing newline.
FIND0582 and RECORD11 are EOF-APPENDS: pure concatenation, each slice's own
leading blank line INSIDE the slice, nothing prepended, nothing stripped. This
block contains no FROM/TO pair.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `3351878d`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r13.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r13.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r13.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN13 slice, byte-verbatim, whole file. Commit
   alone.

3. C2 — append FIND0582 and then RECORD11 to `.agent/live_review.md` under the
   append convention, FIND0582 first, one commit for both. FIND0582 registers
   R-0582; RECORD11 is the reviewer's R12 verdict and registers no id.

4. C3 then C4 — one commit each, in that order, each slice byte-verbatim and
   whole file, nothing else in either. Both paths are NEW:
   `packages/orchestration/release_gate.py` beside `ci_stages.py`, and
   `tests/orchestration/test_release_gate.py`. Create no `__init__.py` and no
   directory that does not already exist — both parent directories do.

5. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 3351878d..<HEAD>`. Over the 100-line cap, declare the
   overage under AGENTS.md DECISION D15 and name its cause; drop no mandated
   section to meet it. Report your own C5 insertion count and the post-C5 path
   set in the ROUND REPORT, not in the file, because a handoff cannot measure the
   commit that writes it (§3 item 14). `Next` names, in order, the next session's
   first two actions: re-read `.agent/STOP` (Phase 1 rule 1), then the Open PR
   Gate (rule 2).

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r13.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `packages/orchestration/release_gate.py`,
   `tests/orchestration/test_release_gate.py`, and `.agent/handoff.md` at C5.
   `pyproject.toml`, `.github/workflows/ci.yml`, `hatch_build.py`,
   `apps/cli/version_report.py` and `packages/orchestration/ci_stages.py` are NOT
   in it: this round adds a module and wires nothing. `CHANGELOG.md` is NOT in it
   either — that file does not exist yet and this round does not create it.
3. `git status --porcelain` in the primary checkout is EMPTY at every commit and
   at the handback, and `git worktree list` is exactly one line at the handback.
   The mutation gate adds one worktree and removes it; a higher count while it
   exists is expected.
4. Suite commands run in the PRIMARY checkout, never in a worktree, and SERIALLY
   — each starts only after the previous has ENDED (finding R-0518).
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
6. SIZE, measured at emission: 490 lines TOTAL — 246 prose, 244 slice including
   10 marker lines — against DECISION F085 D6's 490 total and D5's 400 prose.
   Re-measure both from the COMMITTED C0a file and report your readings; a
   disagreement with these numbers is what makes drift visible.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `git worktree list` exactly 1 line at the
    handback; `.agent/STOP` absent, re-read from disk before C0a and again at the
    handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r13.md`, the committed
    `.agent/authored/f086-r13.md` and the committed `.agent/last_block.md` are
    all three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters,
    never elided — plus the byte count and the line count. Finding R-0581 is why
    every digest ordered below is reported in full.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN13 slice extracted
    from the COMMITTED `.agent/authored/f086-r13.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to FIND0582
    followed immediately by RECORD11, concatenated in that order. Report the
    remainder's full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST AGREE. Extract twice — once by
    PARAGRAPH (split on blank lines; a paragraph counts when it STARTS with
    `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and
    `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Report the symmetric difference of the
    HEAD registered set against the `3351878d` set as the SET itself; it must be
    exactly `['R-0582']`. The reviewer measured 164 / 2 / 162 at `3351878d` under
    both, so HEAD must read 165 registered / 2 resolved / 163 open under both.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md`, `packages/orchestration/release_gate.py` and
    `tests/orchestration/test_release_gate.py` at HEAD each contain 0 lines
    beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<` substrings.

G7  THE LEDGER CARRIES A VERDICT FOR EVERY REVIEWED ROUND OF THIS BRANCH. Count
    the paragraphs in `.agent/live_review.md` beginning `Gate: ` and report the
    count with the round each names. At `3351878d` the reviewer measured 10,
    naming R3 through R12; C2 adds the eleventh, so HEAD must read 11 and the
    added one must name R13. R13's OWN entry is absent by construction and that
    absence is the terminator, not a gap — do NOT add one.

G8  THE CODE IS THE SLICE. `packages/orchestration/release_gate.py` and
    `tests/orchestration/test_release_gate.py` at HEAD are each byte-equal to
    their slice; report both full sha256s and line counts, and confirm with
    `git ls-tree 3351878d` that both are ABSENT at the base.

G9  THE GATE REFUSES FOR EACH REASON AND ACCEPTS WHEN IT SHOULD. In the PRIMARY
    checkout run `python3 -m pytest tests/orchestration/test_release_gate.py -q
    -rf` → report the real exit code and pass count. Then, separately and OUTSIDE
    pytest, import `refuse_release` and report its ACTUAL return value for five
    requests built from an accepting one by changing one field each: (a)
    unchanged → `()`; (b) `ci_green=False`; (c) a tag that is not the version;
    (d) a changelog with no section for the version; (e) `wheel_bytes` one byte
    over `WHEEL_SIZE_BUDGET_BYTES`. PRINT EACH RETURNED TUPLE VERBATIM. Each of
    (b) to (e) must be non-empty and (a) must be empty. Printing the tuples is
    the point: a count of refusals cannot show WHICH rule fired, and a rule that
    fires for the wrong reason still raises the count.

G10 THE TESTS CAN FAIL. In a THROWAWAY worktree only, take these two mutations
    to `packages/orchestration/release_gate.py` one at a time, each reverted
    before the next, and report the pass/fail counts for each. (i) Replace the
    single line `    if request.wheel_bytes > WHEEL_SIZE_BUDGET_BYTES:` with
    `    if False:`. (ii) Replace the single line `    if not request.ci_green:`
    with `    if False:`. Each must turn at least one test RED. Before each edit
    report that the replaced line occurs exactly 1x in the file; after the last
    revert report that worktree's `git status --porcelain`, so the restoration is
    measured and not assumed.

G11 THE PARSER CAN SAY NO. Separately from pytest, report what
    `changelog_section("# Changelog\n\n## [1.0.0] - 2026-01-01\n\n- x\n",
    "0.0.0-absent")` returns. It must be None — without that control G9 (d)
    proves nothing.

G12 NO REGRESSION, ROUND GATE SUITE AND CANARY. Three runs in the PRIMARY
    checkout, each started only after the previous ENDED; state that none
    overlapped, and report each real exit code and pass count. (a) `python3 -m
    pytest tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py -q` — the existing readers of
    the package this round adds a module to. (b) `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed.
    (c) `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.

G13 LINT IS CLEAN ON WHAT THIS ROUND ADDS. Run `python3 -m ruff check
    packages/orchestration/release_gate.py
    tests/orchestration/test_release_gate.py` at HEAD. Both paths are NEW, so
    there is no base reading to compare and the requirement is exit 0 with an
    EMPTY rule-code multiset. Report the exit code and the multiset.

G14 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `3351878d..HEAD` BEFORE C5, one line each;
    none may exceed 500. Report C5's own count in the round report.

G15 HISTORY. Every commit in `3351878d..HEAD` has exactly one parent, the chain
    is linear, and `git reflog` over this round shows only `commit:` entries — no
    amend, rebase, reset, force-push. Report the chain.

G16 PATH SET. `git diff --name-only 3351878d..HEAD`, measured before C5, is
    exactly the paths constraint 2 lists other than `.agent/handoff.md`. Report
    the post-C5 set in the round report. Confirm `pyproject.toml`,
    `.github/workflows/ci.yml`, `hatch_build.py`, `apps/cli/version_report.py`
    and `packages/orchestration/ci_stages.py` are ABSENT, and confirm with
    `git ls-tree 3351878d` that all five EXIST at the base, so the clause forbids
    something real. `CHANGELOG.md` must be absent from the range AND absent at
    the base; report both readings, since a clause forbidding a file that does
    not exist either side forbids nothing (finding R-0559).

G17 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report it verbatim; merge nothing.

Handback:
Completion report plus a rewritten `.agent/handoff.md`. Push after C4 and again
after C5. Report every gate with its REAL exit code and output — "green" as a
word is a finding. If a gate is red, say so with the raw output and hand off.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN13>>>
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
R13, this round: T003's decision half. `packages/orchestration/release_gate.py`
refuses a release on red CI, a tag that does not match the version, a missing or
empty changelog section, or a wheel over budget, with one seeded-failure test
each. Also records the R12 verdict and registers R-0582.

## Next Steps
1. R14 — the DATA and the CALLER, which R13 deliberately left out: a
   keep-a-changelog `CHANGELOG.md` with a section for the version
   `pyproject.toml` declares, a test that the real changelog covers the real
   version, and a manual-trigger workflow calling `refuse_release` with the real
   tag, version, changelog and wheel size. UNTIL THEN THE GATE REFUSES NOTHING.
2. Then the install smoke, the integration gate, and closure. The packaging
   ist-doc is written at closure, when the built state stops moving.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
<<<END PLAN13>>>

<<<SLICE FIND0582>>>

- R-0582 — Low — THE HANDBACK LINE CAP HAS BECOME NOMINAL, AND THE REVIEWER'S OWN BLOCKS ARE WHY. AGENTS.md caps `.agent/handoff.md` at 100 lines and DECISION D15 admits a DECLARED overage. Measured on this branch, the declared overage is now every round and it is growing: 113 lines at R10, 165 at R11, 223 at R12, against a cap of 100 — the last of those 2.2x. No round hid it; each declared the overage and named its cause, so no worker is at fault and none of these is a process breach. The defect is that the reviewer's blocks ORDER more mandated content than the cap admits, so D15's exception has stopped being an exception. R12's block is the plain case: it ordered a per-commit table for eight commits, a Verification transcript for seventeen gates, and — correctly, per R-0581 — every digest written out in full at 64 characters rather than elided, which alone costs more lines than elision did. A cap that is exceeded by design every round constrains nothing and stops carrying information: a reader cannot tell an unusually long handback from an ordinary one, which is exactly what a cap is for. TWO REPAIRS ARE AVAILABLE AND THIS FINDING RULES ON NEITHER, because AGENTS.md is the higher authority and docs/agents/planner_reviewer_prompt.md §4 item 7 routes a repository rule to planning rather than to the reviewer. Either the cap moves to a number the mandated content can actually meet, which is an AGENTS.md edit and an operator decision; or the reviewer stops ordering the full transcript into the handback and orders it into the ROUND REPORT instead, keeping the handback to the state the next session needs — which is a block-authoring change the reviewer may make alone, and is the cheaper of the two. What must NOT happen is the third option nobody has proposed and everybody drifts toward: leaving the cap in place and declaring against it forever. OPEN.
<<<END FIND0582>>>

<<<SLICE RECORD11>>>

Gate: R13 — the R12 entry. R12 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `ee22186c..3351878d` rather than read from the handback, and every reading reproduces. THE FEATURE T002 OWED NOW EXISTS AND IS PROVED ON A REAL ARTIFACT, which is the round's point: in a worktree at `3351878d` sited OUTSIDE this repository, the wheel builds at exit 0 with 417 members, exactly one member matches `REVISION` and it is `remedy-0.1.0.dist-info/extra_metadata/REVISION`, its bytes are `3351878de3880903ca27383da554c3926065fc43\n`, and that string equals the probe worktree's own `git rev-parse HEAD`. Over the unpacked wheel `PathDistribution.read_text("extra_metadata/REVISION")` returns that revision and `read_text("REVISION")` returns None — so the reader's new constant is load-bearing rather than cosmetic. THE RED CONTROL RAN AND IT IS WHAT MAKES THE GREEN MEAN ANYTHING: the same build at the base `ee22186c`, unmodified, also exits 0 — so the control ran rather than failing for an unrelated reason — and ships 416 members with an EMPTY list of REVISION members and `read_text("REVISION")` None. The one-member delta between the two wheels is exactly the new entry. THE TESTS CAN FAIL: 17 passed at exit 0, and under the reviewer's own mutations in a worktree — the `if revision is None:` guard turned to `if False:`, then `REVISION_METADATA_FILE` set back to `"REVISION"`, each byte string counted 1x in its named file first — each reads 1 failed / 16 passed, returning to 17 passed once reverted with that worktree's `git status --porcelain` EMPTY. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original, the committed `.agent/authored/f086-r12.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 cf95003c5e898b1e6ca409bac936a37e389d6f442bd548c80c5e6041150f1b25, 30277 B, 490 lines. EVERY SLICE LANDED BYTE-EXACT AND EVERY DIGEST THE HANDBACK REPORTS MATCHES THE REVIEWER'S OWN, all five written in full rather than elided, which is R-0581 being honoured in the first artifact it applied to: `.agent/plan.md` 17d11ea5cff5747c19ff4ec875d0a7dba9ae892755b411dde529c05d346a51c4 at 38 lines, the 4-line ledger remainder 071a2aee0b8b4c7f47019f7ca604f3f53209c5ee6b8de7c77d5b0929fa765ecc, `hatch_build.py` aa6d90779d6fd50188c3f083a1be1eccd6c0d487fd625b8ff2b53baf0b6d5b90 at 90 lines and `tests/test_build_revision.py` 5e6f26cfa797475ebdd13ebae815f7700cd08e545ea14ce286e715a6a5012255 at 71 lines, both absent at the base; `apps/cli/version_report.py` at HEAD equals the base blob with its single VERFROM occurrence replaced by VERTO, by ordered equality rather than by a count, with VERFROM 1x then 0x and VERTO 0x then 1x. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the six written files. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 163 registered / 2 resolved / 161 open at `ee22186c` and 164 / 2 / 162 at HEAD, with the symmetric difference of the registered sets exactly `['R-0581']` under both; the `Gate: ` paragraphs go from 9 to 10 and the added one names R12. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the primary checkout: 17 passed for the gate suite, 560 for the entry point, 160 for the four state readers and 42 for the canary, each exit 0. RUFF DID NOT GET WORSE: an empty rule-code multiset over the touched files at HEAD, and an empty one over the two that exist at the base, measured in a worktree at `ee22186c` rather than in a checkout standing at HEAD — the distinction matters, because the reviewer's first attempt read the base command in a checkout already advanced to HEAD and would have compared HEAD with itself. THE HYGIENE HELD: eight paths over eight single-parent commits inserting 490, 403, 5, 4, 57, 5, 71 and 186 lines, none over 500. THE ONE DECLARED DEVIATION IS NOT A FINDING BUT IT IS NOW A REGISTERED ONE: `.agent/handoff.md` stands at 223 lines against a 100-line cap, declared under DECISION D15 with its cause named and no section dropped — and R-0582, registered this round, is that the reviewer's blocks order more mandated content than the cap admits, every round, which is the reviewer's defect and not the worker's.
<<<END RECORD11>>>

<<<SLICE GATE>>>
"""The release gate: every reason a release must be refused (T2_F086 T003).

This module DECIDES and RUNS NOTHING. It takes a description of a proposed
release and returns the reasons to refuse it, so each refusal the feature's
Acceptance names is testable without a tag, a wheel or a CI run existing. The
caller — a manual-trigger workflow, not yet written — supplies the real values,
reads the repository's `CHANGELOG.md` and stops on a non-empty result. Until that
caller exists this gate refuses nothing, because nothing calls it. It is
deliberately NOT an entry in `ci_stages.CI_STAGES`, which is pytest-selection
data; this gate selects no tests. Publishing stays a HUMAN command, which
T2_F086's Orchestrator brief requires: nothing here uploads or holds a credential.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: Measured, not guessed: a wheel built at F086 R12 carrying a stand-in
#: `index.html` is 2040197 B, one carrying the built `apps/ui/dist` was 2155470 B
#: at F086 R7. The budget is 8 MiB, about four times that: it admits a real UI
#: bundle's growth while still refusing what it exists to catch — a wheel that
#: swallowed `node_modules`, `.git` or the test corpus.
WHEEL_SIZE_BUDGET_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class ReleaseRequest:
    """A proposed release, as the caller observed it."""

    tag: str
    version: str
    changelog: str
    wheel_bytes: int
    ci_green: bool


def normalise_tag(tag: str) -> str:
    """Return `tag` without a leading `v`, which is how tags are written here."""
    return tag[1:] if tag.startswith("v") else tag


def changelog_section(changelog: str, version: str) -> str | None:
    """Return the body of `version`'s changelog section, or None if it has none.

    A section runs from its own `## [<version>]` heading to the next heading
    starting `## `, or to the end of the file. An empty body is NOT the same as a
    missing section: the caller refuses on both but must be able to say which.
    """
    heading = re.compile(rf"^## \[{re.escape(version)}\][^\n]*\n", re.MULTILINE)
    found = heading.search(changelog)
    if found is None:
        return None
    rest = changelog[found.end():]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest if following is None else rest[: following.start()]


def refuse_release(request: ReleaseRequest) -> tuple[str, ...]:
    """Every reason to refuse `request`; an EMPTY tuple means it may proceed.

    Every rule is evaluated, so the result names ALL the reasons rather than the
    first — a release broken four ways should have to be fixed once.
    """
    reasons: list[str] = []
    if not request.ci_green:
        reasons.append("CI is not green for this commit")
    if normalise_tag(request.tag) != request.version:
        reasons.append(
            f"tag {request.tag!r} does not match distribution version {request.version!r}"
        )
    body = changelog_section(request.changelog, request.version)
    if body is None:
        reasons.append(f"CHANGELOG.md has no section for version {request.version!r}")
    elif not body.strip():
        reasons.append(f"the CHANGELOG.md section for {request.version!r} is empty")
    if request.wheel_bytes > WHEEL_SIZE_BUDGET_BYTES:
        reasons.append(
            f"wheel is {request.wheel_bytes} B, over the "
            f"{WHEEL_SIZE_BUDGET_BYTES} B budget"
        )
    return tuple(reasons)
<<<END GATE>>>

<<<SLICE TESTS>>>
"""Seeded-failure tests for the release gate (T2_F086 T003).

T2_F086's Acceptance names four refusals — red CI, tag/version mismatch, missing
changelog section, budget breach — and asks for one test each. Every test below
starts from a request that PASSES and changes exactly one field, so if the
accepting case ever stops accepting, its own test fails first rather than the
others going quietly meaningless.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from packages.orchestration.release_gate import (
    WHEEL_SIZE_BUDGET_BYTES,
    ReleaseRequest,
    changelog_section,
    normalise_tag,
    refuse_release,
)

CHANGELOG = """# Changelog

## [1.2.3] - 2026-01-01

### Added
- A thing that was added.

## [1.2.2] - 2025-12-01

### Fixed
- A thing that was fixed.
"""

ACCEPTING = ReleaseRequest(
    tag="v1.2.3",
    version="1.2.3",
    changelog=CHANGELOG,
    wheel_bytes=2_040_197,
    ci_green=True,
)


def _with(**changes) -> ReleaseRequest:
    """The accepting release with exactly `changes` applied."""
    return replace(ACCEPTING, **changes)


@pytest.mark.unit
class TestTheGateAccepts:
    def test_a_sound_release_is_not_refused(self):
        assert refuse_release(ACCEPTING) == ()

    def test_a_bare_tag_without_the_v_prefix_also_matches(self):
        assert refuse_release(_with(tag="1.2.3")) == ()
        assert normalise_tag("1.2.3") == "1.2.3"


@pytest.mark.unit
class TestTheGateRefuses:
    """One test per refusal T2_F086's Acceptance names."""

    def test_red_ci_is_refused(self):
        assert any("CI is not green" in r for r in refuse_release(_with(ci_green=False)))

    def test_a_tag_that_does_not_match_the_version_is_refused(self):
        reasons = refuse_release(_with(tag="v9.9.9"))
        assert any("does not match distribution version" in r for r in reasons)

    def test_a_missing_changelog_section_is_refused(self):
        reasons = refuse_release(_with(version="4.5.6", tag="v4.5.6"))
        assert any("no section for version" in r for r in reasons)

    def test_an_empty_changelog_section_is_refused(self):
        empty = "# Changelog\n\n## [1.2.3] - 2026-01-01\n\n## [1.2.2] - 2025-12-01\n\n- x\n"
        assert any("is empty" in r for r in refuse_release(_with(changelog=empty)))

    def test_a_wheel_over_the_budget_is_refused(self):
        reasons = refuse_release(_with(wheel_bytes=WHEEL_SIZE_BUDGET_BYTES + 1))
        assert any("over the" in r and "budget" in r for r in reasons)

    def test_a_wheel_exactly_at_the_budget_is_not_refused(self):
        assert refuse_release(_with(wheel_bytes=WHEEL_SIZE_BUDGET_BYTES)) == ()

    def test_every_broken_rule_is_named_not_only_the_first(self):
        reasons = refuse_release(
            _with(ci_green=False, tag="v9.9.9", wheel_bytes=WHEEL_SIZE_BUDGET_BYTES + 1)
        )
        assert len(reasons) == 3


@pytest.mark.unit
class TestChangelogParsing:
    def test_a_section_runs_only_to_the_next_heading(self):
        body = changelog_section(CHANGELOG, "1.2.3")
        assert "A thing that was added." in body
        assert "A thing that was fixed." not in body

    def test_an_absent_version_has_no_section(self):
        assert changelog_section(CHANGELOG, "0.0.0-absent") is None

    def test_the_last_section_runs_to_the_end_of_the_file(self):
        body = changelog_section(CHANGELOG, "1.2.2")
        assert "A thing that was fixed." in body
<<<END TESTS>>>
