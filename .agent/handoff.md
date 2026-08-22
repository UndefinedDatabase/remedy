# Handback — F009 R33, closure round one

## Range
Review of `1dc72f82333f681fe61af0b75712ac8ff7e34c39`..HEAD — round base
`1dc72f82`, five commits: C0a `02eb5f8e`, C0b `a97537ee`, C1 `f54fe49a`,
C2 `97d02898` (ACCEPTED HEAD), C3 this commit.

Fortschritt: ~100 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidence-Job und Review-Zip in
             dieser Runde; danach bleiben nur STATUS-Zeile, README-Sync und der
             Pull Request) — Schätzung

## Closure values
| Value | Reading |
|---|---|
| Evidence job | `f009-closure` |
| package | `remedy-review-20260822-085607-READY_FOR_REVIEW.zip` |
| SHA-256 | `ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f` |
| accepted HEAD | `97d028980b5781cbf22a0f651f7e879eea1a0485` |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `02eb5f8e` |
| C0b | done | `a97537ee` |
| C1 | done | `f54fe49a` |
| C2 | done | `97d02898` — the ACCEPTED HEAD both artefacts record |
| C3 | done | this commit |

## Commits
### 02eb5f8e docs(state): save the F009 R33 closure block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f009-r33.md` | 462/0 | the received block saved byte for byte |

### a97537ee docs(state): mirror the F009 R33 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 402/190 | mirrored FROM the committed C0a blob |

### f54fe49a docs(state): point the F009 plan at closure round one
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 13/14 | PLANF009R33 applied as a whole-file replacement |

### 97d02898 docs(review): record the R32 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | LEDGER33 appended; this commit is the ACCEPTED HEAD |

### C3 — this commit — docs(state): write the F009 R33 closure handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-reference | a handoff cannot table the commit that writes it (R-0149); its numstat belongs in the round report (§4 item 14) |

## External actions
- `git push -u origin feature/f009-single-write-channel` after C2 → `1dc72f82..97d02898`; `git rev-parse origin/feature/f009-single-write-channel` == `97d028980b5781cbf22a0f651f7e879eea1a0485`. Exit 0.
- `git push` after C3 → the round's last action, reported in the round report; a handback cannot record the push of the commit that writes it.
- No `gh` command, no worktree add/remove, NO pull request created — the PR is the next round.

