# Handoff — F086 Release capability, R9 (T001 part (b): the packaging guard landed)

Branch feature/f086-release-capability, continued; no branch created, no PR opened.
Open findings 161 (163 registered, 2 resolved), both extractions agreeing. R-0580
registered, the R8 verdict recorded. Every gate G1–G16 returned its ordered value.

## Range

Review of 419fb683..HEAD

## Commits

### d0c5c259 docs(state): save the F086 R9 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r9.md | +467/-0 | C0a, `shutil.copyfile` of `.remedy-wt/f086-r9.md` |

### fa2940ba docs(state): mirror the R9 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +391/-305 | C0b, whole-file mirror of the COMMITTED C0a blob |

### 4411f89c docs(state): advance the plan to the F086 R9 round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-14 | C1, PLAN9 slice byte-verbatim, whole file |

### 1c065d88 chore(review): register R-0580 in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, FINDINGS3 EOF-append |

### 1d5909b9 chore(review): record the F086 R8 verdict in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3, RECORD7 EOF-append |

### f754228e feat(packaging): fail the wheel build when built UI assets are absent
| Path | +/- | Reason |
|---|---|---|
| hatch_build.py | +45/-0 | C4(a), HOOK slice byte-verbatim, new file |
| pyproject.toml | +5/-0 | C4(b), the single TOMLFROM occurrence replaced by TOMLTO |

### 6a5021e3 test(packaging): cover the UI asset guard and both resolver modes
| Path | +/- | Reason |
|---|---|---|
| tests/test_packaging_smoke.py | +73/-0 | C5, TESTS slice byte-verbatim, new file |

### C6, this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | a handoff cannot measure the commit writing it |

## External actions

- `git push origin feature/f086-release-capability` after C5 → `419fb683..6a5021e3`, ok.
- same push after C6 → in the round report.
- `git worktree add /home/decodeux/remedy-f086r9-check HEAD` → ok; removed + pruned.
- `git worktree add /home/decodeux/remedy-f086r9-basechk 419fb683` → ok; removed + pruned.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]` (G16).
- No PR created, edited or merged; no force-push, amend, rebase or reset.

## Verification

G1 `git status --porcelain` EMPTY; `git worktree list` 1 line; `.agent/STOP` absent, re-read
   from disk before C0a and at handback; branch feature/f086-release-capability.
G2 the three block copies byte-EQUAL: sha256 5e8c7518…, 28751 B, 467 lines.
G3 `.agent/plan.md` == PLAN9, sha256 d6e8c994…, 41 lines (< 50); holds `## Goal`,
   `## Next Steps`, `F086`.
G4 C2 pre 195960c1… is a byte-exact prefix of post 2a302418…, remainder == FINDINGS3
   e66ad5d9…; C3 pre 2a302418… prefix of post d1e461ac…, remainder == RECORD7 e74a6297….
G5 HEAD, BOTH extractions: 163 registered / 2 resolved / 0 duplicate / 0 unregistered
   resolutions / 0 `Landed:` / 161 open, registered id SETS EQUAL; added over the
   419fb683 set = `['R-0580']` under both. Control at 419fb683: both 162 / 2 / 160, EQUAL.
G6 `hatch_build.py` == HOOK, sha256 d5543cd6…, 45 lines; `tests/test_packaging_smoke.py`
   == TESTS, sha256 63780f12…, 73 lines; `git ls-tree 419fb683 -- <path>` EMPTY for both.
G7 TOMLFROM occurs 1x in the 419fb683 blob; that blob with the one occurrence replaced by
   TOMLTO and `pyproject.toml` at HEAD are both sha256 09cc3a83…, 5842 B — MATCH.
G8 `build --wheel --no-isolation`, worktrees OUTSIDE the repository:
   (a) HEAD + dist → exit 0, wheel, 417 members, 3 under `apps/ui/dist/`;
   (b) HEAD − dist → exit 1, NO wheel, error text contains `apps/ui/dist/index.html`;
   (c) base − dist → exit 0, wheel, 414 members, 0 UI — the RED CONTROL fires;
   (d) base + dist → exit 0, wheel, 417 members, 3 UI.
G9 `python3 -m pytest tests/test_packaging_smoke.py -q -rf`, primary → exit 0, 6 passed.
   Controls, out-of-repo worktree only: (i) the 1x resolver string one `.parent` shorter
   → exit 1, 2 failed 4 passed; (ii) `    if not index.is_file():` → `    if False:` →
   exit 1, 2 failed 4 passed; (iii) both reverted → exit 0, 6 passed, worktree PROVED
   restored (its `git status --porcelain` empty).
G10 the four state-reader suites, primary → exit 0, `160 passed in 19.98s`.
G11 `tests/cli/test_golden_path.py`, primary → exit 0, `42 passed in 20.48s`; begun only
   after G10 had ENDED — the two runs did not overlap.
G12 `python3 -m ruff check hatch_build.py tests/test_packaging_smoke.py` → exit 0,
   `All checks passed!`.
G13 insertions before C6: 467, 391, 13, 2, 2, 50, 73 — none over 500; C6 in the report.
G14 7 commits, each exactly 1 parent, linear 419fb683 → d0c5c259 → fa2940ba → 4411f89c →
   1c065d88 → 1d5909b9 → f754228e → 6a5021e3; reflog shows only `commit:` entries.
G15 `git diff --name-only 419fb683..HEAD` before C6 is exactly the seven paths tabled
   above. 0 paths under `docs/`, `scripts/`, `apps/` or `packages/`, all four of which
   EXIST at 419fb683 per `git ls-tree`.
G16 `[]` — no open PR; nothing merged.

## Authored-text proofs

All seven slices were extracted programmatically by their one-line markers from the
COMMITTED `.agent/authored/f086-r9.md` and applied byte-verbatim; that file is byte-equal
to `.remedy-wt/f086-r9.md` and to `.agent/last_block.md` (G2). Slice sha256 prefixes:
PLAN9 d6e8c994, FINDINGS3 e66ad5d9, RECORD7 e74a6297, HOOK d5543cd6, TESTS 63780f12,
TOMLFROM a59ed6f7, TOMLTO c1913c9e. 0 lines beginning `<<<SLICE ` or `<<<END ` reached
`.agent/plan.md`, `.agent/live_review.md`, `hatch_build.py`, `pyproject.toml` or
`tests/test_packaging_smoke.py`.

## Deviations & assumptions

Overage declared under AGENTS.md DECISION D15: this file is 127 lines against the 100-line
cap for a >5-commit round. Cause: the mandated per-commit tables for 8 commits plus the
transcript for 16 ordered gates, four of which (G5, G8, G9, G15) carry several independent
readings each. No section was dropped to meet the cap.
Commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 executed exactly as ordered — one commit
each, none dropped, added or reordered. No gate was red. No other deviation.
Assumption: `.remedy-wt/f086r9-pylib` (hatchling 1.32.0, build 1.5.0) was reused as the
block permits rather than re-installed.

## Next

The next session's first two actions, in order: (1) re-read `.agent/STOP` from disk
(Phase 1 rule 1); (2) run the Open PR Gate (Phase 1 rule 2). Then R10 — T002, the version
single-source and the build info behind `remedy --version` (DECISION F086 D2).
