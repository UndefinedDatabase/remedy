── STEP R12 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R11 PASS, resolve R-0501, and register the two gate defects the R11
gate found in the reviewer's OWN block. A verdict that is not written down did not
happen (planner_reviewer_prompt.md §4 item 13), and this session began by finding
R9's PASS stranded off-disk — this round exists so R11's is not. No production
module is touched and no behaviour changes.

Base: `0406ceba`, the R11 handback commit and the tip of
`feature/f085-sandbox-hardening`. Every range gate names that SHA. Stay on this
branch; create no other.

Bundle (ordered, one commit each; none added, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r12.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` += RECORD-R11, DONE-R0501, R0502, R0503
  C2  `.agent/plan.md` := the PLAN pair applied
  C3  rewrite `.agent/handoff.md` (the handback)

Slice convention:
Each authored unit sits between a `<<<SLICE NAME>>>` and a `<<<END NAME>>>` marker,
each occupying a line whose ENTIRE content is that marker. Extract slices by those
marker LINES programmatically and apply byte-verbatim; a `<<<` mid-line inside a
slice is prose, and no marker line reaches a target file. The slices are RECORD-R11,
DONE-R0501, R0502, R0503 and the FROM/TO halves of PLAN, each ending with a single
trailing newline.

Round type: SPLIT, as every round of this feature is. The change set is `.agent/**`
only, but the single-writer rule of docs/agents/self_drive_protocol.md is unchanged:
the reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block byte for byte to `.agent/authored/f085-r12.md`.
   The reviewer's original is at `.remedy-wt/f085-r12.md` and its sha256 is in the
   delegation; COPY that file rather than retyping it (`shutil.copyfile` is fine —
   the gate names a byte property, not a tool). Verify the digest, then commit alone.
2. C0b — copy the COMMITTED `.agent/authored/f085-r12.md` over
   `.agent/last_block.md`, whole file. Commit alone.
3. C1 — append to `.agent/live_review.md`, in this order, each preceded by exactly
   one blank line, byte-verbatim, nothing else in the file touched: RECORD-R11, then
   DONE-R0501, then R0502, then R0503. All four are APPENDS — unlike R10's C1 there
   is no `Landed:` line to retire, because R11 fixed no registered finding. The
   pre-C1 content must remain a byte-exact PREFIX of the post-C1 content, and the
   numstat deletion column must therefore be 0.
4. C2 — apply the PLAN pair to `.agent/plan.md`, a REWRITE spanning `## Current
   Step` only; `## Goal`, `## Next Steps` and `## Risks` are NOT touched and must
   come through byte-identical. Commit alone.
5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its state
   block repeats the delegation's Fortschritt line verbatim. A DECISION D15
   stated-cause overage is allowed with its cause named; sections are never dropped
   to meet the cap. Its "Next" section names, in order, Phase 1 rule 1 of
   self_drive_protocol.md — re-read `.agent/STOP` — and only THEN the Open PR Gate.

Constraints:

1. The guardrails G1-G8 of docs/agents/self_drive_protocol.md bind unchanged and
   this block restates none of them — read that file before you start. Beyond them:
   no PR is created and none is merged this round; `.agent/STOP` is re-read from
   disk before the FIRST and again before the LAST commit; and all gate scratch
   lives under the gitignored `.remedy-wt/` and never enters the change set.
2. Apply every slice byte-verbatim. If a slice looks wrong, STOP and say so in the
   handback rather than correcting it — a corrected slice makes the reviewer's proof
   measure text the reviewer never wrote.
3. The change set is exactly `.agent/authored/f085-r12.md`, `.agent/last_block.md`,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. NOTHING under
   `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`. `.agent/context.md` and
   `.agent/decisions.md` are deliberately NOT updated: scope is unchanged.

Done when — run each gate from the repository root and report its exact output:

G1  `git status --porcelain` EMPTY before each commit; `.agent/STOP` absent per
    constraint 1; `git worktree list` exactly one line at the handback.
G2  TRANSPORT: sha256 of `.remedy-wt/f085-r12.md`, the committed
    `.agent/authored/f085-r12.md` and the committed `.agent/last_block.md` — all three
    EQUAL. Report the one digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD: report sha256, bytes and lines; confirm `## Goal`,
    `## Next Steps`, a `\bF\d{3}\b` match, under 50 lines, and that `## Goal`,
    `## Next Steps` and `## Risks` are byte-identical to their text at 0406ceba.
G4  C1 SHAPE: the pre-C1 blob is a byte-exact PREFIX of the post-C1 file, and the
    remainder equals one blank line + RECORD-R11 + blank + DONE-R0501 + blank +
    R0502 + blank + R0503, byte for byte. Report `git show --numstat` for the path
    at C1 beside this as a READING; its deletion column is 0 because C1 only appends.
    Report also that each of the four slices occurs exactly once in the WHOLE file
    at HEAD.
G5  ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `,
    `^Done: R-\d+ — ` and `^Landed: R-\d+`. At base 0406ceba the reviewer measured
    116 registered, 2 resolved, 0 landed. At HEAD: 118 registered, 3 resolved, 0
    landed, so 115 open. REGISTERED symmetric difference HEAD vs base = {R-0502,
    R-0503} with base minus HEAD empty. RESOLVED symmetric difference = {R-0501}.
    0 duplicate ids; 0 resolutions naming an unregistered id. Max R-0503, next free
    R-0504. The open count RISES by one this round; report it as measured.
G6  `.agent/live_review.md` still contains the substring `Steps`; report the count,
    do not assert it.
G7  `git diff --name-only 0406ceba..HEAD` equals the constraint-3 set minus
    `.agent/handoff.md`, measured before C3 (R-0149, R-0494). Report every path, and
    that 0 paths fall outside `.agent/`.
G8  UNCHANGED, the honesty gate: sha256 of `packages/orchestration/exec_guard.py`
    and `tests/orchestration/test_exec_guard.py` at 0406ceba and at HEAD are pairwise
    EQUAL. This round changes no code, so no containment claim follows from it.
G9  `python3 -m pytest tests/cli/test_golden_path.py -q` → the canary; the reviewer
    measured `42 passed` at 0406ceba. Then, this round rewriting `.agent/` state:
    `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q`
    → the reviewer measured `157 passed` at 0406ceba.
G10 INSERTIONS (the `+` column) per commit for C0a, C0b, C1 and C2 — not C3, whose
    own count cannot exist while its text is written (R-0489). None may exceed 500.
G11 HISTORY: `git log --format=%p 0406ceba..HEAD` shows one parent per commit; report
    the reflog and confirm no amend, rebase, reset, branch switch or force-push.

Handback: completion report + rewrite `.agent/handoff.md`. Push after C2 and again
after C3, then run
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`, report its
output and create no PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLANF>>>
## Current Step
R11, this round: the FIRST half of T002a — environment scrubbing in
`exec_guard.py` behind an opt-in `env_allowlist`, with a `FORBIDDEN_ENV_KEYS`
floor a wrong allowlist cannot lower. No call site is migrated, so the running
system gains nothing yet and no containment claim follows from this round.
<<<END PLANF>>>

<<<SLICE PLANT>>>
## Current Step
R12, this round: record the R11 PASS, resolve R-0501 and register R-0502 and
R-0503 — two gate defects the reviewer wrote into its own R11 block. Pure record
round: no code, no tests, no behaviour, `.agent/` state only.
<<<END PLANT>>>

<<<SLICE RECORD-R11>>>
Gate: R11 — PASS, the round that gave `exec_guard` an opt-in environment allowlist
with a floor beneath it. All thirteen ordered gates were re-run by the reviewer from
the repository root at 0406ceba and every one reproduces the handback's reading.
TRANSPORT, disk-to-disk against the reviewer's OWN scratchpad original and NOT by
digest fallback (§4.9): `.remedy-wt/f085-r11.md`, the committed
`.agent/authored/f085-r11.md` and the committed `.agent/last_block.md` are byte-EQUAL
at sha256 0ac925d29a4c537683a695d732ed4d4af62e600ed7486d7d0d762514715a469b, 19176 B,
400 lines — at the 400-line block cap of DECISION F105 D5, not over it. `.agent/plan.md`
is sha256 699172bfed0791f5ab282384ef8f669c26249c6418ddc4fdd7a8c1688edd361a, 2446 B, 42
lines, under the 50-line cap, and the PLAN pair did what a narrowed pair is for: the
`## Goal` and `## Risks` sections are byte-IDENTICAL to their text at 2587780d, the
`## Next Steps` list renumbers contiguously 1-2-3 with no orphaned entry, and PLANF
occurs 0 times against PLANT once. ALL TEN pair shapes read exactly as declared over
the whole of each target file: FROM 0 / TO 1 for the rewrites PLAN, GUARD1, GUARD2,
GUARD4, GUARD6 and TEST1, and FROM 1 / TO 1 for the appends GUARD3, GUARD5, GUARD7 and
TEST2, with NEWTESTS occurring once and the test file ending with it. THE CHANGE
ITSELF, read as a diff and not as a summary: `FORBIDDEN_ENV_KEYS` is a frozenset whose
members and spelling match `managed_builder_execution._FORBIDDEN_ENV_KEYS`;
`scrub_child_env` intersects a caller's allowlist with the source mapping AFTER
subtracting that floor, so an allowlist naming a secret cannot lower it, and an
allowlisted key the source never defined is absent rather than empty; `env_allowlist`
is a new frozen-dataclass field defaulting to None; and `run_guarded` computes
`child_env` from `os.environ` or from `policy.env` ONLY when the allowlist is not
None, so the T001 pass-through contract is byte-for-byte unchanged when it is. The
module docstring's absence note was narrowed rather than deleted, and a new paragraph
states the honest limit a reader would otherwise have to discover: an allowlist bounds
what the PARENT hands over and never what the child's runtime adds back, a CPython
child setting `LC_CTYPE` itself under PEP 538 locale coercion, so the child's
environment is a SUPERSET of the scrubbed one. That paragraph is why the tests
subtract an interpreter-added key instead of asserting an exact environment — the
reviewer hit that exact failure in its own pre-emission dry run, which is what a dry
run is for. THE PROPERTY IS MEASURED, NOT ASSERTED: before ordering the block the
reviewer ran three red controls in a disposable worktree and each was decisive —
dropping the `FORBIDDEN_ENV_KEYS` subtraction reddens exactly
`test_a_secret_like_variable_never_reaches_the_child_even_when_allowlisted`; scrubbing
unconditionally reddens eight tests including every T001 fixture, which is what proves
the None path load-bearing; and returning `""` for an undefined key reddens exactly
`test_scrub_child_env_drops_a_key_the_source_never_defined`. Restored, the suite is
green again. At HEAD the reviewer's own ten consecutive runs of `python3 -m pytest
tests/orchestration/test_exec_guard.py -q` are ten exits of 0 and ten `12 passed`
summaries between 7.71s and 7.79s — 12 against the 7 of R9, the five new tests. The
import path was verified in the same session (`m.__file__` resolves inside the primary
checkout and both new names are present), because a shell cwd that had silently
persisted into a worktree is a real failure mode this session hit. Ruff is exit 0 for
both files under the repository's own configuration, and the worker took the same
reading at base BEFORE touching either file, so the green is unchanged rather than
newly earned. The canary is `42 passed in 20.46s` and the four `.agent/` state readers
are `157 passed in 19.74s`, both matching base. THE HONESTY GATE HOLDS, by a corrected
measurement: the only TRACKED `.py` file containing the string `exec_guard` is the test
file, and no tracked module imports `packages.orchestration.exec_guard`, so NO call
site was migrated and nothing in the running system is scrubbed by this round. The
change set is exactly the six ordered paths. Per-commit insertions are C0a 400, C0b
358, C1 145 and C2 7, none over 500; the history is five single-parent commits
a1726eb7←2587780d through 0406ceba with no amend, rebase, reset or force-push; and
`git status --porcelain` is EMPTY with one worktree. `.agent/handoff.md` measures 90
lines against its own DECISION D15 declaration of 90, so its self-measurement is
honest. The round's six declared deviations were all checked and all are accurate; two
of them report defects in the REVIEWER's gates rather than in the work, and the worker
was right to report them as measured instead of repairing text to make a number come
out — they are registered here as R-0502 and R-0503 rather than held against the round.
LAST_REVIEWED_SHA advances to 0406ceba.
<<<END RECORD-R11>>>

<<<SLICE DONE-R0501>>>
Done: R-0501 — Resolved at R12. The counter-measure has now been applied twice on disk
and verified by the reviewer both times: the R10 handback's "Next" section opens with
"FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read
`.agent/STOP` from disk" and only then reaches the Open PR Gate, and the R11 handback
does the same. Both blocks ordered that ORDER explicitly rather than describing the
section's content, which is the counter-measure the finding named. The rule the R9
handback missed — Phase 2's "every handoff that names the next session's first action
names Phase 1 rule 1 before rule 2" — is therefore satisfied by the two most recent
handbacks, and the belt-and-braces reminder exists again for the next session that
resumes cold. Promotion of the counter-measure into the
docs/agents/planner_reviewer_prompt.md §3 checklist stays a `docs/agents/**` edit
outside this feature's change set and is NOT claimed here; it remains routed to the
paydown branch, which this feature's DECISION D2 calls overdue.
<<<END DONE-R0501>>>

<<<SLICE R0502>>>
- R-0502 — Low, A REVIEWER GATE ASKED grep FOR A STRING THE TARGET FILE CANNOT
CONTAIN, MAKING ITS EXPECTED RESULT UNREACHABLE. Raised by the reviewer at the R11
gate against its own R11 block. Gate 11 of that block ordered
`grep -rln "exec_guard" packages apps scripts tests` and declared that it "names
exactly two paths — `packages/orchestration/exec_guard.py` and
`tests/orchestration/test_exec_guard.py`". `grep -l` matches file CONTENT, and
`exec_guard.py` does not contain the string `exec_guard` anywhere in its own source,
so the module could never appear in that output — at 2587780d exactly as at HEAD. The
declared result was unreachable when the gate was written, not broken by the round.
The worker did the right thing: it reported the gate as measured, named the cause,
demonstrated the underlying property by a different route, and changed nothing to make
the number come out. This is the R-0371 family — a gate that cannot be satisfied by
any honest run — and the neighbouring R-0438 case, where a path that did not resolve
made a gate silently vacuous; here the gate was loud rather than vacuous, which is why
it cost only a deviation. The PROPERTY the gate exists for does hold, by the corrected
measurement the reviewer ran at the gate: intersected with `git ls-files`, the only
tracked `.py` file containing `exec_guard` is `tests/orchestration/test_exec_guard.py`,
and no tracked module imports `packages.orchestration.exec_guard`, so no call site was
migrated. Counter-measure, binding on the reviewer from this round on: a no-caller gate
names the IMPORT statement over TRACKED files —
`git grep -ln "from packages.orchestration.<module> import"` — and never a bare
filename grep, because a module's own name is the one string its source is least likely
to contain, and untracked `__pycache__` artifacts otherwise pollute the result. OPEN.
<<<END R0502>>>

<<<SLICE R0503>>>
- R-0503 — Low, AN "EXACTLY ONCE AMONG THE ADDED LINES" PROOF IS UNSATISFIABLE FOR
STRUCTURAL LINES. Raised by the reviewer at the R11 gate against its own R11 block.
Gate 4 ordered, for each append-shaped pair, that "each TO-ONLY added line" occur
"exactly once AMONG THE LINES THAT COMMIT ADDS", quoting
docs/agents/planner_reviewer_prompt.md §4 item 9. Applied literally that is unmeetable
whenever a TO adds more than one blank line or more than one bare `"""`, which every
multi-definition Python slice does: R11's C1 added six blank lines to `exec_guard.py`,
twenty-three to the test file, and two bare docstring terminators. The worker met the
gate for every CONTENT-carrying line — GUARD3 18/18, GUARD5 1/1, GUARD7 5/5, TEST2
16/16, zero content strays — and enumerated the structural repeats instead of
filtering them out of sight, which is the honest reading and the one the reviewer
accepts. The §4 item 9 rule was written for prose files, where a repeated line is a
real signal that a slice landed twice; in a source file a repeated blank line carries
no information at all. This is the same shape as R-0253, which already had to bend the
whole-file version of this count because a TO legitimately repeats a sentence the file
already carries — the rule bends, never the text. Counter-measure, binding on the
reviewer from this round on: an "exactly once among the added lines" gate over a
SOURCE file scopes itself to lines that are not blank and not a bare docstring
delimiter, and says so in the gate rather than leaving the worker to discover the
exception and spend a deviation on it. Whether §4 item 9 itself should carry that
carve-out is a `docs/agents/**` edit outside this feature's change set and is NOT
claimed here; it is routed to the paydown branch with R-0502. OPEN.
<<<END R0503>>>
