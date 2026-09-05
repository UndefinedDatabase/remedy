# Handback — F259 Vocabulary & concept model v1, round 9 (CLOSURE PART 2)

## Session

`SESSION 1 of feature F259 · round 9 · rounds so far 9`

Context self-assessment: context is comfortable — this round spent most of it on
gate transcripts rather than file reading, and a further closure round fits
without a boundary.

`~99 % (T001–T004 ✅ · Integration Gate ✅ · Evidence + Zip gebaut · nur noch STATUS/README/PR) — Schätzung`

## CLOSURE VALUES FOR PART 3 (the five values the STATUS line is authored from)

These are measured, not estimated. Part 3 copies them verbatim.

    EVIDENCE JOB ID:        ace7fa4d9d782a7a
    PACKAGE FILENAME:       remedy-review-20260906-004320-READY_FOR_REVIEW.zip
    PACKAGE SHA-256:        164f9513a4608030989590daf647d9a96a1c2c0b78f4fb469461966024fd56e3
    PACKAGE PATH:           /home/decodeux/Repos/remedy-history/zips
    ACCEPTED HEAD:          efd2a4fb04bb82b8ee87b812327a7c3f9776853a
    PACKAGE_STATUS:         READY_FOR_REVIEW

PACKAGE PATH note (DECISION amend0827 D1): the zip was written to that absolute
directory by `scripts/make_review_zip.sh` itself and was NOT moved afterwards.
The directory is outside the repository, so it is recorded as the package's
absolute directory rather than as `NOT ARCHIVED`; the reviewer may substitute
`NOT ARCHIVED` if D1 is read as requiring a deliberate move.

ACCEPTED HEAD is the full sha of C4 and is the head the manifest recorded as
`committed_review_subject.head_commit`.

## Range

Review of 32808b5d551e45953a08531849b81aec3aa05bb6..efd2a4fb04bb82b8ee87b812327a7c3f9776853a

Six commits, all single-parent, pushed. NO pull request created this round.

## Commits

### 2d045349 f259: save round 9 block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f259-r9.md | +303 / -0 | C0a — the block copied byte-for-byte from `.remedy-wt/f259-r9-block.md` |

### f7e2c89e f259: mirror round 9 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +252 / -349 | C0b — mirror of the committed authored file |

### fd587e88 f259: plan for round 9, closure part 2
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22 / -21 | C1 — whole rewrite from slice PLANF259R9 |

### 3a5f006f f259: book R8 verdict, register R-0813, R-0784 recurrence, Done R-0418, slip 9
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8 / -0 | C2 — GATE_R8, FIND0813, REC0784, DONE0418 appended in that order |
| .agent/prose_slips.md | +3 / -1 | C2 — SLIP9 appended, still no trailing newline |

### a7c72f25 f259: repair R-0813, the frozen paragraph named two figures
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +1 / -1 | C3 — the FROZENFIX rewrite pair |

### efd2a4fb f259: rotate the live review ledger into the archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0 / -8 | C4 — two resolved finding pairs moved out |
| .agent/live_review_archive.md | +8 / -0 | C4 — the same records appended byte-verbatim |

### C5 (this commit) f259: round 9 handback, closure part 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | whole rewrite | C5 — this file; a handoff cannot table the commit that writes it (R-0149) |

