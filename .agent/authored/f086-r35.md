── STEP R35 — F086 Release capability ─────────────────────────
Goal:        Record R34's verdict in the ledger so it is not stranded, and leave
             the branch ready for the Open PR Gate with the pull request still
             open. No finding is registered and none is resolved this round.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record R34 · C3 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f086-r35.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. No source
             file, no test and no document changes this round. These paths are
             PRESENT at d56cadad and must stay untouched: `hatch_build.py`,
             `tests/test_packaging_smoke.py`, `docs/system/release-capability-v1.md`,
             `docs/roadmap/STATUS.md`, `README.md`, `pyproject.toml`,
             `.agent/context.md`, `.agent/candidates.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f086-r35.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f086-r35.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL to
   each other; the reviewer stated its expected digest when it delegated, and
   that digest cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. PLAN35 is a WHOLE-FILE replacement of
   `.agent/plan.md` and RECORD34 is an APPEND to `.agent/live_review.md`. The
   reviewer extracted this block's own slices programmatically and ran the
   containment test over them before emission; it reported no pair to classify,
   so no FROM count and no FROM-zero count is ordered anywhere below.
4. THE LEDGER APPEND IS BLANK-SEPARATED. RECORD34 is appended preceded by
   exactly one blank line (R-0578). Nothing already in that file is rewritten,
   reordered or deleted. NEITHER SET CHANGES this round: no `- R-` paragraph and
   no `Done:` paragraph is added, so the registered and resolved counts must both
   come back UNCHANGED, which G5 orders measured rather than assumed.
5. YOU NEVER WRITE A `Done:` PARAGRAPH, and this round has no `Landed:` line to
   write either — nothing is fixed here, only recorded.
6. THE PULL REQUEST IS NOT MERGED and not touched. #207 already exists for this
   branch; C3 is followed by `git push` only, which updates it. Do not run
   `gh pr merge`, `gh pr create`, `gh pr edit` or any force push. Its merge
   belongs to the next feature's Open PR Gate, which is not this round.
7. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
8. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
9. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion. The reviewer
   watches the runs this branch's pushes start; a conclusion cannot be known when
   the text that would carry it is written, which is why no slice below states
   one for any commit of this round.

<<<SLICE PLAN35
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and unmerged; the CI check on 665c45df, run 32405232165, is green —
the first green run this branch has had. It merges at the next feature's Open PR
Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R35: record R34's verdict in `.agent/live_review.md` so it is not stranded
(DECISION F085 D9). This round registers no finding, resolves none, and changes
no source file, test or document.

## Next Steps
1. THE OPEN PR GATE MERGES #207, per AGENTS.md, before any new branch is cut.
   The operator may merge it manually at any time instead.
2. R35'S OWN VERDICT IS RECORDED BY THE NEXT FEATURE'S FIRST REVIEWED ROUND,
   the way F085's closure candidates reached F086 R1. R35 does NOT claim the
   terminator carve-out: R-0583 gives that to the round creating the branch's
   pull request, which was R31, so the regress ends at the merge and not here.
3. F086 STAYS `[x]` IN THE LEDGER. Neither R-0598 nor R-0599 falsifies the
   closure's own claim, so each correction is a dated ledger entry and never a
   rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- A GREEN CI RUN IS NOT A WHEEL INSTALL. It proves the dev install and the suite,
  which is what R-0598 broke, and it proves neither risk above.
- R-0571 IS THE HOLE THIS ROUND ROUTES AROUND BY HAND rather than fixes: a last
  round whose verdict was written and one whose verdict was never written are
  indistinguishable on disk, and the fix edits files F086 does not own.
<<<END PLAN35

<<<SLICE RECORD34
Gate: R35 — the R34 entry. R34 PASSED with NO finding against its own work and none against its block. Every gate the R34 block ordered was RE-EXECUTED by the reviewer over `d2b83b0b..d56cadad` rather than read from the handback, and every one holds as written. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f086-r34.md`, the committed `.agent/authored/f086-r34.md` at `c3db3f8f` and the committed `.agent/last_block.md` at `f2854a40` are byte-EQUAL at sha256 8b6a657cbde58d2ecd57fddadc335d7af24a69b88b6527122108714e925c2c00 over 15233 B and 177 lines, and the two commits carry the identical git blob `5941b129`. THE PLAN LANDED AS AUTHORED: `.agent/plan.md` at `b7e373cb` byte-equals PLAN34 extracted programmatically from the committed block at sha256 7270a6b4e7be2d765c1c25633442aad488f6447dcbded9e4872519175efe0e44 over 2483 B and 43 lines, under the AGENTS.md cap, carrying `## Goal` once, `## Next Steps` once and `F086` twice. THE LEDGER APPEND HELD UNDER TWO INDEPENDENT EXTRACTIONS AND A NEGATIVE CONTROL, which is what R-0572 and R-0578 ask for: the pre-C2 blob at `b7e373cb` is a byte-exact PREFIX of the blob at `eaca4ed2`, its 2-line remainder equals a blank line followed by RECORD33 at sha256 88184b09435291de34f967a77033ac4dce2f35a139495275bc4e647e1a4e7692 over 3641 B with the blank separator PRESENT, a paragraph-level split of the whole post-commit blob independently yields RECORD33 as the last of its 225 paragraphs at sha256 2e625c2042172a92166d202c60dd1bdd64e918d16ef5eee7369485e6348737b9, and a remainder mutated at a single byte is REJECTED by both extractions rather than by neither. THE SETS DID NOT MOVE AND BOTH ENDS WERE MEASURED: registered 182, resolved 7, open 175 and `Landed:` 0 at `d2b83b0b`, and each of those four numbers identical at `eaca4ed2` — which is what a `Gate:` paragraph adding no `- R-` line and no `Done:` line must produce, and what constraint 4 of that block ordered measured rather than assumed. THE TWO SCANS RAN AND THE CONTROL PROVED THE FIRST OF THEM: with backtick-quoted spans deleted first, the unquoted word-boundary match on the four capital letters reads 0 over the two lines `eaca4ed2` ADDS, while the same extractor over `fd166295`'s four added lines to that same file reads 3, so the gate is not vacuous; `Gate: R` headers go 31 to 32, the only key occurring more than once is unchanged at both ends and is exactly `Gate: R19 — the R18 entry`, and `Gate: R34 — the R33 entry.` occurs once, sits last, and is followed by text beginning `R33 ` once its leading space is stripped. THE ROUND GATE WAS RE-RUN SERIALLY IN THE PRIMARY CHECKOUT, never two pytest processes at once: the four-file state-reader selection exited 0 at `160 passed` and the canary exited 0 at `42 passed`, each equal to the reading the R34 block records the reviewer taking at `d2b83b0b`. THE RANGE IS WHAT THE HANDBACK DECLARES: five `.agent/` paths over five single-parent commits, every `+/-` cell of the `## Commits` table byte-identical to `git diff --numstat` at 177/0, 75/78, 17/16 and 2/0 with the handback commit's own 23/23 correctly routed to the round report rather than claimed inside itself, a maximum insertion column of 177 under the 500 cap, every `git reflog` entry of the round reading `commit:`, each of the eight paths the Change section names as untouched present at `d2b83b0b` and absent from the range, zero marker lines in either target, and a handback of 55 lines carrying all seven mandated headings in the template's order under the 60-line cap. THE PERMANENT RECORD IT WROTE IS TRUE, which is the check a `Gate:` entry owes the entry below it: the reviewer re-measured every factual claim RECORD33 makes — the R33 transport digest 508110e0 over 18942 B and 180 lines, the `222a0205` plan digest fde90315 over 42 lines, the 181-to-182 and 6-to-7 set moves gaining exactly `R-0599` and `R-0598`, the 30-to-31 header count, the five-commit numstat series 180/0, 112/259, 17/17, 6/0 and 27/34, and the 55-line seven-heading handback — against disk at the SHAs that sentence names, and every one of them holds. R34 IS NOT A TERMINATOR and never claimed to be: R-0583 gives that carve-out to the round whose bundle creates the branch's pull request, which on this branch is R31, so this entry exists because DECISION F085 D9 requires it.
<<<END RECORD34

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f086-release-capability; `git status --porcelain`
   EMPTY after every commit and at the handback; `git worktree list` reports the
   primary checkout alone, because this round creates none. No reading is taken
   by overwriting a file in the primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f086-r35.md`, of `.agent/authored/f086-r35.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 PLAN. `.agent/plan.md` at C1 byte-equals PLAN35; report its sha256 and line
   count, that the count is under 50, and that `## Goal`, `## Next Steps` and
   `F086` all occur in it.
