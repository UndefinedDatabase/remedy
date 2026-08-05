# Handback — F075 R13 CLOSURE

## Range
Review of 8bc1305a..HEAD (4 commits, incl. this one).

## Commits
### b49e6bdb chore(f075): save the R13 closure block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +241/-235 | the block, own commit (R-0198); two transport defects repaired against the digests — see proofs |

### 634b0be8 chore(f075): persist the R12 gate verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f075-r13-{1..5}.md | +129 | the five reviewer texts, sha256-verified |
| .agent/live_review.md | +29 | r13-1 applied; LAST_REVIEWED_SHA = 8bc1305a |

### 36f3bc81 docs(f075): record the accepted Built State ← ACCEPTED HEAD
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F075.md | +53 | r13-2 byte-appended (precondition 4) |

### &lt;this commit&gt; the closure commit (Rule A4, last on the branch)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md · README.md | ±1 / ±2 | r13-3 with the four placeholders filled · r13-4 both edits, same commit (R-0154) |
| .agent/candidates.md | rewrite | r13-5 full replacement, 4 candidates |
| .agent/plan.md · context.md · handoff.md · last_block.md | rewrite | final F075-closed state · this handback · OUTCOME |

## External actions
- 4x `git push origin feature/f075-self-run-gauntlet`, one per commit — OK. NO force-push (R-0195).
- `bash scripts/make_review_zip.sh --evidence-dir <scratch>/remedy-job-evidence-f075-closure` — REVIEW_PACKAGE_CREATED=true.
- `gh pr create --base main` runs AFTER this commit (Rule A4 puts the STATUS edit last), so the number is reported in the session handback, not here — the F071 closure precedent. NOT merged (protocol §6). No other gh command.

## Verification
`pytest tests/cli/test_golden_path.py -q` → 42 passed, EXIT=0 (P1, P2, closure) · `pytest tests/docs/ -q` → 293 passed, EXIT=0 (P2, closure) · `remedy integrity check --json` → `passed: true`, every check pass · `git status --porcelain` empty at every phase boundary.
EVIDENCE JOB **b1b6eb7ed4962309** — `create_manual_completion_bundle(review_feature_id="f075")`, base 563b15b4d35b785563d9720fb762d393883d744d, head 36f3bc8150a9bdaae3c1e3a743c1621998c48691, 4 verification runs (272 / 42 / 293 / 74 = 681 passed), authority 76, verdict PASS_WITH_RISKS; built OUTSIDE the repo, NOT committed. Coordinator validation attempt 1 → `ok: False`, raw blocking_reasons: `"final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid"` and `"verification_tests.json runs[0] test_files is not sorted"`. Fixed AT THE CAUSE (test_files sorted at authoring), rejected dir deleted, rebuilt → attempt 2 `ok: True`, `blocking_reasons: []`.
REVIEW ZIP **remedy-review-20260805-144354-READY_FOR_REVIEW.zip** · SHA-256 `d63cda6b2b9e83bf993889d33fa716646f712f90eabc992a472d12390b8910d3` (recomputed independently with sha256sum — equal to the builder's report) · PACKAGE_STATUS=READY_FOR_REVIEW · REVIEW_SUBJECT_ALIGNMENT=PASS · EVIDENCE_AUTHORITATIVE=true · committed_review_subject 563b15b4…d744d → 36f3bc81…c48691 (the accepted HEAD) · 2064 members, 76 authoritative · `testzip` → no bad member · import smoke over the PACKAGED sources (extracted to tmp, removed after): PASS_CRITERIA len 9, GAUNTLET_ORDER_SET_VERSION 4, gauntlet_runner imports → PASS.

## Authored-text proofs
| text | sha256 vs BEGIN digest | applied, byte-identical |
|---|---|---|
| f075-r13-1 | 67b700f9…d1e0 EQUAL | TO block occurs 1x in live_review.md, tail-anchored |
| f075-r13-2 | 9c3e097e…3a72 EQUAL | occurs 1x in T1_F075.md, file ends with it, prior content intact as prefix |
| f075-r13-3 | b6ff64e8…f94b EQUAL | TO line occurs 1x in STATUS.md, ONE line of 347 chars, 4 placeholders filled |
| f075-r13-4 | 91123541…873d EQUAL | both TO lines occur 1x in README.md, both FROM lines gone |
| f075-r13-5 | 55af55f4…b030 EQUAL | `cmp` exit 0 vs .agent/candidates.md |

DECLARED, transport — two defects, both caught by the digests BEFORE anything was applied, neither guessed: (1) a duplicated instruction region (PHASE 4 tail through the end of PHASE 6) was injected between the first `BEGIN f075-r13-1` marker and the real payload — the complete second BEGIN/END pair hashes to 67b700f9, proving the first marker plus duplicate is corruption; (2) r13-3 arrived WRAPPED across three lines, the exact F071 lesson the block itself names — unwrapping to one line reproduced b6ff64e8. Both repairs are in the archived block (b49e6bdb).

## Deviations & assumptions
- The evidence-job rebuild after a coordinator rejection is protocol-ordered, not a deviation; raw reasons above. The evidence dir stays in session scratch and is NOT committed — the durable pointer is package + SHA-256 + job id in the STATUS line.
- Runtime actuals as authored: 13 rounds 2026-08-04..05, three live campaigns + seven `--only` re-proofs, tokens **not-measured** (the local provider reports no ledger usage).

## Next
The Open PR Gate at the next feature's start merges the closure PR; F079 (Context handoffs) begins in a fresh session and its FIRST reviewed round must empty .agent/candidates.md (4 entries).
