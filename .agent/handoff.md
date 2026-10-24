# Handoff — F162 round 4

## Session

SESSION 1 of feature F162 · round 4 · rounds so far 4. This session booked round 3's verdict,
appended DECISION F162 D4 and the plan rewrite in its first commit, then built the first half of
T003: the `WorkerSandboxDefault` declaration on the adapter contract, the claude-cli reference
adapter's own default profile and reason, the conformance kit's eighth dimension, the deleted
orphan entry, and the contract page's new section; context self-assessment: every new declaration
was proved by parsing its own TOML text through the existing parser and comparing the resulting
`SandboxProfile` against a literal written out in the test, rather than trusting the string's
shape by inspection alone, and the kit's own broken-toy pattern was reused for the two new refusal
cases so the new dimension is proved the same way every older one already is.

Fortschritt: ~55 % (T001, T002 landed · T003 under way) — Schätzung.

## Range

Review of `652dc874d`..`95c733534` (C1 to C3, plus one correction commit on C2's paths; C4 — this
file — is the commit that carries it, per the handback template's self-reference exception).

## Commits

### 7e2159a8a F162 R4 C1: book round 3, DECISION F162 D4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r4.md` | +128/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +15/-0 | DECISION F162 D4 appended: the contract, the claude-cli default, the kit, the doubles, what waits for the next round |
| `.agent/live_review.md` | +2/-0 | round 3's gate/verdict entry booked |
| `.agent/plan.md` | +9/-8 | rewritten: Current Step moves to T003 under DECISION F162 D4 |
| `.agent/prose_slips.md` | +1/-0 | round 3's own prose slip (the orphan reason's raw-text line wrap) appended |

