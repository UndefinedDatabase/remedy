# F085 R16 — record the R15 PASS, register three block defects, resolve R-0506

Feature T2_F085 Sandbox hardening (stage 1) · Round R16 · Branch feature/f085-sandbox-hardening
Base of this round: the R15 handback commit, `git rev-parse HEAD` at start = 7185d949.
Fortschritt: ~60 % (T001 gebaut · R13/R14/R15 PASS · T002a: Builder-Site und CLI-Runner migriert ·
gekoppelte CLI-Sites, `stream_evidence.py`, T002b-d, T003 offen).

## Goal

A record-and-repair round, no behaviour change. R15 passed the reviewer's gate and that verdict is
written by C1, together with the three defects R15's worker found in the reviewer's own block text
and reported instead of repairing. Then the debt: R-0506's two falsified absence claims are
corrected in `exec_guard.py` and `managed_builder_execution.py` — the round its own text named — and
`.agent/plan.md`'s malformed numbering, which is R-0509, is repaired by a pair spanning the whole
section rather than a prefix of it.

Evidence already taken by the reviewer, reported so the worker does not repeat it: the C2 docstring
pairs were applied to a `git archive HEAD` extraction, where the exec-guard, managed-builder and
CLI-guard suites are 152 passed at BOTH base and the extraction, ruff is exit 0 on both touched
paths, the three retired phrases occur 0 times afterwards, and the caller grep names four paths.

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R16 step block verbatim` — `.agent/authored/f085-r16.md`
- C0b `docs(f085): mirror the R16 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R15 PASS and register three block defects` — `.agent/live_review.md`
- C2 `docs(f085): correct the absence claims the guard migration falsified` — both source files
- C3 `docs(review): resolve R-0506 now that its fix has landed` — `.agent/live_review.md`
- C4 `docs(f085): advance the plan and repair its numbering` — `.agent/plan.md`
- C5 `docs(f085): rewrite the handback for R16` — `.agent/handoff.md`

C3 is a separate commit ON PURPOSE and must not be folded into C1: a resolution written before its
fix lands would claim on disk something no commit had yet done, which is the exact hazard the
`Landed:`/`Done:` split exists to prevent (planner_reviewer_prompt.md §4.4).

## Change set — exactly these paths, nothing else

`.agent/authored/f085-r16.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `packages/orchestration/exec_guard.py`,
`packages/orchestration/managed_builder_execution.py`. Nothing under `docs/`, `apps/`, `scripts/` or
`tests/`; no other file under `packages/`. No test changes: this round alters docstrings and `.agent`
state only, and `pingpong_provider.py` is NOT touched — its coupled unit is R17's.
`.agent/context.md` and `.agent/decisions.md` are NOT touched.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` and prove the BYTE
   property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded: the review slices' regex-looking text and backticks are
   prose and land as prose.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. Pair shapes, classified mechanically by containment
   at build time and printed with this block: EGF→EGT REWRITE, MBE1F→MBE1T REWRITE, MBE2F→MBE2T
   REWRITE, PLANF→PLANT REWRITE. No "FROM 0x" reading is ordered for any pair not listed REWRITE.
4. This round orders NO destructive check and no mutation red-proof. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE RECORD1>>>
Gate: R15 — PASS, the round that gave the claude CLI seam its guarded runner. All ten ordered gates
were re-run by the reviewer from the repository root over c5d80471..7185d949 and every one
reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's `.remedy-wt/f085-r15.md`, the committed `.agent/authored/f085-r15.md` and
`.agent/last_block.md` are byte-EQUAL at sha256
e2f4ef715c40f02df7d552e15348268b2d0edb24b986ff91e762c666314e2d88, 22895 B, 400 lines — AT the
DECISION F105 D5 block cap, not over it. C1 IS A PURE APPEND: the pre-C1 blob is a byte-exact PREFIX
of the post-C1 file, HEAD equals it, the remainder is exactly blank + RECORD1 + blank + FIND1, each
occurring ONCE, and C1 added no marker line — the one slice-marker token the file holds is R7 prose,
present at both ends. THE ARITHMETIC: 121 / 3 / 0 at base against 122 / 3 / 0 at HEAD, the open set rising 118 to
119 by one registration against no resolution, difference exactly R-0507, no duplicate id and no
resolution naming an unregistered id. THE CHANGE ITSELF, read as a diff and then re-measured: the
module gains `_cli_exec_policy`, `_decode_cli_stream` and `_guarded_cli_run`, and `_resolve_version`
now calls the runner. By AST over the HEAD blob, `_resolve_version` and `_guarded_cli_run` hold ZERO
subprocess spawn nodes while `_call` and `_call_reviewer_structured` still hold ONE each — the
coupled unit R-0507 names, deliberately untouched. THE STRONGEST PROOF AVAILABLE WAS TAKEN: the
committed `pingpong_provider.py` and `test_claude_cli_exec_guard.py` are BYTE-IDENTICAL to the
`git archive` extraction the reviewer dry-ran before emission, where seven red controls each
reddened exactly their own tests, so the gates that pass here are the same gates proven capable of
failing. At HEAD the goldens are 8 passed, the seven-file regression set is 333 passed at C1 and 333
at HEAD, ruff is exit 0 on both touched paths, state readers 157 passed and the canary 42 passed.
The change set is exactly the seven declared paths with 0 outside; insertions are 400, 339, 50, 134
and 9, none over 500; six single-parent commits, every reflog entry `commit:`-prefixed, no amend,
rebase, reset or force-push; `git status --porcelain` is EMPTY and `git worktree list` is ONE line.
THE ROUND'S OWN REPORTING IS WHY THIS IS A PASS AND NOT A REPAIR: all three anomalies it declared
are defects in the REVIEWER'S block text, not in its execution, and it reported each rather than
quietly repairing a slice it was told to apply byte-verbatim. They are registered below as R-0508,
R-0509 and R-0510. LAST_REVIEWED_SHA advances to the R15 handback commit.
<<<END RECORD1>>>
<<<SLICE FIND1>>>
- R-0508 — Low, A PAIR'S SHAPE WAS ASSERTED FOR ONE PAIR AND ASSUMED FOR THE REST, AND THE
ASSUMPTION WAS WRONG. Raised by the R15 worker in its handback and confirmed by the reviewer against
its own R15 block. Constraint 3 of that block classified CLST as APPEND-shaped — correctly, its TO
contains its FROM — and then said "Every other pair is a REWRITE". IMP3 is not: IMP3T is
`from packages.orchestration.exec_guard import ...` followed by the model-aliases import line that
IS IMP3F, so the TO contains the FROM verbatim and IMP3F still occurs exactly 1x at HEAD, which the
reviewer re-measured. Nothing broke, because no gate in that block ordered an "IMP3F 0x" reading —
had one existed it would have been unsatisfiable by construction, which is the R-0207 failure this
classification exists to prevent. The defect is the method, not the damage: checklist item 4 says a
pair is declared APPEND only after checking that the TO literally CONTAINS the FROM, and the block
performed that check for the pair it suspected and generalised to the others by eye. An import
insertion that keeps the anchor line is the single most common append-shaped pair in this
repository, so eye-checking is exactly where it fails. Counter-measure, applied in the build of the
block that registers this: pair shapes are classified MECHANICALLY, every TO tested for containment
of its FROM, and the result printed beside each pair before emission — never written by hand. OPEN.
<<<END FIND1>>>
<<<SLICE FIND2>>>
- R-0509 — Medium, A REWRITE PAIR ENDED IN THE MIDDLE OF A NUMBERED LIST AND LEFT THE LIST
MALFORMED ON DISK. Raised by the R15 worker and confirmed by the reviewer. R15's PLANF covered
`## Current Step` plus only the FIRST item of `## Next Steps`; PLANT replaced it with a Current Step
and TWO numbered items. The surviving items below the FROM kept their old numbers, so
`.agent/plan.md` at 7185d949 reads 1, 2, 2, 3 — measured, not inferred. The worker was right not to
touch it: constraint 2 forbids rewording a slice, so repairing the numbering would have meant
editing authored text, and reporting the defect was the only honest move left to it. This is the
family where a pair's FROM is scoped to the text the reviewer INTENDED to change rather than to the
structure that text belongs to; a numbered list, a table and a fenced block are all single
structures whose arity a partial rewrite silently corrupts. Counter-measure, binding from this round
on: when a TO changes how many items a numbered list or table holds, the pair's FROM spans the WHOLE
structure, never a prefix of it. The block registering this carries the repair — its plan pair
covers the entire `## Next Steps` section and renumbers it 1 through 4. OPEN.
<<<END FIND2>>>
<<<SLICE FIND3>>>
- R-0510 — Low, A SECTION HEADING COUNTED ITS OWN CONTENTS BY HAND AND GOT IT WRONG. Raised by the
R15 worker and confirmed by the reviewer. That block's heading read "Change set — exactly these SIX
paths, nothing else" and the section then enumerated SEVEN, which is also what
`git diff --name-only c5d80471..HEAD` prints; the six-path reading is the one gate G10 orders for
the range BEFORE the handback commit, so both numbers exist and the heading attached the wrong one
to the wrong set. No gate was contradicted and nothing was mis-executed. This is the R-0402 /
R-0404 / R-0436 family that memory keeps re-learning — checklist item 11: count it mechanically or
state NO numeral — and its persistence has a specific cause worth naming. The R15 block DID apply
the rule: its Bundle heading was rewritten to carry no count precisely because the commit list had
grown by one. The Change set heading was not swept in the same pass, so the fix was applied to the
instance that was noticed rather than to the class. That is the R-0417 staleness shape wearing a
different hat. Counter-measure, applied in the build of this block: no heading in it states a count
of its own contents, and the build script greps the emitted bytes for a number-word standing next to
"paths" or "commits" and fails the build if it finds one. OPEN.
<<<END FIND3>>>
<<<SLICE DONE1>>>
Done: R-0506 — the two documented absence claims the R13 migration falsified are corrected, in the
round its own text named as the one that owes them. `packages/orchestration/exec_guard.py` no longer
says "NO CALLER. Nothing in this repository imports this module yet"; it now states PARTIAL coverage,
names the managed builder seam and the CLI provider as the callers, says which classes still spawn
unsupervised, and deliberately writes NO number, because the number changes with every migration
round and the caller grep is the honest answer. The allowlist sentence no longer claims choosing one
per command class "is not done here" — it records that callers choose it, the builder policy pinning
one and the CLI policy deliberately not. `packages/orchestration/managed_builder_execution.py` no
longer calls itself the only place that may INVOKE subprocess for builder execution: it may LAUNCH
one, and since F085 T002a it delegates the spawn to `exec_guard.run_guarded` while keeping the
policy, in both the module docstring and `run_managed_builder`'s. Both "shell=False ALWAYS" promises
are replaced by "No shell, ever" plus a pointer to the AST assertion that actually enforces it, so
the sentence that made R-0504 possible — a docstring a source-text test could satisfy — is gone.
Verified at the fix commit: the three retired phrases occur 0 times, the caller grep scoped to
`-- packages tests` names four paths, and the exec-guard and managed-builder suites are 152 passed,
matching base exactly.
<<<END DONE1>>>
<<<SLICE EGF>>>
- NO CALLER. Nothing in this repository imports this module yet. Migrating the
  in-scope call sites is T002, so no subprocess in the running system is
  limited, supervised or sandboxed by anything written here.
