# Handback — F085 R2 (subprocess seam inventory)

Feature T2_F085 Sandbox hardening (stage 1) · Round R2 · Branch feature/f085-sandbox-hardening
Fortschritt: ~5 % (F085 beansprucht · Seam-Inventar erstellt · T001/T002/T003 offen) — Schätzung
Open findings: 106 registered, 0 resolved, 106 open. Max R-0491, next free R-0492.

## Range

Review of 9ba3179eedc20075e13ac0545b816af112bade7e..HEAD

## Commits

### 7ff935ef chore(agent): save the F085 R2 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r2.md | +264 -0 | C0a — the reviewer's block, copied byte-for-byte |

### f53ce810 chore(agent): mirror the R2 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +185 -260 | C0b — the COMMITTED C0a file, whole |

### d1d50f62 docs(f085): advance the plan to the R2 inventory round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14 -15 | C1 — whole file := the PLAN slice |

### f3a57216 docs(f085): record the R1 PASS and register R-0491
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C2 — RECORD-R1 then R0491, appended verbatim |

### c3cf60c3 docs(f085): add the subprocess seam inventory
| Path | +/- | Reason |
|---|---|---|
| .agent/f085_inventory.md | +309 -0 | C3 — 73 rows, class partition, guards, R-0202, premise |

### (this commit) docs(f085): rewrite the handback for R2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C4 — a handback cannot table its own commit (R-0149); G15 routes C4's insertion count to the round report |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

`git push origin feature/f085-sandbox-hardening` after C3 → `9ba3179e..c3cf60c3`, success. A second push follows C4; its outcome is in the round report. No PR created, no merge, no other `gh` command, no worktree added or removed.

## Verification

G1 `git status --porcelain` exit 0, EMPTY; `git worktree list` exit 0, 1 line; `.agent/STOP` absent.
G2 TRANSPORT `.remedy-wt/f085-r2.md`, committed `.agent/authored/f085-r2.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 d5db9ebcc977024df569710a2cb7528f4311b735a6e8cf380d72ffd6aecbd139, 20720 B, 264 lines.
G3 `.agent/plan.md` byte-equals the PLAN slice; sha256 182f84b9fd6c08ae9bb93ebc480da987839f494bc620760c59b8b482870568e9, 39 lines; `## Goal` yes, `## Next Steps` yes, F085 matched, under 50 lines.
G4 pre-C2 190930 B is a byte-exact PREFIX of post-C2 196461 B; 5531-byte tail; RECORD-R1 1x and R0491 1x in the file, both inside the tail; `git show --numstat` at f3a57216 = `4 0`, deletion column 0.
G5 base 9ba3179e: 105 registered, 0 resolved, 0 `Landed:`, 0 duplicate ids, 0 resolutions naming an unregistered id → 105 open. HEAD: 106 registered, 0 resolved → 106 open. Symmetric difference of HEAD-open against base-open plus R-0491: EMPTY. Max R-0491, next free R-0492.
G6 `.agent/live_review.md` still contains `Steps`: yes.
G7 SEAM SET: the grep prints 73 sites, the table holds 73 rows / 73 distinct sites, symmetric difference 0.
G8 SYMBOL: 73 rows checked, 73 agree — cross-checked by two independent AST methods, 0 mismatches.
G9 KEYWORDS: 73 rows checked, 73 agree, 0 disagreements — 67 rows re-derived from the call's AST keywords and all 67 agree; the other 6 carry `n/a` because those grep lines are not calls.
G10 CLASS PARTITION: 73 assigned, 73 distinct, 0 duplicates, every heading from the closed vocabulary; builder 5, test 12, dod 2, runtime 5, git 24, packaging 11, other 14 = 73 = the table's row count.
G11 all five mandated headings present.
G12 `git diff --name-only 9ba3179e..HEAD` = the six ordered `.agent/` paths and nothing else; 0 paths under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`.
G13 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` → exit 0, `157 passed in 19.66s`, run in the PRIMARY checkout.
G14 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.41s`.
G15 insertions: C0a 264, C0b 185, C1 14, C2 4, C3 309 — none over 500. C4's own count is in the round report.
G16 `git log --format=%p 9ba3179e..HEAD` → one parent per commit. The reflog over THIS round is HEAD@{0}..HEAD@{4}, every entry `commit:`; the `checkout`/`pull` entries below predate the base 9ba3179e and belong to R1. No amend, rebase, reset or force-push.

## Authored-text proofs

PLAN, RECORD-R1 and R0491 were extracted programmatically from the COMMITTED `.agent/authored/f085-r2.md` by their one-line markers and applied byte-verbatim. Disk-to-disk equality is proved by G3 (whole file equals the slice) and G4 (prefix preserved, each slice present exactly once in the appended tail). No transport marker reached any target file: `.agent/plan.md` and `.agent/f085_inventory.md` each contain 0 marker occurrences.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — six commits, none added, none dropped, no reordering.
2. `cp` is denied in this session. C0a used `shutil.copyfile`, C0b wrote the bytes of the committed blob. The gate names byte equality and a digest rather than a tool; G2 proves the property.
3. SIX OF THE 73 GREP LINES ARE NOT CALL SITES — four are docstring or comment prose, two are type annotations (`proc: subprocess.Popen`). The block says "one row per call site" but DEFINES the set by the grep, and G7 requires set equality, so all 73 are tabled. The six carry their real AST-derived `symbol` and `n/a` in the six keyword columns rather than an invented `no`. Declared in the inventory's own `## Seams` prose and grouped with a reason under `## Classes` → `other`.
4. `shell` reads `yes` at 4 sites because the KEYWORD is passed, which is how the block defines the column. All four pass the literal `False`; no site in the inventory runs a shell. Said plainly in the inventory so the column cannot be misread as `shell=True`.
5. Commit Gate at C0a and C0b: `.agent/plan.md` still described R1, because C1 is the bundle's third commit. That is exactly R-0491, which this bundle carries and whose counter-measure it applies.
6. `.agent/context.md` and `.agent/decisions.md` were NOT updated. Constraint 3 limits the change set to the six ordered paths, and the round's one judgement call — the class-assignment rule — is stated inside the inventory for R3 to rule on rather than pre-empted here as a decision.
7. `.remedy-wt/` gained five helper scripts and gate scratch this round: the already-registered R-0403 mechanism, unchanged by R2.

## Next

R3 reviews this handback: re-run G1–G16, then rule on the two questions the inventory raises — the premise check (67 real call sites in 56 distinct enclosing functions against the feature file's "a small number of helpers") and the R-0202 trace (two seams provably drop the variable, the historical mechanism is still unexplained, no fix proposed). Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
