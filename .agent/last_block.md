── STEP T002-apply / F111 — Round 13 ──────────────────────────────
Goal:
  Settle finding R-0315 by decision, then land the apply-and-fallback half of
  T002 as a seam module with tests. No call site is added — T003 wires it.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r13-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  append TEXT-A to .agent/live_review.md
  C4  apply PAIR-B and append TEXT-C to docs/roadmap/features/T2_F111.md, and
      in the SAME commit append the Landed line for R-0315 to
      .agent/live_review.md
  C5  new packages/orchestration/diff_repair_apply.py + PAIR-E in
      packages/orchestration/diff_repair_response.py
  C6  new tests/orchestration/test_diff_repair_apply.py
  C7  replace .agent/plan.md with TEXT-D, then rewrite .agent/handoff.md

Change — C5, the ONLY production commit of this round:
  New file packages/orchestration/diff_repair_apply.py. Public API, exactly:

    DIFF_REPAIR_MODE_DIFF = "diff"
    DIFF_REPAIR_MODE_FULL_FALLBACK = "full_fallback"

    @dataclass(frozen=True)
    class DiffRepairApplyResult:
        mode: str
        applied: bool
        fallback_reason: str
        apply_id: str
        snapshot_id: str
        files_modified: int
        errors: tuple[str, ...]

    def apply_diff_repair(
        response: DiffRepairResponse,
        repo_path: Path,
        *,
        job: Any,
        intent_id: str,
        data_dir: str | Path | None = None,
        job_fences: dict | None = None,
    ) -> DiffRepairApplyResult

  Behaviour, in this order and nothing beyond it:
  1. validate_diff_repair_response(response). Non-empty issues -> return
     mode=DIFF_REPAIR_MODE_FULL_FALLBACK, applied=False,
     fallback_reason="validation:" + "; ".join(issues[:3]),
     apply_id="", snapshot_id="", files_modified=0, errors=tuple(issues).
     Nothing on disk is read or written on this path.
  2. Fence precheck. When job_fences is None, derive it from the job EXACTLY as
     source_apply.apply_structured_patch does — {"allow": job.fences.allow,
     "deny": job.fences.deny} when hasattr(job, "fences") and job.fences is not
     None, else None — so the precheck and the applicator's own
     enforce_change_set read the SAME spec and cannot disagree. Then call
     precheck_diff_repair_fences(Path(repo_path), response, job_fences=<that>).
     allowed False -> return mode=DIFF_REPAIR_MODE_FULL_FALLBACK, applied=False,
     fallback_reason="fence_denied:" + ",".join(precheck.denied_paths),
     apply_id="", snapshot_id="", files_modified=0,
     errors=tuple(f"{p}: {r}" for p, r in precheck.reasons).
     The applicator is NOT called on this path — that is the feature file's
     acceptance criterion "a diff targeting a fence-denied path never reaches
     the applicator (rejected at validation)".
  3. diff_repair_response_to_patch(response), then
     source_apply.apply_structured_patch(patch, Path(repo_path),
     data_dir=str(data_dir) if data_dir else None,
     job_id=getattr(job, "id", None), job=job, intent_id=intent_id).
  4. apply_result.success True -> mode=DIFF_REPAIR_MODE_DIFF, applied=True,
     fallback_reason="", apply_id/snapshot_id/files_modified taken from
     apply_result, errors=().
  5. apply_result.success False -> mode=DIFF_REPAIR_MODE_FULL_FALLBACK,
     applied=False,
     fallback_reason="apply_failed:" + "; ".join(apply_result.errors[:3]),
     apply_id/snapshot_id from apply_result, files_modified=0,
     errors=tuple(apply_result.errors).

  Import apply_structured_patch at MODULE level (not inside the function), so
  the tests can monkeypatch packages.orchestration.diff_repair_apply.
  apply_structured_patch and prove the fence and validation paths never reach it.

  The module docstring states, in the repository's existing voice: this module
  implements NO rollback and NO diff parsing of its own; the all-or-nothing
  guarantee is source_apply's durable snapshot, created and verified before any
  mutation and restoring every touched file when a hunk conflicts; and the
  module is a SEAM with no call site until T003. Carry the one-line WHY comment
  above each public definition, as the sibling modules do.

  Same commit, PAIR-E in packages/orchestration/diff_repair_response.py. Nothing
  else in that file changes.

  PAIR-E is a REWRITE (the TO does not contain the FROM verbatim).
  FROM (3 lines, exact):
