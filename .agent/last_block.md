# STEP — F037 Rendered diff viewer, round 26 — EVIDENCE AND THE REVIEW ZIP

## Who you are and what binds you

You are the WORKER of a self-drive round (docs/agents/self_drive_protocol.md).
AGENTS.md is the highest authority and nothing here weakens it. You are the only
actor in this round that writes anything; the reviewer re-runs every gate itself
before issuing a verdict, so a number you report and a number that is true must
be the same number.

BASE. This round starts from commit `f676042c`, the tip of branch
`feature/f037-rendered-diff-viewer`. Read `.agent/STOP` from disk before your
first commit; if it exists, write the handback and end without doing anything
else.

SESSION. Session 8 of F037, round 26. This session's rounds are R25 (PASSED),
R26 (this one) and R27, which ends the session and the feature. Carry "SESSION 8
of feature F037 · round 26 · rounds so far 26" in the handback's Session section.

WHAT THIS ROUND IS. Steps 1 and 2 of docs/roadmap/STATUS_closure_protocol.md,
plus the Built State section its precondition 4 requires. A FAILING ZIP BUILD IS
A CLOSURE BLOCKER, never something to work around.

## Goal

Bring F037 to where only the STATUS line remains: the feature file records what
was built, the R25 verdict is in the ledger, and a READY review package with its
SHA-256 sits in the operator's archive.

## Bundle, in this commit order

- C0a — save the block verbatim to `.agent/authored/f037-r26.md`.
- C0b — mirror the same bytes into `.agent/last_block.md`.
- C1 — rewrite `.agent/plan.md` from the PLANF037R26 slice.
- C2 — append GATER25 to `.agent/live_review.md`.
- C3 — append the BUILTSTATE slice to `docs/roadmap/features/T5_F037.md`.
- Then, from the CLEAN TREE AT C3 and before any further commit, run the evidence
  job and build the review zip. C3 is the accepted head the package records.
- C4 — rewrite `.agent/handoff.md` as the handback, carrying the package name,
  its SHA-256 and its archived path, then push.

## Change set — these paths and nothing else

