── STEP F110 R17 — CLOSURE ROUND 2: THE EVIDENCE JOB AND THE REVIEW ZIP ──
Round 17 · SESSION 7 of F110 · base `e9e319e2` (F110 R16 repair C2)

Goal:
  Book round 16's PASS verdict (both the original session-5/6 block and
  the session-7 repair that resumed the stalled self-use job to a real
  terminal state) as the `Gate: F110 R16` ledger entry, add the self-use
  run's two defect strings as NEW EVIDENCE to the already-OPEN finding
  `R-0784` (never a new id — the reviewer searched the open set and found
  R-0784 already describes this exact defect class, per
  docs/agents/planner_reviewer_prompt.md §3 item 30), then build the
  closure evidence bundle (`f110-closure`, covering `T001`-`T003`) and a
  FRESH review zip over the accepted HEAD this round creates. No STATUS
  line, no README edit, no Built State section and no pull request happen
  here — those are rounds 18 and 19.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r17.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN17 to `.agent/plan.md` (whole-file replacement)
  C2   append RECORD17 to `.agent/live_review.md`
  [no commit] run the evidence job and the review zip — both write only
       under the gitignored `.remedy-wt/` and are NEVER committed
  C3   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r17.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/`, `docs/`,
  `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/candidates.md`
  or `scripts/self_use_queue.json` is touched by this round's own commits.
  This round mints NO finding id, writes no `- R-` entry and no `Done:`
  line — RECORD17 is the ONLY ledger content, and it references `R-0784`
  by number rather than editing its paragraph (append-only ledger).

Constraints:
  1. `.agent/STOP` is read FROM DISK before the first commit and again
     before C3. If it exists at either reading: finish the commit in
     hand, write the handback, push, and stop.
  2. Transport is PROMPT-EMBEDDED, not a scratch file (the reviewer here
     is 100% read-only and holds no separate scratch original). Copy the
     bytes between BEGIN BLOCK / END BLOCK (excluding those sentinel
     lines) verbatim into `.agent/authored/f110-r17.md`.
  3. Extract each of PLAN17, RECORD17 and EVIDENCESCRIPT from the
     COMMITTED `.agent/authored/f110-r17.md` by locating its
     `<<<BEGIN X>>>` / `<<<END X>>>` marker lines and taking the lines
     strictly between them (markers excluded) — never from this prompt
     directly, and never retyped.
  4. `.agent/plan.md` at C1 is REPLACED IN FULL by PLAN17 — not a
     FROM/TO pair, a whole-file write. Report `wc -l` (must be under 50)
     and sha256 of the result.
  5. `.agent/live_review.md` at C2: the reviewer measured the base at
     `e9e319e2` as exactly 2232554 bytes, 2566 lines, ending WITHOUT a
     trailing newline. The append is TWO newlines followed by RECORD17
     verbatim (RECORD17 itself is 5696 bytes, one paragraph, zero
     internal newlines), so the committed file must be EXACTLY
     2232554 + 2 + 5696 = 2238252 bytes, and the base bytes must be an
     exact PREFIX of the result. Report the arithmetic and `cmp`-style
     prefix confirmation (e.g. compare the first 2232554 bytes of the
     new file against the old file directly).
  6. Do NOT author any `- R-` entry, any `Done:` line, any
     `.agent/decisions.md` DECISION, or any `.agent/prose_slips.md` line
     this round. RECORD17 already contains everything this round owes
     the ledger.
  7. THE EVIDENCE JOB. Copy EVIDENCESCRIPT byte for byte to
     `.remedy-wt/r17_evidence.py` and run it with `python3` from the
     repository root (never through a pipe — a script run via `| tail`
     makes its own exit code unrecoverable). Report its REAL exit code
     and the full JSON summary it prints at the end: `authority_count`,
     `commit_count`, `head_commit`, `job_id`, `manual_completion`,
     `operator_attested_tasks`, `partition`, `total_passed`, `verdict`.
     `head_commit` MUST equal C2's SHA; if it does not, STOP — something
     was committed after C2. Report every `OUTPUT_HASH ... True` line (six
     of them) and the `SCAN rejected strings: 0` / `SCAN red control: a
     local absolute path` lines. Expected values, already measured by the
     reviewer in a dry run at this same base with a differently-named
     job id (`f110-closure-dryrun`), which your REAL run (job id
     `f110-closure`) must reproduce except for `job_id`, `commit_count`
     (yours will be 4 higher: C0a, C0b, C1, C2) and `head_commit` (yours
     is C2's real SHA): `authority_count=15`,
     `manual_completion=true`, `operator_attested_tasks=["T001","T002",
     "T003"]`, `partition={"T001": 5, "T002": 5, "T003": 5}`,
     `total_passed=838`, `verdict="PASS_WITH_RISKS"`. Per-run expected
     values: vr-0001 (test_config.py) 81 passed 0 skipped; vr-0002
     (test_job_role_routing.py) 14 passed 0 skipped; vr-0003
     (test_job_task_runner.py) 191 passed 0 skipped; vr-0004
     (test_model_routing.py) 406 passed 3 skipped; vr-0005
     (test_orchestrator_model_routing.py) 20 passed 0 skipped; vr-0006
     (test_role_config.py) 126 passed 0 skipped.
  8. THE INTEGRITY CHECK, closure precondition 3: run
     `from packages.orchestration.integrity_gate import run_integrity_checks`
     then `run_integrity_checks()` (the `remedy` CLI may be sandbox-denied
     this session; use the module directly). Report `passed`, `fail_count`
     and the name plus status of every check. The reviewer measured this
     at C2's base: `passed=True`, `fail_count=0`, five checks all PASS.
  9. THE REVIEW ZIP, closure algorithm step 2, run AFTER the evidence job,
     with `git status --porcelain` printing 0 lines immediately before the
     build and the branch already pushed (push after C2, before the zip
     build). Run, from the repository root, NOT through a pipe:
     `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f110_closure_evidence/remedy-job-evidence-f110-closure`
     Report its REAL exit code, the package filename, `final_sha256`
     (and that `sha256sum` on disk reproduces it), `PACKAGE_STATUS`
     (must be `READY_FOR_REVIEW` — anything else is a CLOSURE BLOCKER:
     stop, report it, change nothing to force it green),
     `EVIDENCE_AUTHORITATIVE` (must be `true`), `REVIEW_SUBJECT_ALIGNMENT`
     (must be `PASS`), `member_count`, and the archived path
     (`REVIEW_PACKAGE_DIR` / `ZIP_PATH` the script prints — the reviewer's
     own dry run found `/home/decodeux/Repos/remedy-history/zips/` writable
     and auto-populated by the script itself; report whatever the script
     actually does, do not assume). From inside the package's
     `.review_zip_manifest.json`, report `committed_review_subject.
     base_commit` (must be the full 40-char
     `6f2230cea29af36a75fea253afc10f4dfe5a79f0`), `head_commit` (must equal
     C2's SHA), `base_is_ancestor`, `commit_count`, `file_count`,
     `packaged_evidence_job_id`, `ready_gate_matrix.ok` with its
     `blocking_reasons`.
 10. THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     in the primary checkout, serially. The reviewer measured this at the
     round base: exit 0, 42 passed. Report your own real result.
 11. Do NOT run `ruff`, `npm`, or any formatter — this round's own commits
     write no `.py` file under `packages/`, `apps/`, or `tests/` (the
     evidence script runs from `.remedy-wt/` scratch, never committed).

Done when — each gate run and reported as ONE LINE in the handback with
its real exit code, at a commit STRICTLY EARLIER than C3 (except the zip
and evidence checks, which by their nature run after C2 and before C3 —
report them there, not as C3's own numbers):

G1 TRANSPORT — sha256sum of `.agent/authored/f110-r17.md` and
   `.agent/last_block.md` — must match each other. Report `wc -l
   .agent/authored/f110-r17.md`.

G2 THE PLAN — `wc -l .agent/plan.md` under 50; sha256 of the result;
   `grep -c '^## Goal$'` and `grep -c '^## Next Steps$'` each 1.

G3 THE LEDGER APPEND — the arithmetic from constraint 5, reproduced: base
   2232554, +2, +5696, total 2238252; confirm the first 2232554 bytes of
   the new file equal the old file byte for byte; report
   `grep -c '^Gate: F110 R16'` over the file (expect 0 before C2, 1 after);
   report that the string `R-0784` occurs at least once in RECORD17 (the
   evidence-attachment sentence) and that no NEW `^- R-` or `^Done: R-`
   line was added anywhere in the file (line count of both patterns must
   be identical before and after C2).

G4 THE EVIDENCE JOB — full JSON summary and all values from constraint 7,
   reported exactly as measured (not copied from this block).

G5 THE INTEGRITY CHECK — `passed`, `fail_count`, all five check statuses.

G6 THE REVIEW ZIP — every value from constraint 9.

G7 THE CANARY — real exit code and passed count.

G8 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C3 is staged — EMPTY.
   `git diff --stat e9e319e2..<C2-sha> -- packages/ apps/ tests/ docs/
   .agent/decisions.md .agent/prose_slips.md .agent/candidates.md
   scripts/self_use_queue.json` — must be EMPTY.
   `git ls-files .remedy-wt` — 0 (the evidence dir and zip script are
   gitignored scratch, never committed).
   PER-COMMIT INSERTIONS, the `+` column only, for C0a, C0b, C1 and C2,
   reported cell by cell against the handback's own `## Commits` table
   and each confirmed under 500 (C0b and C2 may be whole-file rewrites;
   report the real `git diff --numstat` cells regardless).

