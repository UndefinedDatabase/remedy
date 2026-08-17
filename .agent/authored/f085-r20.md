# F085 R20 — record the R19 PASS and close the session on a written handoff

Feature T2_F085 Sandbox hardening (stage 1) · Round R20 · Branch feature/f085-sandbox-hardening
Base of this round: the R19 handback commit, `git rev-parse HEAD` at start = 6b6cfee5.
Fortschritt: ~70 % (T001 gebaut · R13-R19 PASS · T002a: Builder-Site und CLI-Half fertig ·
`stream_evidence.py`, T002b-d, T003 offen) — Schätzung.

## Goal

A record round, and deliberately nothing else. R19 passed the reviewer's gate and that verdict is
written by C1, because a verdict that exists only in a session's chat is a verdict that did not
happen: `.agent/live_review.md` is where a round's gate lives, and the round AFTER a PASS is what
writes it there. This session reached its declared round cap with R19, so the work that would
normally follow — deciding the shape of `stream_evidence.py`:595, T002a's last spawn site — does
NOT start here. Starting it would mean opening a design question at a session boundary, which is
the ambiguity guardrail G8 of docs/agents/self_drive_protocol.md exists to prevent.

R20's own verdict is the TERMINATOR described in docs/agents/planner_reviewer_prompt.md §4.13: the
last round of a session has no on-disk gate entry by construction, because the round that would
write it is the one that never runs. That absence is expected and is NOT a missing gate — the next
session must not open a repair round to close it. C3's handoff carries R20's verdict instead, and
names the next session's first action in the protocol's own order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk) BEFORE rule 2 (the Open PR Gate).

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R20 step block verbatim` — `.agent/authored/f085-r20.md`
- C0b `docs(f085): mirror the R20 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R19 PASS` — `.agent/live_review.md`
- C2 `docs(f085): advance the plan to the stream-evidence decision` — `.agent/plan.md`
- C3 `docs(f085): rewrite the handback for R20 and close the session` — `.agent/handoff.md`

## Change set — exactly these paths, nothing else

`.agent/authored/f085-r20.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`. Nothing under `packages/`, `tests/`, `apps/`, `scripts/` or `docs/`.
`.agent/context.md` and `.agent/decisions.md` are NOT touched. Create NO pull request: this feature
is not at closure, T002b-d and T003 are open, and the PR is created by the closure round.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` or a byte write and prove
   the BYTE property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded.
3. Apply the FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it does
   not occur exactly once, STOP and report. Pair shape, classified MECHANICALLY by containment at
   build time and printed here rather than judged by eye: PLANF→PLANT REWRITE — the TO was tested
   for containment of its FROM and does not contain it. The pair rewrites the `## Current Step`
   section only; `## Next Steps` keeps its arity and is not spanned.
4. This round orders NO destructive check and no mutation red-proof. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.
6. If the single `python3` heredoc that writes the C0a bytes is rejected for length, split it into
   sequential appends to the same path. The method is fixed (programmatic write, never retyping);
   the number of calls is not.

