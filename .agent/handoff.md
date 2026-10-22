# Handback — F307 round 29: book round 28, the consolidation pass, the self-use item, the one full suite

## Session

SESSION 7 of feature F307 · round 29 · rounds so far 29

Context self-assessment: this worker verified every prepared digest before any write, copied each prepared file by a script that proved equality over bytes, ran the self-use run and the suite once each through the launcher, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~98 % (T001 to T021 landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `50850011f`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 07aba1fe4 F307 R29 C1: book round 28, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r29.md` | 152/0 | NEW FILE, this round's block, byte copy (152 lines, sha256 `bef1388b494ab67274a36f1f59c8c630f96496a78d6d51e226b3f026a9cc10b5`) |
| `.agent/authored/f307-r29-selfuse.py` | new | NEW FILE, the reviewer's self-use script, byte copy |
| `.agent/live_review.md` | 2/0 | prepared file copied (round 28's verdict booked) |
| `.agent/plan.md` | 14 lines changed | prepared file copied |

289 insertions, 6 deletions over 4 files (`git show --shortstat`).

### 828f9c35e F307 R29 C2: the checklist's consolidation pass for F307
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 14/0 | prepared file copied (`git show --numstat` reads `14	0`) |

14 insertions (`git show --shortstat`).

### c0cbaf535 F307 R29 C3: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, SU-073, `consumed_by` empty |
| `.agent/selfuse_f307/` | 10 new files | the run's ten record files |

327 insertions over 11 files (`git show --shortstat`).

### d3648405e F307 R29 C4: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-closure-suite.txt` | 29/0 | NEW FILE, the suite transcript and cost reading (the suite is RED, committed as read) |

29 insertions (`git show --shortstat`).

### (this commit) F307 R29 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | commit `07aba1fe4`, four byte proofs held |
| C2 | done | commit `828f9c35e`, numstat `14	0` |
| C3 | done | commit `c0cbaf535`, self-use run exit 0, one queue entry appended |
| C4 | done | commit `d3648405e`, suite RED (2 failed), transcript committed as read, not re-run |
| C5 | done | this handback commit |
| Gate 1 | done | status empty; verify.py `ALL True` |
| Gate 2 | done | all ten files non-empty |
| Gate 3 | done | exit 1, `2 failed, 23181 passed, 11 skipped`, two bad node ids |
| Gate 4 | done | `fail_count` 0; open set of 6 ids as ordered |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

The self-use run made real provider calls through the `self_use` role (2 calls, see below). It added and removed a temporary worktree at `.remedy-wt/f307-r29-jobtree` itself. No `gh` command, no pull request, no fetch or pull. `git push origin feature/f307-findings-paydown-v9` follows this commit and is reported in the session reply. `.remedy-wt/f307-r29-worker/` holds the digest checker, the copy script, the commit messages, the launcher logs and this handoff's generator.

## Verification

1. Digests before any write: `block.md`, `verify.py` and `digests.txt` equal the prompt's; every file `digests.txt` lists matched (checker run with `python3 -I`); `bad 0`.
2. Preconditions: HEAD `50850011f` equal to `origin/feature/f307-findings-paydown-v9`, `git status --porcelain` empty, `.agent/STOP` absent. `git branch --show-current` read `feature/f307-findings-paydown-v9` before each of C1 to C4.
3. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f307-r29/prep/verify.py .` printed `True` on every line, `absent` for C5, last line `ALL True`.
4. Gate 2: byte sizes under `.agent/selfuse_f307/`: `SU-073.md` 1810, `changed_paths.txt` 152, `entry_and_job_file.txt` 225, `execution_config.txt` 1367, `full_transcript.txt` 1543, `job_diff.txt` 13980, `result_state.txt` 866, `run_defects.txt` 5, `staleness_after.txt` 367, `timing.txt` 105; all non-empty.
5. Gate 3: the suite of C4, exit 1; `2 failed, 23181 passed, 11 skipped, 1 warning in 449.10s (0:07:29)`; bad node ids `tests/orchestration/test_record_client_answers.py::test_the_folder_holds_one_answer_per_case_and_matches_a_fresh_recording` and `tests/orchestration/test_record_client_answers.py::test_the_check_names_every_changed_answer_and_exits_1`. The first fails with `client-story-working.dirty_start: new` / `client answers: 1 difference(s)`; the second sees `3 difference(s)` where it expects 2, the extra one the same `client-story-working.dirty_start: new`. Not investigated, per the block.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0, `fail_count` 0; `handler_import` pass (`handlers=194`), `live_review_verdict` pass, `plan_consistency` pass, `relevant_untracked` pass, `repo_root_hygiene` pass, `high_blockers_open` pass. `open_finding_ids` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418']`.

## Authored-text proofs

Applied this round, each proved equal over bytes by `copy_c.py` right after writing and again by `verify.py` against the committed blobs: `.agent/authored/f307-r29.md`, `.agent/authored/f307-r29-selfuse.py`, `.agent/live_review.md`, `.agent/plan.md` (C1) and `docs/agents/planner_reviewer_prompt.md` (C2). `block.md` read 152 lines, sha256 `bef1388b494ab67274a36f1f59c8c630f96496a78d6d51e226b3f026a9cc10b5`, equal to the prompt's.

## Self-use run

- Entry: `SU-073`, "Address ledger finding R-1418", provenance `generated (self-use-generator tier 1, ledger scan, R-1418)`.
- Job id: `09fe11ff74a542bd`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`; reviewer: `claude-cli`, model `claude-sonnet-4-6` (from `execution_config.txt`).
- Job state: `completed`; stop reason: empty.
- Tasks: `T001` `applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`, 0 repair rounds.
- Wall seconds (`timing.txt`): 514.6.
- Changed paths (`changed_paths.txt`):
- `docs/guides/environment.md`
- `packages/orchestration/config.py`
- `packages/orchestration/self_use_generator.py`
- `tests/orchestration/test_self_use_generator.py`

Job diff (`job_diff.txt`) verbatim:

```
$ git diff HEAD...remedy/job-09fe11ff74a542bd  (exit 0)
diff --git a/docs/guides/environment.md b/docs/guides/environment.md
index 2e1bc3e29..132bb0be2 100644
--- a/docs/guides/environment.md
+++ b/docs/guides/environment.md
@@ -119,6 +119,7 @@ not read as its type; neither warning stops Remedy from running.
 | `REMEDY_RUN_REAL_OLLAMA` | yes or no (1, true, yes / 0, false, no) | no | env-only | Run scripts/remedy_test_real_providers.sh against a real Ollama server instead of skipping (env-only flag) |
 | `REMEDY_SCOPE_ALLOW` | a comma-separated list | none | `scope.allow` | Glob patterns for allowed write paths (F017 scope fences) |
 | `REMEDY_SCOPE_DENY` | a comma-separated list | none | `scope.deny` | Glob patterns for denied write paths (F017 scope fences) |
+| `REMEDY_SELF_USE_BUILDER_HAS_NETWORK` | yes or no (1, true, yes / 0, false, no) | no | `self_use.builder_has_network` | Whether the self-use builder can reach the network (R-1418). Unset or false, the order tier skips the toolchain refresh order because its tasks read from the package index and from GitHub URLs and a builder without network access can only block. Set it to true when the configured provider's harness provides WebFetch or equivalent network tools — for example, a claude-cli builder started with claude_cli.all_tools enabled. |
 | `REMEDY_SELF_USE_MODEL` | text | none | `self_use.model` | Model for both roles of a self-use run (operator amendment amend0920-selfuse-real, DECISION D2). Unset means the alias table's Sonnet alias, which the run's cost bound of at most 8 provider calls and 6.00 USD per closure is written for. |
 | `REMEDY_SELF_USE_PROVIDER` | text | none | `self_use.provider` | Provider for BOTH the builder and the reviewer of a self-use run (operator amendment amend0920-selfuse-real, DECISION D2). Unset means `claude-cli`: a self-use run repairs THIS repository, which is frontier work, and five consecutive runs on the local model (SU-019 to SU-023) landed nothing. Set it to `ollama` to put the track back on the local model. |
 | `REMEDY_SERVE_API_PORT` | a whole number | none | `serve.api_port` | When set, the `remedy serve start` supervisor also answers the public HTTP API (F253) on 127.0.0.1 at this port, and nothing else there; 0 picks a free port |
diff --git a/packages/orchestration/config.py b/packages/orchestration/config.py
index f675cfcd1..205f8027d 100644
--- a/packages/orchestration/config.py
+++ b/packages/orchestration/config.py
@@ -672,6 +672,21 @@ _CONFIG_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
         value_type=str,
         default=None,
     ),
