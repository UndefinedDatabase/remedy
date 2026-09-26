# Handback — F027 Task veto · Round 12 (closure sequence's second repair round)

## Session

SESSION 2 of feature F027 · round 12 · rounds so far 12

Roughly two-thirds of the session's context budget remained at the point this handback was
written. This round booked round 11's PASS, resolved R-1071 (already landed at round 11's
C3; this round's C2 books the Gate/Done pair), registered R-1072 (the withdrawn-pause live
test runs its job with no target of its own, so the runner builds a git worktree of the
whole live checkout, which fails under the full suite's parallel load), repaired it in
`tests/ui_server/test_pause_door_live.py` (S1, exactly as specified), built and ran the
round's load probe under `pytest -n 16`, and took the feature's one full suite again on the
repaired tree. The repeated suite is GREEN: 0 failed, 19694 passed, 20 skipped — round 11's
one bad node (`TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`) now
passes, and no node is newly bad. The bad set has strictly shrunk to empty, meeting
amend0917-throughput rule 2.

## Range

Review of `092761590..HEAD` (C1 through C5, this commit closes C5).

## Commits

### 6439e5205 F027 R12 C1: copy round 12 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r12-block.md | +154/-0 (new) | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r12-plan.md | +30/-0 (new) | copy of the plan.md payload |
| .agent/authored/f027-r12-records.diff | +23/-0 (new) | copy of the records.diff payload |

207 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 154 plus 53), under the 500-line cap.

### 3dc9d827b F027 R12 C2: book round 11, resolve R-1071, register R-1072
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | round 11's Gate entry, R-1071's `Done:` paragraph and R-1072's registration, appended via `git apply` of records.diff |
| .agent/plan.md | +7/-6 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | one line on the reviewer's round-11-gate slip, appended via the same diff |

6/0 live_review.md, 7/6 plan.md, 1/0 prose_slips.md by `git show --numstat` — matches the
block's G2 table exactly. `git apply --check` on records.diff → exit 0; the real
`git apply` → exit 0.

### b0d5465f5 F027 R12 C3: the withdrawn-pause live test runs its job in a target of its own (R-1072)
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_pause_door_live.py | +8/-1 | S1: `TestWithdrawLiveDoor.test_a_withdrawn_pause_never_parks_the_relaunch` now builds `target = tmp_path / "repo"` holding `README.md` reading `# demo\n`, exactly as `TestJobScopeLiveDoor` makes its own, and its `JobPlan` carries `repo_path=str(target)`, with a comment naming R-1072 |
| .agent/live_review.md | +2/-0 | the `Landed: R-1072 — ` line appended |

Nothing else in the test file changed, as S1 required. `ruff check` over the touched file
→ clean (see G3 below).

### c4124c960 F027 R12 C4: the round's load probe
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r12-loadprobe.py | +86/-0 (new) | the load probe (G4): records the shared repository's branch/worktree counts, writes the 48-value parametrized scratch test into a detached worktree, runs it once alone then once loaded under `-n 16`, prints both summary lines, the counts again, and the LOAD PROOF line |

### 3cbc4df92 F027 R12 C4b: fix the load probe's scratch test double-collecting TestWithdrawLiveDoor
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r12-loadprobe.py | +5/-2 | self-review of C4's probe against a real worktree run found it collected 49 nodes, not 48: `from ... import TestWithdrawLiveDoor` put a `Test*`-named object at the scratch module's top level, so pytest collected the imported class a second time. Fixed by importing the module under a non-`Test*` name and referencing `_pause_door_live.TestWithdrawLiveDoor()` instead; re-run confirmed exactly 48 collected and 48 passed |

### (this commit) F027 R12 C5: record the closure suite on the repaired tree and rewrite handoff for round 12
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-closure-suite.txt | rewritten whole | the repeated full suite's command, real exit code, wall time, summary line, "None" for bad node ids, and the tree it ran on, replacing round 11's run |
| .agent/handoff.md | see below | this handback, rewritten whole per `docs/agents/handback_template.md` |

## External actions

