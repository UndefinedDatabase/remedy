# Handback — F033 · SESSION 7 · round 28 · THE CLOSURE PREPARATION ROUND

> Written by the WORKER at the close of the round-28 delegation. The reviewer
> holds the pre-emission original of the step block and runs the other half of
> the transport comparison itself.

## THE CLOSURE FACTS, as their own labelled lines

The next round quotes these without re-deriving them.

    Evidence job    f033-closure
    package         remedy-review-20260829-154912-READY_FOR_REVIEW.zip
    SHA-256         3b646ca5a18f10ae21f3218a753be00970762ba0fe4513ef53a3f60a9f711ccc
    package path    /home/decodeux/Repos/remedy-history/zips
    accepted HEAD   8738c5f1643b2bd667bc796257a4ddc502f36191
    self-use        NONE (queue exhausted)

`package path` is the ARCHIVED PATH DECISION amend0827 D1 requires: the absolute
directory the package was MOVED to by `scripts/make_review_zip.sh`, which is
OUTSIDE this repository's working tree. It is NOT the literal `NOT ARCHIVED`.
The package status is `READY_FOR_REVIEW`, so the operator's review window is
open at that path.

## Session

SESSION 7 of feature F033 · round 28 · rounds so far 28.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

Both triggers of the amend0827 rule 6 soft limit remain reached: this is the
SEVENTH session and the TWENTY-EIGHTH round. The scope report is carried
forward with its arithmetic advanced — item 3 of "what is missing" is now half
delivered, and the closure's preconditions are all measured TRUE.

### Scope report — required by operator amendment amend0827 rule 6

WHAT IS FINISHED. The feature's Goal & Done is met on every clause the feature
file states: stable content-hash ids and their stability property (T001); the
command, its validation, the all-or-nothing subset apply, the hunk ledger and
the write door (T002); partial-state truth on all three surfaces — viewer, task
node and report line (T003, R-0738); and the rejection-to-repair loop end to
end. THE FEATURE'S FUNCTIONAL SCOPE CLOSED AT ROUND 24 and this round did not
touch it. Round 26 added the `docs/` operator guide. Round 27 ran the
integration gate.

NEWLY FINISHED THIS ROUND: the round-27 verdict is BOOKED, R-0750 is
REGISTERED, R-0736 is EXTENDED without spending an id, the feature file now
carries its Built State section, and the four closure preconditions that must
hold BEFORE a STATUS line can be authored are all measured TRUE — the integrity
check PASSES, the evidence bundle is complete on all eight closed-schema gates,
and the review zip built from a CLEAN tree after the last content commit is
`READY_FOR_REVIEW`. THIS ROUND CHANGED NO FILE UNDER `packages/`, `apps/` OR
`tests/`: the measured path set over `f13134fe`..C3 is five paths, four under
`.agent/` and one under `docs/roadmap/features/`.

WHAT IS MISSING, and none of it is feature work:
  1. ~~the `docs/` operator guide~~ — DELIVERED at round 26.
  2. ~~the integration-gate round~~ — DELIVERED at round 27.
  3. The closure sequence, which by precedent is two rounds. THIS ROUND IS THE
     FIRST OF THE TWO. What remains for the second: the STATUS `[x]` line and
     the README capability sync in ONE commit (the R-0154 pin), the final
     `.agent/` state, then the pull request — which is NOT merged in this
     session.
  4. R-0745 (Low, OPEN) — the write door's import guard reads DIRECT imports
     only, and the door's transitive closure reaches `subprocess` through
     `evidence_index`.
  5. R-0750 (Medium, OPEN, registered THIS round) — a second oversize commit
     landed on this branch. Its fix is forward-looking by construction: history
     is not rewritten, the repair is to the ORDER a future integration-gate
     block gives.

THE PROPOSAL, unchanged and still a proposal only: let F033 close on the
Acceptance it has met, carrying R-0745 and R-0750 as the documented Low and
Medium risks the closure protocol's precondition 1 admits, so the STATUS line
reads PASS_WITH_RISKS. NEITHER READING IS EXECUTED ON A WORKER'S OWN AUTHORITY.

## Range

Review of `f13134fe`..`8738c5f1` on branch `feature/f033-hunk-approval-v2`,
pushed. FIVE commits, C0a through C3; the range is named to C3 because C5 is
the commit that writes this file and cannot name its own SHA (R-0149 pattern),
and because C4 IS NOT A COMMIT — see deviation 1.

