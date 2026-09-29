# Handback — F041, session 1 end: round 4 reviewed PASS, T003 next

## Session

SESSION 1 of feature F041 · round 4 · rounds so far 4. The planner and reviewer of this session
merged pull request 294 (F286) at the Open PR Gate as `45c584e6`, claimed F041, and ran four
delegated rounds, every one PASS: round 1 the claim and T001's sanitized markdown pipeline, round 2
the artifact file route and R-1105's repair, round 3 T002's preview record, runner and command
line, and round 4 the door's preview pair, the server's preview worker and the gated view. This
file is written by the reviewer at the session's end and applied by a worker; it replaces round 4's
own handback, which stays in git history at `3c923d23`. The session ends at four rounds, below the
six-to-eight target, because the next slice is the cockpit's user interface, which needs the whole
design reference loaded and a rendered proof, and this session's context was past half spent after
four fat rounds whose reviewer had already made three authoring slips. Context self-assessment: past
half used, enough to write this handoff safely but not to author and review a user-interface round.

For the operator, in plain words: Remedy can now show a job's README as safe formatted text and
list its screenshots, over the cockpit's server, and it can start a job's project as a live
preview, check that the preview really answers before showing a link, stop it on request, stop it
by itself after fifteen minutes with nobody looking, and stop every preview when the cockpit's
server closes. What is still missing is the part a person sees: the panel in the cockpit that shows
the README, the screenshot gallery that opens a picture large, and the card with the start and stop
buttons. That is the next session's work, followed by one end-to-end run on a small real app and
the feature's closing sequence.

## Range

Review of `45c584e6`..`3c923d23`, every round reviewed; this handoff commit follows `3c923d23`.

## Commits

### (this commit) F041 S1 end: rewrite handoff at the end of session 1
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-s1-handoff.md | new | the reviewer's handoff text, copied verbatim |
| .agent/handoff.md | rewrite | the same bytes, replacing round 4's handback |

The four rounds' own commit tables are in their handbacks at `e1dc49dd`, `8130599a`, `468b3a36` and
`3c923d23`, and in the gate entries of `.agent/live_review.md`.

## External actions

This session's reviewer ran `gh pr merge 294 --merge --delete-branch` after hosted CI run
36515276903 ended `success` on both jobs, then `git checkout main` and `git pull --ff-only`, and the
round 1 worker cut `feature/f041-artifact-preview` from `45c584e6`. Every round's worker pushed its
own commits; no pull request is open. The worker applying this file pushes it.

## Verification

Round 4, re-run by the reviewer at `3c923d23`: the round's selection, serially,
`3454 passed, 1 skipped` at exit 0, the skip being the D12 quarantine of
`tests/test_agent_tooling.py`; `python3 -m apps.cli.main integrity check --json`, six checks pass at
`fail_count` 0; the records, wiring and test files equal to the reviewer's simulation tree byte for
byte; the worker's mutation tool in a disposable worktree at `3c923d23`,
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` over eight mutations. Rounds 1 to 3 are recorded
in their gate entries.

## Authored-text proofs

This file is the reviewer's text; the worker applying it compares `.agent/handoff.md` with
`.agent/authored/f041-s1-handoff.md` byte for byte at the commit that writes both.

## Deviations & assumptions

None in round 4. Across the session, each declared and recorded in its round's gate entry or in
`.agent/prose_slips.md`: round 1's C3 stop clause was the reviewer's sizing error and needed an
amendment splitting C3; round 3's worker wrote a placeholder command in a docstring, which its own
gate caught, and fixed it in one added commit.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The first commit of the next round books round 4's gate entry, whose text the reviewer of this
   session wrote and is carried here verbatim, below this list.
3. T003, the cockpit's preview panel, in one or two rounds: the README fragment, the screenshot
   grid and lightbox, and the app card, per `docs/ui/design_reference/` (`component_spec.md`
   lines 108 to 120 describe the DetailPopover's "Open app" entry and the glass sheet it opens;
   nothing there describes a lightbox, so its deviations go to `assumption_log.md`). Measured by
   this session: `apps/ui/src` has no `dangerouslySetInnerHTML`, so the one site that inserts the
   server's sanitized fragment needs a contract test pinning that it is the only one; the README's
   own relative image paths are kept by the sanitizer but the file route serves only `README.md`
   and `captures/<name>`, so the panel decides what a README image that is not a capture shows;
   the card reads `GET /api/jobs/<id>/preview` (the read counts as a viewer) and sends
   `job.preview-start` and `job.preview-stop` through the write door; the result tour's anchor
   kinds are node, diff, evidence and command, and T5_F036.md reserves a preview anchor for this
   feature; `components/graph/evidencePanel.ts` `EVIDENCE_TABS` is the closest host for an
   artifacts tab.
4. The end-to-end run on a fixture app (open, live link answers, idle, stopped, state truthful),
   then the closure sequence: the one full-suite run, the evidence and the package, the close.

Open findings: 0. Operator questions open: 1 (the empty-paydown question, unchanged).

Gate entry for round 4, to be appended to `.agent/live_review.md` verbatim by the next round's first
commit:

Gate: F041 R4 — the F041 round 4 entry, T002 through the door: the booking of round 3, DECISION F041 D4, the door's preview pair, `preview_worker.py` with its revalidation and idle stop, the gated `preview` view and the `preview.idle_ttl_seconds` key. VERDICT PASS. Re-derived over `468b3a36`..`3c923d23` by the planner and reviewer of F041's first session, whose own runs produced every reading below. THE RANGE IS 8 COMMITS, each single-parent and each under the 500-line cap by `git show --numstat`: `87bb46a4` 384, `fcb89507` 297, `6b151ad3` 217, `09d38e04` 19, `1c728743` 428, `ed5c91c6` 441, `332e36db` 206 and `3c923d23` 163; the worker declared no deviation, after a first delegation that ended on a server error before writing anything. THE TRANSPORT PROOF: the block and every payload copy equal the reviewer's originals byte for byte, and at `3c923d23` the ledger, the decisions, the wiring files and the four test files equal the reviewer's simulation tree byte for byte. THE CODE: the reviewer read `preview_worker.py` and the `ui_server.py` diff of `1c728743` whole against D4 and the block's S1 to S3. THE TESTS: the round's selection read `3454 passed, 1 skipped` at exit 0 on the reviewer's own serial run at `3c923d23`, the skip being the D12 quarantine; all six `integrity check` checks read pass. THE RED PROOFS: the worker's tool, run by the reviewer in a disposable worktree at `3c923d23`, caught all eight mutations with byte-identical restores and green controls.
