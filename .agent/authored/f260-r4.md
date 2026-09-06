── STEP T001 (part 3) — F260 ─────────────────────────────────
Goal:        Ship the id-minting functions DECISION F260 D2 rules — one per KIND
             of id, all in `data_paths` — with their tests and a real mutation
             red-proof. First production-code round of this feature.
Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the record
             (the R3 gate entry) · C3 the reviewer's slip · C4 the minting
             functions and their tests · C5 the handback
(the rule line below is 62 copies of U+2500, per §3 item 37)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `599b3df0`, already pushed. Do NOT
create a branch, merge, or open a pull request. Round 3 PASSED — the reviewer
re-ran every gate and reproduced every number, including 865153 → 873291 with
N = 2 and both rulings landing once each.

This is a SPLIT round over production code (planner_reviewer_prompt.md §3,
Round types): the code below is DESCRIBED, not supplied as a byte slice. You
write it, in the repository's own idiom, and the gates prove it.

## Change set — nothing outside this list

    .agent/authored/f260-r4.md              (new, C0a)
    .agent/last_block.md                    (C0b)
    .agent/plan.md                          (C1)
    .agent/live_review.md                   (C2)
    .agent/prose_slips.md                   (C3)
    packages/orchestration/data_paths.py    (C4)
    tests/test_data_paths.py                (C4)
    .agent/handoff.md                       (C5)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r4-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r4.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone.

## C1 — the plan

`.agent/plan.md` from the PLANF260R4 slice, byte-for-byte plus exactly one
trailing newline. FIRST substantive commit (§3 item 23).

## C2 — the record

Append to `.agent/live_review.md` exactly `"\n" + GATE_R3 + "\n"`. Measured at
`599b3df0`: the file is 873291 bytes, ends with exactly one newline, and holds
299 `^- R-\d{4} — ` registrations against 4 `^Done: R-\d{4} — ` lines. This round
registers no finding and resolves none, so both counts are unchanged by it.

## C3 — the reviewer's slip

Append to `.agent/prose_slips.md` exactly `"\n\n" + SLIP3`. Measured at
`599b3df0`: the file ends WITHOUT a trailing newline and must still end without
one. Append-only: nothing already in it is rewritten.

## C4 — the minting functions and their tests

ONE commit carrying both the code and the tests that pin it, because a commit
that ships a function with no test is a state this round has no reason to create.

### The code — `packages/orchestration/data_paths.py`

DECISION F260 D2, as ruled in `docs/roadmap/features/T2_F260.md` at `599b3df0`,
requires the 16-hex shape `uuid4().hex[:16]` AND a separate minting function per
KIND of id, so that a swapped argument is greppable even though it is not a type
error. Add THREE module-level functions to that file. Their names are fixed by
D2 and are not yours to choose:

    mint_job_id()      -> str
    mint_run_id()      -> str
    mint_episode_id()  -> str

Each returns a fresh `uuid4().hex[:16]`. Requirements:

- Each carries a one-line WHY comment or docstring line directly above or as its
  first line, naming WHAT KIND of thing the id names — AGENTS.md's "the one-line
  WHY comment sits directly above the definition". Say what it names, not what
  it does; "mint the id of one job" is the shape, "return 16 hex chars" is not.
- Each is a SEPARATE function with its own `def`. Do NOT write one helper and
  three one-line aliases, and do NOT set `mint_run_id = mint_job_id`: the point
  of D2 is that the four kinds are distinguishable at every call site, and an
  alias is invisible at the call site. A shared private helper called by three
  distinct `def`s is acceptable; three names bound to one function object is not.