single walk that reads hunk headers. Remedy deliberately does not APPLY the
converted patch from this module — the apply-and-fallback half attaches to the
bridge, where the job, the approved intent and the snapshot already live.
  TO (4 lines, exact):
single walk that reads hunk headers. Remedy deliberately does not APPLY the
converted patch from this module — that is
``diff_repair_apply.apply_diff_repair``, which the bridge calls in T003 because
the job, the approved intent and the snapshot already live there.

Change — C6, tests/orchestration/test_diff_repair_apply.py, new file:
  Reuse the approved-job scaffolding of
  tests/orchestration/test_source_apply_transaction.py (_make_approved_job:
  REMEDY_DATA_DIR monkeypatched to tmp_path, Job with repo_generated_write set,
  one Artifact carrying patch_intent_explanations, save_job, make_intent_id,
  set_approval_state APPROVED). Do not invent a second scaffolding shape.
  Build DiffRepairResponse values directly; the header form the parser needs is
  "--- a/<path>" / "+++ b/<path>", as tests/orchestration/test_diff_repair_
  response.py already uses.

  Six tests, no more:
  1. clean apply. repo/a.py = "line1\nline2\n"; diff
     "--- a/a.py\n+++ b/a.py\n@@ -1,2 +1,2 @@\n-line1\n+LINE1\n line2\n";
     files ("a.py",). Assert mode == "diff", applied is True,
     fallback_reason == "", and (repo/"a.py").read_text() == "LINE1\nline2\n".
  2. a conflicting hunk falls back and leaves BOTH files byte-identical.
     a.py and b.py both exist; the diff's a.py section applies cleanly and its
     b.py section quotes a context line b.py does not contain; files
     ("a.py","b.py"). Read both files' bytes BEFORE the call. Assert
     mode == "full_fallback", applied is False, fallback_reason.startswith(
     "apply_failed:"), and each file's bytes equal what was read before. This
     is the all-or-nothing proof: it must read the real files, never the
     result object.
  3. a fence-denied path never reaches the applicator. files ("remedy.toml",)
     with a diff whose header pair names remedy.toml. Monkeypatch
     packages.orchestration.diff_repair_apply.apply_structured_patch with a
     function that raises AssertionError, so the test fails if the applicator
     is called at all. Assert mode == "full_fallback",
     fallback_reason.startswith("fence_denied:"), "remedy.toml" in
     fallback_reason, apply_id == "".
  4. a validation rejection short-circuits. Declared files ("a.py",) but the
     diff touches only b.py. Same applicator monkeypatch guard as test 3.
     Assert mode == "full_fallback", fallback_reason.startswith("validation:"),
     apply_id == "".
  5. a creation diff falls back instead of creating — this test PINS DECISION
     F111 D6. new.py does not exist; diff
     "--- /dev/null\n+++ b/new.py\n@@ -0,0 +1,2 @@\n+alpha\n+beta\n";
     files ("new.py",). Assert mode == "full_fallback", applied is False,
     fallback_reason.startswith("apply_failed:"), and
     (repo/"new.py").exists() is False. Name the test so a reader searching for
     the decision finds it, and put the D6 pointer in its docstring.
  6. job_fences is derived from the job when the caller passes none. Set
     job.fences = JobFences(allow=["src/**"], deny=[]) (packages.core.models),
     response touches docs/guide.md, call apply_diff_repair WITHOUT job_fences,
     and assert mode == "full_fallback" with fallback_reason.startswith(
     "fence_denied:") and "docs/guide.md" in fallback_reason. Without the
     derivation this test goes green through the default spec instead of the
     job's, so assert precheck reasons name docs/guide.md too.

