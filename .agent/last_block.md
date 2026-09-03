== STEP closure-evidence / F109 — ROUND 20 ==

SESSION 4 of feature F109. Round 20. Rounds so far: 19 done, this is the 20th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 20 rounds and 4 sessions it is NOT reached. No line of this
block is a run of a repeated character, so there is no run length to recover
(§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Closure-protocol algorithm steps 1 and 2: the EVIDENCE JOB and a FRESH REVIEW
ZIP, plus the integrity check precondition 3 demands. Register the three findings
the round 19 self-use run exposed. This round does NOT write the STATUS line and
does NOT create the PR — that is round 21, and the protocol requires the closure
commit to FOLLOW a READY package.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r20.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN20 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD20 to `.agent/live_review.md`  (verdict, three registrations)
- C3   rewrite `.agent/handoff.md`

The evidence bundle and the zip are built BETWEEN C2 and C3, from the clean tree
at C2. Neither is committed: `.gitignore` excludes `remedy-job-evidence-*/` and
the zip, and the closure protocol's "Evidence dir is not committed" rule is
explicit that a committed evidence dir puts evidence files into the review
subject and packages BLOCKED_EVIDENCE. So C2's SHA is the ACCEPTED HEAD the
manifest records, and you report it.

## Change set — these paths and nothing else

    .agent/authored/f109-r20.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/handoff.md

## Constraints

1. EVERY authored slice is applied BYTE FOR BYTE. EVIDENCESCRIPT is COPIED to
   `.remedy-wt/f109_evidence.py` and run — it is never retyped and never edited.
   If it fails, report the real traceback; do not "fix" it silently.
2. `.agent/live_review.md` ends WITHOUT a trailing newline: append exactly the two
   bytes `\n\n` then RECORD20, which itself ends without one.
3. THE ZIP IS BUILT FROM A CLEAN TREE. Run `git status --porcelain` immediately
   before the build and record that it was empty. A package built from a dirty
   tree is invalid.
4. A FAILING ZIP BUILD IS A CLOSURE BLOCKER. If it fails, record the raw error in
   the handback, do NOT close, and stop the round there. `PACKAGE_STATUS` is the
   reading — NOT the exit code, which is 0 for both READY_FOR_REVIEW and
   BLOCKED_EVIDENCE.
5. Register the three findings EXACTLY as RECORD20 words them. Do not add a
   `Done:` or `Landed:` line for any of them: all three are documented Low risks
   carried into closure, and none is F109's code to repair — `R-0785` and
   `R-0786` belong to F258's generator, and repairing another feature's code from
   this branch is the scope drift AGENTS.md forbids.
6. Nothing outside the change set is edited. If the sweep finds something else,
   DECLARE it; do not repair it.
7. `python3 -m pytest` is the pytest route. Env-var assignment (`VAR=x cmd`,
   `env`, `export`) and `cp` are DENIED: copy with
   `python3 -c "import shutil; shutil.copyfile(a, b)"`. A `bash -c` wrapper around
   a Python heredoc, and a heredoc with braces adjacent to quotes, have both been
   observed DENIED — write such logic to a scratch `.py` under `.remedy-wt/` and
   run it with `python3 -B`.
8. Never force-push, never work on main, never create or merge a PR this round.

## SLICE FORTSCHRITT — one line, applied verbatim into the handback's state block

BEGIN FORTSCHRITT
| **Fortschritt** | ~99 % (T001-T003 ✅ · Integration Gate ✅ · Self-Use ✅ · Evidence+Zip in Arbeit) — Schätzung |
END FORTSCHRITT

## SLICE PLAN20 — the whole of `.agent/plan.md`

BEGIN PLAN20
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 20, session 4. CLOSURE, steps 1 and 2: the evidence job and a FRESH
review zip, plus the integrity check. Register the three findings the
round 19 self-use run exposed, all three as documented Low risks carried
into closure — two of them are F258's generator, not F109's code. The
STATUS line and the PR are round 21, because the closure commit must
FOLLOW a READY package.

## Next Steps

- Round 21, the closure commit: the authored STATUS line with the README
  capability sync in the SAME commit, `consumed_by` set to F109 on
  `SU-005`, the final `.agent/` state, then the PR. That round also runs
  the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- A failing zip build is a CLOSURE BLOCKER, never something to work
  around; `PACKAGE_STATUS` is the reading, not the exit code.
- SEVEN findings on this branch were one class: prose TRUE when written
  and falsified by a later round. The consolidation should answer the
  class, not add an eighth id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
END PLAN20

## SLICE RECORD20 — appended to `.agent/live_review.md`, four paragraphs

BEGIN RECORD20
Gate: F109 R19 — the round 19 entry. VERDICT PASS, over the range `cb19e916..a06a6e69`. CLOSURE PRECONDITION 6 IS DISCHARGED AND THE RUN WAS REAL. `SU-005` — "Address ledger finding R-0418", provenance `generated (self-use-generator tier 1, ledger scan, R-0418)`, which is exactly what the reviewer's own read-only probe predicted at `cb19e916` — was generated by the shipped generator, planned, and RUN for 184.3 seconds under provider `ollama` and model `muse-glimmer:latest` for both roles, with the default budgets and NO `builder_name`/`reviewer_name` override. Its `execution_config` records `builder='ollama'`, `reviewer='ollama'`, source `cli`, so the run was NOT faked, which constraint 5 of that round made the condition of the precondition being discharged at all. The job then stopped at the NORMAL APPROVAL GATE: `JobPlan.status='blocked'`, task T001 `final_status='repair_exhausted'`, `reviewer_verdict='fail'`, both repair rounds spent, nothing promoted. THE REVIEWER RE-VERIFIED THE ROUND independently: `cmp` of the reviewer's own `.remedy-wt/f109-r19.md` against the committed authored copy exited 0; the queue holds 5 items where it held 4, the four prior ones parse identically, the new one carries an EMPTY `consumed_by` as constraint 3 required; the ledger reads 344 distinct registered ids and 68 distinct resolved over 70 `Done:` lines, so the open set is 276; and the five gate suites re-run to 23, 20, 11, 18 and 42, totalling 114 at exit 0. THE ROUND FOUND THREE THINGS BEYOND ITS ORDERED TUPLE and repaired none of them, which is correct: two are registered below as `R-0785` and `R-0786`, and the third — the retained job worktree `.remedy-wt/job-5e91e080219342d9`, `worktree_cleanup_status='retained'` — is PRE-EXISTING product behaviour with four such worktrees already present, is gitignored, and is recorded here without an id rather than charged to this feature. ONE SENTENCE OF THE REVIEWER'S OWN PLAN WENT STALE INSIDE THIS ROUND and the worker declared it: `.agent/plan.md` at `5c051818` says "the queue holds no pending item", which was true when C1 was written and false after C3 appended one. It reads as the round's GOAL rather than as a claim about the end state, nothing on disk is wrong, and `.agent/plan.md` is rewritten every round by construction — so it is a `.agent/prose_slips.md` line at the consolidation, not an id.

- R-0784 — Low, THE SELF-USE RUN THIS CLOSURE CONSUMED ENDED BLOCKED AT THE APPROVAL GATE, AND BOTH STRINGS `describe_self_use_run_defects` RETURNED ARE REGISTERED HERE BECAUSE CLOSURE PRECONDITION 6 REQUIRES IT. The two strings, verbatim and in order, are `job 5e91e080219342d9 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. THEY ARE ONE DEFECT SEEN TWICE — the job-level view and the task-level view of the same gate failure — so they take ONE id and not two, per §3 checklist item 30, which forbids minting a second id for a defect the set already holds. WHAT ACTUALLY HAPPENED, stated plainly rather than dressed up: `SU-005`'s task was to repair `R-0418`, a finding about REVIEWER BLOCK-AUTHORING PRACTICE under self-drive, whose fix is a rule about what a block must contain and not a code change any builder can make. The configured local model spent both repair rounds and the reviewer role failed it, so the job blocked and promoted nothing. THAT IS THE SYSTEM WORKING: an approval gate that refuses an unfinished job is the gate doing its job, and the alternative — promoting it — is the outcome the gate exists to prevent. WHY THIS IS LOW AND NOT A PRODUCT DEFECT: no Remedy code behaved wrongly, no state on disk is wrong, and the run is evidence that the self-use rail executes end to end against a real provider. What it does expose is a CURATION mismatch worth naming: the generator's tier 1 picks the oldest open Low/Medium ledger finding without asking whether that finding's fix is something a builder CAN perform, and a process rule aimed at the reviewer is not. FIX: none is owed by F109, whose code this is not. The durable answer belongs to F258's generator — either a tier-1 filter that skips findings whose fix binds the reviewer rather than the code, or an explicit acceptance that some generated items will honestly block. Resolved when the generator either filters such findings or documents that blocking on them is the intended outcome.

- R-0785 — Low, THE SELF-USE GENERATOR REWRITES THE WHOLE QUEUE FILE WITH `ensure_ascii` AT ITS DEFAULT, ESCAPING ELEVEN EM DASHES IN CONTENT IT NEVER TOUCHED. Found by the WORKER of F109 R19 during that round's G8 sweep and MEASURED INDEPENDENTLY by the reviewer across `cb19e916..a06a6e69`: the literal U+2014 character occurs 11 times in `scripts/self_use_queue.json` before the append and 0 times after, while the six-character JSON escape that stands in for it occurs 0 times before and 18 times after. `append_generated_item` in `packages/orchestration/self_use_generator.py` ends with `path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")`, and `json.dumps` defaults `ensure_ascii=True`, so appending ONE item rewrites EVERY byte of a file that is otherwise operator-curated. EVERY PARSED VALUE IS UNCHANGED — the reviewer confirmed the four prior items compare equal after `json.loads` — so no reader misbehaves and nothing is corrupted in the sense that matters to code. WHY IT IS STILL A FINDING: the wrong state is on disk under `packages/` by way of a producer that damages bytes it was never asked to touch, which is the amend0827 rule 2 test, and the practical cost is that every future generated append produces a whole-file diff in which the one real change is invisible — the exact review hazard AGENTS.md's commit discipline exists to prevent. WHY LOW: values survive, the loader re-validates, and the file stays valid JSON with `schema_version` 2. FIX: pass `ensure_ascii=False` to that `json.dumps` call. NOT REPAIRED BY F109, and deliberately: this is F258's generator, and repairing another feature's production code from this branch is the scope drift AGENTS.md forbids outright. Resolved when `append_generated_item` preserves non-ASCII characters it did not author.

- R-0786 — Low, THE SELF-USE QUEUE FILE'S OWN DESCRIPTION NOW DENIES WHAT THE FILE CONTAINS. Found by the WORKER of F109 R19 and confirmed by the reviewer at `a06a6e69`: `scripts/self_use_queue.json` carries a `description` reading "Operator-curated DATA, not discovery: Remedy never invents an item and never appends one", while the file's fifth item is `SU-005`, whose own `provenance` field reads `generated (self-use-generator tier 1, ledger scan, R-0418)` — invented and appended by Remedy. The description's dated notes stop at 2026-08-30 and never record the generator's arrival at all. THIS IS THE SAME CLASS AS THE SEVEN STALE-PROSE FINDINGS THIS BRANCH ALREADY CARRIES — a sentence TRUE when written and falsified by a later feature landing — and it is the first instance of that class found OUTSIDE this feature's own files, which is worth saying because it suggests the class is a repository habit rather than a property of F109's rounds. WHY LOW: no behaviour depends on the description, every loader reads the `items` array, and the suite is green. WHY IT IS A FINDING AND NOT A SLIP: the wrong state is on disk in a file an operator is explicitly invited to curate by hand, and a curator who believes "Remedy never appends one" will misread a generated item as their own. FIX: restate the description so it distinguishes operator-curated items from generator-appended ones, and record the generator's arrival in its dated notes. NOT REPAIRED BY F109 — the file belongs to F257 and its generator to F258; this branch registers it and leaves it. Resolved when the description no longer denies that Remedy appends items.
END RECORD20

## EVIDENCESCRIPT — copy to `.remedy-wt/f109_evidence.py`, run with `python3 -B`

Adapted from `.agent/authored/f009-r33.md`'s slice of the same name, which is the
known-good shape. The reviewer PRE-SCANNED all six candidate suites at `a06a6e69`
with `build_review_manifest._unsafe_text`: ZERO node ids were rejected in any of
them, so no `-k` deselection is needed and none is ordered. The scanner's own red
control fired correctly on an absolute path in that same probe.

BEGIN EVIDENCESCRIPT
"""F109 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f109_closure_evidence", "remedy-job-evidence-f109-closure"
)
BASE = "5e18a8536afa086b591b5a2e13009d68d6227432"
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
    splits it (finding R-0611). No -k deselection is used for F109 — the
    reviewer scanned all six suites and none carries a rejectable id.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    cmd = "python3 -m pytest " + path + " -q"
    collect = subprocess.run(
        ["python3", "-m", "pytest", path, "-q", "--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest", path, "-q"], cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped) == (expect, 0, 0), (rid, passed, failed, skipped)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": cmd,
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": 0, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/orchestration/test_semantic_dedupe.py", 130),
    mkrun("vr-0002", "tests/orchestration/test_prompt_trace.py", 54),
    mkrun("vr-0003", "tests/orchestration/test_session_resume.py", 27),
    mkrun("vr-0004", "tests/ui_server/test_prompt_trace_payload.py", 20),
    mkrun("vr-0005", "tests/ui_server/test_prompt_trace_lens.py", 13),
    mkrun("vr-0006", "tests/test_observability_index.py", 14),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "files", len(r["test_files"]), "dur", r["duration_seconds"])

# Every packaged string is scanned; prove the ids and commands pass BEFORE the
# bundle is written, so a rejection is a red here and not a BLOCKED zip later.
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
    job_id="f109-closure",
    job_title="F109 Semantic dedupe - closure",
    step_range="T001-T003",
    prior_job_ids=[],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F109 closure",
    review_feature_id="f109",
)
print(json.dumps(result, indent=2, sort_keys=True))

# The output_hash preimage rule: sha256 over stdout_summary EXACTLY. This is the
# pitfall that blocked the F083 closure and it is not in the protocol's list.
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
END EVIDENCESCRIPT

## Done when — the eight gates. RUN each one and record its REAL exit code.

G1 TRANSPORT. `cmp .remedy-wt/f109-r20.md .agent/authored/f109-r20.md`, report the
   exit code; that scratch file is the REVIEWER'S OWN original. Then
   `sha256sum .agent/authored/f109-r20.md .agent/last_block.md` — one digest twice.

G2 THE PLAN. Extract PLAN20 by delimiter index and `cmp` against `.agent/plan.md`
   after C1: exit 0. Report `wc -l` under 50, and `grep -c '^## Goal'` and
   `grep -c '^## Next Steps'`, each 1.

G3 THE RECORD APPEND, four readings.
   (a) base size and sha256 of `.agent/live_review.md` at `a06a6e69`, appended
       length S, new size, and whether base + S equals it; still no trailing
       newline.
   (b) a SECOND READER counting no byte, over the WHOLE appended region: split the
       file on blank-line boundaries, let N be RECORD20's paragraph count as YOUR
       SCRIPT COUNTS IT from the slice, assert the LAST N units equal RECORD20's N
       paragraphs IN ORDER, printing each one's first 60 characters.
   (c) a NEGATIVE CONTROL on the FIRST appended paragraph, on a copy at
       `.remedy-wt/live_review_negative_control_r20.md`; show reader (b) rejects
       the copy and accepts the tracked file, report the tracked sha256 before and
       after, then delete the copy BY EXACT PATH and report `os.path.exists` False.
   (d) COUNTS AS A SET DIFFERENCE, never a subtraction (`R-0778`), base read from
       `git show a06a6e69:.agent/live_review.md` — THE ROUND'S OWN BASE. Report
       registered ids, DISTINCT registered, `Done:` lines, DISTINCT resolved, and
       `len(set(registered) - set(resolved))`, for base and new. Also
       `grep -c '^Gate: F109 R19 — '` = 1 and `grep -c '^- R-078[456] — '` = 3.

G4 THE EVIDENCE BUNDLE. Run EVIDENCESCRIPT and report: every `mkrun` line, the
   SCAN rejected count (must be 0) and the red control (must be truthy), the full
   summary dict `create_manual_completion_bundle` returned including its final
   verdict, and one `OUTPUT_HASH ... matches sha256(stdout_summary): True` line
   per run. Any False there is a BLOCKER — stop and report it.

G5 THE TREE WAS CLEAN AT BUILD TIME. Report `git status --porcelain` IMMEDIATELY
   before the zip build; it must be empty, and constraint 3 makes a package built
   from a dirty tree invalid.

G6 THE REVIEW ZIP. Build with
   `bash scripts/make_review_zip.sh --evidence-dir <EVIDENCE_DIR>`. Report the
   package FILENAME, its SHA-256, its `PACKAGE_STATUS`, `EVIDENCE_AUTHORITATIVE`,
   and the manifest's `committed_review_subject` base and head. PACKAGE_STATUS
   must read READY_FOR_REVIEW — it is the reading, NOT the exit code, which is 0
   either way. Also report the package's ARCHIVED PATH: the absolute directory it
   now sits in, or the literal `NOT ARCHIVED` if you left it where it was built
   (DECISION amend0827 D1). Record the head commit the manifest names; that is the
   ACCEPTED HEAD round 21's STATUS line will carry.

G7 THE INTEGRITY CHECK, closure precondition 3. The `remedy` binary may be denied,
   so run `from packages.orchestration.integrity_gate import run_integrity_checks`.
   The result is an object with `.passed`, `.fail_count` and `.checks` —
   ATTRIBUTES, not a dict, so `.get(...)` raises. Report `.passed` and
   `.fail_count`, and name every failing check if there are any.

G8 THE TREE AND THE SWEEP. `git status --porcelain` EMPTY at the end and
   `git ls-files .remedy-wt` returning nothing; confirm no evidence dir and no zip
   is tracked. Report each commit's insertion count from `git show --numstat` —
   the `+` column ONLY — for every commit EXCEPT C3, compared cell by cell against
   your own `## Commits` table. Then re-read each file this round touched and
   report every sentence now stale, with the reason.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md; no length cap.
Its STATE BLOCK carries the FORTSCHRITT slice VERBATIM. It must also carry: the
SESSION NUMBER (4) and round (20); the item-status table with C0a, C0b, C1, C2, C3
each appearing exactly once; a per-commit changed-files table with the `+/-`
column; ONE LINE PER GATE G1 through G8 with its real reading; and, in its own
unmissable section, THE CLOSURE FACTS round 21 needs — `Evidence job f109-closure`,
the package FILENAME, its SHA-256, its ARCHIVED PATH, the PACKAGE_STATUS, and the
ACCEPTED HEAD the manifest records. Also the open-finding count as a SET
DIFFERENCE, your deviations, and the next expected action. Then
`git push -u origin feature/f109-semantic-dedupe` and report the result. Create no
PR and write no STATUS line this round.
