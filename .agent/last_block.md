── STEP R4/8 — F082 Self-benchmark (record R3, then the frozen order set) ──
Goal:        Record the R3 gate and R-0408, survey the sample project the
             orders must run against, then build the five frozen bench orders
             and the per-order version freeze that makes an unbumped edit fail.
Bundle:      C0a/C0b save this block · C1 the R3 verdict, R-0408, DECISION
             F082 D2 and the plan re-sync, findings persisted FIRST · C2 the
             sample-project survey · C3 the five orders and the freeze · C4
             handback.
Change:      .agent/live_review.md, .agent/decisions.md, .agent/plan.md,
             .agent/f082_inventory.md, packages/orchestration/bench_orders.py
             (NEW), scripts/bench_orders/ (NEW: five order files plus
             manifest.json), tests/orchestration/test_bench_orders.py (NEW),
             .agent/authored/f082-r4.md, .agent/last_block.md,
             .agent/handoff.md. NOTHING else — in particular no gauntlet
             module, no gauntlet order file, and none of the seven gauntlet
             test files.
Constraints: Findings persist FIRST, in their own commit, before any code
             (planner_reviewer_prompt.md §4 item 4). Never write a `Done:` or
             `Landed:` paragraph of your own. Every authored slice is applied
             disk-to-disk out of the COMMITTED block file, never retyped.
             Push after every commit. Never merge, never force-push, never
             work on main. The factoring stays ADDITIVE (R2 Q11): reuse
             gauntlet symbols by importing them, move none of them.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r4-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (findings R-0381, R-0399).
