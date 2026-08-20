── STEP R3 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R2 PASS, register R-0492, and leave the branch on a clean session
boundary. This is a RECORD round: no inventory work, no production code, no
test content, no `docs/` file.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r3.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` whole file := the PLAN slice
  C2  `.agent/live_review.md` += the RECORD-R2 slice, then the R0492 slice
  C3  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `2d492d49967b29dbc4aad852c11c624ecf372cad`, the R2
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R2 and R0492. Every slice's bytes end with a single
trailing newline, and the whole-file slice is the COMPLETE file including it.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r3.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r3.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r3.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

4. C2 — append to `.agent/live_review.md`, in this order, each preceded by
   exactly one blank line, both byte-verbatim, nothing else touched in the file:
   a. the RECORD-R2 slice;
   b. the R0492 slice.
   The pre-C2 file content must remain a byte-exact PREFIX of the post-C2 file.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~6 % (F085 beansprucht · Seam-Inventar erstellt und abgenommen · T001/T002/T003 offen) — Schätzung`
   Its "Next" section states exactly this, because the session ends here and the
   handoff is the only return channel:
   - the next session's FIRST action is Phase 1 rule 1 of
     docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk —
     and only then rule 2, the Open PR Gate;
   - there is NO open PR for this branch and none is opened before closure;
   - R4 is the next round: it writes the `docs/roadmap/features/T2_F085.md`
     amendment DECISION F085 D1 names, and rules the stage-1 command classes
     and their policies. R4 touches `docs/roadmap/**`, so its gate list adds
     `python3 -m pytest tests/docs/ -q`;
   - the R3 verdict itself lives only in this file, the reviewer's round report
     and the PR, because the last round of a branch has no on-disk gate entry
     by construction (docs/agents/planner_reviewer_prompt.md §4 item 13). That
     absence is the TERMINATOR and no repair round opens to close it.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the five in the ordered bundle. No
   production code, no test file, no `docs/` file, and NOT
   `.agent/f085_inventory.md`, which R2 closed and R3 does not revise.
4. Never force-push, never rebase, never amend, never reset, never work on
   `main`, never delete a branch. Do not create a PR.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent.
G2  TRANSPORT: `.remedy-wt/f085-r3.md`, the committed `.agent/authored/f085-r3.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256
    and line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b`
    match, and is under 50 lines.
G4  `.agent/live_review.md`: the pre-C2 content is a byte-exact PREFIX of the
    post-C2 content, and the appended tail contains the RECORD-R2 slice and the
    R0492 slice, each byte-verbatim and each exactly once. Report
    `git show --numstat` for that path at C2 and confirm its deletion column
    is 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, `Landed:`, duplicate ids and
    resolutions naming an unregistered id. REQUIRED: the set of OPEN ids equals
    the set open at `2d492d49` PLUS exactly `R-0492`; report both counts rather
    than predicting them, plus the max id and the next free id.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `.agent/f085_inventory.md` is BYTE-IDENTICAL to its content at `2d492d49`.
    Report the sha256 at both commits; they must be equal.
G8  `git diff --name-only 2d492d49..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f085-r3.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`.
    Report the real list and flag any difference rather than editing to match.
    In particular no path under `packages/`, `apps/`, `tests/`, `scripts/` or
    `docs/` may appear.
G9  `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
    → exit 0. Run in the PRIMARY checkout, not a worktree: the reviewer measured
    `157 passed`, exit 0, at the R2 head, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`
    because `apps/ui/node_modules` is gitignored and absent there — the known
    R-0480 mechanism, not a base red.
G10 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at the R2 head. `tests/docs/` is NOT
    gated this round because no `docs/` path is in the change set.
G11 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1 and C2 only. None may exceed 500. C3's own insertion count cannot
    exist while C3's text is being written, so it is reported in your FINAL
    MESSAGE — the round report — and not in this file.
G12 `git log --format=%p 2d492d49..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` entries — no amend,
    rebase, reset, checkout of another branch, or force-push.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

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
R3, this round: record the R2 PASS, register R-0492, and close the session on a
clean boundary. The seam inventory `.agent/f085_inventory.md` is complete and
accepted; it is not revised again.

## Next Steps
1. R4 — write the `docs/roadmap/features/T2_F085.md` amendment that DECISION
   F085 D1 names, correcting the "small number of helpers" premise the
   inventory disproved, and rule the stage-1 command classes and their policies.
   R4 changes `docs/roadmap/**`, so its gate list adds `tests/docs/`.

## Risks
- T002's seam migration is scoped against a premise the inventory disproved: 67
  real call sites in 56 enclosing functions, of which the four helpers the
  feature file names cover 24. R4 re-slices before any code is written.
- R-0202 has one reader and two seams that provably drop the variable. Naming
  them is not fixing them, and no round may fix them outside T002.
<<<END PLAN>>>