## Commits

### 5541f4a5 docs(f033): save the session 7 closure prep block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r28.md | +302/-0 | C0a — the block saved verbatim, copied with `shutil.copyfile`, never retyped |

### 685cc0e7 docs(f033): mirror the closure prep block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +231/-210 | C0b — the same bytes mirrored, copied from the saved file |

### 7291698f docs(f033): retarget the plan at the closure prep round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +22/-22 | C1 — full rewrite from slice PLAN28 |

### 24ea131f docs(f033): book the round 27 verdict, register R-0750, extend R-0736
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6/-0 | C2 — slice RECORD28 appended: the R27 `Gate:` paragraph, the R-0750 registration, and the R-0736 EXTENSION which spends no id |

### 8738c5f1 docs(f033): record the feature file built state at closure
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T5_F033.md | +54/-0 | C3 — slice BUILTSTATE appended as the LAST section, per the T5_F256 convention. THE LAST CONTENT COMMIT; the zip's accepted HEAD |

### C4 — NOT A COMMIT
| Path | +/- | Reason |
|------|-----|--------|
| (none) | — | C4 produced the integrity check, the evidence bundle and the review zip. NOTHING of it is committable: the evidence dir is gitignored BY DESIGN and the package is written outside the repo. The Bundle is therefore SIX commits, not seven. See deviation 1 |

### C5 — the handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C5 — this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f033-hunk-approval-v2` after C3 — REAL exit 0,
  `f13134fe..8738c5f1`. Run BEFORE the zip build because the canonical zip build
  sequence of docs/roadmap/STATUS_closure_protocol.md step 1 requires a clean
  AND pushed branch. See deviation 2.
- `git push origin feature/f033-hunk-approval-v2` after C5 — the handback push.
- NO PR created, none edited, none merged. NO merge of any kind. No force-push.
- No `gh` command run. No worktree added or removed.
- `bash scripts/make_review_zip.sh --evidence-dir <dir>` — REAL exit 0; it MOVED
  the package to `/home/decodeux/Repos/remedy-history/zips`.

## Verification

Every exit code below is REAL, taken from `subprocess.run(...).returncode`
inside a script under the gitignored `.remedy-wt/`, never through a pipe
(constraint 9). ALL EIGHT GATES ARE GREEN.

G1 TRANSPORT — REAL exit 0.
    FIVE readings, ONE digest:
      `.remedy-wt/f033-r28-block.md`   25853 bytes, 302 lines
      committed `.agent/authored/f033-r28.md` (C0a) 25853 bytes, 302 lines
      committed `.agent/last_block.md`        (C0b) 25853 bytes, 302 lines
      both working-tree copies                     25853 bytes, 302 lines
    ALL FIVE share sha256
      49ac004ea04f27c2ad007dc737218610c2dae92c94c36bde5a2911bf6617f275
    That EQUALS the digest, the 25853 bytes and the 302 lines the reviewer
    stated for its pre-emission original. Both hops used `shutil.copyfile`;
    nothing was retyped. Reading `.remedy-wt/` was NOT denied, so the
    report-and-stop fallback was not used.

G2 THE PLAN, at C1 — REAL exit 0.
    byte length 2197 · line count 42 · under 50 lines True
    byte-EQUAL to slice PLAN28 True
      (both sha256 8bd8a4811194f7d7b864f424bb63334247e93eaf24f38a538a3bcec2b425e916)
    holds `## Goal` True · holds substring `Steps` True

G3 THE RECORD APPEND, at C2 — REAL exit 0.
    MEASURED base 1625403 + 1 + RECORD28 8596 = 1634000 = committed.
      RECONSTRUCTS True. The base was RE-MEASURED by this worker at the commit
      it appended at (constraint 2); it matches the 1625403 the block stated,
      but the reading is this worker's own.
    pre-commit blob is byte PREFIX True · slice is exact SUFFIX True
    separator byte is a newline True · working tree equals committed blob True
    N COUNTED by the script: 3. File blank-line units: 734.
    LAST 3 units EQUAL the slice's paragraphs IN ORDER True
      unit -3 `Gate: F033 R27 — THE INTEGRATION GATE. THE R…`
      unit -2 `- R-0750 — Medium, A SECOND OVERSIZE COMMIT …`
      unit -1 `R-0736 EXTENSION — INDEPENDENTLY CONFIRMED A…`
    NEGATIVE CONTROL: the FIRST appended paragraph spans [1625404, 1629541);
      flip offset 1627472, inside that span True; byte b'o' flipped to b'O'.
      reader A, SUFFIX     : accepts unflipped True / rejects flipped True
      reader B, PARAGRAPHS : accepts unflipped True / rejects flipped True
      reader 0, BASE PREFIX: accepts unflipped True / accepts flipped True —
        UNMOVED, and necessarily so: the flip at 1627472 lies beyond the base's
        1625403 bytes, so a prefix reader over the base cannot see it. See
        deviation 3.

