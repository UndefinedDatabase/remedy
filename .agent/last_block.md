── STEP R10 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R9 PASS, retire the `Landed: R-0500` marker into the reviewer's
resolution, and register the one finding the R9 gate produced. A verdict that is
not written down did not happen (planner_reviewer_prompt.md §4 item 13), and
R9's PASS currently exists nowhere in this repository. No production module is
touched, no test changes, and no behaviour changes. T002a is R11's work: its
block is already drafted and dry-run, and it is NOT started here.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r10.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` := DONE-R0500 replaces LANDED-R0500, then
      += RECORD-R9, then += R0501
  C2  `.agent/plan.md` whole file := the PLAN slice
  C3  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `02043452794972c1f1b87cfe75fad7d3180eedcb`, the R9
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a `<<<SLICE NAME>>>` marker and a
`<<<END NAME>>>` marker, each occupying a line whose ENTIRE content is that
marker. Extract each slice programmatically by those marker LINES and apply it
byte-verbatim; a `<<<` appearing mid-line inside a slice is prose and never a
marker. No marker line ever reaches a target file. The slices are PLAN,
LANDED-R0500, DONE-R0500, RECORD-R9 and R0501. Every slice's bytes end with a
single trailing newline, and a whole-file slice is the COMPLETE file including
it.

Round type: SINGLE-SESSION rules do NOT apply — this is a SPLIT round like every
other in this feature. The change set is `.agent/**` only, but the
single-writer rule of docs/agents/self_drive_protocol.md is unchanged: the
reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r10.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r10.md` and its sha256 is stated in the delegation carrying
   this block; copy that file rather than retyping it (`shutil.copyfile` is fine
   — the gate names the byte property, not the tool). Verify the digest BEFORE
   committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r10.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/live_review.md`, in this order, nothing else in the file
   touched:
   a. replace the LANDED-R0500 slice with the DONE-R0500 slice. This pair is a
      REWRITE: the worker's marker retires into reviewer-authored text
      (planner_reviewer_prompt.md §4 item 4). LANDED-R0500 is the file's last
      line before this commit and occurs exactly once; after the commit it
      occurs zero times.
   b. append the RECORD-R9 slice, preceded by exactly one blank line.
   c. append the R0501 slice, preceded by exactly one blank line.
   One blank line is THIS file's separator convention, stated because it is a
   prose file; the separator a Python source file requires is two, which is a
   different number and is R11's business (R-0500).

4. C2 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats the Fortschritt line of this block's delegation verbatim.
   Under DECISION D15 a stated-cause overage is allowed and its cause is named;
   sections are never dropped to meet the cap. Its "Next" section names, in this
   order, Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read
   `.agent/STOP` from disk — and only THEN the Open PR Gate, because a handoff
   that names the next session's first action must name rule 1 before rule 2.
   That ordering is the fix for R-0501, which this block registers.

Constraints:

1. Never work on `main`; never force-push; no history rewrite; no branch
   deletion. No PR is created and none is merged this round.
2. Apply every slice byte-verbatim. If a slice looks wrong, STOP and say so in
   the handback rather than correcting it — a corrected slice makes the
   reviewer's proof measure text the reviewer never wrote.
3. The change set is exactly `.agent/authored/f085-r10.md`,
   `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
   `.agent/handoff.md`. NOTHING under `packages/`, `tests/`, `docs/`, `apps/` or
   `scripts/`. `.agent/context.md` and `.agent/decisions.md` are deliberately
   NOT updated: scope and constraints are unchanged.
4. Any destructive or red-proof check runs ONLY in a disposable worktree under
   the gitignored `.remedy-wt/`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at every commit. Remove and prune such a
   worktree before the handback.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the
   LAST. If it appears, finish the commit in flight, write the handback and end.
6. Gate scratch (extracted slices, blobs, drafts) goes under `.remedy-wt/` and
   never enters the change set.
7. Record every gate's REAL exit code. "Green" as a word is a finding. If a gate
   is red, stop at that commit, keep what is committed, and report it.

Done when — run each gate from the repository root and report its exact output:

G1  `git status --porcelain` EMPTY before each commit; `.agent/STOP` absent per
    constraint 5; `git worktree list` exactly one line at the handback.
G2  TRANSPORT: sha256 of `.remedy-wt/f085-r10.md`, of the committed
    `.agent/authored/f085-r10.md` and of the committed `.agent/last_block.md` —
    all three EQUAL. Report the one digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD byte-equals the PLAN slice. Report its sha256, byte
    count and line count; confirm `## Goal`, `## Next Steps`, a `\bF\d{3}\b`
    match, and fewer than 50 lines.
G4  C1 SHAPE: the pre-C1 blob with its final LANDED-R0500 line stripped is a
    byte-exact PREFIX of the post-C1 file, and the remainder equals DONE-R0500 +
    one blank line + RECORD-R9 + one blank line + R0501, byte for byte. That
    byte-level property is what proves the shape; report `git show --numstat`
    for the path at C1 as a READING beside it, not as an assertion. Report also
    that LANDED-R0500 occurs 0 times and each of DONE-R0500, RECORD-R9 and
    R0501 exactly once in the WHOLE file at HEAD.
G5  ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `,
    `^Done: R-\d+ — ` and `^Landed: R-\d+`. At base 02043452 the reviewer
    measured 115 registered, 1 resolved, 1 landed. At HEAD: 116 registered, 2
    resolved, 0 landed, so 114 open. REGISTERED symmetric difference HEAD vs
    base = {R-0501} with base minus HEAD empty. RESOLVED symmetric difference =
    {R-0500}. 0 duplicate ids; 0 resolutions naming an unregistered id. Max
    R-0501, next free R-0502.
G6  `.agent/live_review.md` still contains the substring `Steps`; report the
    count, do not assert it.
G7  `git diff --name-only 02043452..HEAD` equals the constraint-3 set minus
    `.agent/handoff.md`, measured before C3 (a handback cannot table itself,
    R-0149/R-0494). Report that it lists 0 paths outside `.agent/`.
G8  UNCHANGED, the honesty gate: sha256 of `packages/orchestration/exec_guard.py`
    and of `tests/orchestration/test_exec_guard.py` at 02043452 and at HEAD are
    pairwise EQUAL. The reviewer measured the guard at
    7dde71c84992af985b28c72d9b460280238721dae474938806f28f9b421b3b67. This round
    changes no code, so no containment claim follows from it.
G9  `python3 -m pytest tests/cli/test_golden_path.py -q` → the canary. The
    reviewer measured `42 passed` at 02043452.
G10 `.agent/` STATE READERS, because this round rewrites `.agent/` state:
    `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q`
    → the reviewer measured `157 passed` at 02043452.
G11 INSERTIONS (the `+` column) per commit for C0a, C0b, C1 and C2 — not for C3,
    whose own count cannot exist while its text is being written (R-0489).
    Report each; none may exceed 500.
G12 HISTORY: `git log --format=%p 02043452..HEAD` shows one parent per commit;
    report the reflog over this round and confirm no amend, rebase, reset,
    branch switch or force-push.

Handback: completion report + rewrite `.agent/handoff.md`. Push after C2 and
again after C3. Then run
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
report its output; create no PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN>>>
# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R10, this round: record the R9 PASS, resolve R-0500 and register R-0501. Pure
record round — no code, no tests, no behaviour, `.agent/` state only.

## Next Steps
1. R11 builds the FIRST half of T002a: environment scrubbing in `exec_guard.py`
   behind an opt-in `env_allowlist`, with a `FORBIDDEN_ENV_KEYS` floor a wrong
   allowlist cannot lower, plus tests for the secret-like variable, the R-0202
   variable and the untouched no-allowlist path.
2. T002a's migration half: the five builder sites of amendment F085 D1 —
   `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208
   and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy
   and behaviour-equality goldens.
3. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
4. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
<<<END PLAN>>>

<<<SLICE LANDED-R0500>>>
Landed: R-0500 — the new test is now separated from the one above it by two blank lines, matching every other test in the file; the edit adds exactly one newline byte and changes no code; `tests/orchestration/test_exec_guard.py`, commit C2 of R9.
<<<END LANDED-R0500>>>

<<<SLICE DONE-R0500>>>
Done: R-0500 — Resolved at R10. The new test is separated from the one above it by
two blank lines, matching every other top-level definition in
`tests/orchestration/test_exec_guard.py`; the fix was commit 76f53036 of R9 and
added exactly one newline byte and no code. The reviewer re-measured the property
at 02043452 rather than reading the claim: the separator list over the whole file
is `[3, 3, 3, 3, 3, 3, 3]` at HEAD against `[3, 3, 3, 3, 3, 3, 2]` at b868401f, and
the file grew from 8134 to 8135 bytes, a difference of exactly one. The
counter-measure the finding names is carried into R11, whose block states the
separator PYTHON requires for the tests it appends, distinguishes it from the
one-blank-line convention that governs this prose file, and measures it directly
instead of resting on a linter that never evaluates the rule. Promoting the
counter-measure into the docs/agents/planner_reviewer_prompt.md §3 checklist
remains a `docs/agents/**` edit outside this feature's change set and is NOT
claimed here; it stays routed to the paydown branch, whose backlog this round's
DECISION D2 calls overdue.
<<<END DONE-R0500>>>

<<<SLICE RECORD-R9>>>
Gate: R9 — PASS, the round that recorded the R8 verdict and fixed the separator the
R8 block got wrong. All fifteen ordered gates were re-run by the reviewer from the
repository root at 02043452 and every one reproduces the handback's reading; the
verdict rests on those runs and not on any earlier session's claim about them, a
distinction that matters because R9's PASS existed nowhere in this repository
until this line. TRANSPORT: the committed `.agent/authored/f085-r9.md` and the
committed `.agent/last_block.md` are byte-EQUAL at sha256
e8011bbab7c5e3cd1817c1566e1112fde16ec47975b65e5cb05a358ff6d6f42d, 23297 B, 263
lines — computed over the COMMITTED files, the digest fallback of §4.9, because
this session did not author that block and holds no scratchpad original of it.
`.agent/plan.md` byte-equals its slice at sha256
83b4a6777d941144520af17a34a3731a16ab650bbc962822f1f17d356971eedb, 2217 B, 39
lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The
two `.agent/live_review.md` commits are pure appends as ordered: the pre-C1 blob is
a byte-exact PREFIX of the post-C1 file with a 7530-byte remainder, the pre-C3 blob
is byte-identical to the post-C1 blob and is a PREFIX of the file at HEAD with a
250-byte remainder, and both numstats carry a deletion column of 0. The open set
moved exactly as ordered: 114 registered / 1 resolved at b868401f against 115 / 1
at HEAD, registered delta exactly {R-0500} with nothing lost, resolved UNCHANGED at
{R-0496} because R9 resolved nothing, 0 duplicate ids, 0 resolutions naming an
unregistered id, and exactly one `^Landed:` record, naming R-0500 — which is what
an unreviewed fix is supposed to look like, and which the commit carrying this
record retires. The substring `Steps` survives 25 times. THE FIX ITSELF, read as a
diff and not as a summary: commit 76f53036 adds ONE blank line before
`@pytest.mark.subprocess` on the file's last test and changes no code, numstat
`1 0`, 8134 B to 8135 B. THE PROPERTY IS MEASURED, NOT ASSERTED: the separator list
runs `[3, 3, 3, 3, 3, 3, 2]` at b868401f and `[3, 3, 3, 3, 3, 3, 3]` at HEAD, so
every decorated test now carries the two blank lines Python separates top-level
definitions by, and the trailing 2 that was the defect is gone.
`packages/orchestration/exec_guard.py` is UNCHANGED across the round at sha256
7dde71c84992af985b28c72d9b460280238721dae474938806f28f9b421b3b67 on both sides, so
R9 added nothing to the module R8 fixed and no containment claim follows from it.
Ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py
-q` at the reviewer's own hand are ten exits of 0 and ten `7 passed` summaries
between 7.60s and 7.66s; ruff is exit 0 under the repository's own configuration
and says nothing about the separator, exactly as the block declared; the canary is
`42 passed in 20.49s`, exit 0; and the eight-file structural sweep is `350 passed,
6 skipped`, exit 0, three times out of three, so R-0499 gained no new observation.
The change set is exactly the six ordered paths with nothing under `docs/`, `apps/`
or `scripts/`. Per-commit insertions are C0a 263, C0b 124, C1 4, C2 1, C3 2 and C4
6, none over 500, and the history is seven single-parent commits 831a2b0c←b868401f
through 02043452 with no amend, rebase, reset or force-push. The values R9 routed
nowhere are recorded HERE, measured by the reviewer at 02043452 (R-0494): the
handback commit 02043452 inserted 43 lines and deleted 47, `.agent/handoff.md`
measures 100 lines against its own DECISION D15 declaration of 100 so its
self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list`
is one line, and origin carries 02043452 with no PR open. The round's five declared
deviations were all checked and all are accurate. LAST_REVIEWED_SHA advances to
02043452.
<<<END RECORD-R9>>>

<<<SLICE R0501>>>
- R-0501 — Low, A HANDBACK NAMED THE NEXT SESSION'S FIRST ACTION WITHOUT NAMING
PHASE 1 RULE 1 BEFORE RULE 2. Raised by the reviewer at the R9 gate against the R9
block, which authored that section. docs/agents/self_drive_protocol.md Phase 2 ends
with a standing requirement on this exact text: "every handoff that names the next
session's first action names Phase 1 rule 1 before rule 2", rule 1 being the
re-read of `.agent/STOP` from disk and rule 2 the Open PR Gate. The R9 handoff's
"Next" section opens with "R10 starts T002a" — a next-session first action — and
among its remaining bullets names the absence of an open PR, which is rule-2
territory, while rule 1 appears nowhere in the file. The requirement exists because
Phase 0 is one-shot while G6 binds at any point, so a sentinel appearing
mid-session stays invisible until an unrelated gate trips over it (R-0347); the
belt-and-braces reminder is what is missing. Severity is Low precisely because
Phase 0 does probe `.agent/STOP` at session start and did so here, finding it
absent, so nothing was actually missed. This is the same family as R-0500 and the
second instance in two rounds: in both, the block author reused a section's
established wording without re-reading the rule that governs that section.
Counter-measure, binding on the reviewer from this round on and demonstrated by the
block that registers this finding: a block ordering a handback's "Next" section
states the rule ORDER that section must carry rather than describing its content,
as change item 5 does here. The recurrence is why this round's DECISION D2 calls
the paydown branch overdue: a counter-measure that cannot be written into
docs/agents/planner_reviewer_prompt.md §3 while a feature branch is open binds only
the block that states it, and this family has now cost two rounds. OPEN.
<<<END R0501>>>