Split it unconditionally, and retype neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r4.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R4 order-set block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r4.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R4 block into last_block`

── C1 — the R3 verdict, R-0408, DECISION D2, plan ────────────────────
ONE commit, the FIRST after C0.
  Subject: `docs(f082): record the R3 verdict and register R-0408`

C1a. `.agent/live_review.md`. APPEND ONLY, in this order, separated by exactly
one blank line, each exactly ONE physical line: FINDING-R408, then GATE-R3.
Nothing above the append may move — prove it against the pre-C1 revision over
the file's existing 103 lines.
C1b. `.agent/decisions.md`. APPEND ONLY the DECISION-D2 slice at the end,
preceded by exactly one blank line. Touch no existing entry.
C1c. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.

--- BEGIN SLICE FINDING-R408 ---
- R-0408 — Low — reviewer blocks order a named TOOL where they mean a PROPERTY, and the tool's availability is not constant across the sessions that execute them. Every block this feature has emitted orders `cmp <a> <b>` for its transport proof and `cp` for its block save; the R3 worker reported both DENIED to it by the permission layer, along with compound shell forms reading `$?`, and satisfied the same obligation with a `python3` byte comparison plus a sha256 of each side — a proof that is strictly stronger, because it reports the digest rather than only an exit code. The R1 and R2 workers reported `cmp` exit 0 for the identical obligation, so availability varies by session class or invocation form rather than being uniformly absent, which is exactly what makes ordering the tool unsafe: a block cannot know which side of that line its worker will land on, and a worker that meets the obligation by another route is forced to spend a declared deviation proving the reviewer's phrasing wrong rather than anything about the repository. This is the same shape as the already-recorded `remedy`-entry-point split, where the CLI name is denied session-wide and `python3 -m apps.cli.main` is the working form. Nothing on disk is wrong and no verdict moves: byte equality was proven in all three rounds. The counter-measure, binding from R4 on: a transport or comparison gate states the PROPERTY and its evidence — "prove the two files are byte-identical and report the shared sha256" — and names a tool only as a suggestion, never as the gate. R4's gate 2 is worded that way. OPEN.
--- END SLICE FINDING-R408 ---

--- BEGIN SLICE GATE-R3 ---
Gate: R3 — PASS, with one new finding. Verification tier: round gate plus the scoped ruff plus the state-file contract readers plus the canary; no full-suite claim is made, and the integration gate is not owed until R7. Every one of the twenty ordered gates was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: the scratchpad, `.agent/authored/f082-r3.md` and `.agent/last_block.md` are byte-identical at shared sha256 `41c13e120fc2e3542a8ddc1cc0aec123b562ba6525f6046ac9537948ba1380e8`, 314 lines, inside the 400-line cap, and that digest equals the one the reviewer measured on its own bytes before emitting. The append is clean: the record's first 95 lines are byte-identical to the pre-C1 revision, the C1 numstat for that path is `8 0` with deletion column 0, and all four appended slices are exactly ONE physical line each. The record's counts re-measured by the reviewer are `^Gate: R2 — PASS` 1, `^- R-0405 — ` 1, `^- R-0406 — ` 1, `^- R-0407 — ` 1, `^## Steps` 1 and `^Landed: ` 0; the open set recomputed mechanically is exactly THIRTY-SEVEN with no duplicate and max id R-0407; `^## DECISION F082 D1` is 1 with deletion column 0 on that path. The change set is ten paths, every one inside the block's Change list and none outside it, which is the ceiling wording R-0405's counter-measure introduced this round. The production change was READ, not merely gated: `git diff` over `gauntlet_runner.py` is three added lines and two removed, confined to `measure_tokens`, with no other function in the file touched. The repair is correct — `usage.get("input_tokens") or usage.get("prompt_tokens") or 0` — and the reviewer re-derived the red-proof independently rather than trusting the reported colour: evaluating the OLD expression against the new test's own fixture `{"input_tokens": 111, "output_tokens": 222}` yields exactly `{"in": 0, "out": 0}`, which is precisely the assertion the worker reported failing in its disposable worktree, and the worker proved the mutated copy was the imported one by printing `__file__` under `.remedy-wt/` first (R-0337). The new module was read line by line and its claims about other code were checked at their source rather than accepted: `capability_bench._postmortem_classes_of` documents "the same rule as `gauntlet_matrix.postmortem_classes`", and that function does dedupe first-seen and does substitute the literal `"(absent)"`, so both attributions hold — the class of false attribution R-0338 registers was actively looked for and is not present. The module is pure as ordered, with zero hits for `open(`, `Path(`, `requests`, `time.` or `datetime`, and its `None`-not-zero handling is the R-0178 invariant this round had to repair rather than a restatement of it. Suites re-run by the reviewer at the branch head, in one invocation: the new `test_capability_bench.py`, the seven gauntlet files and `test_orchestrator_loop.py` together `479 passed`, which is exactly 7 + 276 + 196 against the 276 and 196 baselines the reviewer measured at `13953c5f` BEFORE authoring; the canary and the three state-file contract readers reproduce their 42 and 142; scoped `ruff check` over the three files R3 owns exits 0; `integrity check --json` returns `passed: true`, `fail_count: 0` over 5 checks. The gauntlet's own seven test files are byte-unmodified — `git diff --name-only` over `tests/orchestration/` returns exactly one path, the new bench test file — so the ADDITIVE constraint R2 Q11 derived held under its first real load. `git status --porcelain` is empty and `git worktree list` is one line, so the red-proof worktree was genuinely removed and pruned. Four deviations, all declared and all accepted: `cmp`, `cp` and `$?` forms were denied to the worker and replaced by digest-based proofs, which is registered above as R-0408 against the REVIEWER's phrasing rather than the worker's conduct; the docstring addition is one 116-character line inside ruff's 120 limit; the handback is 150 lines carrying its DECISION D15 stated cause with no section dropped; and the commit messages carry no trailer, matching this repository's history. One observation costs no id: `usage.get("input_tokens") or usage.get("prompt_tokens")` treats a present-but-ZERO first spelling as absent, so a body carrying both spellings with a zero input and a non-zero prompt would report the second — unreachable, because the reviewer confirmed writer-side that no producer emits both spellings and every real body carries exactly one, and the returned value is identical under either reading whenever one spelling is present. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R3 ---

--- BEGIN SLICE DECISION-D2 ---
## DECISION F082 D2 (2026-08-14) — the bench freeze binds each order's VERSION to its digest

CONTEXT. F082's acceptance says "Changing an order file without bumping its
version fails validation." The gauntlet's freeze does not give that for free.
`gauntlet_orders.load_order_set` compares each order file's sha256 against the
digest recorded for it in `manifest.json`, so an edit alone DOES fail — but the
obvious repair is to recompute the manifest digest, and that passes with no
version bump anywhere. R2 Q3 confirmed there is no per-order version field at
all: `GauntletOrder` carries `id`, `file_name` and `sha256`, and the only
version constants are module-level and set-wide.

DECISION. Each bench order file carries its own `bench_order_version` integer,
and the manifest records, per order, a `digests` map from version string to the
sha256 of the bytes published under that version. Validation requires that the
order file's CURRENT digest equals `digests[str(version)]`. Editing the bytes
without bumping the version therefore fails, because the new bytes do not match
the digest recorded for the version the file still claims; bumping the version
requires adding a new entry to the map, which is a deliberate act and leaves the
previous pair in place as the series' own history. Changing an order starts a
new series, which is the comparability honesty the feature file asks for.

