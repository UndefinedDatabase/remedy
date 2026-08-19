# Handback — F085 · R73 (closure prep: R72 PASS recorded, findings registered, Built State written)

Branch feature/f085-sandbox-hardening · base d6d96e50 · tip before C4 e461e9c4 · `.agent/STOP` absent.

Fortschritt: ~100 % der Bauarbeit. R72 ist gegengeprüft und PASSED — Transport, Slice-Formen,
Arithmetik und das Integration Gate hat der Reviewer selbst nachgemessen statt gelesen, und der
einzige rote Lauf unter vier eigenen Voll-Suite-Läufen ist die xdist-Flake-Klasse, die
docs/agents/integration_gate.md Schritt 4 protokolliert statt blockiert. Diese Runde schreibt nur
noch das Protokoll und den Built State; offen bleibt allein die Closure. Schätzung, gemessen gegen
die Klassentabelle aus Amendment F085 D1.

## Range
Review of d6d96e50..HEAD

## Commits
### 0173ad97 chore(f085): save the R73 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r73.md | +293/-0 | C0a — block saved byte-verbatim |

### 5054e081 chore(f085): mirror the R73 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +279/-360 | C0b — verbatim rewrite, AGENTS.md DECISION F104 D1 exempt |

### 319060db chore(f085): advance the plan to R73
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +10/-7 | C1 — PLAN27F→PLAN27T |

### 1961e5cc chore(f085): record the R72 PASS and register three findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +93/-0 | C2 — RECORD42 appended at EOF |

### e461e9c4 docs(f085): append the Built State section to the feature file
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +32/-0 | C3 — BUILTSTATE appended at EOF |

### (this commit) chore(f085): write the R73 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handback cannot table its own commit (R-0149 pattern) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## Verification
G1 STATE: `.agent/STOP` absent immediately before C0a and immediately before C4 (`ls` → No such file or directory). `git status --porcelain` empty at round start and after each of C0a, C0b, C1, C2, C3. `git worktree list` is 1 line at the start and 1 line at the end; no worktree was created this round.
G2 TRANSPORT: all four reads EQUAL — sha256 5fd5b62c53488cd9386701ac8d3781aac6914d15ccbbf4b78a7f3fec34cc8b12, 24180 B, 293 lines, 9 lines beginning `BEGIN-` or `END-`. Budget: TOTAL 293 ≤ 490; slice line counts PLAN27F 11, PLAN27T 14, RECORD42 93, BUILTSTATE 32, sum 150; PROSE 293 − 150 = 143 ≤ 400. Slice sha256 as measured: PLAN27F d851c3bb6037a6c347938762739defa03572630fb91f701fcc0c18eb2990e588, PLAN27T a475859083f95a11d72c5b08f7ccb94e1549fee06d58afd6109d3ce8f8f68b58, RECORD42 ee1701e927e0c5c061b444fb792d72255de9db2c382614acc30a8f49467a92a6, BUILTSTATE 8bf4eaddee75cf0d783dcc2a347e9761b868910a28da9419ed302d0dcb7d4632.
G3 SHAPES: PLAN27F→PLAN27T at 319060db — FROM 1× in the pre-commit blob, 0× post; TO 1× post; `TO contains FROM: false`; re-applying FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY (True). RECORD42 at 1961e5cc and BUILTSTATE at e461e9c4 — ORDERED EQUALITY holds for both: pre is a byte-exact PREFIX (True), slice is an exact SUFFIX (True), `pre + slice == post` (True), and the diff-ADDED lines equal the slice's lines IN ORDER (True). numstat: `10 7 .agent/plan.md`, `93 0 .agent/live_review.md`, `32 0 docs/roadmap/features/T2_F085.md`. Marker lines at the tip before C4: `.agent/plan.md` 0, `.agent/live_review.md` 0, `docs/roadmap/features/T2_F085.md` 0.
G4 DOCS: `python3 -m pytest tests/docs/ -q -rf` exit 0, `295 passed in 0.51s`. `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` exit 0, `30 passed in 0.42s`. Both in the primary checkout, serially, after C3; sum 325, matching the reviewer's pre-applied worktree reading.
G5 STATE READERS: the four-file command exit 0, `160 passed in 19.93s`, primary checkout, serially, after C2.
G6 PLAN CONTRACT at 319060db: `.agent/plan.md` is 41 lines ≤ 50; `## Goal` present, `## Next Steps` present, `\bF\d{3}\b` matches `F085`.
G7 ARITHMETIC (DECISION F085 D7, OPEN = REGISTERED − DONE): at d6d96e50 — 181 registered, 32 done, OPEN 149, which is exactly the reviewer's own base reading. At e461e9c4 — 184 registered, 32 done, OPEN 152. Registered symmetric difference {R-0567, R-0568, R-0569}; done symmetric difference empty. 0 duplicate registered ids and 0 resolutions naming an unregistered id at BOTH SHAs. Max registered R-0566 → R-0569; max resolved R-0564 at both. Next free id R-0570.
G8 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 20.39s`.
G9 HYGIENE: `git diff --name-only d6d96e50..e461e9c4` = `.agent/authored/f085-r73.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F085.md` — five of the six paths the Change set names, the sixth (`.agent/handoff.md`) being C4 itself; none ends `.log`; none lies under `packages/`, `apps/`, `scripts/` or `tests/`. Insertions per commit before C4: 293, 279, 10, 93, 32 — all ≤ 500. All five commits in the range are single-parent.

## Authored-text proofs
Disk-to-disk under the digest fallback (no scratchpad original exists in self-drive): the committed `.agent/authored/f085-r73.md`, the committed `.agent/last_block.md` and both working copies are byte-EQUAL at sha256 5fd5b62c53488cd9386701ac8d3781aac6914d15ccbbf4b78a7f3fec34cc8b12. Every applied slice was extracted PROGRAMMATICALLY from the committed authored blob `0173ad97:.agent/authored/f085-r73.md` by its marker pair under the block's CONVENTION — never retyped and never re-copied from the prompt a second time. No `Done:` and no `Gate:` text was authored by this worker.

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C4. No PR created, nothing merged, no `git worktree add` and therefore no `git worktree remove`.

## Deviations & assumptions
- No departure from the block's ordered commit sequence: exactly C0a, C0b, C1, C2, C3, C4 in that order — no extra commit, no dropped commit, no reordering.
- READING NOTE, not a fix and not a contradiction: G2's count of lines beginning `BEGIN-` or `END-` is 9, of which 8 are the four slices' own marker lines; the ninth is the CONVENTION prose line that begins `END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD42 AND BUILTSTATE`. The block predicts no value for this count, so both readings are reported rather than reconciled. That prose line reaches no target file — G3's per-file marker counts are 0.
- `.agent/context.md` and `.agent/decisions.md` are deliberately untouched, exactly as the block's Change set states; their absence is not an omission.
- Scratch helpers (slice extractor, suite runner, arithmetic script, gate logs) live under the gitignored `.remedy-wt/` and never enter a commit; `git status --porcelain` is empty with them present.
- Deviations, declared: this handback is 81 lines against the 60-line cap. Cause, all of it mandated content: six per-commit changed-files tables (24 lines), the item-status table (8 lines), and the nine gate results of G1–G9 with their real operands and digests. No section was dropped to meet the cap.

## Next
Reviewer gates this round, then R74 CLOSURE per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the reviewer-authored STATUS line and README capability sync, and the PR the operator merges at the next Open PR Gate. Open findings at the tip: 152.
