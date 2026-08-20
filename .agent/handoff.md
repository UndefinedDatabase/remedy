## Range

Review of 8fe709a8..d420e8e5 (C0a–C5), plus C6 which writes this file and C7 which appends VERDICT.

## Commits

| Commit | Path | +/- | Reason |
|---|---|---|---|
| b674a9cf C0a | `.agent/authored/f086-r26.md` | +388/-0 | the R26 block saved as authored text |
| 5329860b C0b | `.agent/last_block.md` | +255/-196 | the same bytes mirrored |
| 8c199616 C1 | `.agent/plan.md` | +17/-17 | PLAN26 — the ledger advanced to R26 |
| 7d06c6ef C2 | `.agent/live_review.md` | +4/-0 | FIND0593 and RECORD25 appended |
| 3beba069 C3 | `packages/orchestration/release_gate.py` | +5/-3 | GATE pair — "nothing calls it" retired |
| e9e01ab7 C4 | `pyproject.toml` | +3/-1 | TOML pair — "is still owed" retired |
| d420e8e5 C5 | `docs/roadmap/features/T2_F086.md` | +23/-0 | BUILT pair — `## Built State` appended |
| C6, C7 | `.agent/handoff.md` | round report | this file, then VERDICT appended; §3 item 14 forbids self-measurement |

Every `+/-` cell above is read out of `git diff --numstat <sha>^ <sha>` per constraint 9, never from a file's line count.

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> `[]`. Nothing created, nothing merged.
`git push` of `feature/f086-release-capability`, once, after C7 — outcome in the round report.

## Verification

G1 HYGIENE — `.agent/STOP` absent on both readings; branch `feature/f086-release-capability`; `git status --porcelain` empty at every commit and at the handback; `git worktree list` one line throughout.
G2 TRANSPORT — scratchpad, `.agent/authored/f086-r26.md` at b674a9cf and `.agent/last_block.md` at 5329860b all three byte-EQUAL: sha256 3a01faf9a7b183650e1ef6ec97d505644db511cd80a4586cfba44b149465e3a2, 29011 B, 388 lines.
G3 PLAN — `.agent/plan.md` at 8c199616 byte-equal to PLAN26 extracted from the committed C0a, sha256 5d0503dd3fecf37d9d5c1afbc74d5251410dca45043b0e5486420960f9795d10, 45 lines (under the AGENTS.md 50), carrying `## Goal`, `## Next Steps` and `F086`.
G4 LEDGER APPEND — the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; the 4-line remainder equals blank + FIND0593 + blank + RECORD25 at sha256 cf4de522b14a06365e6bf887fbebe8f202531ea2aedf8d129084b65903b94f26, 6137 B.
G5 LEDGER SETS — both independent extractions AGREE at each end: 175 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 171 open at 8fe709a8, and 176 / 4 / 0 / 0 / 0 / 172 at C2; the resolved set is EQUAL, the registered set gains exactly `R-0593`; the control over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`.
G6 ITEM-20 SCAN — backtick-quoted spans deleted first, `\bHEAD\b` reads 0 over C2's 4 added lines; the RED CONTROL over `fd166295`'s added lines reads 3, so the extractor bites.
G7 ITEM-26 HEADER CHECK — 22 headers at 8fe709a8, 23 at C2; the duplicated-header set is UNCHANGED and is exactly `Gate: R19 — the R18 entry.` (constraint 3 forbids repairing it); `Gate: R26 — the R25 entry.` occurs 1x, is the LAST such header, and the text after it begins ` R25 PASSED with NO finding.`
G8 THE THREE PAIRS — GATE and TOML are REWRITES: `TO contains FROM: False`, FROM 0x and TO 1x at C3 and C4. BUILT is an APPEND: `TO contains FROM: True`, FROM 1x at 8fe709a8 and 1x at C5, no FROM-zero attempted. All three satisfy the ORDERED EQUALITY against the 8fe709a8 blob. sha256/lines at their commits: a3745e34…/84, f97b11b7…/158, e0237d1c…/90.
G9 THE CLAIM IS TRUE AT 8fe709a8 — `scripts/release_gate_check.py` exists and imports `refuse_release`; `.github/workflows/release.yml` exists and its only trigger key is `workflow_dispatch`; `hatch_build.py` exists and `hooks.custom.path` is `hatch_build.py`; 8cdecc5b, 25336879 and f754228e are ancestors of 8fe709a8, and 3b738f6d is an ancestor of f754228e.
G10 NO MARKER LEAKED — marker LINES beginning `<<<SLICE ` or `<<<END ` count 0 in each of `.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/release_gate.py`, `pyproject.toml` and `docs/roadmap/features/T2_F086.md` at C6; the `.agent/handoff.md` reading is post-C7 and is in the round report.
G11 PARSE, TOML AND LINT — the import prints `packages.orchestration.release_gate` at exit 0; `pyproject.toml` at C4 loads under `tomli` still carrying `hooks.custom.path == "hatch_build.py"` and `wheel.artifacts == ["apps/ui/dist/**"]`; the ruff rule-code MULTISET over the touched file is EMPTY at 8fe709a8 and EMPTY at C3 — UNCHANGED, both `All checks passed!` at exit 0.
G12 SUITES, SERIALLY — the packaging and release set: 45 passed, 0 skipped, exit 0; then the canary `tests/cli/test_golden_path.py`: 42 passed, exit 0. `tests/test_install_smoke.py` is NOT in this selection and its install coverage remains zero, which this round neither changes nor implies.
G13 CHANGE SET AND HISTORY — the range's 7 paths equal the Change list with no path on either side alone; all 7 forbidden paths are PRESENT at 8fe709a8 and untouched; 7 commits, each at exactly one parent; every round `git reflog` entry is `commit:`; every measurable `+/-` cell above is byte-identical to its numstat pair, largest insertion 388, under the 500 cap (DECISION F104 D1).
G14 THE HANDBACK — this file's `wc -l` at C6 and again at C7 is measured against the bound the block's CONSTRAINT 8 states for each; both readings are self-referential here and go to the round report (§3 item 14), as does the prefix-and-remainder equality against VERDICT. All seven mandated headings of docs/agents/handback_template.md are present, in the template's order, none dropped.
G15 OPEN PR GATE — re-read at the handback: `[]`.

## Authored-text proofs

PLAN26, FIND0593, RECORD25, GATEFROM/GATETO, TOMLFROM/TOMLTO, BUILTFROM/BUILTTO and VERDICT were extracted PROGRAMMATICALLY from the committed C0a at b674a9cf and applied byte-verbatim; G2, G3, G4 and G8 above are the disk-to-disk results. No slice was retyped, rewrapped or reformatted, and no marker line reached a target file.

## Deviations & assumptions

None. The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7 was executed exactly as the block labels it — no extra commit, no dropped commit, no reordering — and no slice was edited.

## Next

The planner/reviewer reviews `8fe709a8..HEAD` and records R26's verdict as `Gate: R27 — the R26 entry.`; the packaging ist-doc under `docs/system/` with its `docs/README.md` row is the next round's first work, and closure follows it.
