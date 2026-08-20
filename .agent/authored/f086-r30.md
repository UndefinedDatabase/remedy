── STEP closure evidence and the review package — F086 R30 ────
Goal:
Record R29's verdict, then produce the two artifacts the closure protocol makes
mandatory and that nothing else in this feature can supply: the feature-scoped
EVIDENCE BUNDLE and a FRESH REVIEW ZIP built from a clean tree at the reviewed
head. This round also re-confirms closure precondition 2 by running the FULL
suite once more in the primary checkout. It commits no `docs/` and no `README.md`
change at all: the STATUS line, the README capability sync and the pull request
are R31's closure commit, and they are held back for one reason — the STATUS line
must quote the package filename, its SHA-256 and the accepted HEAD, and none of
those three values exists while this block is being written. Ordering a value that
cannot exist at authoring time is the R-0371 defect this workflow has paid for
seven times, so this round MEASURES those values and R31 authors them.

Bundle:
1. The block, saved and mirrored.
2. `.agent/plan.md` advanced to R30 (§3 item 23 — this round appends to the
   ledger, so the plan moves FIRST among the substantive commits).
3. `.agent/live_review.md` gains RECORD29.
4. The full-suite confirmation, the evidence bundle and the review zip — none of
   which is committed, and all of which are REPORTED.
5. The handback, carrying the four values R31 needs.

Change:
Exactly these paths:
  `.agent/authored/f086-r30.md`                   (C0a)
  `.agent/last_block.md`                          (C0b)
  `.agent/plan.md`                                (C1)
  `.agent/live_review.md`                         (C2)
  `.agent/handoff.md`                             (C3)
Nothing else, and this round's forbidden list is where its discipline lives: NOT
`docs/roadmap/STATUS.md`, not `README.md`, not `.agent/candidates.md`, not
`docs/system/release-capability-v1.md`, not `docs/README.md`, not
`docs/roadmap/features/T2_F086.md`, not `CHANGELOG.md`, not `pyproject.toml`, not
`hatch_build.py`, not `apps/cli/version_report.py`, not
`packages/orchestration/release_gate.py`, not `scripts/release_gate_check.py`, not
`.github/workflows/release.yml`, and nothing under `apps/`, `packages/`, `tests/`
or `docs/agents/`. Every path this paragraph FORBIDS exists at `ea4ac5fa` —
`.agent/candidates.md` included, which is why it is named rather than assumed —
each resolved with `git ls-tree` at emission per §3 item 24.

THE EVIDENCE DIRECTORY AND THE ZIP ARE NEVER COMMITTED. `.gitignore` excludes
`remedy-job-evidence-*/` at line 226 and `remedy-review-*` at line 223, both
verified at emission, and the evidence dir is written under `.remedy-wt/`, which
is excluded at line 235. A committed evidence dir puts evidence files into the
base..HEAD review subject and the package then builds BLOCKED_EVIDENCE — the F147
attempt-2 lesson, recorded in STATUS_closure_protocol.md.

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
   If a slice is wrong, apply it as written and DECLARE the problem in the
   handback; repairing it silently is the failure this rule exists to prevent.
   EVIDENCESCRIPT is a slice: it is written to `.remedy-wt/f086_r30_build_evidence.py`
   byte-for-byte and RUN, never retyped and never "fixed" on the fly.

2. The change set is the path list above and nothing else.

3. THE LANDED RECORD IS NOT REWRITTEN. The duplicate header `Gate: R19 — the R18
   entry.` that entered at `4dc7cbdf` stays exactly as it is (§3 item 20). You
   append only. G7 is written so the R19 duplicate is EXPECTED rather than
   forbidden.

4. EVERY SLICE IS THE REVIEWER'S TEXT. Do not summarise, rewrap or reformat one.
   Do not write a verdict of your own anywhere — not in the handoff, not in a
   commit message, not in your report (§4.4).

5. THE ZIP IS BUILT AT C2, FROM A CLEAN TREE, AND THAT COMMIT IS THE ACCEPTED
   HEAD. Order of operations is load-bearing and is the whole reason this round
   exists: C0a, C0b, C1, C2 commit; then `git status --porcelain` is confirmed
   EMPTY; then the full suite, the evidence bundle and the zip all run at C2
   without committing anything; then C3 writes the handback. The manifest's
   `committed_review_subject.head_commit` must therefore equal C2's SHA, and that
   value is what R31 will write as `accepted HEAD`.

