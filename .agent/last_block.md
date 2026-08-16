── STEP R2 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R1 PASS, register R-0491, and produce the subprocess-seam inventory
the feature file's "inspect current shape before building" demands. No
production code, no test content, no `docs/` file at all this round.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r2.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` whole file := the PLAN slice
  C2  `.agent/live_review.md` += the RECORD-R1 slice, then the R0491 slice
  C3  create `.agent/f085_inventory.md` — the seam inventory
  C4  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `9ba3179eedc20075e13ac0545b816af112bade7e`, the R1
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Why C1 comes before C2 and C3: AGENTS.md's Commit Gate requires
`.agent/plan.md` to match the current work before EVERY commit, and R1 declared
that its first three commits landed while the plan still described the previous
feature. This bundle moves the plan update ahead of the round's substance so
only the two block-save commits precede it. That is the counter-measure
R-0491 states.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R1 and R0491. Every slice's bytes end with a single
trailing newline, and the whole-file slice is the COMPLETE file including it.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r2.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r2.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r2.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

4. C2 — append to `.agent/live_review.md`, in this order, each preceded by
   exactly one blank line, both byte-verbatim, nothing else touched in the file:
   a. the RECORD-R1 slice;
   b. the R0491 slice.
   The pre-C2 file content must remain a byte-exact PREFIX of the post-C2 file.

5. C3 — create `.agent/f085_inventory.md`. Its content is YOUR research, not an
   authored slice, but its SHAPE is fixed by the gates below.

   Section `## Seams` — a markdown table, ONE ROW PER CALL SITE, no row for
   anything else, with exactly these columns in this order:

   | site | symbol | callee | cwd | env | timeout | capture | check | shell |

   - `site` is `path:line`, exactly as `git grep -n` prints it.
   - `symbol` is the innermost enclosing `def`/`async def`/`class` name at that
     line, or `<module>` when the call is at module level. Derive it with an AST
     walk over the file, not by eye.
   - `callee` is the attribute called: `run`, `Popen`, `call`, `check_output` or
     `check_call`.
   - `cwd`, `env`, `timeout`, `check`, `shell` are `yes` when that keyword is
     passed AT THAT CALL and `no` otherwise — read the call's keywords from the
     AST, do not infer from surrounding code.
   - `capture` is `yes` when any of `capture_output`, `stdout` or `stderr` is
     passed at that call, `no` otherwise.
   - `class` does NOT get a column; classification lives in the next section.

   The call-site set is defined by exactly this command, run at C3's HEAD from
   the repository root:
   `git grep -n -E 'subprocess\.(run|Popen|call|check_output|check_call)' -- packages/ apps/`
   The reviewer measured 73 matching lines across 33 files at `a5a70621` and the
   same 73 at the R1 head; report what you measure rather than assuming it.

   Section `## Classes` — assign every `site` to exactly one class from this
   closed vocabulary and list the sites under each heading:
   `builder` (spawns a builder/agent tool), `test` (spawns a test command),
   `dod` (spawns a Definition-of-Done command), `runtime` (spawns or manages the
   runtime harness or a dev/UI server), `git` (internal git plumbing),
   `packaging` (evidence, review-subject or manifest tooling), `other` (name the
   reason in one clause). Every site appears exactly once across all classes.
   State the per-class counts and state that they sum to the total.

   Section `## Guards already in force` — the tests that already constrain these
   files, each with `file:symbol` and one clause on what it forbids. At minimum
   `tests/orchestration/test_test_runner.py::test_no_subprocess_in_discovery_module`
   and `tests/orchestration/test_test_runner.py::test_no_shell_true_in_orchestration`.
   Grep for any others that assert over these paths rather than trusting this
   list to be complete; if you find none beyond these two, say so plainly.

   Section `## R-0202 — the REMEDY_UI_NO_AUTO_BUILD spawn path` — locate every
   place that variable is read or set, with `file:symbol`, and state which spawn
   path can drop or ignore it. If the mechanism is still unexplained after the
   grep, say exactly that and name what you checked. Do NOT guess a cause and do
   NOT fix anything.

   Section `## Premise check` — the feature file says subprocess execution
   "already flows through a small number of helpers". State whether the measured
   inventory supports that, in one short paragraph, with the numbers. This is an
   observation for the reviewer to rule on, not a decision you make.

   Do NOT propose a design, do NOT write `exec_guard.py`, do NOT edit any file
   outside the ordered set.

6. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~5 % (F085 beansprucht · Seam-Inventar erstellt · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table covering
   C0a, C0b, C1, C2, C3 and C4, every gate reading below with its real exit
   code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the six in the ordered bundle. No
   production code, no test file, no `docs/` file. If the work seems to require
   one, stop and hand off.
4. The inventory RECORDS the current shape. It proposes nothing, fixes nothing
   and renames nothing.
5. Destructive or red-proof verification runs only inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout.
6. Never force-push, never rebase, never amend, never reset, never work on
   `main`, never delete a branch. Do not create a PR.
7. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
8. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent.
G2  TRANSPORT: `.remedy-wt/f085-r2.md`, the committed `.agent/authored/f085-r2.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256
    and line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b`
    match, and is under 50 lines.
G4  `.agent/live_review.md`: the pre-C2 content is a byte-exact PREFIX of the
    post-C2 content, and the appended tail contains the RECORD-R1 slice and the
    R0491 slice, each byte-verbatim and each exactly once. Report
    `git show --numstat` for that path at C2 and confirm its deletion column
    is 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, `Landed:`, duplicate ids and
    resolutions naming an unregistered id. REQUIRED: the set of OPEN ids equals
    the set open at `9ba3179e` PLUS exactly `R-0491`; report both counts rather
    than predicting them, plus the max id and the next free id.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  SEAM SET: the set of `path:line` values in the `## Seams` table equals, as a
    SET, the set of `path:line` values the grep in step 5 prints at HEAD.
    Report both counts and the symmetric difference, which must be empty.
G8  SYMBOL RESOLUTION: for every row, re-derive the innermost enclosing
    `def`/`async def`/`class` at that line by an AST walk and compare it to the
    `symbol` column. Report the number of rows checked and the number that
    agree; the two numbers must agree.
G9  KEYWORD FACTS: for every row, re-derive `cwd`, `env`, `timeout`, `check`,
    `shell` and `capture` from that call's AST keywords and compare with the
    table. Report rows checked, rows agreeing, and every disagreement with its
    site. The two numbers must agree.
G10 CLASS PARTITION: every `site` in the table appears exactly once across the
    `## Classes` sections, every class heading is from the closed vocabulary,
    and the per-class counts sum to the table's row count. Report the counts.
G11 The inventory contains the four other mandated sections by heading:
    `## Guards already in force`, `## R-0202 — the REMEDY_UI_NO_AUTO_BUILD spawn path`,
    `## Premise check`, and `## Seams` and `## Classes` themselves.
G12 NO CODE TOUCHED: `git diff --name-only 9ba3179e..HEAD` lists exactly this
    set and nothing else: `.agent/authored/f085-r2.md`, `.agent/f085_inventory.md`,
    `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`. Report the real list and flag any difference rather than
    editing to match. In particular no path under `packages/`, `apps/`,
    `tests/`, `scripts/` or `docs/` may appear.
G13 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
    → exit 0. Run in the PRIMARY checkout, not a worktree: the reviewer measured
    `157 passed`, exit 0, at the R1 head, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`
    because `apps/ui/node_modules` is gitignored and absent there — the known
    R-0480 mechanism, not a base red.
G14 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at the R1 head. `tests/docs/` is NOT
    gated this round because no `docs/` path is in the change set.
G15 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3 only. None may exceed 500. C4's own insertion count
    cannot exist while C4's text is being written, so it is reported in your
    FINAL MESSAGE — the round report — and not in this file. If the inventory
    commit C3 would exceed 500 insertions, STOP before committing it and report:
    do not split the inventory on your own initiative and do not trim rows.
G16 `git log --format=%p 9ba3179e..HEAD` shows one parent per commit (linear).
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
R2, this round: record the R1 PASS, register R-0491, and write
`.agent/f085_inventory.md` — every `subprocess.*` call site in `packages/` and
`apps/` with its enclosing symbol, its command class and the keyword facts of
the call itself. No production code and no test content.

## Next Steps
1. R3 — record R2, rule the stage-1 command classes and their policies as a
   DECISION, and rule on the premise the inventory tests: the feature file
   assumes subprocess execution already flows through a small number of
   helpers, and the measured call-site count is what decides whether T002's
   seam migration is the job the task slicing assumes.

## Risks
- If the inventory shows the seams are many rather than few, T002 as sliced is
  under-scoped. That is a spec finding for R3 to route, not a reason for any
  round to widen itself.
- R-0202 is carried into this feature: a spawned path once ignored
  REMEDY_UI_NO_AUTO_BUILD and the mechanism was never explained. R2 locates the
  path; it does not fix it.
<<<END PLAN>>>

<<<SLICE RECORD-R1>>>
Gate: R1 — PASS. All fifteen ordered gates reproduce at the reviewer's own hand, from the repository root at 9ba3179e, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r1.md`, the committed `.agent/authored/f085-r1.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 7a34422a0df2ca34a94599de5804a87cf9b53e211c17de6a1e99f9d81b006512, 21785 B, 339 lines. THE RESET IS HONEST, which is this round's only irreversible act: the pre-reset blob at a5a70621 holds 117 registered ids, 13 resolved, 0 `Landed:` lines, 0 duplicates and 0 resolutions naming an unregistered id, so 104 were open; at HEAD the record holds 105 registered and 0 resolved, the set of open ids equals the pre-reset open set plus exactly R-0490 with an EMPTY symmetric difference, and each of the 104 carried paragraphs was extracted by id from the pre-reset blob and compared byte-for-byte against its counterpart at HEAD — 104 compared, 104 equal, none missing, none altered, no id registered that was not open at the base. Next free id R-0491. STATUS: the FROM line occurs 0x and the TO line 1x, `^- \[~\]` is 1x, `^- \[x\] F\d{3} — ` is still 50x, `<<` is 0x, and replacing the TO back with the FROM reproduces the base file BYTE-FOR-BYTE, which proves the commit moved that one line and nothing else. README.md is byte-identical to the base, correctly, because the capability counters move only at closure. The three whole-file state slices are byte-equal to their authored originals — context.md 297bd398… 48 lines, plan.md 05d8bf54… 40 lines, candidates.md ffa9a740… 12 lines — every contract assertion their four reader tests make is satisfied at HEAD, and no transport marker reached any target file. Re-run by the reviewer: the four state-file readers `157 passed` exit 0, `tests/docs/` `295 passed` exit 0, the canary `42 passed` exit 0. Per-commit insertions C0a 339, C0b 322, C1 41, C2 66, C3 — the handback commit — 49, none over 500; the change set is exactly the eight ordered paths and no path under `packages/`, `apps/`, `tests/` or `scripts/`; history is five single-parent commits and the reflog shows no amend, rebase, reset or force-push. The handback is 74 lines against a 60-line cap, declared inside the file with that exact count and its cause under the AGENTS.md DECISION D15 stated-cause rule, with no section dropped — permitted, not a finding. Two further declared deviations are accepted and are not findings: `shutil.copyfile` for a denied `cp`, which the block itself sanctioned because the gate names the byte property rather than the tool, and the worker's note that `.remedy-wt/` has accumulated roughly a thousand scratch entries, which is the already-registered R-0403 mechanism and unchanged by this round. The third — that `.agent/plan.md` still described the previous feature during C0a, C0b and C1 — is real, is the reviewer's fault rather than the worker's, and is registered below as R-0491.
<<<END RECORD-R1>>>

<<<SLICE R0491>>>
- R-0491 — Low, THE CANONICAL ROUND BUNDLE PUTS THE BLOCK-SAVE COMMITS AHEAD OF THE PLAN UPDATE, SO EVERY ROUND'S FIRST COMMITS LAND WHILE `.agent/plan.md` STILL DESCRIBES THE PREVIOUS ROUND OR THE PREVIOUS FEATURE. Raised by the reviewer at the R1 gate, from a deviation the R1 worker declared correctly rather than routing around. AGENTS.md's Commit Gate is unconditional — "Before committing: 1. Verify `.agent/plan.md` matches the current work ... If any of these fail: DO NOT COMMIT" — and its Task Completion Protocol repeats it as "Before every commit: 1. Verify that `.agent/plan.md` reflects the current state". The R1 bundle ordered C0a, C0b and C1 before the PLAN slice landed in C2, and at C0a the plan on disk still described `amend0816 CI hosted green`, a closed and merged branch. Three commits therefore landed against a plan that did not match the current work. This is not a worker defect: the worker followed the ordered sequence, which Constraint 2 of that block required byte-verbatim, and declared the conflict in its handback instead of silently reordering — the correct behaviour on both counts. It is a REVIEWER defect, and a structural one rather than a slip, because the same ordering appears in the F083 R1 and F083 R28 bundles and would otherwise recur in every round of this feature by construction, arriving as a re-declared deviation each time instead of as a fixed rule. Low, because nothing false was written and no gate was weakened: the plan was correct from C2 on and the round's own gates proved it byte-equal to its authored slice. Counter-measure, binding on the reviewer from R2 on and demonstrated by the R2 bundle that carries this finding: the `.agent/plan.md` update is ordered as the FIRST commit of a round that has substance to record, ahead of the live-review record and ahead of the round's work, so that only the two block-save commits — which write nothing but the block itself — can precede it. Where a round genuinely cannot do that, the block says so in its own text and names the commit at which the plan becomes current, rather than leaving the worker to discover the conflict. The wider question of whether a pure block-save commit should be exempt from the Commit Gate at all is an AGENTS.md question that F085 does not own; AGENTS.md forbids mixing an unrelated fix into a feature branch, so that half routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.
<<<END R0491>>>
