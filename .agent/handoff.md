# Handback — F051 R3 (CLOSURE, protocol v4) — CLOSED

## Range
`1a651fd..HEAD` · feature/f051-escalate-instead-of-block · 3 commits
(persist+Built State · evidence · closure). Base `894375e`.
PR **#165** updated, **NOT merged** — it merges at the next feature's start via
the Open PR Gate.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 guard | done | block f051-r3 recorded, OUTCOME pending → executed |
| 2 four authored texts | done | all four sha256 verified; r3-3 needed the documented rejoin |
| 3 commit A + gates | done | `54df8f7`; docs 292 exit 0, canary 42 exit 0 |
| 4 preconditions | done | integrity PASS (5/5), tree clean, `0 0` synced |
| 5 evidence job | done | `785d275a-2f78-4b44-bd29-f8764ff95bb8`, 426 passed |
| 6 READY zip | done | **attempt 1 BLOCKED_EVIDENCE, attempt 2 READY_FOR_REVIEW** — both recorded below |
| 7 evidence commit | done | `1d7ec52`, after the READY zip |
| 8 FINAL commit | done | this commit; STATUS + README + .agent only |
| 9 push + PR update | done | PR #165 body carries R3; not merged |
| 10 handback | done | this file + completion report |

## Authored-text verification — `sha256sum` output verbatim
    f27dce59a1c6ca8adce415e1ccdc671603473d5e4abfcfbeefd76e1175c789d1  .agent/authored/f051-r3-1.md
    5bcf6f7b9ec2552597912af5ce22ee15c7def5ebd64be5c7d74724883008c2a5  .agent/authored/f051-r3-2.md
    7e90d44b22e537ba6bc84c186e729ca0ab27037bb1567535b2048516a70511be  .agent/authored/f051-r3-3.md
    867258c9249e75d0450fa1fb23547a0e77e10e7c6049c670a327ef84c858d4a2  .agent/authored/f051-r3-4.md
**Transport fault (recoverable, documented):** `f051-r3-3` arrived hard-wrapped
across three lines (splits after "live review" and after "accepted HEAD").
Rejoining the fragments with a single space reproduced the authored bytes
exactly — hash verified BEFORE any use, template is ONE line, all four
placeholders intact. Same class as f050-r3-2 and r0154-r1-1. The other three
texts arrived clean and matched on first computation.
`cmp` live_review vs f051-r3-1 → **0**. Template re-verified to
`7e90d44b…0511be` immediately before substitution.

## Item 4 — preconditions (raw)
`python3 -m apps.cli.grouped integrity check --json` → **EXIT 0**,
`"fail_count": 0, "check_count": 5`: handler_import `handlers=312` · pass;
live_review_verdict `- R1: PASS (reviewer, 2026-07-30)…` · pass;
plan_consistency `unchecked=0, context_complete=False` · pass;
relevant_untracked `untracked=0, relevant=0` · pass; high_blockers_open
`no open blocker/high findings` · pass.
(`remedy` is not on PATH as a module — the console script is
`apps.cli.grouped:main` per pyproject; same command, module invocation.)
`git status --porcelain` → **empty**.
`git push` → `1a651fd..54df8f7`; `git rev-list --left-right --count @{u}...HEAD`
→ **`0	0`**.

## Item 5 — evidence job
**`785d275a-2f78-4b44-bd29-f8764ff95bb8`** via
`create_manual_completion_bundle(review_feature_id="f051", …)`, base
`894375e40f2d88c3d2cd2859073423faa2b17120` (full 40, verified in
`current_change_content_proof.json`) → head `54df8f7…`. Verdict
**PASS_WITH_RISKS**, authority 10 files, 15 commits, T001/T002/T003
operator-attested, **total_passed 426**.
Four REAL runs, executed now, all exit 0:

    vr-0001  pytest tests/orchestration/test_escalation.py -q      66 passed   0.5s
    vr-0002  pytest tests/cli/test_open_decisions_view.py -q       26 passed   0.3s
    vr-0003  pytest tests/cli/test_golden_path.py -q               42 passed  19.3s
    vr-0004  pytest tests/docs/ -q                                292 passed   0.4s

