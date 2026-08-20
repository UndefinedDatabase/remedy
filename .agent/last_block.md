── STEP T2/3 — F086 R20 ──────────────────────────────────────

Goal:        Land the install smoke DECISION F086 D4 rules — one opt-in module
             whose pure helpers and skip path are gated here and whose install is
             executed elsewhere — and record R19's verdict with the finding that
             round produced against the reviewer.

Bundle:      1. `.agent/plan.md` := PLAN20.
             2. `.agent/live_review.md` += FIND0586, then RECORD18.
             3. `tests/test_install_smoke.py` := SMOKE, a file that does not yet
                exist on this branch.
             4. The handback.

Change:      C0a `.agent/authored/f086-r20.md` := this block, byte-verbatim, the
                 single top separator line included and nothing after the last
                 slice's END marker.
             C0b `.agent/last_block.md` := a mirror of the COMMITTED C0a, read
                 back from git rather than retyped.
             C1  `.agent/plan.md` := PLAN20, whole file. Alone. This is the round's
                 FIRST substantive commit because the bundle moves the finding
                 ledger (§3 item 23).
             C2  `.agent/live_review.md` += a blank line, FIND0586, a blank line,
                 RECORD18. Pure append; nothing already in the file changes.
             C3  `tests/test_install_smoke.py` := SMOKE, a NEW file whose entire
                 content is that slice. Alone.
             C4  `.agent/handoff.md` := your rewrite.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   SMOKE is CODE: apply it as bytes, do not reformat it, do not let an editor
   strip a trailing blank line, and do not run a formatter over it.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r20.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `tests/test_install_smoke.py`, and
   `.agent/handoff.md` at C4. NOT `tests/conftest.py`, not `pyproject.toml`, not
   `packages/orchestration/ci_stages.py`, not `apps/cli/version_report.py`, not
   `hatch_build.py`, not `tests/test_packaging_smoke.py`, and nothing else under
   `apps/`, `packages/`, `docs/` or `.github/`. Every path this constraint
   FORBIDS exists at `bc85e5f7`, so the prohibition forbids something real
   (R-0559), while `tests/test_install_smoke.py` deliberately does NOT exist
   there and G8 measures that absence rather than assuming it.
3. FIND0586, RECORD18, PLAN20 and SMOKE are the reviewer's text. Do not
   summarise or reformat them, and do not write a verdict of your own anywhere —
   in the handoff, in a commit message, or in your report. Reporting what a gate
   MEASURED is your job; ruling on a round is not.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback. This round DOES order mutation probes, so it adds ONE
   disposable worktree under `.remedy-wt/`, runs G10 and G11 inside it, and
   removes it with `git worktree remove --force` plus `git worktree prune` before
   the handback; `git worktree list` reads one line at the handback. No mutation
   ever touches the primary checkout (§4.10).
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
6. NO INSTALL RUNS THIS ROUND, in any command you issue. `REMEDY_INSTALL_SMOKE`
   stays unset in every environment you create, the probe worktree's included, so
   the module's one install test SKIPS in every run this round reports. Say that
   plainly in the handback: a skipped test is not coverage, and DECISION F086 D4
   already records that F086's DONE condition stays UNPROVEN until that variable
   is set on a host that can honour it. Do not set it to "prove" the module works.
7. SIZE, measured at emission on the final bytes: this block is 482 lines TOTAL —
   212 prose and 270 slice including its 8 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`;
    `git worktree list` one line at the handback, per constraint 4.

G2  TRANSPORT. `.remedy-wt/f086-r20.md`, the committed
    `.agent/authored/f086-r20.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at the commit C1 creates is byte-equal to the PLAN20
    slice extracted from the COMMITTED `.agent/authored/f086-r20.md`. Report its
    full sha256 and line count, confirm the count is under 50, and confirm it
    contains `## Goal`, `## Next Steps` and `F086`.

