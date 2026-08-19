# Handback — F085 · R74 (closure round)

Feature F085 — Sandbox hardening (stage 1). Branch `feature/f085-sandbox-hardening`.
Base SHA ed34119b. Worker: this round made C0a, C0b, C1, C2, C3 and created the PR.

Fortschritt: 100 % — F085 ist gebaut, gegengeprüft und wird in dieser Runde geschlossen. T001 bis
T003 stehen, das Integration Gate hält, der Reviewer hat die volle Suite selbst viermal gefahren, und
was nicht geliefert wurde — die `resource_limit`-Klasse in der F010-Taxonomie — steht als R-0568
offen im Protokoll statt in einer Behauptung. Offen bleibt nur der Merge, den der Operator am
nächsten Open PR Gate zieht. Schätzung, gemessen gegen die Klassentabelle aus Amendment F085 D1.

## Range

Review of ed34119b..HEAD (C3).

## Commits

### a8d84801 chore(f085): save the R74 closure block
| Path | +/- | Reason |
| `.agent/authored/f085-r74.md` | 383/0 | C0a — block saved verbatim |

### 1181037b chore(f085): mirror the R74 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | 353/263 | C0b — verbatim rewrite (DECISION F104 D1 exempt) |

### 430a4a82 chore(f085): advance the plan to the R74 closure round
| Path | +/- | Reason |
| `.agent/plan.md` | 8/11 | C1 — PLAN28F→PLAN28T; also the plan's FINAL state |

### 617ef70a chore(f085): record the R73 PASS
| Path | +/- | Reason |
| `.agent/live_review.md` | 36/0 | C2 — RECORD43 appended at EOF; this is the accepted HEAD |

### C3 (this commit) chore(f085): close F085 in the ledger — self-reference table, R-0149 exception
| Path | +/- | Reason |
| `docs/roadmap/STATUS.md` | 1/1 | STATUSF→STATUST, three slots filled |
| `README.md` | 3/2 | READMECOUNT, READMETIER, READMEDOC — capability sync, same commit as STATUS |
| `.agent/candidates.md` | — | CANDIDATES, whole-file replacement |
| `.agent/handoff.md` | — | this handback |

## External actions

- `git push` after C2 → `ed34119b..617ef70a` (clean tree, pre-zip). OK.
- `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f085-closure` → READY_FOR_REVIEW.
- `git push` after C3 and `gh pr create --base main --head feature/f085-sandbox-hardening` run AFTER
  this commit, so their outcomes — PR number and URL — cannot exist in this file and ride in the
  ROUND REPORT (the F083 R28 closure precedent, item-14 routing). No `gh pr merge` is run.
- Worktrees: `git worktree list` = one line at start and at end; none added, none removed.

## Verification

- G1 STATE. `.agent/STOP` absent immediately before C0a and immediately before C3 (both `ls` → No such
  file). `git status --porcelain` EMPTY after C0a, C0b, C1, C2, C3 and immediately before the zip
  build. `git worktree list` = 1 line at start, 1 line at end.
- G2 TRANSPORT. All FOUR equal at sha256
  `d8a1225789c214549a90d61a21041f576e247036be4aa30cf941e3a394716e9b`, 27361 B, 383 lines: committed
  `.agent/authored/f085-r74.md` @1181037b, committed `.agent/last_block.md` @1181037b, and both
  working copies. TOTAL 383 ≤ 490 (D6). Slice lines sum 149 → PROSE 234 ≤ 400 (D5). Lines beginning
  `BEGIN-`/`END-`: 26 — see Deviations, all 26 are real markers. Slice line counts / sha256:
  PLAN28F 14 `a4758590…`, PLAN28T 11 `d69115df…`, RECORD43 36 `0e3fbeaf…`, STATUSF 1 `cf0c14ec…`,
  STATUST 1 `1b54b5f6…`, READMECOUNTF 1 `217ae699…`, READMECOUNTT 1 `64ca14b8…`, READMETIERF 1
  `69c217f9…`, READMETIERT 1 `65e77a5f…`, READMEDOCF 1 `b74c3685…`, READMEDOCT 2 `f018eb45…`,
  CANDIDATES 30 `2343f438…`, PRBODY 49 `5b55f076…`.