## Verification
- G1 exit 0 — `.agent/STOP` ABSENT before C0a and again before C3; branch `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and immediately before both artefact builds. Round base read at step 0: `1dc72f82333f681fe61af0b75712ac8ff7e34c39`. Base targets: `.agent/live_review.md` 584339 bytes/1144 lines ending in exactly ONE newline, `.agent/plan.md` 2029 bytes/38 lines.
- G2 TRANSPORT — the committed C0a blob, `.agent/last_block.md` at C0b and the received `.remedy-wt/f009-r33.md` are all sha256 `0ee2aa94c7875f7912274654a5974c83c06444092fdf09b204ce5bb7f4bff9ca` over 33170 bytes and 462 lines. C0b was written FROM the committed C0a blob via `git show`, never from the scratch copy.
- G3 SLICES — extracted from the committed C0a blob by marker line; the script printed an aggregate of **3** slices over **186** CONTENT lines. PLANF009R33 `d3bfc1d3…` 2091 bytes/37 lines; LEDGER33 `51bbd2a9…` 5306 bytes/1 line; EVIDENCESCRIPT `75931cd7…` 6675 bytes/148 lines. Constraint 10 re-measured from that same blob: TOTAL **462** (cap 490), PROSE **276** (cap 400) — both agree with the block.
- G4 PLAN — `cmp .agent/plan.md` vs PLANF009R33 exit **0**, both sha256 `d3bfc1d3291b00e24dd9686fa271115afe0a06d2e2e18686499739d220a2321a`; negative control `cmp` vs `.agent/last_block.md` exit **1**. `wc -l` 37 against the 50-line cap. `^## Goal$` 1, `^## Next Steps$` 1, `\bF\d{3}\b` matches include `F009`.
- G5 APPEND, two independent readers + negative control — N counted BY SCRIPT = **1**. (a) prefix reader: the base blob is a byte-exact PREFIX and the remainder equals a newline plus the slice; (b) paragraph reader: the last 1 blank-line-separated unit equals the slice's 1 paragraph. 584339→589646 bytes, 1144→1146 lines; slice sha256 `51bbd2a9…` 5306 bytes/1 line; post-file sha256 `0a08ad05…`. Flipping one printable byte (`G`→`Z`, equal length, offset 584340) INSIDE the FIRST appended paragraph: BOTH readers REJECT the mutant, BOTH ACCEPT the true file. Script exit 0.
- G6 SETS, line-anchored, at the round base AND at C2 — base: `- R-` entries **213** all DISTINCT, `Done: R-` **3**, `Landed: ` **0**, `Gate: R` keys **32** over **32** DISTINCT, `Gate: R33` **0**. C2: entries **213** all DISTINCT, `Done: R-` **3**, `Landed: ` **0**, `Gate: R` keys **33** over **33** DISTINCT, `Gate: R33` **1**. Every base reading reproduces the reviewer's.
- G7 ANCHORING CONTROL as a DIFFERENCE, both scan shapes named, at the round base AND at C2 — base: **213** anchored ids, **273** distinct `R-\d{4}` anywhere, **60** never registered as a leading id, **32** anchored `Gate: R\d+` keys, unanchored KEY-SHAPED `Gate: R\d` **84**, unanchored LITERAL `Gate: R` **131** — all six reproduce the reviewer's. C2 as MEASURED: **213**, **273**, **60**, **33**, key-shaped **88**, literal **140**.
- G8 CEILING by DECISION F009 D10 (anchored `^- R-\d+ — ` minus `^Done: R-\d+`) — base: max REGISTERED id **R-0647**, open **210**. C2: max REGISTERED id **R-0647**, open **210** — both UNCHANGED, which is constraint 3 as a measurement. Next free id remains R-0648.
- G9 RANGE base→C2 — lists exactly `.agent/authored/f009-r33.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`; set difference EMPTY in both directions; **0** paths beginning `packages/`, `apps/`, `docs/` or `tests/`; `docs/roadmap/STATUS.md` ABSENT and `README.md` ABSENT. Four commits, each ONE parent; `git show --numstat` (no `--` before the SHA) and `git diff --numstat` AGREE on every cell, and every cell equals the `## Commits` +/- column: 462/0, 402/190, 13/14, 2/0. Pre-handback insertions 462, 402, 13, 2 — each under the 500 cap. Line-anchored `<<<SLICE ` and `<<<END ` read **0** LINES in both slice targets (`.agent/live_review.md` holds 25 unanchored substrings of each, which LEDGER33 legitimately quotes mid-line). `git ls-files .remedy-wt` **0**. This round's **4** reflog rows all classify as `commit`; `amend` **0**, `rebase` **0**, `cherry` **0**; no total asserted over the whole reflog.
- G10 CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the primary checkout, serially — REAL exit **0**, `42 passed in 20.49s`.
- G11 EVIDENCE JOB at C2 — clean tree before and after the push; `.remedy-wt/r33_evidence.py` sha256 `75931cd75f70797093b47daac7116aa57bd93929dc43f58c3a1a492dcaea56c5` EQUALS the slice's. Bundle dir did NOT pre-exist (read before the run); holds **27** entries after. Script REAL exit **0**. Per-run lines it printed: vr-0001 selected 99 node_ids 99 deselected 1 files 1; vr-0002 4/4/0/1; vr-0003 27/27/1/1; vr-0004 16/16/1/1; vr-0005 11/11/0/1 — every one matching the block. `SCAN rejected strings: 0 []` and `SCAN red control: a local absolute path`. `OUTPUT_HASH` True for all five runs. Producer summary: `authority_count` 17, `commit_count` 233, `head_commit` `97d028980b5781cbf22a0f651f7e879eea1a0485` (EQUALS C2), `job_id` `f009-closure`, `manual_completion` true, `operator_attested_tasks` ["T001","T002","T003"], `total_passed` **157**, `verdict` **PASS_WITH_RISKS**.
- G12 INTEGRITY CHECK at C2 via `from packages.orchestration.integrity_gate import run_integrity_checks` then `run_integrity_checks()` — `passed` **True**, `fail_count` **0**, five checks all PASS: `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `high_blockers_open`.
- G13 REVIEW ZIP at C2, clean tree and branch pushed, run WITHOUT a pipe under a wrapper — REAL exit **0**. `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`. Package `remedy-review-20260822-085607-READY_FOR_REVIEW.zip`, script `final_sha256` `ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f`, and sha256 recomputed over the file on disk RECOMPUTES the same value. `member_count` 12906 == `zipfile.namelist()` 12906. From `.review_zip_manifest.json` inside the package: `base_commit` `ce49348b8f5b0374417f5b6c47d8c04966e7108e` (the required 40 chars), `head_commit` `97d028980b5781cbf22a0f651f7e879eea1a0485` (EQUALS C2), `base_is_ancestor` true, `commit_count` 233, `file_count` 64, `packaged_evidence_job_id` `f009-closure`, `ready_gate_matrix.ok` true with `blocking_reasons` [], `review_subject_evidence_alignment.verdict` PASS with 0 issues and 0 hash mismatches. Exit 0 is NOT the reading; PACKAGE_STATUS is, and it is READY_FOR_REVIEW.
- G14 HANDBACK — this file carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a, C0b, C1, C2 and C3, the round base SHA, one line per gate, the block's `Fortschritt:` VERBATIM across all four of its lines, the `## Closure values` table with exactly four rows, and both points' values for every gate that ordered a reading at several points (G1, G6, G7, G8). Its `wc -l` is declared below.

