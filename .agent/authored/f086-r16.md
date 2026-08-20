── STEP R16 — F086 Release capability (the TRIGGER; close the session) ──

Goal:
Give the release gate its trigger, then close the session on disk. R15 made the
gate refuse something real — a changelog with the declared version's section, and a
caller observing a release from the built wheel's own filename. What is still
missing is the thing that INVOKES it on GitHub. This round adds a manual-trigger
`.github/workflows/release.yml` and the text guards that keep it manual, thin and
publish-free, then records the R15 verdict and writes the reviewer's own session
verdict to disk (finding R-0571).

THE WORKFLOW IS GATED AS TEXT AND NEVER RUN — the convention
`tests/orchestration/test_ci_workflow.py` already holds for `ci.yml`, for the
reason its docstring records. No round can dispatch a `workflow_dispatch`
workflow; PLAN16 says so on disk rather than letting a reader assume otherwise.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r16.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN16 slice, whole file
  C2  append RECORD14 to `.agent/live_review.md`
  C3  `.github/workflows/release.yml` := the WORKFLOW slice, a NEW file
  C4  `tests/orchestration/test_release_workflow.py` := the GUARDS slice, NEW
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C6  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 item 23 requires the plan to advance before any commit
touching the finding ledger; C3 precedes C4 because the guards read the workflow.
This round registers NO finding — R15 produced none — so the open set does not
move and no FINDINGS slice exists.

Base:
This round starts from `efc021d9`, the tip of `feature/f086-release-capability` and
the R15 handback commit. Every range gate names that SHA. Stay on the branch: do
NOT create one, merge, or open a PR — F086's PR belongs to its closure round.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN16, WORKFLOW
and GUARDS are COMPLETE files, each including its single trailing newline. RECORD14
and VERDICT are EOF-APPENDS: pure concatenation, each slice's own leading blank
line INSIDE the slice, nothing prepended, nothing stripped. No FROM/TO pair exists
in this block, so no pair shape is claimed and no FROM-count is orderable.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `efc021d9`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r16.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r16.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r16.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN16 slice, byte-verbatim, whole file. Alone.

3. C2 — append RECORD14 to `.agent/live_review.md` under the append convention.
   Commit alone. It is the reviewer's R15 verdict; it begins `Gate:` and
   registers no finding id, so it moves no ledger set.

4. C3 — create `.github/workflows/release.yml` := the WORKFLOW slice. Commit alone.
   Do not add it to `packages/orchestration/ci_stages.py`, which is
   pytest-selection data: this workflow selects no tests.

5. C4 — create `tests/orchestration/test_release_workflow.py` := GUARDS. Alone.

6. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of efc021d9..<HEAD>`; write the literal token `HEAD`, this
   branch's convention from R10 onward, because a handoff cannot name the SHA of
   the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT — one line per gate:
   its number, what it measured in a clause, and its real colour or value. This
   is the R-0582 repair, which held at R14 and R15; G14 measures it. The FULL
   transcript goes in your ROUND REPORT, which no cap binds.
   THE BUDGET IS ARITHMETIC: the VERDICT slice C6 appends is 43 lines, measured by
   the reviewer, so 57 of the 100 remain for your text. Measure it yourself from
   the COMMITTED C0a file before writing C5, and state the FINAL line count of
   `.agent/handoff.md` — your lines plus the slice's — in your Deviations section.
   Do NOT trim after C6.
   `Next` names, in order, the next session's first three actions: re-read
   `.agent/STOP` from disk (Phase 1 rule 1), run the Open PR Gate (rule 2), then
   review `efc021d9..HEAD` and record R16's verdict (rule 4).

7. C6 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C5 must be a byte-exact PREFIX of the file at HEAD.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r16.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `.github/workflows/release.yml`,
   `tests/orchestration/test_release_workflow.py`, and `.agent/handoff.md` at C5
   and C6. Not `pyproject.toml`, not `hatch_build.py`, not
   `.github/workflows/ci.yml`, not `scripts/release_gate_check.py`, not
   `CHANGELOG.md`, and nothing under `apps/` or `docs/`.
3. The VERDICT slice and RECORD14 are the reviewer's text. Do not summarise or
   reformat them, and do not write a verdict of your own anywhere — in the handoff,
   in a commit message, or in your report. Reporting what a gate MEASURED is your
   job; ruling on a round is not.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback. This round adds exactly ONE disposable worktree, for G9's
   three controls; it is removed and pruned before the handback, where `git
   worktree list` reads one line. Every other gate command runs in the PRIMARY
   checkout, and suites run SERIALLY — the second starts only after the first has
   ENDED (R-0518).
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
   The WORKFLOW slice legitimately CONTAINS such shell forms — it is YAML for
   GitHub's runner, not a command you execute. Write it, never run it.
6. SIZE, measured at emission on the final bytes: this block is 490 lines TOTAL
   — 250 prose and 240 slice including its 10 marker lines — against DECISION
   F085 D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED
   C0a file and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r16.md`, the committed
    `.agent/authored/f086-r16.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN16 slice extracted
    from the COMMITTED `.agent/authored/f086-r16.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob and the remainder is byte-equal to RECORD14.
    Report THE REMAINDER'S OWN full sha256 and its line count.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST NOT MOVE. Extract twice — once
    by PARAGRAPH (split on blank lines; a paragraph counts when it STARTS with
    `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and
    `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Expected at HEAD: 166 registered, 2
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:`, 164 open.
    Report the symmetric difference of the HEAD registered set against the
    `efc021d9` set AS THE SET; it must be EMPTY, this round registering nothing.
    CONTROL: the SAME extractor over `6f5a589a..efc021d9` must read `['R-0583']`.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md`, `.github/workflows/release.yml` and
    `tests/orchestration/test_release_workflow.py` at HEAD each contain 0 lines
    beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<`.

G7  THE TWO NEW FILES ARE THEIR SLICES, AND THEY ARE NEW.
    `.github/workflows/release.yml` and
    `tests/orchestration/test_release_workflow.py` at HEAD are byte-equal to
    WORKFLOW and GUARDS respectively, extracted from the COMMITTED C0a file.
    Report each one's full sha256, byte count and line count. Confirm with
    `git ls-tree efc021d9 -- <path>` that each is ABSENT at the base, so both
    commits are creations and not edits.

G8  THE RELEASE SUITES, in the PRIMARY checkout: `python3 -m pytest
    tests/orchestration/test_release_workflow.py
    tests/orchestration/test_release_gate_wiring.py
    tests/orchestration/test_release_gate.py -q -rf` → exit 0, 28 passed.

G9  RED PROOFS — EACH GUARD CAN FAIL, AND FAILS FOR ITS OWN REASON. In the
    disposable worktree at the round's HEAD, apply each mutation below to
    `.github/workflows/release.yml` ONE AT A TIME, reverting fully between them,
    and after each run `python3 -m pytest
    tests/orchestration/test_release_workflow.py -q -rf` THERE. Each run must read
    exactly 1 failed and 6 passed, and the ONE name listed must be its pair:
      (a) in the single line containing `--tag "$TAG" \`, counted 1x in that file
          first, write `--tag '${{ inputs.tag }}' \` instead → ONLY
          `test_release_workflow_passes_the_tag_through_the_environment`;
      (b) insert the lines `  push:` and `    branches: [main]` directly after the
          line `on:` → ONLY `test_release_workflow_is_triggered_by_hand_only`;
      (c) insert a step whose `run:` line is `twine upload dist/*` → ONLY
          `test_release_workflow_publishes_nothing`.
    After the third revert, re-run and report 7 passed at exit 0 with that
    worktree's porcelain EMPTY. Report the names you actually saw.

G10 RUFF, SCOPED TO WHAT THIS ROUND ADDS. `python3 -m ruff check
    tests/orchestration/test_release_workflow.py` in the PRIMARY checkout → exit
    0 with an EMPTY rule-code multiset. That is the round's ONLY new Python path;
    `.github/workflows/release.yml` is YAML and ruff is not run over it. There is
    no base reading to compare against, the path being absent at `efc021d9` (G7
    measures that); say so rather than inventing one.

G11 CANARY AND THE STATE READERS, in the PRIMARY checkout, serially: `python3 -m
    pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed; then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.
    State that they did not overlap.

G12 HISTORY AND COMMIT SIZE. Every commit in `efc021d9..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Report the chain, and
    with it the INSERTION count — the `+` column of `git show --numstat` — for
    every commit BEFORE C5, one each; none over 500. C5's and C6's own go in the
    round report (§3 item 14).

G13 PATH SET. `git diff --name-only efc021d9..HEAD`, measured before C5, is
    exactly the six paths constraint 2 lists other than `.agent/handoff.md`. Report
    the post-C6 set in the round report. Confirm `pyproject.toml`, `hatch_build.py`,
    `.github/workflows/ci.yml`, `scripts/release_gate_check.py` and `CHANGELOG.md`
    are ABSENT from the range and all five EXIST at `efc021d9` under `git ls-tree`,
    so the clause forbids something real.

G14 THE HANDBACK STAYS UNDER ITS CAP. Report the line count of `.agent/handoff.md`
    at HEAD — after C6, so including the appended VERDICT slice. It must be AT MOST
    100, the AGENTS.md cap, with NO DECISION D15 overage declared, and hold all
    seven mandated headings of docs/agents/handback_template.md in the template's
    order. R14 read 98 and R15 read 59; if yours exceeds 100, declare the overage
    plainly — a repair that stopped working is a finding.

G15 THE VERDICT LANDED AND NOTHING ELSE MOVED. `.agent/handoff.md` as committed
    by C5 is a byte-exact PREFIX of the file at HEAD, and the remainder is
    byte-equal to the VERDICT slice. Report the remainder's full sha256 and line
    count.

G16 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report it verbatim; merge nothing.

Handback:
A FULL completion report — every gate, its real command, its real exit code, its
output and every digest at 64 characters — plus the SHORT `.agent/handoff.md` C5
writes and C6 extends. Push after C4 and again after C6. "Green" as a word is a
finding; a red gate is reported plainly, with raw output, and the round hands off.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN16>>>
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
R16, this round: the TRIGGER, and the session closes. A manual-trigger
`.github/workflows/release.yml` builds the wheel, reads this commit's real CI
conclusion and calls `scripts/release_gate_check.py`; text guards keep it manual,
thin and publish-free. Then the R15 verdict is recorded and the reviewer's own
session verdict is written to disk (finding R-0571).

## Next Steps
1. The install smoke T2_F086 T001 still owes: a fresh virtualenv, the wheel
   installed into it, `remedy` on PATH, and the golden path and the UI serve
   probed from it. The round that writes it must name its execution host.
2. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN. It is gated as TEXT, the way
   `tests/orchestration/test_ci_workflow.py` gates `ci.yml`. No round can
   dispatch it; its first real run is a human action, and its guards check what
   they say and nothing more.

## Risks
- The install smoke creates a fresh virtualenv and runs the wheel's console
  script. This session's permission layer refuses to execute any interpreter
  under `.remedy-wt/`, so the round that writes it must name its execution host
  or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
<<<END PLAN16>>>

<<<SLICE RECORD14>>>

Gate: R16 — the R15 entry. R15 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `6f5a589a..efc021d9` rather than read from the handback, and every reading reproduces. THE GATE NOW REFUSES SOMETHING REAL, which was the whole point of the round: `scripts/release_gate_check.py` observes a release from the built wheel's own FILENAME, `CHANGELOG.md` on disk and the wheel's real size, and the reviewer's own spot-check — outside pytest, against the COMMITTED script and the COMMITTED changelog, on a file one byte over the budget — exits 1 with `REFUSED: wheel is 8388609 B, over the 8388608 B budget`. That is the budget branch driven through `main()`, which no ordered gate had reached. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the primary checkout: 21 passed for the wiring and gate suites, 160 for the four state readers and 42 for the canary, each exit 0; ruff over both new Python paths exits 0 with an EMPTY rule-code multiset, and there is no base reading to compare against because both paths are absent at `6f5a589a`. THE TESTS CAN FAIL: in a worktree the single line `## [0.1.0] - 2026-08-20`, counted 1x in `CHANGELOG.md` first, was replaced by `## [0.1.0-broken] - 2026-08-20`, and the wiring suite read 3 failed / 6 passed naming exactly `test_the_declared_version_has_a_non_empty_section`, `test_this_repository_is_refused_for_no_reason_at_all` and `test_a_sound_release_exits_zero`, returning to 9 passed on revert with that worktree's `git status --porcelain` EMPTY. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: `.remedy-wt/f086-r15.md`, the committed `.agent/authored/f086-r15.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 32e7a86bc55f95bea3acdcb3c6dbc97530a5148fa217c16275a62994a1303819, 29861 B, 489 lines, and the block's own size sentence — 489 total, 244 prose, 245 slice — is what the reviewer re-measured from the committed file. EVERY SLICE LANDED BYTE-EXACT: `.agent/plan.md` equals PLAN15 at 015be2445b9af70bf33beabf960b61540d23b89d8676406b16ff70dcaa330c55 over 42 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals FIND0583 followed by RECORD13 at 5531598030afb293bae396508b6a40ff8de2772ce41d1ff57d6d43b169d8f3fc; `CHANGELOG.md` equals CHANGELOG at 6b16665e1009caf4a6c8b69f407e95181beb822991a64f6d772035174cacbff7 over 24 lines, `scripts/release_gate_check.py` equals RUNNER at 39990fb423b4d2b266730831f6c62f9aea307a500ef6677945ec89e2636954ab over 72 lines, and `tests/orchestration/test_release_gate_wiring.py` equals TESTS at 3a7ea729f2185afa66d0f9ecde7a7e879201efb74541ce4e38bbc120c1d1d6d0 over 91 lines — and those three digests are the SAME ones the reviewer measured on its own pre-emission dry run, so the bytes proved green before delegation are the bytes that landed. All three are ABSENT at `6f5a589a`, so all three commits are creations. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the six written files. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 165 registered / 2 resolved / 163 open at `6f5a589a` and 166 / 2 / 164 at HEAD with the two registered SETS equal, the symmetric difference is exactly `['R-0583']`, and the control over `3351878d..a662abcc` reads `['R-0582']`. THE HYGIENE HELD: eight paths over eight single-parent commits inserting 489, 404, 16, 4, 24, 72, 91 and 33 lines, none over 500 and no DECISION F104 D1 exemption invoked; `pyproject.toml`, `hatch_build.py`, `packages/orchestration/release_gate.py` and `.github/workflows/ci.yml` are absent from the range and all four exist at the base, and `.github/workflows/release.yml` is absent from the range AND at the base, which the block ordered reported precisely so the clause would not forbid nothing (R-0559). THE HANDBACK STAYED UNDER ITS CAP for the second round running: 59 lines against 100, all seven mandated headings in the template's order, no DECISION D15 overage — the R-0582 repair is holding.
<<<END RECORD14>>>

<<<SLICE WORKFLOW>>>
# Remedy's release gate, hosted. MANUAL TRIGGER ONLY: cutting a release is a
# human decision, so nothing here fires on a push, a tag or a schedule. Like
# ci.yml this file is a THIN WRAPPER — it builds the wheel, observes the real
# conclusion of this commit's CI run, and hands both to the gate runner under
# scripts/, which owns every rule. Remedy deliberately does not publish from CI:
# there is no upload step and no index credential here, because T2_F086's
# Do-not-touch keeps the final upload a HUMAN command.
name: Release gate

on:
  workflow_dispatch:
    inputs:
      tag:
        description: 'The tag being released, for example v0.1.0'
        required: true

# Read-only: the gate reads a CI conclusion and writes nothing back.
permissions:
  contents: read
  actions: read

jobs:
  gate:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: pip

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm
          cache-dependency-path: apps/ui/package-lock.json

      # The wheel must carry real UI assets: hatch_build.py fails the build when
      # apps/ui/dist is absent, so this step is a precondition of the next one.
      - name: Build the UI assets
        run: npm ci --prefix apps/ui && npm run --prefix apps/ui build

      - name: Build the wheel
        run: |
          python3 -m pip install build
          python3 -m build --wheel

      # The gate judges the CI run that really happened for THIS commit. When no
      # run exists the step reports 'missing', which is not 'success', so the
      # gate refuses rather than treating an absent answer as a green one.
      - name: Read this commit's CI conclusion
        id: ci
        env:
          GH_TOKEN: ${{ github.token }}
          COMMIT: ${{ github.sha }}
        run: |
          found=$(gh run list --workflow=ci.yml --commit="$COMMIT" \
            --limit 1 --json conclusion --jq '.[0].conclusion')
          echo "conclusion=${found:-missing}" >> "$GITHUB_OUTPUT"

      # The tag reaches the runner through the ENVIRONMENT, never interpolated
      # into a shell line, so a crafted tag cannot become a command.
      - name: Refuse the release unless every rule passes
        env:
          TAG: ${{ inputs.tag }}
          CI_STATUS: ${{ steps.ci.outputs.conclusion }}
        run: |
          built=$(ls dist/*.whl)
          python3 scripts/release_gate_check.py --tag "$TAG" \
            --wheel "$built" --ci-status "$CI_STATUS"
<<<END WORKFLOW>>>

<<<SLICE GUARDS>>>
"""Guards that keep the hosted release gate manual, thin and publish-free (T2_F086).

The workflow is read as TEXT and never parsed. PyYAML is in neither
`dependencies` nor the `dev` extra of `pyproject.toml`, so a `yaml.safe_load`
guard would raise ImportError on exactly the clean checkout these guards exist to
protect — the reasoning `test_ci_workflow.py` already records for `ci.yml`.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "release.yml"
RUNNER_PATH = "scripts/release_gate_check.py"


def workflow_text() -> str:
    """The hosted release workflow as text — the single subject of every guard."""
    return WORKFLOW_PATH.read_text()


def executable_lines() -> list[str]:
    """Every line of the workflow that is not a comment."""
    return [line for line in workflow_text().splitlines() if line.strip()[:1] != "#"]


def test_release_workflow_file_exists():
    """A gate that is not at the path GitHub reads gates nothing."""
    assert WORKFLOW_PATH.is_file(), WORKFLOW_PATH


def test_release_workflow_calls_the_gate_runner_exactly_once():
    """One owner of the rules: the workflow decides nothing of its own."""
    called = [line for line in executable_lines() if RUNNER_PATH in line]
    assert len(called) == 1, called


def test_release_workflow_is_triggered_by_hand_only():
    """Cutting a release is a human decision, so no event may fire this job."""
    text = workflow_text()
    assert "workflow_dispatch:" in text
    for event in ("\n  push:", "\n  pull_request:", "\n  schedule:", "\n  release:"):
        assert event not in text, event


def test_release_workflow_publishes_nothing():
    """T2_F086's Do-not-touch keeps the final upload a HUMAN command."""
    text = workflow_text().lower()
    for forbidden in ("twine", "pypi", "gh release create", "upload-artifact", "secrets."):
        assert forbidden not in text, forbidden


def test_release_workflow_never_auto_retries():
    """T2_F083 rules that retries hide rot; the release gate inherits that."""
    for token in ("continue-on-error", "retry", "max_attempts"):
        assert [line for line in executable_lines() if token in line] == [], token


def test_release_workflow_passes_the_tag_through_the_environment():
    """A tag interpolated into a shell line would be a command-injection seam."""
    assert '--tag "$TAG"' in workflow_text()
    carriers = [line for line in executable_lines() if "inputs.tag" in line]
    assert carriers, "the workflow never reads its own tag input"
    for line in carriers:
        assert line.strip().startswith("TAG:"), line


def test_release_workflow_refuses_when_no_ci_run_is_found():
    """An absent CI answer must not read as a green one."""
    assert "missing" in workflow_text()
<<<END GUARDS>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md. The reviewer wrote nothing in the work tree,
one delegated worker per round made every commit, and every verdict below rests
on gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R14 | a662abcc..6f5a589a | PASS — one finding, R-0583, against the reviewer |
| R15 | 6f5a589a..efc021d9 | PASS — no finding |
| R16 | efc021d9..HEAD | verdict not yet on disk; see the last paragraph |

R14 was inherited ungated, so Phase 1 rule 4 reviewed it first, and every ordered
property held. Its one defect is in its own appended verdict, which called R14 a
branch TERMINATOR: it was not one, the branch continued into R15 and R16, and
`Gate: R15 — the R14 entry` is now in the ledger. That is R-0583, and its
counter-measure is narrow — the terminator carve-out of §4 item 13 belongs only to
a round whose own bundle CREATES the branch's pull request.

R15 is the round that made the release gate real. Before it, `refuse_release`
decided correctly and nothing called it, so it refused nothing. After it there is a
`CHANGELOG.md` carrying the version `pyproject.toml` declares, and a caller reading
the version out of the built wheel's own filename rather than trusting a second
declaration that could drift. The reviewer's own spot-check, outside pytest and
against the committed script, refused a wheel one byte over the budget. R16 adds
the manual trigger, gated as TEXT the way `ci.yml` is gated, and publishing stays a
human command: the guards go red if a `push:` trigger, a `twine upload` step, or a
tag interpolated into a shell line ever appears — each proved by its own red
control rather than asserted.

WHAT THIS FEATURE STILL OWES: the install smoke, whose fresh-virtualenv step this
session's permission posture cannot execute; then the integration gate and closure.
The release workflow has never been dispatched, and no round can dispatch it.

R16 IS NOT A TERMINATOR — F086's pull request is created at closure, which has
not happened — so this session claims no carve-out and leaves its last verdict to
be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review `efc021d9..HEAD` and record R16's verdict in
`.agent/live_review.md` as `Gate: R17 — the R16 entry`.
<<<END VERDICT>>>