Every `output_hash` is 64-hex and equals `sha256(stdout_summary)` as stored
(checked all four → consistent): `stdout_summary` was pre-truncated to the
producer's own last-2000-char window and `output_hash` left EMPTY, so the two
cannot diverge (F252 lesson). `selected` == `len(node_ids)` for every run.
Gate matrix: final_verifier PASS_WITH_RISKS · fresh_evidence PASS ·
artifact_contract PASS · change_provenance PASS · runtime_integration PASS ·
commit_execution NEEDS_HUMAN_APPROVAL with `blocked_gates: []` — the same shape
as F050's and F252's accepted bundles.

## Item 6 — the zip: TWO attempts, both recorded
**Attempt 1 — `remedy-review-20260730-172126-BLOCKED_EVIDENCE.zip`**,
SHA-256 `c519ac2cb085d22f11f242dc51e78f561feee53b24e44700c9b0fc675a05d3b6`.
`PACKAGE_STATUS=BLOCKED_EVIDENCE`, `evidence_authoritative=false`; raw warning:
`WARNING: Evidence validation failed (is_valid_current_run=false).`
Cause, read out of the package's own `.review_zip_manifest.json`
(`current_evidence.validation.validation_errors`):

    verification_tests.json runs[0] node_ids count (0) != selected (66)
    verification_tests.json runs[1] node_ids count (0) != selected (26)
    verification_tests.json runs[2] node_ids count (0) != selected (42)
    verification_tests.json runs[3] test_file 'tests/docs/' is not a safe relative path
    verification_tests.json runs[3] node_ids count (0) != selected (292)
    verification_tests.json top-level test_file 'tests/docs/' is not a safe relative path

Both defects were in MY run records, not in the product: the packaging validator
requires `len(node_ids) == selected` and rejects a `test_files` entry that is not
a safe relative FILE path (a directory argument such as `tests/docs/` must be
expanded). These are two more producer pitfalls of the same family the block
named — worth adding to the protocol's step-1 pitfall list.
Fix (one focused attempt): the builder now runs `--collect-only` for each
command, records the real node ids, derives `test_files` from them, and refuses
to write a record where `len(node_ids) != selected`. Attempt-1 evidence dir and
zip were deleted before the rebuild so no stale artifact could be picked up.

**Attempt 2 — `remedy-review-20260730-172315-READY_FOR_REVIEW.zip`**
**SHA-256 `e85932c425acf204d8e9c24a030d4988aecbe4d3779dc5b4a57193f4f7c0648a`**
(script output; independent `sha256sum` agrees byte for byte).
`PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`,
`REVIEW_SUBJECT_ALIGNMENT=PASS`, 1607 members, authoritative 10, publication
SUPPORTED, `is_valid_current_run: true`, `validation_errors: []`.
Manifest `committed_review_subject`: base
`894375e40f2d88c3d2cd2859073423faa2b17120` → head
`54df8f7a1adea2f3d140efef22e2e6f991aea6ff`, `base_is_ancestor: true`,
commit_count 15, file_count 23 — spans base..HEAD with head = commit A, as
required. Import check `ZipFile.testzip()` → **None**.
Built from a clean tree BEFORE the evidence commit and before the final commit.
**accepted HEAD = `54df8f7a1adea2f3d140efef22e2e6f991aea6ff`**, taken from the
manifest's `committed_review_subject.head_commit`.

## Item 8 — applied text + proofs
Applied STATUS line, verbatim:

    - [x] F051 — Escalate instead of block (unattended) (T001–T003 complete; accepted 2026-07-30 · live review PASS — ACCEPTED · Evidence job 785d275a-2f78-4b44-bd29-f8764ff95bb8 · package remedy-review-20260730-172315-READY_FOR_REVIEW.zip · SHA-256 e85932c425acf204d8e9c24a030d4988aecbe4d3779dc5b4a57193f4f7c0648a · accepted HEAD 54df8f7a1adea2f3d140efef22e2e6f991aea6ff)

