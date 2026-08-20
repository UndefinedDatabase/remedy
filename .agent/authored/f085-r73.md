── STEP T003 closure prep — F085 · R73 ─────────────────────────────
Goal:        Record the R72 PASS, register the three findings that gate produced, and write the
             feature file's Built State section — so the closure round that follows can touch only
             the paths docs/roadmap/STATUS_closure_protocol.md item 5 allows.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R72 PASS and register R-0567, R-0568 and R-0569 · C3 append the Built State section to
the feature file · C4 handback.

Change:      exactly these paths and nothing else —
             `.agent/authored/f085-r73.md` (new, C0a)
             `.agent/last_block.md` (C0b, verbatim rewrite, AGENTS.md DECISION F104 D1 exempt)
             `.agent/plan.md` (C1, PLAN27F→PLAN27T)
             `.agent/live_review.md` (C2, RECORD42 appended at EOF)
             `docs/roadmap/features/T2_F085.md` (C3, BUILTSTATE appended at EOF)
             `.agent/handoff.md` (C4)
             `.agent/context.md` and `.agent/decisions.md` need no update this round — scope,
             assumptions and constraints are unchanged and no new decision is taken — so they are
             deliberately absent from this change set and their absence is not an omission.

CONVENTION, binding on every count and every proof here, carried verbatim in force from the R72
block. A line count is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS
THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS
LAST CONTENT LINE: extract it as everything after the `BEGIN-` line's own newline up to and including
the newline immediately before the `END-` line, so that `pre + slice` is already a newline-terminated
file and NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIR IS PLAN27. ITS
END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD42 AND BUILTSTATE — listed rather than
counted. Both appends open with an EMPTY first line, which is the blank separator the target needs;
neither target file ends in a blank line, so do not add one.

Constraints:
 1. Apply every slice BYTE-VERBATIM, extracted programmatically from the committed
    `.agent/authored/f085-r73.md` by marker pair under the CONVENTION above. Edit no slice for any
    reason. If a slice looks wrong to you, see constraint 8.
 2. Re-read `.agent/STOP` from disk immediately before C0a and again immediately before C4. If it
    exists at either point, finish only the commit already in flight, write the handback, and stop.
 3. Commit in exactly the order C0a, C0b, C1, C2, C3, C4. C1 advances the plan BEFORE either ledger
    commit, which is what docs/agents/planner_reviewer_prompt.md §3 checklist item 23 requires of a
    round that registers findings. This ordering constraint is also what makes RECORD42's statements
    about this round's own commits true when they are written (§3 checklist item 20, finding R-0524).
 4. `git status --porcelain` is EMPTY after every commit. Any destructive or red-proof check runs
    only inside a disposable `git worktree` under `.remedy-wt/`, never in the primary checkout, and
    the worktree is removed and pruned and its throwaway branch deleted before the handback.
 5. Never force-push. Never work on `main`. Create no PR and merge nothing this round.
 6. Run every suite command in the PRIMARY checkout and SERIALLY, one pytest process at a time: a
    fresh worktree has no `apps/ui/node_modules` and two concurrent pytest processes produce false
    reds in the runtime-bound suites.
 7. Push the branch after C4.
 8. REPORT DISAGREEMENT, DO NOT FIX IT. If any number, path, quotation or claim in this block
    contradicts what you measure, record BOTH readings in the handback under "Deviations &
    assumptions" and change no slice. Three rounds of this feature were saved by a worker doing
    exactly that.
 9. Author no `Done:` and no `Gate:` text of your own anywhere. Those are reviewer-authored strings
    (docs/agents/planner_reviewer_prompt.md §4 item 4); this block already carries every one this
    round needs.