- `uuid4` is NOT imported in this module. Measured by the reviewer at
  `599b3df0`: line 34 reads `from uuid import UUID` and is the file's only
  `uuid` import, so you must extend it to `from uuid import UUID, uuid4` (or add
  the import in the module's existing style). Do not leave `UUID` unimported —
  `resolve_job_id` and `resolve_any_job_id` both still use it.
- Add the three names to the module docstring's `Public API::` block, in the
  same style as the entries already there.
- Change NOTHING else in the file. `resolve_job_id`, `resolve_any_job_id`,
  `_SHORT_HEX_RE` and every directory helper stay exactly as they are; D2 rules
  that the two resolvers are deleted, but that happens in T004 after T002 builds
  the store they would resolve against, and deleting them here would break every
  caller with nothing to replace them.

### The tests — `tests/test_data_paths.py`

Add ONE new test class at the end of the file, in the file's existing idiom
(plain `class Test...` with `def test_...` methods, no fixtures it does not
already use). Measured at `599b3df0`: that file is 217 lines and `python3 -m
pytest tests/test_data_paths.py -q` reports 23 passed. The class pins, one test
per property, and every one of these must be a real assertion about the SHIPPED
functions — import them and CALL them, never re-implement the shape in the test:

1. Each of the three returns a 16-character string, and every character is a
   lowercase hex digit.
2. Two successive calls to the same function differ — the id is minted, not
   constant.
3. The three names are three DIFFERENT function objects. Assert on the objects
   themselves (`mint_job_id is not mint_run_id` and the other two pairings), so
   an alias fails this test. This is the test that makes D2's "not one function"
   clause real.
4. Every minted id satisfies `data_paths._SHORT_HEX_RE.fullmatch(...)`, which is
   what lets the existing prefix resolvers accept it.
5. `uuid.UUID(mint_job_id())` raises `ValueError`. This is the probe round 2's
   inventory recorded as the reason `resolve_job_id` can never resolve a
   ping-pong job id, and pinning it here stops a later round "fixing" the shape
   back to a UUID without noticing what it breaks.

Do not modify or delete any existing test in that file.

## C5 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. No length cap.
Mandated sections, the changed-files table with `+/-` from `git diff --numstat`
(NOT before/after line counts — §3 item 28), one line per gate with real exit
code and real output, the item-status table, every deviation, and:

    SESSION 1 of feature F260 · round 4 · rounds so far 4

plus one sentence of context self-assessment (self_drive_protocol.md G7). The
state block repeats this line verbatim:

    ~25 % (T001 ✅ · Minting-Funktionen ✅ · Resolver + T002–T005 offen) — Schätzung

C5 is the LAST commit. Then `git push origin feature/f260-one-world`. No pull
request, no merge.

## Constraints

1. Apply every authored PROSE slice byte for byte. The CODE is a spec, not a
   slice: write it yourself to the requirements above, in the module's idiom.
2. Nothing outside the change set is created, edited or deleted.
3. Only the two named production/test files change. No other file under
   `packages/`, `apps/` or `tests/` is touched.
4. Commit order C0a, C0b, C1, C2, C3, C4, C5 — no extra, none dropped, none
   reordered.
5. Every commit single-parent, every insertion count under 500 (the `+` column
   only — DECISION F104 D1).
6. Destructive verification runs ONLY inside a disposable `git worktree`; the
   primary checkout is `git status --porcelain` empty at the end.
7. `.agent/plan.md` stays under 50 lines.
8. Commit subjects carry no leading-slash token, no absolute path, no
   secret-like string.

## Done when — the gates

Every one runs for real; report its true exit code and true output.

- **G1 TRANSPORT.** `sha256sum .remedy-wt/f260-r4-block.md
  .agent/authored/f260-r4.md .agent/last_block.md` prints ONE digest three
  times, equal to the BLOCK_SHA the delegating prompt states. A COPY chain over
  scratch, saved copy and mirror; per §3 item 37 it is not a claim about bytes
  emitted into a prompt.
- **G2 THE RECORD AND THE SLIP.** For `.agent/live_review.md`: the pre-image is
  a byte-exact PREFIX of the post-image and the remainder equals
  `"\n" + GATE_R3 + "\n"`; the registration count stays 299 and the `Done:`
  count stays 4; `grep -c '^Gate: R3 — the F260'` goes 0 → 1; no two `^Gate: R`
  headers are byte-identical. For `.agent/prose_slips.md`: the post-image equals
  the pre-image plus exactly `"\n\n" + SLIP3`, and it still ends WITHOUT a
  trailing newline.
- **G3 THE SHIPPED FUNCTIONS ARE RUN, NOT READ.** `python3 -m py_compile
  packages/orchestration/data_paths.py` exits 0. Then, in a script under
  `.remedy-wt/`, IMPORT the three functions from
  `packages.orchestration.data_paths` and CALL each of them 1000 times, and
  report: the set of returned lengths (must be exactly `{16}`), the number of
  distinct values per function out of 1000, whether every character across all
  3000 values is in `0123456789abcdef`, whether all three `is not` each other
  pairwise, and the exception type and message from `uuid.UUID(mint_job_id())`.
  Report the three functions' `__name__` and `__qualname__` too, so an alias is
  visible in the output rather than only in an assertion. Also attempt
  `ruff check packages/orchestration/data_paths.py` and report either its real
  output or the exact refusal text.
- **G4 THE MUTATION RED-PROOF, in a disposable worktree at the round's own
  commit, never in the primary checkout.** Purge `__pycache__` and run pytest
  with `python3 -B` and the worktree as the working directory.
  (i) THE UNMUTATED CONTROL FIRST, in that same worktree:
  `python3 -B -m pytest tests/test_data_paths.py -q` — report its exit code and
  passed count. A colour with no baseline is not evidence (§3 item 33).
  (ii) THEN the mutation: in the worktree's copy of
  `packages/orchestration/data_paths.py`, inside the body of `mint_job_id` ONLY,
  change the slice `[:16]` to `[:32]`. The three function bodies are identical,
  so identify the one to change by its enclosing `def mint_job_id`, and print
  the changed line with its line number to prove which one you edited.
  (iii) Re-run the same command. Report the exit code, the failed count, and the
  NODE IDS of the failing tests. The round's claim is that this mutation is
  CAUGHT; if it is not caught, that is a red gate and a real finding about the
  tests, so report it as such rather than adjusting anything.
  (iv) DISCARD the worktree with `git worktree remove --force` and prune. The
  worktree is thrown away, never reverted, so no revert target is named and no
  edit ever reaches a tracked file.
  Report `git worktree list` afterwards and `git status --porcelain` on the
  primary checkout, both as proof of (iv).
- **G5 THE STATE CONTRACTS.** `.agent/plan.md` holds `## Goal`, `## Next Steps`
  and a `\bF\d{3}\b` match, and is under 50 lines. `.agent/context.md` holds
  `Steps`, `## Active Branch`, `feature/`, a `\bF\d{3}\b` match, and `resource`
  or `pytest` case-insensitively, and none of `steps-74_1-79`, `Steps 91-100`,
  `allow repo_test_run`, `synthetic_count: 4`, `job=None source_apply bypass`.
  `.agent/live_review.md` holds `Steps`.
- **G6 THE SUITES, RUN SERIALLY, one at a time, in the primary checkout.**
  Report exit code and passed count for each:

      python3 -m pytest tests/test_data_paths.py -q
      python3 -m pytest tests/storage/ -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q

  Measured by the reviewer at `599b3df0`, before this block was emitted:
  `tests/test_data_paths.py` 23 passed, and the last seven read 303, 30, 515,
  52, 21, 16 and 42, every one exit 0. `tests/test_data_paths.py` MUST rise by
  exactly the number of tests your new class adds — state both the new total and
  the number of tests you wrote, and say whether they agree. `tests/storage/`
  has no reviewer-measured expectation; report the number you get. Any other
  suite differing is not automatically a failure: report the number and name the
  node ids that account for it.
- **G7 STRUCTURE AND PUSH.** Every commit single-parent
  (`git log --format='%h %p' 599b3df0..HEAD`) and every insertion count under
  500, reported per commit for C0a through C4. C5's own numbers cannot exist
  while C5 is being written and self-drive has no round report to route them to,
  so do NOT state them anywhere: the reviewer measures them at the next gate
  (§3 item 31). `git status --porcelain` empty. `git ls-files .remedy-wt` empty.
  `git diff --name-only 599b3df0..HEAD` lists exactly the change set above and
  nothing more. The push result reported. `python3 -m apps.cli.grouped integrity
  check --json` prints `"passed": true`, `"fail_count": 0`.

## Handback

Completion report plus the `.agent/handoff.md` rewrite described at C5. Declare
every deviation. If a gate goes red, STOP there, do not route around it, and
report the exact output — as you correctly did in rounds 1, 2 and 3.

────────────────────────── authored slices ──────────────────────────

<<<BEGIN PLANF260R4>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 3 are reviewed; rounds 2 and 3 PASSED. T001
is closed: the inventory is on disk and DECISION F260 D1 and D2 are ruled.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 4 is the first production-code round. It ships the three id-minting
functions DECISION F260 D2 rules — `mint_job_id`, `mint_run_id` and
`mint_episode_id`, each a separate `def` returning `uuid4().hex[:16]` — into
`packages/orchestration/data_paths.py`, with a test class that pins the shape,
the freshness, the three-distinct-objects property an alias would break, and the
`UUID()` rejection that is the whole reason the id shapes must converge. A
mutation red-proof in a disposable worktree proves the tests catch a widened
slice.

## Next Steps

- The ONE resolver D2 rules, replacing `resolve_job_id` and `resolve_any_job_id`,
  written while both stores still exist and deleted from its predecessors only in
  T004.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/` with its evidence beside it, and `runs/<run_id>/` keyed by run
  id. Finding R-0814 is fixed here, because that layout removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R4>>>

<<<BEGIN GATE_R3>>>
Gate: R3 — the F260 R3 entry. R3 CLOSED T001 BY RULING DECISION F260 D1 AND D2 FROM ROUND 2'S MEASURED INVENTORY, AND REGISTERED R-0814. VERDICT PASS. Range bd42e0bc..599b3df0, six commits, all single-parent, pushed, no pull request; largest commit 345 insertions, so no commit approached the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF and reproduced every number. THE RECORD: 873291 bytes from 865153, growth 8138 equal to the appended length exactly; the pre-image is a byte-exact PREFIX; `region_post == region_pre + appended` is true with `region_pre` hashing `e91d392a9188…`, which is precisely what the round-2 entry recorded as its POST-image region digest, so the chain across rounds 2 and 3 is continuous rather than merely consistent. Blank-line units ran 419 to 421, so N counts 2, and the last two units are the R-0814 registration FIRST and the R2 gate entry second — the order §4 item 4 requires, findings before verdicts. Registrations went 298 to 299 and the `Done:` count stayed 4; twelve `Gate:` headers, all distinct. THE TWO RULINGS: `docs/roadmap/features/T2_F260.md` went 17231 to 22955 bytes; both pairs measured FROM 1x before and 0x after against TO 0x before and 1x after, both with the containment test printing `TO contains FROM: false` so both are REWRITES and the FROM-zero reading is attainable; the whole file reconstructs byte-exactly from its pre-edit bytes with only those two replacements applied; it still ends with exactly one newline; and `^### DECISION F260 D` matches four times with D0, D1, D2 and D3 each appearing exactly once. Both retired headings are gone and both new ones occur once. NOTHING UNDER `packages/`, `apps/` OR `tests/` MOVED — `git diff --name-only` over the range lists six paths, five under `.agent/` and one under `docs/roadmap/`, which is what a design round should look like. The suites were re-run serially at 303, 30, 515, 52, 21, 16 and 42, every one exit 0, and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342. THE WORKER CORRECTED THE REVIEWER TWICE MORE, and both corrections are upheld. Its deviation 2 catches a STALE NUMERAL in the reviewer's own GATE_R2 slice: that slice says a plain `## Findings` substring search "matches 7 times", which is the reading at round 2's pre-image `4b704705` and not at `bd42e0bc`, where the reviewer independently measures 9 — each appended gate record that quotes the token raises the count, so the figure was true of the image it described and stale for any later one, and the sentence never named which image it meant. The load-bearing clause survives at every image, because what the gate turns on is that the ANCHORED match is exactly 1 while the substring match is not 1, and that holds throughout; the numeral was decoration and the decoration went stale. That is §3 item 20 asking a slice to name the commit its reading was taken at, applied to a count rather than to a claim about code, and the reviewer records it as a dated line in `.agent/prose_slips.md` in the round after this one rather than spending an id, because nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result. Its deviation 3 flags the same class from the other side and pre-empts a misreading: the digest `0d32b1f4…` named in the GATE_R2 slice is round 2's own `region_pre`, while round 3 measures `e91d392a9188…`, and the two are the two ends of one continuous chain rather than a contradiction — flagging it so a later reader finding two digests in one ledger does not open a repair round over a chain that is intact. Its deviation 4(b) is the better catch of the round on its own work: its first attempt at the suite gate piped pytest into `tail`, which reports `tail`'s exit code and not pytest's, and it DISCARDED that reading rather than reporting it, re-running all seven suites through a runner that records each true `returncode`. A worker that throws away its own green reading because the pipe made it meaningless is doing exactly what G4 of docs/agents/self_drive_protocol.md means by gates that run rather than are assumed.
<<<END GATE_R3>>>

<<<BEGIN SLIP3>>>
2026-09-06 · F260 R3 (reviewer) · The GATE_R2 slice the round-3 block carried into the append-only review record states that a plain `## Findings` substring search "matches 7 times" while the anchored pattern matches once, and it names no image for that reading. Seven is the count at `4b704705`, round 2's pre-image; at `bd42e0bc`, the image the round-3 worker actually applied the slice to, the reviewer independently measures 9, because every appended gate record that QUOTES the token in backticks raises the count. The worker measured the discrepancy, applied the slice byte-for-byte as constraint 1 required, and declared it. Nothing follows from it: the clause is load-bearing only in the contrast — the anchored match is exactly 1 where the substring match is not 1 — and that holds at every image the file has ever had, so the numeral was decoration. THE LESSON: §3 item 20 requires a slice stating a fact about a file's content to name the commit the reading was taken at, and this is that rule reaching a COUNT rather than a claim about code — the shape a reviewer does not think of as a "fact about a file" and therefore does not date. A count over a file that this workflow appends to every round is stale by construction the moment the next round runs; either name the image beside it, or state the PROPERTY without the numeral, which here would have been strictly better. Reviewer-authored stale numeral in an `.agent/` record; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP3>>>