G4  THE LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob, and the remainder is byte-equal to a blank line,
    FIND0586, a blank line, RECORD18, in that order. Report the remainder's own
    full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At the commit C2 creates report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Expected there: 169 registered, 3
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:` lines, 166
    open. Report the symmetric difference of that registered set against the
    `bc85e5f7` set AS THE SET; it must be exactly `['R-0586']`.
    CONTROL: the SAME extractor over `f0b27118..7b84524c` must read `[]` for the
    registered symmetric difference while its RESOLVED set gains exactly `R-0584`,
    so the extractor is measured on a range that moved a resolution and not a
    registration.

G6  THE FINDING'S OWN RULE, MEASURED ON THE TEXT THAT LANDS. Take the lines C2's
    diff ADDS to `.agent/live_review.md`. FIRST delete every backtick-quoted span
    from them — the regex `` `[^`]*` `` — because a token this finding QUOTES is
    not a token it USES, and a guard that cannot tell the two apart is satisfied
    by the quotation (R-0584 class). THEN count `\bHEAD\b` in what remains; the
    count must be 0. RED CONTROL, so the reading is measured and not blind: the
    SAME two-step extractor over the lines `fd166295`'s diff ADDS to that same
    file reads 3. Report both numbers. This gate is R-0586's counter-measure
    demonstrated in the round that registers it; the checklist promotion is
    R21's, and FIND0586 says so rather than claiming a §3 edit this block does
    not order (§3 item 11).

G7  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md` and `tests/test_install_smoke.py` each contain 0 lines
    beginning `<<<SLICE ` or `<<<END ` at the commit C4 creates. Count marker
    LINES, not `<<<`.

G8  THE NEW MODULE IS THE SLICE, AND IT IS NEW. `git ls-tree bc85e5f7 --
    tests/test_install_smoke.py` prints NOTHING, so the file is created by this
    round; and at the commit C3 creates that file is byte-EQUAL to the SMOKE
    slice extracted from the COMMITTED `.agent/authored/f086-r20.md`. Report the
    full sha256 and line count of both, and state that they match. For a file the
    round CREATES, §4.9's ordered-equality obligation for a CODE slice reduces to
    whole-file byte equality, so no per-line count of added lines is ordered here
    (R-0531).

G9  THE MODULE RUNS AND ITS SKIP IS REAL. In the PRIMARY checkout, with
    `REMEDY_INSTALL_SMOKE` UNSET: `python3 -m pytest tests/test_install_smoke.py
    -q -rs` → exit 0, 14 passed, 1 skipped. Report the skip-reason line VERBATIM;
    it must name `REMEDY_INSTALL_SMOKE`. Exactly one test skips, and it is the
    install test — so no wheel was built, no venv was created and no network was
    reached, which is what constraint 6 requires and what this gate proves.

G10 LINT, BOTH HALVES, WITH A PROBE THAT SHOWS WHICH HALF SEES WHAT. At the
    commit C3 creates, in the primary checkout: `python3 -m ruff check
    tests/test_install_smoke.py` and `python3 -m ruff check --preview
    tests/test_install_smoke.py` each exit 0. Then, INSIDE the disposable worktree
    of constraint 4 and never in the primary checkout, in that same file, delete
    ONE of the two blank lines separating the definition of
    `install_smoke_is_enabled` from the definition of `resolve_build_root`, re-run
    BOTH commands, and report each one's exit code and the rule codes it names.
    Report what you observe rather than confirming a colour: the two halves are
    expected to disagree, because ruff's E301-E306 are preview-only (R-0500), and
    that disagreement is what makes ordering the preview half worth anything.
    Revert the deletion before G11.

G11 THE MUTATION PROBES, one at a time, each reverted before the next, ALL inside
    the disposable worktree of constraint 4 at the commit C3 creates. For each,
    FIRST count the bytes you are about to replace in `tests/test_install_smoke.py`
    and confirm the count is 1 in THAT file (§3 item 25), then run
    `python3 -m pytest tests/test_install_smoke.py -q -rf` and report the exit code
    and the NAMES of the tests it lists as failed — the names, never a count.
    (a) replace the single line
        `    return environ.get(INSTALL_SMOKE_ENV, "").strip().lower() not in DISABLED_VALUES`
        with `    return False`;
    (b) replace the single line
        `    if candidate == repo or repo in candidate.parents:`
        with `    if False:`.
    In BOTH probes the install test must STILL skip, and you report that it did:
    these mutations are chosen so the module's own logic can go red without any
    install being attempted, which is how constraint 6 and a real red-proof both
    hold.

G12 SUITES, in the PRIMARY checkout, serially, each starting only after the
    previous has ENDED and reported its code (R-0518 class: never two pytest
    processes at once). First
    `python3 -m pytest tests/test_test_categories.py tests/test_no_step_files.py
    tests/orchestration/test_ci_stages.py -q -rf` → exit 0, 24 passed: these are
    the guards a NEW test file could trip — the marker definitions, the forbidden
    step-file names, and the CI stage tuple and its budgets. Then
    `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed: the
    readers that PARSE the state files this round rewrites. Then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.

G13 CHANGE SET. `git diff --name-only bc85e5f7..HEAD` before C4 prints the paths
    constraint 2 NAMES other than `.agent/handoff.md`. Report the list it prints
    and the list constraint 2 names, and compare them AS SETS — state no numeral
    for either. Confirm with `git ls-tree bc85e5f7 -- <path>` that every path
    constraint 2 FORBIDS exists at that base, and report those readings.

G14 HISTORY AND COMMIT SIZE. Every commit in `bc85e5f7..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Walk the range with
    `git rev-list --reverse` and report the INSERTION count — the `+` column of
    `git show --numstat`, never insertions+deletions (DECISION F104 D1) — for
    every commit BEFORE C4, one reading each; none over 500. C4's own goes in the
    round report (§3 item 14).

G15 THE HANDBACK AND THE PR GATE. `.agent/handoff.md` at the commit C4 creates is
    AT MOST 100 lines and carries all seven mandated headings of
    docs/agents/handback_template.md in the template's order; report the `wc -l`
    reading and the heading list, and if it exceeds 100 declare the DECISION D15
    overage with its cause rather than dropping a section. Then re-read the Open
    PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its output. Create nothing, merge nothing.

Handback: your completion report with the FULL transcript — every gate's real
command, exit code and output, which is where the transcript belongs (R-0582) —
plus C4's rewrite of `.agent/handoff.md` carrying ONE line per gate.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN20>>>
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
R20: write the install smoke DECISION F086 D4 rules — `tests/test_install_smoke.py`,
one module that self-skips unless `REMEDY_INSTALL_SMOKE` is set — and record R19's
verdict plus R-0586, the finding R19 produced against the reviewer.

## Next Steps
1. R21 promotes R-0586's rule into the §3 pre-emission checklist, item 20, where a
   rule has to live to bind the next block, and records R20's verdict.
2. Then the smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a 300 s budget
   that AGENTS.md forbids raising by hand.
3. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions.

## Risks
- The install smoke needs network, a venv interpreter and minutes. MEASURED at
  R17: this session's permission layer refuses to execute an interpreter under
  `.remedy-wt/`, so a self-drive round can write that smoke but cannot run it.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN20>>>

<<<SLICE FIND0586>>>
- R-0586 — Low — A GATE-RECORD SLICE NAMED THE RE-RESOLVING LABEL `HEAD` FOR READINGS TAKEN AT A PRIOR ROUND'S TIP, AND NO GATE CHECKS WHAT §3 ITEM 20 ALREADY FORBIDS. RECORD17, committed at `fd166295` into `.agent/live_review.md`, reports R18's readings and writes the bare token `HEAD` three times, among them `167 / 3 / 0 / 0 / 0 / 164 at HEAD` for the ledger's six-value reading. That sentence is landed, permanent and unalterable, and `HEAD` re-resolves: measured at `bc85e5f7` with a paragraph extractor and a line-anchored extractor that agree, the same six values now read 168 / 3 / 0 / 0 / 0 / 165, so the sentence is false one commit after the round that wrote it and grows more false with every later round. §3 item 20 as narrowed by R-0521 rules exactly this — a commit is named by an absolute identifier that already EXISTS when the slice is written, never by a label like `HEAD` or `main` — and the SHA was available, because `7b84524c` is the base the block's own gates state. The carve-out R-0524 adds does not reach it: that carve-out covers a claim about the round's OWN commits, and every reading in RECORD17 is of the PRIOR range `f0b27118..7b84524c`. WHY THIS IS A FINDING RATHER THAN A HABIT, AND WIDER THAN THE ROUND THAT PROVOKED IT: the rule was written down and then broken by the same author under it, repeatedly. Measured at `bc85e5f7` with backtick-quoted spans removed first, the `Gate:` entries from R10 through R19 carry 3, 2, 2, 6, 3, 1, 1, 0, 4 and 3 unquoted occurrences in that order — every one of those entries except R17's carries at least one — so this is a standing property of the record and not one round's slip. That reading is of those entries only and is NOT a claim about the rest of the file. A rule nothing measures is a rule that degrades, and this class already cost R-0521 a round. THE LANDED ENTRIES ARE NOT REWRITTEN: §3 item 20 rules that the counter-measure is the commit name in NEW text, never a rewrite, because overwriting landed text is worse than a dated wrong sentence — so no repair round is opened to sweep them, and this paragraph is the dated correction. WHY LOW: nothing acted on the wrong number. `.agent/live_review.md` is a record read by humans and by the reviewer's own extractor, which reads ids rather than prose, so no gate and no state file consumed the stale reading — the damage is a permanent record that misstates itself to a later reader, which is the harm this ledger exists to prevent. COUNTER-MEASURE, split so that neither half overclaims: this round's own G6 counts `\bHEAD\b` over the lines its ledger commit ADDS and requires 0, with the same count over `fd166295`'s added lines as the red control that proves the extractor sees anything at all; and R21 promotes the rule into §3 item 20 as a mechanical pre-emission scan, because a rule that lives only in a finding body is a rule the next block does not read (R-0452, R-0548).
<<<END FIND0586>>>

<<<SLICE RECORD18>>>
Gate: R19 — the R18 entry. R19 PASSED, with ONE finding — R-0586, against the reviewer, registered by this round's own FIND0586 slice. Every gate R19's block ordered was re-executed by the reviewer over `7b84524c..bc85e5f7` rather than read from the handback, and every reading reproduces. THE CHECKLIST EDIT LANDED WHERE IT WAS AIMED AND MOVED NOTHING ELSE: in `docs/agents/planner_reviewer_prompt.md` the CHECKFROM anchor occurs 1x at `7b84524c` and 1x at `bc85e5f7` — what an append means — each of CHECKTO's seven TO-ONLY lines occurs 1x among the lines `fc181c06`'s diff ADDS, the file at `bc85e5f7` is byte-equal to the `7b84524c` blob with that single occurrence replaced and nothing else changed at sha256 f0666f4ba57e0c2611f34f7eea1b96c9f28b3f0ec9adc740c9285304b5757f22 over 773 lines against 766, and the line immediately after the inserted text is the item-17 line, which `grep -c '^  17\. \*\*'` finds exactly once. THE REVIEWER RE-RAN THE CLAIM THAT COMMIT RESTS ON rather than repeating it: `docs/agents/planner_reviewer_prompt.md` is named exactly once under `tests/`, in `tests/test_agent_tooling.py`, inside the `reason=` string of a `@pytest.mark.skip` decorator whose test reads `.claude/agents/remedy-reviewer.md` and never that file, so no suite could have gone red on `fc181c06` and the pair proof is genuinely that commit's whole evidence. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 167 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 164 open at `7b84524c` and 168 / 3 / 0 / 0 / 0 / 165 at `bc85e5f7`, the two registered SETS are equal, the symmetric difference is exactly `['R-0585']`, and the reviewer's control over `f0b27118..7b84524c` reads `[]` for the registered difference while its resolved set gains `R-0584`. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r19.md`, the committed `.agent/authored/f086-r19.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 993bf12e0db8b8ead632b28a474e25dc5502996eebc75d8fb73242855e4587ea, 26901 B over 359 lines — 359 total, 245 prose, 114 slice including 12 marker lines, which is what constraint 6 of that block declares of itself. `.agent/plan.md` equals PLAN20's predecessor PLAN19 at f840f9adf868fab275244d3575c5dfd066f1d36cfe93242552fcedbd82dc170e over 43 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals FIND0585 then RECORD17 at a2c19e541cb7ad88d3e356c2b2a045539e505313f72b8abf66aee534030b936e; and the `5eeeae40` handoff blob is a byte-exact PREFIX of the file at `bc85e5f7` whose 42-line remainder is the VERDICT slice. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the four written files. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: exit 0 and 160 passed for the four state readers, then exit 0 and 42 passed for the canary. THE HYGIENE HELD: six paths over seven single-parent commits inserting 359, 204, 10, 4, 7, 28 and 42 lines, none over 500 and no DECISION F104 D1 exemption invoked; `.github/workflows/release.yml`, `packages/orchestration/ci_stages.py`, `pyproject.toml`, `scripts/release_gate_check.py` and `tests/orchestration/test_release_workflow.py` are absent from the range and all five exist at `7b84524c`. THE HANDBACK CAME IN UNDER ITS CAP at 96 lines against 100, all seven mandated headings in the template's order, no DECISION D15 overage. WHERE R19 WENT WRONG is in none of its own gates but in the prose of the record it landed, which names `HEAD` where it had a SHA to hand; that is R-0586, and R20's G6 measures the same property over its own ledger commit.
<<<END RECORD18>>>

<<<SLICE SMOKE>>>
"""Install smoke — the wheel installs and the installed CLI works (F086 T2).

DECISION F086 D4 rules that this module is WRITTEN here and EXECUTED elsewhere:
it self-skips unless `REMEDY_INSTALL_SMOKE` is set, because a self-drive round has
neither network access nor permission to spawn an interpreter it has just
installed. What every ordinary run of this file DOES gate is the opt-in decision
and the pure helpers below. What it does NOT gate is the install itself: a
skipped test is not coverage, and F086's DONE condition stays UNPROVEN until the
variable is set on a host that can honour it.

Remedy deliberately does not build the wheel inside this repository. Hatchling
drops every VCS exclusion when the build root is matched by `.gitignore`, so a
probe rooted in a gitignored scratch directory ships files a real wheel omits
(finding R-0574). `resolve_build_root` is that rule written as code.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

INSTALL_SMOKE_ENV = "REMEDY_INSTALL_SMOKE"
REPO_ROOT = Path(__file__).resolve().parents[1]
DISABLED_VALUES = frozenset({"", "0", "false", "no", "off"})
UNKNOWN_MARKER = "dev"
VERSION_REPORT_FIELDS = ("remedy", "build", "python", "platform")
DECLARED_VERSION_PATTERN = re.compile(r'(?m)^version\s*=\s*"([^"]+)"')


def install_smoke_is_enabled(environ: dict[str, str]) -> bool:
    """Return whether the opt-in variable asks for the real install to run."""
    return environ.get(INSTALL_SMOKE_ENV, "").strip().lower() not in DISABLED_VALUES


def resolve_build_root(repo_root: Path, scratch_root: Path) -> Path:
    """Return the wheel build root, refusing any path inside the repository."""
    repo = repo_root.resolve()
    candidate = scratch_root.resolve()
    if candidate == repo or repo in candidate.parents:
        raise ValueError(f"build root {candidate} lies inside the repository {repo}")
    return candidate


def read_declared_version(pyproject_path: Path) -> str:
    """Return the one version literal `pyproject.toml` declares (DECISION F086 D2)."""
    match = DECLARED_VERSION_PATTERN.search(pyproject_path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"no version declaration in {pyproject_path}")
    return match.group(1)


def parse_version_report(text: str) -> dict[str, str]:
    """Parse `remedy --version` output into its field mapping."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        name, _, value = line.partition(" ")
        if name in VERSION_REPORT_FIELDS and value.strip():
            fields[name] = value.strip()
    return fields


def version_report_proves_an_install(report: dict[str, str], expected_version: str) -> bool:
    """Return whether the report came from an INSTALLED wheel rather than a checkout."""
    if sorted(report) != sorted(VERSION_REPORT_FIELDS):
        return False
    if report["remedy"] != expected_version or report["remedy"] == UNKNOWN_MARKER:
        return False
    return report["build"] != UNKNOWN_MARKER


def _report_text(version: str = "0.1.0", build: str = "abc1234") -> str:
    """Render a `remedy --version` report the way `render_version_report` does."""
    return f"remedy   {version}\nbuild    {build}\npython   3.11.2\nplatform Linux-6.1"


@pytest.mark.unit
class TestInstallSmokeOptIn:
    """The gate that keeps this module inert on a host that cannot honour it."""

    def test_an_unset_variable_leaves_the_smoke_disabled(self):
        assert install_smoke_is_enabled({}) is False

    def test_every_documented_disabled_value_leaves_it_disabled(self):
        for raw in sorted(DISABLED_VALUES):
            assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: raw}) is False

    def test_any_other_value_enables_it(self):
        assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: "1"}) is True
        assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: " yes "}) is True


@pytest.mark.unit
class TestBuildRootLiesOutsideTheRepository:
    """Finding R-0574 as an executable rule rather than a comment."""

    def test_a_path_inside_the_repository_is_refused(self, tmp_path):
        with pytest.raises(ValueError) as excinfo:
            resolve_build_root(tmp_path, tmp_path / "scratch" / "build")
        assert "lies inside the repository" in str(excinfo.value)

    def test_the_repository_root_itself_is_refused(self, tmp_path):
        with pytest.raises(ValueError):
            resolve_build_root(tmp_path, tmp_path)

    def test_a_sibling_path_is_accepted(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        assert resolve_build_root(repo, outside) == outside.resolve()


@pytest.mark.unit
class TestVersionReportReading:
    """The `--version` half of F086's DONE condition, parsed and judged."""

    def test_the_declared_version_is_read_from_pyproject(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "remedy"\nversion = "1.2.3"\n')
        assert read_declared_version(pyproject) == "1.2.3"

    def test_a_pyproject_without_a_version_is_refused(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "remedy"\n')
        with pytest.raises(ValueError):
            read_declared_version(pyproject)

    def test_a_real_report_parses_into_its_four_fields(self):
        assert parse_version_report(_report_text()) == {
            "remedy": "0.1.0", "build": "abc1234",
            "python": "3.11.2", "platform": "Linux-6.1",
        }

    def test_an_installed_report_is_accepted(self):
        assert version_report_proves_an_install(parse_version_report(_report_text()), "0.1.0") is True

    def test_a_checkout_report_is_refused_because_both_fields_read_dev(self):
        report = parse_version_report(_report_text(version="dev", build="dev"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_an_embedded_revision_of_dev_is_refused_on_its_own(self):
        report = parse_version_report(_report_text(build="dev"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_a_version_that_differs_from_the_declaration_is_refused(self):
        report = parse_version_report(_report_text(version="0.9.9"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_a_truncated_report_is_refused(self):
        assert version_report_proves_an_install({"remedy": "0.1.0"}, "0.1.0") is False


def _fixture_git_repo(root: Path) -> Path:
    """Create the minimal committed git repository `remedy init` expects."""
    root.mkdir(parents=True)
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "smoke", "GIT_AUTHOR_EMAIL": "smoke@example.invalid",
        "GIT_COMMITTER_NAME": "smoke", "GIT_COMMITTER_EMAIL": "smoke@example.invalid",
    }
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True, env=env,
    )
    return root


@pytest.mark.smoke
@pytest.mark.slow
@pytest.mark.subprocess
@pytest.mark.skipif(
    not install_smoke_is_enabled(dict(os.environ)),
    reason=f"install smoke is opt-in: set {INSTALL_SMOKE_ENV}=1 on a host with network access",
)
def test_the_wheel_installs_and_the_installed_cli_runs_the_golden_path(tmp_path):
    """Build outside the repo, install into a fresh venv, drive the installed CLI."""
    build_root = resolve_build_root(REPO_ROOT, tmp_path / "build")
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", f"file://{REPO_ROOT}", str(build_root)],
        check=True, capture_output=True, timeout=300,
    )
    shutil.copytree(REPO_ROOT / "apps" / "ui" / "dist", build_root / "apps" / "ui" / "dist")

    venv = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, timeout=300)
    subprocess.run(
        [str(venv / "bin" / "python"), "-m", "pip", "install", "--quiet", str(build_root)],
        check=True, capture_output=True, timeout=1800,
    )

    remedy = venv / "bin" / "remedy"
    assert remedy.exists(), "the console entrypoint is not on the fresh venv's PATH"
    assert next(venv.glob("lib/python*/site-packages/apps/ui/dist/index.html"), None) is not None, (
        "the installed wheel carries no built UI assets"
    )

    version = subprocess.run([str(remedy), "--version"], check=True, capture_output=True, text=True, timeout=120)
    expected = read_declared_version(REPO_ROOT / "pyproject.toml")
    report = parse_version_report(version.stdout)
    assert version_report_proves_an_install(report, expected) is True, report

    project = _fixture_git_repo(tmp_path / "project")
    env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path / "data")}
    init = subprocess.run(
        [str(remedy), "init"], cwd=str(project), env=env,
        capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL,
    )
    assert init.returncode == 0, init.stderr
    do = subprocess.run(
        [str(remedy), "do", "install smoke mission", "--no-llm"], cwd=str(project), env=env,
        capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL,
    )
    assert do.returncode == 0, do.stderr
<<<END SMOKE>>>