Done when — run each gate, record its REAL exit code and real output, and never report a colour you
did not observe:

 G1 STATE. `.agent/STOP` absent at the two points constraint 2 names. `git status --porcelain` empty
    at round start and after every commit. `git worktree list` one line at the start and one line at
    the end of the round.
 G2 TRANSPORT. After C0b, compute sha256 over all four of: the committed `.agent/authored/f085-r73.md`,
    the committed `.agent/last_block.md`, and both working copies. Report the digest, the byte size,
    the line count and the number of lines that begin with `BEGIN-` or `END-`. All four MUST be equal.
    Then report the budget reading: TOTAL is the block's line count and must be ≤ 490 (DECISION F085
    D6); PROSE is TOTAL minus the sum of the four slices' line counts and must be ≤ 400 (DECISION
    F085 D5); marker lines count as PROSE. Report each slice's line count and sha256 as measured, not
    as predicted.
 G3 SHAPES, one reading per unit, each taken against that commit's OWN pre-commit blob.
    PLAN27F→PLAN27T at C1 is a REWRITE: the containment test the reviewer ran before emission printed
    `TO contains FROM: false`, so order no append proof here. Report FROM occurrences in the
    pre-commit blob (expected 1) and in the post-commit blob (expected 0), TO occurrences in the
    post-commit blob (expected 1), and whether re-applying FROM→TO to the pre-commit blob reproduces
    the post-commit blob BYTE-EXACTLY. RECORD42 at C2 and BUILTSTATE at C3 are EOF appends and take
    ORDERED EQUALITY, which is the obligation §4 item 9 sets for a slice whose lines may recur: the
    pre-commit blob is a byte-exact PREFIX of the post-commit file, the slice is an exact SUFFIX of
    it, `pre + slice` equals the post-commit file byte for byte, and the lines that commit's diff
    ADDS are exactly the slice's lines IN ORDER. Report `git show --numstat <commit> -- <path>` for
    all three commits. Finally report the count of lines beginning `BEGIN-` or `END-` in
    `.agent/plan.md`, `.agent/live_review.md` and `docs/roadmap/features/T2_F085.md` at the tip
    before C4 — markers never reach a target file, so each must be 0.
 G4 DOCS GATES, in the primary checkout, serially, after C3. This round's change set includes
    `docs/roadmap/**`, so BOTH halves run:
      `python3 -m pytest tests/docs/ -q -rf`
      `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
    The reviewer ran both at the base d6d96e50 before ordering them and observed exit 0 with
    `295 passed` and `30 passed` respectively, and ran them once more against a throwaway worktree
    with THIS block's PLAN27T and BUILTSTATE already applied, observing exit 0 and `325 passed` for
    the two together. Report your own exit codes and summary lines. The second half is ordered
    because `tests/docs/` asserts nothing about a feature file's BODY — finding R-0493 proved that by
    red control — so the first half alone would be vacuous for a C3 that edits one.
 G5 STATE READERS, in the primary checkout, serially, after C2. This round rewrites `.agent/` state,
    so the four files that read that state live are gated, exactly as `.agent/context.md` requires:
      `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    The reviewer ran this exact command at d6d96e50 and observed exit 0, `160 passed`.
 G6 PLAN CONTRACT, at the C1 commit. Report `.agent/plan.md`'s line count — it must be ≤ 50 — and
    that `## Goal`, `## Next Steps` and a string matching `\bF\d{3}\b` are all present.
 G7 ARITHMETIC over `.agent/live_review.md`, under DECISION F085 D7: OPEN = REGISTERED − DONE, where
    REGISTERED counts lines matching `^- R-\d+ — ` and DONE counts lines matching `^Done: R-\d+ — `,
    and a `Landed:` line is never subtracted. Report both operands and OPEN at the base d6d96e50 and
    at the tip before C4, plus the symmetric differences of the registered and the done id sets
    between those two SHAs, the count of duplicate registered ids, the count of resolutions naming an
    unregistered id, the maximum registered and maximum resolved id at each SHA, and the next free
    id. The reviewer measured the base itself: 181 registered, 32 done, OPEN 149.
 G8 CANARY, in the primary checkout, serially: `python3 -m pytest tests/cli/test_golden_path.py -q`.
    The reviewer observed exit 0, `42 passed in 22.92s` at d6d96e50.
 G9 HYGIENE. Report `git diff --name-only d6d96e50..<tip before C4>` in full — every path must be one
    of the six this block's Change set names, none may end `.log`, and none may lie under `packages/`,
    `apps/`, `scripts/` or `tests/`. Report the insertion count of each commit BEFORE C4 — each must
    be at most 500 — and confirm every commit in the range is single-parent. C4's own insertion count
    belongs in the round report, not in a gate, because it cannot exist while C4's text is written.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — feature and round,
branch, base SHA d6d96e50 and the per-commit changed-files tables, the item-status table covering
C0a, C0b, C1, C2, C3 and C4 with every item present exactly once, the real verification results for
G1 through G9, the authored-text proofs, external actions, deviations and assumptions, the open-
findings count and the next expected action. Exceed the 60-line cap only if the MANDATED content
genuinely does not fit, and then carry a "Deviations, declared" line naming the actual line count and
the specific mandated content that caused it. Never drop a section to meet the cap.

