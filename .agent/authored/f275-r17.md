STEP T001 — F275 round 17 — the repair round: sweep the advertisements rounds 15 and 16 left behind

Goal: book session 9's round 16 FAIL verdict and its prose slips, register R-0861, and sweep
the surviving operator-facing advertisements of commands rounds 15 and 16 deleted, which is
what turned round 16's gate G4 red.

WHY THIS ROUND EXISTS. Round 16's own G4 gate went RED at exit 1, correctly, and the worker
declared it rather than widening its change set — which is the sanctioned move and the right
one. The defect is the reviewer's: the round 16 block's exhaustive change set never named
`docs/guides/simple-operator-quickstart-v0.md`, so three operator-facing sections advertising
`remedy worker doctor`, `remedy worker add` and `remedy worker disable` survived the commit
that deleted those commands. The reviewer's own re-run of G4 confirms the worker's reading
exactly — RAW 16, STRIPPED 6, three stripped lines outside `docs/roadmap/features/`, all in
that one file — and the RAW list additionally shows four more advertisements that the
backtick-stripping filter hides from the binding count but which are just as stale. This round
sweeps all of them.

Base: `12dd60ad`. Branch: `feature/f275-one-world-completion-part-three`. Session 9, round 17.

EVERY NUMERAL BELOW WAS MEASURED BY AN APPLIED DRY RUN, NOT DERIVED. The reviewer applied this
exact change set in a disposable worktree at `12dd60ad`, ran the documentation and catalog
guards green, re-ran the completeness sweep to zero outside `docs/roadmap/features/`, and read
the numstat off the resulting commit.


BUNDLE — the commits below, in this order

  C0a  save the authored block:  `shutil.copyfile` `.remedy-wt/f275-r17.md` to
       `.agent/authored/f275-r17.md`. Never retype it.
  C0b  mirror the same bytes:    `shutil.copyfile` the same source to `.agent/last_block.md`.
  C1   advance `.agent/plan.md`  — replaced WHOLE by the PLAN17 slice.
  C2   the record: append LEDGER17 to `.agent/live_review.md` and SLIPS17 to
       `.agent/prose_slips.md`.
  C3   sweep the advertisements — three paths.
  C4   the handback: rewrite `.agent/handoff.md` whole.

C1 is the FIRST substantive commit and advances the plan before the ledger commit, per §3
item 23. C2 books the verdict and registers R-0861 BEFORE C3 repairs what it describes, which
is the ordering §4 item 4 requires of a repair round: findings persist first, in their own
commit, and only then is the defect fixed.


THE CHANGE SET OF C3 — three paths, 8 insertions against 51 deletions

  docs/guides/simple-operator-quickstart-v0.md                     0 / 32
      Delete three whole `###` sections and three table rows. The sections are
      `### Check worker readiness`, `### Add a worker` (with its `Known workers:` line) and
      `### Disable a worker`, each with its fenced `bash` block and its explanatory prose.
      `### Check core health` sits between the second and third and SURVIVES UNTOUCHED —
      `remedy doctor core` is not deleted. In the "Normal command / Advanced equivalent(s)"
      table, delete the three rows whose first cell is `` `worker add claude` ``,
      `` `worker doctor claude` `` and `` `worker disable claude` ``; the `job status`,
      `job report`, `job run-loop` and `doctor core` rows all SURVIVE, and the table's header
      and separator rows are untouched.
  docs/system/core-product-spine-v0.md                             8 / 8
      Two edits. FIRST, the body of the `## What a worker is` section is REPLACED — the
      heading itself stays — by the deliberate-absence note AGENTS.md's Code Discoverability
      Conventions require, because text search cannot find a command that does not exist and
      this section is exactly where a reader will look for one. The replacement text is the
      SPINE17 slice below, applied byte for byte between the heading line and the blank line
      preceding `## What a report is`. SECOND, in the command-taxonomy table delete the two
      rows `| `worker doctor <name>` | Check worker readiness | No | No |` and
      `| `worker add <name>` | Enable adapter + template | Metadata | No |`.
  docs/system/mission-run-loop-morning-report-v0.md                0 / 11
      Delete the whole `## How Claude Code fits` section — its heading, its one-line
      introduction and its five numbered steps — up to but not including `## How Self-Repair
      Proposals fit`. Every one of those five steps names a rail this feature has deleted:
      step 1 is `remedy worker add`, steps 2 and 3 are the managed execution round 15 removed,
      and step 4 is the sandbox intake round 13 removed. The section describes a path that no
      longer exists end to end, so it goes whole rather than losing a step at a time.

