# Handoff — F260 One world · round 10 · THE RESOLVER RETURNS A STRING

## Session

SESSION 3 of feature F260 · round 10 · rounds so far 10

Context self-assessment (amend0905-throughput): context is comfortable — this
round read four protocol files, one 321-line block and roughly 700 lines of
target source, and spent no rounds on rework. More delegated rounds fit in this
session.

## Range

Review of `ce08cfd0da8da2f2ad12237d385d26ea85698f0f`..`HEAD`.

Six commits before this one, all single-parent, in the block's ordered sequence
C0a → C4. No reordering, no extra commit, no dropped commit. C5 is this file.
Largest insertion count 320 (`.agent/authored/f260-r10.md`, a single `.agent/**`
state write and exempt under the AGENTS.md counting rule); largest CODE commit
37. Nothing approached the 500-insertion cap.

## Commits

### e0bbad3d f260: save the round 10 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r10.md | +320 / -0 | C0a — the block copied byte-for-byte with `shutil.copyfile`, verified by `cmp` (silent) before staging |

### 52864610 f260: mirror the round 10 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +224 / -304 | C0b — same bytes again by `copyfile`, verified by `cmp` |

### 6fcc4223 f260: point the plan at the string-returning resolver
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22 / -22 | C1 — whole-file replacement from the PLAN slice; 48 lines, under the AGENTS.md 50-line cap |

### a58f4ae0 f260: book the round 9 verdict and resolve finding R-0814
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | C2 — DONE0814 appended FIRST, then GATE_R9, in the order constraint 7 fixes; 904283 → 912232 bytes |

### 39581d7f f260: append the three round 9 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +6 / -0 | C3 — SLIP4/5/6 appended; 101682 → 105750 bytes |

### d2af8906 f260: make the classic resolver return a string and the loader take either
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/data_paths.py | +18 / -13 | `resolve_job_id` annotated `-> str`; parse path `str(UUID(raw))`, prefix path `matches[0]`; docstring rewritten to carry the classic-store restriction in the SEARCH; `Public API::` line updated; `resolve_any_job_id`'s docstring corrected where this change falsified it (deviation D2) |
| packages/orchestration/storage.py | +8 / -3 | `load_job` / `load_job_safe` take `UUID \| str` with the one-line WHY comment above `load_job`; `JobNotFoundError.__init__` widened to match (deviation D3) |
| apps/cli/commands/job_stop_cmd.py | +1 / -1 | line 119: the now-redundant `str(` dropped |
| apps/cli/commands/project.py | +1 / -1 | line 449: the now-redundant `str(` dropped |
| tests/test_data_paths.py | +6 / -4 | three return-type assertions compare against `str(uid)`; `test_full_uuid_returns_uuid` RENAMED `test_a_full_uuid_resolves_to_its_own_canonical_string_form` |
| tests/cli/test_patch_cmd.py | +3 / -2 | two return-type assertions compare against `str(job.id)`; the uppercase test NOT weakened — it still asserts the canonical lowercase form |

### C5 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | the round-10 handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/base-probe ce08cfd0` | created, detached at `ce08cfd0`, to measure the G6 suite-3 base count (deviation D1) |
| `git worktree remove .remedy-wt/base-probe --force` | removed |
| `git worktree add .remedy-wt/g7-wt d2af8906` | created, detached at `d2af8906`, for G7 only |
| `git worktree remove .remedy-wt/g7-wt --force` | removed; `git diff` inside it was EMPTY before removal, so both mutations were fully reverted |
| `git worktree prune` | run; the eleven remaining `.remedy-wt/job-*` worktrees are pre-existing `remedy/job-*` branches from earlier job runs, NOT created by this round and NOT touched |
| `git push -u origin feature/f260-one-world` | pushed after C5 |

No pull request created, none merged, no force-push, no work on `main`.

## Verification