6. HYGIENE. `git status --porcelain` in the PRIMARY checkout is EMPTY at every
   commit, before the zip build, and at the handback; `git worktree list` reads
   ONE line throughout — this round runs no destructive check and needs no
   worktree. NO FILE IN THE PRIMARY CHECKOUT IS OVERWRITTEN TO TAKE A READING (§3
   item 29): every reading at a non-current revision comes from
   `git show <sha>:<path>`.

7. THIS SESSION'S BASH GUARD refuses shell loops, `$( )`, `${arr[0]}`, `$?`,
   brace-with-quote literals (an inline Python dict or set literal counts) and
   env-prefix command forms. Route that work through `python3 - <<'PY'` heredocs
   or scripts under `.remedy-wt/`. Capture exit codes with
   `subprocess.run(...).returncode`, never with `$?`.

8. A RED FULL SUITE ENDS THE ROUND. If the confirmation run is not green, do NOT
   build the evidence bundle and do NOT build the zip: closure precondition 2 has
   failed, and the honest outcome is a handback naming the failing ids. Never
   deselect, never re-run until green, never raise a budget to pass a check.

9. THE ZIP IS A CLOSURE BLOCKER, NOT A FORMALITY. If `make_review_zip.sh` fails
   or reports anything other than a READY package, capture the RAW error in full
   and put it in the handback verbatim. Do not retry more than twice, do not
   improvise a different build route, and do not proceed to C3 pretending a
   package exists. A BLOCKED_EVIDENCE package is a FAILED zip for this purpose.

10. THE COMMITS TABLE IS A MEASUREMENT, NOT A RECOLLECTION (§3 item 28). Every
    `+/-` cell in the handback's `## Commits` table is READ OUT of
    `git diff --numstat <sha>^ <sha>` and pasted from that reading.

11. THE HANDBACK'S SIZE IS STATED ONCE, HERE, AND NOWHERE ELSE (§3 item 14's
    sweep rule). This round appends no verdict slice, so C3 is the only commit
    that writes `.agent/handoff.md`. KEEP C3 AT 60 LINES OR FEWER, the AGENTS.md
    cap. Write it in the COMPACT form: one commits table, ONE LINE PER GATE, the
    transcript in your round report and not in the file (R-0582). G13 NAMES this
    constraint instead of restating its numeral: measured at emission, `60`
    occurs in this constraint and in no other clause of this block. If C3 lands
    above the bound, do NOT drop a mandated section — exceed it and write the
    DECISION D15 "Deviations, declared" line with the real count and the cause.

12. THE HANDBACK CARRIES THE FOUR VALUES R31 NEEDS, in its `## Next` section and
    spelled exactly as the tools printed them: the evidence job id, the package
    FILENAME, the package SHA-256, and the accepted HEAD (C2's full 40-character
    SHA). R31 cannot author the STATUS line without all four, and a value
    paraphrased here is a value wrong there.

Done when:

G1 HYGIENE. `.agent/STOP` absent, read from disk before C0a and again at the
   handback; branch `feature/f086-release-capability`; constraint 6's readings all
   taken and reported, including that `git status --porcelain` was EMPTY
   immediately before the zip build and that no primary-checkout path was
   overwritten to take a reading.

G2 TRANSPORT. `.remedy-wt/f086-r30.md`, the committed `.agent/authored/f086-r30.md`
   and the committed `.agent/last_block.md` are all three byte-EQUAL. Report the
   shared sha256, the byte count and the line count.

G3 PLAN. `.agent/plan.md` at C1 is byte-equal to PLAN30 extracted programmatically
   from the COMMITTED C0a — never retyped. Report its sha256 and line count, which
   must be under 50 (AGENTS.md), and confirm it contains `## Goal`, `## Next Steps`
   and `F086` (§4.11 contract).

G4 LEDGER APPEND, proved in the prefix-and-remainder form against RECORD29
   extracted from the committed C0a: the pre-C2 blob is a byte-exact PREFIX of the
   post-C2 blob whose remainder is a blank line followed by RECORD29. Report the
   remainder's sha256 and line count. The blank separator is mandatory (R-0578).