- `.agent/authored/f037-r26.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `docs/roadmap/features/T5_F037.md`
- `.agent/handoff.md`

Nothing under `apps/`, `packages/` or `tests/` is touched, and no test is edited,
added, deleted or skipped. Neither the evidence directory nor the zip is ever
committed; both are gitignored, and their durable record is the STATUS line R27
writes.

## Slice convention

The authored texts below are delimited by lines beginning `<<<SLICE ` and
`<<<END `, each naming its own label. The delimiter lines are transport markers
and never reach a target file. Apply each slice BYTE FOR BYTE, including its
trailing newline and excluding the delimiter lines. The labels used below are
PLANF037R26, GATER25, BUILTSTATE and EVIDENCESCRIPT. EVIDENCESCRIPT is the ONE
slice not applied to a tracked file: you write it to
`.remedy-wt/f037_evidence.py` and execute it from the repository root.

<<<SLICE PLANF037R26
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS and the design amendments A1 through A6, the last of
which records what this feature deliberately no longer ships.

## Current Step
R26 is the EVIDENCE-AND-ZIP round, the second of F037's closure sequence. The
integration gate PASSED at R25: branch and merge base each showed one failure,
both serial-pass flakes, with no branch-only failure reaching feature code. This
round books the R25 verdict, appends the feature file's Built State section so
closure precondition 4 holds, then builds the `f037-closure` evidence bundle and
a FRESH review package from the clean tree at the Built State commit. Nothing
under `apps/`, `packages/` or `tests/` is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R25 verdict | ordered | record first |
| C3 the Built State section | ordered | closure precondition 4 |
| the evidence job and the review zip | ordered | from the clean tree at C3 |
| C4 the handback | ordered | carries package, hash and path |

## Next Steps
1. The STATUS round: the `[x]` line for F037, the README capability paragraph,
   the README accepted count with its `Next:` clause and the README tier row —
   all four in the SAME commit — then the closure PR, which is not merged here.
2. The split-off scope of amendment A6 wants its own STATUS line. That remains a
   PROPOSAL to the operator and is executed by no session.

## Risks
- A failing zip build is a closure BLOCKER, not a deviation. If it packages
  BLOCKED_EVIDENCE, the round stops and hands back with the raw error.
- `R-0714` stays open and is carried into closure as a documented Medium risk:
  it is a defect in a ui_server test, out of F037's scope, and fixing it here
  would be scope drift.
<<<END PLANF037R26

<<<SLICE GATER25
Gate: F037 R25 — the INTEGRATION-GATE round, the first of F037's closure sequence. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each one independently at `f676042c` rather than reading the handback's numbers. TRANSPORT IS PROVED AT ITS STRONGEST AVAILABLE LINK, and for once that is stronger than the two rounds before it: the reviewer's own scratch original `.remedy-wt/f037-r25-block.md` was written BEFORE the worker existed, and the committed `.agent/authored/f037-r25.md` blob is BYTE EQUAL to it at 25345 bytes, 346 lines, sha256 `790f708e7f3492ea3a369baf52f0a54b67a74ec214528dc54dc1a9d5da4c9980` — so this chain covers the EMISSION and not merely the worker's self-consistency, which is the distinction the checklist's transport item requires a verdict to state. At `fe72ccae` the authored path and `.agent/last_block.md` are ONE blob `0888befa412e7ae0923fa7f14fd7a5f00d8c57c3`.

EVERY SLICE WAS RE-EXTRACTED FROM THE COMMITTED BLOB AND RE-APPLIED BY THE REVIEWER. `.agent/plan.md` at `3d99164d` is byte equal to PLANF037R25 including its trailing newline, the control dropping that newline is False, and the file is 44 lines with exactly one `## Goal` and one `## Next Steps`. The two-slice append at `9a7e5f16` satisfies reader (a) byte for byte with a control flipped inside the FIRST appended paragraph REJECTED, and the pre-round blob is a byte PREFIX at 1316230 bytes growing to 1322142; reader (b) counted 6 blank-line units against the two slices' 6 paragraphs, matching IN ORDER. THE RECORD MOVED EXACTLY AS THE BLOCK PREDICTED BEFORE THE ROUND RAN: registrations UNMOVED at 292 and all 292 DISTINCT, `^Done: R-\d+ — ` 42 to 43, `^Landed: R-` UNMOVED at 11, `^Gate: F\d+ R\d+ — ` 94 to 95, and the OPEN SET computed AS A SET fell from 252 to 251, with `Gate: F037 R24` and `Done: R-0719` each occurring exactly once.

THE INTEGRATION GATE ITSELF, which is what this round existed to produce. Dist was measured WARM before the branch run and nothing was rebuilt in the primary checkout beforehand. Branch at `9a7e5f16`: exit 1, 161.0s, 18118 passed, 20 skipped, ONE `FAILED` line. Base at merge base `9dde54956afbe5f432bfd429bf4ba0bb272f6d07` in a throwaway worktree on a real branch: exit 1, 155.2s, 17981 passed, ONE `FAILED` line. Branch-only 1 id, base-only 1 id, intersection EMPTY, both lists recorded in full and neither truncated. The branch-only id is `tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_the_suite` and the base-only id is `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`; the worker re-ran each SERIALLY ten times and each passed 10 out of 10, which is the xdist-flake class the procedure records rather than blocks on. NEITHER FILE IS AMONG THE PATHS THIS BRANCH CHANGED and neither reaches feature code. THE REVIEWER DID NOT TAKE THAT ON TRUST AND HAS ITS OWN INDEPENDENT MEASUREMENT: before delegating this round the reviewer ran `python3 -m pytest -n auto -q` itself at `38966bf3` and got exit 0 with 18119 passed, 20 skipped and ZERO `FAILED` lines, and after the round it re-ran the branch-only node id serially and it passed. The flake classification therefore rests on two independent runs by two actors, not on one.

PARITY IS VOID AND WAS HANDED BACK VOID RATHER THAN REPAIRED, which is the honest outcome and the one the block ordered. All four files under the base worktree's `apps/ui/dist` carry an mtime inside the run window `1787918225.50` to `1787918380.72`, and the vite content-hash asset names changed across the run, so a real rebuild happened despite `REMEDY_UI_NO_AUTO_BUILD=1` being passed through `env=`. The block's clause that a void claim costs nothing when the base-only set is empty did NOT apply, because that set held one id; the worker attributed it by direct serial reproduction at the base instead, and attributed both sets unconditionally as ordered.