Provenance per substituted value:
| Placeholder | Value | Source |
|---|---|---|
| `<JOB_ID>` | 785d275a-2f78-4b44-bd29-f8764ff95bb8 | producer output (item 5) |
| `<ZIP_FILENAME>` | remedy-review-20260730-172315-READY_FOR_REVIEW.zip | `make_review_zip.sh` JSON `final_path` |
| `<ZIP_SHA256>` | e85932c4…0648a | same JSON `final_sha256`; independent `sha256sum` agrees |
| `<HEAD_SHA>` | 54df8f7a1adea2f3d140efef22e2e6f991aea6ff | manifest `committed_review_subject.head_commit` |

Each placeholder occurred exactly once before substitution. Nothing else in the
line was touched.
- STATUS: new line `grep -cF` = **1**, old `- [~] F051 …` = **0**,
  `grep -F <line> STATUS.md | cmp - <substituted template>` → exit **0**.
- README, all three ordered edits, each FROM = 1 before / 0 after, each TO = 1
  after: `26 of 252 … Next: F051 (…)` → `27 of 252 … Next: F052 (Self-healing
  test rounds).` · `| 1 | Self-Build Bootstrap | 10 | 22 |` → `| 11 |` ·
  `F050 DAG scheduling.` → `F050 DAG scheduling, F051 escalate instead of block.`
- Post-commit gates: `pytest tests/docs/ -q` → exit **0**, `292 passed`;
  canary `tests/cli/test_golden_path.py -q` → exit **0**, `42 passed`.
  `grep -c '^- \[x\]' docs/roadmap/STATUS.md` → **27**.

## Commits
| Commit | Files | Note |
|---|---|---|
| `54df8f7` chore persist | `.agent/authored/f051-r3-{1..4}.md`, `.agent/{live_review,last_block}.md`, `docs/roadmap/features/T1_F051.md` | R2 verdict persisted; Built State current (`grep -c "integration gate PASS"` → 1). **The accepted HEAD.** |
| `1d7ec52` chore evidence | `.data/evidence_exports/785d275a-…/` (73 files) | the closure bundle; `git add -f` past `.gitignore .data/`; committed only AFTER the READY zip existed (F147 lesson) |
| this commit | `docs/roadmap/STATUS.md`, `README.md`, `.agent/{handoff,last_block}.md` | STATUS `[x]` + README sync in ONE commit (R-0154 / protocol step 5), plus final state |

## Deviations
1. **The zip took two attempts.** Attempt 1 was BLOCKED_EVIDENCE for two
   defects in my own verification-run records (empty `node_ids`, a directory in
   `test_files`). Both raw outputs are recorded above; the fix was one focused
   correction of the record builder, not of any product code, and attempt 2 is
   READY_FOR_REVIEW. No product file was changed to make packaging pass.
2. Nothing else. Every other item executed as written.

## Runtime actuals (observed)
3 rounds on 2026-07-30 — R1 (LARGE, T001–T003), R2 (R-0157 + Built State +
integration gate), R3 (closure). 17 commits on the branch. Models: as
configured; **tokens/cost not-measured** (this session's ledger has no actuals
for the worker's own runs).

## Open findings
2 documented risks, both planning-routed, both accepted for closure:
**R-0155** (process, Low — refined this round: the base worktree lacks the ROOT
`node_modules` and `apps/ui/dist`) and **R-0156** (process, Medium — the
README/STATUS accepted-count cross-check is unenforced in tests/docs).
**R-0157** is Resolved. Next free ID: **R-0158**.

## Next
F051 is closed. PR #165 merges at the next feature's start via the Open PR Gate
— the gap is the operator's manual-review window. Next per Rule A5: **F052 —
Self-healing test rounds**, fresh window.