DELIBERATELY NOT TOUCHED, unchanged from rounds 15 and 16: the roadmap files under
`docs/roadmap/features/`. After this round's sweep the completeness measurement reads RAW 11
and STRIPPED 3, and all three stripped lines are in `T2_F262.md`, `T2_F267.md` and
`T8_F151.md` — two closed features' records and one whose repair is already registered as
R-0858.


CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it as written and
    declare it in the handback. Never edit a slice.
 2. The change set above is EXHAUSTIVE. Touch no other path. If a gate demands a change to a
    path not listed, stop and declare it rather than widening — that is exactly what round 16's
    worker did, correctly, and it is why this round exists.
 3. Each append is `post = pre + b"\n" + slice`, where the slice is the bytes strictly between
    its marker lines INCLUDING the newline that ends its last text line. Both targets end with
    a newline, so the joining byte is one `\n`.
 4. `.agent/plan.md` is replaced WHOLE by PLAN17. Measure its line count against the AGENTS.md
    cap of 50 and report the number you measured; it carries `## Goal` and `## Next Steps`.
 5. This round changes only `docs/` and `.agent/`, so no mutation red-proof over production
    code is owed and none is ordered. The documentation gate of §3 verification tier 5 applies
    instead and is gate G4 below.
 6. Env-var assignment (`VAR=x cmd`, `env VAR=x`, `export`) and `cp` are DENIED by this
    sandbox. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`. Capture real exit
    codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess.run`.
 7. The primary checkout satisfies `git status --porcelain` empty at the handback.
 8. Report every number you measure even where it differs from a number above.
 9. In the change-set section the runs of SPACES that align the `ins / del` column carry no
    meaning and are not appliable bytes: the appliable bytes are the four marker-delimited
    slices alone, each proved against its own target by its own gate (§3 item 37).


AUTHORED SLICES

--- BEGIN-SPINE17 ---
Remedy deliberately ships no worker-onboarding command. Delegating a task to
an external tool ran through a builder adapter and a bounded command template,
and F275 deleted both together with the runner that used them, so there is no
`worker doctor`, `worker add` or `worker disable` and no stub standing in for
them. The bounded-subprocess guard those rails were built on survives as
`packages/orchestration/exec_guard.py`, which F085 owns; a future feature that
reintroduces external workers builds on that guard rather than on the deleted
adapter.
--- END-SPINE17 ---

--- BEGIN-PLAN17 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 17 is a REPAIR round. Round 16's gate G4 went red because three operator-facing sections
of `docs/guides/simple-operator-quickstart-v0.md` still advertised `worker doctor`, `worker
add` and `worker disable` after the commit that deleted them; the reviewer's change set never
named that file. This round books round 16's FAIL verdict, registers R-0861 and sweeps every
surviving advertisement across three documentation pages, replacing the core product spine's
worker section with the deliberate-absence note AGENTS.md requires.

## Next Steps

1. The `overnight_executor` component, the order file's first line. It is a SINGLE module.
2. The remaining components in the recorded order — `worker_registry`, then
   `overnight_readiness`, then the `provider_trust` / `provider_trust_verification` pair,
   which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0861 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep,
   R-0858's repair of F267 and R-0859's referential-closure test.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 84 by distinct id at this round's base `12dd60ad`; the ledger commit this
  block fixes as C2 registers one, taking it to 85. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- The advertised-commands guard did NOT catch these three sections, which is R-0847's blindness
  measured a third time. Until R-0847 is fixed, every deletion round of this feature runs the
  token sweep by hand and reads its RAW list, not only its stripped count.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN17 ---

