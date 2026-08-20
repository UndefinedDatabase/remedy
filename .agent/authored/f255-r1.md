── STEP R1 — F255 Teacher role ────────────────────────────────
Goal:        Merge the F086 pull request at the Open PR Gate, claim F255 in the
             ledger, reset the live-review record so it carries the F086 open
             set forward without losing a byte, register R-0600 and record the
             F086 R35 verdict, which has no home in the record it belongs to.
             No source file and no test changes this round.

Bundle:      S0 the Open PR Gate and the new branch · C0a save this block ·
             C0b mirror it · C1 claim F255 and reset the scope · C2 reset the
             review record and register R-0600 · C3 gate F086 R35 · C4 the plan ·
             C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r1.md`
             C0b `.agent/last_block.md`
             C1  `docs/roadmap/STATUS.md` and `.agent/context.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `.agent/plan.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base and must stay untouched: `hatch_build.py`,
             `pyproject.toml`, `README.md`, `.agent/candidates.md`,
             `.agent/decisions.md`, `docs/roadmap/features/T5_F255.md`,
             `docs/agents/planner_reviewer_prompt.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r1.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r1.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. S0 IS THE OPEN PR GATE AND COMES FIRST, before any commit of this round.
   Run `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   and report it. Exactly one PR — #207, `feature/f086-release-capability` into
   `main`, not a draft — is the expected reading; ANY other reading stops the
   round and you write the handback instead. Then, exactly as AGENTS.md orders:
   `gh pr merge 207 --merge --delete-branch`, `git checkout main`,
   `git pull --ff-only`, `git checkout -b feature/f255-teacher-role`. No force
   push, no history rewrite, and no commit is ever made on `main`.
4. ONE PAIR, AND IT IS A REWRITE. CLAIM255FROM and CLAIM255TO are a FROM→TO pair
   over `docs/roadmap/STATUS.md`. The reviewer ran the containment test over the
   two slices before emission and the test printed `TO contains FROM: False`, so
   the pair is a REWRITE and G5 orders the FROM-zero count that shape owes.
   Every other slice is a whole-file replacement or an append, and owes no pair
   proof at all.
5. THE RECORD IS RESET BY SCRIPT, NEVER BY HAND. C2 writes
   `.agent/live_review.md` by running the RESETPY slice, which carries its own
   three controls and fails loudly rather than writing a damaged record. You do
   not retype, rewrap, reorder or summarise a single carried finding. The
   reviewer dry-ran this exact script against the base record and it printed
   registered 182, resolved 7, carried 175, orphans 0, first_id R-0570, last_id
   R-0599, out_units 179. R0600 is then APPENDED to that reset record, in the
   same C2 commit, preceded by exactly one blank line (R-0578) and placed after
   the last carried finding; RECORD35 is appended to the result the same way at
   C3. Both are copied from their extracted slice files, never retyped.
6. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH. Nothing is fixed this
   round, only recorded. R-0600 is REGISTERED, and the reset carries the open
   set forward unresolved.
7. `.agent/STOP` is read from disk before S0. If it exists, stop and write the
   handback instead — the merge does not happen either.
8. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
9. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion. The
   reviewer watched run 32411743463 on `538323e0` to its conclusion before
   emitting this block, which is why S0 may merge at all.

<<<SLICE CLAIM255FROM
- [ ] F255 — Teacher role (evidence-grounded live explainer & learn-along tutor)
<<<END CLAIM255FROM

<<<SLICE CLAIM255TO
- [~] F255 — Teacher role (evidence-grounded live explainer & learn-along tutor)
<<<END CLAIM255TO

<<<SLICE LRHEAD255
# Live Review — F255 Teacher role

> Round-by-round review record for the F255 branch, reset at the feature claim.
> The F086 record closed with pull request #207, merged into `main` at this
> feature's Open PR Gate. That branch's LAST round, R35, has no gate entry in
> its own record by construction, because a round's verdict is written by the
> NEXT reviewed round (DECISION F085 D9) and R35 was the last round F086 had;
> its entry is therefore the first `Gate:` paragraph below. Finding ids continue
> the monotonic R-XXXX series across the reset.
> Next free id: R-0601.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when
> the F086 record closed are reproduced verbatim below, extracted BY ID out of
> the previous record by script and never retyped, never rewrapped and never
> summarised. The pre-reset record held no `Landed:` line.

## Steps
R1 merge #207 at the Open PR Gate, claim F255 in the ledger, reset this record
carrying the F086 open set forward, register R-0600 and gate R35 → R2 the
teacher-role inventory: how `role_config` resolves a role today, which ledger
events carry a vocabulary stable enough to key narration to, how F103 separates
a budget pool, what `ActionClass` read_only already enforces and how the watch
path isolates a reader from the run — each MEASURED in the source rather than
read off the feature file → R3 record R2 and rule the teacher role's shape, its
three grounding sources and its own budget pool as a DECISION, amending
`docs/roadmap/features/T5_F255.md` with the Design, Task slicing, Acceptance and
Do-not-touch sections its registration stub has never carried → R4 onward the
built work, in the T-slices that DECISION names.

## Findings
<<<END LRHEAD255

<<<SLICE RESETPY
"""Reset .agent/live_review.md for F255, carrying the F086 open set forward.

Paragraph convention, stated because a digest without it is unrecoverable
(finding R-0600): a UNIT is a run of text between blank-line separators, taken
WITHOUT any trailing newline. The file is exactly the units joined by a blank
line, plus one final newline.
"""
import re
import sys

SRC = sys.argv[1]          # the pre-reset .agent/live_review.md
HEADSLICE = sys.argv[2]    # the extracted LRHEAD255 slice
OUT = sys.argv[3]          # where the reset record is written

src = open(SRC, encoding="utf-8").read()
units = [u.rstrip("\n") for u in src.split("\n\n")]

# CONTROL 1 - the split is lossless: it reconstructs the source byte for byte.
assert "\n\n".join(units) + "\n" == src, "paragraph split is not lossless"

reg = re.compile(r"^- (R-\d+) — ")
done = re.compile(r"^Done: (R-\d+) — ")

registered, resolved, orphans = [], set(), 0
for u in units:
    if reg.match(u):
        registered.append(u)
    elif done.match(u):
        resolved.add(done.match(u).group(1))
    elif not (u.startswith("#") or u.startswith(">") or u.startswith("Gate: R")):
        orphans += 1

# CONTROL 2 - a truncated carry shows up as a fragment that matches no kind.
assert orphans == 0, "orphan fragment: the record does not split cleanly"

carried = [u for u in registered if reg.match(u).group(1) not in resolved]
ids = [reg.match(u).group(1) for u in carried]

# CONTROL 3 - every carried unit is an EXACT ELEMENT of the source unit list.
# Substring containment is NOT enough: a truncated paragraph is still a
# substring of the source, so "u in src" cannot reject a truncated carry.
source_units = set(units)
for u in carried:
    assert u in source_units, "carried unit is not a verbatim source paragraph"

head = open(HEADSLICE, encoding="utf-8").read().rstrip("\n")
out = "\n\n".join([head] + carried) + "\n"
open(OUT, "w", encoding="utf-8").write(out)

print("registered", len(registered))
print("resolved", len(resolved))
print("carried", len(carried))
print("orphans", orphans)
print("first_id", ids[0], "last_id", ids[-1])
print("out_units", len(out.split("\n\n")))
<<<END RESETPY

<<<SLICE R0600
- R-0600 — Low — A DIGEST STATED FOR AN EXTRACTED REGION WITHOUT ITS BYTE AND LINE COUNT LEAVES THE NEWLINE CONVENTION UNRECOVERABLE, SO RE-MEASURING A TRUE RECORD READS FAIL. The entry `Gate: R35 — the R34 entry.`, appended to the F086 record at `f7c9ac12` and not carried into this file, which carries findings only, states its second and independent extraction as "a paragraph-level split of the whole post-commit blob independently yields RECORD33 as the last of its 225 paragraphs at sha256 2e625c2042172a92166d202c60dd1bdd64e918d16ef5eee7369485e6348737b9" and gives neither a byte count nor a line count with it. Re-measured by the F255 R1 reviewer at `eaca4ed2`: the last of that blob's 225 paragraphs digests to `925b1388cc9b1194` over 3640 B when the paragraph's trailing newline is INCLUDED, and to `2e625c2042172a92` over 3639 B when it is STRIPPED, so the entry is TRUE under the stripped reading, unverifiable under the other, and nothing in the sentence says which was taken. The same round's own handback states the counterpart measurement the other way — `2b5b3239`, 4349 B, 1 line, newline INCLUDED — so two texts of one round record the same class of measurement under opposite conventions, and only the one carrying counts can be checked at all. Nothing on disk is wrong and no carry was lost; the defect is in the proof text, which is the permanent record, and discharging it cost the next reviewer a re-measurement round. The counter-measure is a §3 pre-emission checklist item: every digest a block or a record states for an extracted region carries the byte count and the line count of the exact bytes digested. The R1 dry run of this feature's own reset found the same class in its second half — an extraction-equality control written as substring containment cannot reject a TRUNCATED carry, because a truncated paragraph remains a substring of the source, so that control was replaced before emission by exact membership in the source's paragraph SET, with negative controls that reject truncation, corruption and omission alike. Both halves belong in one checklist item: a measurement that cannot fail and a measurement whose units are unstated are the same defect wearing different clothes.
<<<END R0600

<<<SLICE RECORD35
Gate: R1 — the F086 R35 entry. R35 PASSED with NO finding against its own work and none against its block, and its verdict is recorded HERE rather than in the record it belongs to because R35 was the last round of the F086 branch and a round's verdict is written by the NEXT reviewed round (DECISION F085 D9). Every gate the R35 block ordered was RE-EXECUTED by the reviewer over `d56cadad..538323e0` rather than read from the handback, and every one holds as written. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f086-r35.md`, the committed `.agent/authored/f086-r35.md` at `83f47722` and the committed `.agent/last_block.md` at `e1ea7e37` are byte-EQUAL at sha256 e343fbc2c680a40000caefa03e0a18759d02a5bdd206a1e585805a2fa218c200 over 16778 B and 188 lines, and both commits carry the identical git blob `ad133a89`. THE PLAN LANDED AS AUTHORED: `.agent/plan.md` at `a7754e89` byte-equals PLAN35 extracted programmatically from the committed block, at sha256 581b3997e921679e4b1bb23207c48b4c284850c4571aa65479e324bc1b94a2f8 over 2467 B and 43 lines, under the AGENTS.md 50-line cap, carrying `## Goal` once, `## Next Steps` once and `F086` four times. THE LEDGER APPEND HELD UNDER TWO EXTRACTIONS AND A NEGATIVE CONTROL: the pre-C2 blob at `a7754e89`, 456242 B over 1069 lines, is a byte-exact PREFIX of the post-C2 blob at `f7c9ac12`, 460592 B over 1071 lines; the 2-line remainder is a blank line followed by RECORD34 at sha256 dbe1fe3999384b375c11ad55cb204fb6a246f31cae063c3bc558a2079813c7e5 over 4350 B with the blank separator PRESENT; a paragraph-level split of the post-C2 blob independently yields RECORD34 as the last of its 226 paragraphs, at sha256 2b5b3239ef0c3666887369ebcb2ffa5753c3c5ad9f894424e0a4567c14c65ae4 over 4349 B and 1 line with the paragraph's trailing newline INCLUDED and at sha256 6dff0faa70f04b8469647007f831b09395d4e8504e1a8286d9962776aa2f3d82 over 4348 B with it STRIPPED, both stated because R-0600 is registered this round for omitting exactly that; and a remainder mutated at one byte, offset 40, space to the letter X, is REJECTED by both extractions rather than by neither. THE SETS DID NOT MOVE AND BOTH ENDS WERE MEASURED: registered 182, resolved 7, open 175 and `Landed:` 0 at `d56cadad`, and each of those four numbers identical at `f7c9ac12`, which is what a `Gate:` paragraph adding no `- R-` line and no `Done:` line must produce. THE TWO SCANS RAN AND THE CONTROL PROVED THE FIRST OF THEM: with backtick-quoted spans deleted first, the unquoted word-boundary match on the four capital letters reads 0 over the two lines `f7c9ac12` adds, while the same extractor over `fd166295`'s four added lines to that same file reads 3, so the gate is not vacuous; `Gate: R` headers go 32 to 33, the only key occurring more than once is unchanged at both ends and is exactly `Gate: R19 — the R18 entry`, and `Gate: R35 — the R34 entry.` occurs once, sits last, and is followed by text beginning `R34 ` once its leading space is stripped. THE ROUND GATE WAS RE-RUN SERIALLY IN THE PRIMARY CHECKOUT, never two pytest processes at once: the four-file state-reader selection exited 0 at `160 passed` and the canary exited 0 at `42 passed`, each equal to the count the R35 block records the reviewer measuring at `d56cadad`. THE RANGE IS WHAT THE HANDBACK DECLARES: five `.agent/` paths over five single-parent commits, every `+/-` cell of the `## Commits` table byte-identical to `git diff --numstat` at 188/0, 65/54, 10/10 and 2/0, with the handback commit's own 20/20 correctly routed to the round report rather than claimed inside itself; a maximum insertion column of 188, under the 500 cap; every `git reflog` entry of the round reading `commit:`; each of the eight paths the Change section names as untouched present at `d56cadad` and absent from the range; zero marker lines in either target; and a handback of 55 lines carrying all seven mandated headings in the template's order, under the 60-line cap. THE PERMANENT RECORD IT WROTE IS TRUE, which is the check a `Gate:` entry owes the entry below it: the reviewer re-measured every factual claim RECORD34 makes — the R34 transport digest 8b6a657c over 15233 B and 177 lines with blob `5941b129`, the `b7e373cb` plan digest 7270a6b4 over 2483 B and 43 lines with its heading counts of one, one and two, the prefix property with its 88184b09 remainder over 3641 B, the 225-paragraph split, the 182/7/175/0 sets at both ends, and the 31-to-32 header count — against disk at the SHAs that sentence names, and every one of them holds; its single unrecoverable clause is the bare paragraph digest R-0600 registers. R35 IS NOT A TERMINATOR and never claimed to be: R-0583 gives that carve-out to the round whose bundle creates the branch's pull request, which on F086 was R31.
<<<END RECORD35

