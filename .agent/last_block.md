### STEP T005 — F256 Diff viewer completion, round 9 (THE INTEGRATION GATE AND THE PACKAGE)

Goal: satisfy closure preconditions 2, 3 and 5 of
`docs/roadmap/STATUS_closure_protocol.md` — the dedicated integration-gate round
over the full suite, the integrity check, the evidence bundle and the review
package — and record the package name, its SHA-256 and its archived path so the
NEXT round can write the STATUS line. THIS ROUND DOES NOT CLOSE THE FEATURE: it
does not touch `docs/roadmap/STATUS.md` or `README.md`, and it creates no pull
request. Precondition 4, the feature file's Built State, was met at `f6d5d064`.

Base: `f69bff0d`, the tip of `feature/f256-diff-viewer-completion`. Every reading
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r9.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R8 verdict to `.agent/live_review.md`
- then the integration gate, the evidence job, the integrity check, the package
  and the archive — NONE of which is a commit
- C3 rewrite `.agent/handoff.md`

Change set, these paths and nothing else:

- `.agent/authored/f256-r9.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/handoff.md`

C2 IS THE ACCEPTED HEAD. The package records the tree at C2 as the head it
covers, so NOTHING IS COMMITTED BETWEEN C2 AND THE ZIP BUILD. C3 is the handback
and follows the READY package, exactly as F037's closure sequence did.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   with its real output. Do NOT create or merge a pull request. Stay on
   `feature/f256-diff-viewer-completion`; do not branch, never work on `main`.
1. Apply every authored slice BYTE FOR BYTE. A slice you believe is wrong is
   applied as written and the problem is declared in the handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r9.md`, never from this prompt's text.
   That includes EVIDENCESCRIPT, which you write to
   `.remedy-wt/f256_evidence.py` and run — never retype it.
4. AGENTS.md binds in full: self-review before every commit, one logical step per
   commit, `.agent/plan.md` current before every commit, clean tree, push.
5. NO FILE UNDER `apps/`, `packages/`, `tests/` OR `docs/` CHANGES BY A BYTE, and
   neither does `docs/roadmap/STATUS.md` or `README.md`. This round writes only
   the five `.agent/` paths above.
6. Shell forms rejected by this session's guard are RE-EXPRESSED as a script file
   under `.remedy-wt/` run with `python3`, never skipped and never weakened. A
   rejected form NEVER justifies weakening or skipping a gate. Report each one.
7. A BLOCKED_EVIDENCE PACKAGE, OR ANY ZIP BUILD ERROR, ENDS THE ROUND: record the
   raw error in full, write the handback, hand back. Never retry with a reduced
   record, never trim a node-id list, never delete a verification run to make the
   package go READY. PACKAGE_STATUS IS THE READING, NEVER THE EXIT CODE — the
   pipeline returns exit 0 for both READY_FOR_REVIEW and BLOCKED_EVIDENCE, so an
   exit code alone proves nothing. Say so in the handback beside the status.
8. The evidence directory and the zip are GITIGNORED. If either appears as
   untracked in `git status --porcelain`, STOP — it was written to the wrong
   place. `git status --porcelain` is 0 at every commit boundary.
9. If the integration gate at G6 is RED, the round ends there: record the FULL
   untruncated failure list and hand back. A closure cannot be built on a red
   suite, and no test is deleted, deselected or weakened to make it green.

### The pipeline, in detail

j. Write the EVIDENCESCRIPT slice to `.remedy-wt/f256_evidence.py` and run it
   from the repository root with `python3`. It asserts its own expected counts,
   so a changed count is a RED here rather than a surprise at packaging time.
   Record its full stdout. Every `OUTPUT_HASH` line must read True and
   `SCAN rejected strings` must be 0 with the red control reading True.

k. Closure precondition 3, the integrity check. The `remedy` CLI is denied in
   this session, so run
   `from packages.orchestration.integrity_gate import run_integrity_checks`. The
   result is an `IntegrityGateResult` OBJECT with attributes `.passed`,
   `.fail_count` and `.checks` — it is not a dict and `.get(...)` raises. Report
   `.passed`, `.fail_count` and each check's name and status. The reviewer
   measured `passed=True`, `fail_count=0` and all five checks PASS at `f69bff0d`
   — `handler_import`, `live_review_verdict`, `plan_consistency`,
   `relevant_untracked` and `high_blockers_open`; you re-measure at C2.

l. Build the package with
   `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR the script
   used>` from a CLEAN tree at C2. Record the script's final output verbatim.
   Then read the manifest INSIDE the package and report `PACKAGE_STATUS`,
   `EVIDENCE_AUTHORITATIVE`, and `committed_review_subject`'s base and head — the
   head MUST equal C2 and the base MUST equal
   `0e8ab5b4f780b5265a6aa604ee89067399046b1e`. Report the package FILENAME and
   its SHA-256, computed by you over the file on disk.

m. Archive the package by MOVING it to `/home/decodeux/Repos/remedy-history/zips`,
   which the reviewer measured at `f69bff0d` as an existing writable directory
   already holding the previous closures' packages. Record the ABSOLUTE directory
   as the `package path` value DECISION amend0827 D1 requires; if the move fails,
   record the literal `NOT ARCHIVED` and the reason. Then delete
   `.remedy-wt/f256_evidence.py` by that exact path, never by a glob, and leave
   the evidence directory itself in place.

### The authored slices

<<<SLICE PLANF256R9
# Plan — F256 Diff viewer completion

Branch: feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`.
F256 was claimed by Rule A5 as the first unchecked line of Package 1 in
`docs/roadmap/STATUS.md`.

