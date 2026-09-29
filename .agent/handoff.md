# Handback — F041 round 5: T003's results panel, all gates green

## Session

SESSION 2 of feature F041 · round 5 · rounds so far 5. Context self-assessment: after finishing
G5's mutation run and the render's own red probe, roughly a third of the session's context budget
remained — enough to write this handoff carefully and push, not enough to start a sixth round.

## Range

Review of `d735c0587`..`45082a7ec`, this handoff commit follows `45082a7ec`.

## Commits

### bd1ea3ac2 F041 R5 C1a: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r5-assumption_line.md | +1/-0 | copy of the payload, byte for byte |
| .agent/authored/f041-r5-block.md | +400/-0 | copy of this round's block, byte for byte |
| .agent/authored/f041-r5-plan.md | +28/-0 | copy of the plan.md payload, byte for byte |

### 9ca8e6b4f F041 R5 C1b: copy round 5 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r5-records.diff | +28/-0 | copy of the records diff payload, byte for byte |

### 49c81c38b F041 R5 C2: book round 4, record D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10/-0 | `git apply` of records.diff: DECISION F041 D5 |
| .agent/live_review.md | +2/-0 | `git apply` of records.diff: round 4's gate entry |
| .agent/plan.md | +7/-7 | rewritten to the plan.md payload |

### 4100e8d77 F041 R5 C3a: decide what the results panel shows
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/artifactPreview.ts | +347/-0 | S1: the two decoders, the three paths, `readmeCockpitHtml`, `captureCaption`, `lightboxIndexAfter`, the poll delay and `previewCardView` |

### fcb927e57 F041 R5 C3b: read its two views and pin the pure rules with tests
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/artifactPreview.test.ts | +317/-0 | S6: whole-shape literal tests for both decoders, the three paths, `readmeCockpitHtml`, `captureCaption`, `lightboxIndexAfter`, the poll delay and `previewCardView` |
| apps/ui/src/api/remedyApi.ts | +41/-0 | S3: `loadArtifactsView` and `loadPreviewView`, directly after the tour door's section |

### b882360fb F041 R5 C4: send the preview pair through the door
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/previewSend.ts | +175/-0 | S2: the preview send, composing `pauseSend.ts`'s `submitPauseSendRequest` and `PauseSendDeps` |
| apps/ui/src/api/previewSend.test.ts | +161/-0 | S6: every status/outcome of `describePreviewSendResult` for both commands, and `sendPreviewCommand`'s four fakes |

### 984ad729c F041 R5 C5: show the README, the screenshots and the app card in a panel
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/artifacts/AppPreviewCard.tsx | +85/-0 | S4: the app card, one timer keyed on `[jobId, serverToken, visible, tick]` |
| apps/ui/src/components/artifacts/ArtifactLightbox.module.css | +58/-0 | S4: the tour overlay's backdrop/card rules, the picture's max-height |
| apps/ui/src/components/artifacts/ArtifactLightbox.tsx | +87/-0 | S4: the lightbox, portaled, arrow keys and Escape |
| apps/ui/src/components/artifacts/ArtifactsPanel.module.css | +104/-0 | S4: the panel's dock, the grid, reused by the app card |
| apps/ui/src/components/artifacts/ArtifactsPanel.tsx | +145/-0 | S4: the panel, the one `dangerouslySetInnerHTML` site |

### a0728b05a F041 R5 C6: open the results panel from the right panel
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/artifactPreview.ts | +7/-2 | correction (declared below): the `readmeCockpitHtml` placeholder now uses a printable-ASCII marker instead of a NUL-delimited one, after eslint's `no-control-regex` caught the control character in the self-review loop |
| apps/ui/src/components/panels/RightLivePanel.tsx | +4/-1 | S5: `onOpenResults` prop and the Results button, directly after Story |
| apps/ui/src/components/shell/RemedyShell.tsx | +10/-1 | S5: `resultsOpen` state, `onOpenResults` passed to `RightLivePanel`, `ArtifactsPanel` mounted outside `<main>` |
| docs/ui/design_reference/assumption_log.md | +1/-0 | the assumption_line.md payload, appended byte for byte |