<<<SLICE PLAN255
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at the merge commit of pull
request #207, which this round merged at the Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to ledger events (Stage 1, deterministic
templates, zero tokens) and on-demand Q&A (Stage 2, through the teacher role's
own model) both work, the three grounding sources are never mixed silently,
teacher spend is its own budget pool in the F103 ledger, and the read-only
invariants hold under test.

## Current Step
R1: merge #207, claim F255, reset `.agent/live_review.md` carrying the F086 open
set forward, register R-0600 and record the F086 R35 verdict. No source file and
no test changes this round.

## Next Steps
1. R2 MEASURES THE GROUND BEFORE ANYTHING IS DESIGNED, because the feature file
   is a registration stub: how `role_config` resolves a role, which ledger
   events carry a stable vocabulary, how F103 separates a budget pool, what
   `ActionClass` read_only enforces, and how the watch path isolates a reader.
2. R3 RECORDS R2 AND RULES THE SHAPE AS A DECISION, amending
   `docs/roadmap/features/T5_F255.md` with the Design, Task slicing, Acceptance
   and Do-not-touch sections it has never carried.
3. R4 ONWARD BUILDS THE T-SLICES that DECISION names, Stage 1 before Stage 2.

## Risks
- THE FEATURE FILE IS A STUB. It carries Goal & Done, Scope and Non-goals only,
  so the Task slicing and Acceptance every build round reads are absent, and
  designing from the stub alone would be guessing rather than planning.