--- BEGIN-SLIPS17 ---
2026-09-09 · F275 R16 · The round 16 block ordered the `related=("worker.doctor", "mission.report")` tuple repaired on "the surviving `mission.run` record". That tuple belongs to the `doctor.core` record; `mission.run` carries a different one, `related=("mission.report", "mission.ledger", "dogfood.run-loop")`. The worker resolved the tuple to the record that actually carries it and applied the order there, then declared the difference, which is the correct reading of an order whose quoted bytes are unambiguous and whose attribution is not. The reviewer re-resolved every `related=` tuple in the catalog at the base and confirms the worker: the owners are `worker.add`, `mission.run`, `doctor.core` and `repo.status`. The lesson is that an order naming a RECORD and quoting its BYTES must have the record resolved mechanically before emission, exactly as §3 item 9 requires of a `file:line` citation, because the quoted bytes were right and only the name beside them was wrong.

2026-09-09 · F275 R16 · The R-0859 slice the round 16 block shipped states that `mission.ledger` names `dogfood.run-loop` and that a `readiness`-group record names `readiness.show`. Both attributions are wrong: the owners are `mission.run` and `repo.status`, resolved by the reviewer at `38e03d2f` by walking back from each `related=` line to its `command_id`. The finding's load-bearing claims are untouched — two dangling references exist, at those two sites, naming those two deleted commands, and no guard in the repository resolves `related=` at all — so under AGENTS.md's prose-slips rule this is a non-load-bearing inaccuracy in landed text and earns a dated line rather than a correction round. The record is append-only and the sentence stands; this line is the correction a later reader will find beside it.

2026-09-09 · F275 R16 · The round 16 block predicted `apps/cli/commands/worker_facade_cmd.py` at 0/210 and `tests/cli/test_worker_facade_cmd.py` at 4/157, and the round landed 0/218 and 4/166 for a C3 total of −2519 against a predicted −2502. The difference is entirely the worker deleting `_ADAPTER_PATCH` and `_SAVE_ADAPTER`, two module-level constants that the four test classes the block ordered deleted were the only readers of. The block did not name them; the worker deleted them inside a path the change set does name, declared it, and was right — R-0855's fix clause binds every deletion round of this feature to sweep the constants left with no reader, and leaving those two would have been the very defect that clause exists to prevent. The lesson is that a block ordering a test CLASS deleted also names the module-level constants that class alone reads, rather than leaving the worker to choose between an unswept constant and an unordered edit.
--- END-SLIPS17 ---