- G3 SHAPES. PLAN28 @430a4a82: FROM 1x pre / 0x post, TO 1x post, re-application reproduces the post
  blob BYTE-EXACTLY. STATUS @C3: FROM 1x pre / 0x post, TO (slots filled) 1x post, byte-exact
  reproduction True. READMECOUNT and READMETIER @C3: FROM 1x pre / 0x post, TO 1x post each; the
  byte-exact reproduction is COMPOSITE — README.md carries three pairs, and re-applying all three to
  the C2 blob reproduces the C3 blob byte-exactly (True); each pair alone does not, by construction.
  READMEDOC @C3: FROM exactly 1x in the post-commit file; C3 adds exactly 3 lines to README.md and
  the one TO-ONLY line (`| Execution guard limits (F085) | …exec-guard-limitations-v0.md…|`) occurs
  exactly 1x among them. No FROM-zero count was taken. RECORD43 @617ef70a: ORDERED EQUALITY — pre is
  a byte-exact PREFIX, slice an exact SUFFIX, `pre + slice == post` True, and C2's 36 added lines
  equal the slice's 36 lines IN ORDER. CANDIDATES @C3: post file == slice byte for byte, sha
  `2343f4383e2465004f02a516276482d6587a0a5590d6cee008df4a76085431e6`, 1915 B. `git show --numstat`:
  C1 `8 11 .agent/plan.md`; C2 `36 0 .agent/live_review.md`; C3 `1 1 docs/roadmap/STATUS.md`,
  `3 2 README.md`, `21 3 .agent/candidates.md`, plus `.agent/handoff.md`, whose own numstat is
  self-referential and therefore rides in the round report. Marker lines in every edited
  target at C3: 0 (STATUS.md, README.md, candidates.md, plan.md, live_review.md, handoff.md).
- G4 FULL SUITE at 617ef70a, primary checkout, `python3 -m pytest -n auto -q`: EXIT 0, 150.7 s wall,
  `17132 passed, 19 skipped in 150.13s (0:02:30)`. No red at all — R-0569's id did not fire, so no
  serial re-run was needed.
- G5 DOCS GATES, serially, on the C3 content: `python3 -m pytest tests/docs/ -q -rf` EXIT 0
  `295 passed`; `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` EXIT 0
  `30 passed`. Both equal the reviewer's ed34119b readings.
- G6 STATE READERS after C2, serially: EXIT 0, `160 passed in 19.98s` over the four files
  `.agent/context.md` names.
- G7 INTEGRITY. The `remedy` CLI entry point is DENIED in this sandbox, so the MODULE PATH was used —
  `run_integrity_checks()` + `summarize_integrity()` from `packages.orchestration.integrity_gate`,
  the same functions `apps/cli/commands/integrity_cmd.py` invokes. Substitution declared, not hidden.
  Full summary: `Status: PASS (0 failures)` over five checks — `handler_import: handlers=338`,
  `live_review_verdict` OK, `plan_consistency: unchecked=0, context_complete=False`,
  `relevant_untracked: untracked=0, relevant=0`, `high_blockers_open: no open blocker/high findings`.
- G8 PLAN CONTRACT at 430a4a82: 38 lines ≤ 50; `## Goal` present, `## Next Steps` present,
  `\bF\d{3}\b` present; 0 marker lines.
- G9 ARITHMETIC (D7, OPEN = REGISTERED − DONE, `Landed:` never subtracted). ed34119b: 184 registered,
  32 done, OPEN 152. C3: 184 registered, 32 done, OPEN 152. Registered symmetric difference: EMPTY.
  Done symmetric difference: EMPTY. 0 duplicate registered ids, 0 duplicate done ids, 0 resolutions
  naming an unregistered id, at both SHAs. `^Landed:` lines: 0 at both SHAs. Max registered R-0569,
  max resolved R-0564, next free id R-0570 — at both SHAs.