- THE THREE GROUNDING SOURCES ARE THE WHOLE FEATURE. A teacher that silently
  mixes ledger fact, workspace code and model knowledge is worse than no
  teacher, so their separation is a test obligation and not a prompt wish.
- READ-ONLY IS AN INVARIANT, NOT AN INTENTION. `ActionClass` read_only and the
  watch isolation must be shown to hold for the teacher path itself.
<<<END PLAN255

<<<SLICE CONTEXT255
# Context — F255 Teacher role

## Active Branch
feature/f255-teacher-role, cut from `main` at the merge commit of pull request
#207, which this round merged at the Open PR Gate. Self-drive session per
docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit.

## Scope
In: a fourth configured role `teacher`, resolved through the same `role_config`
mechanism as orchestrator, worker and reviewer; passive narration keyed to
ledger events (Stage 1: deterministic templates, zero tokens, offline);
on-demand Q&A (Stage 2) through the teacher role's own model over a small
context; three grounding sources kept separate and labelled; a teacher budget
pool reported apart from mission spend in the F103 ledger; a level dial; and the
CLI surfaces `remedy do watch --learn` and `remedy teach ask`.

Out, per the feature file's Non-goals: any write access to the run, mission
steering, and any influence on orchestrator, worker or reviewer decisions. The
cockpit panel ships with Tier 5 and not before.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state
  live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- THE FEATURE FILE IS A REGISTRATION STUB: Goal & Done, Scope and Non-goals and
  nothing else. R2 inventories the ground and R3 rules the shape and amends the
  file; no build round starts before that amendment lands.