G4 THE LEDGER, at `f13134fe` and at C2 — REAL exit 0.
    | rev | `^- R-\d+ — ` distinct | `^Done: R-\d+ — ` lines | distinct | `^Landed: ` | `^Gate: F033 R27 — ` | open |
    |-----|------------------------|-------------------------|----------|-------------|----------------------|------|
    | f13134fe | 310 | 55 | 53 | 22 | 0 | 257 |
    | 24ea131f | 311 | 55 | 53 | 22 | 1 | 258 |
    ADDED registered ids `['R-0750']` — exactly the ordered id, and only it.
    REMOVED registered `[]`. Resolved lines, resolved distinct and `^Landed: `
    all UNMOVED — this round resolved nothing, as ordered.
    `^R-0736 EXTENSION — ` occurrences 0 -> 1.
    `^- R-0736 — ` occurrences 1 -> 1, UNMOVED.
    THE EXTENSION THEREFORE ADDED NO ID: the open set rises by exactly one, and
    that one is R-0750.

G5 THE BUILT STATE, at C3 — REAL exit 0 on both halves.
    ORDERED EQUALITY:
      before 6358 bytes / 117 lines -> after 9936 bytes / 171 lines
      pre-commit blob is a byte PREFIX of the post-commit file True
      slice is an exact SUFFIX of it True
      lines C3's diff ADDS = 54 = 1 blank separator + 53 slice lines
      ADDED lines are exactly the slice's lines IN ORDER True
      DELETED lines 0 — ZERO, as the append-only constraint requires
      no `## Built State` heading existed in the file before C3 True
    `python3 -m pytest tests/docs/ -q` — REAL exit 0, **295 passed** in 0.44s.
      That is EXACTLY the 295 this branch measured at round 26; the count did
      not move, so the new section registered cleanly.

G6 THE INTEGRITY CHECK AND THE EVIDENCE JOB, at C4 with a CLEAN tree — REAL
    exit 0. `git status --porcelain` was EMPTY before either half ran.
  (a) `python3 -m apps.cli.grouped integrity check --json` — REAL exit 0.
      VERDICT FIELD: `"passed": true`, `fail_count` 0 over `check_count` 5.
        handler_import       pass  handlers=341
        live_review_verdict  pass
        plan_consistency     pass  unchecked=0
        relevant_untracked   pass  untracked=0, relevant=0
        high_blockers_open   pass  no open blocker/high findings
      NOT a non-PASS, so no closure blocker. The `remedy` console script is
      denied in this sandbox; the `python3 -m apps.cli.grouped` form was used.
  (b) `packages.orchestration.job_evidence.create_manual_completion_bundle`
      with `review_feature_id="f033"` — the canonical producer, not
      `write_runtime_integration_gate`.
      JOB ID: `f033-closure`
      EVIDENCE DIR:
        `/home/decodeux/Repos/remedy/.remedy-wt/f033_closure_evidence_r28/remedy-job-evidence-f033-closure`
      RESULT: verdict `PASS_WITH_RISKS`, commit_count 237, authority_count 44,
        total_passed 458, partition T001 15 / T002 15 / T003 14.
      THE EIGHT CLOSED-SCHEMA GATE DOCUMENTS, listed as written on disk:
        final_verifier_report  -> final_verifier_report.json     PRESENT
        fresh_evidence         -> fresh_evidence_gate.json       PRESENT
        artifact_contract      -> artifact_contract_gate.json    PRESENT
        change_provenance      -> change_provenance_gate.json    PRESENT
        manifest_integrity     -> manifest_integrity.json        PRESENT
        postmortem_integrity   -> postmortem_integrity.json      PRESENT
        commit_execution       -> commit_execution_gate.json     PRESENT
        runtime_integration    -> runtime_integration_gate.json  PRESENT
      ABSENT COUNT 0 — the set is COMPLETE. 295 files total in the dir.
      The nine verification runs were all re-run green before the bundle was
      written, each with `len(node_ids) == selected` and every `test_files`
      entry a real FILE, and every packaged node id and command string was put
      through `build_review_manifest._unsafe_text` FIRST: 0 rejected, with a
      red control confirming the scanner was live. `output_hash` matches
      `sha256(stdout_summary)` on all nine.