G5 LEDGER SETS, with TWO independent extractions that must AGREE, plus a control.
   Registered = `^- R-\d+ — `; resolved = `^Done: R-\d+ — `. Report at `ea4ac5fa`
   and at C2: registered, resolved, duplicate, unregistered-resolution, `Landed:`
   and open counts. This round registers and resolves NOTHING, so assert the
   EQUALITY of the sets rather than predicting their sizes, and REPORT both counts.
   CONTROL, which must MOVE so an all-equal reading is not vacuous: the same two
   extractions over `f0b27118..7b84524c` report `[]` registered gained while the
   resolved set gains exactly `R-0584`.

G6 ITEM-20 SCAN. Over the lines C2 ADDS to `.agent/live_review.md`, delete every
   backtick-quoted span FIRST (R-0584), then count `\bHEAD\b` in what remains: it
   must read 0. RED CONTROL, the same two-step extractor over the lines `fd166295`
   adds to the same file: it must read 3, or the extractor is broken.

G7 ITEM-26 HEADER CHECK. Match `^Gate: R(\d+) — the R(\d+) entry\.` against
   `.agent/live_review.md`. Report the header count at `ea4ac5fa` and at C2 and the
   SET occurring more than once at each: that set must be UNCHANGED and exactly
   `Gate: R19 — the R18 entry.`. Then `Gate: R30 — the R29 entry.` occurs exactly
   1x, is the LAST such header, and the text that follows it on the same line
   begins `R29 ` once its leading space is stripped.

G8 CLOSURE PRECONDITION 3 — INTEGRITY. Run the gate through the MODULE, because
   the `remedy` CLI is denied to this session class:
   `python3 -c "import sys; sys.path.insert(0,'.'); from packages.orchestration.integrity_gate import run_integrity_checks; r=run_integrity_checks(); print([(c.name, c.status.value, c.message) for c in r.checks])"`
   Report every check's name, status and message. All five must be `pass`;
   `relevant_untracked` must report `untracked=0, relevant=0` and
   `high_blockers_open` must report no open blocker/high findings. Report this as
   met THROUGH THE MODULE and say so — never claim the CLI was run.

G9 CLOSURE PRECONDITION 2 — THE FULL SUITE, re-confirmed. In the PRIMARY checkout
   at C2, with no other pytest process running:
   `python3 -m pytest -n auto -q`. Report the exit code and the FULL final summary
   line verbatim — passed, failed, skipped, errors and wall time. Constraint 8
   governs a red result. Report the numbers beside the integration gate's own
   reading of `17192 passed, 20 skipped` at `39bfc199`, and if they differ, report
   the difference as a fact rather than reconciling it: rounds R24 through R29
   landed since, so the counts are not required to match and only a FAILURE ends
   the round.

G10 THE EVIDENCE BUNDLE. First write the five `-v` logs the script reads, one
    command each, serially, into `.remedy-wt/f086_r30_logs/`:
      `python3 -m pytest tests/test_packaging_smoke.py -v > .remedy-wt/f086_r30_logs/vr0001.txt`
      `python3 -m pytest tests/orchestration/test_release_gate.py -v > .remedy-wt/f086_r30_logs/vr0002.txt`
      `python3 -m pytest tests/orchestration/test_release_gate_wiring.py -v > .remedy-wt/f086_r30_logs/vr0003.txt`
      `python3 -m pytest tests/orchestration/test_release_workflow.py -v > .remedy-wt/f086_r30_logs/vr0004.txt`
      `python3 -m pytest tests/cli/test_golden_path.py -v > .remedy-wt/f086_r30_logs/vr0005.txt`
    The reviewer measured these five at 6, 12, 9, 7 and 42 passed with ZERO
    skipped at `ea4ac5fa`, which is why they and not the install smoke are the
    bundle's runs: `tests/test_install_smoke.py` reports 1 skipped and the
    producer's own assertion rejects a run with any skip. Then write
    EVIDENCESCRIPT verbatim to `.remedy-wt/f086_r30_build_evidence.py` and run it
    with `python3`. Report its printed per-run line and the final JSON summary,
    and confirm the summary's final verdict is READY and that the evidence
    directory exists under `.remedy-wt/f086_closure_evidence/`. If the script
    raises, report the traceback VERBATIM and stop — do not edit the script.

