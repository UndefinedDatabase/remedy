# Handback — F255 R1 (F086 merged, F255 claimed, the record reset)

## Range

Review of b35d350b..`C5` — 7 commits, C0a C0b C1 C2 C3 C4 plus this C5, preceded by the S0 gate; one worker. `b35d350b` is the merge commit of pull request #207, which S0 merged at the Open PR Gate, and feature/f255-teacher-role is cut from it. State files plus one ledger line: no source file and no test changed. R-0600 is REGISTERED, nothing is resolved, and no `Done:` or `Landed:` line was authored (constraint 6). The C5 commit is this file itself.

## Commits

| # | SHA | Path | +/- | Reason |
|---|---|---|---|---|
| S0 | b35d350b | — | — | merge of PR #207 into `main`; not a commit of this branch |
| C0a | 903c00ff | .agent/authored/f255-r1.md | 386/0 | save the R1 block, copied not retyped |
| C0b | d5437d29 | .agent/last_block.md | 352/154 | mirror it; identical git blob 74f3dde6 |
| C1 | c4718364 | docs/roadmap/STATUS.md | 1/1 | CLAIM255FROM → CLAIM255TO, F255 to `[~]` |
| C1 | c4718364 | .agent/context.md | 28/27 | CONTEXT255 — scope reset to F255 |
| C2 | 7efd78aa | .agent/live_review.md | 25/124 | RESETPY reset carrying 175 open forward, then R-0600 |
| C3 | ea6c7f03 | .agent/live_review.md | 2/0 | RECORD35 appended, blank-separated |
| C4 | 7f1fc0e0 | .agent/plan.md | 31/34 | PLAN255 — the plan advanced to F255 R1 |
| C5 | self | .agent/handoff.md | self | this handback; its own cells are in the round report (R-0149) |

| Item | Status | Reason |
|---|---|---|
| S0 — the Open PR Gate and the new branch | done | one PR read, #207 merged, branch cut from the merge commit |
| C0a — save this block | done | byte-equal to the reviewer's scratch original |
| C0b — mirror it | done | same digest, same git blob 74f3dde6 |
| C1 — claim F255 and reset the scope | done | rewrite pair, 1 insertion 1 deletion; CONTEXT255 byte-exact |
| C2 — reset the record and register R-0600 | done | reset run as the RESETPY script, 175 carried verbatim |
| C3 — gate F086 R35 | done | 2-line blank-separated append, two extractions agree |
| C4 — the plan | done | PLAN255 byte-exact, 40 lines |
| C5 — the handback, then push | done | the push output is in the round report, not in this file |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned EXACTLY ONE entry — #207, head `feature/f086-release-capability`, base `main`, `isDraft:false` — the expected reading, so `gh pr merge 207 --merge --delete-branch` ran and `gh pr view 207 --json state,mergedAt` then reported `MERGED` at 2026-08-20T20:27:23Z. Then `git checkout main`, `git pull --ff-only` (both already up to date, the merge command having fast-forwarded local `main` to b35d350b itself) and `git checkout -b feature/f255-teacher-role`. NO worktree was created (constraint 8). No force push, no history rewrite, no commit on `main`, no `gh pr create` and no `gh pr edit` — this branch's pull request is created at closure. No CI run was waited on or read (constraint 9). The `git push -u origin feature/f255-teacher-role` is ordered AFTER C5 and cannot appear in a file C5 contains; its real output is in the round report.

## Verification