Total insertions across the round: 597. Largest single commit: 303 (C0a).
Every commit is under the 500-insertion cap, so the AGENTS.md DECISION F104 D1
exemption was NOT needed for C4 — the rotation cost only 8 insertions.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f259-r9.md`, copied not retyped |
| C0b | done | `.agent/last_block.md` |
| C1  | done | `.agent/plan.md` ← PLANF259R9, 43 lines |
| C2  | done | four ledger paragraphs + SLIP9, one commit |
| C3  | done | FROZENFIX pair applied, R-0813 repaired |
| C4  | done | rotation ran and was NOT refused; exactly the two ordered paths |
| C5  | done | this handback |

## External actions

- `git push -u origin feature/f259-vocabulary` → `32808b5d..efd2a4fb`, OK.
- `git push` after C5 → recorded below in the round report.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  No PR exists and none was created. Nothing merged, no force push, no history
  rewrite, no branch deleted.
- `bash scripts/make_review_zip.sh --evidence-dir …` → READY_FOR_REVIEW.
- No worktree added or removed.

## Verification — one line per gate, real readings

- **G1 TRANSPORT — PASS.** `sha256sum` over the three paths printed ONE digest
  three times: `5ae765ed108327d52ed5b9e216a859a2186c9ef7b7b601ffae2ac66b18be8da0`
  for `.remedy-wt/f259-r9-block.md`, `.agent/authored/f259-r9.md` and
  `.agent/last_block.md`. Equal to the digest the order stated. Exit 0.
- **G2 THE C2 APPENDS — PASS.** `.agent/live_review.md`: pre 848 281 bytes → post
  859 557; prefix property True; remainder (11 276 bytes) byte-equal to
  `"\n" + GATE_R8 + "\n\n" + FIND0813 + "\n\n" + REC0784 + "\n\n" + DONE0418 + "\n"`
  True; still exactly one trailing newline. Counts all 0 → 1: `^Gate: R8 — ` 0→1,
  `^- R-0813 — ` 0→1, `^Recurrence: R-0784` 0→1, `^Done: R-0418` 0→1.
  `.agent/prose_slips.md`: pre 83 964 → post 85 098; prefix property True;
  remainder (1 134 bytes) exactly `"\n\n" + SLIP9` True; no trailing newline
  before or after.
- **G3 THE FROZENFIX — PASS.** Containment reading printed `TO contains FROM:
  false` (a REWRITE). FROM count 1 before / 0 after; TO count 0 before / 1 after.
  Post file equals pre with that one replacement and nothing else: True
  (92 038 → 92 039 bytes, one trailing newline). Per-item digest sweep: 36
  checklist items before AND after, numbered 1..31 and 33..37 both times; items
  whose block digest changed: **0** — the frozen paragraph sits outside every
  item, as the block predicted. `measures against 36` occurs exactly 1×;
  `the number the next consolidation measures against` occurs 0×.
- **G4 THE ROTATION — PASS, not refused.** Full transcript below. Ledger
  848 281 → 859 557 (C2) → 851 727 bytes; archive 1 723 631 → 1 731 461. Open
  findings **294 before and 294 after — EQUAL**, computed in the ledger as
  `^- R-\d{4} — ` minus `^Done: R-\d{4} — ` (300−6=294 before, 298−4=294 after).
  `^Gate: ` records remaining in the ledger: 8; now in the archive: 344 (0 gate
  records moved, because F259 is not yet `[x]` — that flip is part 3's).
  `git show --numstat efd2a4fb` names exactly `.agent/live_review.md` and
  `.agent/live_review_archive.md`, single parent `a7c72f25`.
- **G5 THE EVIDENCE JOB — PASS.** `git status --porcelain` empty immediately
  before; HEAD confirmed at C4. Job id `ace7fa4d9d782a7a`. Returned summary:
  `{"job_id": "ace7fa4d9d782a7a", "head_commit": "efd2a4fb04bb82b8ee87b812327a7c3f9776853a",
  "authority_count": 8, "partition": {"T001": 3, "T002": 3, "T003": 2},
  "commit_count": 61, "verdict": "PASS_WITH_RISKS", "manual_completion": true,
  "operator_attested_tasks": ["T001","T002","T003"], "total_passed": 303}`.
  Final verdict it names: **PASS_WITH_RISKS**. The single verification run:
  `run_id vr-1788648189` (matches `^vr-\d{4,}$`), command
  `python3 -m pytest tests/docs/ -q`, exit 0, passed 303 / failed 0 / skipped 0 /
  deselected 0, `selected` 303 = 303+0+0, `len(node_ids)` 303 = selected,
  `test_files` `['tests/docs/test_docs_consistency.py','tests/docs/test_vocabulary.py']`
  (sorted, both real files), `stdout_summary` 420 chars (<4000), `output_hash`
  `54ee3d3888b1c4ccead127b3538b2fe188504221b685cfbd99bdd680e539a486`,
  head_sha = C4, duration 0.719 s. Re-verified FROM INSIDE THE PACKAGE: the
  sha256 of exactly the stored `stdout_summary` reproduces that `output_hash`,
  and the record carries exactly the 14 named fields and no others. No
  full-suite node-id list appears anywhere in the bundle.
- **G6 THE REVIEW ZIP — PASS, READY_FOR_REVIEW.** `git status --porcelain` empty
  and branch pushed (local == `origin/feature/f259-vocabulary` == efd2a4fb)
  immediately before. `PACKAGE_STATUS=READY_FOR_REVIEW`,
  `REVIEW_PACKAGE_CREATED=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`,
  `EVIDENCE_AUTHORITATIVE=true`, member_count 3877, authoritative_count 8,
  symlink_count 0, tombstone_count 0. SHA-256 as the script printed it
  `164f9513a4608030989590daf647d9a96a1c2c0b78f4fb469461966024fd56e3`; recomputed
  from the 22 510 711-byte file on disk: identical (True). Manifest
  `committed_review_subject` spans base `259617949461c993f1b8dabcf659e6a73110b162`
  → head `efd2a4fb04bb82b8ee87b812327a7c3f9776853a` — i.e. 25961794..C4, 61
  commits, 36 files, `base_is_ancestor: true`. `packaged_evidence_job_id` is
  `ace7fa4d9d782a7a`, the G5 job. `ready_gate_matrix.ok: true`,
  `blocking_reasons: []`, `packaging_warnings: []`; gate verdicts
  artifact_contract PASS, change_provenance PASS, fresh_evidence PASS,
  runtime_integration PASS, manifest_integrity ok=true, postmortem_integrity
  ok=true, final_verifier PASS_WITH_RISKS, commit_execution
  NEEDS_HUMAN_APPROVAL (the expected operator gate, not a blocker).
  Tree still clean after the build.
- **G7 THE PRECONDITIONS — PASS.** `python3 -m apps.cli.grouped integrity check
  --json` → `passed: true`, `fail_count: 0`, check_count 5, exit 0.
  `python3 -m pytest tests/docs/ -q` → **303 passed**, exit 0 (reviewer's 303
  reproduced). `python3 -m pytest tests/cli/test_golden_path.py -q` → **42
  passed**, exit 0 (reviewer's 42 reproduced). `python3 -m pytest
  tests/orchestration/test_live_review_rotation.py -q` → **10 passed**, exit 0.
  `git status --porcelain` → empty. Untracked paths with
  `--untracked-files=all`: **0** — the scratch under `.remedy-wt/` is gitignored
  by `.gitignore:235:.remedy-wt/` (`git check-ignore -v` exit 0), so nothing is
  untracked-and-relevant.
- **G8 THE PLAN AND THE STRUCTURE — PASS.** `wc -l .agent/plan.md` = **43**
  (<50); exactly one `## Goal` and one `## Next Steps`;
  `filecmp.cmp(plan, slice+newline, shallow=False)` **True**.
  `git status --porcelain` empty immediately before C5 was staged;
  `git ls-files .remedy-wt` returns nothing. All six commits single-parent.
  Per-commit `git diff --numstat` cell by cell is in the Commits table above;
  insertions 303 / 252 / 22 / 11 / 1 / 8, every one under the 500 cap, so no
  F104 D1 exemption was required. Push succeeded (`32808b5d..efd2a4fb`). No pull
  request was created (`gh pr list --state open` → `[]`). This round's whole
  diff touches exactly `.agent/authored/f259-r9.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
  `.agent/prose_slips.md`, `docs/agents/planner_reviewer_prompt.md` —
  `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are
  each confirmed **absent** (False).