G11 THE REVIEW ZIP, mandatory and fresh. With `git status --porcelain` confirmed
    EMPTY, run exactly:
    `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f086_closure_evidence/remedy-job-evidence-f086-closure`
    Report the exit code, the printed package FILENAME and its SHA-256 verbatim.
    Then, from the package itself, report the manifest's
    `committed_review_subject` base and head commits, and confirm the head equals
    C2's full SHA and the base equals `76661dc1ff5ccc7cd4fe15ab88d53cff82d6d9dc`,
    which is where this branch was cut from `main`. Confirm the package name ends
    `READY_FOR_REVIEW.zip`; a `BLOCKED_EVIDENCE` package is a FAILURE under
    constraint 9. Finally confirm `git status --porcelain` is still EMPTY after
    the build, since both the zip and the evidence dir are gitignored.

G12 NO MARKER LEAKED. Count LINES beginning `<<<SLICE ` or `<<<END ` in
    `.agent/plan.md` and `.agent/live_review.md` at C3: each must be 0. Count
    marker LINES, not substrings — this handback quotes gate text, so a substring
    gate over `.agent/handoff.md` would be unmeetable (F086 R5).

G13 CHANGE SET, HISTORY AND THE HANDBACK. Print the range's path set and confirm
    it equals the Change list, with no path on either side alone — in particular
    confirm `docs/roadmap/STATUS.md`, `README.md` and `.agent/candidates.md` are
    NOT in it. Confirm every path the Change section FORBIDS is PRESENT at
    `ea4ac5fa` and untouched, that the range is linear, and that the round's
    `git reflog` entries are all `commit:`. Per constraint 10, for every commit
    BEFORE C3 print `git diff --numstat <sha>^ <sha>` and confirm each `+/-` cell
    of the handback's `## Commits` table is byte-identical to that pair, insertion
    column alone against the 500 cap (DECISION F104 D1); C3's own row goes in the
    round report (§3 item 14). Then report `wc -l` of `.agent/handoff.md` at C3
    against the bound CONSTRAINT 11 states — this gate names that constraint
    rather than restating its numeral — and confirm all seven mandated headings of
    docs/agents/handback_template.md are present in the template's order.

G14 OPEN PR GATE, re-read at the handback:
    `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
    Report its literal output. Create nothing and merge nothing: the pull request
    belongs to R31, together with the STATUS line and the README sync.

Handback:
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md — all seven
sections, one line per gate, the transcript in your round report instead. The
`## Next` section carries constraint 12's four values. Push the branch once, after
C3. This round appends no verdict: R30's verdict is recorded by R31's own ledger
commit.
──────────────────────────────────────────────────────────────

<<<SLICE PLAN30>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists yet: it belongs to R31, the closure commit.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R30: record R29's verdict, re-confirm the full suite, and build the two artifacts
closure cannot proceed without — the feature-scoped evidence bundle and a FRESH
review zip from a clean tree. It commits no `docs/` change and creates no PR.

## Next Steps
1. R31 IS THE CLOSURE COMMIT and the branch terminator. It is a round of its own
   because the STATUS line quotes the package filename, its SHA-256 and the
   accepted HEAD, and none of those exists before R30 measures them — ordering a
   value that cannot exist when the text is written is the R-0371 defect. R31
   authors the `[x]` STATUS line, the README capability sync in the SAME commit
   (R-0154: README and STATUS may never disagree in any committed state), any
   closure candidates into `.agent/candidates.md`, and the final `.agent` state,
   then creates the PR. Its path set is exactly those four areas.
2. THE PR IS NOT MERGED THIS SESSION. It merges at the next feature's start via
   the Open PR Gate, which is the operator's manual-review window; the operator
   may merge manually at any time instead.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- The review zip packages `.remedy-wt/`, registered as R-0403 and never paid
  down; it makes the package larger and is not a build failure.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs, so it is
  deliberately NOT one of the evidence bundle's verification runs.
- The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
- `remedy integrity check` is denied to this session class, so precondition 3 is
  met through `packages.orchestration.integrity_gate` and reported as such.
<<<END PLAN30>>>

