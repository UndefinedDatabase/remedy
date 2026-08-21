── STEP R19 — F255 Teacher role · CLOSURE EVIDENCE ─────────────
Goal:        Meet the closure preconditions and produce the two artifacts only a
             worker can make. R18 PASSED: 0 branch-only failures over a full
             suite the reviewer re-ran itself. This round persists that verdict,
             RESOLVES R-0610, adds the feature file's missing Built State section
             — precondition 4, measured absent at `195b6cf3` — then runs the
             evidence job and builds the review zip. It authors NO STATUS line:
             that is R20's, because the line quotes values only this round's zip
             can produce.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             resolve R-0610 · C3 record the R18 verdict · C4 the Built State
             section · then the evidence job and the zip, from the clean tree at
             C4 · C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r19.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `docs/roadmap/features/T5_F255.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged in the TRACKED
             tree. NO source file and NO test file is touched. THE EVIDENCE DIR
             IS NEVER COMMITTED (DECISION 2026-08-01): it lives in scratch under
             the gitignored `.remedy-wt/`, and a pre-committed evidence dir puts
             evidence files into the base..HEAD review subject and packages
             BLOCKED_EVIDENCE. Neither is the zip committed. These paths are
             PRESENT at the base `195b6cf3` and must stay untouched:
             `packages/orchestration/teacher_model.py`,
             `packages/orchestration/teacher_qa.py`,
             `packages/orchestration/teacher_spend.py`,
             `apps/cli/commands/teach_cmd.py`, `docs/roadmap/STATUS.md`,
             `README.md`.
             `docs/roadmap/STATUS.md` and `README.md` are named untouched ON
             PURPOSE: they are R20's closure commit and must not move early.

             THE EVIDENCE JOB, AFTER C4 AND FROM A CLEAN TREE. First capture one
             `-v` log per scoped suite into `.remedy-wt/.cache/r19_logs/`, run
             SERIALLY, never two pytest processes at once:
               vr0001.txt  `python3 -m pytest tests/orchestration/test_teacher_model.py -v`
               vr0002.txt  `python3 -m pytest tests/orchestration/test_teacher_qa.py -v`
               vr0003.txt  `python3 -m pytest tests/orchestration/test_teacher_spend.py -v`
               vr0004.txt  `python3 -m pytest tests/orchestration/test_teacher_narration.py -v`
               vr0005.txt  `python3 -m pytest tests/cli/test_teach_cmd.py -v`
               vr0006.txt  `python3 -m pytest tests/cli/test_golden_path.py -v`
             The reviewer measured these six at `195b6cf3` as 18, 19, 5, 38, 19
             and 42 passed, each exit 0 with 0 failed and 0 skipped, and the
             EVIDENCESCRIPT slice asserts exactly those numbers so a drift stops
             the round instead of packaging a wrong count. THE FULL SUITE IS
             DELIBERATELY NOT A VERIFICATION RECORD: `len(node_ids) == selected`
             forbids filtering, and the packaging metadata scan rejects the
             redaction-torture parametrisations whose ids embed fake secrets by
             design, so a full-suite node-id list packages BLOCKED_EVIDENCE. The
             full-suite proof rides in the committed `.agent/gate_f255_r18/`
             evidence and the reviewer's own re-run instead.
             Then save the EVIDENCESCRIPT slice to
             `.remedy-wt/.cache/r19_evidence.py` and run it UNEDITED with
             `python3`. It writes the bundle to
             `.remedy-wt/f255_closure_evidence/remedy-job-evidence-f255-closure`.
             Report the summary dict it prints, in full.

             THE REVIEW ZIP, MANDATORY AND FRESH. With the tree still clean and
             the branch pushed, run
             `bash scripts/make_review_zip.sh --evidence-dir <the bundle dir>`
             and report its REAL output: the final zip filename, its SHA-256 and
             the PACKAGE_STATUS. A FAILING ZIP BUILD IS A CLOSURE BLOCKER — do
             not close, do not retry blindly; report the raw error and end the
             round under constraint 12. Report also the manifest's
             `committed_review_subject` base and head commits. Do NOT assert the
             bundle contains the value `READY`: `READY_FOR_REVIEW` is the ZIP's
             vocabulary and the bundle's own verdicts read `PASS` or
             `PASS_WITH_RISKS` (finding R-0597) — report what each artifact
             really says.

Constraints:
1. NO SLICE IS EDITED, including EVIDENCESCRIPT, which is SAVED AND RUN
   UNEDITED. Every text between the SLICE and END markers is applied byte for
   byte. A slice you believe is wrong is applied anyway and DECLARED in the
   handback. Marker lines never reach a target file.
2. TRANSPORT. `.remedy-wt/f255-r19.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r19.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL.
3. THE PLAN COMES FIRST (R-0377, R-0491, R-0548). Only C0a and C0b precede it.
4. THE RESOLUTION PERSISTS BEFORE THE VERDICT. C2 resolves R-0610 and C3 records
   the R18 verdict, in that order. This round resolves ONE finding and registers
   NONE: registered stays 186, resolved goes 3 to 4, open goes 183 to 182.