ALTERNATIVES CONSIDERED. (a) Reuse the gauntlet's single-digest manifest
unchanged: rejected, it is exactly the mechanism that permits a silent
recompute. (b) Derive the version from git history of the order file: rejected,
validation must hold in an exported evidence bundle where no git history is
present. (c) Store only the newest (version, digest) pair rather than a map:
rejected, it loses the series history that makes an old bench row's basis
readable, at no saving worth having.

HOW TO REVERSE. Drop the `digests` map from the manifest and compare against a
single `sha256` per order, matching the gauntlet's shape, and delete the
version-binding tests in `tests/orchestration/test_bench_orders.py`.
--- END SLICE DECISION-D2 ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0409. Open findings: thirty-eight — the thirty-two carried from F077,
R-0403 at the claim, R-0404 at the R1 gate, R-0405 to R-0407 at the R2 gate,
and R-0408 at the R3 gate. `.agent/live_review.md` is the source of truth.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R4: the R3 gate recorded, R-0408 and DECISION F082 D2 registered, the sample
project surveyed, and the five frozen orders built behind a freeze that binds
each order's version to its digest.

## Next Steps
1. R5 — T001 closed: the dry run of `build_bench_record` against RECORDED
   fixture evidence, end to end from an order file to a row.
2. R6 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R7 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R8 the integration gate, R9 closure.

## Risks
- The five capabilities the feature file names may not all be expressible
  against the existing sample project. C2 surveys it FIRST and stops rather
  than inventing an order that cannot run — an unrunnable frozen order is
  worse than a missing one, because the freeze makes it permanent.
- Thirty-eight open findings is the largest carry any feature has started with.
--- END SLICE PLAN ---

── C2 — survey the sample project FIRST ──────────────────────────────
Append a section `## S1..S4 — the sample project (R4)` to
`.agent/f082_inventory.md`. Read-only; commit alone.
  Subject: `docs(f082): survey the sample project the bench orders must run in`

The five orders F082 names probe a small CLI tool, an API endpoint with tests,
a frontend widget judged by build plus an HTTP-level smoke, a bugfix on a
fixture repo, and a behaviour-preserving refactor. Whether the project the
harness materialises can host those is unknown and must not be assumed.

S1. `scripts/gauntlet_sample_project` — what is actually in it? Languages,
    entry points, test runner, and how a mission is expected to change it.
    Cite `path::symbol` or a real file path for each claim.
S2. `gauntlet_runner.py::materialise_sample_project` and `_default_make_project`
    — how the project reaches a run's workspace, and whether an order can
    select a DIFFERENT template than the frozen one. R2's Q3 answer noted the
    template digest is folded into the set freeze; say what that implies for a
    bench order that would need its own fixture.
S3. For EACH of the five capabilities above, answer expressible: yes or no,
    against what is actually in the project, with the file that settles it.
    Count the five as you answer them and state the count.
S4. If any answer in S3 is no: name the smallest fixture addition that would
    make it yes, and say plainly that F082 has not built it.

STOP CLAUSE. If fewer than THREE of the five are expressible, do not write any
order file: finish this commit, write the handoff naming which are not
expressible and why, and hand back. A frozen order that cannot run is worse
than a missing one, because the freeze makes it permanent. If three or four are
expressible, write orders for those and record the remainder in S4 as owed —
do not invent them, and say so in the handback rather than quietly shipping
fewer than five.

── C3 — the five frozen orders and the freeze ────────────────────────
Only if C2's stop clause did not fire. Commit together.
  Subject: `feat(f082): add the frozen bench order set and its version freeze`

`scripts/bench_orders/<id>.json`, one per expressible capability, keys sorted,
each carrying: `id`, `kind`, `title`, `goal`, `rationale`, `risk_probed`,
`milestones` with a `dod` list, `budget`, `injections`, and
`bench_order_version` starting at 1. Follow the field shape of
`scripts/gauntlet_orders/g01-pure-code-change.json`, which is the format the
harness already reads; the goals must be achievable in the project C2 surveyed,
not aspirational.

`scripts/bench_orders/manifest.json` carrying `bench_order_set_version`, and
per order `{id, file, version, digests: {"<version>": "<sha256>"}}` per
DECISION F082 D2.

`packages/orchestration/bench_orders.py` (NEW) with the loader and the freeze.
Import what it needs from `gauntlet_orders` rather than moving anything out of
it (R2 Q11): reuse `GauntletOrder` and the digest helper if they fit, and if
they do not, say why in a comment rather than silently duplicating. Raise a
named error on the first thing that does not hold — a digest that does not
match the digest recorded for the order's own claimed version, a version absent
from its `digests` map, an id that repeats, a file the manifest does not list,
or a file on disk the manifest omits.