- No environment scrubbing UNLESS the policy asks for it: with
  `env_allowlist=None` the policy's `env` reaches the child UNCHANGED, which every
  T001 test relies on. CHOOSING an allowlist per command class is T002a's
  migration half and is not done here.
<<<END EGF>>>
<<<SLICE EGT>>>
- PARTIAL COVERAGE, and the gap is the point. Since F085 T002a the managed
  builder seam and the claude CLI provider run through this module; every other
  subprocess in the repository — the test, DoD, runtime, git and packaging
  classes — still spawns unsupervised. No count is written here on purpose: it
  changes with every migration round, and the caller grep is the honest answer.
- No environment scrubbing UNLESS the policy asks for it: with
  `env_allowlist=None` the policy's `env` reaches the child UNCHANGED, which every
  T001 test relies on. Callers CHOOSE the allowlist per command class — the
  builder policy pins one, the CLI-provider policy deliberately does not — so what
  a child inherits is that caller's decision, never this module's default.
<<<END EGT>>>
<<<SLICE MBE1F>>>
This module is the ONLY place in the codebase that may invoke subprocess for builder execution.
It enforces:
  - shell=False ALWAYS (argv list only, never a shell string).
<<<END MBE1F>>>
<<<SLICE MBE1T>>>
This module is the ONLY place in the codebase that may LAUNCH a builder execution. Since F085
T002a it does not spawn the child itself: it delegates to `exec_guard.run_guarded`, which owns the
spawn and its limits, while this module owns the policy. It enforces:
  - No shell, ever (argv list only, never a shell string) — asserted by AST against the guard's
    single Popen, because a docstring sentence is not a test (R-0504).