--- BEGIN-LEDGER17 ---
Gate: F275 R16 — the F275 round 16 entry. VERDICT FAIL, on gate G4 alone, booked by round 17 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `12dd60ad`. THE VERDICT WAS ISSUED BY THE PLANNER AND REVIEWER OF SESSION 9, which re-ran every one of the eight gates itself against the COMMITTED blobs over the range `38e03d2f`..`12dd60ad`; the worker's report was evidence for nothing. THE FAIL IS THE REVIEWER'S DEFECT AND NOT THE WORKER'S, and it is recorded that way because the record is read later by sessions deciding whom to trust. G4 ordered that every line surviving the completeness sweep with backtick-quoted spans stripped must lie in `docs/roadmap/features/`. It does not: the reviewer's own independent re-run reads RAW 16 and STRIPPED 6 over 1676 tracked files outside `.agent/` and `.data/`, and THREE of the six stripped lines are in `docs/guides/simple-operator-quickstart-v0.md` — a user-facing quickstart whose sections `### Check worker readiness`, `### Add a worker` and `### Disable a worker` each still instruct an operator to run a command that commit C3 deleted. That path was never named in the block's exhaustive change set, so under constraint 2 the worker could not repair it without leaving its scope; it declared the red gate and stopped, which is the sanctioned move and the same one round 14's worker was credited for. THE RAW LIST SHOWS FOUR MORE ADVERTISEMENTS THAT THE STRIPPED FILTER HIDES and that are just as stale — three quickstart table rows mapping the deleted `worker` commands onto the deleted `builder adapter-*` commands, two command-taxonomy rows in `docs/system/core-product-spine-v0.md`, and a five-step `## How Claude Code fits` section in `docs/system/mission-run-loop-morning-report-v0.md` whose every step names a rail rounds 13, 15 or 16 deleted — so the round 17 repair sweeps the raw list rather than the binding count. EVERY OTHER GATE PASSED AND WAS RE-RUN INDEPENDENTLY. Six single-parent commits C0a `e5fe544f`, C0b `3720c48b`, C1 `453b80d6`, C2 `876dc89e`, C3 `3384dd53` and C4 `12dd60ad`, per-commit insertions 395, 275, 20, 18 and 13 for the five before the handback commit, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 was the PRIMARY proof of §4 item 9: the reviewer's own delegation source and both committed copies are 45340 bytes at `994447338d251f5fb4a068aef05ea266acd07e362d150b80713d7abf84e253bb` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to PLAN16 at 2454 bytes, 45 lines against the cap of 50, both mandated headings present, the block 395 lines against its cap of 490. G3, over TWO appends: `.agent/live_review.md` 634559 to 650049, growth 15490 = 1 + 15489; `.agent/prose_slips.md` 185058 to 189111, growth 4053 = 1 + 4052; for both the prefix and suffix byte-exact and the joining byte read back as a newline; N COUNTED from each slice by the reviewer's own reader as 4 and 5, ordered equality over the WHOLE appended region; and BOTH negative controls, flipped IN MEMORY inside the FIRST appended paragraph per §3 item 36, REJECTED by BOTH readers, with both files re-read from disk and byte-equal to their committed post-blobs. `^Gate: ` 37 to 38, and `^Gate: F275 R15 `, `^Done: R-0855 — `, `^- R-0859 — ` and `^- R-0860 — ` exactly 1 each; THE OPEN SET 83 TO 84 BY DISTINCT ID against registrations 87 to 89 and resolutions 4 to 5, the fifth being the R-0855 this round's predecessor resolved. G5: through the SHIPPED readers, by import with the resolved `__file__` printed at both ends, `_BASE_CATALOG` and `collect_all_handlers()` both fell 250 to 237, `GROUPS` 48 to 47 and `ALL_KNOWN_ACTIONS` 106 to 100, zero duplicate ids at both ends; the `builder` group and all TEN of its ids ABSENT from both readers at C3; the `worker` GROUP still present with exactly its nine surviving ids and `worker.doctor`, `worker.add` and `worker.disable` gone; `patch.approve`, `do.continue`, `mission.run`, `mission.report` and `doctor.core` all PRESENT. THREE PROPERTIES THIS ROUND TURNED ON WERE MEASURED RATHER THAN ASSUMED: the catalog's `# ── ` section comments fell 57 to 56, so exactly one disappeared and the `# ── brain ───` comment the reviewer's own first dry run had swallowed SURVIVED; the dangling `related=` set at C3 is EXACTLY `dogfood.run-loop` and `readiness.show` with `worker.doctor` gone from it, so the repair landed; and the regenerated order file holds FOUR components against five, EQUAL to a fresh regeneration from the live import graph at both ends, a PURE shrink with no survivor moving and its 26-line header sha256 unchanged at `aff913e6…`. G6: ALL FOUR RED-PROOFS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE AT C3, `__pycache__` purged before every run, `python3 -B`, each probe's control run over that probe's OWN selection in the SAME script immediately before its mutation — controls exit 0 at 3, 3, 3 and 37 passed against mutants exit 1 at 1, 1, 2 and 2 failures — every target restored byte-identically and proved by sha256, worktree porcelain empty. G7: THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18603 passed, 23 skipped and ZERO failed, with 18603 + 23 = 18626 equal to the C3 collection; the id arithmetic closes at 18712 to 18626, 86 LOST and ZERO gained. G8: `.agent/STOP` absent, porcelain empty, ONE worktree, branch correct, and the C3 path set an EXACT MATCH on 24 paths with the missing and extra sets both EMPTY. WHAT THE ROUND ACHIEVED, and it is not undone by the FAIL: the ELEVENTH module group, `main_builder_adapter` at 964 module lines, in ONE commit at 13 insertions against 2519 deletions over 24 paths, taking its 143-line handler whole, the `builder` group and its TEN commands, SIX `ContractAction` members, two test files, two documentation pages and the three `worker` commands R-0857's fix clause ordered deleted rather than narrowed a second time. TWELVE DEVIATIONS WERE DECLARED AND ALL TWELVE ARE SUSTAINED; three are the reviewer's own authoring errors and are dated `.agent/prose_slips.md` lines rather than ids, per amend0827-process-diet rule 2, because not one put anything wrong on disk beyond what G4 already names. THE ROUND'S ONLY DEFECT ON DISK IS REGISTERED BELOW AS R-0861, and the repair is ordered by the block this entry travels in.