<<<SLICE RECORD29>>>
Gate: R30 — the R29 entry. R29 PASSED with NO finding, the third such round in a row, and every gate its block ordered was RE-EXECUTED by the reviewer over `05c6e012..ea4ac5fa` rather than read from the handback. THE TRANSPORT HELD IN THE PRIMARY FORM AND PROVED THE ROUND'S OWN ORDER: `.remedy-wt/f086-r29.md`, the committed `.agent/authored/f086-r29.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 3c7aba5f2af0cf4958e4bdf131f5fa728cd35b614c4a9e13b75532803f9193ed over 32762 B and 475 lines, and that digest is the one the reviewer computed BEFORE delegating, so the block the worker executed is provably the block the reviewer authored. PLAN29 landed byte-exact at sha256 983b73027a5a1922e814e2b9703ab70df0f90333f2e38c4d521716f45abd9123 over 44 lines, under the 50-line cap and carrying `## Goal`, `## Next Steps` and `F086`; the 2-line C2 remainder is a blank line plus RECORD28 at sha256 8a67100852ff2a3f43e86b2eca35f8e9c659907edff3d4863fd94e8f69b00850, appended to a byte-exact prefix. THE LEDGER DID NOT MOVE, which is what a round registering nothing owes: both extractions AGREE at both ends at 179 registered / 6 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 173 open, the registered and resolved SETS are equal at `05c6e012` and at C2, and the control over `f0b27118..7b84524c` still MOVES — `[]` registered gained, exactly `R-0584` resolved gained — so the all-equal reading is not vacuous. THE SCANS HELD WITH THEIR CONTROL BITING: over C2's 2 added lines, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 while the same extractor over `fd166295`'s added lines reads 3; the duplicated-header set is unchanged at exactly `Gate: R19 — the R18 entry.`; and `Gate: R29 — the R28 entry.` occurs 1x, is the LAST such header, and its text begins `R28 ` once the separating space is stripped. THE IST-DOC LANDED AS ORDERED AND AS A CREATION: `docs/system/release-capability-v1.md` is absent at `05c6e012` and present at C3, its bytes equal the DOC slice at sha256 6f4a10254c81df2a53d8e90c5b4609833aed4428b8c255a6540ce542f93224fa over 154 lines, and the 154 lines C3's diff adds for that path are exactly the slice's lines IN ORDER, which is the §4.9 obligation for a code-or-document append and strictly stronger than the per-line count it replaces. BOTH INDEX PAIRS HELD IN THE APPEND FORM THEIR CONTAINMENT TESTS DICTATED — `TO contains FROM: True` for each, so no FROM-zero count was ordered or reported for either — with each FROM 1x at both ends, each TO 1x at C3, the ordered equality satisfied at sha256 4eeb90b7c2998ef2ebf04ecb790966d46672c28c8acc27cf889819f33d984d40 over 230 lines against the base's 228, and exactly 2 added lines of which each new row is 1x. THE ROUND'S CENTRAL CLAIM WAS PROVED BY THE REVIEWER INDEPENDENTLY AND IN BOTH DIRECTIONS, which is what makes R28's repair worth what it cost: at C3 the single case `TestPrimaryDocLinksResolve::test_every_relative_markdown_link_exists[docs/README.md]` — a case that exists ONLY because R28 repaired the parametrisation — PASSES over the two rows C3 added; and in a disposable worktree at C3 with both occurrences of `system/release-capability-v1.md` rewritten to a `-v0.md` that does not exist, that same case FAILS with `AssertionError: docs/README.md has broken links` naming both rows. The index rows are therefore not merely present but GUARDED, and the two rounds' ordering — repair the gate, then add the rows it judges — did exactly what it was designed to do. THE DOCUMENT IS TRUE AGAINST THE TREE, checked claim by claim before it was authored rather than after it landed: the console entrypoint, the `artifacts` carry and its measured 414-versus-417 member readings, the single hook class, the withdrawn dual-mode resolver and the test that still pins both modes, the `extra_metadata/REVISION` path, the five refusal rules and the 8 MiB budget with its two measured wheel sizes, the manual-dispatch-only workflow with its `contents: read` and `actions: read`, and the `REMEDY_INSTALL_SMOKE` opt-in that makes the install coverage zero — every one resolves in the file it names, and the page's own outbound link resolves on disk. THE SUITES ARE GREEN ON THE REVIEWER'S OWN SERIAL RUNS: `tests/docs/` 295 passed at exit 0, equal to the 295 at `05c6e012` and a count no new `docs/system/` page could move because nothing in this repository enumerates that directory; then the four-file state-reader selection 160 passed at exit 0; then the canary 42 passed at exit 0. THE HYGIENE HELD: seven paths over six single-parent commits, all thirteen forbidden paths present at `05c6e012` and none touched, every `git reflog` entry `commit:`, no marker LINE in any target, `git worktree list` one line and the tree clean, with the reviewer's own control worktree removed and pruned; item 28 bound for the fourth round running, with all five measurable `+/-` cells byte-identical to `git diff --numstat` and a maximum insertion column of 475 under the 500 cap; and the handback is 58 lines, inside its cap with no DECISION D15 overage owed and all seven mandated headings present in the template's order. THE TWO NOTES THE WORKER DECLARED ARE BOTH ITS OWN PROBE ARTEFACTS AND NEITHER TOUCHED THE WORK — a bash guard refusal it rerouted, and a heading-order check that read `False` because `## Next` occurs inside a quoted `` `## Next Steps` `` until it was line-anchored — and declaring them rather than quietly re-running is the behaviour this split exists to produce.
<<<END RECORD29>>>