`tests/orchestration/test_bench_orders.py` (NEW), each test pinning one
behaviour: the set loads and every order validates; an order file edited in a
tmp copy WITHOUT bumping its version FAILS with the named error — this is the
feature's acceptance criterion and is the most important test in the round;
bumping the version AND recording the new digest passes; a duplicate id fails;
a manifest entry whose file is missing fails; an on-disk file the manifest does
not list fails. Build every negative case in a tmp copy of the directory —
never mutate `scripts/bench_orders/` in a test.

── C4 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Under 60
lines, or carry a DECISION D15 stated-cause line naming the real count and the
mandated content. Commit and push.
  Subject: `chore(f082): handback R4`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  Transport, stated as a PROPERTY rather than a tool (R-0408): prove that the
    scratchpad, `.agent/authored/f082-r4.md` and `.agent/last_block.md` are
    byte-identical, and report the shared sha256 and the line count, which must
    be at or under 400. Any means is acceptable — `cmp`, a `python3` byte
    compare, or a digest of each — provided you report the digest.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: the first 103 lines of the new `.agent/live_review.md` equal
    the pre-C1 file. Report the C1 numstat for that path; DELETION column 0.
    Report the physical line count of FINDING-R408 and GATE-R3; each exactly 1.
5.  `grep -c "^Gate: R3 — PASS" .agent/live_review.md` → 1;
    `grep -c "^- R-0408 — " .agent/live_review.md` → 1;
    `grep -c "^## Steps" .agent/live_review.md` → 1;
    `grep -c "^Landed: " .agent/live_review.md` → 0.
6.  Open set recomputed mechanically — `^- R-[0-9]\+ — ` paragraphs minus
    `^Done: R-[0-9]\+ — ` lines. Expect THIRTY-EIGHT; name every id; report
    duplicates as none or name them; report max and next free.
7.  `grep -c "^## DECISION F082 D2" .agent/decisions.md` → 1; DELETION column 0
    for that path in C1.
8.  `wc -l .agent/plan.md` → under 50. Report it.
9.  C2's stop clause: state plainly whether it fired, how many of the five
    capabilities are expressible, and the count you counted. If it fired, gates
    10 to 14 report "not reached" and that is a PASSING round.
10. `git diff --name-only cb79d388..HEAD` → report every path and
    COUNT them mechanically, stating the count. The Change list is a CEILING:
    every path reported appears in it; a path the block exempts may be absent.
    Name any path present that the list does not contain — there must be none.
11. The freeze's acceptance test, run and reported by name: the test that edits
    an order without bumping its version must FAIL validation. Report the test
    name, that it passes, and the error type it asserts. Then prove it is not
    vacuous: in a DISPOSABLE worktree under `.remedy-wt/` only, weaken the
    version check to compare against any digest in the map, re-run that test,
    and report that it goes RED. Print the module's `__file__` from inside that
    worktree first and report the path — it must be under `.remedy-wt/`
    (R-0337). Remove and prune the worktree.
12. `python3 -m pytest tests/orchestration/test_bench_orders.py -q` → exit 0;
    report the count. No baseline, the file is new.
13. The gauntlet stays untouched and green: `git diff --name-only
    cb79d388..HEAD -- tests/orchestration/ packages/orchestration/` must
    contain no `gauntlet_*` path — report the real list. Then run the seven
    gauntlet files plus `test_capability_bench.py`; the planner measured that
    set directly at cb79d388 today at 283 passed. Report the real number.
14. `python3 -m ruff check packages/orchestration/bench_orders.py
    tests/orchestration/test_bench_orders.py` → exit 0. Repository-wide ruff is
    RED on main and is NOT a gate (R-0364).
15. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0.
    Planner baseline at cb79d388 today: 42 passed.
16. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Planner baseline at
    that commit today: 142 passed.
17. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
18. Every order file's `bench_order_version` and the digest recorded for it:
    report the id, the version, the recorded digest and the file's real sha256
    for each, and state that they match. Count the orders and state the count.
19. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.

Transport proof: state, for each of FINDING-R408, GATE-R3, DECISION-D2 and
PLAN, that it was extracted from the COMMITTED `.agent/authored/f082-r4.md` and
applied disk-to-disk, with its sha256 and byte length, and the proof that the
applied region equals it. Confirm no BEGIN/END marker line reached any target
file. Scan every file you touched for trailing whitespace and report the result.