Constraints:
  - AGENTS.md in full: self-review loop before every commit, one logical step
    per commit, <500 INSERTIONS per commit, plan.md current before committing,
    clean tree, push after every commit.
  - The change set is EXACTLY these nine paths and nothing else:
    .agent/authored/f111-r13-1.md, .agent/last_block.md, .agent/live_review.md,
    docs/roadmap/features/T2_F111.md,
    packages/orchestration/diff_repair_apply.py,
    packages/orchestration/diff_repair_response.py,
    tests/orchestration/test_diff_repair_apply.py, .agent/plan.md,
    .agent/handoff.md. Touching any other path is a scope violation — report it
    instead of doing it.
  - Do NOT modify packages/orchestration/source_apply.py in this round. The
    file-existence guard STAYS, by DECISION F111 D6.
  - Do NOT fix R-0313 (the blank-context "" normalisation) in this round. It is
    open by decision and belongs to R14.
  - Do NOT add a call site: builder_bridge.py, pingpong_loop.py and
    repair_context.py are untouched. A seam without a caller is the intended
    R13 end state.
  - Do NOT write any `Done:` paragraph in .agent/live_review.md. The reviewer
    authors every resolution (planner_reviewer_prompt.md §4.4). Your only mark
    is the single Landed line specified in TEXT-B-LANDED below.
  - No fuzzy apply, no shelling out to `patch` or `git apply`
    (docs/roadmap/features/T2_F111.md, Orchestrator brief).
  - Never force-push, never work on main, never merge.

TEXT-A — append verbatim to the END of .agent/live_review.md (commit C3):
### DECISION F111 D6 (2026-08-13) — new-file creation stays on the full-file path
Chosen for finding R-0315: amend the feature file to match v1 reality rather
than lift the applicator's file-existence guard. `_apply_unified_diff` keeps
requiring `full.is_file()`, so a creation diff fails the apply and the round
falls back to the full-file path — the route deletions already take. Three
reasons. The feature file lists applicator semantics under Do not touch, and
teaching the diff applicator to create files is exactly a semantics change.
A creation diff carries no existing content for the strict context check to
validate against, so the one guarantee this applier sells — every context and
removal line compared against the real file — buys nothing on that path. And
the full-file path already creates files through `_apply_file_op`'s `create`
action, under the same durable snapshot and the same rollback. Alternatives
considered: (a) implement creation behind the fence check, as the A9 sentence
said — rejected on the three reasons above; (b) leave the contradiction on disk
and let T003 discover it — rejected, that is how R-0315 was born. Reverse this
decision by deleting the D6 section of docs/roadmap/features/T2_F111.md and
restoring the A9 sentence.

TEXT-B-LANDED — append verbatim to the END of .agent/live_review.md, in commit
C4, after the feature-file edit is staged. Replace <sha> with C4's own short
SHA is NOT possible before committing, so write the path form instead, exactly:
Landed: R-0315 — T2_F111.md A9 sentence rewritten and the D6 Built State
section appended; the applicator guard is unchanged by decision.

PAIR-B — docs/roadmap/features/T2_F111.md, a REWRITE (the TO does not contain
the FROM verbatim). FROM (3 lines, exact, including the two leading spaces):
  exact content; fuzziness is a source of silent corruption. New-file
  creation inside a diff is allowed if the path passes fences; deletions
  require the full-file path in v1 (rare, riskier).
TO (3 lines, exact, including the two leading spaces):
  exact content; fuzziness is a source of silent corruption. New-file
  creation and deletions BOTH require the full-file path in v1 (rare,
  riskier) — DECISION F111 D6 below says why creation moved there.

TEXT-C — append verbatim to the END of docs/roadmap/features/T2_F111.md
(commit C4), separated from the preceding section by one blank line:
## Built State — new-file creation stays on the full-file path (DECISION F111 D6, 2026-08-13)
Amends the "Edge cases & assumption defaults (A9)" sentence above: in v1 a diff
that CREATES a file is not applied as a diff. `source_apply._apply_unified_diff`
requires `full.is_file()` and otherwise reports `<path>: file not found for
diff`, so a creation diff fails the apply and the round falls back to the
full-file path — the route deletions already take, for the same reason. Lifting
the guard would widen applicator semantics, which this file lists under Do not
touch, and it would send the `@@ -0,0 +1,N @@` shape onto a path with no
existing content for the strict context check to validate against. The fallback
is honest rather than silent: the attempt is discarded whole, the reason is
recorded, and the full-file round creates the file through `_apply_file_op`'s
`create` action under the same durable snapshot. Remedy deliberately does not
create files from a unified diff in v1. Reverse this decision by deleting this
section and restoring the A9 sentence (finding R-0315).

