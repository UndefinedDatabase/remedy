── STEP R20 — F255 Teacher role · CLOSURE EVIDENCE, REPAIRED ───
Goal:        Produce the two closure artifacts R19 could not, because the
             reviewer's own EVIDENCESCRIPT slice was defective. R19's SEVEN
             commits are all correct and none is redone: the plan, the R-0610
             resolution, the R18 verdict and the Built State section stay exactly
             as they landed. This round registers R-0611 against that slice,
             records the R19 verdict, and then runs a CORRECTED evidence job and
             builds the review zip. It authors no STATUS line; that is the next
             round's, because the line quotes values only this round can produce.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             register R-0611 · C3 record the R19 verdict · then the evidence job
             and the zip, from the clean tree at C3 · C4 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r20.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged in the TRACKED
             tree. NO source file and NO test file is touched, and NOTHING R19
             committed is amended or reverted. THE EVIDENCE DIR AND THE ZIP ARE
             NEVER COMMITTED. These paths are PRESENT at the base `b42cab39` and
             must stay untouched: `docs/roadmap/features/T5_F255.md`,
             `packages/orchestration/teacher_model.py`,
             `apps/cli/commands/teach_cmd.py`, `docs/roadmap/STATUS.md`,
             `README.md`. The last two are R21's closure commit and must not move
             early.

             WHAT WENT WRONG, SO THE REPAIR IS UNDERSTOOD RATHER THAN COPIED. The
             R19 EVIDENCESCRIPT built its node-id list by matching `-v` output
             against a pattern requiring a run of NON-WHITESPACE characters after
             `::`. One id in this feature's own suite is
             `tests/orchestration/test_teacher_qa.py::TestGroundingSourcesAreLabelled::test_no_code_fact_without_real_code`
             followed by a parametrised suffix CONTAINING SPACES, so 18 of 19 ids
             parsed, `len(node_ids) == selected` failed by one, and the script
             aborted before writing anything. The reviewer reproduced this at
             `b42cab39`: the same pattern yields 18 while the suite reports 19
             passed. THE FIX IS THE ROUTE THE CLOSURE PROTOCOL ALREADY NAMES —
             its producer-pitfall (a) says to run `--collect-only` for real ids —
             so node ids now come from a `--collect-only -q` listing, one id per
             line, and are never parsed out of `-v` output. The reviewer measured
             all six listings at `b42cab39`: 18, 19, 5, 38, 19 and 42 ids, each
             equal to that suite's passed count, with the whitespace id present
             and intact in the second.

             THE TWELVE CAPTURES, AFTER C3 AND FROM A CLEAN TREE. Run SERIALLY,
             never two pytest processes at once, writing into
             `.remedy-wt/.cache/r20_logs/`. For each suite capture BOTH a `-v`
             log, which supplies the counts, the duration and the stdout summary,
             and a `--collect-only -q` listing, which supplies the node ids:
               vr0001  tests/orchestration/test_teacher_model.py      expect 18
               vr0002  tests/orchestration/test_teacher_qa.py         expect 19
               vr0003  tests/orchestration/test_teacher_spend.py      expect 5
               vr0004  tests/orchestration/test_teacher_narration.py  expect 38
               vr0005  tests/cli/test_teach_cmd.py                    expect 19
               vr0006  tests/cli/test_golden_path.py                  expect 42
             naming them `vrNNNN.txt` and `vrNNNN.ids.txt`. The `-v` command is
             `python3 -m pytest <suite> -v` and the listing command is
             `python3 -m pytest <suite> --collect-only -q`. Every one must exit 0
             with 0 failed and 0 skipped. THE FULL SUITE IS DELIBERATELY NOT A
             VERIFICATION RECORD: a full-suite node-id list packages
             BLOCKED_EVIDENCE, and that proof rides in the committed
             `.agent/gate_f255_r18/` evidence instead.
             Then save the EVIDENCESCRIPT2 slice to
             `.remedy-wt/.cache/r20_evidence.py` and run it UNEDITED with
             `python3`. It writes the bundle to
             `.remedy-wt/f255_closure_evidence/remedy-job-evidence-f255-closure`.
             If that directory already exists from a previous attempt, DELETE it
             first so the bundle is built from scratch rather than merged into a
             stale one. Report the summary dict it prints, in full.

             THE REVIEW ZIP, MANDATORY AND FRESH. With the tree still clean and
             the branch pushed, run
             `bash scripts/make_review_zip.sh --evidence-dir <the bundle dir>`
             and report its REAL output: the final zip filename, its SHA-256 and
             the PACKAGE_STATUS, plus the manifest's `committed_review_subject`
             base and head commits. A FAILING ZIP BUILD IS A CLOSURE BLOCKER —
             report the raw error, write the handback and end the round. Do NOT
             assert the bundle contains the value `READY`: `READY_FOR_REVIEW` is
             the ZIP's vocabulary while the bundle's own verdicts read `PASS` or
             `PASS_WITH_RISKS` (R-0597). Report what each artifact really says.