THE CAUSE OF THE VOID IS A SECOND MEASURED OCCURRENCE OF `R-0714`, AND NO NEW ID IS SPENT ON IT. The worker measured the mechanism rather than inferring it — `tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default` pops `REMEDY_UI_NO_AUTO_BUILD` from a cleared environment and calls the real unpatched `_auto_build_frontend()`, and run alone with the flag correctly set it moved the same four dist mtimes again — and it correctly minted no id, because the block forbids a worker authoring ledger paragraphs. Before minting one the reviewer searched the OPEN SET for the DEFECT as the checklist's duplicate item requires, and `R-0714` already names this exact test, this exact class and this exact counter-measure; it was raised at the F032 R17 gate against a different feature and a different merge base. This round is its recurrence at merge base `9dde5495`, which is evidence that it is environment-independent and not an artefact of one branch. The reviewer confirmed the mechanism by reading the code at `f676042c`: `ui_root` is resolved from `Path(__file__).resolve().parent.parent.parent`, so `apps/ui/package.json` resolves in any checkout including a git worktree, the early return never fires, and the assertion `result is None or isinstance(result, Path)` is a tautology over a function annotated `Path | None`. The counter-measure `R-0714` already carries — patch the `exec_guard` seam and assert it WAS CALLED, as the sibling test in the same class already does — stands unperformed, and `R-0714` is carried into F037's closure as a documented Medium risk because the defect is in a ui_server test that F037 does not own.

RE-RUN BY THE REVIEWER, primary checkout, ONE pytest process at a time, each exit 0: the canary `tests/cli/test_golden_path.py` 42 passed, and `tests/ui_contracts/` 653 passed 4 skipped — both equal to the worker's readings and to the base. THE STRUCTURE IS CLEAN: six single-parent commits with insertions 346, 301, 19, 12, 447 and 329, each under 500 and each equal to the corresponding cell of the handback's `## Commits` table; the path residue is EMPTY IN BOTH DIRECTIONS over the ten evidence files plus the four state paths; `git diff --stat` restricted to `apps/`, to `packages/`, to `tests/` and to `docs/` prints NOTHING in all four cases; the transport-marker sweep is 0 in both real targets against 6 in the C0a blob as its control; `git worktree list` shows the primary checkout alone; and `gh pr list --state open` is `[]`. THE TWO BINDING FIX CLAUSES THE OPEN SET CARRIED FOR THIS BLOCK WERE BOTH PERFORMED: `R-0677`'s reading of `git ls-files` over every build-output glob `.gitignore` names came back 0 across all of them, and `R-0675`'s rule that any commit beyond the ordered sequence takes its own `## Commits` row and item-status row was carried in the handback paragraph, with the ordered sequence in fact followed exactly.
<<<END GATER25

<<<SLICE BUILTSTATE

## Built State (F037, 2026-08-28)

What exists on disk at the close of F037, so a later reader need not reconstruct
it from the roadmap's future tense. Amendment A6 above governs what is NOT here.

**The parser.** `packages/orchestration/diff_parser.py` carries
`parse_unified_diff_to_view` and the vocabulary the JSON contract is written in:
`DIFF_VIEW_VERSION`, the five statuses `DIFF_STATUS_ADDED`,
`DIFF_STATUS_MODIFIED`, `DIFF_STATUS_DELETED`, `DIFF_STATUS_RENAMED` and
`DIFF_STATUS_BINARY` collected in `DIFF_VIEW_STATUSES`, the three line kinds
`DIFF_LINE_CONTEXT`, `DIFF_LINE_ADDED` and `DIFF_LINE_DELETED`, the
`DIFF_BINARY_SENTINEL` and `DIFF_TRUNCATED_SENTINEL` markers, and the bounds
`DIFF_INTRALINE_MIN_RATIO`, `DIFF_VIEW_MAX_BODY_LINES` and `DIFF_VIEW_MAX_FILES`
that DECISIONS F037 D5, D6 and D7 rule. Its tests are
`tests/orchestration/test_diff_parser.py`.