<<<SLICE EVIDENCESCRIPT>>>
"""F086 R30 closure — build the evidence bundle with the canonical producer.

Scratch only; lives in the gitignored .remedy-wt/ so the evidence directory never
enters the base..HEAD review subject (STATUS_closure_protocol.md, "Evidence dir is
not committed"). Adapted in shape from the F115 R26 / F107 R20 / F105 R50 scripts
that produced READY packages.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = "/home/decodeux/Repos/remedy"
LOGS = os.path.join(REPO, ".remedy-wt", "f086_r30_logs")
EVIDENCE_DIR = os.path.join(REPO, ".remedy-wt", "f086_closure_evidence",
                            "remedy-job-evidence-f086-closure")

sys.path.insert(0, REPO)
os.chdir(REPO)

BASE = "76661dc1ff5ccc7cd4fe15ab88d53cff82d6d9dc"
HEAD = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                      cwd=REPO).stdout.strip()
assert len(BASE) == 40 and len(HEAD) == 40, (BASE, HEAD)

_NODE = re.compile(r"^(tests/\S+::\S+)\s+(?:PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)",
                   re.MULTILINE)


def _tail(text):
    """The last 2000 chars, on a WHOLE-LINE boundary, path-scrubbed TWICE.

    ``job_evidence._scrub_paths`` only relativises paths under REPO. A short
    pytest -v log keeps its header line inside the 2000-char window, and that line
    ends in the interpreter's own absolute path, which
    ``build_review_manifest._unsafe_text`` correctly rejects as a local absolute
    path -> BLOCKED_EVIDENCE. The second pass is the shared production redactor.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths
    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def parse(log_name):
    with open(os.path.join(LOGS, log_name), encoding="utf-8") as fh:
        text = fh.read()
    ids = _NODE.findall(text)
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    return ids, passed, failed, skipped, dur, _tail(text)


def mkrun(rid, command, log_name, expect, test_files=None):
    ids, passed, failed, skipped, dur, tail = parse(log_name)
    assert passed == expect, (rid, passed, expect)
    assert failed == 0 and skipped == 0, (rid, failed, skipped)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = test_files if test_files is not None else sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": command, "exit_code": 0,
        "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": 0, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": tail,
    }


runs = [
    mkrun("vr-0001", "python3 -m pytest tests/test_packaging_smoke.py -v",
          "vr0001.txt", 6),
    mkrun("vr-0002", "python3 -m pytest tests/orchestration/test_release_gate.py -v",
          "vr0002.txt", 12),
    mkrun("vr-0003", "python3 -m pytest tests/orchestration/test_release_gate_wiring.py -v",
          "vr0003.txt", 9),
    mkrun("vr-0004", "python3 -m pytest tests/orchestration/test_release_workflow.py -v",
          "vr0004.txt", 7),
    mkrun("vr-0005", "python3 -m pytest tests/cli/test_golden_path.py -v",
          "vr0005.txt", 42),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "files", len(r["test_files"]), "dur", r["duration_seconds"])

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f086-closure",
    job_title="F086 Release capability - closure",
    step_range="T001-T003",
    prior_job_ids=["f085-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F086 closure",
    review_feature_id="f086",
)
print(json.dumps(result, indent=2, sort_keys=True))
<<<END EVIDENCESCRIPT>>>