Handback: rewrite `.agent/handoff.md` in full per
docs/agents/handback_template.md — feature and round, SESSION 7 of
   F110, branch, base and head SHAs, the per-commit changed-files table
   with its `+/-` column, ONE line per gate above with its real exit code,
   the item-status table AGENTS.md mandates, the deviations, the
   open-findings count (278, UNCHANGED — no new id was minted this
   round), a `## Closure values` table with these rows: `Evidence job`
   (job id), `package` (filename), `SHA-256` (hash), `package path`
   (absolute archived dir, or `NOT ARCHIVED`), `accepted HEAD` (C2's full
   SHA). Its `## Next` section names round 18 (Built State section for
   `docs/roadmap/features/T3_F110.md`) as the next expected action. It
   has NO length cap. Then `git push -u origin
   feature/f110-model-routing-by-task-class` (after C2, before the zip
   build) and again after C3; create NO pull request, merge nothing.

<<<BEGIN PLAN17>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 17 — CLOSURE ROUND 2: THE EVIDENCE JOB AND THE REVIEW ZIP. Round 16
is CLOSED: the self-use precondition ran to a real terminal state
(`SU-006`, job `6f74dd7367704fd5`, `status='blocked'` at the normal
approval gate after a cross-session resume), its two defect strings are
recorded as new evidence on the already-OPEN `R-0784` rather than as a
fresh id, and DECISION F110 D6 already ruled the checklist-consolidation
obligation discharged. This round builds the closure evidence bundle
(`f110-closure`, covering `T001`-`T003`) and a FRESH review zip over the
accepted HEAD this round creates. No STATUS line, no README edit, no
Built State section and no pull request happen here.