### 23aab7b6c F041 R5 C7: pin the results panel's seams
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_artifact_preview.py | +128/-0 | S6: the ten seam assertions over comment-stripped source |

### 3ea142996 F041 R5 C8a: drive the results panel headless over CDP
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r5-render_drive.mjs | +388/-0 | S7: the eight checks C-a to C-h over CDP |

### 97231f63c F041 R5 C8b: build, serve and render the results panel headless, and record the run
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r5-render.txt | +32/-0 | the harness's whole output, 8 of 8 checks passing |
| .agent/authored/f041-r5-render_index.html | +11/-0 | S7: the harness page |
| .agent/authored/f041-r5-render_main.tsx | +153/-0 | S7: the `window.fetch` stand-in and the real `ArtifactsPanel` mount |
| .agent/authored/f041-r5-render_measure.py | +215/-0 | S7: build, fixture PNG, serve, launch Chrome, drive, teardown |
| .agent/authored/f041-r5-render_vite.config.mjs | +28/-0 | S7: the scratch vite config |

### fea7ba7b6 F041 R5 C8c: pin the two read doors with a fake fetcher
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/artifactPreview.test.ts | +51/-0 | correction (declared below): `loadArtifactsView`/`loadPreviewView` covered with a fake fetcher, the pattern `ownership.test.ts`/`resultTour.test.ts` use for `remedyApi.ts`'s own doors |

### 45082a7ec F041 R5 C9: add the round 5 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r5-mutations.py | +277/-0 | the 13 mutations m1-m13, two runners (vitest, pytest) |

## External actions