G4 LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
   PREFIX of the post-C2 blob, and the remainder is a blank line followed by
   RECORD34 — report the remainder's sha256 and line count and that the blank
   separator is present. Report it twice, by two INDEPENDENT extractions that
   must agree: the byte-level remainder above, and a paragraph-level split of the
   post-C2 blob whose LAST paragraph is RECORD34 (R-0572, R-0578). Run a NEGATIVE
   CONTROL — mutate one character of the expected remainder and confirm BOTH
   extractions reject it — and report both rejections.
G5 LEDGER SETS. With `^- R-\d+ — ` as registered and `^Done: R-\d+ — ` as
   resolved, report both counts plus open and `Landed:` at d56cadad and at C2.
   The reviewer measured 182 registered, 7 resolved, 175 open and 0 `Landed:` at
   d56cadad. Constraint 4 orders every one of those four numbers UNCHANGED at C2;
   report the measured pairs rather than the word unchanged.
G6 ITEM-20 SCAN. Over C2's ADDED lines only, delete backtick-quoted spans first,
   then report the count of `\bHEAD\b` — it must be 0. Run the SAME extractor
   over `fd166295`'s added lines to that file as a RED CONTROL and report that
   count too; the reviewer measured 3 there, and a control that does not read
   above 0 makes the gate worthless.