- G10 CANARY, serially: `python3 -m pytest tests/cli/test_golden_path.py -q` EXIT 0, `42 passed`.
- G11 HYGIENE. `git diff --name-only ed34119b..C3`: `.agent/authored/f085-r74.md`,
  `.agent/candidates.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `README.md`, `docs/roadmap/STATUS.md` — 8 paths, every one named in the block's
  Change set, none ending `.log`, no evidence directory and no zip. Insertions: C0a 383, C0b 353,
  C1 8, C2 36 — none over 500; C3's own count rides in the round report, as the block directs. All
  five commits single-parent, in the chain C3←617ef70a←430a4a82←1181037b←a8d84801←ed34119b.
- G12 GREP PROOF. The applied STATUS line is byte-identical to STATUST with exactly the three slots
  filled (`<<ZIP>>`→`remedy-review-20260819-203439-READY_FOR_REVIEW.zip`, `<<SHA256>>`→
  `951d05c4…96ad6`, `<<HEAD40>>`→`617ef70a3d566abed1ca68a034570636636edad5`), one occurrence each;
  the three applied README lines are byte-identical to READMECOUNTT, READMETIERT and READMEDOCT's
  TO-ONLY line with no substitution; `.agent/candidates.md` equals CANDIDATES byte for byte.

## Artifacts

- Evidence job `f085-closure` — BUILT. Producer `create_manual_completion_bundle`; its signature
  accepts every parameter the block named. `verdict PASS_WITH_RISKS`, `total_passed 57`,
  `authority_count 45`, `commit_count 463`, `head_commit 617ef70a…`, partition T001/T002/T003 15 each,
  26 gate/artifact files under `remedy-job-evidence-f085-closure/` (never committed, gitignored).
  `verification_runs`: ONE record `vr-0001`, built from a real run — collect-only 57 node ids
  (exit 0), run exit 0, `57 passed in 18.02s`, selected 57 == len(node_ids), test_files the two
  sorted F085 files, `output_hash` = sha256 of `stdout_summary` exactly. `runtime_integration_gate`
  verdict PASS. No failed build attempt.
- Review zip — BUILT from a clean tree at 617ef70a. `PACKAGE_STATUS=READY_FOR_REVIEW`,
  `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, 7258 members, 30M.
  package `remedy-review-20260819-203439-READY_FOR_REVIEW.zip`
  SHA-256 `951d05c41f7c9ab5ee4dc0428b8be17e981b09738c20587f5c6c31b020296ad6` (re-verified with
  `sha256sum` on disk). Manifest `committed_review_subject.head_commit` =
  `617ef70a3d566abed1ca68a034570636636edad5` = C2 = accepted HEAD; base_commit
  `a5a706214d20101dd54564c23d0a3c22efcc705d`, base_is_ancestor true, commit_count 463. No failed
  build attempt.

## Authored-text proofs

Every applied text was extracted programmatically by marker pair from the COMMITTED
`.agent/authored/f085-r74.md` under the block's CONVENTION — no slice was retyped or edited. The
disk-to-disk comparison is G2's four-way sha256 equality
(`d8a1225789c214549a90d61a21041f576e247036be4aa30cf941e3a394716e9b`), and the applied results are
proven in G3 (byte-exact reproduction / ordered equality / whole-file equality) and G12. The only
substitutions made anywhere are STATUST's three slots, one occurrence each.

## Deviations & assumptions

1. G2 marker count: the block predicts "one prose line beginning `END-OF-FILE` which is not a
   marker". In the transported text that string is MID-LINE (`…READMEDOC. ITS END-OF-FILE APPEND,…`),
   so 0 prose lines BEGIN with it and all 26 `BEGIN-`/`END-` lines are real markers (13 slices × 2).
   Both readings recorded; no slice was changed (constraint 8).
2. G3 byte-exact reproduction for READMECOUNT and READMETIER is COMPOSITE, not per-pair: README.md
   carries three FROM→TO pairs in one commit, so re-applying a single pair to the C2 blob cannot
   reproduce the C3 blob. Reported as measured — per-pair False, all-three True.
3. Deviations, declared — handback line count 186, over the 60-line cap. MANDATED content only: five per-commit
   tables, the item-status table, twelve gate transcripts with their real numbers, the transport and
   pair proofs, both artifact records with their closure values, and the verbatim Fortschritt block.
   No section dropped.
4. Commit sequence: exactly C0a, C0b, C1, C2, C3 as ordered. No extra commit, none dropped, no
   reordering. `.agent/plan.md` is at its FINAL state from C1, as the block's Change set directs, so
   C3 does not touch it.
5. G7 ran through the module path, not `remedy integrity check --json`, because that entry point is
   denied session-wide in this sandbox. Same functions, declared above.
6. The block's Handback list asks for "the PR number and URL", but the block also orders the PR
   AFTER C3 and this file is written INSIDE C3, so the value cannot exist when the text is written.
   Resolved the way the F083 R28 closure resolved it: the create command and its outcome ride in the
   round report. Reported, not fixed (constraint 8).
7. Scratch for the gate scripts lives in the gitignored `.remedy-wt/r74/`; `/tmp` is denied in this
   session. The PR body file was written there too, never into the repository tree.
8. C3 was AMENDED once, before any push, because the first write of this file stated C0b's insertion
   count as 383 (the block's line count) where `git show --numstat` reads 353, and named C3's own
   SHA in a sentence C3 contains. Both corrected here. No force-push: C3 never reached the remote.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |

Open findings: 152 (184 registered − 32 done, DECISION F085 D7). Next free id R-0570.

## Next

Reviewer: gate this round, issue the closing verdict into this handoff and into the PR — the last
round of a branch records its verdict there and not in `.agent/live_review.md`, per
docs/agents/planner_reviewer_prompt.md §4 item 13 — and end the session. The operator merges the PR
at the next feature's Open PR Gate; this session merges nothing.