**The source and the endpoint.** `packages/orchestration/diff_view_source.py`
carries `build_diff_view` and `list_task_run_ids` over the two scopes
`DIFF_SCOPE_JOB` and `DIFF_SCOPE_TASK_RUN`, naming every absence in its own
envelope through `DIFF_REASON_NO_EVIDENCE_DIR`, `DIFF_REASON_ARTIFACT_MISSING`
and `DIFF_REASON_UNKNOWN_TASK_RUN` rather than raising. `ui_server.py` reaches it
through the two thin callers `_build_diff_json` and `_build_task_run_diff_json`,
serving `/api/jobs/<job_id>/diff` and
`/api/jobs/<job_id>/task-runs/<task_id>/diff`. Tests:
`tests/orchestration/test_diff_view_source.py`,
`tests/ui_server/test_diff_endpoint.py` and
`tests/ui_contracts/test_diff_envelope_door.py`.

**The client.** `apps/ui/src/api/diffViewModel.ts` carries the envelope reader
`readDiffEnvelope`, the row model `buildDiffRowModels` over `DiffFileRow`,
`DiffHunkHeadRow` and `DiffLineRow`, the collapse rules
`defaultCollapsedHunkIds` and `toggleHunkCollapse` against
`DIFF_HUNK_COLLAPSE_THRESHOLD_LINES`, the sidebar summaries
`buildDiffFileSummaries`, the intraline splitter
`splitLineIntoIntralineSegments`, and the virtual-scroll window
`computeDiffRowWindow` with `diffRowWindowForViewport` and their constants
`DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS`, `DIFF_VIRTUAL_ROW_HEIGHT_PX`,
`DIFF_VIRTUAL_OVERSCAN_ROWS` and `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS`. The lazy
language model — `DIFF_SUPPORTED_LANGUAGES`, `diffLanguageForPath` and
`loadDiffLanguageBundle` with its promise cache and retry-after-rejection rule —
is complete, tested and, per amendment A6, deliberately UNWIRED. The components
are `DiffView` and `DiffFileSidebar` under
`apps/ui/src/components/diff/`, with `DiffView.module.css` carrying the binding
CSS, mounted from `RemedyShell` through the `DetailPopover` door. Tests:
`apps/ui/src/api/diffViewModel.test.ts` and the five suites
`tests/ui_contracts/test_diff_view_model.py`, `test_diff_view_render.py`,
`test_diff_file_sidebar.py`, `test_diff_surface_css.py` and
`test_diff_viewer_mount.py`.
<<<END BUILTSTATE

<<<SLICE EVIDENCESCRIPT
"""F037 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f037_closure_evidence", "remedy-job-evidence-f037-closure"
)
BASE = "9dde54956afbe5f432bfd429bf4ba0bb272f6d07"
assert len(BASE) == 40, BASE

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE.

    job_evidence._scrub_paths only relativises paths under REPO. A pytest header
    line can end in the interpreter's own absolute path, which
    build_review_manifest._unsafe_text correctly rejects as a local absolute
    path -> BLOCKED_EVIDENCE.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def mkrun(rid, path, expect):
    """One verification record. Node ids come from --collect-only, never from a
    -v log: a parametrized id can contain whitespace and a regex over -v output
    splits it. No F037 suite needs deselection — the reviewer measured all nine
    at zero deselected and zero strings rejected by the packaging scan.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    collect = subprocess.run(
        ["python3", "-m", "pytest", path, "-q", "--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest", path, "-q"],
        cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    desel = sum(int(x) for x in re.findall(r"(\d+) deselected", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped, desel) == (expect, 0, 0, 0), (
        rid, passed, failed, skipped, desel)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted(set(i.split("::")[0] for i in ids))
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": "python3 -m pytest " + path + " -q",
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": desel, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/orchestration/test_diff_parser.py", 43),
    mkrun("vr-0002", "tests/orchestration/test_diff_view_source.py", 15),
    mkrun("vr-0003", "tests/ui_contracts/test_diff_envelope_door.py", 13),
    mkrun("vr-0004", "tests/ui_contracts/test_diff_file_sidebar.py", 11),
    mkrun("vr-0005", "tests/ui_contracts/test_diff_surface_css.py", 8),
    mkrun("vr-0006", "tests/ui_contracts/test_diff_view_model.py", 8),
    mkrun("vr-0007", "tests/ui_contracts/test_diff_view_render.py", 19),
    mkrun("vr-0008", "tests/ui_contracts/test_diff_viewer_mount.py", 14),
    mkrun("vr-0009", "tests/ui_server/test_diff_endpoint.py", 6),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "files", len(r["test_files"]), "dur", r["duration_seconds"])