5. BOTH APPENDS ARE BLANK-SEPARATED (R-0578), each preceded by exactly one blank
   line. DONE0610 and RECORDR18 are EACH single-paragraph — the reviewer measured
   each for an interior blank line and found none — so the LAST-UNIT paragraph
   reading is exact for each. BUILTSTATE is MULTI-paragraph, so NO last-unit
   reading is ordered or owed for it and none may be reported as if it were; its
   proof is the prefix-and-remainder reading alone (R-0606).
6. THIS ROUND CONTAINS NO FROM/TO PAIR (§4.9, R-0207).
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH OF YOUR OWN. DONE0610 is
   the reviewer's authored resolution and the only one this round applies.
8. THE EVIDENCE DIR AND THE ZIP ARE NEVER COMMITTED, AND THE ZIP IS BUILT FROM A
   CLEAN TREE AFTER C4. A package built from a dirty tree is invalid.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit, before the zip build,
    and at the handback. No git worktree is created.
11. YOU DO NOT WAIT ON ANY CI RUN.
12. YOU CREATE NO PULL REQUEST AND YOU EDIT NEITHER `docs/roadmap/STATUS.md` NOR
    `README.md`. Those are R20's, and the STATUS line is authored by the reviewer
    from the values THIS round reports. If the zip fails, the feature does not
    close: report the raw error, write the handback and end.

<<<SLICE PLAN255R19
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
R19 is the CLOSURE EVIDENCE round. It persists the R18 verdict, resolves R-0610,
adds the feature file's Built State section — closure precondition 4, measured
absent — and then produces the two artifacts only a worker can make: the evidence
job and a FRESH review zip. It authors no STATUS line.

## Next Steps
1. R20 CLOSES THE FEATURE: the reviewer authors the STATUS `[x]` line from the
   values R19's zip reports, the worker applies it verbatim in the SAME commit as
   the README capability sync (R-0154), writes any closure candidates to
   `.agent/candidates.md`, and opens the pull request. That PR is NOT merged in
   its own session; it merges at the NEXT feature's Open PR Gate, which is the
   operator's manual-review window.

## Risks
- A FAILING ZIP IS A CLOSURE BLOCKER, not a retry. The feature goes `[!]` with a
  stated reason rather than closing without a package.
- THE OPEN SET STAYS LARGE AND THAT IS NOT A BLOCKER: the integrity gate's
  `high_blockers_open` check reports no open blocker or high finding, so every
  open item is a documented Medium or Low risk, which is what closure
  precondition 1 permits.
- R-0607, R-0608 and R-0609 REMAIN OPEN by design. All three are reviewer-process
  defects whose fix edits `docs/agents/`, a path the closure commit's own R-0154
  path set cannot reach; they route to a paydown branch.
