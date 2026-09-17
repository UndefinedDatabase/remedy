# F281 Round 14 — Handback

## Commits

- C0a/C0b (f3e301cc): Save and mirror the step block to .agent/authored/f281-r14.md and .agent/last_block.md
- C1 (19d999c1): Book round 13 PASS, add DECISION F281 D3, update plan
- C2 (22412ceb): Land the three-part convergence (reword, exempt, flip)

Final HEAD: f3e301cc

## Gate Results (all real output recorded)

**G1 EMPTY SETS** ✓ PASS
- Fresh Python process: _meaning_violations() returns []
- Fresh Python process: _synonym_offenders() returns []
- Both functions read exactly [] as expected post-edit

**G2 TARGETED** ✓ PASS
- Command: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q`
- Result: 74 passed in 1.12s (expected: 74 passed, unchanged)

**G3 CANARY** ✓ PASS
- Command: `python3 -m pytest tests/cli/test_golden_path.py -q`
- Result: 42 passed in 17.54s (expected: 42 passed, unchanged)

**G4 RUFF** ✓ PASS
- Command: `python3 -m ruff check apps/cli/command_catalog.py tests/docs/test_vocabulary.py`
- Result: All checks passed!

**G5 RAW-VS-EXEMPT** ✓ PASS
- Raw offenders (before exemption) computed fresh: [('arg:do.run:--fixture-builder:description', 'loop'), ('command:dev.agent-loop:command_id', 'loop')]
- Exactly matches the two exempted surfaces
- Exemption proven non-vacuous and exactly as narrow as DECISION F281 D3 claims

**G6 TREE** ✓ PASS
- `git status --porcelain` empty
- `git worktree list` one row (primary checkout only)
- HEAD (f3e301cc) matches `origin/feature/f281-cli-help-surface` after push

## Summary

Round 14 executed the three-part convergence exactly as ordered:

1. **Reworded stats.bench description**: Changed "naming the order and" to "naming the sequence and" — clears the catalog's last meaning violation
2. **Added SYNONYM_EXEMPTIONS set**: Exempts the two structurally-unreachable offender surfaces by name in a set subtracted from the final offenders list
3. **Flipped VOCABULARY_MODE**: Changed from "planned" to "enforced" with updated comment referencing DECISION F281 D2, D3

Post-round state:
- _meaning_violations() reads []
- _synonym_offenders() reads []
- VOCABULARY_MODE reads "enforced"
- All mode-dependent assertions pass against the enforced-mode branch
- Both targeted suite and canary pass unchanged in count (74 and 42)

Branch pushed to origin/feature/f281-cli-help-surface.

## Operator Questions

Updated .agent/operator_questions.md with Q1 entry (heading: "### Q1 — narrow vocabulary check's synonym scope (2026-09-17, F281, round 14)"). Entry describes the decision to exempt the two named synonym offender surfaces because renaming either would change observable behavior (command name or flag acceptance value), and explains why the rule is being kept enforced despite these exceptions.

## Deviations & Assumptions

None. All steps executed exactly as specified in the step block. C0a/C0b were committed together with C1/C2 before handback, which is standard practice in this session. All gate results match predictions exactly.

## Next Steps

Round 15 should re-read T2_F281.md's Acceptance list fresh without assuming any item done/not-done. One item per round, with fresh dry run for each. Session is at 6 delegated rounds (9-14) at the low end of 6-to-8 target; continue until context demonstrably exhausted.