Constraints:
1. NO SLICE IS EDITED, including EVIDENCESCRIPT2, which is SAVED AND RUN
   UNEDITED. If it too proves defective, DECLARE that with the real traceback and
   end the round; do not repair a reviewer's script on your own initiative. R19's
   worker did exactly that and it is why this repair is possible.
2. TRANSPORT. `.remedy-wt/f255-r20.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r20.md` and C0b copies the same file to
   `.agent/last_block.md`. Prove all three byte-EQUAL.
3. THE PLAN COMES FIRST (R-0377, R-0491, R-0548). Only C0a and C0b precede it.
4. THE FINDING PERSISTS BEFORE THE VERDICT. C2 registers R-0611 and C3 records
   the R19 verdict, in that order (§4.4). This round registers ONE finding and
   resolves NONE: registered goes 186 to 187, resolved stays 4, open goes 182 to
   183.
5. BOTH APPENDS ARE BLANK-SEPARATED (R-0578), each preceded by exactly one blank
   line, and FIND0611 and RECORDR19 are EACH single-paragraph — the reviewer
   measured each for an interior blank line and found none — so the LAST-UNIT
   paragraph reading is exact for each.
6. THIS ROUND CONTAINS NO FROM/TO PAIR (§4.9, R-0207).
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
8. THE EVIDENCE DIR AND THE ZIP ARE NEVER COMMITTED, AND THE ZIP IS BUILT FROM A
   CLEAN TREE AFTER C3 WITH THE BRANCH PUSHED. A package built from a dirty tree
   is invalid.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit, immediately BEFORE the
    zip build, and at the handback. No git worktree is created.
11. YOU DO NOT WAIT ON ANY CI RUN, YOU CREATE NO PULL REQUEST, and you edit
    NEITHER `docs/roadmap/STATUS.md` NOR `README.md`.
12. THE FORTSCHRITT LINE THIS BLOCK MANDATES IS TRUE ONLY IF THE ZIP IS BUILT. If
    the zip does not build, say so in the handback IN PLACE of that line rather
    than carrying a sentence the disk contradicts — R19 carried a mandated line
    whose third clause was false and had to annotate it, and that is the
    reviewer's defect to avoid repeating, not the worker's to inherit.

<<<SLICE PLAN255R20
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R20 REPAIRS the closure evidence. R19 committed everything correctly and could
not build its artifacts because the reviewer's evidence script parsed node ids
out of `-v` output and one parametrised id in this feature's own suite contains
whitespace. This round registers that as R-0611, records the R19 verdict, and
re-runs the evidence job with ids taken from `--collect-only`, then builds the
review zip.

## Next Steps
1. R21 CLOSES THE FEATURE: the reviewer authors the STATUS `[x]` line from the
   values THIS round's zip reports, the worker applies it verbatim in the SAME
   commit as the README capability sync (R-0154), writes any closure candidates
   to `.agent/candidates.md`, and opens the pull request. That PR is NOT merged
   in its own session; it merges at the NEXT feature's Open PR Gate, which is the
   operator's manual-review window.

## Risks
- A FAILING ZIP IS A CLOSURE BLOCKER, not a retry. The feature goes `[!]` with a
  stated reason rather than closing without a package.
- THE CLOSURE PRECONDITIONS OTHER THAN THE PACKAGE ARE MET AND MEASURED: the
  integrity gate passes with no open blocker or high finding, the Built State
  section landed at R19, the full suite passed the R18 gate with 0 branch-only
  failures, and the tree is clean and pushed.
- R-0607, R-0608, R-0609 AND R-0611 REMAIN OPEN by design: all four are
  reviewer-process defects whose fixes edit `docs/agents/` or the closure
  protocol, paths the closure commit's own R-0154 path set cannot reach.