- Repository-wide `ruff check` is RED at the claim and is NOT a gate (R-0364):
  the reviewer measured 26 errors at 538323e0 — 20 I001, 4 F401, 1 UP035 and
  1 F821. Ruff is gated scoped to the files a round touches, measured against
  the SAME files at the claim so a pre-existing error is not read as a new one.
- 176 findings are open once this round registers R-0600, all carried forward
  into the reset record per DECISION F057 D1. R-0403, R-0448, R-0482, R-0487,
  R-0490, R-0567, R-0568, R-0569, R-0570 and R-0571 stay routed to a paydown
  branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXT255

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before S0 and reported absent or
   present; `git status --porcelain` EMPTY after every commit and at the
   handback; `git worktree list` reports the primary checkout alone, because
   this round creates none; the branch after S0 is feature/f255-teacher-role.
   No reading is taken by overwriting a file in the primary checkout — use
   `git show <sha>:<path>`.
G2 THE OPEN PR GATE. Report the `gh pr list` output BEFORE the merge verbatim,
   the exact merge command and its real output, then `gh pr view 207 --json
   state,mergedAt` showing `MERGED`, then `git log --oneline -n 1 main` and
   `git rev-parse main`. Report that the new branch's merge-base with `main` IS
   that merge commit, and that `git log --oneline -n 1 origin/main` agrees. No
   commit of this round has `main` as its branch.