ONE LINE PER GATE, each with its REAL exit code. No gate is reported as a word.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | `sha256sum` over `.agent/authored/f260-r10.md` and `.agent/last_block.md` both return `28a3d69386e087be9fb6c8bd723592cc8121e60c5417686eea53e02fe6545f87`, equal to the digest carried in the delegation and to `.remedy-wt/f260-r10-block.md`. `cmp` silent for both pairs. One reading, not a chain. |
| G2(a) EXACT IMAGE | 0 | the C2 post-image EQUALS `pre + b"\n" + DONE0814 + b"\n\n" + GATE_R9 + b"\n"` byte for byte, byte-equality **True**. Measured length 912232 (pre 904283 + 1 + 2934 + 2 + 5011 + 1). `pre` re-read from `git show ce08cfd0:.agent/live_review.md`, sha256 `7adf2ccf…`, identical to the file before C2. |
| G2(b) STRUCTURAL | 0 | split on `"\n\n"`: units 428 → **430**, exactly as ordered. The last TWO units, with the file's terminating newline stripped from the final one, equal DONE0814 and GATE_R9 IN THAT ORDER — byte for byte. |
| G2(c) NEGATIVE CONTROL | 0 | **the reworded clause is satisfiable and satisfied.** One byte flipped at absolute offset 904324 (inside the DONE0814 region 904284–907218), same length as the post-image: reading (a) → **False**, reading (b) → **False**, BOTH reject. After restore, (a) → True and (b) → True, both accept. This is the clause round 9 could not pass; rewording (a) from a length-plus-prefix test to an exact-image equality fixed it, as SLIP4 predicted. |
| G2(d) POPULATIONS | 0 | `^Gate: ` headers **19**, all 19 distinct; `^- R-\d{4} — ` registrations **299** over **299 distinct** ids; `^Done: R-\d{4} — ` lines **5** over **THREE** distinct ids (`R-0721`, `R-0725`, `R-0814`); `^Landed: R-0814 — ` still exactly **1** and byte-identical to `ce08cfd0` (compared against the base line, not merely counted). |
| G3 THE SLIPS | 0 | post-image EQUALS `pre + b"\n" + SLIP4 + b"\n\n" + SLIP5 + b"\n\n" + SLIP6 + b"\n"`, byte-equality **True**; 101682 → 105750 bytes; blank-line units 134 → **137**, a rise of exactly THREE, one per slip. Not 135, not 136 — the separators did not fuse. |
| G4 THE PLAN | 0 | `.agent/plan.md` equals the PLAN slice plus exactly one trailing newline (2577 + 1 = 2578 bytes), byte-equality **True**; **48 lines**, under 50. |
| G5(a) TYPE | 0 | asserted on `isinstance`, never on the annotation. Full-id form → `str` and NOT `UUID`; unique-prefix form → `str` and NOT `UUID`. Read from the SHIPPED function with `REMEDY_DATA_DIR` at a scratch directory, module resolving from the primary checkout as expected for a non-destructive probe. |
| G5(b) CASE | 0 | `resolve_job_id('0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D')` → `'0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d'`, the canonical lowercase string, with the fixture first asserted to really change case. This is the property a naive `return raw` destroys, and G7(ii) proves the test catches it. |
| G5(c) EXIT CODES | 0 | ambiguous prefix `aaaa1111` → exit **2** (`Error: ambiguous job id prefix 'aaaa1111' matches 2 jobs:`); unmatched prefix `deadbeef` → exit **1** (`Error: no job matches prefix 'deadbeef'`); invalid string `not-a-job-id!!` → exit **1** (`Error: invalid job ID: 'not-a-job-id!!'`). Unchanged from the base contract. |
| G5(d) THE LOADER TAKES BOTH | 0 | with a classic job on disk, `storage.load_job(job.id)` and `storage.load_job(str(job.id))` return EQUAL `Job` records, and both are the saved one. NON-VACUITY: the two arguments were asserted to be of genuinely different types (`UUID` vs `str`) and not the same object, so a loader ignoring its argument could not pass. `load_job_safe` checked the same way. |
| G6 suites, group 1 | 0 | `pytest tests/test_data_paths.py tests/cli/test_patch_cmd.py -q -p no:randomly` → **59 passed** |
| G6 suites, group 2 | 0 | `pytest tests/cli/ -q -p no:randomly` → **1537 passed** in 327.98s. Carries the canary `tests/cli/test_golden_path.py`. |
| G6 suites, group 3 | 0 | `pytest tests/ui_server/test_command_channel.py tests/ui_server/test_live_state.py tests/orchestration/test_test_runner.py -q -p no:randomly` → **203 passed** serially. The block predicts 262 at base; the base really is 203 — see deviation **D1**. Serially green at base AND at HEAD, which is the property the gate exists for. |
| G6 integrity | 0 | `python3 -m apps.cli.grouped integrity check --json` → `"passed": true`, `"fail_count": 0`, `"check_count": 5` (handler_import handlers=342, live_review_verdict, plan_consistency, relevant_untracked, high_blockers_open). |
| G7 MUTATION | 0 | see the block below. |
| G8 LINT + CLEAN | 0 | `ruff check` over exactly the six change-set paths under `packages/`, `apps/`, `tests/` → "All checks passed!". `git status --porcelain` EMPTY. `git ls-files .remedy-wt` EMPTY. |