The handback's state block repeats this Fortschritt line verbatim, label included:

Fortschritt: ~100 % der Bauarbeit. R72 ist gegengeprüft und PASSED — Transport, Slice-Formen,
Arithmetik und das Integration Gate hat der Reviewer selbst nachgemessen statt gelesen, und der
einzige rote Lauf unter vier eigenen Voll-Suite-Läufen ist die xdist-Flake-Klasse, die
docs/agents/integration_gate.md Schritt 4 protokolliert statt blockiert. Diese Runde schreibt nur
noch das Protokoll und den Built State; offen bleibt allein die Closure. Schätzung, gemessen gegen
die Klassentabelle aus Amendment F085 D1.

Next expected action for the reviewer: gate this round, then R74 CLOSURE per
docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the reviewer-authored
STATUS line and README capability sync, and the PR the operator merges at the next Open PR Gate.
────────────────────────────────────────────────────────────────────

BEGIN-PLAN27F
## Current Step
R72, this round: the integration gate re-taken, plus the ledger work R71 left open. R71 PASSED —
its repair is verified and R-0564 is resolved by reviewer text here — and the reviewer's own
arithmetic slip in the R71 block is registered as R-0566 and settled as DECISION F085 D7: the open
count is REGISTERED minus DONE, and a `Landed:` line is an unreviewed fix rather than a resolution.
The gate is re-run because a repair landing after a gate makes that gate's comparison stale.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line authored by the reviewer, and the PR the operator merges at the next Open PR Gate — unless
   this round's gate returns a blocker, in which case its repair round comes first.
END-PLAN27F
BEGIN-PLAN27T
## Current Step
R73, this round: R72's verdict recorded, the findings its gate produced registered, and the feature
file's Built State written — so the closure round that follows touches only the paths
docs/roadmap/STATUS_closure_protocol.md item 5 allows. R72 PASSED: its transport, its slice shapes,
its arithmetic and its integration gate were re-taken by the reviewer rather than read, and the
branch-side full-suite failure the reviewer's own repeated runs produced passes serially, which
docs/agents/integration_gate.md step 4 classifies as the xdist-flake class to record and not to block.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line and the README capability sync authored by the reviewer, and the PR the operator merges at
   the next Open PR Gate.
2. R-0567, R-0568 and R-0569 close as documented risks in that closure under precondition 1 of that
   protocol, rather than by a repair round inside this feature.
END-PLAN27T
BEGIN-RECORD42

Gate: R73 — the R72 entry. R72 PASSED. Every gate its block ordered was re-taken by the reviewer over
f023e2b1..d6d96e50 rather than read from the handback, except the absence of `.agent/STOP` at the two
points R72's constraints name and `git status --porcelain` after each intermediate commit, which are
unobservable once a round has ended and are accepted on the worker's report; both hold observably now,
and `git worktree list` is one line with no `tmp/` branch left behind. TRANSPORT HELD, disk-to-disk,
under the digest fallback of docs/agents/planner_reviewer_prompt.md §4 item 9 rather than against a
scratchpad original, because a self-drive reviewer writes nothing it could later compare against: the
committed `.agent/authored/f085-r72.md`, the committed `.agent/last_block.md` and both working copies,
all read at d6d96e50, are byte-EQUAL at sha256
8deb1e027ffa9a44f0a870c8b780ca7f048f3c1a4e1904eb7625c5f061193383, 29673 B, 374 lines, 12 marker lines;
TOTAL 374 against the 490 cap and PROSE 263 against 400. THE SHAPES HELD, one reading per unit, every
slice re-extracted from that committed file by marker under its own convention rather than retyped:
PLAN26F→PLAN26T over `.agent/plan.md` at 4bbfac80 and LANDEDF→LANDEDT over `.agent/live_review.md` at
0f7e3f7e both read `TO contains FROM: false`, both show FROM 1x pre-commit and 0x post-commit with TO
exactly 1x post-commit, and both reproduce their post-commit blob BYTE-EXACTLY when re-applied.
RECORD41 at 5f592bdd and DECISIOND7 at 2f786299 each satisfy ORDERED EQUALITY against their own
pre-commit blob — PREFIX, SUFFIX and `pre + slice` equal byte for byte. The slice digests recomputed
here agree with every prefix the handback recorded. Marker LINES are 0 in all three edited files at
d6d96e50. THE INTEGRATION GATE HOLDS AND ITS BRANCH HALF WAS RE-RUN, NOT READ: the reviewer ran
`python3 -m pytest -n auto -q` in the primary checkout at d6d96e50 four times, and the first returned
`1 failed, 17131 passed, 19 skipped in 117.44s` while the other three each returned
`17132 passed, 19 skipped`, in 143.94s, 150.09s and 152.08s. The single red id was
`tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome`, which
re-ran SERIALLY at `1 passed in 1.07s` — the xdist-flake class docs/agents/integration_gate.md step 4
records rather than blocks — and R-0569 below carries its mechanism and the reason it is not coupled
to this feature. THE BASE HALF is accepted on the worker's committed evidence rather than re-run, the
reviewer having spent its suite budget on four branch runs instead of one: `comm -13` is empty,
`comm -23` holds five ids, and each of those five is attributed per id by direct evidence in
`.agent/gate_f085_r72/attribution.txt`. THE PROVENANCE HELD: every scratch log named in
`.agent/gate_f085_r72/full_log_provenance.txt` still exists and hashes to exactly the digest recorded
there. THE ARITHMETIC HELD under DECISION F085 D7: 180 registered / 31 done at f023e2b1 and 181 / 32
at d6d96e50, so OPEN is 149 at BOTH SHAs; registered symmetric difference {R-0566}, done symmetric
difference {R-0564}, 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs, max
registered R-0565→R-0566 and max resolved R-0563→R-0564. THE HYGIENE HELD: `git diff --name-only
f023e2b1..d6d96e50` lists fifteen paths, ALL under `.agent/`, none under `packages/`, `apps/`,
`docs/`, `scripts/` or `tests/` and none ending `.log`; the eight commits are single-parent and insert
374, 301, 8, 44, 15, 26, 185 and 107 lines, none over 500. THE PLAN CONTRACT HELD at d6d96e50: 38
lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id all present.

