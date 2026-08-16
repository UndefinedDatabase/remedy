# F085 R14 — record the R13 PASS and register two findings the round measured

Feature T2_F085 Sandbox hardening (stage 1) · Round R14 · Branch feature/f085-sandbox-hardening
Base of this round: the R13 handback commit, `git rev-parse HEAD` at start = ee8e7ba1.
Fortschritt: ~50 % (T001 gebaut · R13 PASS · T002a: erste von fünf Builder-Sites migriert, der
Guard hat seinen ersten Caller · vier Sites, T002b-d, T003 offen).

## Goal

A pure record round: no code, no tests, no behaviour, `.agent/` state only. R13 passed the
reviewer's gate and that verdict is written here, together with the two findings R13's own gates
measured — one defect in the reviewer's block, one stale-text pair the migration falsified.

## Bundle — five commits in this order, none added, dropped or reordered

- C0a `docs(f085): save the R14 step block verbatim` — `.agent/authored/f085-r14.md`
- C0b `docs(f085): mirror the R14 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R13 PASS and register two measured findings` — `.agent/live_review.md`
- C2 `docs(f085): advance the plan to the R14 record round` — `.agent/plan.md`
- C3 `docs(f085): rewrite the handback for R14` — `.agent/handoff.md`

## Change set — exactly these FIVE paths, all under `.agent/`, nothing else

`.agent/authored/f085-r14.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`. Nothing under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`.
`.agent/context.md` and `.agent/decisions.md` are deliberately NOT touched — scope is unchanged.

## Constraints

1. `cp` and the `remedy` CLI are denied: copy with `shutil.copyfile` and prove the BYTE property,
   never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, split by substring, reformatted or reworded: the review slices' regex-looking
   text and backticks are prose and land as prose.
3. Apply the PLAN pair by locating PLANF exactly once and replacing it with PLANT; if it does not
   occur exactly once, STOP and report. This round orders no destructive check, so no disposable
   tree and no worktree operation is needed or permitted.
4. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE RECORD1>>>
Gate: R13 — PASS, the round that gave `exec_guard` its first caller and put one live seam under
supervision. All twelve ordered gates were re-run by the reviewer from the repository root at
ee8e7ba1 and every one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by
digest fallback: the reviewer's `.remedy-wt/f085-r13.md`, the committed
`.agent/authored/f085-r13.md` and `.agent/last_block.md` are byte-EQUAL at sha256
e7f57d218a3bb2418b744753b46e667cfa8cf6e2ab22f43342e672c2eb865808, 23370 B, 400 lines — AT the
DECISION F105 D5 block cap, not over it. C1 IS A PURE APPEND: the pre-C1 blob is a byte-exact
PREFIX of the post-C1 file, HEAD equals it, and the 3777-byte remainder is exactly RECORD-R12 and
R-0504, each occurring ONCE. THE ARITHMETIC: 118 / 3 / 0 at base against 119 / 3 / 0 at HEAD, so
the open set rose 115 to 116 by exactly one registration against no resolution, with nothing lost,
no duplicate id and no resolution naming an unregistered id. THE CHANGE ITSELF, read as a diff:
`run_managed_builder` no longer calls `subprocess.run`; it calls `run_guarded` under a
`_builder_exec_policy` that sets the wall deadline, the per-stream output cap, the cwd pin, a zero
core dump and `env_allowlist=tuple(sorted(env))` — an identity over an already-sanitized env that
adds `FORBIDDEN_ENV_KEYS` as a floor — and deliberately leaves `cpu_seconds`,
`address_space_bytes` and `open_files` None with the reason written where a reader will look. A
wall trip is re-raised as `subprocess.TimeoutExpired` so the module's existing timeout path is
reached unchanged, and the result is wrapped in a `subprocess.CompletedProcess` so every
downstream reader keeps its shape; `_guarded_exit_code` rebuilds the -SIGNUM form the guard
reports as a NAME. BEHAVIOUR EQUALITY WAS MEASURED, NOT ASSERTED: before ordering the block the
reviewer ran six paired probes against base and HEAD — echo, false, a 1s wall timeout, a missing
command, an over-cap output and a SIGKILL suicide — and all six agree on status, exit code, stored
output length and safe summary, including exit_code -9 on both sides and a child environment of
exactly the eight sanitized keys with `GITHUB_TOKEN` absent. FOUR RED CONTROLS were decisive, each
reddening EXACTLY its own test and nothing else, and the reviewer re-ran control (b) itself
against the COMMITTED code in an isolated extraction: restoring the direct spawn reddens the AST
test, disabling the wall re-raise reddens the timeout test, returning the raw returncode reddens
the signal test, and dropping `env_allowlist` reddens the policy test. At HEAD the suite is
132 passed against 129 at base, `test_exec_guard.py` is 12 passed unchanged, ruff is exit 0 for
both files at base AND at HEAD, the canary is 42 passed and the four state readers are 157 passed.
THE CALLER GATE, scoped to `-- packages tests` so no block file can match itself: ONE path at base
and THREE at HEAD, adding the module and its test — the guard's no-caller era is over.
`.agent/plan.md` is 42 lines under its 50-line cap with `## Goal` and `## Risks` byte-IDENTICAL to
base. The change set is exactly the seven declared paths with 0 outside; insertions are 400, 391,
42, 124 and 8, none over 500; the history is six single-parent commits with no amend, rebase,
reset or force-push; `git status --porcelain` is EMPTY and `git worktree list` is ONE line; and
`.agent/handoff.md` measures 95 lines against its own declaration of 95. The round's seven
declared deviations were all checked and all are accurate — deviation 7 correctly caught a stale
numeral in the dispatching brief, which named fourteen gates where the block numbers twelve; the
block governed and all twelve ran. LAST_REVIEWED_SHA advances to the R13 handback commit.
<<<END RECORD1>>>