# Every packaged string is scanned; prove the ids and commands pass BEFORE the
# bundle is written, so a rejection is a red here and not a BLOCKED zip later.
sys.path.insert(0, os.path.join(REPO, "scripts"))
from build_review_manifest import _unsafe_text  # noqa: E402

rejected = [(r["run_id"], v) for r in runs for v in r["node_ids"] + [r["command"]]
            if _unsafe_text(v)]
print("SCAN rejected strings:", len(rejected), rejected[:3])
assert not rejected, rejected
print("SCAN red control:", bool(_unsafe_text("/home/user/repo/tests/x.py::t")))

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f037-closure",
    job_title="F037 Rendered diff viewer - closure",
    step_range="T001-T003",
    prior_job_ids=["f032-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F037 closure",
    review_feature_id="f037",
)
print(json.dumps(result, indent=2, sort_keys=True))

# The output_hash preimage rule: sha256 over stdout_summary EXACTLY.
vt = os.path.join(EVIDENCE_DIR, "verification_tests.json")
if os.path.isfile(vt):
    with open(vt, encoding="utf-8") as fh:
        doc = json.load(fh)
    for row in doc.get("runs", []):
        want = hashlib.sha256(row.get("stdout_summary", "").encode()).hexdigest()
        print("OUTPUT_HASH", row.get("run_id"), "matches sha256(stdout_summary):",
              row.get("output_hash") == want)
else:
    print("OUTPUT_HASH no verification_tests.json at", vt)
<<<END EVIDENCESCRIPT

## Constraints

1. Apply every slice byte for byte. A slice you believe is wrong is applied as
   written and the problem is declared in the handback's deviations.
2. The change set above is exhaustive. `apps/`, `packages/` and `tests/` are
   untouched by every commit of this round.
3. `.agent/plan.md` is rewritten at C1, before the record commit, because this
   round moves the finding ledger.
4. You author no `Done:`, `Gate:` or `Landed:` paragraph of your own. GATER25 is
   the reviewer's text and is the only thing entering `.agent/live_review.md`.
5. BUILTSTATE is APPENDED to the END of `docs/roadmap/features/T5_F037.md`,
   after amendment A6, with nothing above it edited, reordered or deleted. Its
   first line is blank by construction, so add no newline by hand.
6. NOTHING IS COMMITTED BETWEEN C3 AND THE ZIP BUILD. The package records C3 as
   the accepted head; a commit in between makes the manifest describe a tree that
   is no longer the one reviewed.
7. A BLOCKED_EVIDENCE package, or any zip build error, ENDS THE ROUND: record the
   raw error in full, write the handback, and hand back. Never retry with a
   reduced record, never trim a node-id list, and never delete a verification run
   to make the package go READY.
8. Never force-push, never rewrite history, never work on `main`, create no pull
   request. `git status --porcelain` is 0 at every commit boundary; the evidence
   directory and the zip are gitignored, and if either shows up as untracked,
   STOP — it was written to the wrong place.
9. This session's shell guard rejects some command FORMS — shell loops, command
   substitution, indexed expansions, inline environment assignments, and brace
   literals containing quotes. Re-express through `python3 - <<'PY'` and pass
   `env=` to `subprocess.run`. A rejected form never justifies weakening or
   skipping a gate; report every re-expression in the handback.

## The evidence job and the zip, in detail

j. Write EVIDENCESCRIPT to `.remedy-wt/f037_evidence.py` and run it from the
   repository root with `python3`. It asserts its own expected counts, so a
   changed count is a RED here rather than a surprise at packaging time. Record
   its full stdout. Every `OUTPUT_HASH` line must read True.