<<<SLICE RECORD-R2>>>
Gate: R2 — PASS. All sixteen ordered gates reproduce at the reviewer's own hand, from the repository root at 2d492d49, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r2.md`, the committed `.agent/authored/f085-r2.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 d5db9ebcc977024df569710a2cb7528f4311b735a6e8cf380d72ffd6aecbd139, 20720 B, 264 lines. The C2 append is honest: the pre-C2 blob of 190930 B is a byte-exact PREFIX of the 196461 B post-C2 file, the RECORD-R1 and R0491 slices each occur exactly once inside the appended tail, the numstat is `4 0` with a zero deletion column, and no transport marker reached any file. The open set moves by exactly one: 105 open at the base, 106 at HEAD, the set comparison against the base set plus R-0491 has an EMPTY symmetric difference, 0 duplicate ids and 0 resolutions naming an unregistered id, next free R-0492. THE INVENTORY WAS RE-DERIVED, NOT READ: the reviewer ran the block's own grep at HEAD, got 73 sites, and found the table's 73 rows equal to it as a SET with an empty symmetric difference; then re-parsed every one of the 33 files with an independent AST walk and re-computed all six keyword columns from each call's own keywords, agreeing on 73 of 73 rows; then re-derived the class partition, finding all seven headings inside the closed vocabulary, every declared per-class count equal to the count actually listed under it, the seven counts summing to 73, every site assigned exactly once, and the assigned set equal to the table set. The reviewer's independent walk also reproduces the worker's most valuable declaration — that only 67 of the 73 grep lines are real calls, the other six being four docstring lines and two type annotations at exactly the sites the handback names. Re-run by the reviewer: the four state-file readers `157 passed` exit 0, the canary `42 passed` exit 0. Per-commit insertions C0a 264, C0b 185, C1 14, C2 4, C3 309, C4 — the handback commit — 61, none over 500; the change set is exactly the six ordered `.agent/` paths with nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`; history is six single-parent commits with no amend, rebase, reset or force-push. One symbol disagreed between the reviewer's walk and the table — `test_execution_service.py:361`, where the table says `<module>` and an innermost-range walk says `_kill_process_group` — and the table is RIGHT under the scope-of-execution reading it applies consistently to all six non-call rows, since line 361 is the `def` header itself and a def header executes in module scope. The ambiguity is the block's, not the worker's, and is registered below as R-0492. DECISION F085 D1, recorded here per §4 item 7 and reversible by any later relay: the feature file's premise that subprocess execution "already flows through a small number of helpers" is FALSIFIED by measurement — 67 real call sites in 56 distinct enclosing functions, of which the four helpers it names cover 24, while git plumbing alone holds 24 with 12 of them in `worktrees.py`. The chosen option is to amend `docs/roadmap/features/T2_F085.md` in R4 and re-slice T002 against the measured shape rather than the assumed one; the alternatives considered were to proceed on the written slicing, which would under-scope T002 by roughly two thirds, and to widen R2 to do the re-slicing, which would have mixed an inventory round with a planning ruling. R4 also carries that amendment's `tests/docs/` gate. The map in this file's Steps section is amended by that same decision: ruling the stage-1 command classes moves from R3 to R4, because R3 is this session's terminator round.
<<<END RECORD-R2>>>

<<<SLICE R0492>>>
- R-0492 — Low, A BLOCK DEFINED ITS INVENTORY UNITS BY A TEXT GREP WHILE ITS COLUMNS DEMANDED FACTS ABOUT CODE, SO SIX OF THE SEVENTY-THREE ORDERED "CALL SITES" ARE NOT CALLS AND ONE SYMBOL WAS UNDEFINED. Raised by the reviewer at the R2 gate against its own R2 block. That block's step 5 says "ONE ROW PER CALL SITE, no row for anything else", and then defines the set with `git grep -n -E 'subprocess\.(run|Popen|call|check_output|check_call)' -- packages/ apps/` while gate G7 demands the table equal that grep as a SET. A regex over text cannot distinguish a call from prose about a call, and six of the 73 matches are not calls: four are documentation — `command_discovery.py:190` and `:205`, `dod_runners.py:12`, `test_runner.py:24`, three of which are docstrings that promise the very safety properties this feature is about — and two are type annotations, `test_execution_service.py:361` and `dev_server.py:1440`. The two halves of the block are therefore unsatisfiable together, and the worker resolved the conflict the right way: it tabled all 73 to satisfy the set-equality gate, marked the six non-calls `n/a` in the six keyword columns rather than inventing `no`, and declared the tension in its handback instead of silently dropping rows. The reviewer's independent AST walk reproduces exactly those six. The same root cause produced a second defect: `symbol` is specified as "the innermost enclosing `def`/`async def`/`class` name at that line", which is undefined when the matched line IS a `def` header, as `test_execution_service.py:361` is. The table's `<module>` is correct under the scope-of-execution reading it applies consistently to all six non-call rows — a def header executes in module scope — but the block never states which reading governs, so an innermost-range walk disagrees and neither answer can be called wrong. Low, because nothing false was recorded, no gate was weakened, the six rows are honestly marked, and the inventory's value is untouched: the 67 real calls carry fully re-derived facts. Counter-measure, binding on the reviewer from R4 on: when a block orders an inventory of code units, the SET is defined by the semantic predicate the columns describe — here "a `subprocess.*` call node in the AST" — and any text grep is named only as the starting candidate list, with the block stating explicitly what to do with candidates the predicate rejects; and any column whose value depends on a scope reading names the reading. This is the R-0367 and R-0463 family seen from a new side: those bar a reviewer from asserting a number the producing tool cannot yield, while this one bars defining a set with one tool and describing it with another. OPEN.
<<<END R0492>>>
