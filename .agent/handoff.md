# Handoff — F157 round 9 (C1 to C3 landed, suite green)

## Session

SESSION 3 of feature F157 · round 9 · rounds so far 9. This round booked round 8's verdict and
DECISION F157 D7 cleanly, ran the masking script once to record `SU-081`'s job diff past the
commit hook's agent-state guard, and ran the closure's one full suite, which came back green end
to end, so precondition 2 and precondition 6 of the closure protocol now both hold for F157.

Fortschritt: ~90 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung.

## Range

Review of `bfaac3257`..`b2c695c26`.

## Commits

### cb89f6182 F157 R9 C1: book round 8, DECISION F157 D7, the plan, the block and the masking script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r9.md` | +97/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/authored/f157-r9-mask-job-diff.py` | +55/-0 | NEW FILE — the reviewer-authored masking script (DECISION F157 D7) |
| `.agent/live_review.md` | +2/-0 | books round 8's PASS verdict, C3/C4 carried to round 9, the self-use run and the commit-hook refusal |
| `.agent/decisions.md` | +10/-0 | DECISION F157 D7 — the self-use record masks what the agent-state guard refuses |
| `.agent/prose_slips.md` | +2/-0 | two prose-slip lines (round 1 subagent race note; round 8 self-use/full-suite notes) |
| `.agent/plan.md` | +5/-23 | rewritten: Current Step → round 9's book/mask/suite sequence, Next Steps → evidence/package/closing |

