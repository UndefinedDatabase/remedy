# Handback — F306 round 10: book round 9 and R-1275, move the two stray review folders, re-run the one full suite clean

## Session

SESSION 3 of feature F306 · round 10 · rounds so far 10

Context self-assessment: this round's three commits and four gates all read as the block ordered,
with the one permission refusal on the move handled by the block's own named fallback, no
`.agent/STOP` and no open pull request encountered; context held comfortably throughout.

Fortschritt: ~95 % (T001 to T004 and T006 to T008 landed; R-1275 resolved; the suite run on a clean
root · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `788c2207b`..`90b4a3251`

## Commits

### 11e14289e F306 R10 C1: book round 9 and R-1275, record the move of the two review folders, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r10.md` | +109/-0 | NEW FILE, byte copy of `block.md` (109 lines, sha256 `6027ab6167d3a3488d1ee9652aa3fabebaf299adc74952c453372713f72c58b2`) |
| `.agent/decisions.md` | +12/-0 | DECISION F306 D3 appended, byte-identical to `decision-fallback.txt` (the fallback destination: the home-folder `mkdir` was refused by the session's own tool permission) |
| `.agent/live_review.md` | +4/-0 | round 9's PASS verdict (suite reading void) and R-1275's resolution appended, byte-identical to `append-live_review.txt` |
| `.agent/plan.md` | +3/-3 | replaced by `dry-plan.md` |

### 90b4a3251 F306 R10 C2: the closure's one full suite on a clean root and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-closure-suite.txt` | +20/-30 | whole content replaced (round 9's transcript stays in git history), the new clean-root run's transcript in round 9's shape plus the `tree note:` line the block orders |

### (this commit) F306 R10 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`: confirmed no open
  pull request for this branch, before and after this round's work.
- Move (no commit, git ignores both folders): the block's preferred destination, a `mkdir` of
  `/home/decodeux/remedy-review-moved`, was refused by the session's own tool permission with:
  `mkdir in '/home/decodeux/remedy-review-moved' needs approval. The path is outside the working
  directories for this session ('/home/decodeux/Repos/remedy'). Allowing runs the command as
  written.` Per the block's named fallback, `mkdir /home/decodeux/Repos/remedy/.remedy-wt/remedy-review-moved`
  then one `mv` of both folders into it ran without a second refusal. `ls -la
  /home/decodeux/Repos/remedy` afterward showed neither folder.
- `python3 /home/decodeux/Repos/remedy/.remedy-wt/f306-r8/prep/launch.py suite ...` then `wait.py
  suite ... 50`: one detached run, exit 0, wall 398.3s (launcher's reading) / 397.60s (pytest's own
  reading) — see "Closure suite" below.
- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8`
  — result in the session's final reply (with retry-on-500 up to three times per the block).
- No worktree added or removed by this session. No `gh pr merge`, `gh pr edit` or `gh pr create`.

## Verification

Preconditions confirmed before C1: `git rev-parse HEAD` read
`788c2207b12541fc272ad37a2b323d716e3e4294`, equal to
`git rev-parse origin/feature/f306-findings-paydown-v8`; `git status --porcelain` was empty;
`.agent/STOP` was absent; `git branch --show-current` read `feature/f306-findings-paydown-v8`.

Every prepared-file digest matched before use (all eight files named in the prompt, each read in
full first, each check printing an exact 64-character sha256 match via a Python reader):
`block.md` (109 lines, `6027ab6167d3a3488d1ee9652aa3fabebaf299adc74952c453372713f72c58b2`),
`append-live_review.txt`, `decision-home.txt`, `decision-fallback.txt`, `dry-plan.md`, `verify.py`,
`launch.py`, `wait.py`.

`git branch --show-current` read `feature/f306-findings-paydown-v8` immediately before each of
C1, C2 and C3's commits, as ordered.

M: the root held both folders before the move (confirmed by `ls -la`); the home-folder `mkdir` was
refused (verbatim quote above); the fallback `mkdir` and one `mv` of both folders (the second name
quoted, since it holds a space) into `.remedy-wt/remedy-review-moved` succeeded; `ls -la
/home/decodeux/Repos/remedy` afterward showed neither folder.

C1: a Python script under `.remedy-wt/f306-r10-worker/` wrote the four files, then printed `True`
for every one of the four byte-equality checks (`f306-r10.md` == `block.md`, `plan.md` ==
`dry-plan.md`, `live_review.md` == base + `append-live_review.txt`, `decisions.md` == base +
`decision-fallback.txt`), plus the copy's own line count (109) and sha256
(`6027ab6167d3a3488d1ee9652aa3fabebaf299adc74952c453372713f72c58b2`), matching the digest given in
the task. `git status --porcelain` before the commit showed exactly the four named paths (one new,
three modified) and nothing else.

C2 step 1: the root was confirmed clean again; reflog read
`11e14289e HEAD@{2026-10-14 00:12:53 +0200}: commit: F306 R10 C1: book round 9 and R-1275, record
the move of the two review folders, the plan, save the block`.
C2 step 2: `launch.py suite` started the detached run; `wait.py suite ... 50` returned after one
poll window with `exit 0 wall 398.3` — GREEN, no failed or error node. C2 step 3: the reflog was
read again the same way and read byte-identical to step 1's line — the branch did not move during
the run. C2 step 4:
`python3 scripts/closure_suite_cost.py --feature F306 --record /home/decodeux/.remedy-loop/test_load.jsonl`
→ printed output whose own branch text ("within the 14.1 percent limit") corresponds only to exit
code 0 in the script's `compare()` function (read from source rather than a second invocation, to
avoid running this idempotent, read-only reader twice; see Deviations). C2 step 5:
`.agent/authored/f306-closure-suite.txt` written in round 9's shape, with the empty bad-node-ids
list written as `  NONE` and the `tree note:` line the block orders added after `tree it ran on:`.
No leftover pytest process after the run (`pgrep -af pytest` found none).

Gate 1: `git status --porcelain` → empty. Then `verify.py` →
```
root holds neither folder True
found True F306 R10 C1: 11e14289e5aa9e90343cdb26921045e57cf54ce4
C1 parent is the base True
decisions equal to the base plus one variant True ['decision-fallback.txt']
both folders at the variant's destination True /home/decodeux/Repos/remedy/.remedy-wt/remedy-review-moved
equal at F306 R10 C1: True .agent/live_review.md
equal at F306 R10 C1: True .agent/plan.md
equal at F306 R10 C1: True .agent/authored/f306-r10.md
F306 R10 C1: names exactly its paths True []
ALL True
```

Gate 2: read from the committed transcript — exit code `0`; summary line `22976 passed, 22
skipped, 1 warning in 397.60s (0:06:37)`; bad node ids: none (the goal-3 target node is absent and
no other node is bad).

Gate 3: `python3 -m apps.cli.main integrity check --json` →
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
and
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1252']` (exit 0, matches expectation).

Gate 4: runs after the push; its command, exit code and comparison are in the session's final
reply, not in this file (the push had not yet happened when this file was written, per the
write-once rule).

## Authored-text proofs

- `.agent/authored/f306-r10.md` against `block.md`: byte-equal, 109 lines, sha256
  `6027ab6167d3a3488d1ee9652aa3fabebaf299adc74952c453372713f72c58b2` (Gate 1's `names exactly its
  paths True []` plus C1's own equality print).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (C1's equality print).
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (C1's
  equality print).
- `.agent/decisions.md` against the base plus `decision-fallback.txt`: byte-equal (C1's equality
  print and Gate 1's `decisions equal to the base plus one variant True ['decision-fallback.txt']`).

`.agent/authored/f306-closure-suite.txt` is this session's own transcript of real tool output, not
a prepared-file copy, so it carries no digest proof — its content is quoted verbatim below instead.

## Closure suite

`.agent/authored/f306-closure-suite.txt`, quoted whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 398.3s (the launcher's reading); pytest's own reported wall time: 397.60s (0:06:37)
summary line: 22976 passed, 22 skipped, 1 warning in 397.60s (0:06:37)
bad node ids (failed + errors):
  NONE
bad set before this run:
  - tests/orchestration/test_model_routing.py::TestTheCallSiteInventoryIsChecked::test_the_swept_multiset_equals_the_declared_inventory
the bad set shrank with no node newly bad: yes
leftover processes: NONE
tree it ran on: 0c68adcde (F306 R9 C2: the call-site inventory names the module the role-configuration call moved to (R-1275))
tree note: C1 changed only .agent/ files
reflog before: 11e14289e HEAD@{2026-10-14 00:12:53 +0200}: commit: F306 R10 C1: book round 9 and R-1275, record the move of the two review folders, the plan, save the block
reflog after: 11e14289e HEAD@{2026-10-14 00:12:53 +0200}: commit: F306 R10 C1: book round 9 and R-1275, record the move of the two review folders, the plan, save the block
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F306 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1321.14 CPU seconds, 397.62 wall seconds, 22998 tests collected, exit status 0, recorded 2026-10-13T22:19:48Z
This closure's suite used 1321.14 CPU seconds, 5.1 percent more than F203's 1257.35, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F203's closure run:
  +17.55 s  tests/test_grouped_cli.py (25.72 -> 43.27)
  +4.40 s  tests/orchestration/test_self_use_runner.py (4.02 -> 8.42)
  +3.91 s  tests/orchestration/test_serve_daemon.py (15.16 -> 19.07)
  +2.92 s  tests/orchestration/test_token_ledger.py (7.19 -> 10.11)
  +2.70 s  tests/orchestration/test_subtree_rerun_prepare.py (11.33 -> 14.03)
  +2.43 s  tests/orchestration/test_review_package_full_integration.py (3.74 -> 6.17)
  +2.41 s  tests/orchestration/test_job_worktree_integration.py (7.16 -> 9.57)
  +1.93 s  tests/cli/test_serve_client_parity.py (8.06 -> 9.99)
  +1.77 s  tests/orchestration/test_stream_export_e2e.py (3.26 -> 5.03)
  +1.66 s  tests/ui_server/test_pause_e2e_live.py (4.33 -> 5.99)
```

## Deviations & assumptions

1. **M used the fallback destination, as the block foresaw.** The preferred `mkdir
   /home/decodeux/remedy-review-moved` was refused by the session's own tool permission (verbatim
   quote in "External actions" above); per the block's own instruction ("do not try another way
   to write outside the checkout … instead `mkdir
   /home/decodeux/Repos/remedy/.remedy-wt/remedy-review-moved`"), that exact fallback ran instead,
   and `decisions.md` carries `decision-fallback.txt`, not `decision-home.txt`. Not a departure
   from the block — the block named this exact path and ordered it taken on refusal.

2. **The cost script's exit code was read from its own branch logic, not a second invocation.**
   `scripts/closure_suite_cost.py` is a pure reader of the test-load record already written by the
   suite's own `conftest.py`; it mutates nothing. Its `compare()` function returns exit code 0
   only on the branch that prints "within the … percent limit" and code 1 only on the branch that
   prints "that is above the … limit … registers a finding" — mutually exclusive by construction.
   This run's printed output read "within the 14.1 percent limit", so its exit code is 0 by that
   same construction; re-running it a second time just to read `$?` in the same shell call was
   judged unnecessary and skipped, since the block says "Run once" for this command and a shell
   tool call does not retain `$?` across turns.

No other deviation. C1 and C2 ran exactly as the block ordered.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Phase 1 rule 2: the Open PR Gate (no pull request is open for this branch yet).
3. The reviewer reviews round 10 and books its verdict in the next round's first commit.
4. The evidence bundle and the review package.
5. The closing round.

Operator questions open: 1.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## For the operator, in plain sentences

The two old review folders that had landed in the project's main folder were moved into a folder
set aside inside the project's own working area, because the folder first suggested for them could
not be written to from here; nothing inside either one was opened, changed or removed, and the
move can be undone by putting them back exactly where they were. With the main folder clean again,
the whole test collection was run once more from the start: this time every test that belongs to
this project passed and none failed, and the run took a little under seven minutes. The question
about where those two folders should live stays open until you answer it; the move already done is
only temporary and easy to reverse.

## Item status

| Item | Status | Reason |
|---|---|---|
| M | done | home destination refused; fallback destination used, as the block ordered |
| C1 | done | |
| C2 | done | suite green, bad set empty |
| C3 | done | this handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` `ALL True` |
| Gate 2 | done | suite exit 0; bad set empty |
| Gate 3 | done | `fail_count` 0; open set `['R-1235', 'R-1246', 'R-1252']` |
| Gate 4 | pending | runs after the push; reported in the session's final reply only |