<<<END PLAN255R19
<<<SLICE DONE0610
Done: R-0610 — RESOLVED at F255 R17 and verified by the reviewer at `b3146e91`. `remedy teach ask` gained `--file` at `da0ed2d9`, which reads ONE named workspace file through `Path.read_text` and passes its text as `code` with the path as `code_path`, giving grounding source (2) the production caller it had never had; reading writes nothing, so the `write_metadata` class DECISION F255 D10 rules for that command is untouched and the ledger row stays its only write. The SAME `code` and `code_path` reach both the context whose grounding list is printed and the context `ask_teacher` builds, so the printed sources cannot disagree with the prompt; and an unreadable path prints a line naming the path and the reason, leaves `code_path` None rather than asserting a file it never opened, and still answers, because a teacher that could fail a run would not be the passive role this feature specifies. The four tests at `aa3a47c9` pin the behaviour where it actually matters — they capture the prompt the injected transport seam received and assert the file's text and its path are IN it, that `[code]` is absent without the option, that an unreadable path is said out loud at exit 0, and that the data-root hash map with the ledger excluded by name is unchanged while the source file is byte-identical afterwards. THE MEASUREMENT THE FINDING TURNED ON WAS RE-TAKEN AND INVERTED: at `8f885b4f` the only caller of `ask_teacher` outside `tests/` passed neither argument, and at `b3146e91` that same single caller passes both. The overstatement half of the finding is answered too — the Fortschritt line that called T004 complete while source (2) had no caller was the reviewer's own authored text, and R17's replacement says plainly that at R16 it did not.
<<<END DONE0610
<<<SLICE RECORDR18
Gate: R19 — the R18 entry. R18 PASSED, and it is the ONE round of F255 entitled to the words "full suite". NO finding is registered against it: the round did exactly what its block ordered, declared no deviation, and the nine base-only failures it surfaced are all accounted for by findings ALREADY OPEN rather than by anything new — which is why no id was minted here, the open set having been searched for the DEFECT first, as checklist item 30 requires. THE GATE'S LOAD-BEARING NUMBER IS ZERO AND THE REVIEWER RE-RAN IT RATHER THAN READING IT BACK: `python3 -m pytest -n auto -q` in the primary checkout at `195b6cf3` exits 0 at `17315 passed, 20 skipped` in 146.26 s over a 146.8 s wall, with 0 lines beginning `FAILED` — the same 17315 the worker's own branch run reported at `b926a473`, and `branch_failed.txt` and `comm_branch_only_failures.txt` are both EMPTY files. BRANCH-ONLY FAILURES: 0, which is the gate's passing shape and the real number. THE BASE RUN AND ITS NINE: the base worktree at the merge base `b35d350b` — confirmed by the reviewer as BOTH `git merge-base main HEAD` and the tip of `main` — was created ON the branch `tmp/base-gate-r18` and never detached, artifact parity was restored with `shutil.copytree(..., symlinks=True)` with both destinations verified real directories rather than symlinks, and the run exited 1 at `9 failed, 17188 passed, 20 skipped`. PARITY_CLAIM=VOID, correctly: the `apps/ui/dist` digest and file count were unchanged on both sides and the PRIMARY checkout's `index.html` mtime never moved, but the BASE worktree's moved from 1787279383323951913 to 1787279587674706567, and a moved mtime voids the claim by rule because `_frontend_is_stale` decides by MTIME while the digest is blind to a byte-identical rebuild. THE VOID WAS HONOURED RATHER THAN NOTED: all nine ids were attributed individually by direct evidence, eight of them `tests/ui_server/test_live_state.py::TestUIServerIntegration` ids each carrying `ERROR: React UI not built.` in the base run's own captured stderr, and all nine pass serially at that same base commit, which is the direct evidence that none is a genuine base defect. TWO ALREADY-OPEN FINDINGS EXPLAIN ALL OF IT, and this round is fresh recurrence evidence for both rather than a new id for either. R-0445 is exactly the eight: it states that the canonical procedure restores parity by COPYING, that a copy preserves the SOURCE mtime while `git worktree add` stamps the checked-out sources with the checkout time, that the copied build is therefore ALWAYS older than the sources it was built from, and that this manufactures the same eight `test_live_state` failures on EVERY gate run for EVERY feature — and R18's measurement is that mechanism observed again, with the numbers named: newest `apps/ui/src` at 1787279477444570086 against `dist/index.html` at 1787279383323951913 as copied. R-0444 is exactly the unexplained mtime move: it states that the neutralisation flag does NOT stop every path from rewriting the artifact inside the base-run window, and R18's worker measured that move, proved the base log holds 0 lines matching `auto-build (` so `_auto_build_frontend` never launched npm, and then explicitly declined to name the mover — an honest "what is not claimed here" section rather than a guess, which is the behaviour this record exists to reward. The ninth id, `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`, is the known xdist-flake class: its repo-wide `pgrep` matched another worker's pid, and integration_gate.md step 4 records a serial-pass as flake rather than a blocker. THE EVIDENCE IS COMPLETE AND ITS PROVENANCE VERIFIES: nine `.txt` files under `.agent/gate_f255_r18/`, never `.log`, and the reviewer recomputed the sha256 of all five raw logs named in `full_log_provenance.txt` — branch run, base run, serial probe, parity before and parity after — every one MATCHING, with the raw logs kept outside the tracked tree per R-0176. THE ROUND'S OWN SHAPE HOLDS: transport byte-equal at the delegated digest over 24576 B and 273 lines; two slices; `.agent/plan.md` at `77f5f0b4` byte-equal to PLAN255R18 at 40 lines; the verdict append a byte-exact prefix-plus-remainder of 6105 B whose 211-unit paragraph split ends in RECORDR17; sets 186 / 3 / 183 / 0 unchanged at both ends because a `Gate:` paragraph is neither kind of line; 18 distinct `Gate: R` keys; six single-parent commits with insertions 273, 205, 18, 2, 284 and 41, all under the cap; zero marker leaks; the base worktree removed, `tmp/base-gate-r18` deleted and `git worktree list` reporting the primary checkout alone; and a 79-line handback carrying all seven mandated headings and an item table naming C0a through C4 exactly once.
<<<END RECORDR18
<<<SLICE BUILTSTATE
## Built State — what F255 delivered