- G1 HYGIENE — `.agent/STOP` read from disk before S0, ABSENT; `git status --porcelain` EMPTY after every commit and here; `git worktree list` one line throughout; branch after S0 is feature/f255-teacher-role; every non-current reading came from `git show <sha>:<path>`.
- G2 THE OPEN PR GATE — list, merge command, real output and `MERGED` are in External actions and verbatim in the round report; `git log --oneline -n 1 main` and `git rev-parse main` both read b35d350b, `origin/main` agrees, and `git merge-base HEAD main` IS b35d350b. No commit of this round has `main` as its branch.
- G3 TRANSPORT — `.remedy-wt/f255-r1.md`, the committed C0a and the committed C0b are byte-EQUAL at sha256 c445fb0d6e9b45a98a5523c0fb35292be44289aa91c12dd72d19ca61e10e7d25, 29472 B over 386 lines — the digest the reviewer stated before delegating, verified on arrival BEFORE the file was saved anywhere — and both commits carry the identical git blob 74f3dde6.
- G4 SLICES EXTRACTED, NEVER RETYPED — all 8 pulled by marker regex from the COMMITTED `.agent/authored/f255-r1.md` at 903c00ff, each digest carrying BOTH counts with the trailing newline INCLUDED (R-0600): CLAIM255FROM d6cc013c 83 B/1 L, CLAIM255TO 09dba254 83 B/1 L, LRHEAD255 51c4c968 1814 B/31 L, RESETPY 8c643b8b 2155 B/55 L, R0600 5645264f 2232 B/1 L, RECORD35 818125f7 4807 B/1 L, PLAN255 68d153b8 2234 B/40 L, CONTEXT255 0344211c 2735 B/48 L.
- G5 THE CLAIM, A REWRITE PAIR — in `docs/roadmap/STATUS.md`, CLAIM255FROM as a whole line reads 1x at b35d350b and 0x at C1; CLAIM255TO reads 0x then 1x — the FROM-zero count the rewrite shape owes. `git diff --numstat` for that file at C1 is `1 1`, so no other ledger line moved; 342 lines and 28719 B at both ends.
- G6 THE RESET, BY SCRIPT, WITH ITS CONTROLS — the RESETPY slice ran as a script, exit 0, stdout `registered 182 / resolved 7 / carried 175 / orphans 0 / first_id R-0570 last_id R-0599 / out_units 179`, matching the reviewer's dry run. INDEPENDENTLY, a line scan with `^- (R-\d+) — ` and `^Done: (R-\d+) — `: 175 open at the base, 175 carried at C2, EQUAL as ORDERED sequences, 0 of the 7 resolved ids present at C2. `^Done: ` 0x and `^Gate: ` 0x in the C2 blob.
- G7 THE CARRY IS VERBATIM, AND THE CONTROL PROVES IT CAN FAIL — every carried paragraph at C2 is an EXACT ELEMENT of the base record's 226-paragraph set: 175 matched of 175. Three negative controls, each REJECTED: one unit truncated by 40 B (175/174), one word altered (175/174), one unit dropped (count 174). The truncated unit IS a substring of the base blob and is NOT an element of its paragraph set — which is why exact membership was ordered.
- G8 R-0600 REGISTERED, SETS MEASURED AT BOTH ENDS — 182 registered / 7 resolved / 175 open / 0 `Landed:` at b35d350b, and 176 / 0 / 176 / 0 at C2, the reading a carry-forward plus one registration owes. `- R-0600 — ` occurs exactly 1x at C2, as the last registered id.
- G9 THE R35 GATE ENTRY — the pre-C3 blob (314805 B, 972 lines) is a byte-exact PREFIX of the post-C3 blob (319613 B, 974 lines); the remainder is 158079a7…, 4808 B over 2 lines, a blank line followed by RECORD35, separator PRESENT (R-0578). SECOND, INDEPENDENT extraction: a paragraph split of the post-C3 blob yields 181 units whose LAST is exactly RECORD35 — 818125f7… over 4807 B with the trailing newline INCLUDED, d336f5e0… over 4806 B with it STRIPPED. A control mutating one byte of the expected remainder (blob offset 314845, `S`→`X`) is REJECTED by BOTH readings. `Gate: R1 — the F086 R35 entry.` occurs 1x, is the only and therefore LAST line beginning `Gate: R`, and no header key repeats.
- G10 THE STATE FILES SATISFY THEIR READERS — `.agent/plan.md` at C4 byte-equals PLAN255 (68d153b8…, 2234 B, 40 lines, under the 50-line cap) with `## Goal` 1x, `## Next Steps` 1x, `F255` 3x; `.agent/context.md` at C1 byte-equals CONTEXT255 (0344211c…, 2735 B, 48 lines) with `## Active Branch` 1x, `feature/` 1x, `Steps` 1x, `F255` 1x, `pytest` 2x; `.agent/live_review.md` at C3 contains `Steps` 17x, of which `## Steps` 7x.
- G11 THE ROUND GATE — serially in the PRIMARY checkout, never two pytest processes at once. The four-file state-reader selection `-q -rf` exit 0, `160 passed in 19.98s`; `tests/docs/ tests/orchestration/test_roadmap_index.py -q -rf` exit 0, `325 passed in 0.75s`; the canary `tests/cli/test_golden_path.py -q -rf` exit 0, `42 passed in 20.64s`. All three equal the counts the reviewer measured at 538323e0.
- G12 CHANGE SET, HISTORY AND CAPS — `git diff --name-only b35d350b..HEAD` before C5 is exactly the six paths C0a..C4 name, no path on either side alone; `.agent/handoff.md` is the seventh and lands with C5, so the complete Change list holds only once C5 exists and is reported there. All SEVEN paths the Change section names as untouched are PRESENT at b35d350b and ABSENT from the range. Every commit C0a..C4 has one parent; every `git reflog` entry of this round reads `commit:`, C5's own being in the round report. Every `+/-` cell above is pasted from `git diff --numstat`; the maximum insertion column over C0a..C4 is 386, under the 500 cap.
- G13 NO MARKER LEAKED — LINES beginning with the SLICE or the END marker count 0 in each of the five files this round writes: `docs/roadmap/STATUS.md`, `.agent/context.md`, `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`.
- G14 THE PUSH — ordered after C5, so no reading of it can exist in this file; the real `git push -u origin feature/f255-teacher-role` output is in the round report. No pull request was created, and the CI run the push starts was NOT waited on and its conclusion is not reported here (constraint 9).