## Next Steps

- Round 18: give `docs/roadmap/features/T3_F110.md` its Built State
  section and its Design/Task-slicing bullet updates — split out of what
  round 16's own plan called "round 17" because bundling it with the
  evidence job and zip would put this round over the 490-line block cap.
- Round 19: the closure commit — the authored STATUS `[x]` line and the
  README capability sync in the SAME commit, `SU-006`'s `consumed_by`
  set to `F110`, and the pull request.

## Risks

- The zip is a closure BLOCKER, not a formality: a `PACKAGE_STATUS` other
  than `READY_FOR_REVIEW` stops closure rather than being worked around.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
- `R-0784` stays OPEN; its fix belongs to F258's generator, not to F110.
<<<END PLAN17>>>

<<<BEGIN RECORD17>>>
Gate: F110 R16 — the round 16 entry. VERDICT PASS, over two block-authoring passes and three sessions (5, 6, 7), range `1d1a82e1..e9e319e2`. THE ROUND CLOSED CLOSURE PRECONDITION 6's SELF-USE ITEM, RUN FOR REAL AGAINST A GENUINE PROVIDER, AFTER A CROSS-SESSION CRASH RECOVERY THE REVIEWER VERIFIED INDEPENDENTLY AT EVERY STEP. SESSION 5 (original block, transport re-verified by the reviewer): `.agent/authored/f110-r16.md` is 24917 bytes over 288 lines, sha256 `3ae664fbe94eb5ecb8c9d3821a4e6bafb5ed3b095cd793fea0108193d01ffe6e`, reproduced by the reviewer directly against the committed blob. Its worker ran C0a through C2 cleanly (booking round 15's PASS verdict, DECISION F110 D6 and one prose slip), then began constraint 6's self-use step: `generate_and_append_if_empty()` appended `SU-006` to `scripts/self_use_queue.json` (the queue held 5 items, now 6, `consumed_by` empty), and the runner's planning phase wrote `.remedy-wt/selfuse-f110-run/SU-006.md` and created job `6f74dd7367704fd5` at base `cf0e00e9` — then the session ended with NO handback, mid-run, task T001 left at `status='running'`. SESSION 6 found the dirty tree at its own Phase 0 probe, investigated read-only per G8 rather than guessing, committed only the one confirmed harmless side effect already on disk (the `SU-006` queue append, `+8/-0`) and handed back declaring constraint 6's remaining steps INCOMPLETE — no job code was invoked, no `.remedy-wt/` path was touched. SESSION 7 (this reviewer's own round) RE-INVESTIGATED FROM DISK rather than trusting either prior session's prose: `load_job_plan('6f74dd7367704fd5')` printed `status='running'`, `worktree_cleanup_status='active'`, task T001 `status='running'`, `first_running_at` set — the process that ran it was provably dead (a fresh session), so the job was genuinely stalled, not merely slow. `resume_job_plan('6f74dd7367704fd5')` — THE PRODUCT'S OWN RECOVERY API, never `run_next_self_use_item`, which would have replanned and orphaned the stalled job — resumed the SAME worktree, SAME branch, SAME base commit in 52.4s and reached a terminal state: `status='blocked'`, task T001 `final_status='review_inconsistent'`, `reviewer_verdict='fail'` after 1 of 2 repair rounds. THE REVIEWER REPRODUCED THIS INDEPENDENTLY, not read from the handback: `load_job_plan('6f74dd7367704fd5')` at this gate again prints `status='blocked'`, `worktree_cleanup_status='retained'`, matching exactly. TRANSPORT FOR THE REPAIR BLOCK, digest-fallback per docs/agents/self_drive_protocol.md (the reviewer is 100% read-only and holds no scratch original): `.agent/authored/f110-r16-repair.md` and `.agent/last_block.md` are byte-identical, sha256 `14152c2f5f38eb19796f9f553ebba11620e307c976ad788b91b102d3779ef612` over 164 lines, reproduced by the reviewer directly against the committed blob, which the reviewer also compared line for line against the prompt bytes it emitted — identical. THE EVIDENCE COPY IS BYTE-IDENTICAL, reproduced independently: `sha256sum` of `.agent/selfuse_f110/SU-006.md` on disk is `6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd`, matching both the source and copied digests `run.txt` records. THE TREE AND THE SWEEP, reproduced independently: `git diff --stat 1d1a82e1..e9e319e2 -- packages/ apps/ tests/ docs/` is EMPTY across the round's full two-session-plus-repair span — the round changed no production code anywhere; `git worktree list` shows job `6f74dd7367704fd5`'s worktree RETAINED and no new one; `.remedy-wt/selfuse-f110-run` is gone; `scripts/self_use_queue.json`'s `SU-006` entry still carries an empty `consumed_by`, unchanged since session 5 — setting it is round 19's closure commit, not this round's. The branch is pushed at `e9e319e2` with no pull request open. CLOSURE PRECONDITION 6's REGISTRATION OBLIGATION: `describe_self_use_run_defects(plan)` returned two strings, quoted verbatim in `.agent/selfuse_f110/run.txt` — `job 6f74dd7367704fd5 (blocked): task_T001_gate_failed: final_status=review_inconsistent; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=review_inconsistent; reviewer_verdict=fail`. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE ANY ID WAS CONSIDERED, per §3 item 30: `R-0784`, OPEN since F109 R19, already describes exactly this class — a self-use run against `R-0418` (a reviewer-block-authoring-practice finding no builder can fix in code) blocking at the normal approval gate, registered against job `5e91e080219342d9`'s two analogous strings. This occurrence is the SAME defect recurring on a SECOND job, on a DIFFERENT branch, with a DIFFERENT proximate trigger — `review_inconsistent` after 1 of 2 repair rounds, where `R-0784`'s instance was `repair_exhausted` after both — which is new evidence that the underlying curation gap R-0784's own FIX clause names (F258's generator needs a tier-1 filter for reviewer-practice findings, or an explicit acceptance that some generated items will honestly block) is not a one-off: it has now recurred exactly as R-0784 predicted, on the very next feature to consume a self-use item. Per item 30 this evidence is ADDED TO `R-0784` here rather than minted as a second id; `R-0784` remains OPEN and its fix is unchanged, still owed to F258 and not to F109 or F110. THE OUTCOME IS A NORMAL APPROVAL-GATE RESULT, NOT A ROUND FAILURE, exactly as both the original and repair blocks' own constraints ruled: the self-use rail executed end to end against a real local provider (`ollama`, both roles) and correctly refused to promote unfinished work. NO PRODUCTION CODE WAS TOUCHED, NO FINDING BEYOND THE R-0784 ADDITION IS OWED, and `.agent/candidates.md` is unchanged and still EMPTY.
<<<END RECORD17>>>