G7 THE REVIEW ZIP, at C4, from a CLEAN tree after C3 — REAL exit 0.
    `bash scripts/make_review_zip.sh --evidence-dir <the dir G6 reported>`
    PACKAGE FILENAME  remedy-review-20260829-154912-READY_FOR_REVIEW.zip
    SHA-256           3b646ca5a18f10ae21f3218a753be00970762ba0fe4513ef53a3f60a9f711ccc
      — recomputed independently by this worker over the archived file; it
        matches the hash the script printed.
    ARCHIVED PATH     /home/decodeux/Repos/remedy-history/zips
      — the absolute directory the package was MOVED to, outside the repo
        working tree. Not `NOT ARCHIVED`.
    size 20486078 bytes · member_count 3605 · authoritative_count 44
    PACKAGE_STATUS = READY_FOR_REVIEW · EVIDENCE_AUTHORITATIVE = true
    REVIEW_SUBJECT_ALIGNMENT = PASS · publication_capability SUPPORTED
    MANIFEST `committed_review_subject`, read from `.review_zip_manifest.json`
    INSIDE the built zip:
        base_commit      bd8d952942d8ec1d243d787ccfe16e0ad04360d2
        head_commit      8738c5f1643b2bd667bc796257a4ddc502f36191
        base_is_ancestor True · commit_count 237 · file_count 89 · tombstones 0
      THE HEAD IS C3. Confirmed by direct comparison: head_commit == C3 True.
    THE ZIP IMPORT CHECK'S OWN RESULT: PASSED. `scripts/make_review_zip.sh`
      runs its verification inline and aborts non-zero on any failure; it exited
      0 and emitted no `REVIEW_ZIP_ERROR` and no verify error. Independently
      re-read from the manifest: `ready_gate_matrix.ok` true with
      `blocking_reasons` [], `token_truth_authority` VERIFIED_EQUAL,
      `final_verifier_reproducible` true, `snapshot_inventory_status.ok` true,
      `packaging_warnings` [], `external_paths_detected` [], and the
      per-document verdicts artifact_contract PASS, change_provenance PASS,
      fresh_evidence PASS, runtime_integration PASS, final_verifier_report
      PASS_WITH_RISKS, manifest_integrity ok=true, postmortem_integrity ok=true,
      commit_execution NEEDS_HUMAN_APPROVAL (the expected state for an unmerged
      closure). `packaged_evidence_job_id` = `f033-closure`, task ids
      T001/T002/T003. STALE EVIDENCE DIRS INSIDE THE ZIP: 0 — the
      `remedy-job-evidence-*` prefix appears on no member.
    THE BUILD DID NOT FAIL, so there is no raw error to record and no closure
    blocker. It was run ONCE; no retry with different arguments was needed. No
    manifest was hand-edited.

G8 STRUCTURE, at C4 — REAL exit 0. ALL FOUR CLAUSES HOLD.
    `git status --porcelain` -> `''`, EMPTY True.
    PER-COMMIT INSERTIONS, C0a through the last commit before the handback,
    every commit single-parent:
        5541f4a5 302 · 685cc0e7 231 · 7291698f 22 · 24ea131f 6 · 8738c5f1 54
      MAX 302. EVERY COMMIT UNDER 500 = **True**. This round had no evidence log
      to commit, so — as the block says — a number over 500 here would have been
      a defect rather than a declared exception. There is none.
    PATH SET over `f13134fe`..C4 EQUALS the change set minus `.agent/handoff.md`
      in BOTH directions: `measured - declared` [] and `declared - measured` [].
      The five paths: `.agent/authored/f033-r28.md`, `.agent/last_block.md`,
      `.agent/plan.md`, `.agent/live_review.md`,
      `docs/roadmap/features/T5_F033.md`.
      Files under `packages/`, `apps/` or `tests/` in this range: NONE.
    `git ls-files --others --exclude-standard` -> COUNT 0, list EMPTY.
      THE EVIDENCE DIR AND THE PACKAGE ARE UNTRACKED, NOT MERELY UNCOMMITTED,
      and this is shown rather than asserted:
        `git check-ignore -v <evidence dir>` -> exit 0, rule
          `.gitignore:235:.remedy-wt/`
        `git ls-files --error-unmatch <evidence dir>` -> exit 1, i.e. NOT TRACKED
        tracked files under `.remedy-wt/` = 0
        repo toplevel `/home/decodeux/Repos/remedy`; the package directory
          `/home/decodeux/Repos/remedy-history/zips` is OUTSIDE it entirely.
      NO EVIDENCE DIRECTORY WAS COMMITTED. Both were left where they are.