TEXT-D — the COMPLETE new content of .agent/plan.md (commit C7). Replace the
file; do not merge with what is there:
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 34319061 — R12's verdict
lives in the handoff (planner_reviewer_prompt.md §4.13 terminator).
Next free finding ID: R-0316. Open findings: 33 entering R13. None High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R13 closes T002. R-0315 is settled by DECISION F111 D6: new-file
creation stays on the full-file path in v1 and the feature file is
amended to say so. `diff_repair_apply.apply_diff_repair` is the
apply-and-fallback seam — validate, fence-precheck, convert, apply,
and on any failure report mode `full_fallback` with a named
`fallback_reason`. It has NO call site yet.

## Next Steps
1. R14 — R-0313, the response-side blank-context normalisation. A
   blank context line stripped to "" makes an otherwise valid diff
   REJECT. It belongs in the response half, where the diff's own line
   structure is known, never in `_apply_hunks`, where a trailing ""
   from `split("\n")` would make the last hunk over-consume.
2. R15 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- All-or-nothing rests entirely on source_apply's durable snapshot.
  `apply_diff_repair` adds no rollback of its own, so a snapshot
  regression is a fallback-correctness regression.
- A green suite over unreferenced modules is not a working feature.
  R15 is the round that makes F111 real.

Done when — run every command, record the REAL exit code and the REAL counted
value for each. "Green" as a word is a finding.
  a. cmp .remedy-wt/f111r13/BLOCK .agent/authored/f111-r13-1.md
     cmp .agent/authored/f111-r13-1.md .agent/last_block.md
     cmp .remedy-wt/f111r13/PLAN .agent/plan.md
     All three exit 0 and print nothing.
  b. grep -c 'creation inside a diff is allowed' docs/roadmap/features/T2_F111.md
     -> prints 0, exit 1 (that is the pass).
     grep -c 'creation and deletions BOTH require' docs/roadmap/features/T2_F111.md
     -> 1.
     grep -c '^## Built State — new-file creation stays' docs/roadmap/features/T2_F111.md
     -> 1.
  c. grep -c 'the apply-and-fallback half attaches to the' packages/orchestration/diff_repair_response.py
     -> prints 0, exit 1 (that is the pass).
     grep -c 'diff_repair_apply.apply_diff_repair' packages/orchestration/diff_repair_response.py
     -> 1.
  d. grep -c '^### DECISION F111 D6' .agent/live_review.md -> 1.
     grep -c '^Landed: R-0315' .agent/live_review.md -> 1.
     grep -c '^Done:' .agent/live_review.md -> 7, unchanged from R12.
  e. python3 -m pytest tests/orchestration/test_diff_repair_apply.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_source_apply_transaction.py -q
     -> exit 0. Record the passed count.
  f. python3 -m pytest tests/docs/ -q -> exit 0. Required because this round's
     change set includes docs/roadmap/** (planner_reviewer_prompt.md §3,
     docs-round gate). Record the passed count.
  g. python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0, canary.
     Record the passed count.
  h. grep -rn 'diff_repair_apply' packages/ apps/ --include='*.py' | grep -v
     '^packages/orchestration/diff_repair_apply.py' -> exactly ONE line, the
     PAIR-E docstring pointer in diff_repair_response.py. More than one means a
     call site was added, which this round forbids.
  i. git status --porcelain -> empty.
     git diff --name-only 34319061..HEAD -> exactly the nine paths listed under
     Constraints, no others.
     git show --stat <sha> for EVERY commit -> each insertion count under 500;
     report the numbers.
     git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD
     -> 0	0 after the final push.

Handback: completion report + rewrite .agent/handoff.md per AGENTS.md
(feature + round, branch, per-commit table with insertion counts, changed-files
table, the a-i gate results with real exit codes and counted values, open
findings count, item-status table covering C1-C7 exactly once each, next
expected action). Repeat this Fortschritt line verbatim in the handoff:
Fortschritt: ~68 % (T001 ✅ · T002 ✅ Record+Split+Schema+Fence+Apply · T003 offen · R-0315 entschieden, R-0313 offen für R14) — Schätzung
──────────────────────────────────────────────────────────────