+    ConfigKeySpec(
+        key="self_use.builder_has_network",
+        env_var="REMEDY_SELF_USE_BUILDER_HAS_NETWORK",
+        description=(
+            "Whether the self-use builder can reach the network (R-1418). "
+            "Unset or false, the order tier skips the toolchain refresh order "
+            "because its tasks read from the package index and from GitHub URLs "
+            "and a builder without network access can only block. Set it to "
+            "true when the configured provider's harness provides WebFetch or "
+            "equivalent network tools — for example, a claude-cli builder "
+            "started with claude_cli.all_tools enabled."
+        ),
+        value_type=bool,
+        default=False,
+    ),
     ConfigKeySpec(
         key="planner.provider",
         env_var="REMEDY_PLANNER_PROVIDER",
diff --git a/packages/orchestration/self_use_generator.py b/packages/orchestration/self_use_generator.py
index 0b104e971..af1461cd5 100644
--- a/packages/orchestration/self_use_generator.py
+++ b/packages/orchestration/self_use_generator.py
@@ -67,9 +67,9 @@ Public API::
     SelfUseGenerationError: a source this module needs could not be read
     default_ledger_path() -> Path
     default_source_root() -> Path
-    generate_self_use_item(queue_path=None, ledger_path=None, *, source_root=None) -> SelfUseQueueEntry | None
+    generate_self_use_item(queue_path=None, ledger_path=None, *, source_root=None, builder_has_network=None) -> SelfUseQueueEntry | None
     append_generated_item(entry, queue_path=None) -> None
-    generate_and_append_if_empty(queue_path=None, ledger_path=None, *, source_root=None) -> SelfUseQueueEntry | None
+    generate_and_append_if_empty(queue_path=None, ledger_path=None, *, source_root=None, builder_has_network=None) -> SelfUseQueueEntry | None
 
 Deliberate absences:
   * REMEDY DELIBERATELY DOES NOT SUMMARIZE A FINDING. The rendered job's Task 1
@@ -196,6 +196,13 @@ _ORDER_PROVENANCE_RE = re.compile(
     r"^generated \(self-use-generator order tier, (?P<path>[^,]+), (?P<day>\d{4}-\d{2}-\d{2})\)$"
 )
 
+#: THE TOOLCHAIN REFRESH ORDER REQUIRES NETWORK ACCESS (R-1418). Its tasks read from the package
+#: index and from GitHub's hosted-runner manifest URL. The order tier skips it unless
+#: ``self_use.builder_has_network`` is true: the default is ``False`` because the Pi harness
+#: runs builders in a private network namespace where those fetches cannot succeed, and spending
+#: a budget on a job that must block is worse than not queueing it.
+ORDER_REQUIRES_NETWORK = True
+
 #: Severities this generator's Tier 1 will pick from — never High or Critical,
 #: which are judgement calls a generator does not make for itself.
 _ELIGIBLE_SEVERITIES = ("Low", "Medium")
@@ -294,8 +301,28 @@ def _last_order_day(queue_path: Path | None) -> date | None:
     return max(days) if days else None
 
 
-def _order_tier(queue_path: Path | None, order_path: Path, today: date) -> SelfUseQueueEntry | None:
-    """Tier 0: the toolchain refresh order, verbatim, when fourteen days have passed."""
+def _builder_has_network() -> bool:
+    """Read ``self_use.builder_has_network`` from the process config (R-1418)."""
+    from packages.orchestration.config import get_config
+    return bool(get_config().get("self_use.builder_has_network"))
+
+
+def _order_tier(
+    queue_path: Path | None,
+    order_path: Path,
+    today: date,
+    builder_has_network: bool | None = None,
+) -> SelfUseQueueEntry | None:
+    """Tier 0: the toolchain refresh order, verbatim, when fourteen days have passed.
+
+    Skipped when the builder cannot reach the network (R-1418): the order's tasks read from the
+    package index and GitHub URLs, so a network-less builder can only block. ``builder_has_network``
+    defaults to the ``self_use.builder_has_network`` config key (default ``False``).
+    """
+    if ORDER_REQUIRES_NETWORK:
+        capable = builder_has_network if builder_has_network is not None else _builder_has_network()
+        if not capable:
+            return None
     if not order_path.is_file():
         return None
     last = _last_order_day(queue_path)
@@ -880,6 +907,7 @@ def generate_self_use_item(
     order_path: Path | None = None,
     today: date | None = None,
     source_root: Path | None = None,
+    builder_has_network: bool | None = None,
 ) -> SelfUseQueueEntry | None:
     """The next item to append, from the first tier that has one, or ``None``.
 
@@ -887,10 +915,17 @@ def generate_self_use_item(
     :func:`append_generated_item` for the write and
     :func:`generate_and_append_if_empty` for the seam that combines both
     behind the "only when the queue is empty" rule.
+
+    ``builder_has_network`` controls whether the order tier may queue the toolchain
+    refresh order (R-1418). ``None`` reads the ``self_use.builder_has_network`` config
+    key (default ``False``).
     """
     ledger = ledger_path or default_ledger_path()
 
-    order_result = _order_tier(queue_path, order_path or default_order_path(), today or date.today())
+    order_result = _order_tier(
+        queue_path, order_path or default_order_path(), today or date.today(),
+        builder_has_network=builder_has_network,
+    )
     if order_result is not None:
         return order_result
 
@@ -947,6 +982,7 @@ def generate_and_append_if_empty(
     order_path: Path | None = None,
     today: date | None = None,
     source_root: Path | None = None,
+    builder_has_network: bool | None = None,
 ) -> SelfUseQueueEntry | None:
     """The seam a closure round calls: generate and append, but ONLY when empty.
 
@@ -959,6 +995,7 @@ def generate_and_append_if_empty(
         return None
     entry = generate_self_use_item(
         queue_path, ledger_path, order_path=order_path, today=today, source_root=source_root,
+        builder_has_network=builder_has_network,
     )
     if entry is None:
         return None
diff --git a/tests/orchestration/test_self_use_generator.py b/tests/orchestration/test_self_use_generator.py
index e288572a7..63f671cc3 100644
--- a/tests/orchestration/test_self_use_generator.py
+++ b/tests/orchestration/test_self_use_generator.py
@@ -588,7 +588,7 @@ class TestOrderTier:
         real = Path(__file__).resolve().parents[2] / ORDER_RELATIVE_PATH
         queue_path = _write_queue(tmp_path, [])
         entry = generate_self_use_item(queue_path=queue_path, ledger_path=tmp_path / "none.md",
-                                       order_path=real, today=self.DAY)
+                                       order_path=real, today=self.DAY, builder_has_network=True)
         assert entry is not None and entry.job_markdown == real.read_text(encoding="utf-8")
         assert entry.title == "Refresh the pinned toolchain"
 
@@ -597,7 +597,7 @@ class TestOrderTier:
         ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
         order = self._order(tmp_path)
         entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger, order_path=order,
-                                       today=self.DAY)
+                                       today=self.DAY, builder_has_network=True)
         assert entry.job_markdown == order.read_text(encoding="utf-8")
         assert entry.why == "Why it runs."
         assert entry.provenance == ("generated (self-use-generator order tier, "
@@ -607,21 +607,24 @@ class TestOrderTier:
         queue_path = _write_queue(tmp_path, [self._order_item("2026-09-10")])
         ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
         entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
-                                       order_path=self._order(tmp_path), today=self.DAY)
+                                       order_path=self._order(tmp_path), today=self.DAY,
+                                       builder_has_network=True)
         assert entry.provenance.startswith("generated (self-use-generator tier 1")
 
     def test_after_fourteen_days_the_order_is_due_again(self, tmp_path):
         queue_path = _write_queue(tmp_path, [self._order_item("2026-09-09")])
         ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
         entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
-                                       order_path=self._order(tmp_path), today=self.DAY)
+                                       order_path=self._order(tmp_path), today=self.DAY,
+                                       builder_has_network=True)
         assert entry.id == "SU-002" and "order tier" in entry.provenance
 
     def test_an_absent_order_file_leaves_the_ledger_tier_in_charge(self, tmp_path):
         queue_path = _write_queue(tmp_path, [])
         ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
         entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
-                                       order_path=tmp_path / "absent.md", today=self.DAY)
+                                       order_path=tmp_path / "absent.md", today=self.DAY,
+                                       builder_has_network=True)
         assert entry.provenance.startswith("generated (self-use-generator tier 1")
 
     def test_an_order_file_that_is_not_a_job_is_refused(self, tmp_path):
@@ -629,7 +632,29 @@ class TestOrderTier:
         order.write_text("Just prose, no job title.\n", encoding="utf-8")
         with pytest.raises(SelfUseGenerationError, match="not a job file"):
             generate_self_use_item(queue_path=_write_queue(tmp_path, []), ledger_path=tmp_path / "none.md",
-                                   order_path=order, today=self.DAY)
+                                   order_path=order, today=self.DAY, builder_has_network=True)
+
+    def test_order_is_skipped_when_builder_has_no_network(self, tmp_path):
+        """R-1418: the order requires network; a network-less builder gets the ledger tier instead."""
+        queue_path = _write_queue(tmp_path, [])
+        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
+        order = self._order(tmp_path)
+        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger, order_path=order,
+                                       today=self.DAY, builder_has_network=False)
+        assert entry is not None
+        assert entry.provenance.startswith("generated (self-use-generator tier 1")
+
+    def test_order_is_skipped_by_default_without_network_config(self, tmp_path, monkeypatch):
+        """R-1418: builder_has_network=None reads the config key, which defaults to False."""
+        from packages.orchestration import self_use_generator
+        monkeypatch.setattr(self_use_generator, "_builder_has_network", lambda: False)
+        queue_path = _write_queue(tmp_path, [])
+        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
+        order = self._order(tmp_path)
+        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger, order_path=order,
+                                       today=self.DAY)
+        assert entry is not None
+        assert entry.provenance.startswith("generated (self-use-generator tier 1")
 
 
 class TestTheAcceptanceAsksForTheRepairAlone:
```

`run_defects.txt` verbatim:

```
NONE
```

## Closure suite

Quoting `.agent/authored/f307-closure-suite.txt` whole:

```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 450.0s (the launcher's reading); pytest's own reported wall time: 449.10s (0:07:29)
summary line: 2 failed, 23181 passed, 11 skipped, 1 warning in 449.10s (0:07:29)
bad node ids (failed + errors):
  - tests/orchestration/test_record_client_answers.py::test_the_folder_holds_one_answer_per_case_and_matches_a_fresh_recording
  - tests/orchestration/test_record_client_answers.py::test_the_check_names_every_changed_answer_and_exits_1
leftover processes: NONE
tree it ran on: c0cbaf535 (F307 R29 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C3 changed only .agent/ files, the checklist page and the self-use queue
reflog before: c0cbaf535 HEAD@{2026-10-22 05:17:12 +0200}: commit: F307 R29 C3: the closure's self-use item run to its approval gate, never applied
reflog after: c0cbaf535 HEAD@{2026-10-22 05:17:12 +0200}: commit: F307 R29 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F307 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1400.13 CPU seconds, 449.11 wall seconds, 23194 tests collected, exit status 1, recorded 2026-10-22T03:24:44Z
This closure's suite used 1400.13 CPU seconds, 6.1 percent more than F303's 1319.51, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F303's closure run:
  +14.64 s  tests/runtimes/test_supervisor_portability.py (49.20 -> 63.84)
  +13.11 s  tests/serve_http_handler/test_public_api.py (0.00 -> 13.11)
  +10.87 s  tests/serve_http_handler/test_public_api_lifecycle.py (0.00 -> 10.87)
  +7.13 s  tests/cli/test_do_scale_matrix.py (39.17 -> 46.30)
  +5.23 s  tests/serve_http_handler/test_subtree_rerun_e2e_live.py (0.00 -> 5.23)
  +4.29 s  tests/orchestration/test_review_zip_hygiene.py (38.42 -> 42.71)
  +3.93 s  tests/orchestration/test_persisted_call_ownership.py (7.82 -> 11.75)
  +3.93 s  tests/orchestration/test_self_use_generator.py (4.04 -> 7.97)
  +3.23 s  tests/serve_http_handler/test_pause_e2e_live.py (0.00 -> 3.23)
  +3.23 s  tests/orchestration/test_subtree_rerun_prepare.py (11.56 -> 14.79)
```

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C4, then this C5), each touching only its named paths. The suite was RED and its transcript was committed as read, as the block orders; nothing was re-run, investigated or fixed. The cost script printed its reading and its exit code was 0 (the shell reported no failure); the self-use run exited 0. No amend, rebase, force-push or `--no-verify`, no pull request, `.data` never read, `REMEDY_TEST_MAX_WORKERS` never set.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 29, books its verdict and registers every self-use run defect in the next round's first commit.
4. A repair round naming every bad node id: `tests/orchestration/test_record_client_answers.py::test_the_folder_holds_one_answer_per_case_and_matches_a_fresh_recording` and `tests/orchestration/test_record_client_answers.py::test_the_check_names_every_changed_answer_and_exits_1`.
5. The closing round: the Built State, the re-assigned findings, the rotation, the next findings paydown, the STATUS line, the README and the pull request.

Operator questions open: 0. Open findings count gate 4 printed: 6.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship.

The paid run was asked to stop Remedy's own practice queue from scheduling a software-update chore for a helper that has no internet access; it finished in about eight and a half minutes, its work passed the second model's review, and it was left unapplied for a person to decide.

The full test collection ran 23183 tests in all: 23181 passed and 2 failed, both failures coming from one check that compares recorded answers against fresh ones and sees one new difference.

The run took about seven and a half minutes, and the cost reading said the computer time was about six percent higher than the previous feature's, inside the allowed ten percent.
