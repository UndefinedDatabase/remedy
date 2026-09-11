# F275 T003 — the `.status.value` family resolved BY TYPE, and it is nine sites rather than seventy-six

> Measured by the reviewer at `abc9b8a9`, this round's base, in one disposable `git
> worktree` under the gitignored `.remedy-wt/`, removed and pruned before this text was
> authored. THIS FILE RECORDS A MEASUREMENT; IT REWRITES NOTHING. No line under
> `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
> It joins `.agent/f275_t003_descriptor_sites.md`, which resolved the OTHER three fields at
> `a815c9a3` and whose method this round repeats without changing it.

## 1. The question, and why a receiver name could not answer it

DECISION F275 D32 names three retype rule families. Two are built. The third — a read of
`.value` on a status that is a `str` after the flip — was left unbuilt by round 58 and
DECISION F275 D34 recorded why: 76 sites over ten receiver names, of which `record` at 18,
`latest`, `c`, `held` and `released` decide nothing by name, and `status` was never in the
ruled site set, which covers `id`, `name` and `description` only. Resolving it by receiver
name is the heuristic DECISION F275 D29's P1 exists to have killed.

This is the receiver-name distribution, recorded so that the thing being refused is on the
page rather than described:

    t 39 · record 18 · task 10 · latest 2 · an unnamed expression 2
    c 1 · proposed 1 · ptask 1 · held 1 · released 1

Four readings were taken instead, in order, and a site is claimed only where one of them
DECIDES it. A fifth was tried and REJECTED; section 7 records that, because a reading that
looks decisive and is not is the more useful half of this artefact.

## 2. THE FIRST FACT, and it narrows the question before any probe runs

`Job` HAS NO `status` FIELD. It has `state`, and `JobPlan.state` is `RunState` on the
unified record exactly as `Job.state` is on the classic one — so `job.state.value` reads
the same enum before and after the flip and is not in this family at all. Read off the live
classes at `abc9b8a9`.

A sweep over the live class objects of every class kind under `packages.` and `apps.` —
328 modules walked, ZERO skipped on import — finds 61 classes declaring a `status` field
and only FOUR whose `status` is an enum:

    packages.core.models.Task                              RunState
    packages.orchestration.job_fulfillment.JobFulfillmentRecord  JobFulfillmentStatus
    packages.orchestration.proposed_tasks.ProposedTask     ProposedTaskStatus
    packages.orchestration.integrity_gate.IntegrityCheck   IntegrityStatus

The other 57 declare `status` as `str`, and `TaskEntry.status` — the unified record's own —
is one of them. So `.status.value` is meaningful on exactly four records, the flip retypes
exactly ONE of them, and the whole question is which chain belongs to which.

## 3. The descriptor probe, run twice

The DECISION F272 D7 probe of round 53, with ONE line changed: its descriptor tuple becomes
`(("Task", "status"),)`. Everything else — the write half, the outward frame walk, the
absolute-`co_filename` test — is that instrument verbatim, and the three defects its
docstring records are therefore not re-introduced.

| Run | pytest summary | probe rows |
|---|---|---:|
| 1 | `18386 passed, 23 skipped, 1 warning in 1288.00s (0:21:28)` REAL_EXIT=0 | 219 |
| 2 | `18386 passed, 23 skipped, 1 warning in 1295.36s (0:21:35)` REAL_EXIT=0 | 219 |

Compared as SETS of `(owner, field, mode, path, line, func)`: run 1 holds 219, run 2 holds
219, SYMMETRIC DIFFERENCE 0. That intersection gives 138 distinct `(path, line)` READ sites
and 81 WRITE sites for `Task.status`.

A FIRST ATTEMPT AT RUN 1 IS DISCARDED AND REPORTED RATHER THAN HIDDEN. The probe was copied
INTO the worktree root, where `ruff check .` scans it, and the run came back `2 failed` with
`test_this_repository_really_is_at_or_below_the_lint_ceiling` red — the exact defect the
probe's own docstring records, reproduced by the reviewer who had just read it. The probe
was moved out and reached through `PYTHONPATH`; both runs above are from that route and
both are green. No row from the discarded run is used anywhere on this page.

## 4. The static sweep

Over the tracked tree at `abc9b8a9`, excluding the three modules that DEFINE the records:

    tracked `.py` scanned            991
    unparsable                         0
    `<expr>.status` attribute nodes  1529
    `<expr>.status.value` chains       76

## 5. THE SPLIT THAT NEITHER A NAME NOR A LITERAL FINDS, and it is decidable without running anything

A `RunState` member is immutable, so `x.status.value = "..."` CANNOT execute against a real
enum. A chain in STORE context therefore proves its receiver is a mock, whatever it is
named and whatever literal sits beside it.

    STORE context (an assignment target)  8
    LOAD  context (a read)               68

All 8 store chains are `t.status.value = "completed" if i == 0 else "pending"` inside test
fixtures, and THREE INDEPENDENT READINGS AGREE on them: the context is Store, the receiver
is bound to `MagicMock()` in the same file in all 8 cases, and the probe recorded NONE of
them as a `Task.status` read. They are mock attribute writes. The flip must leave them
alone: rewriting `t.status.value = x` to `t.status = x` changes what the mock holds, and the
code under test reads it back through `.value`.