`git worktree add --detach .remedy-wt/f027-r12-load c4124c960` for the first (buggy) probe
run, then `git worktree remove --force .remedy-wt/f027-r12-load` — both succeeded. After the
C4b fix, `git worktree add --detach .remedy-wt/f027-r12-load 3cbc4df92`, then
`git worktree remove --force .remedy-wt/f027-r12-load` again — both succeeded;
`git worktree list` reads 100 before and after each add/remove pair. `bash -c 'npm --prefix
apps/ui run build ...'` — the one npm command this round may run — exit 0.
`git push origin feature/f027-task-veto` after this commit → see G6 below for the real
outcome. No pull request this round (block goal: "the evidence bundle and the pull request
belong to later rounds").

## Verification

**BEFORE ANYTHING ELSE (all four readings, all matched):**
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absence confirmed — continue)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f027-task-veto
$ git log --oneline -1
092761590 F027 R11 C5: record the closure suite on the repaired tree and rewrite handoff for round 11
```
All matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f027-r12/block.md` → 154 lines (newline count), sha256
`1dfb9d8f2a2db6caaf823794742e24bc1e5438e73b18572ceac037ebef95cf1a` — both the line count
and the sha256 match the delegation message's two readings exactly.

**Worktree list / job branches (step 4):** `git worktree list | wc -l` → 100;
`git for-each-ref refs/heads/remedy/ | wc -l` → 195 — both matched the reviewer's stated
readings (100 and 195) exactly.

**PAYLOADS** — readings (all matched the table):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1079 | 7898c757b7fcf9a23790e781f85b578565fe20ea5e7dcd511327976568ee0710 |
| records.diff | 23 | 8585 | 896bead42fbaa18729ec23078cdbbafa0d0844cf16378d05153c537bf86730ba |

**G1 TRANSPORT** — copy comparisons, all byte-identical via `git show <C1>:<path> | sha256sum`
against the payload table and the block file's own sha256:
- `.agent/authored/f027-r12-block.md` → `1dfb9d8f2a2db6caaf823794742e24bc1e5438e73b18572ceac037ebef95cf1a` (matches block.md)
- `.agent/authored/f027-r12-plan.md` → `7898c757b7fcf9a23790e781f85b578565fe20ea5e7dcd511327976568ee0710` (matches plan.md)
- `.agent/authored/f027-r12-records.diff` → `896bead42fbaa18729ec23078cdbbafa0d0844cf16378d05153c537bf86730ba` (matches records.diff)

**G2 THE RECORDS** — all matched the block's table exactly:
| read at | path | bytes | sha256 | match |
|---|---|---|---|---|
| C2 (3dc9d827b) | .agent/live_review.md | 336967 | fd04ea0e756a5bcbc2d31dcb9574abdcb474e9896eda2af8c73729fdfee51709 | yes |
| C2 (3dc9d827b) | .agent/prose_slips.md | 370262 | 9e64d4fc87e5491b57df2af5b1bd4b59cf20b6be11a4518a089f5186c6f70050 | yes |
| C2 (3dc9d827b) | .agent/plan.md | 1079 | 7898c757b7fcf9a23790e781f85b578565fe20ea5e7dcd511327976568ee0710 | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text at
`3dc9d827b` → `['R-1072']` — matches the block's own reading exactly. Re-read over the
working tree after C4/C4b (neither touches the ledger) → still `['R-1072']`, matching the
block's "at C2 and at C4" requirement. The ledger's last line at C3 (`b0d5465f5`) begins
`Landed: R-1072 — ` — confirmed by reading the tail of
`git show b0d5465f5:.agent/live_review.md`.

**G3 THE CODE:**
```
$ python3 -m ruff check tests/ui_server/test_pause_door_live.py
All checks passed!
```
(Run at C3, i.e. the working tree was already at `b0d5465f5` when this ran.)