### b9597df6b F157 R9 C2: the closure's self-use item run to its approval gate, never applied, its job diff masked
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | one appended entry, `SU-081`, `consumed_by` empty (round 8's generator run) |
| `.agent/selfuse_f157/SU-081.md` | +11/-0 | NEW FILE — the queue item's own markdown |
| `.agent/selfuse_f157/changed_paths.txt` | +1/-0 | NEW FILE — the job's one changed path |
| `.agent/selfuse_f157/entry_and_job_file.txt` | +5/-0 | NEW FILE — entry/job file identity |
| `.agent/selfuse_f157/execution_config.txt` | +43/-0 | NEW FILE — builder/reviewer provider, model, budgets |
| `.agent/selfuse_f157/full_transcript.txt` | +14/-0 | NEW FILE — the run's own transcript |
| `.agent/selfuse_f157/job_diff.txt` | +107/-0 | NEW FILE — the job's diff, MASKED by this round's script (DECISION F157 D7) |
| `.agent/selfuse_f157/result_state.txt` | +12/-0 | NEW FILE — job/task state and verdict |
| `.agent/selfuse_f157/run_defects.txt` | +1/-0 | NEW FILE — `NONE` |
| `.agent/selfuse_f157/staleness_after.txt` | +2/-0 | NEW FILE — staleness reading after the job |
| `.agent/selfuse_f157/timing.txt` | +3/-0 | NEW FILE — wall seconds |

### b2c695c26 F157 R9 C3: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-closure-suite.txt` | +27/-0 | NEW FILE — the one full suite's transcript and the cost script's reading |

### (this commit) F157 R9 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |

## External actions

`git push origin feature/f157-capability-matrix` — run once immediately after this commit; no pull
request opened or merged this round, per the block's constraint. No worktree created or removed.
No `gh pr create`/`merge` run.

## Verification

**Gate 1.** `git status --porcelain` (run after C3, before this commit) → empty output, exit 0.
Then `python3 .remedy-wt/f157-r9/prep/verify.py .` → every check line `True` except `absent	C4`
(expected — C4 had not been committed yet when the gate ran), last line `ALL True`. Full output:

```
True	cb89f6182 single parent equal to the commit before it
True	cb89f6182 carries a new F157 R9 Cn subject: F157 R9 C1: book round 8, DECISION F157 D7, the plan, the block and the masking script
True	cb89f6182 insertions 171 under 500
True	b9597df6b single parent equal to the commit before it
True	b9597df6b carries a new F157 R9 Cn subject: F157 R9 C2: the closure's self-use item run to its approval gate, never applied, its job diff masked
True	b9597df6b insertions 207 under 500
True	b2c695c26 single parent equal to the commit before it
True	b2c695c26 carries a new F157 R9 Cn subject: F157 R9 C3: the closure's one full suite and its CPU cost
True	b2c695c26 insertions 27 under 500
True	on feature/f157-capability-matrix
True	C1 paths exactly [...six paths...]
True	C1 .agent/authored/f157-r9-mask-job-diff.py equals c1-.agent__authored__f157-r9-mask-job-diff.py
True	C1 .agent/authored/f157-r9.md equals c1-.agent__authored__f157-r9.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths are the queue and .agent/selfuse_f157/: [...eleven paths...]
True	C2 appends exactly one queue entry: SU-081
True	C2 entry is SU-081, unconsumed
True	C2 job_diff.txt is the masked copy
True	C2 holds eleven paths: 11
True	C2 <each of ten .agent/selfuse_f157/ paths> holds no machine path   (×10)
True	C3 is the transcript alone: ['.agent/authored/f157-closure-suite.txt']
True	C3 transcript holds no machine path
absent	C4
True	the saved block equals block.md
ALL True
```

**Gate 2.** The ten files under `.agent/selfuse_f157/`, each non-empty, byte sizes:
`SU-081.md` 927, `changed_paths.txt` 36, `entry_and_job_file.txt` 299, `execution_config.txt` 1367,
`full_transcript.txt` 1580, `job_diff.txt` 3521, `result_state.txt` 865, `run_defects.txt` 5,
`staleness_after.txt` 200, `timing.txt` 105.

**Gate 3.** C3's suite: exit code 0. Summary line verbatim:
`23870 passed, 11 skipped, 1 warning in 366.16s (0:06:06)`. Bad node ids (failed + errors): `NONE`.
One informational line appeared in the log at the very end of the run, not a failure and not
counted by the guard that printed it: `R-1411: 3 entries of the configured data root ... changed
in the folders a supervisor this run did not start and its clients write; not counted: [...]` — a
background-session data-root note, not a test failure; exit code and summary line are unaffected.

**Gate 4.** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
{"message": "no reviewer scratch, evidence dir or archive at the root", "name":
"repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
"high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
"schema_version": 1, "version": 1}`.
Then `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']` — exactly the
eight ids the block names.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f157-r9-worker/c1_copy.py`) read `equal=True` disk-to-disk for all six
targets immediately after copying: `.agent/authored/f157-r9.md`,
`.agent/authored/f157-r9-mask-job-diff.py`, `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/plan.md`. `block.md` read `line_count=97`,
`sha256=3f19c37c087a2a8d576d8b9d612416797b2451867beae7d069bea76d0b4a4ec8`. `verify.py`'s gate-1 run
independently re-confirmed all six `C1 <path> equals c1-<path>` lines `True`, and
`the saved block equals block.md` `True`. No other reviewer-authored text was applied this round
(`.agent/authored/f157-r9-mask-job-diff.py` itself was never edited, only run, per the block).

## Self-use run

Entry `SU-081`, "Write the first tests for packages/common/public_text_redaction.py" (tier 5,
untested module). Job id `11b187c9221f49b1`. Builder `claude-cli`, model `claude-sonnet-4-6`,
effort `medium`; reviewer `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (from
`execution_config.txt`). Job state `completed`, no stop reason, no error, no run-manifest error.
Task `T001`: status `applied_to_job_workspace`, reviewer verdict `pass`, final status
`staged_review_passed`, 1 repair round used, run id `d8852927701f4d02`. Wall seconds (`timing.txt`)
`104.2`. Changed path (`changed_paths.txt`): `tests/test_public_text_redaction.py`.
`run_defects.txt`, verbatim: `NONE`.

Job diff (`.agent/selfuse_f157/job_diff.txt`, as committed, VERBATIM — masked per DECISION F157 D7):

```
MASKED COPY: 12 match(es) on 12 line(s) that the agent-state guard refuses are
replaced by a [MASKED: <rule>] marker (DECISION F157 D7). The job branch named in the diff's
first line keeps the diff whole. Unmasked sha256: 36a656d2d253203f02ff90aeaa480e2f76c7a34e17464e2a0b82bb1ce2428117

$ git diff HEAD...remedy/job-11b187c9221f49b1  (exit 0)
diff --git a/tests/test_public_text_redaction.py b/tests/test_public_text_redaction.py
new file mode 100644
index 000000000..16e093b58
--- /dev/null
+++ b/tests/test_public_text_redaction.py
@@ -0,0 +1,96 @@
+import pytest
+from packages.common.public_text_redaction import _scrub_public, _safe_path_label
+
+
+# --- _scrub_public ---
+
+def test_scrub_public_passthrough():
+    assert _scrub_public("hello world") == "hello world"
+
+
+def test_scrub_public_private_key():
+    text = "[MASKED: credential]\nMIIEow..."
+    assert "[redacted-secret]" in _scrub_public(text)
+    assert "PRIVATE KEY" not in _scrub_public(text)
+
+
+def test_scrub_public_aws_access_key():
+    text = "key is [MASKED: credential]"
+    result = _scrub_public(text)
+    assert "[redacted-secret]" in result
+    assert "[MASKED: credential]" not in result
+
+
+def test_scrub_public_openai_sk_token():
+    text = "Authorization: [MASKED: credential]"
+    result = _scrub_public(text)
+    assert "[redacted-secret]" in result
+    assert "[MASKED: credential]" not in result
+
+
+def test_scrub_public_bearer_token():
+    text = "Authorization: [MASKED: credential]"
+    result = _scrub_public(text)
+    assert "[redacted-secret]" in result
+
+
+def test_scrub_public_api_key_assignment():
+    text = "[MASKED: credential]"
+    result = _scrub_public(text)
+    assert "[redacted-secret]" in result
+    assert "supersecretvalue" not in result
+
+
+def test_scrub_public_abs_path_home():
+    text = "error in [MASKED: machine-local path]"
+    result = _scrub_public(text)
+    assert "[redacted-path]" in result
+    assert "[MASKED: machine-local path]" not in result
+
+
+def test_scrub_public_abs_path_users():
+    text = "file: [MASKED: machine-local path]"
+    result = _scrub_public(text)
+    assert "[redacted-path]" in result
+    assert "[MASKED: machine-local path]" not in result
+
+
+def test_scrub_public_traceback():
+    text = "Traceback (most recent call last):\n  File 'x.py', line 1"
+    result = _scrub_public(text)
+    assert "[redacted-trace]" in result
+    assert "Traceback (most recent call last)" not in result
+
+
+def test_scrub_public_unrelated_path_not_redacted():
+    # Only home-ish absolute paths are masked; a relative path is left alone.
+    text = "see tests/conftest.py for details"
+    assert _scrub_public(text) == text
+
+
+# --- _safe_path_label ---
+
+def test_safe_path_label_relative_unchanged():
+    assert _safe_path_label("src/foo/bar.py") == "src/foo/bar.py"
+
+
+def test_safe_path_label_absolute_returns_basename():
+    assert _safe_path_label("[MASKED: machine-local path]") == "main.py"
+
+
+def test_safe_path_label_backslash_normalised():
+    assert _safe_path_label("src\\foo\\bar.py") == "src/foo/bar.py"
+
+
+def test_safe_path_label_truncated_at_80():
+    long_path = "a" * 100
+    assert len(_safe_path_label(long_path)) == 80
+
+
+def test_safe_path_label_empty_string():
+    assert _safe_path_label("") == ""
+
+
+def test_safe_path_label_none_guard():
+    # The function guards against falsy input with `path or ""`; None must not raise.
+    assert _safe_path_label(None) == ""  # type: ignore[arg-type]
```

The masking script's own printed lines (run once, exit 0):
```
lines refused before 12, matches masked 12, refused after 0
unmasked sha256 36a656d2d253203f02ff90aeaa480e2f76c7a34e17464e2a0b82bb1ce2428117
masked sha256 faa60b779dc43b9422cbfaf1cee15c7fd6c2fff193652eb68d383a0379a4b86f
```

## Closure suite

`.agent/authored/f157-closure-suite.txt`, whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 367.1s (the launcher's reading); pytest's own reported wall time: 366.16s (0:06:06)
summary line: 23870 passed, 11 skipped, 1 warning in 366.16s (0:06:06)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: b9597df6b (F157 R9 C2: the closure's self-use item run to its approval gate, never applied, its job diff masked)
tree note: C1 and C2 changed only .agent/ files and the self-use queue; round 8 changed only .agent/ files and the checklist page
reflog before: b9597df6b HEAD@{2026-10-24 06:17:12 +0200}: commit: F157 R9 C2: the closure's self-use item run to its approval gate, never applied, its job diff masked
reflog after: b9597df6b HEAD@{2026-10-24 06:17:12 +0200}: commit: F157 R9 C2: the closure's self-use item run to its approval gate, never applied, its job diff masked
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F157 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1413.16 CPU seconds, 366.18 wall seconds, 23881 tests collected, exit status 0, recorded 2026-10-24T04:23:32Z
This closure's suite used 1413.16 CPU seconds, 1.8 percent more than F314's 1387.98, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F314's closure run:
  +8.11 s  tests/serve_http_handler/test_subtree_rerun_e2e_live.py (5.33 -> 13.44)
  +8.01 s  tests/runtimes/test_supervisor_portability.py (40.66 -> 48.67)
  +6.86 s  tests/orchestration/test_review_zip_hygiene.py (31.18 -> 38.04)
  +4.57 s  tests/cli/test_do_several_projects.py (7.81 -> 12.38)
  +3.39 s  tests/cli/test_do_sequence_cli.py (34.17 -> 37.56)
  +3.30 s  tests/contracts/test_capability_matrix.py (0.00 -> 3.30)
  +2.95 s  tests/orchestration/test_job_digest.py (5.12 -> 8.07)
  +2.87 s  tests/orchestration/test_job_evidence.py (10.84 -> 13.71)
  +2.61 s  tests/orchestration/test_event_name_coupling.py (14.31 -> 16.92)
  +2.38 s  tests/serve_http_handler/test_task_injection_e2e_live.py (2.84 -> 5.22)
```

## Deviations & assumptions

None from the ordered commit sequence: C1 to C3 landed exactly as the block orders, in order, each
gated by the preceding commands it names, and the four gates all read green on the first and only
run. Two minor observations, neither a deviation:

1. The masking script and the suite log each printed one informational, non-blocking line that is
   not part of what any commit or gate required: the masking script's own three report lines
   (recorded above, as the block's C4 orders) and the suite log's one `R-1411` data-root note
   (recorded in Verification, gate 3) — a background-session note the guard itself did not count
   against the run; exit code and summary line were unaffected.
2. `git log -1 --format=%h` on this checkout already returns a 9-character short hash by local
   config, so no `--short=9` override was needed to name C2's short SHA in the closure-suite
   transcript's `tree it ran on:` line; the value matches what `verify.py`'s own commands produce.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | masking script ran once, exit 0; commit hook refused nothing (already masked) |
| C3 | done | suite green, cost script exit 0 |
| C4 | done | this handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` `ALL True` (C4 `absent` at gate time, expected) |
| Gate 2 | done | all ten `.agent/selfuse_f157/` files non-empty, sizes recorded |
| Gate 3 | done | exit 0, summary line recorded, bad node ids `NONE` |
| Gate 4 | done | `fail_count: 0`; eight open finding ids match exactly |
| Push | pending | `git push origin feature/f157-capability-matrix` runs immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated; no pull request is
   open for this branch yet.
3. The reviewer reviews round 9, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. Then the evidence bundle and the review package (closure algorithm steps 1 and 2) — the suite is
   green, so this is the next step, not a repair round.
5. Then the closing round: the Built State, the ledger rotation, the STATUS line, the README and
   the pull request.
6. Operator questions open: 2.
7. Open findings count (gate 4): 8.

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of work on itself with a paid model — writing
the first tests for a small redaction helper — and that work finished and was approved. Then Remedy
ran its whole test collection once on the code that will ship, and all of it passed: 23,870 tests
passed, none failed, in a little over six minutes. The cost reading said this feature's test run
used a little more computer time than the previous feature's, well inside the normal range Remedy
allows before it treats the extra cost as a finding. A run now names, in its own report, every
place where the model it runs on could not do something natively and Remedy used a weaker fallback
instead.