This is the split a receiver-name rule gets exactly backwards — `t` is the most common
receiver name in the family, and 8 of its 39 occurrences are not records at all.

## 6. THE SECOND SPLIT: 29 of the 68 reads are ALREADY shape-agnostic

A site written `t.status.value if hasattr(t.status, "value") else str(t.status)` reads an
enum today and a `str` after the flip WITHOUT being rewritten. Twenty-nine of the 68 reads
carry that guard, on the same line or the line before:

    ui_server.py 10 · job.py 7 · propose_cmd.py 4 · ui_view_model.py 2
    worker_queue.py 2 · job_fulfillment.py 1 · proposed_tasks.py 1
    reviewer.py 1 · task_execution.py 1

A rule that rewrote these would be churn, not a fix. That leaves 39 BARE reads.

## 7. THE FOUR READINGS, AND THE ONE THAT WAS REJECTED

Each of the 68 reads is assigned an owner by the first reading that decides it:

    the probe                 26   a recorded `Task.status` read at that exact (path, line)
    a unique literal          19   a compared string in exactly one of the four enums
    the module's own record   13   the chain sits in the module that defines the record
    the receiver's binding     8   `latest = records[-1]` from `list_fulfillment_records`,
                                   `for task in job.tasks`, `held = self._fulfill(...)`
    UNDECIDED                  2

THE REJECTED READING was "the set of records the FILE imports or names". It is unsound and
the probe proves it: `packages/orchestration/ui_server.py` names only `ProposedTask`, while
the probe records SEVEN of its chains as `Task.status` reads. One file holds chains of more
than one owner, so a file-level reading would have mis-assigned them — and it would have
done so silently, in the confident direction. It is recorded here so the next round does not
re-derive it as a shortcut.

## 8. THE RESULT: owner against guard state, over all 76

| owner | guarded | bare | store | total |
|---|---:|---:|---:|---:|
| `Task` | 23 | 9 | — | 32 |
| `JobFulfillmentRecord` | — | 23 | — | 23 |
| `ProposedTask` | 4 | 5 | — | 9 |
| `IntegrityCheck` | — | 1 | — | 1 |
| a FAKE (`_JobPlanAdapter(FakePlan())`) | — | 1 | — | 1 |
| a MOCK | — | — | 8 | 8 |
| UNDECIDED | 2 | — | — | 2 |
| **total** | **29** | **39** | **8** | **76** |

BOTH UNDECIDED CHAINS ARE GUARDED. They are `ui_server.py:1025` and `ui_server.py:1071`,
inside `_build_job_plan_dashboard`, and each carries the `hasattr` guard of section 6 — so
they read correctly whichever record they hold, and the residue this round could not decide
costs the flip nothing. That is a closure rather than a leftover, and it is the reason this
page claims a complete answer while still reporting two sites it could not name.

## 9. WHAT DECISION F275 D32'S THIRD RULE FAMILY ACTUALLY REWRITES

Nine sites. Every one is a BARE `.status.value` read whose owner is `Task`:

    apps/cli/commands/job.py:655
    packages/orchestration/brain_detail.py:353
    packages/orchestration/brain_detail.py:366
    packages/orchestration/brain_detail.py:372
    packages/orchestration/brain_detail.py:380
    packages/orchestration/project_brain.py:317
    packages/orchestration/trust_report.py:118
    tests/orchestration/test_final_audit_evidence.py:261
    tests/orchestration/test_resume_kill.py:261

THIS AGREES WITH THE RESIDUE THE PREVIOUS ROUND MEASURED, which is the cross-check that
matters most here. `.agent/f275_t003_flip_residue_r59.md` section 8 attributes 61 `str.value`
exception lines to two source frames: `project_brain.py:317` at 54 and `trust_report.py:119`
at 7. Both are in the nine. The `trust_report` line is 118 at `abc9b8a9` and 119 in the
flipped tree because rule I5 inserts a minter import above it, which is the same one-line
offset section 7 of that artefact records.

## 10. What this reading does NOT settle

IT DOES NOT BUILD THE RULE. The nine sites are named; no transform consumes them yet, and
nothing here re-ran the flip. Whether rewriting exactly these nine removes exactly the 61
attributed lines is the next dry run's reading, not this one's.

IT SETTLES NOTHING ABOUT `.status` READS THAT ARE NOT FOLLOWED BY `.value`. The sweep found
1529 `<expr>.status` nodes and this page is about the 76 that continue into `.value`. The
other 1453 are a different question: `TaskEntry.status` is already `str`, so a bare
`task.status` read is flip-safe by construction, but that claim is asserted from the field
types and has not been measured site by site.

THE 81 WRITE SITES THE PROBE RECORDED ARE NOT ANALYSED HERE. A write of `Task.status` is a
construction or an assignment, which the flip's existing constructor rules already reach;
no site of this family is among them, and that is the only claim made about them.

THE FOUR-RECORD ENUMERATION IS AS WIDE AS ITS SWEEP. It walked `packages.` and `apps.` and
skipped nothing on import, so it is complete for the tree as it stands; a record introduced
later with an enum `status` would not be in it, and nothing here ratchets that.