Read at 195b6cf3. A fourth configured role, `teacher`, that explains a running
mission and answers questions about the operator's own code and never writes to
the run: two stages of deliberately unequal cost, three labelled grounding
sources, and spend reported as its own role in the F103 ledger.

- `packages/orchestration/teacher_narration.py` — STAGE 1. Deterministic
  templates keyed to an ENUMERATED set of run-log event names, declared in one
  place and pinned by a test. Zero tokens, no network, no model. An event outside
  the set narrates as unknown rather than being guessed at, which is the feature's
  honesty rule applied to its own blind spot.
- `packages/orchestration/teacher_qa.py` — the half of STAGE 2 that must not
  depend on a model: `GROUNDING_SOURCES` with a per-source honesty rule quoted
  into the prompt beside its own facts, the level dial (`student`, `beginner`,
  `pro`) that selects DEPTH and nothing else, and `claim_set`, computed from the
  facts ALONE so that the same question at two levels carries the same claims by
  construction rather than by hope.
- `packages/orchestration/teacher_model.py` — the teacher's OWN transport
  (DECISION F255 D8), because no generic text-completion provider exists here:
  `OllamaPlanner.raw_call` requires a schema and reads the PLANNER's
  configuration. One free-text chat, no schema, resolved through
  `resolve_role_config("teacher")`, behind an INJECTABLE `call` seam defaulting to
  `ollama_teacher_call`, so no test in this repository opens a socket to answer a
  question. `ask_teacher` refuses honestly when the resolved provider has no
  teacher transport or when that transport fails — not when "no model is
  configured", a state `resolve_role_config` never reaches (DECISION F255 D9) —
  and A REFUSAL IS NEVER BILLED, because there was no call to pay for.
- `packages/orchestration/teacher_spend.py` — exactly one ledger row per answered
  question, attributed to role `teacher` with a NULL `task_id` marking the class
  (DECISION F255 D7), so `query_cost(by="role")` reports teacher spend beside the
  mission roles with no change to that function. A figure the provider did not
  report lands NULL and never as zero.
- `apps/cli/commands/teach_cmd.py` and its two catalog entries — `remedy teach
  narrate <job_id>`, declared `read_only`, and `remedy teach ask "<question>"`
  with `--file`, `--job-id`, `--level`, `--project` and `--json`, declared
  `write_metadata` because it writes exactly that one ledger row and a false
  `read_only` would mislead the permission layer that reads the catalog (DECISION
  F255 D10). `--file` is grounding source (2)'s production caller: it reads one
  named workspace file, and an unreadable path is reported out loud rather than
  silently dropped, so no operator can believe an answer read code it never
  opened.
- THE READ-ONLY INVARIANT IS PROVEN BEHAVIOURALLY (DECISION F255 D4) rather than
  declared: `tests/cli/test_teach_cmd.py` hashes every file under the data root
  before and after each command and compares the maps — for `ask`, with the
  ledger file and its sqlite sidecars excluded BY EXPLICIT NAME and the excluded
  set itself asserted, so any OTHER write still fails the test.