- R-0861 — Medium, THREE OPERATOR-FACING DOCUMENTATION PAGES STILL INSTRUCT A USER TO RUN COMMANDS THIS FEATURE HAS DELETED, AND THE GUARD BUILT TO CATCH EXACTLY THAT DID NOT FIRE. Measured by the reviewer of session 9 at `3384dd53` by running the round 16 block's own G4 sweep independently over the 1676 tracked files outside `.agent/` and `.data/`: RAW 16 lines, STRIPPED 6, and three of the six outside the declared scope. THE INSTANCES. FIRST, `docs/guides/simple-operator-quickstart-v0.md` — a page whose title promises a quickstart for operators — carries three whole `###` sections, each with a fenced `bash` block, telling a reader to run `remedy worker doctor claude --json`, `remedy worker add claude --json` and `remedy worker disable claude --json`; all three commands were deleted at `3384dd53` and every one of those blocks now fails with an unknown-command error. The same page's "Normal command / Advanced equivalent(s)" table maps those three onto `builder adapter-enable`, `builder adapter-show` and `builder adapter-enable --disabled`, which the same commit also deleted, so the row maps a dead command onto a dead command. SECOND, `docs/system/core-product-spine-v0.md` describes `remedy worker add claude` in the prose of its `## What a worker is` section and lists `worker doctor <name>` and `worker add <name>` as two rows of its command-taxonomy table. THIRD, `docs/system/mission-run-loop-morning-report-v0.md` carries a five-step `## How Claude Code fits` section whose step 1 is `remedy worker add`, whose steps 2 and 3 are the managed execution round 15 deleted, and whose step 4 is the sandbox intake round 13 deleted — a path that has not existed end to end for two rounds. WHY NO GATE CAUGHT IT: `tests/cli/test_advertised_commands.py` PASSED over this state at exit 0. It caught one instance in the same file family during the reviewer's dry run and misses these, which is the third measured face of the OPEN finding R-0847 — the advertised-commands scanner is blind to advertisement forms it does not model, and a spaced command name inside a fenced block or a table cell is one of them. WHY THIS IS AN ID AND NOT A PROSE SLIP: three tracked files under `docs/` instruct a user to run commands that do not exist, which is wrong state on disk in the tree AGENTS.md's Documentation Updates section governs, and it is worse than a stale comment because a reader follows it. WHAT WOULD RESOLVE IT, and the block this entry travels in orders exactly that: the three quickstart sections and three table rows deleted; the spine's worker section body replaced by the deliberate-absence note AGENTS.md's Code Discoverability Conventions require, since text search cannot find a command that does not exist and that section is where a reader looks for one; the spine's two taxonomy rows deleted; and the morning report's `## How Claude Code fits` section deleted whole. FIX CLAUSE, BINDING ON EVERY REMAINING DELETION ROUND OF THIS FEATURE: the completeness sweep is read as its RAW list and not only as its stripped count, because a command name inside backticks in a table cell or a fenced block is an ADVERTISEMENT a user will follow and not a mere quotation, and the stripped filter that protects against quoted-token false positives hides exactly those; and the block names every `docs/guides/` and `docs/system/` page the sweep reaches, not only the pages a consumer map predicted.
--- END-LEDGER17 ---


DONE WHEN — five gates, every one EXECUTED with its real exit code recorded

G1 TRANSPORT. `.remedy-wt/f275-r17.md`, the committed `.agent/authored/f275-r17.md` and the
   committed `.agent/last_block.md` are byte-identical: same length, same sha256, all three
   printed. ONE digest comparison; it covers those three artefacts and claims nothing about
   any other bytes (§3 item 37).

G2 THE PLAN, THE BLOCK AND THE SPINE SLICE. `.agent/plan.md` at C1 is byte-identical to the
   PLAN17 slice extracted from the COMMITTED C0a blob between its marker lines, markers
   excluded; print its length, sha256 and line count against the cap of 50; both mandated
   headings present. Report the C0a blob's TOTAL line count against the cap of 490. Then show
   that the SPINE17 slice occurs EXACTLY ONCE in `docs/system/core-product-spine-v0.md` at C3
   and that its bytes there are byte-identical to the slice.

