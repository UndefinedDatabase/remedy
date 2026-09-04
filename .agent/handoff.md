# Handoff — F112 Prompt budget per task class, round 29 (HALTED at C3 — closure precondition 6 already discharged at round 21; redundant duplicate self-use run declared, not committed)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-28 carried forward unresolved — "6 (or 7)")
· round 29 · rounds so far 29.

This round is NOT a fresh loop-session bootstrap — it is a direct
continuation of round 28's own session, so the session number is
unchanged from round 28.

## Range

Review of `6dd06718..HEAD` (base is F112 R28's handback commit).

## Commits

### 6132c7af F112 R29 C0a: save the round 29 step block verbatim to .agent/authored/f112-r29.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r29.md` | +187/-0 | transport proof — verbatim copy of the supplied step block |

### d0d38a82 F112 R29 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +146/-174 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 2d2b07af F112 R29 C1: append RECORD28 to live_review.md (books R28 PASS)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD28 (books round 28's PASS verdict; no new finding registered or resolved) |

### 05852956 F112 R29 C2: apply PLAN29 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-26 | whole-file replace with PLAN29, applied byte-exact per constraint 1 even though its own premise was later found stale (see Deviations item 1) |

### 0c08d6d9 F112 R29 C3: self-use step HALTED — precondition 6 already discharged at R21, redundant run declared not committed
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-23 | AGENTS.md "If Blocked" — corrected plan.md to state the true current position after PLAN29's premise was found false; no self-use evidence files were touched by this commit (see Deviations item 1 for why C3 produced no `.agent/selfuse_f112/` diff) |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) |

## External actions

- `git push -u origin feature/f112-prompt-budget-per-task-class` — run
  after this handback commit; outcome reported in the completion message
  to the operator.
- No PR created, no merge, no `--approve`, nothing force-pushed, `main`
  never touched.

## Verification

Real, trimmed transcripts for every gate this round's block ordered:

```
$ sha256sum f112-r29.md (scratchpad)
10d7a6247bee952420a1da3a12d2269a14f8831025742a608bcdc5a12f2812e2  187 lines, 14694 bytes
-> matches the prompt's stated hash/size/line-count exactly.

$ git status --porcelain   # before C0a
(empty)
```

**C0a/C0b — transport:** `sha256sum .agent/authored/f112-r29.md`
reproduced `10d7a6247bee952420a1da3a12d2269a14f8831025742a608bcdc5a12f2812e2`
(matching the scratchpad original exactly). `git hash-object
.agent/last_block.md .agent/authored/f112-r29.md` both printed blob
`ecf064052b64d4ca72e578de479f318a5e534b4f` — identical. `git rev-parse
HEAD:.agent/authored/f112-r29.md HEAD:.agent/last_block.md` (after C0b's
commit) both printed the same blob id, confirmed.

**C1 — the RECORD28 append:** RECORD28 extracted from the committed
authored file (between its `--- BEGIN RECORD28 sha256=... ---` /
`--- END RECORD28 ---` markers, trailing newline stripped) measured
exactly `4171` bytes with sha256
`70db6db54e3e1007aad2b79ef389e7a4f3c1334594d7097dc47b59272f0d95c3`,
matching the marker's own stamp exactly. Pre-append `.agent/live_review.md`
measured `2334372` bytes; append computed as
`content_bytes + b"\n" + RECORD28_bytes`; post-append measured `2338544`
bytes, exactly `2334372 + 1 + 4171`. `cmp` confirmed the pre-append
content is a byte-exact prefix (EOF at byte 2334372, zero differing
bytes reported). File still ends WITHOUT a trailing newline (`xxd` on the
last byte: `2e` = `.`).

Registered/`Done:`/open counts, counted mechanically (registered =
unique ids matching `^- R-\d{4} —`; resolved = unique ids appearing on a
line matching `^Done: R-\d{4}`, since `R-0721` and `R-0725` each appear
on two `Done:` lines — 76 total `Done:` lines, 74 unique resolved ids):

| | registered | Done: lines | unique resolved | open |
|---|---|---|---|---|
| before C1 | 354 | 76 | 74 | 280 |
| after C1  | 354 | 76 | 74 | 280 |

UNMOVED on both sides, exactly matching the block's own expectation
("354 registered, 74 Done, 280 open" — where "74 Done" is the unique-id
reading, consistent with the F110 R15 precedent's own "72 unique resolved
across 74 Done: lines" wording for the same counting convention).

**C2 — the PLAN29 replacement:** PLAN29 extracted from the committed
authored file measured exactly `2249` bytes with sha256
`a7ed5cae805ccd0df3b904ed8642d8d3d3867b3816013d45e39815c48eb87130`,
matching the marker's stamp exactly. `.agent/plan.md` after C2 reproduced
byte-identical (same 2249 bytes), no trailing newline, `wc -l` = 46
(under 50), `## Goal`/`## Next Steps` each occurring exactly once. This
was applied byte-exact per constraint 1 ("apply every delimited slice
BYTE FOR BYTE... if a slice looks wrong, apply it anyway and DECLARE the
problem") — the problem PLAN29's own text carried is declared in
Deviations item 1 below, and C3 corrected plan.md's content afterward.

**C3 — the self-use step, HALTED. Full transcript of what was actually
run, reported in full per the block's own done-when order, even though
none of this landed as committed evidence (see Deviations item 1):**

```
STOP re-check before C3
  os.path.exists('.agent/STOP') = False

=== C3 STEP 1 -- BEFORE ===
load_self_use_queue() -> 7 entries
  SU-001 consumed_by='F257' title='Document the Markdown job-file format under docs'
  SU-002 consumed_by='F258' title="Fix architecture.md's stale 12-group CLI claim (60 groups shipped)"
  SU-003 consumed_by='F106' title="Give apps/ui's ESLint config a TypeScript parser (R-0622)"
  SU-004 consumed_by='F108' title='Give FailureClass a RESOURCE_LIMIT member (R-0568)'
  SU-005 consumed_by='F109' title='Address ledger finding R-0418'
  SU-006 consumed_by='F110' title='Address ledger finding R-0418'
  SU-007 consumed_by='' title='Address ledger finding R-0418'
pending_self_use_items() -> 1 pending of 7 items (SU-007)
next_self_use_item() -> SU-007
EXPECTATION CONFIRMED: exactly 1 pending item, SU-007, next_self_use_item() == SU-007
(matches the block's own step 4b expectation exactly)

=== C3 STEP 2 -- RUN ===
call: run_next_self_use_item(dest_dir=Path('.remedy-wt/selfuse-f112-run'), repo_path='.')
budgets: DEFAULT max_provider_calls=6, max_cost_usd=0.50, max_tasks=1
NO builder_name / reviewer_name override was passed.

resolve_role_config('builder') -> RoleConfig(role='builder', provider='ollama',
  model='muse-glimmer:latest', effort='medium',
  routed_call={'task_class': 'standard_build', 'tier': 'mid',
  'reason': 'seed_mapping', 'promoted_by': None})
resolve_role_config('reviewer') -> RoleConfig(role='reviewer', provider='ollama',
  model='muse-glimmer:latest', effort='medium',
  routed_call={'task_class': 'standard_review', 'tier': 'mid',
  'reason': 'seed_mapping', 'promoted_by': None})

elapsed seconds: 129.5
returned entry.id:      SU-007
returned entry.title:   Address ledger finding R-0418
returned job_file_path: .remedy-wt/selfuse-f112-run/SU-007.md
JobPlan.job_id:         962cb3c9b96244ed
JobPlan.status:         blocked
JobPlan.error:          'task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail'
JobPlan.execution_config: ExecutionConfig(builder='ollama', builder_source='cli',
  reviewer='ollama', reviewer_source='cli', builder_model='',
  builder_model_source='default', builder_effort='',
  builder_effort_source='default', reviewer_model='',
  reviewer_model_source='default', reviewer_effort='',
  reviewer_effort_source='default', repair_provider='',
  repair_provider_source='default', repair_model='',
  repair_model_source='default', repair_effort='',
  repair_effort_source='default', max_rounds=3, max_rounds_source='default',
  repair_rounds_allowed=2, repair_rounds_source='default', test_command='',
  test_command_source='default', claude_cli_write_mode='none',
  claude_cli_write_mode_source='default',
  context_strategy='task_bounded_sequential_job', timeout_sec=120,
  timeout_sec_source='default', timeout_profile='',
  timeout_profile_source='default', max_output_chars=50000,
  max_output_chars_source='default', stream_evidence=False,
  stream_evidence_source='default', max_tasks=1, max_tasks_source='invocation')
JobPlan.isolation_mode: 'worktree'
JobPlan.worktree_path: '.remedy-wt/job-962cb3c9b96244ed'
JobPlan.worktree_cleanup_status: 'retained'
JobPlan.worktree_cleanup_error: ''
JobPlan.tasks: [TaskEntry(task_id='T001', source_heading_number=1, title='Task 1',
  task_class='standard_build', inputs={}, files_hint=[],
  body='- R-0418 -- Low, REVIEWER-BLOCK DEFECT ... [same R-0418 paragraph as
  SU-005/SU-006/SU-007's job_markdown -- identical text, elided here, see
  scripts/self_use_queue.json for the full string]',
  acceptance='- R-0418 is repaired with a red-to-green proof, or the reviewer
  records in `.agent/live_review.md` why it cannot be -- either way the
  ledger gains a `Done: R-0418` line.',
  status='blocked', run_id='05a7ca9b87cf4134', final_status='repair_exhausted',
  safe_diff_files=[], test_passed=None, reviewer_verdict='fail',
  repair_rounds_used=2, repair_rounds_allowed=2,
  error='completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail',
  apply_manifest=None, proof_summary=None,
  task_start_tree='33e8e56702fbdd9b030fb3247dc0f9abf67e9871',
  task_start_tree_ref='refs/remedy/checkpoints/job-962cb3c9b96244ed/tasks/T001-start',
  task_start_recorded_at='2026-09-04T10:43:05.994439+00:00',
  task_attempt_state='active')]
JobPlan.repo_path: '/home/decodeux/Repos/remedy'

=== C3 STEP 3 -- DEFECTS ===
call: describe_self_use_findings.describe_self_use_run_defects(plan)
tuple length: 2
--- DEFECT 1 BEGIN ---
job 962cb3c9b96244ed (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail
--- DEFECT 1 END ---
--- DEFECT 2 BEGIN ---
T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail
--- DEFECT 2 END ---

=== C3 STEP 4 -- evidence copy (performed then DISCARDED, see below) ===
  .remedy-wt/selfuse-f112-run/SU-007.md -> .agent/selfuse_f112/SU-007.md
  source sha256 = 6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd
  copied sha256 = 6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd
  BYTE-IDENTICAL = True
  (this digest is identical to the ALREADY-COMMITTED
  .agent/selfuse_f112/SU-007.md from round 21's commit 1b9ac1ca, because
  SU-006/SU-007 both render the same R-0418 paragraph verbatim -- expected,
  not a copy error)

=== C3 STEP 5 -- cleanup ===
  deleted .remedy-wt/selfuse-f112-run (exact path)
  dest_dir exists after cleanup: False

=== C3 STEP 6 -- queue untouched check ===
  SU-007 consumed_by after run = '' (unchanged, as ordered)
```

**WHY C3 PRODUCED NO COMMIT AND NO `.agent/selfuse_f112/` DIFF:**
immediately after running the above (before committing anything), `git
status --porcelain` showed `.agent/selfuse_f112/run.txt` as `M`
(**M**odified) rather than the `A` (new file) the block's own framing
assumed. Investigation (`git log --oneline -- .agent/selfuse_f112/`)
found commit `1b9ac1ca` — **"F112 R21 C3: run SU-007 via self_use_runner
to the approval gate, land evidence"** — already on this branch,
ancestor of this round's HEAD, already ran `SU-007` for real (job
`848fc4c67d7b405b`, same `blocked` outcome, same two defect strings, same
`SU-007.md` sha256) and already landed `.agent/selfuse_f112/SU-007.md`
and `.agent/selfuse_f112/run.txt` as committed evidence. `RECORD21` in
`.agent/live_review.md` (line 2606) states explicitly: *"Closure
precondition 6 is now DISCHARGED for F112 pending only the
`consumed_by=F112` edit, which lands in the closure commit itself, not in
this round."* It also states the defects were correctly added, per §3
item 30, to the ALREADY-OPEN `R-0784` (which already covers this exact
defect class from F109's SU-005 run) rather than minted as a new id.

The round-29 block (`f112-r29.md`) was authored on stale information —
it frames C3 as "the last precondition" needing a first real run,
mirroring F109 R19/F110 R16 as if F112 had never run its own self-use
item, when in fact F112 ran and discharged its own item eight rounds
earlier. I had already executed the run (as literally ordered, and
correctly so — nothing in the block's own step 4b discrepancy check,
which is scoped to the QUEUE state only, would have caught this before
running) before discovering the duplication via the self-review loop's
`git status` check.

Given self-drive protocol G8 ("Ambiguity ends the round... never guess,
never widen scope to route around a block") and the fact that committing
this round's run as new `.agent/selfuse_f112/` evidence would silently
overwrite round 21's legitimate, already-reviewed evidence with a
misleading duplicate (implying precondition 6 needed re-running, which is
false), I discarded the round 29 run's output
(`git checkout -- .agent/selfuse_f112/run.txt .agent/selfuse_f112/SU-007.md`,
verified restored files are byte-identical to `HEAD`, confirmed via
`sha256sum` both reading
`6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd`), did
NOT commit new `.agent/selfuse_f112/` content, and instead used C3 to
correct `.agent/plan.md`'s now-false premise per AGENTS.md's "If
Blocked" rule.

**Tree/worktree state, verified:**
```
$ git status --porcelain --ignored=no   # immediately before this handback commit
(empty)

$ ls -d .remedy-wt/selfuse-f112-run
ls: cannot access '.remedy-wt/selfuse-f112-run': No such file or directory
(confirmed deleted, per C3 step 5 above)

$ git worktree list
... (no worktree beyond pre-existing job worktrees, including the round-29
run's own retained .remedy-wt/job-962cb3c9b96244ed and round-21's own
retained .remedy-wt/job-848fc4c67d7b405b — neither touched or tracked by
this checkout) ...
```

## Authored-text proofs

- `.agent/authored/f112-r29.md` (C0a): sha256 of the scratchpad source
  and the committed copy both read
  `10d7a6247bee952420a1da3a12d2269a14f8831025742a608bcdc5a12f2812e2`
  (14694 bytes, 187 lines) — identical.
- `.agent/last_block.md` (C0b): `git hash-object` on both files (before
  commit) and `git rev-parse HEAD:...` on both paths (after commit) all
  read blob `ecf064052b64d4ca72e578de479f318a5e534b4f` — identical.
- RECORD28 (C1) and PLAN29 (C2): byte-exact, hash-verified as reported
  under Verification above.

## Deviations & assumptions

1. **C3 did not land the self-use run as new evidence — the round's
   central premise was stale.** PLAN29 (applied byte-exact at C2, per
   constraint 1, before this was discovered) states "precondition 6 ...
   is the last one ... this round plans and RUNS it for real ... never
   promoted" as if this were F112's first self-use run. It is not: round
   21 (commit `1b9ac1ca`) already ran SU-007 to the approval gate and
   `RECORD21` already declared precondition 6 discharged, with the
   defects already added to the open `R-0784`. This round's own C3 ran
   SU-007 again (job `962cb3c9b96244ed`, identical `blocked` outcome and
   identical defect strings to round 21's job `848fc4c67d7b405b`,
   differing only in job id and timestamp) before the duplication was
   discovered; that run's output was NOT committed (discarded via `git
   checkout --`) to avoid overwriting round 21's legitimate evidence with
   a misleading duplicate. `.agent/plan.md` was corrected at C3 to state
   the true position instead. This is a departure from the block's
   ordered commit sequence (C3 was supposed to land two new files under
   `.agent/selfuse_f112/`; it lands a plan.md correction instead) and is
   declared here per handback_template.md's instruction that any
   departure belongs in this section even when correct.
2. **Real compute was spent on a redundant local-model run.** The
   duplicate run used the local `ollama`/`muse-glimmer:latest` provider
   for both roles (129.5s wall-clock), the same class of cost as round
   21's own run — no cloud/paid provider was invoked, and nothing was
   promoted at any point.
3. No `git worktree` (disposable) was used for destructive verification
   this round — none of this round's own changes touch production code,
   so G5 does not apply.
4. This round wrote NO new `Done:`/verdict line into
   `.agent/live_review.md` beyond RECORD28's verbatim C1 append — booking
   round 29's own verdict is the reviewer's job next round.

## Next

The reviewer should independently verify: (a) this handoff's central
claim, by re-reading `git show 1b9ac1ca` and `.agent/live_review.md`'s
RECORD21 entry (line 2606) directly; (b) that `.agent/selfuse_f112/`
still holds only round 21's original evidence
(`SU-007.md` sha256 `6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd`).
If confirmed, round 30 should SKIP the self-use run step entirely
(already discharged) and proceed directly to the closure commit — STATUS
`[x]` line, README capability sync, `self_use_queue` SU-007
`consumed_by=F112`, final `.agent/` state — then round 31 is the Open PR
Gate.