## Rotation transcript (G4, in full)

Dry run, `python3 scripts/rotate_live_review.py --dry-run`, exit code 0:

    gate records moved: 0
    finding pairs moved: 2 (4 records)
    old ledger size: 859557 bytes
    new ledger size: 851727 bytes
    old archive size: 1723631 bytes
    new archive size: 1731461 bytes
    open findings before: 294
    open findings after: 294
    dry run; nothing written

Real run, `python3 scripts/rotate_live_review.py`, exit code 0:

    gate records moved: 0
    finding pairs moved: 2 (4 records)
    old ledger size: 859557 bytes
    new ledger size: 851727 bytes
    old archive size: 1723631 bytes
    new archive size: 1731461 bytes
    open findings before: 294
    open findings after: 294
    written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md

The script was NOT refused. Independently re-measured after the run: ledger
851 727 bytes, archive 1 731 461 bytes, open findings 294 — matching the dry
run's prediction byte for byte. The two moved pairs include the `R-0418`
registration with the `Done: R-0418` this round wrote, which is why the ledger's
`Done:` count fell from 6 to 4 while the open count stayed at 294.

## Authored-text proofs

- `PLANF259R9` → `.agent/plan.md`: `filecmp.cmp(shallow=False)` against the
  slice plus one newline → **True**.