## Authored-text proofs

All three slices were EXTRACTED from the committed `.agent/authored/f033-r28.md`
by script, between the marker lines exclusive — none was retyped at any point.

| Slice | bytes | lines | sha256 (head) | disk-to-disk result |
|-------|-------|-------|---------------|---------------------|
| PLAN28 | 2197 | 42 | 8bd8a4811194f7… | `.agent/plan.md` byte-EQUAL, G2 |
| RECORD28 | 8596 | 5 (3 paragraphs) | 3ca60681d4e457… | exact SUFFIX of `.agent/live_review.md` at C2, G3 |
| BUILTSTATE | 3577 | 53 | 0340c833832084… | exact SUFFIX of `docs/roadmap/features/T5_F033.md` at C3, G5 |

Transport comparison for the block itself is under G1: five readings, one
digest, equal to the reviewer's stated
`49ac004ea04f27c2ad007dc737218610c2dae92c94c36bde5a2911bf6617f275`.

## Deviations & assumptions

1. C4 IS NOT A COMMIT, AND THE BUNDLE IS SIX COMMITS RATHER THAN SEVEN. The
   block's Bundle item 6 provides for exactly this and asks which it was: it was
   the six-commit form. G6 and G7 produced NO committable file. The evidence
   directory is gitignored by design — committing it would put evidence into the
   base..HEAD review subject and package BLOCKED_EVIDENCE — and the package is
   written outside the repository altogether. A departure from the ordered commit
   sequence belongs here even when the block anticipated it (R-0485), which is
   why it is stated first. Nothing was added or dropped.
2. THE BRANCH WAS PUSHED BEFORE THE ZIP BUILD, NOT ONLY AFTER THE HANDBACK. The
   delegation says to push after C5; the canonical zip build sequence in
   docs/roadmap/STATUS_closure_protocol.md step 1 requires the tree clean AND
   the branch pushed BEFORE `make_review_zip.sh` runs. Both were honoured: a
   push after C3 to satisfy the protocol, and the ordered push after C5. Neither
   was a force-push and no PR was touched.
3. G3's "BOTH READERS" WAS READ AS THE TWO READERS THAT COVER THE APPENDED
   REGION, and the third is reported anyway. A byte flipped INSIDE the first
   appended paragraph lies beyond the base blob's last byte, so a
   base-prefix reader is structurally incapable of rejecting it — it is the
   BASE region's reader, not the appended region's. The two readers that do
   cover the appended text, SUFFIX and PARAGRAPH-ORDER, both accept the
   unflipped bytes and both reject the flipped ones, which is the discrimination
   the negative control exists to demonstrate. The prefix reader's UNMOVED
   result is reported under G3 rather than hidden, so the reviewer can see the
   full three-reader table. No gate wording was weakened to make this pass.
4. THE NINE VERIFICATION SUITES IN THE EVIDENCE BUNDLE WERE CHOSEN BY THIS
   WORKER. The block ordered the canonical producer and the `review_feature_id`
   but named no suites. Chosen: the seven `tests/orchestration/test_hunk_*` and
   `test_pingpong_job_hunk_ledger` / `test_builder_prompt_hunk_rejections`
   suites covering T001-T003, `tests/cli/test_patch_cmd.py` for the operator
   door, and `tests/docs/test_docs_consistency.py`. 458 tests, all green, all
   SCOPED — deliberately NOT a full-suite node-id list, which is the F080 R4
   lesson (d) the closure protocol states. The full-suite proof rides in the
   committed round-27 integration-gate evidence, not in this bundle.
5. THE EVIDENCE DIR WAS PLACED UNDER THE GITIGNORED `.remedy-wt/`, following the
   F257 closure precedent, so that it is outside the review subject by
   construction. It was NOT deleted at cleanup — the block says to leave it and
   the package where they are.