### 7eb93b2ea F162 R4 C2: the adapter contract's sandbox default and the claude-cli declaration
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_contract.py` | +30/-0 | `WorkerSandboxDefault` frozen dataclass after `WorkerIsolation`, with its four D4 (1) refusal rules; the protocol's `sandbox_default()` member after `isolation()` |
| `packages/providers/adapters/claude_cli_reference.py` | +31/-0 | `_SANDBOX_PROFILE_TOML` and `_SANDBOX_DEFAULT_REASON` module constants (D4 (2)'s exact values); `sandbox_default()` returning them, `tool_sandbox=False` |
| `tests/contracts/test_adapter_conformance_kit.py` | +23/-0 | `_ConformingCliToy` and `_ConformingHttpToy` each gain `sandbox_default()` so both stay a `WorkerAdapter` under the grown protocol |
| `tests/contracts/test_adapter_contract.py` | +48/-2 | `WorkerSandboxDefault` added to the frozen-dataclass table; one parametrized case per D4 (1) refusal rule; `_ConformingToy`/`_MissingMapUsage` gain the method, "seven" renamed "eight" |
| `tests/contracts/test_claude_cli_reference.py` | +45/-1 | three new tests: the declaration equals D4 (2) word for word, its `profile_toml` parses to the literal `SandboxProfile`, the adapter is still a `WorkerAdapter` by `isinstance` |
| `tests/orchestration/test_capability_routes.py` | +15/-1 | the two reduced-capability doubles gain `sandbox_default()`, borrowing the reference adapter's, matching their existing `isolation()` pattern |

### b815b3c45 F162 R4 C3: the conformance kit's sandbox dimension, and the contract page
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_conformance_kit.py` | +25/-4 | `CONFORMANCE_DIMENSIONS` gains `"sandbox"` between `"isolation"` and `"transport"`; `_check_sandbox` (D4 (3)'s two messages, catching only `SandboxProfileError`); dispatch table entry; module docstring's exception sentence updated |
| `tests/contracts/test_adapter_conformance_kit.py` | +32/-2 | two new broken toys (not a `WorkerSandboxDefault`; a profile missing `fs_scope`) wired into `_BROKEN_CASES`; the pinned dimension tuple gains `"sandbox"`, "seven" renamed "eight" |
| `tests/test_no_orphan_modules.py` | +0/-2 | the `sandbox_profiles.py` `ALLOWED_UNWIRED` entry deleted — the kit is now a non-test importer |
| `docs/system/worker-adapter-contract-v2.md` | +17/-4 | the method table gains the `sandbox_default()` row; "six methods"/"seven dimensions" become "seven"/"eight"; new `## Sandbox default` section after Worker isolation |

### 95c733534 F162 R4 C2: fix the adapter's comment and give every isolation double an explicit sandbox_default
| Path | +/- | Reason |
|---|---|---|
| `packages/providers/adapters/claude_cli_reference.py` | +2/-2 | correction: a comment named `sandbox_profiles` literally, which the round's own `verify.py` reads as an import of that module; reworded with no behavioural change |
| `tests/orchestration/test_worker_adapter_slot.py` | +6/-0 | correction: `_ThrowawayAdapter` (an `isolation()`-overriding double) gains a trivial `sandbox_default()` delegating to `super()`, so the file holds the literal member `verify.py`'s own text search requires |
| `tests/orchestration/test_worker_isolation.py` | +6/-0 | correction: `_ThrowawayHomeAdapter` gains the same trivial delegating override, for the same reason |

### (this commit) F162 R4 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh pr list`, `gh pr create`, `gh pr merge`, or `git worktree` command this round: this is a
continuation round on the already-open feature branch, not a new branch start, so the Open PR Gate
does not apply here (it is the next round's first duty, named in `## Next`). No `claude` binary
invoked; no model/provider call of any kind; no container image pulled or run. `git push origin
feature/f162-sandbox-profiles` runs once, immediately after this commit, per the block's push
discipline; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** After the C2 correction commit, `git -C <repository root> status --porcelain`: empty
output. Then `python3 .remedy-wt/f162-r4/prep/verify.py .`:
```
True	7e2159a8a single parent equal to the commit before it
True	7e2159a8a subject carries a F162 R4 Cn tag: F162 R4 C1: book round 3, DECISION F162 D4, the plan
True	7e2159a8a insertions 155 under 500 (or the handoff alone)
True	7eb93b2ea single parent equal to the commit before it
True	7eb93b2ea subject carries a F162 R4 Cn tag: F162 R4 C2: ...
True	7eb93b2ea insertions 192 under 500 (or the handoff alone)
True	b815b3c45 single parent equal to the commit before it
True	b815b3c45 subject carries a F162 R4 Cn tag: F162 R4 C3: ...
True	b815b3c45 insertions 74 under 500 (or the handoff alone)
True	95c733534 single parent equal to the commit before it
True	95c733534 subject carries a F162 R4 Cn tag: F162 R4 C2: fix the adapter's comment ...
True	95c733534 insertions 14 under 500 (or the handoff alone)
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [...]: [...] (five paths, exact match)
True	C1 .agent/authored/f162-r4.md equals c1-.agent__authored__f162-r4.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths hold the required set and otherwise only tests: [...] (eight paths, union of both C2-tagged commits)
True	C2 touches no other production file
True	C2 7eb93b2ea adds no machine path
True	C2 95c733534 adds no machine path
True	C3 paths exactly [...]: [...] (four paths, exact match)
True	C3 b815b3c45 adds no machine path
absent	C4
True	every test file with an isolation() double also has sandbox_default(): missing []
True	C2 contract holds the dataclass and the protocol member
True	C2 contract does not import sandbox_profiles
True	C2 adapter does not import sandbox_profiles
True	C2 adapter reason word for word
True	C2 adapter profile holds the allowlist and nofile 1024
True	C3 dimension order isolation, sandbox, transport
True	C3 orphan entry deleted
True	C3 page section and table row
True	the saved block equals block.md
ALL True
```
Every line `True` (C4 correctly `absent`, not yet committed when this gate ran); last line
`ALL True`. The first run of this gate, before the correction commit, read `False` on two lines —
the double-file text-search line (two files named their missing members) and the "C2 adapter does
not import sandbox_profiles" line (a comment, not an import, had spelled the module's name
literally) — every other line was already `True`. The correction commit above fixed both; this
second run is the one quoted.

**Gate 2.** `python3 .remedy-wt/f162-r4/prep/run_selection.py . .remedy-wt/f162-r4-worker/selection-output.txt`,
run once, after C3 and the C2 correction:
```
paths 95
exit 0
4418 passed, 2 skipped in 47.82s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED`
lines are the pre-existing two prior handoffs already named; neither is from this round's new
tests, so the gate is not red on that account. Not red, so no second run was needed.

**Gate 3.** `python3 -m ruff check packages/contracts packages/providers/adapters/claude_cli_reference.py tests/contracts tests/orchestration/test_worker_isolation.py tests/orchestration/test_capability_routes.py tests/orchestration/test_worker_adapter_slot.py tests/test_no_orphan_modules.py`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`9`. Exactly the block's named count.

## Authored-text proofs

C1's five byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated digest-verification script. The authored block's own proof:
`.agent/authored/f162-r4.md` is 128 lines (`wc -l`) with sha256
`276c0cbc14d2de05f6ee2104296298953ba4447133231dc666cb2d2d1d1b8af3`, identical to `block.md`'s own
sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. A correction commit (`95c733534`, tagged `F162 R4 C2`) was added after C3 to fix two defects
   discovered on gate 1's first run, both in C2's own work:
   a. The block's "search `tests/` for `def isolation(self`" step named five files, and the
      round read it as "every file whose double genuinely needs the new member to remain a
      `WorkerAdapter`" — three files needed it for real (either a standalone double or a double
      the kit checks by `isinstance`), so those three gained it in C2 proper. The other two files'
      every `isolation()`-overriding class already subclasses the reference adapter, so each
      already inherits `sandbox_default()` behaviourally; the round judged that sufficient and
      left those two files untouched. The round's own `verify.py`, however, checks the RAW TEXT of
      every file holding `def isolation(self` for the literal substring `def sandbox_default(self`
      anywhere in the file, regardless of inheritance, and both omitted files read `False` on that
      account. The fix adds one trivial `sandbox_default()` override — delegating to `super()`,
      with a WHY comment — to one class already in each file, with no behavioural change (the
      inherited method and the override return the identical value).
   b. A WHY comment on the claude-cli adapter's new profile constant named the parsing module by
      its literal dotted name, to explain that this module does not import it; `verify.py` checks
      that same substring to prove the import claim, so the explanatory comment defeated the very
      check it was trying to support. Reworded with no behavioural change.
   Both fixes touch only paths already inside C2's allowed set (DECISION: the double-file list,
   plus the production file C2 was already allowed to touch), so the fix is tagged `C2` again —
   the same mechanism prior rounds used for a same-commit correction (`verify.py`'s `by_tag`
   grouping unions every same-tagged commit's paths before checking them against the block's named
   set). Gate 1 was then run a second time, as the block allows for a red gate, and read `ALL True`.
