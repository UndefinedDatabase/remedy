# Handback — F086 Release capability, R10 (T002: the version command)

Branch `feature/f086-release-capability`, pushed, unmerged, no PR. R10 registers
no finding; the open set stays at 161.

## Range

Review of e7c219cc..HEAD.

## Commits

### 4759f699 chore(state): save the F086 R10 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r10.md | +490/-0 | C0a, block saved byte-verbatim |

### 555bd335 chore(state): mirror the F086 R10 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +339/-316 | C0b, mirror of the COMMITTED C0a file |

### a36c28b9 docs(state): advance the plan to the F086 R10 step
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-8 | C1, whole file := PLAN10 slice |

### 308e6a28 chore(review): record the F086 R9 verdict in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, RECORD8 EOF-append; registers no id |

### 08a61a13 feat(cli): report version and build info behind a version flag
| Path | +/- | Reason |
|---|---|---|
| apps/cli/version_report.py | +67/-0 | C3a, VERSIONMOD: metadata readers, renderer, flag handler |
| apps/cli/grouped.py | +7/-0 | C3b, PAIRFROM→PAIRTO: called before the help pre-scan |

### 8fd0f701 test(cli): pin both version modes for the version flag
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_version_report.py | +83/-0 | C4, TESTMOD: installed and checkout modes |

### (this commit) docs(state): write the F086 R10 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C5; a handoff cannot table the commit that writes it (R-0149). Its insertion count and the post-C5 path set are in the round report |

## External actions

- `git push -u origin feature/f086-release-capability` after C4 → `e7c219cc..8fd0f701`, ok.
- `git push` after C5 → in the round report.
- `git worktree add /home/decodeux/remedy-f086r10-check HEAD` → ok; removed + pruned;
  `git worktree list` back to 1 line, directory gone.
- No PR created, edited or merged.

## Verification

G1 `git status --porcelain` EMPTY; `git worktree list` 1 line; `.agent/STOP` absent,
   re-read from disk before C0a and again at the handback; branch as named.
G2 scratchpad, committed `.agent/authored/f086-r10.md`, committed `.agent/last_block.md`
   byte-EQUAL: sha256 769c36fe…a35a2710, 28100 B, 490 lines.
G3 `.agent/plan.md` == PLAN10: sha256 25eb0de8…7d295ea6, 45 lines (<50); holds `## Goal`,
   `## Next Steps`, `F086`.
G4 pre-C2 blob a byte-exact PREFIX; remainder == RECORD8, sha256 40f25eed…b1671d12, 3098 B.
G5 BOTH extractions AGREE at HEAD: 163 registered / 2 resolved / 0 duplicates /
   0 unregistered resolutions / 0 `Landed:` / 161 open, registered SETS equal, symmetric
   difference vs `e7c219cc` = `[]`. Control: the same extractor reads `['R-0580']` added
   across `419fb683..e7c219cc` under both.
G6 `apps/cli/version_report.py` == VERSIONMOD, sha256 3985d089…d4938543, 67 lines;
   `tests/cli/test_version_report.py` == TESTMOD, sha256 a8caed7b…b032dd34, 83 lines;
   `git ls-tree e7c219cc` EMPTY for both, so NEW is measured.
G7 PAIRFROM 1x in the `e7c219cc` blob; base-with-replacement and HEAD both sha256
   31b11380d9ad99df9e479fa3f8e292181b69070066ad1aca342f42480fc88fc0 — MATCH.
G8 `python3 -m apps.cli.grouped --version` → exit 0; `remedy   0.1.0` / `build    dev` /
   `python   3.10.12` / `platform Linux-6.17.9-76061709-generic-x86_64-with-glibc2.35`.
   `build` reads `dev`: nothing writes REVISION yet, and no revision was invented.
G9 `pytest tests/cli/test_version_report.py -q -rf` primary → exit 0, 8 passed. Red
   controls, out-of-repo worktree only, each byte string counted 1x first: (i) the
   two-line `embedded is None` guard deleted → exit 1, 4 failed 4 passed; (ii) reverted,
   `if handle_version_flag(argv):` → `if False:` → exit 1, 2 failed 6 passed;
   (iii) both reverted → exit 0, 8 passed, worktree `git status --porcelain` EMPTY.
G10 the four CLI reader suites `-q -rf` primary → exit 0, 601 passed.
G11 the four `.agent/` state-reader suites `-q -rf` primary → exit 0, 160 passed.
G12 `pytest tests/cli/test_golden_path.py -q` primary → exit 0, 42 passed, started only
   after G11 had ENDED; no two suite runs overlapped this round.
G13 `ruff check` on the three touched paths from the repo root → exit 0, All checks passed.
G14 insertions before C5: 490, 339, 12, 2, 74, 83 — none over 500.
G15 six commits, each exactly ONE parent, linear from `e7c219cc`; `git reflog` over this
   round shows only `commit:` entries — no amend, rebase, reset or force-push.
G16 pre-C5 path set is exactly constraint 2 minus `.agent/handoff.md`; `pyproject.toml`,
   `hatch_build.py` and every path under `docs/`, `scripts/`, `packages/` ABSENT, and all
   five confirmed to EXIST at `e7c219cc` by `git ls-tree`.
G17 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

All five slices were extracted programmatically by their one-line markers from the
COMMITTED `.agent/authored/f086-r10.md`, never retyped: PLAN10 (G3), RECORD8 (G4),
VERSIONMOD and TESTMOD (G6), PAIRFROM/PAIRTO by ordered equality (G7). 0 lines
beginning `<<<SLICE ` or `<<<END ` reached any target file.

## Deviations & assumptions

Sequence C0a, C0b, C1, C2, C3, C4, C5 executed exactly: one commit each, none added,
dropped or reordered. Deviations, declared: this file stands at 113 lines against the
100-line cap, an overage under AGENTS.md DECISION D15 caused by the mandated per-commit
tables for 7 commits and the mandated Verification transcript for 17 gates. No section
was dropped to meet the cap.

## Next

The next session's first two actions, in this order: re-read `.agent/STOP` from disk
(Phase 1 rule 1), then run the Open PR Gate (Phase 1 rule 2).