The three suite groups were run SERIALLY, one after another, each invoked
directly so its own exit code is the one reported — never piped into `tail` or
`head`, which would report the pipe's status instead (the F260 R3 lesson).

### G7 — mutation red-proof, in the disposable worktree at `d2af8906`

`__pycache__` purged before every run and `python3 -B` used throughout. Module
resolution was confirmed BEFORE any colour was trusted:
`packages.orchestration.data_paths` resolved to
`.remedy-wt/g7-wt/packages/orchestration/data_paths.py`, inside the worktree and
never the primary checkout — checked because an installed `remedy` distribution
can shadow a worktree. Each mutation target was verified to occur EXACTLY ONCE in
its file before the edit (checklist item 25); the revert target is named by exact
path, `.remedy-wt/g7-wt/packages/orchestration/data_paths.py`, in both cases.

| Step | Exit | Reading |
|---|---|---|
| (i) unmutated control | 0 | **59 passed** — the baseline every colour below is measured against, plus a type probe reading `full=str prefix=str` |
| (ii) parse path drops the normalisation (`UUID(raw); return raw`) | 1 | 1 failed, 58 passed. Failing node id: `tests/cli/test_patch_cmd.py::TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does` — exactly the test the block predicts |
| (iv) control after (ii) | 0 | **59 passed**, and `git diff` in the worktree EMPTY |
| (iii) prefix path back to `return UUID(matches[0])` | 1 | the G5(a) type assertion FAILS as ordered: the type probe reads `prefix=UUID`, so `prefix_is_str` is **False**. The suite is red too at 2 failed, 57 passed. Failing node ids: `tests/test_data_paths.py::TestResolveJobId::test_short_prefix_resolves` and `tests/cli/test_patch_cmd.py::TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_a_short_hex_prefix_records_exactly_as_the_full_id_does` — see deviation **D4** on naming a node id for a probe |
| (iv) control after (iii) | 0 | **59 passed**, and `git diff` in the worktree EMPTY |

## Authored-text proofs

| Text | Proof |
|---|---|
| the whole block | `.agent/authored/f260-r10.md` and `.agent/last_block.md` are byte-identical to `.remedy-wt/f260-r10-block.md` — `cmp` silent for both, and all three sha256 to `28a3d693…`. Applied by `shutil.copyfile`, never re-typed and never text-extracted. |
| PLAN | `.agent/plan.md` == PLAN slice + exactly one `\n`, byte-equality True (2578 bytes) |
| DONE0814 + GATE_R9 | the C2 post-image == `pre + "\n" + DONE0814 + "\n\n" + GATE_R9 + "\n"`, exact-image equality True; and structurally the last two `"\n\n"` units equal the two slices in that order |
| SLIP4 / SLIP5 / SLIP6 | appended at 1394 / 1487 / 1181 bytes with `"\n\n"` separators; exact-image equality True and unit rise exactly 3 |