k. Closure precondition 3, the integrity check. The `remedy` CLI is denied in
   this session, so run
   `from packages.orchestration.integrity_gate import run_integrity_checks`. The
   result is an `IntegrityGateResult` OBJECT with attributes `.passed`,
   `.fail_count` and `.checks` — it is not a dict and `.get(...)` raises. Report
   `.passed`, `.fail_count` and each check's name and status. The reviewer
   measured `passed=True`, `fail_count=0` and all five checks PASS at
   `f676042c`; you re-measure at C3.

l. Build the package with
   `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR above>`
   from a CLEAN tree at C3. Record the script's final output verbatim. Then read
   the manifest inside the package and report `PACKAGE_STATUS`,
   `EVIDENCE_AUTHORITATIVE`, and `committed_review_subject`'s base and head — the
   head MUST equal C3 and the base MUST equal `9dde5495…`. Report the package
   FILENAME and its SHA-256, computed by you over the file on disk.
   PACKAGE_STATUS IS THE READING, NEVER THE EXIT CODE: the pipeline returns exit
   0 for both READY_FOR_REVIEW and BLOCKED_EVIDENCE, so an exit code alone proves
   nothing. State that in the handback beside the status you read.

m. Archive the package by moving it to
   `/home/decodeux/Repos/remedy-history/zips`, which the reviewer measured at
   `f676042c` as an existing writable directory holding the previous closures'
   packages. Record the ABSOLUTE directory as the `package path` value DECISION
   amend0827 D1 requires; if the move fails, record the literal `NOT ARCHIVED`
   and the reason. Then delete `.remedy-wt/f037_evidence.py` by that exact path,
   never by a glob, and leave the evidence directory itself in place.

## Done when — the gates

Run every gate and record its real exit code and real output. "Green" as a word
is a finding. G1 through G7 run at or before C3 and strictly before C4, so the
handback can quote them; C4's own insertion count belongs to the next round's
ledger entry and is not gated here.

G1 HYGIENE. `.agent/STOP` read from disk and reported ABSENT before C0a and again
before C4. `git rev-parse HEAD` before C0a equals the BASE `f676042c`.
`git branch --show-current` is `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` is 0 after each of C0a, C0b, C1, C2 and C3, and
again after the zip build.

G2 TRANSPORT. Report the sha256 of the committed `.agent/authored/f037-r26.md`
blob and the sha256 of the reviewer's own original at
`.remedy-wt/f037-r26-block.md`, and assert they are EQUAL. That file existed
before you did, so this reading covers the emission; state that, and state no
digest you have not computed. Then report that `git rev-parse` of
`HEAD:.agent/authored/f037-r26.md` and of `HEAD:.agent/last_block.md` at C0b name
ONE blob, and give that blob id.

G3 THE PLAN AT C1. PLANF037R26, re-extracted from the COMMITTED C0a blob with
`git show <C0a>:.agent/authored/f037-r26.md`, is BYTE EQUAL to `.agent/plan.md`
at C1 including its trailing newline. Report the file's `wc -l`, strictly under
50, and the counts of lines exactly `## Goal` and exactly `## Next Steps`, each 1.

G4 THE RECORD AT C2, both readers. (a) The `f676042c` blob of
`.agent/live_review.md`, plus a newline, plus GATER25, equals the C2 blob — with
a NEGATIVE CONTROL that flips one byte inside the FIRST appended paragraph and is
REJECTED. (b) Split the C2 blob on blank lines; let N be the number of paragraphs
your own script COUNTS in the slice, and compare the LAST N units of the file
against those paragraphs IN ORDER. Report N as you measured it. Also report that
the pre-round blob is a byte PREFIX of the C2 blob, with both byte lengths. Read
every non-current revision with `git show <sha>:<path>` into memory.

G5 THE LEDGER. Over the C2 blob, with base figures RE-MEASURED at `f676042c`
rather than inherited: `^- R-\d+ — `, which the reviewer measured at 292 and
which must stay UNMOVED, and whether all are DISTINCT; `^Done: R-\d+ — `, 43 and
UNMOVED; `^Landed: R-`, 11 and UNMOVED; `^Gate: F\d+ R\d+ — `, 95, which must
rise by exactly ONE; and the OPEN SET computed AS A SET, 251 and UNMOVED. Report
that `Gate: F037 R25` occurs exactly once, and that `R-0714` is still OPEN —
present as a registration with no `Done:` line — which is the documented Medium
risk F037 closes with.