`git worktree add --detach .remedy-wt/f041-r5-mut 45082a7ec` (G5's disposable worktree); a
`os.symlink` from that worktree's `apps/ui/node_modules` to the primary's, then removed with the
worktree; `git worktree remove --force .remedy-wt/f041-r5-mut` and `git worktree prune` after G5.
`git push origin feature/f041-artifact-preview` after this commit (outcome reported by the worker
applying this handback in its own reply, since this file cannot record a push that follows it).
No `gh pr` command of any kind: no PR is created or touched this round.

## Verification

G1 TRANSPORT — payload readings (measured against the PAYLOADS table, all matched):
`records.diff` 28 lines / 10389 bytes / `a59a03bc914e2d552d3040364ab4b0b84da9b77bfceedc7149d6bed0ad6abdff`;
`plan.md` 28 lines / 975 bytes / `46db78d7fe1e8af3fdca6528929b695b46b0cbbd51cb6e5ecf612279e0b67b81`;
`assumption_line.md` 1 line / 1051 bytes / `27e6b13c17b7990c07054ded3ae957f339f8947cbb6bde47d4a8dcd98a463dd8`.
Each `.agent/authored/f041-r5-*` payload copy, read back with `git show <commit>:<path>`, is
sha256-identical to its source (block copy against `.remedy-wt/f041-r5/block.md`, all four
`match=True`). The assumption log at C6 (`a0728b05a`) is byte-identical to `d735c0587`'s bytes
(27315) followed by `assumption_line.md`'s (1051) = 28366 bytes, sha256
`fb2b87f1ed3d85524d82252465acaf2b5812d4f37eb4d484fe908bf7a87df12f`, matching G2's table exactly.
`git apply --check` on records.diff: real exit 0; the real `git apply`: real exit 0.

G2 THE RECORDS — at C2 (`49c81c38b`): `.agent/decisions.md` 2467439 bytes,
`f5e1d5e444f22d5fad3961127efc4895322a885fbf9b650ae21243b5c305eabb`, match True;
`.agent/live_review.md` 304029 bytes, `2b53622128fab38cf5c5044e92a446c8aa6e6eba5eefbdc095c8c0ea539d8bb9`,
match True; `.agent/plan.md` 975 bytes, `46db78d7fe1e8af3fdca6528929b695b46b0cbbd51cb6e5ecf612279e0b67b81`,
match True. `open_finding_ids` over `.agent/live_review.md`'s TEXT: `[]` at `d735c0587` and `[]` at
`49c81c38b`, matching the reviewer's `[]`/`[]`. `git diff --name-only 9ca8e6b4f 49c81c38b`:
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — exactly the table's three paths.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_artifact_preview.py
.agent/authored/f041-r5-render_measure.py .agent/authored/f041-r5-mutations.py`: real exit 0,
"All checks passed!". The whole of `artifactPreview.ts`, the card's effect and click handler, the
lightbox's keydown listener, the panel's README block, and the changed lines of `remedyApi.ts`,
`RightLivePanel.tsx` and `RemedyShell.tsx` are quoted in the worker's chat reply to the delegating
message (this file summarizes rather than repeats ~350 lines of source; every quoted block there
is read verbatim from the commits named above).

G4 THE TESTS AND THE RENDER — at C9 (`45082a7ec`), serially:
- `pytest` selection (tests/ui_contracts, test_preview_commands.py, test_artifacts_route.py,
  test_dashboard_contract.py, test_import_reachability.py, test_no_orphan_modules.py, tests/docs,
  test_golden_path.py): `1521 passed, 4 skipped` at real exit 0. The four skips are exactly the D3
  quarantine nodes of `test_graph_architecture.py` (2) and `test_ux_quality.py` (2). `--collect-only
  -q` on `tests/ui_contracts/test_artifact_preview.py` alone: 10 nodes. `1447 + 64 + 10 = 1521`,
  matching exactly.
- `vitest run --root apps/ui`: `93 passed | 1 skipped (94)` test files, `1905 passed | 5 skipped
  (1910)` tests, real exit 0. `1831 + 74 = 1905`; the two new files hold 59 (`artifactPreview.test.ts`)
  + 15 (`previewSend.test.ts`) = 74 tests, matching exactly.
- `python3 -m apps.cli.main integrity check --json`: all six checks `"status": "pass"`,
  `"fail_count": 0`, `"ok": true`, real exit 0.
- `python3 .agent/authored/f041-r5-render_measure.py /home/decodeux/Repos/remedy`: real exit 0,
  `RENDER: 8 of 8 checks pass` (every C-a..C-h line `PASS`), saved whole to
  `.agent/authored/f041-r5-render.txt` (a second confirmatory run at C9 also passed 8 of 8, with
  different pids and build milliseconds only — not re-committed, since those two numbers are the
  only difference and neither is a count or a hash this round's gates read). Afterward
  `.remedy-wt/f041-render-run` was gone and `git status --porcelain` was empty. Screenshot:
  `.remedy-wt/f041-r5-worker/render-results.png`, 323045 bytes.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f041-r5-mut 45082a7ec`, then
`.agent/authored/f041-r5-mutations.py` run against it: `control (first) vitest: exit=0 failed=0`,
`control (first) pytest: exit=0 failed=0`; all 13 mutations m1-m13 `caught=True` with
`restored byte-identical: True` after each; `control (last) vitest: exit=0 failed=0`,
`control (last) pytest: exit=0 failed=0`; `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, real
exit 0. THE RENDER'S OWN RED PROBE: `apps/ui/node_modules` symlinked into the worktree (a stray
real `node_modules/.vite` cache directory the mutation tool's own vitest runs had created there
was removed first, since a real directory there would have shadowed the intended symlink); the
harness run UNMUTATED on the worktree printed `RENDER: 8 of 8 checks pass` at real exit 0; m3
alone applied, then `python3 .agent/authored/f041-r5-render_measure.py
/home/decodeux/Repos/remedy/.remedy-wt/f041-r5-mut` printed `FAILED C-d ...` with
`"prematureLink":true` and `RENDER: 7 of 8 checks pass` at real exit 1 — the required FAIL and
non-zero exit; the file was then restored byte-identical to the primary's. `git worktree remove
--force .remedy-wt/f041-r5-mut` and `git worktree prune`: `git worktree list | wc -l` read 61
(equal to the step 4 reading) and `git status --porcelain` was empty.

## Authored-text proofs

Every `.agent/authored/f041-r5-*` payload copy (block, plan.md, assumption_line.md, records.diff)
is sha256-identical, read back from the commit that added it, to its source under
`.remedy-wt/f041-r5-payloads/` or `.remedy-wt/f041-r5/block.md` — see G1 above. `records.diff`
applied cleanly with `git apply` (real exit 0 on both `--check` and the real apply). The
assumption log's appended line is byte-identical to `assumption_line.md`. No other reviewer text
was applied this round — S1 to S7's production code, its tests, the render harness and the
mutation tool are all worker-authored per the block's ROLE AND AUTHORITY.

## Deviations & assumptions

1. C3 was split into **C3a** (`apps/ui/src/api/artifactPreview.ts`, 347 insertions) and **C3b**
   (`artifactPreview.test.ts` + the `remedyApi.ts` door additions, 358 insertions), because the
   combined diff (705 insertions) would have exceeded the 500-line cap (block constraint 2).
2. C6 additionally carries a 7/-2 correction to `apps/ui/src/api/artifactPreview.ts`:
   `readmeCockpitHtml`'s internal placeholder marker was originally NUL-delimited
   (`\u0000<n>\u0000`), which eslint's `no-control-regex` rule flagged as an error in
   `tests/ui_contracts/test_ui_lint.py` during the self-review loop before this commit. Replaced
   with a printable-ASCII marker (`@@artifact-image-<n>@@`) with identical behaviour; all 59
   `artifactPreview.test.ts` cases were re-run green before the commit.
3. C8 was split into **C8a** (`f041-r5-render_drive.mjs`, 388 insertions) and **C8b** (the
   remaining four S7 files plus `f041-r5-render.txt`, 439 insertions), for the same 500-line
   reason (combined would have been 827).
4. **C8c**, a commit the original bundle did not name, was added after C8b: S6 asks that
   `loadArtifactsView` and `loadPreviewView` be covered "with a fake fetcher (the path asked, the
   decoded answer, a throw, a refused payload)" — the pattern this codebase already uses for
   `remedyApi.ts`'s own doors (`ownership.test.ts` tests `loadOwnershipView`, `resultTour.test.ts`
   tests `loadTourView`, neither in `remedyApi.test.ts` itself). C3b's `artifactPreview.test.ts`
   landed without this coverage; found during this worker's own pre-G4 review of S6 against the
   committed test file, and corrected in a new commit (51 insertions) rather than amended into
   C3b, per AGENTS.md's "never amend, create a new commit" rule. This is a scope addition to the
   block's ordered sequence, declared here per the handback template's instruction that any
   departure from the ordered commit sequence belongs in this section even when correct.
5. G4's render harness was run twice at C9 for this handback: once whose output is the committed
   `.agent/authored/f041-r5-render.txt`, and once more as the "official" G4 reading reported above.
   Both printed `RENDER: 8 of 8 checks pass` at exit 0; the only bytes that differed between the
   two runs were the vite build's own elapsed milliseconds and the two subprocess pids, so the
   second run's output was not re-committed (`git checkout --` restored the committed file) to
   avoid churn over numbers no gate reads.
6. No test this round wrote was found wrong; no existing test went red at any point.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 5 (this handback).
3. The result tour's preview anchor and the end-to-end run on a fixture app: open, the live link
   answers, idle, stopped, the state truthful.
4. The closure sequence: the one full-suite run, the evidence, the close.

Open findings: 0. Operator questions open: 1.