G3 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r1.md`, of `.agent/authored/f255-r1.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G4 SLICES EXTRACTED, NEVER RETYPED. Report the command that extracts each slice
   from the COMMITTED `.agent/authored/f255-r1.md` by its markers, and the
   sha256, byte count and line count of each extracted slice. Every count you
   state anywhere for an extracted region carries its bytes AND its lines,
   which is what R-0600 registers.
G5 THE CLAIM, A REWRITE PAIR. In `docs/roadmap/STATUS.md`: report CLAIM255FROM's
   count at the base and after C1, and CLAIM255TO's count at both ends. The
   reviewer measured FROM 1x and TO 0x at the base; the rewrite shape owes FROM
   0x and TO 1x after C1. Report `git diff --numstat` for that file at C1 — it
   must be 1 insertion and 1 deletion, proving no other ledger line moved.
G6 THE RESET, BY SCRIPT, WITH ITS CONTROLS. Report the RESETPY run's full stdout
   and its exit code. Then, INDEPENDENTLY of that script and of any paragraph
   split, scan the pre-reset blob and the C2 blob line by line with
   `^- (R-\d+) — ` and `^Done: (R-\d+) — `, and report: the open set at the base
   as a count, the carried id list at C2 as a count, that the two are EQUAL as
   ORDERED sequences, and that no resolved id appears at C2. The reviewer
   measured 175 open at the base. Report also that `^Done: ` and `^Gate: ` each
   occur 0x in the C2 blob before C3 appends the first gate entry.
G7 THE CARRY IS VERBATIM, AND THE CONTROL PROVES IT CAN FAIL. Every carried
   paragraph at C2 is an EXACT ELEMENT of the base record's paragraph set —
   report that as a count of 175 matched out of 175. Then run THREE negative
   controls over your own extraction and report that EACH is REJECTED: one
   carried paragraph truncated by 40 bytes, one with a single word altered, and
   one dropped entirely. A control that is accepted makes the gate worthless;
   substring containment accepts the first of the three, which is why exact
   membership is ordered here.