G6 THE BUILT STATE AT C3, THE DOCS GATE AND THE CANARY. The `9a7e5f16`-era blob
of `docs/roadmap/features/T5_F037.md` at C2 is a byte PREFIX of the C3 blob, and
that prefix plus BUILTSTATE equals the C3 blob exactly, with a negative control
flipping one byte inside BUILTSTATE REJECTED; report both byte lengths. Report
that lines starting `## Built State` number exactly 1 and lines starting `**A6`
still exactly 1. Then, because this round's change set includes a
`docs/roadmap/**` path, run
`python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` as ONE
command, and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` —
one pytest process at a time, each with its real exit code. The reviewer measured
that combined docs command at 347 passed and the canary at 42, both at
`38966bf3`.

G7 THE EVIDENCE JOB, THE INTEGRITY CHECK AND THE PACKAGE. All of (j) through (m)
executed. Report: the script's per-run lines with every `selected` equal to its
`node_ids` length; `SCAN rejected strings: 0` with the red control reading True;
every `OUTPUT_HASH` line True; the integrity result's `.passed`, `.fail_count`
and the five check statuses; the zip script's final output; `PACKAGE_STATUS` and
`EVIDENCE_AUTHORITATIVE` read from the manifest INSIDE the package;
`committed_review_subject`'s base and head with the head equal to C3; the package
filename; its SHA-256 computed over the file on disk; and the archived absolute
directory or the literal `NOT ARCHIVED` with its reason.

G8 STRUCTURE AND THE OPEN PR GATE, measured at C3. `git diff --name-only
f676042c..<C3>` equals the change set above minus `.agent/handoff.md`, with the
RESIDUE reported EMPTY IN BOTH DIRECTIONS, each printed. `git diff --stat
f676042c..<C3>` restricted to `apps/`, to `packages/` and to `tests/` prints
nothing in all three cases. Every commit from C0a through C3 is single-parent;
report each one's insertion count from `git diff --numstat`, assert each is under
500, and report those same numbers in the handback's `## Commits` table so the
two readings agree cell by cell. `git grep -c` for `^<<<SLICE ` and for
`^<<<END ` is 0 in `.agent/plan.md`, in `.agent/live_review.md` and in
`docs/roadmap/features/T5_F037.md`, against the non-zero control of
`.agent/authored/f037-r26.md`. Because this round's change set carries an
evidence path, run `git ls-files` over each build-output glob `.gitignore` names
— `*.zip`, `*.log`, `*.egg`, `*.egg-info`, `build`, `*/build/*`, `dist`,
`*/dist/*`, `node_modules`, `*/node_modules/*`, `sdist`, `packages.zip` and
`remedy-job-evidence-*` — and require the total EMPTY, the fix clause `R-0677`
binds. `git ls-files .remedy-wt | wc -l` is 0.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` is
reported with its real output.

## Handback

Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md and the
AGENTS.md `### handoff.md` section. It has NO length cap. It carries: the Session
section with the number and roster above; the range `f676042c..HEAD`; a
per-commit `## Commits` table whose `+/-` cells are G8's `git diff --numstat`
readings; the External actions; a Verification section with ONE LINE PER GATE,
G1 through G8, each with its real figures; the Authored-text proofs; the
Deviations, including every re-expressed command form; the item-status table
covering every C and every G exactly once; the open-findings count; and a Next
section naming the STATUS round and telling the next session to apply Phase 1
rule 1 (`.agent/STOP`) before rule 2 (the Open PR Gate). THE PACKAGE FILENAME,
ITS SHA-256, ITS ARCHIVED PATH AND THE EVIDENCE JOB ID APPEAR IN FULL — R27
writes them into the STATUS line and has no other source. Then `git push -u
origin feature/f037-rendered-diff-viewer` and record its outcome; create no PR.

ANY COMMIT BEYOND THE ORDERED SEQUENCE gets its OWN `## Commits` row and its OWN
item-status row, and the Deviations section states its existence rather than
sitting beside a clause denying it. Where the sequence was followed exactly, say
that and nothing more. This is the fix clause `R-0675` binds on the next block
ordering a handback.