Remedy deliberately does not add a follow or tail API for run logs, does not build
`remedy do watch` (DECISION F255 D5), does not create a repository-wide run-log
event registry (DECISION F255 D2), and scopes no budget LIMIT to the teacher: the
cost separation is REPORTING and not a cap (DECISION F255 D3). The cockpit panel
remains Tier 5 work and is not built here.
<<<END BUILTSTATE
<<<SLICE EVIDENCESCRIPT
import json
import os
import re
from datetime import datetime, timezone

REPO = os.path.abspath(".")
LOGS = os.path.join(REPO, ".remedy-wt", ".cache", "r19_logs")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f255_closure_evidence", "remedy-job-evidence-f255-closure"
)
BASE = "b35d350b84b1d371064a1f44e43f40da3ccfa540"

import subprocess  # noqa: E402

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD

_NODE = re.compile(
    r"^(tests/\S+::\S+)\s+(?:PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)", re.MULTILINE
)


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


def parse(log_name):
    with open(os.path.join(LOGS, log_name), encoding="utf-8") as fh:
        text = fh.read()
    ids = _NODE.findall(text)
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    return ids, passed, failed, skipped, dur, _tail(text)


def mkrun(rid, command, log_name, expect):
    ids, passed, failed, skipped, dur, tail = parse(log_name)
    assert passed == expect, (rid, passed, expect)
    assert failed == 0 and skipped == 0, (rid, failed, skipped)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
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
    mkrun("vr-0001", "python3 -m pytest tests/orchestration/test_teacher_model.py -v",
          "vr0001.txt", 18),
    mkrun("vr-0002", "python3 -m pytest tests/orchestration/test_teacher_qa.py -v",
          "vr0002.txt", 19),
    mkrun("vr-0003", "python3 -m pytest tests/orchestration/test_teacher_spend.py -v",
          "vr0003.txt", 5),
    mkrun("vr-0004", "python3 -m pytest tests/orchestration/test_teacher_narration.py -v",
          "vr0004.txt", 38),
    mkrun("vr-0005", "python3 -m pytest tests/cli/test_teach_cmd.py -v",
          "vr0005.txt", 19),
    mkrun("vr-0006", "python3 -m pytest tests/cli/test_golden_path.py -v",
          "vr0006.txt", 42),
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
<<<END EVIDENCESCRIPT

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit, immediately BEFORE the zip build, and at the handback;
   `git worktree list` reports the primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r19.md`, of `.agent/authored/f255-r19.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r19.md` by its markers; report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11). Report also
   that `.remedy-wt/.cache/r19_evidence.py` byte-equals the EVIDENCESCRIPT slice.
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R19; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report that C1
   is the FIRST commit other than C0a and C0b.
G5 THE RESOLUTION AND THE VERDICT. Over `.agent/live_review.md`, for C2 and then
   for C3: the previous blob is a byte-exact PREFIX; the remainder's sha256, byte
   and line counts; that it equals one newline followed by DONE0610 and by
   RECORDR18 respectively; and that the byte after each leading newline is not a
   newline. For EACH, a SECOND, INDEPENDENT blank-line paragraph split whose LAST
   unit is that commit's appended slice, with its sha256 under BOTH newline
   conventions. Re-measure constraint 5 rather than trusting it. Negative control
   for each: one character of the expected remainder mutated, rejected by BOTH
   readings.
G6 THE BUILT STATE SECTION. For C4 over `docs/roadmap/features/T5_F255.md`:
   prefix, remainder sha256 and counts, remainder equal to one newline followed
   by BUILTSTATE, and the separator byte. NO paragraph reading is ordered for it
   (constraint 5). Report that `## Built State` occurs 0x in that file at
   `195b6cf3` and 1x at C4, counted LINE-ANCHORED, which is closure precondition
   4 becoming true.
G7 THE SETS. Report registered / resolved / open / line-anchored `Landed:` over
   `.agent/live_review.md` at `195b6cf3`, at C2 and at C3, the registered count
   being lines matching `^- R-\d+ — ` and the resolved count lines matching
   `^Done: R-\d+ — `: the reviewer measured 186 / 3 / 183 / 0 at `195b6cf3`; C2
   owes 186 / 4 / 182 / 0 because it adds one resolved line and no registered
   one; and C3 owes the same as C2, a `Gate:` paragraph adding neither kind.
   Report that `Done: R-0610` occurs 0x at `195b6cf3` and 1x at C2, and that
   `Gate: R19 — the R18 entry.` occurs 1x at C3 and is the LAST line beginning
   `Gate: R`, every such header key being distinct (R-0584).