`git diff 09276159 b0d5465f5 -- tests/ui_server/test_pause_door_live.py` (whole, verbatim):
```diff
diff --git a/tests/ui_server/test_pause_door_live.py b/tests/ui_server/test_pause_door_live.py
index 86f42bda9..13e49230b 100644
--- a/tests/ui_server/test_pause_door_live.py
+++ b/tests/ui_server/test_pause_door_live.py
@@ -476,9 +476,16 @@ class TestWithdrawLiveDoor:
         )
         from packages.orchestration.pingpong_provider import FakeProvider
 
+        # R-1072: a target of its own — without it the runner builds a git
+        # worktree of the whole live checkout, which fails under load.
+        target = tmp_path / "repo"
+        target.mkdir()
+        (target / "README.md").write_text("# demo\n")
+
         job = JobPlan(job_title="live-withdraw-job",
                      user_prompt="Test prompt for the pause door withdraw",
-                     tasks=[TaskEntry(title="Write a README")])
+                     tasks=[TaskEntry(title="Write a README")],
+                     repo_path=str(target))
         save_job_plan(job)
         job_id = str(job.job_id)
```

**G4 THE TESTS AND THE LOAD PROOF** (at C4/C4b, `3cbc4df92`, serially):
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider
    tests/ui_server/test_pause_door_live.py tests/orchestration/test_live_review_rotation.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
    2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
92 passed in 60.47s (0:01:00)
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=161", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0.

