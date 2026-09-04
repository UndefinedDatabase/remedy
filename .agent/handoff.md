# Handoff — F112 Prompt budget per task class, round 31 (README numerals fixed, docs gate green, PR #234 opened — NOT merged)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-30 carried forward unresolved — "6 (or 7)")
· round 31 · rounds so far 31.

This round is NOT a fresh loop-session bootstrap — it is a direct
continuation of round 30's own session, so the session number is
unchanged from round 30.

## Range

Review of `9b30be51..HEAD` (base is F112 R30's handback commit).

## Commits

### b3b02146 F112 R31 C0a: save the round 31 step block verbatim to .agent/authored/f112-r31.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r31.md` | +158/-0 | transport proof — verbatim copy of the supplied step block |

### 718fc035 F112 R31 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +158/-193 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 619b1fa2 F112 R31 C1: append RECORD30 to live_review.md (books R30 PASS-with-declared-deviation, no new finding)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD30 (books round 30's PASS-with-declared-deviation verdict; no new finding registered or resolved) |

### 98027a76 F112 R31 C2: apply PLAN31 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14/-17 | whole-file replace with PLAN31 |

### 71820a17 F112 R31 C3: fix README's two stale derived numerals moved by round 30's closure commit
| Path | +/- | Reason |
|---|---|---|
| `README.md` | +2/-2 | `69 of 266` → `70 of 266`; Tier 3 table Done cell `4` → `5` (Total `26` unchanged) — only these two lines touched |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) |

## External actions

- `git push -u origin feature/f112-prompt-budget-per-task-class` → succeeded, `9b30be51..71820a17`, upstream tracking set.
- `gh pr create --base main --head feature/f112-prompt-budget-per-task-class --title "F112: prompt budget per task class + evidence-packager fix" --body-file <tmp>` → succeeded, **PR #234**, `https://github.com/UndefinedDatabase/remedy/pull/234`, state OPEN, not draft, base `main`, head `feature/f112-prompt-budget-per-task-class`. NOT merged.
- `gh pr list --state open ...` (pre-C5, Open PR Gate check) → `[]`, no blocking PR.

## Verification

`python3 -m pytest tests/docs/ -q`:
```
295 passed in 0.45s
```
(was `2 failed, 293 passed` at round 30's C3; now fully green as required.)

`python3 -m pytest tests/cli/test_golden_path.py -q`:
```
42 passed in 20.51s
```

`git status --porcelain` — empty, checked before C0a and immediately before this handback commit.

README numeral independent re-derivation (performed before C3, per the
block's own instruction, not trusted from the block's arithmetic):
- `grep -cE '^\- \[x\] F[0-9]{3} — ' docs/roadmap/STATUS.md` → `70`
  (matches the block's expected accepted count).
- Python re-derivation of Tier 3's Done count, resolving each accepted
  `F\d{3}` id's tier via its `docs/roadmap/features/T<n>_F<nnn>.md`
  filename (same method
  `test_the_readme_tier_table_done_column_matches_the_ledger` uses):
  `{0: 16, 1: 22, 2: 14, 3: 5, 5: 13}`, total 70. Tier 3 = `5`, matching
  the block's expected number. Both readings agreed with the block, so
  C3 proceeded.

Post-C3 counts: `69 of 266` → 0 occurrences in README.md; `70 of 266` →
1 occurrence; Tier 3 row reads `| 3 | Full Token Economy & Autonomy | 5
| 26 |` (Total unchanged at 26). `git diff README.md` touches exactly
those two lines, nothing else.

## Authored-text proofs

- `.agent/authored/f112-r31.md` (copied via `cp`, never retyped) sha256
  `d956918ba8b6670d26cad7435495ddbb507aa002ef524c0a94982622ad5f23d9` at
  12589 bytes, 158 lines — matches the supplied stamp exactly (verified
  before starting).
- `git rev-parse HEAD:.agent/authored/f112-r31.md` and
  `HEAD:.agent/last_block.md` both print blob
  `243f97e1f7340dfed0ce145bf7bcea460069bde5` — confirmed equal after C0b.
- RECORD30 extracted from the committed authored file between its
  `--- BEGIN RECORD30 sha256=2e49de0afd8009b49321f130aada5a6ad123c1e855a35f6dea365827efde55a2 ---`
  / `--- END RECORD30 ---` markers: 4121 bytes (trailing newline before
  the END marker excluded), sha256
  `2e49de0afd8009b49321f130aada5a6ad123c1e855a35f6dea365827efde55a2` —
  matches the stamp exactly. Appended as `content_bytes + b"\n" +
  RECORD30_bytes`; `.agent/live_review.md` measured `2346878` bytes
  immediately after (`2342756 + 1 + 4121`, matching the block's pinned
  figure exactly), byte-exact prefix confirmed against the pre-append
  file, no trailing newline. Registered/`Done:`/open counts (354/74/280)
  unmoved both sides of C1 — RECORD30's own text contains no
  "Registered as" mint and explicitly states "NO NEW FINDING ID IS
  MINTED".
- PLAN31 extracted the same way between its
  `--- BEGIN PLAN31 sha256=67b435cbe664767cc0da2e1607ab2e6a311869d164bd9c3ed8a58415e57c77bf ---`
  / `--- END PLAN31 ---` markers: 1700 bytes (trailing newline
  excluded), sha256 `67b435cbe664767cc0da2e1607ab2e6a311869d164bd9c3ed8a58415e57c77bf`
  — matches the stamp exactly. `.agent/plan.md` replaced wholesale,
  reproduced byte-identical (1700 bytes), `wc -l` = 38 (under 50), no
  trailing newline, `## Goal`/`## Next Steps` each exactly once.

## Deviations & assumptions

None. The block's commit sequence (C0a, C0b, C1, C2, C3, C4, C5,
handback) was followed exactly in order; both README numbers were
independently re-derived and agreed with the block before C3 was
applied; the docs gate came back fully green at C4 on the first attempt
(no second guess was needed); C5 pushed and opened PR #234 without
merging it, per the Open PR Gate and G1.

## Next

Round 32 (Open PR Gate): wait for hosted CI on PR #234 to read green,
re-confirm the docs gate/canary/touched suites and the Open PR Gate
checklist, then the planner merges per the standing merge-autonomy rule
(`gh pr merge 234 --merge --delete-branch`) — never in the same round/session
that created the PR. Hand back the built review zip's filename and
SHA-256 to the operator once more for archiving and the formal package
review: `remedy-review-20260904-123332-READY_FOR_REVIEW.zip`, sha256
`b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`.