<<<END PLAN255R20
<<<SLICE FIND0611
- R-0611 — Medium — A REVIEWER-AUTHORED EVIDENCE SCRIPT BUILT ITS NODE-ID LIST BY PARSING `-v` OUTPUT, AND A PARAMETRISED ID CONTAINING WHITESPACE MADE THE CLOSURE ARTIFACTS UNBUILDABLE. The EVIDENCESCRIPT slice of the F255 R19 block, committed at `c331d481`, extracted node ids with a pattern requiring `tests/` followed by runs of NON-WHITESPACE around `::`. This feature's own suite contains `tests/orchestration/test_teacher_qa.py::TestGroundingSourcesAreLabelled::test_no_code_fact_without_real_code` with a parametrised suffix whose value is whitespace, so the pattern stopped at the first space and yielded 18 ids for a suite reporting 19 passed. `create_manual_completion_bundle` was never reached: the script's own `len(ids) == selected` assertion fired first, `AssertionError: ('vr-0002', 18, 19)`, and it exited 1 identically on both attempts. NO EVIDENCE DIRECTORY AND NO ZIP WERE PRODUCED, so F255 could not close in that round. Re-measured by the reviewer at `b42cab39`: the same pattern returns 18 ids against 19 passed, while `python3 -m pytest tests/orchestration/test_teacher_qa.py --collect-only -q` returns 19, the whitespace id present and intact; across all six scoped suites the listings return 18, 19, 5, 38, 19 and 42, each equal to that suite's passed count. THE COUNTER-MEASURE WAS ALREADY ON DISK AND THE BLOCK DID NOT USE IT: docs/roadmap/STATUS_closure_protocol.md's producer-pitfall (a) states that verification records need non-empty node ids with `len(node_ids) == selected` and says, in the same clause, to run `--collect-only` for real ids. The reviewer instead re-derived an id extractor from the F086 R30 script, which had never met a parametrised id containing whitespace, and so carried a latent defect forward as though it were proven practice — the R-0452 and R-0454 shape, a rule that lives in a document the block did not consult. THIS IS NOT A DUPLICATE OF R-0448 OR R-0490, and the open set was searched for the DEFECT before this id was minted, as item 30 requires: both are OPEN, both are closure-block defects that produced a BLOCKED_EVIDENCE PACKAGE — an unsorted `test_files` list and an `output_hash` taken over the wrong text — and both were repaired inside their own round because a package existed to diagnose. This one aborts EARLIER, before any bundle is written, so there is no package and no validator message to read, and its fix is a different clause of the same pitfall list. WHY MEDIUM: nothing false reached disk and no work is wrong — R19's seven commits are all correct and none needs redoing — but the round could not meet its goal, the closure slipped a round, and a mandated Fortschritt line claiming the artifacts were built landed in `.agent/handoff.md` at `b42cab39` where the worker had to annotate it as false rather than carry it silently. FIX: node ids for a verification record come from a `--collect-only -q` listing, one id per line, and are never parsed out of `-v` output; the `-v` log supplies only counts, duration and `stdout_summary`. The reviewer runs the script's own assertions against the real logs BEFORE emitting the block that orders it, which is checklist item 12's dry-run rule applied to an authored script rather than to a gate command.
<<<END FIND0611
<<<SLICE RECORDR19
Gate: R20 — the R19 entry. R19'S SEVEN COMMITS ARE ALL CORRECT AND ITS GOAL IS UNMET, and both halves of that sentence are load-bearing. THE CLOSURE ARTIFACTS DO NOT EXIST: the reviewer confirmed at `b42cab39` that `.remedy-wt/f255_closure_evidence` is absent from disk and that no review zip was produced by this round, so nothing in this record may be read as a package, and R21 cannot write a STATUS line until R20 builds one. THE CAUSE IS THE REVIEWER'S OWN SLICE, registered this round as R-0611: the EVIDENCESCRIPT extracted node ids from `-v` output with a non-whitespace pattern, one parametrised id in `tests/orchestration/test_teacher_qa.py` contains spaces, 18 ids parsed against 19 passed, and the script's own assertion aborted it before `create_manual_completion_bundle` was ever called. THE WORKER'S CONDUCT IS THE REASON THE REPAIR IS CHEAP: it saved the slice byte-equal, ran it UNEDITED, reproduced the failure identically twice, measured the exact cause down to the offending id, and then STOPPED — it did not edit the reviewer's script, did not substitute `--job-id` for `--evidence-dir`, did not hand-build a bundle, and did not package an evidence-less NO_EVIDENCE snapshot that would have misreported a feature which is not docs-only. Each of those shortcuts would have produced an artifact and a false record; refusing all four is what constraint 1 exists to produce. EVERYTHING ELSE R19 WAS ASKED FOR LANDED AND VERIFIES, re-measured by the reviewer rather than read from the handback. Transport: `.remedy-wt/f255-r19.md`, `.agent/authored/f255-r19.md` at `c331d481` and `.agent/last_block.md` at `9a67a1c7` byte-EQUAL at sha256 2932c9f6ccae2646699b065991fe11441552557bba7b9b1d7739c111330001ee over 32800 B and 441 lines, the digest stated at delegation. FIVE SLICES, a count from the reviewer's own ordered extraction: PLAN255R19 2293 B 41 lines; DONE0610 1761 B 1 line; RECORDR18 4775 B 1 line; BUILTSTATE 3657 B 53 lines; EVIDENCESCRIPT 4066 B 108 lines. THE PLAN LANDED FIRST at `f8bb754c`, byte-equal to PLAN255R19 at 41 lines, under the 50-line cap, with `## Goal` and `## Next Steps` each once and the F-id present. R-0610 IS RESOLVED at `e49dc4da` and the R18 VERDICT IS RECORDED at `312f236d`, in that order, each a byte-exact prefix-plus-remainder append preceded by exactly one blank line. THE SETS MOVED BY EXACTLY ONE RESOLUTION: 186 registered / 3 resolved / 183 open / 0 line-anchored `Landed:` at `195b6cf3`, then 186 / 4 / 182 / 0 at both `e49dc4da` and `312f236d`, a `Gate:` paragraph adding neither kind of line. CLOSURE PRECONDITION 4 IS NOW TRUE: `## Built State` occurs 0x in `docs/roadmap/features/T5_F255.md` at `195b6cf3` and 1x at `d8a3dda4`, and the section names every module F255 shipped, the four DECISIONs that shaped them and the deliberate absences. CLOSURE PRECONDITION 3 HOLDS, measured through the same code the denied CLI runs: `run_integrity_checks` reports passed=true, fail_count=0 over five checks, with `high_blockers_open` reading "no open blocker/high findings" — which is what makes the whole open set a documented Medium or Low risk rather than a bar to closure — and `relevant_untracked` reading 0. THE SIX SCOPED SUITES ARE GREEN AND SERIAL at 18, 19, 5, 38, 19 and 42 passed, 0 failed and 0 skipped throughout, and the canary and the state-reader four are exit 0 at 42 and 160 passed. THE RANGE HOLDS: six paths over seven single-parent commits, insertions 441, 392, 19, 2, 2, 54 and 41, every one under the 500 cap; neither `docs/roadmap/STATUS.md` nor `README.md` appears in the range, which is what the block required of a round that must not close early; zero marker leaks; the tree clean and `origin/feature/f255-teacher-role` equal to the branch tip. THE HANDBACK IS HONEST ABOUT ITS OWN MANDATED TEXT, which is the detail worth keeping: the Fortschritt line this reviewer ordered verbatim claims the evidence job and review zip were built at that round, the disk says otherwise, and the worker carried the line as ordered while stating directly above it that the clause is false as measured. A handback that contradicts its own mandated sentence rather than quietly rewriting it is the correct resolution of two rules that could not both hold, and the defect is the reviewer's for mandating a sentence about an outcome the round had not yet reached.
<<<END RECORDR19
<<<SLICE EVIDENCESCRIPT2
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.path.abspath(".")
LOGS = os.path.join(REPO, ".remedy-wt", ".cache", "r20_logs")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f255_closure_evidence", "remedy-job-evidence-f255-closure"
)
BASE = "b35d350b84b1d371064a1f44e43f40da3ccfa540"

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE.

    job_evidence._scrub_paths only relativises paths under REPO. A short pytest -v
    log keeps its header inside the 2000-char window and that line ends in the
    interpreter's own absolute path, which build_review_manifest._unsafe_text
    correctly rejects as a local absolute path -> BLOCKED_EVIDENCE.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def read(name):
    with open(os.path.join(LOGS, name), encoding="utf-8") as fh:
        return fh.read()