2. Before the official gates ran, several single-file `pytest` invocations covering each file
   touched this round, and several `ruff check` runs, were made during drafting to self-review
   each commit's diff before it was staged. None ran concurrently with another test command, none
   was the full suite, and none was a mutation red-proof; gate 2 and gate 3 themselves each ran
   exactly once, after C3 and the correction, as the block requires.
3. A digest-verification script and a byte-copy script were written under
   `.remedy-wt/f162-r4-worker/` (created fresh this round) to verify the prepared files' sha256
   digests and to copy C1's five files with a byte-equality proof; neither is committed and neither
   is a model or `claude`-binary call.
4. A standalone python check (not committed) parsed the claude-cli adapter's new TOML constant
   through the existing profile parser to confirm the exact literal this round's tests assert; this
   is a read-only sanity check, not a test run or a model call.

No other departure from the block's ordered commit sequence beyond the one declared correction
above: no file touched outside the paths named per commit, no mutation red-proof, no full suite run
beyond gate 2's own selection, no `REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no
`claude` binary invoked, no worktree of my own, and no `gh pr merge`, `git checkout`/`git switch`
away from the feature branch, branch creation, rebase, amend, force-push, or `--no-verify`.

## For the operator, in plain sentences

This session finished booking the previous session's result and then built most of the next piece
of the sandbox work: every backend now has to state, in a machine-checked way, what its default
safety profile is and whether its process runs inside the strongest protection this project offers.
The one backend that exists today declares an outside-the-strongest-protection default, because its
login credential lives in a place that protection would hide, and its default only names the one
external address its calls are actually for — a promise that is written down and checked for shape,
though nothing yet refuses a call that breaks it. The machine-checked proof that every backend
honors its promises grew an eighth test to cover this new requirement, matching the shape of the
seven checks already there. A small number of long-standing test stand-ins for a backend needed a
one-line addition each to keep counting as a complete stand-in now that the requirement grew, and
one of those additions, plus one explanatory comment, had to be corrected once a first verification
pass caught that they did not yet satisfy the round's own machine check; both were fixed in a
dedicated follow-up commit before anything moved on. What still needs doing is connecting this new
declaration to how a real worker actually starts, letting a project state its own choice, and
telling the project's health check what to warn about when it cannot trust what it is told.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | the contract's dataclass and protocol member, the claude-cli declaration, their tests, the doubles that needed it; 192 insertions |
| C2 correction | deviated | declared above; fixes two gate-1 defects (two double files missing the literal member, one comment naming the module it must not import); 14 insertions |
| C3 | done | the kit's eighth dimension, the deleted orphan entry, the contract page's row and new section; 74 insertions |
| C4 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | red on two lines on the first run (declared above), green on the re-run: every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `4418 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind`, no SKIPPED from this round's new tests |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `9`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 4's verdict in the next round's first commit.
4. T003: the declaration compiled onto the claude-cli spawn policies, the evidence, the project's
   choice and the doctor, DECISION F162 D5.

Operator questions open: 3.
Open findings: 9 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned by
F316; F162 takes none of them).