G8 R-0600 REGISTERED, SETS MEASURED AT BOTH ENDS. With `^- R-\d+ — ` as
   registered and `^Done: R-\d+ — ` as resolved, report both counts plus open
   and `Landed:` at the base and at C2. The reviewer measured 182 registered,
   7 resolved, 175 open and 0 `Landed:` at the base. At C2 the expected reading
   is 176 registered, 0 resolved, 176 open and 0 `Landed:`, because the reset
   carries the open set only and this round registers R-0600. Report that
   `- R-0600 — ` occurs exactly 1x at C2.
G9 THE R35 GATE ENTRY. C3 appends RECORD35 preceded by exactly one blank line.
   The pre-C3 blob is a byte-exact PREFIX of the post-C3 blob; report the
   remainder's sha256, byte count and line count, and that the blank separator
   is present. Report it a SECOND time by an independent paragraph-level split
   whose LAST unit is RECORD35, giving that unit's sha256 with BOTH newline
   conventions and their byte counts. Run a negative control — one character of
   the expected remainder mutated — and report that BOTH readings reject it.
   Report that `Gate: R1 — the F086 R35 entry.` occurs exactly 1x, is the LAST
   line beginning `Gate: R`, and that no other `Gate: R` header key repeats.
G10 THE STATE FILES SATISFY THEIR READERS. Report, measured on the committed
   files: `.agent/plan.md` at C4 byte-equals PLAN255, its line count is under
   50, and it contains `## Goal`, `## Next Steps` and a roadmap F-id;
   `.agent/context.md` at C1 byte-equals CONTEXT255 and contains `## Active
   Branch`, `feature/`, `Steps`, a roadmap F-id and the word `pytest`;
   `.agent/live_review.md` at C3 contains `Steps`. Report each as the measured
   value, not as the word yes.
G11 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest
   processes at once. This round rewrites `.agent/` state AND touches
   docs/roadmap/**, so both selections gate, plus the canary. Report the exact
   command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed, exit 0 at 325 passed and exit 0
   at 42 passed, all three at 538323e0 in the primary checkout, and measured the
   docs selection green a second time with CLAIM255TO already applied inside a
   disposable worktree.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only <merge-base>..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the seven paths the Change section names as untouched is PRESENT
   at the base and absent from that range; that every commit in the range has
   one parent; that every `git reflog` entry of this round reads `commit:`; and
   each commit's insertion column from `git diff --numstat`, every one under
   500. The same `+/-` cells appear in the handback's `## Commits` table and
   must be byte-identical to the tool's output. C5's own cell cannot exist while
   C5 is written, so it belongs to the round report, and so does the complete
   change set, which C5 completes.
G13 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in every file this round writes: `docs/roadmap/STATUS.md`,
   `.agent/context.md`, `.agent/live_review.md`, `.agent/plan.md` and
   `.agent/handoff.md`. Every count must be 0.
G14 THE PUSH. After C5, `git push -u origin feature/f255-teacher-role` and
   report its real output. Do NOT create a pull request — on this project the
   PR is created by the closure round — and do NOT wait on the CI run the push
   starts (constraint 9). C5's own insertion count and the push cannot appear
   inside C5, so they belong in the round report.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, at most 60
             lines or a DECISION D15 stated-cause line naming the real count and
             the mandated content that caused it. It carries the item-status
             table for the S0..C5 bundle, the `## Commits` table G12 pins, and
             one LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1,
             the `.agent/STOP` re-read, and its SECOND as R2, the teacher-role
             inventory — in that order — and states that R1 awaits review. There
             is no open pull request to merge after this round, because S0
             merged the only one and this branch's PR is created at closure.
             The full transcripts go in the round report you return, never in
             the file. The handback also carries this Fortschritt line verbatim,
             because with no relay you never see the operator brief that would
             otherwise state it (R-0418):
             Fortschritt: ~2 % (F086 merged and closed · F255 claimed · R1 the
             claim and the record reset · R2 the inventory next) — Schätzung
──────────────────────────────────────────────────────────────
