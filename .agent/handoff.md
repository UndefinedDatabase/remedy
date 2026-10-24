# Handoff — F162 round 9

## Session

SESSION 1 of feature F162 · round 9 · rounds so far 9. Every new behaviour this round was proved
against the real sandbox-profile and container-enforcement records the earlier rounds' own tests
already exercise — the generator's word-for-word cell and the new container record test — never
against an assumed outcome. The session ends after this round because the closure sequence needs a
fresh session.

Fortschritt: ~88 % (T001 to T003 landed · the closure open) — Schätzung.

## Range

Review of `2474214d2`..`10e54dedf` (C1 to C2; C3 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### d7c16b954 F162 R9 C1: book round 8, resolve R-1468, register R-1469, DECISION F162 D9, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r9.md` | +99/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +10/-0 | DECISION F162 D9 appended: a `nothing to limit` reason reads `no limit declared`, and its Proof names the process and container tests pinning that reason |
| `.agent/live_review.md` | +6/-0 | round 8's gate/verdict entry booked, R-1469 registered OPEN (the repair R-1469's own text orders) |
| `.agent/plan.md` | +7/-6 | rewritten: Current Step moves to round 9 under DECISION F162 D9; Next Steps point at session 2's closure sequence |

### 10e54dedf F162 R9 C2: repair R-1469, an unlimited dimension reads no limit declared
| Path | +/- | Reason |
|---|---|---|
| `scripts/render_sandbox_model.py` | +27/-3 | `_runner_cell` reads `no limit declared` for the reason `nothing to limit`; `_profile_table` routes such a row's Proof to two new constants — the existing claude-cli record test for the process runner, a new full-tuple container test for the container runner — instead of the per-key `_PROCESS_PROOF`/`_CONTAINER_PROOF` entry |
| `docs/system/sandbox-model.md` | +8/-8 | REGENERATED only via `python3 scripts/render_sandbox_model.py`: the eight rows whose reason is `nothing to limit` (standard and net-local's `ulimits.mem_mb` and `allowed_binaries`; claude-cli default's `ulimits.cpu_s`, `ulimits.mem_mb`, `allowed_binaries` and `tmp_quota_mb`) now read `no limit declared` in both runner columns, with the Proof column pointing at the two D9 tests |
| `tests/docs/test_sandbox_model_doc.py` | +7/-0 | one new test: no line of the rendered document holds `prevents — nothing to limit` |
| `tests/orchestration/test_sandbox_container.py` | +27/-0 | one new test, `test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime`: the claude-cli default, parsed from the reference adapter's `sandbox_default()`, gives `container_sandbox_enforcement` with a runtime its full seven-item tuple, reasons word for word, pinning `nothing to limit` for the same four keys D9 names |

### (this commit) F162 R9 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |
| `.agent/live_review.md` | +1/-0 | one `Landed: R-1469 — RESOLVED at F162 R9 by C2, 10e54dedf. ...` line appended as the file's last line |

## External actions

No `gh pr list`, `gh pr create`, `gh pr merge`, or `git worktree` command this round: this is a
continuation round on the already-open feature branch, not a new branch start, so the Open PR Gate
does not apply here (it is the next round's first duty, named in `## Next`). No `claude` binary
invoked; no model/provider call of any kind. No container image pulled, built or pushed at any
point this round, and no container started outside the test runs. `git push origin
feature/f162-sandbox-profiles` runs once, immediately after this commit, per the block's push
discipline; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** After C2, `git -C <repository root> status --porcelain`: empty output. Then
`python3 .remedy-wt/f162-r9/prep/verify.py .`:
```
True	d7c16b954 single parent equal to the commit before it
True	d7c16b954 subject carries a F162 R9 Cn tag: F162 R9 C1: book round 8, resolve R-1468, register R-1469, DECISION F1
True	d7c16b954 insertions 122 under 500 (or the handback)
True	10e54dedf single parent equal to the commit before it
True	10e54dedf subject carries a F162 R9 Cn tag: F162 R9 C2: repair R-1469, an unlimited dimension reads no limit decla
True	10e54dedf insertions 69 under 500 (or the handback)
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [four paths]: [four paths] (exact match)
True	C1 .agent/authored/f162-r9.md equals c1-.agent__authored__f162-r9.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly [four paths]: [four paths] (exact match)
True	C2 10e54dedf adds no machine path
absent	C3
True	C2 no cell reads prevents — nothing to limit
True	C2 the document says no limit declared
True	C2 a no-limit row's process proof is the claude-cli record test
True	the saved block equals block.md
ALL True
```
Every line `True`; `C3` correctly `absent` (not yet committed when this gate ran). Not re-run: it
was green on the first run.

**Gate 2.** `python3 .remedy-wt/f162-r9/prep/run_selection.py . .remedy-wt/f162-r9-worker/selection-output.txt`,
run once, after C2:
```
paths 111
exit 0
5172 passed, 2 skipped in 55.28s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED` lines
are the same two pre-existing, opt-in skips every prior round's own handoff names; neither is from
the container fixtures, which this gate makes a red condition — every container-runner test,
including the new full-tuple test, passed outright. Not red, so no second run was needed.

**Gate 3.** `python3 -m ruff check scripts/render_sandbox_model.py tests/docs/test_sandbox_model_doc.py tests/orchestration/test_sandbox_container.py`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`11`. Exactly the block's named count (this ran BEFORE C3's `Landed:` append; `Landed:` is not a
`Done:` line, so the count is unchanged by this handback and stays `11` until the next round's
first commit books a proper `Done:` paragraph).