## Goal
Finish the rendered diff viewer F037 shipped: highlighting actually rendered
rather than only modelled, the 10k-line budget measured and recorded, and the
file sidebar's visual treatment ruled by a named authority.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 wire the highlighting | done | DECISIONS F256 D1 and D2 |
| T003 rule on the sidebar's treatment | done | DECISION F256 D3 |
| T002 measure and record, both halves | done | `f6d5d064`, D4 D5 D6 |
| the integration gate | done | this round, full suite |
| the evidence bundle and the package | done | this round |
| the STATUS closure commit | open | next round, with the README sync |

## Next Steps
1. Author the STATUS line from the package name, SHA-256 and archived path this
   round recorded, and apply it with the README capability sync in ONE commit.
2. Open the closure PR per the AGENTS.md workflow; it is NOT merged this
   session — the gap is the operator's manual-review window.
3. Leave `.agent/candidates.md` empty unless the closure gate raises one.

## Risks
- The STATUS `[x]` flip and the README sync must land in the SAME commit or the
  ledger cross-check pin goes red.
- The closure commit is the last on the branch (Rule A4), with the single
  permitted successor DECISION amend0827 D2 names.
<<<END PLANF256R9

<<<SLICE GATEF256R8
Gate: F256 R8 — the RECORDED MEASUREMENT round, which wrote F256's three pieces and both halves of the 10k measurement into the feature file's Built State. THE ROUND PASSED on every gate its block ordered, G1 through G7, and the reviewer re-ran each one independently at `f69bff0d`.

TRANSPORT COVERS THE EMISSION: the reviewer's own scratch original `.remedy-wt/f256-r8-block.md` predates the worker, and the committed `.agent/authored/f256-r8.md` blob at `8569ef20` is BYTE EQUAL to it at 22031 bytes, sha256 `619bf5d68f82d88878248b3ed66e19825f24ade29ae829e1bbbcd6acf352d9dd`. `.agent/plan.md` at `21cc5157` is byte-equal to its slice at 33 lines. At `cb2f3ce1` both appends reconstruct byte for byte from the `b8a918a1` blob plus a newline plus their slice, each pre-round blob is a byte PREFIX, and each negative control is REJECTED; `.agent/prose_slips.md` went from 6 dated lines to 7, gained exactly one, and its first six are unchanged. The ledger moved as a round that registers and resolves nothing should: registrations 293 all DISTINCT, `^Done:` 43, `^Landed:` 11, the OPEN SET as a set 252, and `^Gate: F\d+ R\d+ — ` alone rising by one to 104, with `Gate: F256 R7` occurring exactly once.

THE BUILT STATE IS AN APPEND AND ITS NUMBERS ARE TRUE, which is the gate this round existed for. At `f6d5d064` the feature file is the `b8a918a1` blob plus a newline plus the slice, byte for byte, the pre-round blob is a byte PREFIX so no existing line moved, and `## Built State` occurs exactly once. The reviewer then re-ran the whole cross-check independently: every one of the seventeen recorded literals — `0.1331`, `0.1282`, `0.1489`, `1,045,960` and `4.97` against `tests/ui_server/test_diff_endpoint.py`; `0.678`, `0.271`, `1.408`, `10,002` and `100,020` against `apps/ui/src/api/diffViewModel.test.ts`; `0.105`, `0.010` and `0.021` against `tests/orchestration/test_diff_parser.py`; and the four sidebar class names against `DiffView.module.css` — is present on BOTH sides. A recorded number that is not in the file that produced it would have been a false record, and there is none.

RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/docs/` 295 passed, `tests/ui_contracts/` 664 passed with 4 skipped, `tests/ui_server/` 497 passed, `tests/orchestration/test_diff_parser.py` 43 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. The change set is six paths with both residues empty, every commit single-parent and under 500 insertions, and NO file under `apps/`, `packages/`, `tests/`, `docs/roadmap/STATUS.md` or `docs/roadmap/ROADMAP.md` changed by a byte.

THE REVIEWER ALSO RAN THE FULL SUITE AT `f69bff0d`, ahead of the integration-gate round, so that round begins from a measured position rather than a hope: `python3 -B -m pytest -n auto -q` returned exit 0 with 18150 passed and 20 skipped in 104.3 seconds, with `apps/ui/dist` verified NOT stale beforehand. The integrity gate, run through `packages.orchestration.integrity_gate.run_integrity_checks` because the `remedy` CLI is denied in this session, returned `passed=True` and `fail_count=0` with all five checks PASS.

THE ONE DECLARED DEVIATION IS ACCEPTED AND IS A READING, NOT A DEFECT. The worker reported that `packages/orchestration/diff_parser.py` literally carries `DIFF_VIEW_MAX_BODY_LINES = 20_000` where the Built State's prose says "20,000" — the same value in a different digit grouping — and it adjusted neither side, which is exactly what constraint 8 of that block asked for. The reviewer confirms the file's bytes and the slice's prose both say twenty thousand.
<<<END GATEF256R8

<<<SLICE EVIDENCESCRIPT
"""F256 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f256_closure_evidence", "remedy-job-evidence-f256-closure"
)
os.makedirs(EVIDENCE_DIR, exist_ok=True)
BASE = "0e8ab5b4f780b5265a6aa604ee89067399046b1e"
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
    splits it. The reviewer measured all nine suites at `f69bff0d` with zero
    deselected, zero skipped and node-id counts equal to their passed counts.
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
    mkrun("vr-0004", "tests/ui_contracts/test_diff_file_sidebar.py", 16),
    mkrun("vr-0005", "tests/ui_contracts/test_diff_surface_css.py", 8),
    mkrun("vr-0006", "tests/ui_contracts/test_diff_view_model.py", 8),
    mkrun("vr-0007", "tests/ui_contracts/test_diff_view_render.py", 25),
    mkrun("vr-0008", "tests/ui_contracts/test_diff_viewer_mount.py", 14),
    mkrun("vr-0009", "tests/ui_server/test_diff_endpoint.py", 8),
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
    job_id="f256-closure",
    job_title="F256 Diff viewer completion - closure",
    step_range="T001-T003",
    prior_job_ids=["f037-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F256 closure",
    review_feature_id="f256",
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

`PLANF256R9` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R8` is an
APPEND to `.agent/live_review.md`: the pre-round blob, one newline, then the
slice. `EVIDENCESCRIPT` is not applied to any tracked file — it is written to
`.remedy-wt/f256_evidence.py`, run, and deleted at step m.

### Done when

