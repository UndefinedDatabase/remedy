# Handoff — F062 R4 (CLOSURE)

## Range
Review of `b2c17ea1..HEAD`; accepted HEAD `52a283cf` (deviation 1). F062 closed:
STATUS `[x]`, README synced same commit, Built State recorded, zip verified.

## Commits
### 4bc84da3 chore(f062): persist the R3 verdict
| Path | +/- | Reason |
| --- | --- | --- |
| `.agent/authored/f062-r4-{1..4}.md`, `live_review.md`, `last_block.md` | +249/-96 | four authored texts sha256-verified; r4-1 applied; R4 block verbatim |

### ba4f94db docs(f062): record the accepted Built State
| Path | +/- | Reason |
| --- | --- | --- |
| `docs/roadmap/features/T1_F062.md` | +47 | f062-r4-2 byte-appended (precondition 4) |

### 52a283cf test(f062): package-safe parametrize ids
| Path | +/- | Reason |
| --- | --- | --- |
| `tests/orchestration/test_product_smoke.py` | +14/-7 | explicit ids so no node id reads as a local absolute path (deviation 1) |

### Final closure commit + handoff (grouped self-reference, R-0149)
| Path | +/- | Reason |
| --- | --- | --- |
| `docs/roadmap/STATUS.md`, `README.md`, `.agent/{handoff,last_block}.md` | +3/-3 + rewrite | STATUS `[x]` with the four filled values; both README edits (R-0154, same commit); this report; OUTCOME executed |

## External actions
- `git push` after each commit and before handback (head == remote).
- `gh pr create --base main` → **PR #174**, NOT merged (merges at the next Open
  PR Gate); created before the closure commit — deviation 2.
- No worktrees this round; `git worktree list` → primary only.

## Verification
    $ pytest tests/docs/ -q 293 passed EXIT=0 · test_golden_path.py 42 EXIT=0
    $ pytest .../test_product_smoke.py -q  76 passed EXIT=0
    $ remedy integrity check --json  passed true, 5/5   $ porcelain (empty)
      candidates.md: "No open candidates."
Evidence job **76ee4cb7318e409e**, built outside the repo, never committed.
Pre-zip: `ready_gate_matrix ok True`, `blocking_reasons []`,
`is_valid_current_run True`, `validation_errors []`, final-verifier and
token-truth `VERIFIED_EQUAL`. **The FIRST bundle was rejected** — raw:

    ok: False; blocking_reasons: ['...VerificationTests total is missing or
    invalid', 'verification_tests.json field runs[0].node_ids[29] carries a
    local absolute path']  ← [entry0-must start with '/']

No zip was built from it; dir deleted, rebuilt after the cause fix. Package
**remedy-review-20260801-214231-READY_FOR_REVIEW.zip** · SHA-256
**46e684f5954a32c92994781a734bf3c26d830ba288e63d48fe4d5dc441b8ab29**
(recomputed from disk): READY_FOR_REVIEW · alignment PASS · evidence
authoritative · subject `b836d364..52a283cf` · `testzip()` clean · import smoke
over the PACKAGED sources (modules import, runner registered, no registration
by import, `ps.register()` works); tmp extract removed.

## Authored-text proofs
`f062-r4-1` 913c9ac0… · `-2` 6993425a… · `-3` 97d38c08… · `-4` 93add0b0…, all
matching their BEGIN markers. r4-3's TO arrived transport-wrapped; both forms
hashed before writing, single-line matched (R-0148). r4-1's TO embeds its FROM,
occurring once in `live_review.md`. STATUS: FROM 1→0, TO 0→1, numstat `1 1`;
substituting the four values back reproduces the authored TO byte-for-byte.
README: both FROM gone, both TO once, numstat `2 2`.

## Deviations & assumptions
1. **Accepted HEAD is `52a283cf`, not commit 2.** A parametrize needle
   (`"must start with '/'"`) put a slash inside a node id, which the validator
   reads as a local absolute path. I fixed the cause (explicit `pytest.param`
   ids) rather than trimming the run — a content commit, so zip, manifest and
   STATUS all name `52a283cf`. Same class as F061 R4. **Please confirm.**
2. **PR created before the closure commit**, so the template's "PR entries
   carry the number" rule is met here; Rule A4 holds (closure commit last, PR
   picked it up on push).
3. **My pre-flight guard was too narrow** (caught `[/` and `..`, not a slash
   mid-parameter); tightened to reject ANY slash in a bracketed param id.
4. **`output_hash` omitted** so the producer derives it; evidence dir outside
   the repo per the amended protocol. `PASS_WITH_RISKS` is the producer's
   documented value here, not a new risk. Open findings 0.

## Next
F062 closure complete — PR #174 open, awaiting the next Open PR Gate.