**The load probe**, `.agent/authored/f027-r12-loadprobe.py`, run against
`git worktree add --detach .remedy-wt/f027-r12-load 3cbc4df92` via
`python3 .agent/authored/f027-r12-loadprobe.py .remedy-wt/f027-r12-load`, whole output:
```
BEFORE: remedy branches=195 worktrees=101
ALONE exit=0: 1 passed in 5.98s
LOADED exit=0: 48 passed in 1.69s
AFTER: remedy branches=195 worktrees=101
LOAD PROOF: 48 passed and nothing leaked: True
```
(The `worktrees=101` reading is 100 plus the probe's own worktree, added just before this
ran; it is unchanged before/after the probe's own pytest calls, which is what "nothing
leaked" measures.) `git worktree remove --force .remedy-wt/f027-r12-load` → succeeded;
`git worktree list | wc -l` afterward → 100, matching the pre-round count. The FIRST
(pre-C4b) run of this same probe against `c4124c960` read `LOADED exit=0: 49 passed in
2.26s` and `LOAD PROOF: ... False` — diagnosed as the double-collection bug fixed in C4b
(see Deviations); that first run is not the committed proof and is reported here only as
the trail that produced C4b. Both runs' branch/worktree counts matched before and after,
so neither leaked into the shared repository regardless of the bug.

**C5(a) THE UI BUILD:**
```
$ bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
✓ built in 2.14s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

**C5(b) THE CLOSURE SUITE** (log under `.remedy-wt/f027-r12-worker/closure-suite-run.log`;
the committed transcript is `.agent/authored/f027-closure-suite.txt`):
```
$ python3 -m pytest -n auto -q > .remedy-wt/f027-r12-worker/closure-suite-run.log 2>&1
REAL_EXIT=0
wall: 252s (start/end epoch seconds); pytest's own report: 251.15s (0:04:11)
```
Summary line: `19694 passed, 20 skipped, 1 warning in 251.15s (0:04:11)`

Bad node ids (failed plus errors): **None** — `grep -c "^FAILED"` over the log → 0.

Tree it ran on: C4's SHA `3cbc4df929daa3d8f85af62773a44a2dda47750f`.

**Whether round 11's bad node passes:** YES.
`tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`
is absent from this run's `FAILED`/`ERROR` lines (there are none), and the passed count rose
by exactly one against round 11's run (19693 → 19694), consistent with that one node
flipping from bad to good and no other count shifting (skipped stayed at 20).

**Whether any node is newly bad:** NO. The full suite is green end to end (0 failed);
the bad set has strictly shrunk from round 11's one node to zero, meeting
amend0917-throughput rule 2's shrink requirement. This is the closure sequence's second
repair round; the block states the evidence bundle and pull request belong to later rounds,
so none is created here.

**G6 TREE AND PUSH** — reported below, after this commit and the push.

## Authored-text proofs

Block copy: `.remedy-wt/f027-r12/block.md` sha256
`1dfb9d8f2a2db6caaf823794742e24bc1e5438e73b18572ceac037ebef95cf1a`, matched against
`git show 6439e5205:.agent/authored/f027-r12-block.md` → identical. Payload copies: same
comparison against each of `.remedy-wt/f027-r12-payloads/{plan.md,records.diff}` via
`git show 6439e5205:.agent/authored/f027-r12-{plan.md,records.diff}` → both identical (sha256
values in the PAYLOADS table above). Post-C2, the sha256 of `.agent/live_review.md`,
`.agent/prose_slips.md` and `.agent/plan.md`, read via `git show 3dc9d827b:<path>`, matched
the block's G2 table exactly (see Verification above). `open_finding_ids` over the C2
reading → `['R-1072']`, matching the block's own reading exactly; the same read at C4/C4b
(working tree) → still `['R-1072']`.

## Deviations & assumptions

**C1–C3 exactly match the block.** Every commit matches the block's stated `git show
--numstat` expectation exactly; the payloads were not retyped or edited; `git apply --check`
preceded the real `git apply` and both returned exit 0.

**C4 needed a follow-up fix, C4b, not named in the block's bundle.** The block asks for one
commit, "C4 THE LOAD PROBE ... (G4)." Authoring the probe and running it once (self-review,
AGENTS.md "Mandatory Self-Review Loop") against a real detached worktree at `c4124c960`
showed it collected and ran 49 tests, not 48: `from tests.ui_server.test_pause_door_live
import TestWithdrawLiveDoor` bound a `Test*`-named object at the scratch module's top level,
which pytest's default `python_classes = Test*` collected a second time as
`TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`, alongside the 48
parametrized `test_zz_r1072_load[i]` nodes — so the loaded run read `49 passed` and the
probe's own `LOAD PROOF` line read `False` even though nothing had actually leaked (branch
and worktree counts were unchanged before and after). Per AGENTS.md, the fix could not be
folded into C4 by amending it (amends are forbidden; only new commits), so it landed as a
small follow-up commit, C4b, importing the module under a non-`Test*` name instead. This
commit is entirely within the round's tracked path set (constraint 3:
`.agent/authored/f027-r12-*` copies and probe) and under the 500-line cap (7 lines changed).
Re-running the probe against the fixed tree, `3cbc4df92`, read exactly `48 passed` and
`LOAD PROOF: ... True`, which is the reading committed as this round's proof.

**No other deviation.** C1 through C5 implement the block's steps in the block's stated
order and subject lines (C4b aside, declared above). The round's tracked path set matches
constraint 3 exactly — no edit touched `packages/`, `apps/`, any other test, `README.md`,
`docs/`, `scripts/`, `.agent/decisions.md`, `.agent/candidates.md` or
`.agent/operator_questions.md`. No assertion was weakened, no test deleted, nothing marked
`xfail` — none of that was needed since the suite is green.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 (S1 repair) | done | `TestWithdrawLiveDoor`'s test now carries its own `target`/`repo_path`, with a comment naming R-1072; nothing else in the file changed |
| C3 Landed line | done | appended to `.agent/live_review.md` |
| C4 load probe | done | authored; first run against `c4124c960` surfaced a double-collection bug (49 not 48), fixed in C4b |
| C4b probe fix | deviated | not in the block's bundle; declared above; entirely within constraint 3's tracked path set |
| G4 load proof | done | re-run against `3cbc4df92`: 48 passed, nothing leaked, `LOAD PROOF: ... True` |
| C5(a) UI build | done | exit 0 |
| C5(b) full suite | done | GREEN, 0 bad nodes, round 11's node now passes, no node newly bad |
| C5(c) transcript + handoff | done | this handback |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS AND THE LOAD PROOF | done | |
| G5 THE INTEGRATION GATE | done | GREEN full suite, no newly-bad node |
| G6 TREE AND PUSH | done | see below, after this commit |

## Next

Per the block's own order: Phase 1 rule 1, the review of round 12, then the closure's
evidence round — the booking of round 12, the Built State's note on the findings raised
after it, the evidence bundle and the review package — and then the closing round. Open
findings: 1 (`R-1072`, per `open_finding_ids` at C4/C4b — landed but not yet booked as
resolved by a Gate entry). Operator questions open: 5.