<<<SLICE FIND1>>>
- R-0505 — Medium, TWO CLAUSES OF ONE BLOCK ORDERED INCOMPATIBLE THINGS, AND THE WORKER HAD TO
SPEND A DEVIATION CHOOSING BETWEEN THEM. Raised by the reviewer at the R13 gate against its own
R13 block. Gate G8 of that block ordered the four red controls to run "in a DISPOSABLE worktree
under `.remedy-wt/`", which is what docs/agents/self_drive_protocol.md G5 requires of destructive
verification. Constraint 3 of the SAME block said "No worktree is added, removed or pruned", and
gate G1 ordered `git worktree list` to print ONE line. No execution satisfies all three. The
constraint was correct for the round the block STARTED as — a record round plus a migration, with
no destructive check — and was never revisited when the red controls were added to the gate list
later in authoring. The worker resolved it in favour of the hard constraints, extracting
`git archive HEAD` into a gitignored directory instead of adding a worktree, proved the isolation
and the import path inside that copy, deleted it afterwards, and declared the whole thing. That is
the right call and the right report, and the round was not damaged; what it cost was a deviation
spent on the reviewer's bookkeeping. This is the family the F083 R9 lesson names — clause-versus-
clause is the gap a per-clause checklist misses, because each clause is individually correct and
only the PAIR is wrong. Counter-measure, binding on the reviewer from this round on: when a gate
is added to a drafted block, re-read the CONSTRAINTS section against it before emission, and state
in the constraint itself which gates are exempt from it rather than writing an absolute. A block
that permits no disposable tree must not also order one. OPEN.
<<<END FIND1>>>

<<<SLICE FIND2>>>
- R-0506 — Medium, A MIGRATION FALSIFIED TWO DOCUMENTED ABSENCE CLAIMS AND LEFT BOTH STANDING.
Raised by the reviewer at the R13 gate; the round MEASURED and reported both, exactly as its gate
G12 ordered, and deliberately fixed neither. (1) `packages/orchestration/exec_guard.py` states
under "Deliberate absences, written here because text search cannot find code that does not
exist" that "NO CALLER. Nothing in this repository imports this module yet", and that choosing an
allowlist per command class "is not done here". Both were true until R13 and are FALSE at
ee8e7ba1: the scoped import grep names three paths, and `_builder_exec_policy` chooses exactly
such an allowlist. (2) `packages/orchestration/managed_builder_execution.py`'s module docstring
calls itself "the ONLY place in the codebase that may invoke subprocess for builder execution" and
promises "shell=False ALWAYS", and `run_managed_builder`'s own docstring repeats it; the spawn is
now `run_guarded`'s `subprocess.Popen`, which passes no `shell` keyword at all. The second text is
the one that MADE R-0504 possible — a docstring sentence a source-text test could satisfy — so
leaving it in place while its test has been replaced is the sharper half of this finding. Neither
was fixed at R13 because `exec_guard.py` sits outside that round's declared change set and the
docstring rewrite belongs with the four remaining builder sites, where the same sentences must be
corrected once rather than twice. This is the R-0417 staleness family: a claim of ABSENCE has a
lifetime, and the commit that ends it is the commit that owes the correction. R14 registers it;
the R15 migration round must carry the fix for both files in its change set and gate the property
that neither file claims an absence the caller gate contradicts. OPEN.
<<<END FIND2>>>