G7 ITEM-26 HEADER. Report how many lines begin `Gate: R` at d56cadad and at C2,
   which header keys occur more than once at each end, that
   `Gate: R35 — the R34 entry.` occurs 1x, that it is the LAST such header, and
   that the text following it begins `R34 ` once its leading space is stripped.
   The reviewer measured 32 headers at d56cadad, with exactly
   `Gate: R19 — the R18 entry` occurring more than once, and confirmed that
   `Gate: R35 — the R34 entry.` occurs there 0 times before this round writes it.
G8 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches no source file, so
   the four files that read that state live are the gate, plus the canary.
   Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   d56cadad and both in the primary checkout.
G9 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only d56cadad..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the eight paths the Change section names as untouched is PRESENT
   at d56cadad and absent from that range; that every commit in the range has one
   parent; that every `git reflog` entry of this round is `commit:`; and each
   commit's insertion column from `git diff --numstat`, every one under 500. Per
   checklist item 28 the same `+/-` cells appear in the handback's `## Commits`
   table and must be byte-identical to the tool's output there, which for a
   full-file rewrite is the numstat columns and never the file's line counts.
   C3's own cell cannot exist while C3 is being written, so it belongs to the
   round report, and so does the complete change set, which C3 completes.
G10 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2. Both
   counts must be 0.
G11 THE PUSH. After C3, `git push` and report its real output, then re-read
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   report it verbatim, stating that #207 is still OPEN and was not merged. Do NOT
   merge and do NOT wait on the CI run (constraint 9). C3's own insertion count
   and the push cannot appear inside C3, so they belong in the round report.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, at most 60
             lines or a DECISION D15 stated-cause line naming the real count and
             the mandated content that caused it. It carries the item-status
             table for the C0a..C3 bundle, the `## Commits` table G9 pins, and
             one LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as the Open PR Gate merging
             #207 — in that order — and states that R35 awaits review rather than
             claiming the terminator carve-out, which belongs to R31 alone
             (R-0583). The full transcripts go in the round report you return,
             never in the file. The handback also carries this Fortschritt line
             verbatim, because with no relay you never see the operator brief
             that would otherwise state it (R-0418):
             Fortschritt: ~100 % (F086 closed at R31 · R32 repaired the packaging
             guard · R33 recorded R-0598 resolved and R-0599 registered · R34
             recorded the R33 verdict · R35 records the R34 verdict) — Schätzung
──────────────────────────────────────────────────────────────