## Authored-text proofs
All three slices were extracted PROGRAMMATICALLY from the committed C0a blob by their `<<<SLICE `/`<<<END ` marker lines and applied without retyping. PLANF009R33 → `.agent/plan.md`: `cmp` exit 0, sha256 `d3bfc1d3…` both sides, negative control exit 1 (G4). LEDGER33 → `.agent/live_review.md`: byte-exact prefix + newline + slice under two independent readers with an equal-length printable-byte flip REJECTED by both (G5). EVIDENCESCRIPT → `.remedy-wt/r33_evidence.py`: sha256 `75931cd7…` equal to the slice, executed, never committed as itself — its bytes reach the record inside the C0a blob (G11).

## Deviations & assumptions
- Deviations, declared (DECISION D15): this handback is **88 lines**, over the 60-line cap that applies to a five-commit round (the 100-line allowance needs a per-commit table of more than five commits; this round has exactly five). The overage is caused solely by MANDATED content — the per-commit tables, the item-status table, the `## Closure values` table, the authored-text proofs, and the fourteen gate lines, four of which (G6, G7, G8 and G11/G13) must carry every reading at BOTH measurement points and the artefacts' full digests and manifest fields. No section was dropped to meet the cap.
- NO departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, exactly five commits, in that order, with no extra, no dropped and no reordered commit.
- No finding id was minted and nothing was resolved (constraint 3). The next free id is R-0648, as it was when the round began.
- OBSERVATION, no id spent (closure-candidate rule): none. Every gate reproduced the value the block predicted where it predicted one, and the two gates the block left unpredicted (G7 at C2, G13's manifest counts) were reported as measured.
- Assumption: none required. No slice looked wrong; none was adjusted.

## Next
Closure round TWO — the closure commit: the reviewer-authored STATUS `[x]` line for F009 and the README capability sync in the SAME commit (R-0154), plus the final `.agent/` state, then the pull request per the AGENTS.md PR workflow. NO pull request exists yet; none was created this round. The four `## Closure values` rows above are the sole input the STATUS line is authored from. The PR is NOT merged in this session — it merges at the next feature's start via the Open PR Gate. Before authoring, re-read `.agent/STOP` from disk (Phase 1 rule 1) BEFORE the Open PR Gate (rule 2).
