# Handoff — F071 Mission dossier · R4 (CLOSURE)

## Range
Review of 1121142a..\<HEAD\> · 4 new commits · ACCEPTED_HEAD = acb02acd.

## Commits
### a0eeff86 persist the R3 PASS + gate verdict, register R-0176/R-0177
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f071-r4-1..5.md | +181 | 5 reviewer texts, sha256-verified |
| .agent/live_review.md | +143/-75 | authored full replacement |

### b8b9c043 docs(agents): gate run logs live outside the repo (R-0176)
| Path | +/- | Reason |
|---|---|---|
| docs/agents/integration_gate.md | +9/-1 | authored FROM→TO |
| .agent/live_review.md | +1 | Done: R-0176 |

### acb02acd docs(f071): record the accepted Built State ← ACCEPTED_HEAD
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F071.md | +58 | f071-r4-3 appended verbatim at EOF |

### \<closure sha\> chore(f071): close F071 — STATUS [x] + README sync
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | f071-r4-4, 4 placeholders substituted |
| README.md | +3/-3 | f071-r4-5 pairs 1-3 (pair 3 = R-0177) |
| .agent/live_review · plan · context · handoff.md | rewritten | Done: R-0177 + final state (R-0149 self-ref) |

## Item status
| Item | Status | Reason |
|---|---|---|
| R-0176 | done | b8b9c043 |
| R-0177 | done | closure commit — README tier-12 row Total 9 |
| Built State | done | acb02acd |
| Evidence job | done | b3b98e3ee1d10668 |
| Review zip | done | READY_FOR_REVIEW, subject 097e4959..acb02acd |
| STATUS [x] + README | done | closure commit, exact path set |
| PR | done | created right after this commit, open, NOT merged |

## External actions
- `make_review_zip.sh --evidence-dir <scratch>/remedy-job-evidence-f071` -> exit 0.
- `git push` x2 -> exit 0. `gh pr create` runs AFTER this commit (Rule A4: the STATUS edit is the last commit), so the number is reported in the session handback, not here. NOT merged — the next feature's Open PR Gate merges it.

## Verification
```
pytest tests/docs/ -q  293 EXIT=0 | canary 42 EXIT=0 | (re-run after closure commit: same)
remedy integrity check --json  passed=true, fail_count=0, 5/5
git status --porcelain  empty before evidence AND at handback
```
Evidence job `b3b98e3ee1d10668` — feature-scoped, zero provider calls, 4 runs /
544 passed / 0 failed (dossier 103 · loop 106 · canary 42 · docs 293). Real
`--collect-only` node ids, `len(node_ids)==selected`, 0 skipped; test_files are
FILES (tests/docs/ expanded to 293); run_id `vr-0001..0004`; full-length
base_commit; output_hash == sha256(stdout_summary) verified all 4. READY gate
`ok:True`, blocking `[]`.
Package `remedy-review-20260803-190339-READY_FOR_REVIEW.zip`
SHA-256 `aa117e26a55b0ab1b1941d881a4ed510967c2d1669be021abda30ab0f6e9e99e`,
built from the clean tree at acb02acd; committed_review_subject
097e4959..acb02acd, 25 commits, base_is_ancestor true; 1881 members. Evidence
dir stayed in session scratch — NOT committed.

## Authored-text proofs
All five sha256 match their BEGIN digests (`5cce9c84` `90f443cc` `1358d51e`
`c90535f5` `2e199533`). r4-1 `cmp` vs live_review.md -> 0. r4-2 FROM 1→0,
TO 0→1. r4-3 `doc.endswith(authored)` True, occurrences 1. r4-4 FROM 1→0,
TO 0→1, STATUS diff exactly 1 insertion/1 deletion — **and re-substituting
JOB_ID/ZIP_FILENAME/ZIP_SHA256/ACCEPTED_HEAD back reproduces the authored
template byte for byte (True)**. r4-5 three pairs, each FROM 1→0, TO 0→1.

## Deviations & assumptions
1. **f071-r4-4 digest mismatched on transcription — STOPPED, applied nothing.**
   Got `e93dd811ccbff7772b8ba9d153ba0d26d9229d544f46f2f4d7477d5bc588f0d0`,
   expected `c90535f5…`. Cause: the STATUS TO line is ONE line, displayed
   wrapped; I had transcribed the wrap as a newline. Resolved by HASHING
   candidates only — joining the two display lines with one space reproduces
   `c90535f5…`. Applied only after the digest matched.
2. Final-verifier verdict `PASS_WITH_RISKS`, not PASS — standard zero-provider
   attested outcome (`token_measurement_confidence: low`,
   `human_final_reviewer_required: true`); `unresolved_findings []`,
   `missing_evidence []`, 544 passed. The STATUS line records the LIVE REVIEW
   verdict (PASS), which is what the template asks for.
3. `.agent/context.md` refreshed in the closure commit with plan/handoff — all
   inside the allowed `.agent/` path set.
4. `.agent/candidates.md` left empty: this closure raised no candidates.
5. Cap: the round order grants LARGE cap rules — 95 lines (≤160), ~1.2k tokens
   (≤1600), both met, no section dropped. The base ≤60/≤800 cap would not fit
   4 mandatory per-commit tables plus the protocol's mandatory grep proofs.
6. The PR number is absent from this file by construction: Rule A4 puts the
   STATUS edit last, so the PR is created after this commit is written.

## Next
F071 closed on disk; PR open and unmerged by design. Rule A5 selects F075 in a
fresh session; its Open PR Gate merges this PR.