<<<END MBE1T>>>
<<<SLICE MBE2F>>>
    This is the ONLY function that executes a subprocess for builder adapters.
    shell=False ALWAYS. Sanitized env. Hard timeout. Output byte cap.
<<<END MBE2F>>>
<<<SLICE MBE2T>>>
    This is the ONLY function that launches a builder execution for builder adapters.
    Since F085 T002a the spawn itself lives in `exec_guard.run_guarded`; this function
    owns the policy. No shell, ever. Sanitized env. Hard timeout. Output byte cap.
<<<END MBE2T>>>
<<<SLICE PLANF>>>
## Current Step
R15, this round: record the R14 PASS, register R-0507, and give the claude CLI seam
its guarded runner — `_cli_exec_policy`, `_decode_cli_stream`, `_guarded_cli_run` —
migrating `_resolve_version`, the one site no test's mock reaches, with goldens that
spawn a real fake CLI instead of mocking the stdlib.

## Next Steps
1. R16 migrates the coupled unit of R-0507: `_call`, `_call_reviewer_structured` and
   the envelope test's mock, which must move together, plus R-0506's fix — the stale
   absence claims in `exec_guard.py` and `managed_builder_execution.py`.
2. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R16, this round: record the R15 PASS, register R-0508, R-0509 and R-0510 — three
defects in the reviewer's own R15 block that its worker reported rather than
repaired — resolve R-0506 by correcting the two falsified absence claims, and repair
the malformed numbering this section carried.