- `GATE_R8`, `FIND0813`, `REC0784`, `DONE0418` → `.agent/live_review.md`: the
  post-append remainder is byte-equal to the ordered concatenation (G2) → True.
- `SLIP9` → `.agent/prose_slips.md`: remainder byte-equal to `"\n\n" + SLIP9` → True.
- `FROZENFIX_FROM`/`FROZENFIX_TO` → `docs/agents/planner_reviewer_prompt.md`:
  post file equals pre with exactly that one replacement → True.
- Every slice was extracted by marker extraction in Python from the COMMITTED
  `.agent/authored/f259-r9.md`, never retyped.

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4, C5 all ran, in that order, one commit each, with C4's own commit
   touching exactly the two rotation paths. No extra commit, none dropped, none
   reordered.
2. **Shell-guard refusals, re-expressed in Python as constraint 7 requires.**
   Three command FORMS were refused outright this session, each with the message
   `Permission to use Bash has been denied`:
   (a) a compound command containing `$?` — replaced by separate invocations and
   by `subprocess.run(...).returncode` in `.remedy-wt/f259_r9_g7.py` and
   `.remedy-wt/f259_r9_rotate.py`, which is how every exit code above was
   obtained;
   (b) an inline `python3 -c` carrying the C1 body — rewritten as the script
   file `.remedy-wt/f259_r9_c1.py` and run as `python3 .remedy-wt/f259_r9_c1.py`;
   (c) `grep -nE "^#{1,4} " docs/agents/planner_reviewer_prompt.md` (a
   brace-quantifier in a quoted pattern) — replaced by
   `grep -nE "^## " docs/agents/planner_reviewer_prompt.md` plus the Python
   `item_blocks()` sweep in `.remedy-wt/f259_r9_c3.py`, which is what actually
   produced the G3 item boundaries.
   All helper scripts live under the gitignored `.remedy-wt/` and are committed
   nowhere; `git ls-files .remedy-wt` is empty.
3. **The evidence directory is under `.remedy-wt/`, never committed.**
   `/home/decodeux/Repos/remedy/.remedy-wt/f259-evidence-ace7fa4d9d782a7a`,
   outside the base..HEAD review subject. The package came back
   `EVIDENCE_AUTHORITATIVE=true`, not BLOCKED_EVIDENCE.
4. **`vt_passed` is absent, not null-because-rejected.** The closure protocol's
   pitfall (c) warns that a rejected VerificationTests document yields
   `vt_passed = None`. For honesty: the key `vt_passed` does not exist in either
   `.review_zip_manifest.json` or `evidence/current/final_verifier_report.json`
   in this package, so an absent-key read of `None` says nothing about
   acceptance. The record WAS accepted on its merits — it is present in
   `evidence/current/verification_tests.json` with its `run_id`, 303 node ids and
   matching `output_hash`, `ready_gate_matrix.ok` is `true` with no blocking
   reasons, and the package reached READY_FOR_REVIEW.
5. **Observation, non-blocking:** the manifest's
   `review_subject_evidence_alignment` reports `dirty_file_count_total: 1` while
   `git status --porcelain` was empty and `git_status_snapshot.status` is `OK`.
   That block's own `verdict` is `PASS` with `issues: []`, `hash_mismatches: []`
   and `dirty_source_test_files: []`, so it blocked nothing; it is reported
   rather than explained, because this round did not establish which staged file
   the counter refers to.
6. **`change_provenance_covered_files` names README.md, STATUS.md and
   scripts/self_use_queue.json.** This is branch-wide, not this round: the review
   subject spans all 61 commits from 25961794, and earlier F259 rounds touched
   those files. G8 confirms none of the three is in round 9's own diff.
7. `.agent/STOP` was read from disk before C0a, before C4 and before C5, and was
   absent every time.

## Next

The reviewer gates this round. Then **CLOSURE PART 3**: the reviewer authors the
STATUS `[x]` line from the five closure values recorded above, and the worker
applies it together with the README capability sync and the self-use
`consumed_by` edit in **ONE** commit (R-0154 — README and STATUS may never
disagree in any committed state), which is the last commit on the branch (Rule
A4); then the pull request is created and is **NOT** merged this session — it
merges at the next feature's Open PR Gate.