<<<SLICE RECORD1>>>
Gate: R19 — PASS, the repair round that stopped a heading counting itself. All nine ordered gates
were re-run by the reviewer over 646092ce..6b6cfee5 and every one reproduces the handback's reading.
TRANSPORT is proven twice over, as it was in R18. Disk-to-disk: the committed
`.agent/authored/f085-r19.md`, the committed `.agent/last_block.md` and both working copies are
byte-EQUAL at sha256 4d750d6c237b25d7bd6e990ca0fee97bd3c9b47a03c5d2340ebda2ea81a13fba, 17340 B, 236
lines, 14 marker lines. And by digest fallback against the reviewer's OWN pre-emission measurements:
the block was measured in three regions before delegation and the saved file's three corresponding
regions hash to dc5598e8, f20288aa and a9d3811c exactly as measured. The worker split the C0a write
into seven calls because a single heredoc of that size is rejected by this session's tool; constraint
6 permitted exactly that, and the digests prove the split cost nothing. A declared deviation that a
gate can disprove is how this loop is supposed to work. THE APPEND COMMITS HOLD THEIR SHAPE: for C1
the pre-commit blob (297276 B) is a byte-exact PREFIX of the post-commit file (302599 B) and the
remainder is byte-equal to blank plus RECORD1 plus blank plus REG1; for C3 the pre-commit blob
(302599 B) is a prefix of (303775 B) and the remainder is blank plus DONE1. Each occurs exactly ONCE
at HEAD, no marker line survives, HEAD equals the C3 blob. THE ARITHMETIC MOVED WHERE IT WAS
ORDERED TO: 125 / 8 / 0 and 117 open at base, 126 / 8 / 0 and 118 open after C1 — the registration
landed, which is the reading that was flat in R17 and R18 and had to move here — and 126 / 9 / 0
with 117 open at HEAD. Registered difference exactly R-0511, resolved difference exactly R-0511, no
duplicate and no resolution naming an unregistered id; next free R-0512. THE FIX IS THE ONE THE
FINDING PRESCRIBED: HEADF occurs 0 times at HEAD and HEADT once, the diff is 2 lines for 2 lines,
and the word `twelve` occurs 0 times in the WHOLE file — the numeral was REMOVED rather than
corrected to seventeen, so there is no count left to go stale. The checklist region still parses to
a contiguous 1 through 17, so the commit that stopped counting the list did not disturb it. THE
PLAN PAIR touched what it was scoped to and nothing else: PLANF 0x, PLANT 1x, and `## Goal`,
`## Next Steps` and `## Risks` all byte-IDENTICAL to base, which is the proof that a Current-Step
rewrite did not span the list beside it. `.agent/plan.md` is at sha256
5684439dfacac31c052cd4e63bb661ed8a1b25218ae68c51fc09c3c7e1865d04, 2341 B, 40 lines under its cap.
Doc readers are 305 passed 1 skipped, state readers 157 passed, canary 42 passed, all rc 0 and all
re-run by the reviewer rather than accepted from the report. The change set is exactly the declared
paths with 0 outside; insertions are 236, 155, 58, 2, 13 and 4 before the handback commit, which is
itself 32, none over 500; seven single-parent commits, fourteen reflog entries all
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean, `git worktree list` is
ONE line, and the branch is in sync with its remote. The handback measures 80 lines against its own
declaration of 80. LAST_REVIEWED_SHA advances to 6b6cfee5.
<<<END RECORD1>>>
<<<SLICE PLANF>>>
## Current Step
R19, this round: record the R18 PASS, register R-0511 — the stale check count the R18
worker found in the checklist's own introduction — remove that numeral rather than
correct it, and resolve the finding. The next round leaves the review machinery and
returns to T002a's last spawn site.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R20, this round: record the R19 PASS and close the session on a written handoff. A
record round only — the session reached its declared round cap at R19, and opening
`stream_evidence.py`'s shape question at a session boundary is what guardrail G8 of
the self-drive protocol forbids. R20's own verdict is the §4.13 terminator: it lives
in the handoff, not on disk, and the next session must not open a repair round for it.
<<<END PLANT>>>

## Application order

C1 appends RECORD1 to `.agent/live_review.md`, preceded by exactly one blank line, appending only.
C2 applies PLANF→PLANT to `.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r20.md` after C0a and `.agent/last_block.md` after C0b are
byte-EQUAL: report one sha256, byte length, line count and marker-line count for both. C0b copies
the COMMITTED C0a blob, never the scratch file.

G3 APPEND SHAPE, once. For C1: the pre-commit blob is a byte-exact PREFIX of the post-commit file,
HEAD equals it, and the remainder is byte-equal to blank + RECORD1. RECORD1 occurs exactly ONCE in
the whole file at HEAD and the commit adds no marker line. Report the numstat pair as a READING.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 126 / 9 / 0, 117 open; at HEAD expect 126 / 9 / 0 and 117 open UNCHANGED,
because this round records a verdict and neither registers nor resolves an id. Report the reading at
both ends, both symmetric differences — which must both be EMPTY — duplicate-id counts, any
resolution naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT once. Report `.agent/plan.md` sha256, bytes and
a line count under 50, with `## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base.

G6 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0.
CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42 passed. Report the
state-reader count as a READING rather than matching it against a number: that suite spawns wrapper
processes under flock and timeouts and is timing-sensitive. If a run comes out red, report the
failing test id, re-run `tests/regression/test_resource_safety.py` alone three times and report all
four readings. A failure that reproduces every time is a STOP; one that does not is recorded with
its tally and the round continues. No doc-reader gate and no ruff gate are ordered, and neither is
skipped by oversight: this change set contains no `.py` file and no file under `docs/`.

G7 COMMIT HYGIENE, three readings. `git diff --name-only 6b6cfee5..HEAD` measured BEFORE C3 equals
the declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+` column of
`git show --numstat` for C0a, C0b, C1 and C2: none exceeds 500. C3's own count is ordered nowhere,
because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p 6b6cfee5..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its
exit code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C3. That handoff is
this session's only return channel, so it carries: feature and round, branch, the commit SHAs, the
changed-files table, the real verification readings, the open-findings count (117), and a NEXT
section naming the next session's first action in the protocol's own order — Phase 1 rule 1, re-read
`.agent/STOP` from disk, BEFORE rule 2, the Open PR Gate — and then the first real work item, which
is deciding the shape of `stream_evidence.py`:595, T002a's last spawn site, given that it streams
incrementally where `run_guarded` buffers. State in that NEXT section that R20 is a record-only
round whose own verdict is the §4.13 terminator and must NOT be treated as a missing gate. Run
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` after the final push and
report its output; create NO pull request and merge nothing. Report what the commands PRINTED — a
gate whose result you did not read is a finding. If a gate contradicts this block, report the
contradiction and STOP. Declare every deviation.