G1 HYGIENE AND STRUCTURE. Read `.agent/STOP` with `os.path.exists` before C0a and
again before C3; report both, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `f69bff0d` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1 and C2 and again after the package is archived. Over
`f69bff0d..<C2>` report `git diff --name-only` and both residues against the
change set with `.agent/handoff.md` set aside, printed in both directions and
both expected empty. Report `git diff --stat f69bff0d..<C2>` restricted to
`apps/`, to `packages/`, to `tests/` and to `docs/` — all four expected to print
NOTHING. Report each commit's insertions from `git diff --numstat`, each under
500, and that C0a, C0b, C1 and C2 are single-parent. Report the counts of lines
beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md` and
`.agent/live_review.md` — each expected 0 — beside `.agent/authored/f256-r9.md`
as the non-zero control. Because this round writes an evidence directory, run
`git ls-files` over each build-output glob `.gitignore` names — `*.zip`, `*.log`,
`dist`, `build`, `node_modules`, `sdist`, `packages.zip` and
`remedy-job-evidence-*` — and require the total EMPTY. Report
`git ls-files .remedy-wt | wc -l`, expected 0.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r9.md` against the reviewer's own original at
`.remedy-wt/f256-r9-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more than
self-consistency. Report that `<C0b>:.agent/authored/f256-r9.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R9 including the
trailing newline — report `True` or `False` — with `wc -l` under 50 and the
counts of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers. (a) The `f69bff0d` blob of
`.agent/live_review.md` plus a newline plus GATEF256R8 equals the C2 blob —
report `True` or `False` — the pre-round blob is a byte PREFIX, and a NEGATIVE
CONTROL flipping one byte at an offset your script confirms lies INSIDE THE FIRST
appended paragraph reports the equality now `False`. (b) Let N be the slice's
paragraph count, COUNTED BY YOUR SCRIPT and never taken from this block, ignoring
an empty trailing unit; report N and that the LAST N blank-line units of the file
match those paragraphs IN ORDER.

G5 THE LEDGER AT C2. Over the C2 blob and the `f69bff0d` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round registers and
resolves nothing, so every figure is UNMOVED except `^Gate: F\d+ R\d+ — `, which
rises by exactly ONE. Report that `Gate: F256 R8` occurs exactly 1 time. Report
that `.agent/candidates.md` still contains no candidate entry.

G6 THE INTEGRATION GATE, closure precondition 2, run at C2 from the repository
root in the PRIMARY checkout. Before it, report whether `apps/ui/dist` is stale
against `apps/ui/src` by comparing the newest mtime under each, and if it is,
warm it with `npx vite build` in `apps/ui` spawned from Python with `cwd` set,
reporting that command's REAL exit code — a cold `dist` times out one
`tests/ui_server` test under `-n auto`. Then run

    ["python3", "-B", "-m", "pytest", "-n", "auto", "-q"]

and report its REAL exit code, the final summary line verbatim, and the wall
clock. The reviewer measured exit 0 with 18150 passed and 20 skipped in 104.3
seconds at `f69bff0d`; you re-measure at C2, and a difference in the counts is
reported rather than explained away. Save the FULL raw output to a file under
`.remedy-wt/` and name that file in the handback. If the gate is RED, constraint
9 binds.

G7 THE EVIDENCE JOB AND THE INTEGRITY CHECK, steps (j) and (k). Report the
script's per-run lines with every `selected` equal to its `node_ids` length and
every `files` count 1; `SCAN rejected strings: 0` with the red control reading
True; every `OUTPUT_HASH` line True; and the integrity result's `.passed`,
`.fail_count` and all five check names with their statuses.

G8 THE PACKAGE, steps (l) and (m). Report the zip script's final output verbatim;
`PACKAGE_STATUS` and `EVIDENCE_AUTHORITATIVE` read from the manifest INSIDE the
package; `committed_review_subject`'s base and head, with the head equal to C2 and
the base equal to `0e8ab5b4f780b5265a6aa604ee89067399046b1e`; the package
FILENAME; its SHA-256 computed by you over the file on disk; and the ABSOLUTE
archived directory or the literal `NOT ARCHIVED` with its reason. State explicitly
that PACKAGE_STATUS was READ from the manifest and not inferred from an exit code.
Report `gh pr list --state open` again after the archive, still expected `[]`.

### Handback

Rewrite `.agent/handoff.md` in C3 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F256 · round 9`; the range `f69bff0d..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared cell
by cell against G1's figures; ONE LINE PER GATE G1 through G8 with its real
result; the deviations, including every guard re-expression constraint 6 required;
the item-status table with every C-item and every gate appearing exactly once.

IT ALSO CARRIES, AS ITS OWN SECTION, THE FOUR VALUES THE NEXT ROUND NEEDS TO
WRITE THE STATUS LINE, because `.agent/handoff.md` is the durable carrier and the
evidence directory is not committed: the evidence job id `f256-closure`, the
package FILENAME, the package SHA-256, the ABSOLUTE archived directory (or
`NOT ARCHIVED`), and the ACCEPTED HEAD — the full 40-character SHA of C2. Label
that section clearly; a later session that cannot find these values cannot close
the feature.

State that the next expected action is the closure commit: the STATUS `[x]` line
and the README capability sync in ONE commit, followed by the PR, which is NOT
merged this session.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R8 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C3: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