def mkrun(rid, command, log_name, ids_name, expect):
    """One verification record.

    Node ids come from the --collect-only listing and are NEVER parsed out of -v
    output: a parametrised id may contain whitespace, and a non-whitespace
    pattern silently drops it, which is finding R-0611. The -v log supplies only
    the counts, the duration and the stdout summary.
    """
    text = read(log_name)
    ids = [line for line in read(ids_name).splitlines() if line.startswith("tests/")]
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert passed == expect, (rid, passed, expect)
    assert failed == 0 and skipped == 0, (rid, failed, skipped)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    assert all(ids), (rid, "empty node id")
    files = sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": command, "exit_code": 0,
        "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": 0, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


SUITES = [
    ("vr-0001", "tests/orchestration/test_teacher_model.py", "vr0001", 18),
    ("vr-0002", "tests/orchestration/test_teacher_qa.py", "vr0002", 19),
    ("vr-0003", "tests/orchestration/test_teacher_spend.py", "vr0003", 5),
    ("vr-0004", "tests/orchestration/test_teacher_narration.py", "vr0004", 38),
    ("vr-0005", "tests/cli/test_teach_cmd.py", "vr0005", 19),
    ("vr-0006", "tests/cli/test_golden_path.py", "vr0006", 42),
]

runs = [
    mkrun(rid, "python3 -m pytest " + suite + " -v", stem + ".txt", stem + ".ids.txt", expect)
    for rid, suite, stem, expect in SUITES
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
    job_id="f255-closure",
    job_title="F255 Teacher role - closure",
    step_range="T001-T004",
    prior_job_ids=["f086-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F255 closure",
    review_feature_id="f255",
)
print(json.dumps(result, indent=2, sort_keys=True))
<<<END EVIDENCESCRIPT2

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit, immediately BEFORE the zip build, and at the handback;
   `git worktree list` reports the primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r20.md`, of `.agent/authored/f255-r20.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r20.md` by its markers; report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING (R-0604).
   Report also that `.remedy-wt/.cache/r20_evidence.py` byte-equals
   EVIDENCESCRIPT2.
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R20; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report that C1
   is the FIRST commit other than C0a and C0b.
G5 THE FINDING AND THE VERDICT. Over `.agent/live_review.md`, for C2 and then for
   C3: the previous blob is a byte-exact PREFIX; the remainder's sha256, byte and
   line counts; that it equals one newline followed by FIND0611 and by RECORDR19
   respectively; and that the byte after each leading newline is not a newline.
   For EACH, a SECOND, INDEPENDENT blank-line paragraph split whose LAST unit is
   that commit's appended slice, with its sha256 under BOTH newline conventions.
   Re-measure constraint 5 rather than trusting it. Negative control for each:
   one character of the expected remainder mutated, rejected by BOTH readings.
G6 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` at `b42cab39`, at C2 and at C3, the registered count being lines
   matching `^- R-\d+ — ` and the resolved count lines matching
   `^Done: R-\d+ — `: the reviewer measured 186 / 4 / 182 / 0 at `b42cab39`; C2
   owes 187 / 4 / 183 / 0; and C3 owes the same as C2. Report that `R-0611`
   occurs 0x at `b42cab39`, that `Gate: R20 — the R19 entry.` occurs 1x at C3 and
   is the LAST line beginning `Gate: R`, and that every such header key is
   distinct. COUNT LINE-ANCHORED, never as substrings — R19 correctly reported
   that its own header string also occurs mid-sentence inside an older finding's
   prose, which a substring count would have read (R-0584).
G7 THE TWELVE CAPTURES. Report, per suite, the two exact commands, their exit
   codes, the `-v` summary line, and the number of lines beginning `tests/` in
   the `--collect-only` listing. Each `-v` run must be exit 0 with the passed
   count the Change section states, 0 failed and 0 skipped; each listing's id
   count must EQUAL that passed count. State that all twelve ran SERIALLY. State
   explicitly whether the `vr0002` listing contains an id with a space in it, and
   quote that id.
G8 THE EVIDENCE JOB. State whether the evidence directory existed before the run
   and, if so, that it was deleted first. Report the exact command, its exit code
   and the FULL summary dict `r20_evidence.py` printed, plus the number of
   entries in the bundle directory. Report the `verdict` values that actually
   appear in the summary dict and in `final_verifier_report.json` — report what
   they SAY and assert no particular value (R-0597). If the script aborts,
   report the real traceback verbatim and end the round under constraint 1.
G9 THE REVIEW ZIP, from a clean tree after C3 with the branch pushed. Report the
   exact command, its exit code, the final zip FILENAME, its SHA-256 and the
   PACKAGE_STATUS, all as the script really printed them, and the manifest's
   `committed_review_subject` base_commit and head_commit, stating whether that
   head equals the commit C3 created. A FAILING BUILD IS A BLOCKER: report the
   raw error, write the handback and end the round.
G10 THE CANARY AND THE STATE READERS, UNCONDITIONALLY (R-0607's rule), serially
   in the PRIMARY checkout, never two pytest processes at once:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed at
   `b42cab39`. Report the exact command, exit code and tail of each.
G11 THE INTEGRITY GATE, closure precondition 3, re-measured at this round's head.
   The `remedy` CLI is denied in this session class, so run the SAME code it runs:
   `run_integrity_checks()` then `export_integrity_json()` from
   `packages.orchestration.integrity_gate`. Report `passed`, `fail_count` and the
   status of every named check. The reviewer measured passed=True, fail_count=0
   over five checks at `b42cab39`.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only b42cab39..<C3>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C4
   itself adds, with no path on either side alone — and that NEITHER
   `docs/roadmap/STATUS.md` NOR `README.md` appears in it. Report that each path
   named untouched is PRESENT at the base and ABSENT from the range; that every
   commit has one parent; and each commit's insertion column from
   `git diff --numstat` for C0a through C3, every one under 500, with the same
   `+/-` cells appearing byte-identically in the handback's `## Commits` table.
   C4's own cell belongs to the round report (R-0149). Report also that NOTHING
   R19 committed was amended or reverted: `git log --oneline b42cab39..<C3>`
   names only this round's commits.
   THE REFLOG IS TWO MEASURED CLAIMS (R-0601, R-0605): report the count of this
   round's entries whose OPERATION PREFIX reads exactly `commit`, WITH the commit
   it was taken at and the number of commits made AT THAT MOMENT, and state the
   two are equal; state no total (R-0494). Report the count whose prefix contains
   `amend`, `rebase` or `cherry`, which must be 0, and for EVERY `reset` entry
   report it with the demonstration that its destination is the commit the branch
   already pointed at (R-0608).
G13 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C3 and `.agent/handoff.md` at C4 — every count 0. `git push` after C3 and
   again after C4, reporting real output each time; the branch must be pushed
   BEFORE the zip is built.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C4 bundle, the `## Commits` table G12 pins, and
             one LINE per gate rather than its transcript (R-0582). Its
             `## External actions` section records the evidence job and the zip
             attempt WITH their outcomes — package filename, SHA-256 and
             PACKAGE_STATUS, or the raw error. Its `## Next` section names the
             next session's FIRST action as Phase 1 rule 1, the `.agent/STOP`
             re-read, and its SECOND as R21, the CLOSURE COMMIT: the reviewer
             authors the STATUS `[x]` line from the values THIS round reports, the
             worker applies it verbatim in the SAME commit as the README
             capability sync (R-0154), and opens the pull request, which is NOT
             merged in its own session. It states that R19's seven commits are all
             correct and that its goal was unmet, that R-0611 is registered at C2
             and the R19 verdict recorded at C3, that R-0607, R-0608, R-0609 and
             R-0611 remain OPEN, and that R20 ITSELF IS THE ROUND WHOSE VERDICT IS
             NOT ON DISK. It states that no pull request is open.
             IF AND ONLY IF the zip built, the handback carries this Fortschritt
             line verbatim (R-0418):
             Fortschritt: ~97 % (T001 through T004 COMPLETE and REVIEWED · the
             integration gate PASSED with 0 branch-only failures · evidence job
             and review zip built at this round · only the STATUS line, the README
             sync and the pull request remain) — Schätzung
             If the zip did NOT build, write instead a Fortschritt line of your
             own that states the real position, and say plainly that the mandated
             line was withheld because its claim would be false (constraint 12).
──────────────────────────────────────────────────────────────