6. THE `remedy` CONSOLE SCRIPT WAS NOT USED ANYWHERE. It is denied in this
   sandbox. The integrity check ran as
   `python3 -m apps.cli.grouped integrity check --json`, stated here so the
   evidence chain stays honest (constraint 8).
7. COMMIT SUBJECTS CARRY NO `Co-Authored-By` TRAILER, matching all 232 prior
   commits on this branch. AGENTS.md's "prefer repository state over session
   memory" governs; no subject contains a leading-slash token, an absolute path
   or a secret-like string.
8. NO DEFECT OUTSIDE THE CHANGE SET WAS FOUND THIS ROUND, and nothing outside it
   was touched. `docs/roadmap/STATUS.md`, `README.md` and
   `scripts/self_use_queue.json` were NOT edited — they belong to the next
   round's single closure commit, and splitting them is what the R-0154 pin
   forbids. The self-use queue was READ only: 1 item, `SU-001`, `consumed_by`
   `F257`, ZERO pending, and `next_self_use_item()` returns `None`. That is
   precondition 6's own "exhausted, not blocked" branch, so the closure records
   `self-use NONE (queue exhausted)` and closes normally.
9. Scratch lived under the gitignored `.remedy-wt/` and was run as
   `python3 -B <path>`. All 24 `r28_*` artifacts — 21 scripts, including the
   removal script itself, and the 3 extracted slice `.bin` files — were removed
   BY EXACT PATH, each named individually in a literal list, never by glob;
   `git status --porcelain` is empty and
   `git ls-files --others --exclude-standard` returns 0 paths. TWO THINGS UNDER
   `.remedy-wt/` WERE DELIBERATELY KEPT: the evidence directory
   `.remedy-wt/f033_closure_evidence_r28/`, because the block says to leave it
   and the package where they are, and the reviewer's own pre-emission original
   `.remedy-wt/f033-r28-block.md`, which is the reviewer's file and not this
   worker's scratch to delete.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a — save block to `.agent/authored/f033-r28.md` | done | `5541f4a5`; G1 one digest over five readings |
| C0b — mirror into `.agent/last_block.md` | done | `685cc0e7`; byte-equal |
| C1 — rewrite `.agent/plan.md` from PLAN28 | done | `7291698f`; G2 byte-equal, 42 lines |
| C2 — append RECORD28 to `.agent/live_review.md` | done | `24ea131f`; G3 reconstructs, G4 registers R-0750 and extends R-0736 with no id |
| C3 — append BUILTSTATE to `docs/roadmap/features/T5_F033.md` | done | `8738c5f1`; G5 ordered equality, 0 deleted lines, docs suite 295 passed |
| C4 — the closure artifacts | deviated | NOT A COMMIT; nothing committable. Integrity PASS, bundle complete on all 8 gates, zip READY_FOR_REVIEW. See deviation 1 |
| C5 — rewrite `.agent/handoff.md` | done | this file |
| G1 transport | done | REAL exit 0 |
| G2 the plan | done | REAL exit 0 |
| G3 the record append | done | REAL exit 0 |
| G4 the ledger | done | REAL exit 0 |
| G5 the built state | done | REAL exit 0, 295 passed |
| G6 integrity + evidence job | done | REAL exit 0, verdict `passed: true`, 0 gate documents absent |
| G7 the review zip | done | REAL exit 0, READY_FOR_REVIEW, head == C3 |
| G8 structure | done | REAL exit 0, max 302 insertions, path set equal both ways |

Open findings after this round: **258** (310 -> 311 registered distinct, 53
resolved distinct, unchanged).

## Next

The reviewer books the round-28 verdict, then authors the CLOSURE COMMIT round —
the second and last of the closure sequence. That round applies, verbatim, a
reviewer-authored STATUS line flipping `- [~] F033 — Hunk-level diff approval`
at line 86 of `docs/roadmap/STATUS.md` to `[x]`, carrying the six labelled facts
at the top of this file, together with the README capability sync in the SAME
commit (R-0154), the `.agent/candidates.md` handling if the closure gate raises
any, and the final `.agent/` state. Then the pull request — which is NOT merged
in this session; it merges at the next feature's start via the Open PR Gate,
which is the operator's manual-review window. Nothing in this round touched
STATUS.md, README.md or the self-use queue, so all three are exactly as the
closure commit expects to find them.