## Next Steps
1. R17 migrates the coupled unit of R-0507: `_call`, `_call_reviewer_structured` and
   the envelope test's mock, which must move together. The reviewer has already
   dry-run it green against an extraction, so the round is pairs and goldens only.
2. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
3. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
4. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANT>>>

## Application order

C1 appends RECORD1, then FIND1, then FIND2, then FIND3 to `.agent/live_review.md`, each preceded by
exactly one blank line, appending only. C2 applies EGF→EGT to
`packages/orchestration/exec_guard.py` and MBE1F→MBE1T then MBE2F→MBE2T to
`packages/orchestration/managed_builder_execution.py`. C3 appends DONE1 to `.agent/live_review.md`,
preceded by exactly one blank line. C4 applies PLANF→PLANT to `.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r16.md` after C0a, `.agent/last_block.md` after C0b and the
reviewer's original are byte-EQUAL: report one sha256, byte length and line count for all three.
C0b copies the COMMITTED C0a blob, never the scratch file.

G3 APPEND SHAPE, twice. For C1 and again for C3: the pre-commit blob is a byte-exact PREFIX of the
post-commit file, HEAD equals it, and the remainder is byte-equal to blank + the ordered slices for
that commit — RECORD1, FIND1, FIND2, FIND3 for C1, and DONE1 for C3. Each slice occurs exactly ONCE
in the whole file at HEAD, and neither commit adds a `<<<SLICE` or `<<<END` line. Report both
numstat pairs as READINGS, not predictions.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 122 / 3 / 0, 119 open; expected at HEAD 125 / 4 / 0 → 121 open: three
registrations and one resolution. Report the reading after C1 as well as at HEAD, both symmetric
differences, duplicate-id counts, any resolution naming an unregistered id, and the max and
next-free id.

G5 PLAN PAIR AND ITS NUMBERING, which is the R-0509 repair. PLANF occurs 0 times at HEAD and PLANT
once. Report `.agent/plan.md` sha256, bytes and a line count under 50, with `## Goal` and `## Risks`
byte-IDENTICAL to base. Then parse `## Next Steps` and report the ordered-list numbers it actually
contains: they must read 1, 2, 3, 4 with no repeat — the defect being repaired is that they read
1, 2, 2, 3 at base.

G6 THE R-0506 REPAIR. Over the HEAD blobs of both source files, report the count of each retired
phrase — `NO CALLER`, `ONLY place in the codebase that may invoke subprocess`, and `ONLY function
that executes a subprocess` — each of which must be 0. Then the caller gate, scoped to
`-- packages tests` so no block or state file can match itself:
`git grep -l "from packages.orchestration.exec_guard import" -- packages tests` lists the importing
paths; report the list. `exec_guard.py` claiming an absence this list contradicts is the finding
being closed, so the two readings belong together.

G7 THE SUITES THAT OWN THOSE FILES. `python3 -m pytest
tests/orchestration/test_managed_builder_execution.py tests/orchestration/test_exec_guard.py
tests/orchestration/test_claude_cli_exec_guard.py -q` exits 0 at HEAD with the SAME passed count it
reports at base. Take the base reading at C1, the last commit before C2 changes any source, and
report both numbers.

G8 LINT, scoped and deliberately not repo-wide: `python3 -m ruff check
packages/orchestration/exec_guard.py packages/orchestration/managed_builder_execution.py` exits 0.
A repo-wide `ruff check packages/ tests/` is ALREADY RED at base (UP035 in `dag_schedule.py`, F821
in `gauntlet_injection.py`, F401 and I001 in `test_plan_approval.py`), so it could not fail honestly
for this round and is not ordered.

G9 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0
with 157 passed. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42
passed. Both must match base.

G10 COMMIT HYGIENE, three readings. `git diff --name-only 7185d949..HEAD` measured BEFORE C5 equals
the declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+` column
of `git show --numstat` for C0a, C0b, C1, C2, C3 and C4: none exceeds 500. C5's own count is ordered
nowhere, because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p 7185d949..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its
exit code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C5. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the final push and report its
output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the contradiction and
STOP: never repair text to make a number come out, never widen the change set. Declare every
deviation.