All six slices applied BYTE FOR BYTE, extracted programmatically from the block
between its marker lines. None was repaired, reflowed or reworded. No marker line
reached any file.

## Deviations & assumptions

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4,
C5, in that order, one commit each. No path outside the block's change set was
written.

**D1 — G6's "(262 passed at base)" is unreachable; the base is 203.** The block
annotates suite group 3 with 262 passed at `ce08cfd0`. Measured rather than
assumed: in a disposable worktree at `ce08cfd0` those three files collect
`tests/orchestration/test_test_runner.py: 52`,
`tests/ui_server/test_command_channel.py: 106`,
`tests/ui_server/test_live_state.py: 45` — **203** — and run **203 passed** in
20.53s. At HEAD they collect 203 and run **203 passed**. This round touched none
of the three: `git log ce08cfd0..HEAD -- <those three paths>` is EMPTY. So the
numeral is a reviewer measurement error, not a lost test, and the property the
gate exists for — the group that the reviewer's parallel probe reddened is green
when run serially, at the base and after the change — is DELIVERED at 203. I
recorded the gate against the measured base rather than editing anything to reach
262. Reviewer-prose defect; nothing wrong on disk.

**D2 — two stale docstring sites in `resolve_any_job_id`, inside a change-set
file, corrected beyond the SPEC's enumeration.** SPEC (1) orders the docstring of
`resolve_job_id` and the `Public API::` block. But `resolve_any_job_id`'s
docstring asserted, of the function this round changes, that
"`resolve_job_id` searches only the classic store and returns a ``UUID``, which a
16-hex task-job id can never be" — a sentence THIS ROUND makes false. Left alone
the file would ship a docstring contradicting the function two definitions above
it. Corrected to put the restriction on the SEARCH ("where a 16-hex task-job id
can never match") and to note both now return `str`. The adjacent sentence "The
return type is ``str`` rather than ``UUID``" drew a contrast that no longer
distinguishes the two functions; the four words were dropped. This is the same
class as round 9's deviation D4, which the reviewer upheld: a stale site inside a
file the block already names, falsified by the ordered change.

**D3 — `JobNotFoundError.__init__` widened to `UUID | str`, beyond SPEC (2)'s
enumeration.** SPEC (2) names `load_job` and `load_job_safe` and adds that "both
exception paths already format the id" — true at RUNTIME, and no runtime
behaviour changed. But the ANNOTATION does not survive: `load_job(job_id: UUID |
str)` now passes a `str` into `JobNotFoundError(job_id: UUID)` on its
not-found path, and `[tool.mypy]` is configured in `pyproject.toml`, so this
round would have INTRODUCED a type error the base did not have. One token
widened, same file, same change set, no behaviour change. Declared rather than
done silently because the SPEC had visibly considered the exception paths and
concluded no change was needed.

**D4 — G7(iii) names a node id for something that has none, and reddened two
tests rather than one.** The clause reads "At least one type assertion of G5(a)
must FAIL. Name the node id." G5(a) is a PROBE over the shipped function, not a
pytest test, so it has no node id — a small incoherence between the two gates. I
satisfied both halves: the G5(a) type assertions were re-run inside the mutated
worktree and `prefix_is_str` really is False there, AND the two pytest node ids
that redden under the same mutation are named in the table above. "At least one"
is satisfied at two; neither is a surprise, since both assert the prefix path's
result against a string.

**D5 — `ruff` was invoked as `python3 -m ruff check`.** The gate says `ruff
check`. The bare console script is not on PATH in this sandbox for the same
reason `remedy` is not; `python3 -m ruff` runs the identical entry point over the
identical six paths. Exit 0, "All checks passed!".

**Assumption, stated because it is load-bearing:** the `remedy` console script is
denied in this sandbox, so G6's CLI reading was taken through
`python3 -m apps.cli.grouped integrity check --json`, which is the invocation the
block itself orders.

**Scratch hygiene.** Four helper scripts and three probe directories were created
under the gitignored `.remedy-wt/` and removed BY EXACT PATH, never by glob:
`.remedy-wt/r10_slices.py`, `.remedy-wt/r10_g2.py`, `.remedy-wt/r10_g5.py`,
`.remedy-wt/r10_g7.py`, and the `g5-65v9m54w`, `g5-kf870ua6`, `g5-lpct1g01`
directories. Both worktrees were removed and `git worktree prune` run. The eleven
pre-existing `.remedy-wt/job-*` worktrees belong to earlier `remedy/job-*`
branches and were deliberately left alone. `.remedy-wt/f260-r10-block.md` is the
reviewer's own transport artifact and was not removed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 plan.md ← PLAN | done | |
| C2 live_review.md ← DONE0814 then GATE_R9 | done | order per constraint 7 |
| C3 prose_slips.md ← 3 slips | done | |
| C4 the signature change | deviated | SPEC applied in full, plus two stale docstring sites (D2) and one annotation (D3) inside change-set files |
| C5 handback | done | this file |
| G1 transport | done | PASS — one digest across all three artifacts |
| G2 the record | done | PASS — (a) (b) (c) (d) all green; the reworded negative control now rejects as intended |
| G3 the slips | done | PASS — units 134 → 137 |
| G4 the plan | done | PASS — 48 lines, byte-exact |
| G5 the resolver contract | done | PASS — (a) (b) (c) (d) all green |
| G6 the suites | deviated | all three exit 0 (59 / 1537 / 203) and integrity 5 checks 0 fail; the block's "262 at base" numeral is wrong, base measured at 203 (D1) |
| G7 mutation red-proof | deviated | PASS — both mutations red at named node ids, control 59 green throughout, worktree diff empty after each restore; the "node id" wording for a probe is D4 |
| G8 lint and clean tree | done | PASS — ruff 0 over six paths, tree clean, no tracked scratch |

## Open findings

**296 open by DISTINCT ID.** `.agent/live_review.md` holds 299 registration
paragraphs carrying 299 distinct ids, against 5 `Done:` lines carrying THREE
distinct ids (`R-0721`, `R-0725`, `R-0814`), all three of which are registered
ids. 299 − 3 = 296. The count fell by one from round 9's 297 because R-0814,
LANDED at R9, received its `Done:` paragraph in C2 this round. The §3 item 10
formula that subtracts one raw population from the other still returns 294 here
and is still wrong for the reason SLIP3 recorded: `Done:` LINES outnumber
distinct `Done:` IDS.

## Next

Reviewer gates round 10 against the committed diff `ce08cfd0..HEAD`, re-running
every gate itself. No gate clause is red this round, so no ruling is owed on the
gates; two reviewer-prose items are owed to `.agent/prose_slips.md` by the next
round — G6's "262 passed at base" (D1) and G7(iii)'s node id asked of a probe
(D4). If the verdict is PASS, the next round is the payoff DECISION F260 D4 named:
COLLAPSE `resolve_job_id` and `resolve_any_job_id` into ONE `str`-returning
function over both stores, deleting the loser in the same commit, now that the two
share a return type and `storage.load_job` accepts either. Finding R-0809 — four
wordings for "unknown id", and a real id of the other store rejected — belongs
there. Before authoring it, re-read `.agent/STOP` from disk (self-drive Phase 1
rule 1, before rule 2); it was absent when checked at the end of this round.