<<<SLICE PLANF>>>
## Current Step
R13, this round: record the R12 PASS, register R-0504, and migrate the FIRST of
T002a's five builder sites — `managed_builder_execution.py`:1160 — onto
`run_guarded` under a stage-1 builder policy, with behaviour-equality tests.
`exec_guard` gains its first caller in the running system.

## Next Steps
1. T002a's four REMAINING builder sites of amendment F085 D1 —
   `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to
   `run_guarded` the same way `managed_builder_execution.py` did at R13, each with
   its own behaviour-equality goldens.
<<<END PLANF>>>

<<<SLICE PLANT>>>
## Current Step
R14, this round: record the R13 PASS and register R-0505 and R-0506 — a clause
contradiction in the reviewer's own R13 block, and the two absence claims the R13
migration falsified. Pure record round: no code, no tests, `.agent/` state only.

## Next Steps
1. T002a's four REMAINING builder sites of amendment F085 D1 —
   `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to
   `run_guarded` the way `managed_builder_execution.py` did at R13, each with its
   own behaviour-equality goldens. That round also carries R-0506's fix: the stale
   absence claims in `exec_guard.py` and `managed_builder_execution.py`.
<<<END PLANT>>>

## Application order

C1 appends RECORD1, then FIND1, then FIND2 to `.agent/live_review.md`, each preceded by exactly
one blank line, appending only — never rewriting a byte already there. C2 applies PLANF→PLANT to
`.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit
code as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before each of the five commits; `.agent/STOP` re-read
from disk before the first and last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r14.md` after C0a, `.agent/last_block.md` after C0b and the
reviewer's original are byte-EQUAL: report one sha256, the byte length and the line count for all
three. C0b copies the COMMITTED C0a blob, never the scratch file.

G3 C1 SHAPE. The pre-C1 blob is a byte-exact PREFIX of the post-C1 file; HEAD equals it; the
remainder is byte-equal to blank + RECORD1 + blank + FIND1 + blank + FIND2, in that order; each of
the three slices occurs exactly ONCE in the whole file at HEAD. Report C1's numstat pair as a
READING, not a prediction.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 119 / 3 / 0, 116 open; expected at HEAD 121 / 3 / 0 → 118 open, a rise of
exactly two from two registrations against no resolution. Report both symmetric differences,
duplicate-id counts, any resolution naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF is a REWRITE: it occurs 0 times at HEAD and PLANT once. Report `.agent/plan.md`
sha256, bytes and a line count under 50, with `## Goal` and `## Risks` byte-IDENTICAL to base and
`## Current Step` and `## Next Steps` not.

G6 THE HONESTY GATE. This round changes NO code, so no containment claim follows from it.
`packages/orchestration/exec_guard.py`, `packages/orchestration/managed_builder_execution.py` and
`tests/orchestration/test_managed_builder_execution.py` are byte-IDENTICAL between base and HEAD:
report the sha256 of each at both ends.

G7 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0
with 157 passed. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with
42 passed. Both must match base.

G8 COMMIT HYGIENE, three readings. `git diff --name-only <base>..HEAD` measured BEFORE C3 equals
the five declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+`
column of `git show --numstat` per commit: none exceeds 500, and C3's own count is ordered nowhere
because a handback cannot measure the commit that writes it. `git log --format=%h %p <base>..HEAD`
shows ONE parent per commit and a linear chain, and `git reflog` shows every entry prefixed
`commit:` with no amend, rebase, reset, branch switch or force-push.

## Done when

All five commits exist in order, the branch is pushed, every gate has been RUN with its real exit
code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C3. Run `gh pr
list --state open --json number,headRefName,baseRefName,isDraft` after the final push and report
its output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate
whose result you did not read is a finding. If a gate contradicts this block, report the
contradiction and STOP: never repair text to make a number come out, never widen the change set.
Declare every deviation with its reason.