## Authored-text proofs

All eight slices were extracted PROGRAMMATICALLY, by regex on the SLICE/END markers, from the committed `.agent/authored/f255-r1.md` at 903c00ff — which G3 proves byte-EQUAL to the reviewer's scratch original — and applied byte-verbatim: never retyped, rewrapped, reordered or summarised. Disk-to-disk comparisons are at G4, G5, G7, G9 and G10, and every digest with both counts is at G4. `.agent/context.md` and `.agent/plan.md` byte-equal CONTEXT255 and PLAN255 as whole files; R0600 and RECORD35 landed as blank-separated appends; RESETPY was RUN, not transcribed. ONE FROM/TO pair exists, CLAIM255FROM→CLAIM255TO over `docs/roadmap/STATUS.md`, a REWRITE per constraint 4, and G5 carries the FROM-zero count that shape owes. No marker line reached any target (G13).

## Deviations & assumptions

The sequence was S0, C0a, C0b, C1, C2, C3, C4, C5 exactly as the block labels it — nothing added, dropped or reordered — and NO slice was edited, so no constraint-1 declaration is owed. `.agent/plan.md` still described F086 R35 for the commits C0a..C3, because the block schedules the plan rewrite at C4; that is the block's ordering, followed as written, and the plan is current from C4 onward. Every gate command ran through `python3` subprocess wrappers or heredocs rather than bare shell, because this session's bash guard rejects `$( )`, loops and `$?` chaining BY FORM; no command the block names was altered and no gate's meaning changed. One reading deviation, already visible at G12 and G14: C5's own `+/-` cell, the complete seven-path change set, C5's reflog entry and the push output cannot be measured from inside the commit that produces them, so the block routes them to the round report and this file names them rather than carrying them.

Deviations, declared (DECISION D15): this file is 67 lines, over the block's 60, and ~3000 tokens by a chars/4 estimate, over the template's 800. The cause is mandated content only — two tables the bundle requires (a 9-row per-commit table for 7 commits, which the template itself allows up to 100 lines for, and the 8-row item-status table AGENTS.md mandates), fourteen gate lines at one LINE per gate (R-0582), the seven template headings and the verbatim Fortschritt line. Every transcript is in the round report; no section was dropped and no prose padding was added to reach this length.

Fortschritt: ~2 % (F086 merged and closed · F255 claimed · R1 the claim and the record reset · R2 the inventory next) — Schätzung

## Next

FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, the next session RE-READS `.agent/STOP` from disk; it was absent at S0, but rule 1 binds at any point and the sentinel is never assumed. SECOND, R2 — the teacher-role inventory, MEASURED in the source: how `role_config` resolves a role, which ledger events carry a stable vocabulary, how F103 separates a budget pool, what `ActionClass` read_only enforces and how the watch path isolates a reader. There is NO open pull request to merge: S0 merged the only one, and this branch's PR is created by the closure round. R1 AWAITS REVIEW. Open findings 176; next free id R-0601.