## Authored-text proofs

C1's four byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated copy-and-hash script (every digest in `digests.txt`, and `digests.txt`'s
own sha256 against the one the session prompt named, independently confirmed with `sha256sum -c`
before any prepared file was read). The authored block's own proof: `.agent/authored/f162-r9.md` is
99 lines (`wc -l`) with sha256 `e405d85de745a451f0a5f597ed5f29a9a3e0cebd9df00ee01ceda4ad13ccefe4`,
identical to `block.md`'s own sha256 — the same digest `digests.txt` names for both prepared files.
Gate 1's `verify.py` run independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. DECISION F162 D9 states the Proof swap as "for each runner" on "such a row", without naming
   which axis decides a row is "such a row" when the process and container reasons could in
   principle differ. Every actual case this round touches has both runners reading `nothing to
   limit` together for a given (profile, key) — the record functions return that reason before
   ever consulting the platform or the runtime-available flag — so this round reads the condition
   per cell (`process_item.reason == "nothing to limit"` independently decides the process half of
   the Proof string, and the container reason the container half) rather than requiring both
   together. The two outcomes coincide on every row the rendered document contains today; a future
   dimension whose two runners could disagree on `nothing to limit` would need this read confirmed
   or widened.
2. The new container test's exact name,
   `test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime`, is this
   round's own choice, built to match the existing sibling
   `test_container_sandbox_enforcement_full_tuple_for_strict_with_a_runtime`'s naming rather than
   copied from any pre-typed string; D9 names the test's *content* ("the full value tuple ...,
   reasons included") but not a literal identifier.
3. `tests/orchestration/test_worker_adapter_slot.py` is read, not edited, this round: its existing
   `test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal` already pins the
   process-side `nothing to limit` reasons D9 names, so C2's paths exclude it, matching the block's
   EXPECT set exactly.
4. No file outside the paths named per commit; no mutation red-proof; no full suite run beyond
   gate 2's own selection; no `REMEDY_TEST_MAX_WORKERS`; no two test commands run at once; no
   `claude` binary invoked; no container image pulled, built or pushed, and no container started
   outside the test runs; no worktree of my own; no `gh pr merge`, branch switch, rebase, amend,
   force-push or `--no-verify`; no agent, fork or subagent of any kind — every command this round
   is one call, run alone.

## For the operator, in plain sentences

This session booked the previous session's passing result and then closed the one small honesty
gap that review found in the generated safety page: a dimension a profile leaves completely
unlimited was being described as something a runner "prevents", when there is nothing there for
either runner to prevent at all. Such a row now says plainly that no limit was declared, and the
line backing that claim points at a real test that proves the declaration is really absent, for
both ways of running a worker. With that fix in, the building work this feature set out to do is
complete. What remains is a short closing sequence a fresh session will run next: a self-check of
the feature's own build process, one full pass of every test together, and the packaging of the
evidence that both succeeded, before the result goes up for the project's own review.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | the `no limit declared` reading, the amended proof map, the regenerated document and two new tests; 69 insertions |
| C3 | done | this handoff plus the ledger's one `Landed:` line |
| R-1469 | done | RESOLVED at F162 R9 by C2, `10e54dedf`; booked here as `Landed:`, to become a `Done:` paragraph in the next round's first commit |
| Gate 1 | done | every line `True`, `C3` correctly `absent` |
| Gate 2 | done | exit 0, `5172 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind`, neither skip from the container fixtures |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `11`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate — no PR is open for F162 yet.
3. Re-run `.remedy-wt/f162-r9/prep/verify.py` and book round 9's verdict in the next round's first
   commit.
4. The closure sequence per `docs/roadmap/STATUS_closure_protocol.md`: the self-use run, the
   integration gate, the evidence package, the Built State, the STATUS acceptance.

Operator questions open: 3.
Open findings: 11 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned
by F316; R-1467, owned by F246; R-1469, owned by F162 and landed this round, pending its `Done:`
paragraph).