- R-0567 — Low — the R-0566 registration text attributes its own operands to the wrong commit, and the
R72 worker caught it and declared it rather than editing the slice. That paragraph, applied at
5f592bdd, closes with "the correct reading at f023e2b1 is 181 minus 32, that is 149". Measured here by
the reviewer, `.agent/live_review.md` at f023e2b1 holds 180 lines matching the registered-id pattern
and 31 matching the resolved-id pattern, while 181 and 32 are the readings at d6d96e50 — the SHA that
same round produced. The VALUE is right at both SHAs, which is why this is Low: no count anyone reads
is wrong, and DECISION F085 D7, the rule that sentence exists to justify, is untouched by the slip. It
is a finding and not a typo because docs/agents/planner_reviewer_prompt.md §4 item 20 governs exactly
this shape — a slice stating a fact about a file its own block edits — and requires the sentence to
name the commit its reading was taken at; these operands were read at the round's own tip and written
beside the base's SHA. COUNTER-MEASURE, performed by this paragraph and by no rewrite: item 20 rules
that appending a correction is how this record stays honest and that overwriting landed text is worse
than a dated wrong sentence, so the R-0566 paragraph stands exactly as applied and this one carries
the measured operands. OPEN.

- R-0568 — Medium — the guard's `resource_limit` classification never reached the F010 postmortem
taxonomy, while both the feature file's Design section and `.agent/context.md`'s Scope say it would.
Read at d6d96e50: `packages/orchestration/exec_guard.py` sets `classification` to `resource_limit`
with `tripped_limit` naming `wall_timeout`, `cpu_seconds` or `output_bytes`, and that pair lives on
`ExecGuardResult`; `packages/orchestration/failure_postmortem.py` defines `FailureClass` with no
`RESOURCE_LIMIT` member; and the only reader of a trip outside the guard and its own tests is
`packages/orchestration/managed_builder_execution.py`, which tests whether `tripped_limit` equals
`wall_timeout`. `.agent/context.md` at d6d96e50 closes its Scope section with "The tripped limit
becomes an additive `resource_limit` postmortem class". Not High, because nothing false shipped: the
Acceptance section asks for a fixture "killed by its limit and classified resource_limit with the
limit named" and that is met, and `docs/system/exec-guard-limitations-v0.md` claims no postmortem
class anywhere. Not Low, because a stated in-scope item did not ship and only a grep of the enum
reveals it, which is the deliberate-absence class AGENTS.md's discoverability conventions exist for.
NOT FIXED IN THIS FEATURE: adding a member to the F010 enum and teaching its writers to emit it is
production code beyond what remains here, so it closes as a documented risk under precondition 1 of
docs/roadmap/STATUS_closure_protocol.md. The Built State section this round appends to
`docs/roadmap/features/T2_F085.md` states the same absence where a reader would search for it. OPEN.