<<<BEGIN EVIDENCESCRIPT>>>
"""F110 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f110_closure_evidence", "remedy-job-evidence-f110-closure"
)
BASE = "6f2230cea29af36a75fea253afc10f4dfe5a79f0"
assert len(BASE) == 40, BASE

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE."""
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def mkrun(rid, path, expect, kexpr=None, expect_deselected=0, expect_skipped=0):
    """One verification record. Node ids come from --collect-only, never from a
    -v log (finding R-0611). `expect_skipped` widens the F009 R33 template's
    original `skipped == 0` assumption: F110's test_model_routing.py legitimately
    carries 3 skips (parametrizations already covered by a sibling fixture), so
    the coherence check is (passed, failed, skipped) == (expect, 0, expect_skipped)
    rather than a hard-coded zero.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    sel = [path, "-q"] + (["-k", kexpr] if kexpr else [])
    cmd = "python3 -m pytest " + path + " -q" + (' -k "' + kexpr + '"' if kexpr else "")
    collect = subprocess.run(
        ["python3", "-m", "pytest"] + sel + ["--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest"] + sel, cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    desel = sum(int(x) for x in re.findall(r"(\d+) deselected", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped) == (expect, 0, expect_skipped), (rid, passed, failed, skipped)
    assert desel == expect_deselected, (rid, desel, expect_deselected)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": cmd,
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": desel, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/orchestration/test_config.py", 81),
    mkrun("vr-0002", "tests/orchestration/test_job_role_routing.py", 14),
    mkrun("vr-0003", "tests/orchestration/test_job_task_runner.py", 191),
    mkrun("vr-0004", "tests/orchestration/test_model_routing.py", 406, expect_skipped=3),
    mkrun("vr-0005", "tests/orchestration/test_orchestrator_model_routing.py", 20),
    mkrun("vr-0006", "tests/orchestration/test_role_config.py", 126),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "deselected", r["deselected"], "skipped", r["skipped"],
          "files", len(r["test_files"]), "dur", r["duration_seconds"])

import sys  # noqa: E402
sys.path.insert(0, os.path.join(REPO, "scripts"))
from build_review_manifest import _unsafe_text  # noqa: E402

rejected = [(r["run_id"], v) for r in runs for v in r["node_ids"] + [r["command"]]
            if _unsafe_text(v)]
print("SCAN rejected strings:", len(rejected), rejected[:3])
assert not rejected, rejected
print("SCAN red control:", _unsafe_text("/home/user/repo/tests/x.py::t"))

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f110-closure",
    job_title="F110 Model routing by task class - closure",
    step_range="T001-T003",
    prior_job_ids=["f109-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F110 closure",
    review_feature_id="f110",
)
print(json.dumps(result, indent=2, sort_keys=True))

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
<<<END EVIDENCESCRIPT>>>
