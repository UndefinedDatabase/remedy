── STEP R34 — F086 Release capability ─────────────────────────
Goal:        Record R33's verdict in the ledger so it is not stranded, and hand
             the branch to the next session with the pull request still open.
             No finding is registered and none is resolved this round.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record R33 · C3 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f086-r34.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. No source
             file, no test and no document changes this round. These paths are
             PRESENT at d2b83b0b and must stay untouched: `hatch_build.py`,
             `tests/test_packaging_smoke.py`, `docs/system/release-capability-v1.md`,
             `docs/roadmap/STATUS.md`, `README.md`, `pyproject.toml`,
             `.agent/context.md`, `.agent/candidates.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f086-r34.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f086-r34.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL to
   each other; the reviewer stated its expected digest when it delegated, and
   that digest cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. PLAN34 is a WHOLE-FILE replacement of
   `.agent/plan.md` and RECORD33 is an APPEND to `.agent/live_review.md`. The
   reviewer ran the containment test over this block's own extracted slices
   before emission and it reported no pair to classify, so no FROM count and no
   FROM-zero count is ordered anywhere below.
4. THE LEDGER APPEND IS BLANK-SEPARATED. RECORD33 is appended preceded by
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
   watches the run this round's push starts; a conclusion cannot be known when
   the text that would carry it is written.

<<<SLICE PLAN34
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
R34: record R33's verdict in `.agent/live_review.md` so it is not stranded
(DECISION F085 D9). This round registers no finding, resolves none, and changes
no source file, test or document. It is the last round this session runs.

## Next Steps
1. THE NEXT SESSION REVIEWS R34 FIRST. Its handback is ungated by construction,
   and Phase 1 of docs/agents/self_drive_protocol.md orders rule 1, the `.agent/STOP`
   re-read, before rule 2, the Open PR Gate. R34 does NOT claim the terminator
   carve-out: that belongs only to the round creating the branch's pull request,
   which was R31 (R-0583).
2. THE OPEN PR GATE MERGES #207 at the start of the next feature, per AGENTS.md.
   The operator may merge it manually at any time instead.
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
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
<<<END PLAN34

<<<SLICE RECORD33
Gate: R34 — the R33 entry. R33 PASSED with NO finding against its own work. Every gate its block ordered was RE-EXECUTED by the reviewer over `665c45df..d2b83b0b` rather than read from the handback, and every one holds as written. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f086-r33.md`, the committed `.agent/authored/f086-r33.md` at `c92d3775` and the committed `.agent/last_block.md` at `994de489` are byte-EQUAL at sha256 508110e03e089a20ea34fa9f0342e2a2f1071a23f8ece9ee138f4892045561d4 over 18942 B and 180 lines, which is the digest the reviewer stated before delegating and the digest the worker verified on arrival before saving the file anywhere. THE PLAN LANDED AS AUTHORED: `.agent/plan.md` at `222a0205` byte-equals PLAN33 at sha256 fde90315a9cbc41a6c938138afa8b3f06a5d3d93e4658716fb8d8e1c9c219ca1 over 42 lines, under the AGENTS.md cap. THE LEDGER APPEND HELD UNDER TWO INDEPENDENT EXTRACTIONS AND A NEGATIVE CONTROL, which is what R-0572 and R-0578 ask for and what earlier rounds did not do: the pre-C2 blob is a byte-exact PREFIX of the blob at `a083781d`, its 6-line remainder equals a blank line, R-0599, a blank line, the R-0598 resolution, a blank line and the R32 entry at sha256 aa8d43c3a1020379411f89e0c73b792aff57faa0a8aab4e4a71a692c93b29fb0 with all three blank separators present, a paragraph-level split of the whole post-commit blob independently yields those same three texts as its last three paragraphs in that order, and a deliberately mutated remainder is rejected by BOTH extractions rather than by neither. THE SETS MOVED EXACTLY AS ORDERED: registered 181 to 182 gaining only `R-0599`, resolved 6 to 7 gaining only `R-0598`, no `Landed:` line at either end, and open reading 175 at BOTH ends because one registration and one resolution cancel — a number the block ordered measured rather than assumed, and it was. THE TWO SCANS RAN AND THE CONTROL PROVED THE FIRST OF THEM: unquoted `\bHEAD\b` reads 0 over the six lines `a083781d` ADDS, while the same extractor over `fd166295`'s added lines to the same file reads 3; `Gate: R` headers go 30 to 31, the only key occurring more than once is unchanged at both ends and is exactly `Gate: R19 — the R18 entry`, and `Gate: R33 — the R32 entry.` occurs once, sits last, and is followed by text beginning `R32 ` once its leading space is stripped. THE ROUND GATE WAS RE-RUN SERIALLY IN THE PRIMARY CHECKOUT: the four-file state-reader selection exit 0 at `160 passed`, and the canary exit 0 at `42 passed`, both equal to the readings taken at `665c45df`. THE RANGE IS WHAT THE HANDBACK DECLARES: five `.agent/` paths over five single-parent commits, every `+/-` cell byte-identical to `git diff --numstat` at 180/0, 112/259, 17/17, 6/0 and 27/34, a maximum insertion column of 180 under the 500 cap, every `git reflog` entry of the round reading `commit:`, each of the eight paths the Change section named as untouched present at `665c45df` and absent from the range, zero marker lines in any target, and a handback of 55 lines carrying all seven mandated headings in the template's order. THE THREE DECLARED DEVIATIONS ARE CORRECT AND COST NOTHING: two bash-guard refusals were rerouted through python without changing any command the block names, the full five-path change set genuinely cannot be measured from inside the commit that completes it — the reviewer measured it after the fact and it does equal the Change list — and the worker declared that it proved a 445 KB append's shape mechanically instead of reading the whole file, which for a pure append is the stronger evidence and not the weaker.
<<<END RECORD33

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f086-release-capability; `git status --porcelain`
   EMPTY after every commit and at the handback; `git worktree list` reports the
   primary checkout alone, because this round creates none. No reading is taken
   by overwriting a file in the primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f086-r34.md`, of `.agent/authored/f086-r34.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 PLAN. `.agent/plan.md` at C1 byte-equals PLAN34; report its sha256 and line
   count, that the count is under 50, and that `## Goal`, `## Next Steps` and
   `F086` all occur in it.