- R-0569 — Low — the product-smoke zombie check asserts against a FIXED port inside a suite that runs
under `-n auto`, so it can fail on a port a different worker owns. Read at d6d96e50,
`tests/orchestration/test_product_smoke.py` builds its app fixtures with a `port` parameter defaulting
to 5273, and `dev_server.choose_port` returns the requested port when it is free AT CHOOSE TIME and a
fallback otherwise; the check stops each app and then asserts that a connect to each port it used
fails, 0.2 s later. Nothing serialises those cases across xdist workers, so a second worker binding
5273 in the window between one case's teardown and its assertion produces exactly the observed
failure. The reviewer measured the colour rather than assuming it: four `python3 -m pytest -n auto -q`
runs at d6d96e50 in the primary checkout gave one red and three green, and the red id passed serially
at `1 passed in 1.07s`. NOT COUPLED TO F085, measured rather than argued: `git diff --name-only
a5a70621..d6d96e50` names neither `tests/orchestration/test_product_smoke.py` nor
`packages/orchestration/product_smoke.py`, and this branch's edit to `packages/runtimes/dev_server.py`
changes only the cwd, the environment and the `preexec_fn` of the `DevServer` spawn, leaving
`choose_port` and `stop_process_tree` untouched. What was NOT captured is direct evidence of the
concurrent binder — the run log records the assertion and not the other worker — and the
counter-measure does not depend on it. NOT FIXED IN THIS FEATURE: the repair edits a test's content
and belongs with the paydown branch `.agent/context.md` already routes R-0403, R-0448, R-0482, R-0487
and R-0490 to. The obvious repair, for whoever takes it: give the fixture a port chosen per worker
rather than the literal default, or assert only over the port each case actually bound and poll it to
a bounded deadline instead of sampling once at 0.2 s. OPEN.
END-RECORD42
BEGIN-BUILTSTATE

## Built State — what F085 delivered

Read at d6d96e50. The stage-1 execution guard, its per-class policies and the honest limitations
document, with the seam migration spread across the command classes Amendment F085 D1 names.

- `packages/orchestration/exec_guard.py` — `run_guarded` over the policy record `ExecGuardPolicy`.
  Support for each rlimit is decided in the PARENT by `plan_child_spawn`, so an unsupported limit is
  reported rather than dropped in silence, and the `preexec_fn` it returns runs between fork and exec
  applying those limits and nothing else. The wall timeout is the guard's own supervision of the
  child rather than a forwarded `timeout=` keyword — the design constraint Amendment F085 D1 above
  derives from the `Popen` sites that accept no such keyword. Output caps bound what the guard READS.
  A trip classifies as `resource_limit` with `tripped_limit` naming `wall_timeout`, `cpu_seconds` or
  `output_bytes`.
- The per-class policy constructors, one per stage-1 row of the table above as split by Amendments
  F085 D7 and D8: `test_command_exec_policy`, `dod_process_exec_policy`, `dod_app_exec_policy`,
  `runtime_build_exec_policy` and `runtime_server_exec_policy`. The builder class keeps
  `managed_builder_execution._builder_exec_policy`, which the guard cites rather than restates so the
  two cannot drift apart.
- `docs/system/exec-guard-limitations-v0.md`, registered in the doc index `docs/README.md`. It states
  that the network posture is a PROXY posture and never a kernel one, that an allowlist bounds the
  PARENT and not the child's own runtime, that `address_space_bytes` is enforced but deliberately not
  named in `tripped_limit`, and that there is no filesystem fence.

Remedy deliberately does not classify a guard trip in the F010 postmortem taxonomy at d6d96e50:
`resource_limit` is a field on `ExecGuardResult`, `failure_postmortem.FailureClass` has no
`RESOURCE_LIMIT` member at that commit, and the only reader of a trip outside the guard and its own
tests is `managed_builder_execution`, on the `wall_timeout` value of `tripped_limit`. The Acceptance
section above asks for the classification with the tripped limit named and that is what shipped;
finding R-0568 carries the measurement and the risk this feature closes under. The git, packaging and
other call sites stay outside stage 1 by the D1 scope ruling and still spawn unsupervised, which the
limitations document says in its own words.
END-BUILTSTATE
