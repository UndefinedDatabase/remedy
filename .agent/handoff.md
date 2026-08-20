# Handback — F086 R15, the DATA and the CALLER (branch feature/f086-release-capability)

## Range

Review of 6f5a589a..HEAD

## Commits

| # | Commit | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 16889dd5 | .agent/authored/f086-r15.md | +489/-0 | the block, byte-verbatim |
| C0b | 866d905d | .agent/last_block.md | +404/-245 | mirror of the COMMITTED C0a |
| C1 | b59fbd8f | .agent/plan.md | +16/-17 | the PLAN15 slice, whole file |
| C2 | 96483707 | .agent/live_review.md | +4/-0 | FIND0583 then RECORD13, appended |
| C3 | 3b77cf19 | CHANGELOG.md | +24/-0 | the CHANGELOG slice, a NEW file |
| C4 | 8cdecc5b | scripts/release_gate_check.py | +72/-0 | the RUNNER slice, a NEW file |
| C5 | 5bfdddfa | tests/orchestration/test_release_gate_wiring.py | +91/-0 | the TESTS slice, NEW |
| C6 | this commit | .agent/handoff.md | rewrite | R-0149: cannot table itself |

## External actions

`git push -u origin feature/f086-release-capability` after C5 → `6f5a589a..5bfdddfa`, and again after C6 (the round report carries that one). `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; no PR created, nothing merged. `git worktree add .remedy-wt/r15-probe HEAD --detach` for G9, G10 and G11's control, then `git worktree remove` + `git worktree prune`; `git worktree list` now reads one line.

## Verification

One line per gate. The FULL transcript — every command, its real exit code, its output and every 64-character digest — is in the ROUND REPORT (block step C6, the R-0582 repair; G15 measures it).
G1 primary tree EMPTY at every commit and at the handback, `.agent/STOP` absent before C0a and again at the handback, branch `feature/f086-release-capability`, HEAD at 6f5a589a when the round began.
G2 `.remedy-wt/f086-r15.md` ≡ committed authored ≡ committed last_block, all three byte-EQUAL, 29861 B, 489 lines; size re-measured from the COMMITTED file as 489 total / 244 prose / 245 slice incl. 12 markers, which is what the block declares of itself.
G3 `.agent/plan.md` ≡ PLAN15, 42 lines (under 50), holds `## Goal`, `## Next Steps` and `F086`.
G4 the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob; the 4-line remainder ≡ FIND0583 followed by RECORD13, in that order.
G5 HEAD reads 166 registered / 2 resolved / 0 duplicate ids / 0 unregistered resolutions / 0 `Landed:` / 164 open under BOTH extractions, and the two registered SETS are EQUAL; the symmetric difference against 6f5a589a is `['R-0583']`; the control over 3351878d..a662abcc reads `['R-0582']`, so the extractor can see a difference.
G6 0 lines beginning `<<<SLICE ` or `<<<END ` in plan.md, live_review.md, handoff.md, CHANGELOG.md, scripts/release_gate_check.py and tests/orchestration/test_release_gate_wiring.py.
G7 `CHANGELOG.md` ≡ CHANGELOG (1146 B, 24 lines), `scripts/release_gate_check.py` ≡ RUNNER (2966 B, 72 lines), `tests/orchestration/test_release_gate_wiring.py` ≡ TESTS (3785 B, 91 lines); `git ls-tree 6f5a589a` prints nothing for each, so all three commits are creations, not edits.
G8 exit 0, 21 passed — the wiring suite and the gate suite together, primary checkout.
G9 RED PROOF: the exact line `## [0.1.0] - 2026-08-20` counted 1x, then replaced by `## [0.1.0-broken] - 2026-08-20` in the worktree's CHANGELOG.md and nothing else → exit 1, exactly 3 failed / 6 passed, naming `test_the_declared_version_has_a_non_empty_section`, `test_this_repository_is_refused_for_no_reason_at_all` and `test_a_sound_release_exits_zero`. Reverted → exit 0, 9 passed, that worktree's porcelain EMPTY.
G10 with a 2040197 B file at the worktree's `dist/remedy-0.1.0-py3-none-any.whl`: `--tag v0.1.0 --ci-status success` → exit 0, stdout exactly `release v0.1.0 may proceed`, stderr empty; `--tag v9.9.9 --ci-status failure` → exit 1, stdout empty, exactly 2 stderr lines, both beginning `REFUSED: `, one naming CI and one the tag.
G11 ruff over the two new paths in the primary checkout → exit 0, EMPTY rule-code multiset. No base reading exists to compare against: both paths are ABSENT at 6f5a589a, which G7 measures. CONTROL in the worktree only, `import json` inserted after the 1x line `import argparse` → exit 1 naming F401; reverted → exit 0.
G12 exit 0, 160 passed for the four state readers, then exit 0, 42 passed for the canary. They did NOT overlap: the second process started 3.708 s after the first had ENDED.
G13 linear, every commit exactly one parent: 6f5a589a → 16889dd5 → 866d905d → b59fbd8f → 96483707 → 3b77cf19 → 8cdecc5b → 5bfdddfa; `git reflog` over this round shows only `commit:` entries. Insertions before C6: 489, 404, 16, 4, 24, 72, 91 — none over 500, and no DECISION F104 D1 exemption invoked.
G14 the path set before C6 is exactly the seven paths tabled above other than `.agent/handoff.md`. `pyproject.toml`, `hatch_build.py`, `packages/orchestration/release_gate.py` and `.github/workflows/ci.yml` are ABSENT from the range and all four EXIST at 6f5a589a, so the clause forbids something real. `.github/workflows/release.yml` is absent from the range AND at 6f5a589a — it is R16's work, said plainly so the clause does not read as a guard over a live file (R-0559).
G15 this file is 59 lines at HEAD, AT MOST 100 — no DECISION D15 overage is declared — and all seven mandated headings of docs/agents/handback_template.md are present, in the template's order.
G16 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. Nothing merged.

## Authored-text proofs

PLAN15, FIND0583, RECORD13, CHANGELOG, RUNNER and TESTS were each extracted programmatically by their one-line `<<<SLICE NAME>>>` / `<<<END NAME>>>` markers from the COMMITTED `.agent/authored/f086-r15.md` and applied byte-verbatim; none was retyped or edited. Each applied region byte-EQUALS its slice, verified disk-to-disk against the committed blob. Every sha256 is reported in full, at 64 characters, in the round report; none is written here in part.

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: no deviation. C0a, C0b, C1, C2, C3, C4, C5, C6 ran in the block's order, one commit each, none extra, none dropped, none reordered.
- The Verification section above is a per-gate SUMMARY, not a raw transcript. That departs from this template's "raw transcripts" wording and was ordered by this round's block step C6 as the R-0582 repair; the transcript lives in the round report, which no cap binds. No section is dropped.
- `Range` names the literal token `HEAD`, the R10-onward convention on this branch: a handoff cannot name the SHA of the commit that writes it.
- The worker wrote no verdict of its own anywhere. RECORD13, the R14 entry in the finding ledger, is the REVIEWER's text, applied byte-verbatim by C2.
- Nothing calls the release gate from production code yet: `scripts/release_gate_check.py` is called by its tests and, from R16, by a manual-trigger workflow. It is not executable, has no `[project.scripts]` entry and is imported by no production module — as the block ordered.

## Next

1. Re-read `.agent/STOP` from disk (Phase 1 rule 1).
2. Then run the Open PR Gate (Phase 1 rule 2): `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