G3 THE RECORD, over TWO appends — `.agent/live_review.md` and `.agent/prose_slips.md` at C2:
   (a) BYTE READER: pre-length, post-length, growth == 1 + slice length; the pre-blob a
       byte-exact PREFIX of the post-blob; the slice a byte-exact SUFFIX; the joining byte read
       back out of the post-blob is `b'\n'`.
   (b) STRUCTURAL READER: your script COUNTS N from each slice — never a number this block
       asserts — and the LAST N blank-line units of the whole post-file equal the slice's N
       paragraphs IN ORDER, unit by unit, with a per-unit sha256 printed on both sides.
   (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each
       file (§3 item 36) and show that reader (a) and reader (b) BOTH reject the mutant and
       BOTH accept the truth. Re-read both files from disk afterwards and show them byte-equal
       to their committed post-blobs.
   (d) COUNT PATTERNS in the post-blob of `.agent/live_review.md`: `^Gate: ` rises by exactly
       1; `^Gate: F275 R16 ` and `^- R-0861 — ` are each exactly 1.
   (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted: report registered, done
       and open before and after. The reviewer measured 89 / 5 / 84 at the base.

G4 THE SWEEP IS CLEAN, which is the gate round 16 failed. Over every tracked file outside
   `.agent/` and `.data/` at C3, sweep for these tokens: `main_builder_adapter`,
   `main-builder-adapter`, `BUILDER_ADAPTER_`, `BUILDER_PACKAGE_CREATE`, `BUILDER_SESSION_`,
   `managed_builder_execution`, `managed-external-builder`, each of the ten `builder.<sub>`
   command ids, `worker.doctor`, `worker.add`, `worker.disable`, `worker doctor`, `worker add`,
   `worker disable`, `get_builder_adapter_spec`, `save_builder_adapter_spec`,
   `BuilderAdapterSpec`, `BuilderAdapterMode`, `execution approve` and
   `execution template-show`. PRINT THE RAW RESULT IN FULL, never truncated, and then the
   STRIPPED result. TWO BINDING CONDITIONS, and the first is the one round 16 lacked: every
   RAW line outside `docs/roadmap/features/` lies in a file this block's change set NAMES, and
   every STRIPPED line lies in `docs/roadmap/features/`. The reviewer measured RAW 11 and
   STRIPPED 3 after this change set, with the three stripped lines in `T2_F262.md`,
   `T2_F267.md` and `T8_F151.md` and the single remaining `docs/system/` raw line being the
   deliberate-absence note this round ADDS, which quotes the deleted command names on purpose.

G5 THE GUARDS, THE SUITE AND THE TREE.
   (a) `python3 -B -m pytest tests/docs/ tests/cli/test_advertised_commands.py
       tests/cli/test_product_spine.py tests/cli/test_cli_ux.py tests/test_grouped_cli.py -q`
       — exit 0. This is the §3 verification-tier-5 documentation gate for a `docs/` round.
   (b) The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` — exit 0.
   (c) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout,
       with C3 COMMITTED. BINDING: zero failed, and passed + skipped equals the C3 collection.
       No `.py` file is in this round's change set, so the reviewer expects the round 16
       figures unchanged at 18603 passed and 23 skipped against a collection of 18626 — report
       what you measure, and report any difference as a finding rather than absorbing it.
   (d) `.agent/STOP` re-read from disk and reported ABSENT; `git status --porcelain` empty;
       `git worktree list` naming the primary checkout ALONE; branch correct. Compare
       `git diff --name-only <C2>..<C3>` against this block's three C3 paths as a SET and
       report the missing and extra sets, both of which must be EMPTY. For every commit BEFORE
       C4, report its parent count and its insertion count against the cap of 500; C4's own
       numbers belong to the next round's ledger entry (§3 item 31).


HANDBACK

Rewrite `.agent/handoff.md` WHOLE at C4, per docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3). It carries: SESSION 9 of F275, round 17; the range; a per-commit
changed-files table with the `+/-` column read from `git show --numstat` and compared cell by
cell against the Verification lines (§3 item 28); ONE LINE PER GATE with its real exit code;
the authored-text proofs table; every deviation, declared rather than repaired; the item-status
table; the open-findings count; and the next expected action. Push ONCE, after C4. Create no
PR, edit none, merge none.

Write no verdict, no `Done:` paragraph and no finding of your own. If the sweep this round
performs makes you believe R-0861 is resolved, write `Landed: R-0861 — <one line>` in the
handback and nothing else; the reviewer authors the resolution at the next gate.