G4 LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
   PREFIX of the post-C2 blob, and the remainder is a blank line followed by
   RECORD33 — report the remainder's sha256 and line count and that the blank
   separator is present. Report it twice, by two INDEPENDENT extractions that
   must agree: the byte-level remainder above, and a paragraph-level split of the
   post-C2 blob whose LAST paragraph is RECORD33 (R-0572, R-0578). Run a NEGATIVE
   CONTROL — mutate one character of the expected remainder and confirm BOTH
   extractions reject it — and report both rejections.
G5 LEDGER SETS. With `^- R-\d+ — ` as registered and `^Done: R-\d+ — ` as
   resolved, report both counts plus open and `Landed:` at d2b83b0b and at C2.
   The reviewer measured 182 registered, 7 resolved, 175 open and 0 `Landed:` at
   d2b83b0b. Constraint 4 orders every one of those four numbers UNCHANGED at C2;
   report the measured pairs rather than the word unchanged.
G6 ITEM-20 SCAN. Over C2's ADDED lines only, delete backtick-quoted spans first,
   then report the count of `\bHEAD\b` — it must be 0. Run the SAME extractor
   over `fd166295`'s added lines to that file as a RED CONTROL and report that
   count too; a control that does not read above 0 makes the gate worthless.
G7 ITEM-26 HEADER. Report how many lines begin `Gate: R` at d2b83b0b and at C2,
   which header keys occur more than once at each end, that
   `Gate: R34 — the R33 entry.` occurs 1x, that it is the LAST such header, and
   that the text following it begins `R33 ` once its leading space is stripped.
   The reviewer measured 31 headers at d2b83b0b, with exactly
   `Gate: R19 — the R18 entry` occurring more than once.
G8 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches no source file, so
   the four files that read that state live are the gate, plus the canary.
   Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q`
   The reviewer measured 160 passed and 42 passed at d2b83b0b.
G9 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only d2b83b0b..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the eight paths the Change section names as untouched is PRESENT
   at d2b83b0b and absent from that range; that every commit in the range has one
   parent; that every `git reflog` entry of this round is `commit:`; and each
   commit's insertion column from `git diff --numstat`, every one under 500. Per
   checklist item 28 the same `+/-` cells appear in the handback's `## Commits`
   table and must be byte-identical to the tool's output there. C3's own cell
   cannot exist while C3 is being written, so it belongs to the round report, and
   so does the complete change set, which C3 completes.
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
             `.agent/STOP` re-read, and its SECOND as the Open PR Gate — in that
             order — and states that R34 awaits review rather than claiming the
             terminator carve-out, which belongs to R31 alone (R-0583). The full
             transcripts go in the round report you return, never in the file.
──────────────────────────────────────────────────────────────
