# F106 round 16 — integration gate attribution

## Comparison result

`branch_only.txt` (`comm -13 base_failed.txt branch_failed.txt`): **25 lines.**
`base_only.txt` (`comm -23 base_failed.txt branch_failed.txt`): **0 lines.**

`branch_failed.txt` holds 25 lines (the branch run's own FAILED list, sorted).
`base_failed.txt` holds 0 lines (the base run exited 0 with zero FAILED
lines). Every branch-only id is classified below. There is no base-only id
requiring the environment-parity attribution integration_gate.md step 3
would otherwise require.

## The base run required the R-0736 parity fix, applied proactively

The base worktree was created at `.remedy-wt/wt-r16-base` on throwaway
branch `tmp/base-gate-r16`, at merge-base
`811c2d7e96b4719b8c76e6fc59ec6d926847a026` (re-verified with
`git merge-base feature/f106-session-resume main` immediately before
creating the worktree — matched the block's stated value exactly). Per
R-0736 (Medium, OPEN) and its documented fix, the parity correction was
applied BEFORE the first base run attempt, not after rediscovering the
114-failure signature:

1. `apps/ui/node_modules` and `apps/ui/dist` were copied from the primary
   checkout into the worktree via `shutil.copytree(..., symlinks=True)`
   explicitly (a default `symlinks=False` would dereference npm's bin
   shims — finding R-0591).
2. Measured BEFORE any `os.utime` call: max mtime under the worktree's own
   `apps/ui/src/` = `1788337041.8690844`; the four copied `apps/ui/dist`
   files (carrying the PRIMARY checkout's original mtimes via the copy) =
   `1788057215.8536215` (`index.html`) / `1788057215.8556216` (the three
   `assets/` files) — src newer than dist on every file, which is exactly
   the staleness relation `_frontend_is_stale()`
   (`packages/orchestration/ui_server.py:3071`) reads to trigger a
   rebuild.
3. `os.utime` was applied to all four files under the worktree's copied
   `apps/ui/dist/`, advancing them to `1788337046.8690844` — 5.0 seconds
   strictly after the max `apps/ui/src/` reading, content untouched.
   Measured AFTER the `os.utime` call: all four dist mtimes now read
   `1788337046.8690844`; a re-read of `apps/ui/src/`'s own max mtime
   immediately after (`1788337041.8690844`) is unchanged from the BEFORE
   reading, confirming the call touched only `dist/`. sha256 of all four
   dist files was recorded before and after the `os.utime` call and is
   IDENTICAL in both readings (content-untouched proof; a content hash
   alone never stands alone per R-0444's own caution, but here it
   accompanies the mtime event reading rather than substituting for it):
   `index.html` `78d65c6e82a7…902aa`,
   `diffHighlightGrammars-o9XqnLhb.js` `7da6ba2c8a58…2192b5`,
   `index-D_qZGOuo.css` `f1ba4ab3f95b…37385a`,
   `index-Bh0mkYBD.js` `69d7e86a6e96…dceeaf` (full 64-char digests in
   `base_setup_output.txt`-equivalent console capture, reproduced above
   truncated for readability — the raw run's full output is not itself
   committed as a separate evidence file since `base_run.txt` and this
   prose carry every fact from it).
4. `REMEDY_UI_NO_AUTO_BUILD=1` was set via `os.environ[...] = '1'`
   in-process before invoking pytest (never a shell `VAR=x cmd` prefix,
   per this sandbox's own prior denial of that form).
5. As an ADDITIONAL instrument beyond what the block's own G6 gate
   requires (which asks only for the before/after-`os.utime` reading
   above): the four `apps/ui/dist` files' mtimes were also read
   immediately before and immediately after the actual base pytest
   invocation itself. Both readings are IDENTICAL —
   `1788337046.8690844` on all four files, both before and after the
   181.87s run — confirming `REMEDY_UI_NO_AUTO_BUILD=1` held for the
   whole run and nothing rebuilt mid-measurement (the general run-window
   instrument integration_gate.md step 2's own reasoning describes,
   applied here as corroboration, not as a substitute for the
   before/after-`os.utime` reading the block names).

Result: `grep -c "React UI not built" base_run.txt` = **0**. The base run,
launched with the subprocess's own `cwd` set to the worktree root and no
path argument to pytest (per this round's own instructions, avoiding the
wrong-installed-package artifact F040 R17 diagnosed), read: **exit 0,
18681 passed, 20 skipped, 0 failed, 181.87s (182.47s wall via the
wrapping driver's own timer).** The R-0736 fix worked on the first
attempt this round — no second attempt was needed.

## The 25 branch-only failures — one root cause, all classified feature-coupled-blocker

The branch run (primary checkout, HEAD `e167fb77` at the time of the run —
round 16's own C2 commit): `python3 -m pytest -n auto -q` read **exit 1,
25 failed, 18711 passed, 20 skipped, 129.66s (130.25s wall via the
wrapping driver's own timer)**.

All 25 FAILED lines were grepped into `branch_failed.txt`; `comm -13
base_failed.txt branch_failed.txt` reproduces the same 25 lines exactly
into `branch_only.txt` (base_failed.txt is empty, so branch_only.txt
equals branch_failed.txt here). `grep -c "unexpected keyword argument
'resume'" branch_run.txt` = **25** — every single failure, not merely
most of them, carries the identical error signature:

```
TypeError: <ClassName>.<method>() got an unexpected keyword argument 'resume'
```

raised from `packages/orchestration/pingpong_loop.py`'s own
`_call_with_retry(...)` invocation sites (builder call around line 3080,
reviewer call around line 3354 at this HEAD), which pass `resume=` to
`builder_provider.build(...)` / `reviewer_provider.review(...)`
unconditionally. This is F106's own code — `pingpong_loop.py` is
explicitly named in this round's own block as one of the files whose
coupling makes a branch-only failure a blocker.

**Attribution procedure (integration_gate.md step 4 / this round's block
constraint 4.d), applied to all 25 ids as one serial batch** (a single
`pytest <id1> <id2> ... -q` invocation naming all 25 node ids explicitly,
still fully serial — no `-n auto` anywhere in the command — which
satisfies "serial re-run of the exact node id" for every id at once
rather than one invocation per id):

- **Serial re-run at branch tip** (primary checkout, same 25 ids, no
  `-n auto`): `25 failed in 3.29s` — every id fails again, identically.
  This rules out the xdist-flake class (F135/F052): xdist-flake requires
  a serial PASS, and none of the 25 passed serially.
- **Reproduction at the base** (same 25 ids, same base worktree, serial,
  `REMEDY_UI_NO_AUTO_BUILD=1` still set): `25 passed in 2.98s` — none of
  the 25 reproduces at the base. This is exactly what code inspection
  predicts: `git merge-base --is-ancestor 811c2d7e…
  e151105e8d1dc2d3244865f23fc442b8d20890a1` confirms the merge-base is an
  ancestor of `e151105e` (F106 T002a, "Builder call resumes prior session
  when earned," round 5) — the commit that first introduced
  `resume=builder_resume_ref` into `pingpong_loop.py`. The merge-base
  cannot contain code that does not exist yet on any ancestor path, so a
  TypeError naming a keyword argument that commit introduces is
  structurally impossible at the base; the empirical serial base run
  confirms this directly rather than resting on the inference alone.

Per constraint 4.d's own text: "a reproducible branch-only failure that
does NOT reproduce at the base and is coupled to F106's own code
(`packages/orchestration/pingpong_loop.py` … or their tests) is a
BLOCKER." All 25 ids meet every clause: reproducible (serial-fail, twice
now — once inside the full `-n auto` run, once in the dedicated serial
batch), does not reproduce at base (serial base run, 25/25 passed),
coupled to F106's own `pingpong_loop.py` (the traceback's own top frame
in every one of the 25). **Classification: feature-coupled-blocker, all
25 ids, no exceptions.**

## This is the same defect CLASS as CLOSED R-0758/R-0759, in three NEW files

Per checklist item 30 (retire/avoid a duplicate id — grep the DEFECT
before minting one): `packages/orchestration/pingpong_loop.py`'s
`resume=` passthrough has broken test doubles TWICE before, and both
times the fix was the same additive no-op parameter:

- R-0758 (Medium, CLOSED round 10) — four fake providers in
  `tests/orchestration/test_provider_retry.py`.
- R-0759 (Medium, CLOSED round 12) — four fake reviewers in
  `tests/orchestration/test_repair_loop.py`.

Neither id's own text names any of the three files this round's full-suite
run newly exposes (`test_structured_outputs.py`,
`test_worktree_isolation.py`, `test_worktree_persistence.py`), and both
are already `Done:` — resolved, not reopened. This is NOT a duplicate:
following the exact precedent R-0759 itself set when it was minted as a
NEW id alongside the already-open R-0758 ("the same defect CLASS as
R-0758 …, discovered now in a DIFFERENT file"), this round registers a
NEW id, **R-0760** (Medium), in its own commit (`02c404c2`), BEFORE this
evidence commit, per `docs/agents/planner_reviewer_prompt.md` §4 item 4's
"findings persist FIRST" rule. `.agent/live_review.md`'s registered-id
count moved from 320 (this round's own C2 base) to 321 (after R-0760);
`Done:` and `DECISION` counts are unchanged at 59 and 20. R-0760's own
text names the exact five signatures needing the fix
(`tests/orchestration/test_structured_outputs.py:342` and `:389`,
`tests/orchestration/test_worktree_isolation.py:53`, `:62` and `:166`,
`tests/orchestration/test_worktree_persistence.py:61` and `:68`) and the
same additive `resume: str | None = None` fix shape R-0758/R-0759 already
used.

## Why this was never caught before this round

None of F106's own per-round gates (the recurring three/four-file subset
each round's block has named) ever included
`test_structured_outputs.py`, `test_worktree_isolation.py`, or
`test_worktree_persistence.py`. This round's own Goal line states
plainly that F106 has never had a dedicated integration gate before now —
this is the first time the FULL suite has run for this feature, and it is
precisely a full-suite run that surfaces a break in files no round-scoped
gate ever touched. R-0758 and R-0759 were discovered the same way, by an
incidentally-broader-than-usual suite run in their own rounds; R-0760 is
the same mechanism operating at full scale for the first time.

## Conclusion

**This round's gate is RED.** Per constraint 4.d and this round's own G7
gate ("zero feature-coupled blockers survive into this round's own
verdict — if one exists, this gate is RED and the round's own conclusion
says so"): 25 of 25 branch-only failures are classified
feature-coupled-blocker, none is an xdist-flake, none is a base-only
environment artifact. `docs/roadmap/STATUS_closure_protocol.md`
precondition 2 (a PASSING dedicated integration-gate round) is **NOT
MET** by this round. Per this round's own top-level instructions, no
attempt was made to fix `packages/orchestration/pingpong_loop.py` or the
five affected test-double signatures in this round — the change set is
measurement-only by the block's own declared Change: line, and the fix
belongs to the next round as a dedicated repair round, not to this one.