G8 THE INTEGRITY GATE, closure precondition 3. The `remedy` CLI is denied in this
   session class, so run the SAME code the CLI runs, through Python:
   `run_integrity_checks()` then `export_integrity_json()` from
   `packages.orchestration.integrity_gate`, and print the JSON. Report `passed`,
   `fail_count`, and the status of every named check. The reviewer measured
   passed=True, fail_count=0, check_count=5 at `195b6cf3`, with
   `high_blockers_open` reading "no open blocker/high findings" and
   `relevant_untracked` reading 0 — which is what makes closure precondition 1's
   "documented Medium/Low risk" true of the whole open set. If the CLI is in fact
   available to you, run it too and report both.
G9 THE SIX VERIFICATION LOGS. Report, per log, the command, the exit code and the
   summary line; each must be exit 0 with the passed count the Change section
   states and 0 failed and 0 skipped. State that they were run SERIALLY.
G10 THE EVIDENCE JOB. Report the full summary dict `r19_evidence.py` printed, the
   evidence directory path, and the number of entries in it. Report the `verdict`
   values that actually appear in `final_verifier_report.json` and in the summary
   dict — report what they SAY; do not assert any particular value (R-0597).
G11 THE REVIEW ZIP, from a clean tree after C4. Report the exact command, its
   exit code, the final zip FILENAME, its SHA-256 and the PACKAGE_STATUS, all as
   the script really printed them. Report the manifest's
   `committed_review_subject` base_commit and head_commit, and state whether that
   head equals the commit C4 created. A FAILING BUILD IS A BLOCKER: report the
   raw error, write the handback and end the round (constraint 12).
G12 THE CANARY AND THE STATE READERS, UNCONDITIONALLY (R-0607's rule), serially
   in the PRIMARY checkout, never two pytest processes at once:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed at
   `195b6cf3`. Report the exact command, exit code and tail of each.
G13 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 195b6cf3..<C4>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C5
   itself adds, with no path on either side alone — and that NEITHER
   `docs/roadmap/STATUS.md` NOR `README.md` appears in it. Report that each path
   named untouched is PRESENT at the base and ABSENT from the range; that every
   commit has one parent; and each commit's insertion column from
   `git diff --numstat` for C0a through C4, every one under 500, with the same
   `+/-` cells appearing byte-identically in the handback's `## Commits` table.
   C5's own cell belongs to the round report (R-0149).
   THE REFLOG IS TWO MEASURED CLAIMS (R-0601, R-0605): report the count of this
   round's entries whose OPERATION PREFIX reads exactly `commit`, WITH the commit
   it was taken at and the number of commits made AT THAT MOMENT, and state the
   two are equal; state no total (R-0494). Report the count whose prefix contains
   `amend`, `rebase` or `cherry`, which must be 0, and for EVERY `reset` entry
   report it with the demonstration that its destination is the commit the branch
   already pointed at (R-0608).
G14 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C3, `docs/roadmap/features/T5_F255.md` at C4 and `.agent/handoff.md` at C5
   — every count 0. `git push` after C4 and again after C5, reporting real output
   each time; the branch must be pushed BEFORE the zip is built.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C5 bundle, the `## Commits` table G13 pins, and
             one LINE per gate rather than its transcript (R-0582). Its
             `## External actions` section records the evidence job and the zip
             attempt WITH their outcomes — package filename, SHA-256 and
             PACKAGE_STATUS, or the raw error — because every artifact-build
             attempt appears in the handoff including a failed one. Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R20, the CLOSURE COMMIT: the
             reviewer authors the STATUS `[x]` line from the values THIS round
             reports, the worker applies it verbatim in the SAME commit as the
             README capability sync (R-0154), and opens the pull request, which is
             NOT merged in its own session. It states that R18 PASSED with its
             verdict ON DISK at C3, that R-0610 is RESOLVED at C2, that R-0607,
             R-0608 and R-0609 remain OPEN and route to a paydown branch, and that
             R19 ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON DISK. It states that
             no pull request is open. The handback carries this Fortschritt line
             verbatim (R-0418):
             Fortschritt: ~97 % (T001 through T004 COMPLETE and REVIEWED · the
             integration gate PASSED with 0 branch-only failures · evidence job
             and review zip built at this round · only the STATUS line, the README
             sync and the pull request remain) — Schätzung
──────────────────────────────────────────────────────────────
