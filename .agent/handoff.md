# Handoff — Process-Hardening v2 · PH-4 (R-0149 amendment round)

## Range

Review of `a1a0db7..HEAD` (main..HEAD) — 6 commits.

## Commits

### 86a55b8 chore(ph4): persist authored amendment texts; R-0149 ruling recorded
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/phv2-r1-1.md | +55 −0 | handback template v1.1, verbatim |
| .agent/authored/phv2-r1-2.md | +7 −0 | AGENTS.md cap paragraph, verbatim |
| .agent/authored/phv2-r1-3.md | +5 −0 | split_workflow cap sentence, verbatim |
| .agent/authored/phv2-r1-4.md | +16 −0 | fidelity protocol + hash guard, verbatim |
| .agent/authored/phv2-r1-5.md | +8 −0 | bootstrap bullet, verbatim |
| .agent/authored/phv2-r1-6.md | +7 −0 | reviewer §4 item 9, verbatim |
| .agent/authored/phv2-r1-7.md | +6 −0 | R-0149 ruling text, verbatim |
| .agent/live_review.md | +6 −0 | phv2-r1-7 appended to the R-0149 entry |
| .agent/plan.md | +23 −20 | PH-4 round plan |

### a944c4a docs(agents): handback template v1.1 — cap wording, self-reference rule (R-0149)
| Path | +/- | Reason |
|---|---|---|
| docs/agents/handback_template.md | +7 −1 | A1 — full replace from phv2-r1-1 |
| .agent/plan.md | +2 −2 | Commit Gate |

### 1a1e994 docs: handoff cap ruling in AGENTS.md (R-0149)
| Path | +/- | Reason |
|---|---|---|
| AGENTS.md | +5 −3 | A2 — handoff Purpose paragraph replaced by phv2-r1-2 |
| .agent/plan.md | +2 −2 | Commit Gate |

### 2487616 docs(agents): fidelity hash guard and cap ruling in split workflow (R-0149)
| Path | +/- | Reason |
|---|---|---|
| docs/agents/split_workflow.md | +28 −22 | A3/A4/A5 — phv2-r1-3, r1-4, r1-5 |
| .agent/plan.md | +2 −2 | Commit Gate |

### 77afd6a docs(agents): reviewer emits sha256-stamped authored blocks (R-0149)
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +5 −3 | A6 — §4 item 9 replaced by phv2-r1-6; item 10 untouched |
| .agent/plan.md | +2 −2 | Commit Gate |

### HEAD chore(ph4): handback — handoff per the amended template
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |
| .agent/plan.md | +4 −4 | round complete |

Self-reference note (now codified in handback_template.md): the HEAD table
states intended content, since no commit can table the commit writing it.

## External actions

`gh pr list --state open` → PR #153 (F047) open, NOTED, untouched (D1).
`git push -u origin chore/process-hardening-v2` → new remote branch, then
`git push` ×3 (A2, A3-5, A6) plus one for this handback — all succeeded.
`gh pr create` → PR #155 into main; NOT merged, not edited since (D3).

## Verification

```
$ for n in 1..7; do sha256sum .agent/authored/phv2-r1-$n.md; done
12d0062c… d3d59edd… d0dc6594… 5a7f9649… 7faabd6f… 2b6d6be7… 4f9ef20e…
→ 7/7 identical to the BEGIN-marker hashes. No STOP triggered.

$ python3 - <<'PY'   (Part-3 proof script)
OK ×1 byte-equality, OK ×6 substring, OK ×6 gone-checks
PROOFS: PASS                                              EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 14.91s
                                                          EXIT=0
$ git status --porcelain     # empty
```
Full untruncated hash and proof output is in the completion report.

## Authored-text proofs

All seven texts were saved to `.agent/authored/`, hash-verified against
their BEGIN markers, and only then committed (86a55b8) — the new guard's
first live run, and it also confirms the paste-frame stripping was byte-
correct. Applications: phv2-r1-1 by `cp` (`cmp` clean, byte-equality in the
proof script); the other six as exact-substring inserts. Each replacement
additionally asserts the superseded wording is GONE from its target file —
6/6 OK. No retype anywhere.

## Deviations & assumptions

- D1/D2/D3 per operator directive 2026-07-27: PR #153 untouched, branch is
  `chore/*`, PR #155 created but not merged.
- One formatting edit outside authored text: the split_workflow replacement
  stranded `Purpose: a restarted Window 1` on a short line, so that
  following paragraph was re-wrapped. Own artifact, no wording changed.
- `docs/README.md` needs no update: no docs added or renamed.

## Next

Window 1 reviews `a1a0db7..HEAD`; on PASS, PR #155 merges next block.
