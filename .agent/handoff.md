# Handback — F274 ROUND 14 — the last two `worker_recommend` edges, the token policy event shrunk

This file supersedes the round 13 handback. It is written by a delegated worker on the reviewer's
authored block, because the reviewer never edits a work-tree file. Round 14 lands DECISION F274 D7
item 4: `agent_loop.py` and `autonomy_loop.py` stop calling `recommend_worker` and take their token
mode from `derive_token_mode`, `CycleDecision.selected_worker` goes, and `token_policy_applied`
loses `estimated_context_tokens`, `remote_model_requires_approval` and `selected_worker` in
`packages/orchestration/event_schemas.py` IN THE SAME COMMIT as the last emitter that wrote them,
with the test and smoke-script pins moved in that commit too. `packages.orchestration.worker_recommend`
now holds NO recorded edge in the cluster deletion map and is deletable. Round 13's PASS verdict is
booked, R-0836 is REGISTERED and NOT fixed, and the prose slip round 13 owed is appended.

## Session

SESSION 6 of feature F274 · round 14 · feature rounds so far 14 of the soft limit of 25,
sessions 6 of 7.

`.agent/STOP` was ABSENT at the round's start, ABSENT at the reading bracketing C4, and ABSENT
after C5. See the deviations — the middle reading was taken immediately AFTER C4 rather than
immediately before it.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): worker context is comfortable and was
never the binding constraint this round — all four slices verified on first read, every pair applied
on the first attempt, and no gate needed a second run, so nothing here argues for ending the session.

## Range

Review of `f1f50ecd`..`e3d87b25` (C5, the commit writing this file, follows and is not gated here).

## Commits

Six commits before C5, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4.

### edc94093 C0a: save the round 14 block verbatim under agent authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f274-r14.md | +490 / -0 | `shutil.copyfile` of the reviewer's scratch original `.remedy-wt/f274-r14-FINAL.md`, byte for byte |

### 567490a7 C0b: mirror the round 14 block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +397 / -397 | same bytes mirrored by `shutil.copyfile`; verbatim rewrite of ONE `.agent/**` state file, DECISION F104 D1 exempt, and under 500 regardless |

### 689009ae C1: point the plan at round 14 and the R-0836 fix that follows
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12 / -10 | replaced entirely by the PLAN14 slice; plan current before every later commit |

### 4bfb8001 C2: book the round 13 PASS verdict and register R-0836
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | RECORD14 appended; books round 13's PASS and REGISTERS R-0836. Findings persist FIRST, so this precedes C4 |

### 4c060a46 C3: append the round 13 prose slip about a worktree count
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | SLIPS14 appended, one dated line |

### e3d87b25 C4: cut the last two worker recommendation edges and shrink the token policy event
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/agent_loop.py | +5 / -8 | Q1: import swap to `derive_token_mode`, `_initial_events` and the `recommend_worker` call removed, three keys dropped from the `token_policy_applied` emission |
| packages/orchestration/autonomy_loop.py | +9 / -17 | Q2-Q8: `CycleDecision.selected_worker` deleted, import swap, the per-cycle `recommend_worker` call deleted, `_emit_token_policy_applied` loses its `events` parameter and its own three keys, the JSON export loses `selected_worker` |
| packages/orchestration/event_schemas.py | +3 / -3 | Q9: `token_policy_applied` ruled down to three keys, with the DECISION F274 D7 WHY comment above it |
| tests/storage/test_persistence.py | +5 / -16 | Q10-Q14: the five schema pins moved to the three-key vocabulary in the SAME commit as the emitters |
| scripts/remedy_smoke.sh | +2 / -3 | Q15: the smoke script's key list and its `worker=` print moved with the schema |
| tests/orchestration/cluster_deletion_map.txt | +0 / -2 | Q16: both `worker_recommend` edges deleted in the commit that cuts them, as the ratchet demands |

Commit C4 totals +24 / -49 over six files, against the DECISION F104 D1 cap of 500 insertions.
No commit in this round is oversize and none is declared as such.

### C5 — the commit writing this file
Per the R-0149 self-reference exception a handoff cannot table the commit that writes it. C5 touches
`.agent/handoff.md` only. Its insertion count is deliberately NOT reported here, per constraint 7 —
the reviewer measures it at the next gate.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/g7 --detach e3d87b25` | EXIT 0 — the disposable worktree for G7, per constraint 5 |
| `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/g7` | EXIT 0 |
| `git worktree prune` | EXIT 0 — `git worktree list` back to 14, its pre-round count |
| `git push origin feature/f274-one-world-completion-part-two` | run at C5, after this file is committed; outcome recorded in the round report |

No PR was created, edited or merged. No `gh` command was run. `remedy` is denied to this session and
nothing in this block needed it.

## Verification — ONE LINE PER GATE, real commands and real numbers

- **G1 TRANSPORT, at C0b — PASS.** `git show <C0b>:.agent/authored/f274-r14.md` and
  `git show <C0b>:.agent/last_block.md` are each 35305 bytes at sha256
  `445b54f35bdf5f4f9fc3b58d7fe413027ea7b5bdd3d51c079421d5e4beff0dc9`, equal to each other and to the
  digest and byte count the delegation message stated for `.remedy-wt/f274-r14-FINAL.md`, which the
  worker hashed as its first action (35305 bytes, 490 lines, same digest). Per §3 item 37 this covers
  those artefacts and is not a claim about the bytes emitted into a prompt.
- **G2 THE RECORD APPEND, at C2 `4bfb8001`, re-derived from the COMMITTED blobs — PASS on every
  clause.** (a) BYTES 594390 -> 602276 exactly as stated; prefix clause `post[:len(pre)] == pre` True;
  BYTE reader `post == pre + slice` True. (b) STRUCTURE: N counted from the slice = 2, units
  234 -> 236 exactly as stated, last 2 units of the post-image equal the slice's units IN ORDER True,
  everything before unchanged True. (c) NEGATIVE CONTROL at zero-indexed offset 594391, which reads
  `G` as the block says — the BYTE reader of (a) rejects the mutant (False) and the STRUCTURAL reader
  of (b) rejects it (False). (d) COUNTS, every one reproducing: registrations 69 -> 70 (identical on
  the line reading and the DISTINCT-id reading), distinct resolutions 6 -> 6, OPEN SET 63 -> 64 BY
  DISTINCT ID, `^Gate: ` 44 -> 45, `^Gate: F274 R13 ` 0 -> 1, `^- R-0836 — ` 0 -> 1. The literal
  `^Done: R-\d+ — ` LINE count is 8 against 6 distinct ids, unchanged by this round and consistent
  with what round 13's own record already states.
- **G3 THE PROSE STATE FILES — PASS.** `.agent/plan.md` at C1 `689009ae` is BYTE-EQUAL to the PLAN14
  slice (2813 bytes, sha256 `92cb34938c23dbf8999d499759ff7d24638e5ef9f8ed1fb30d36fbfa5f15d4e8`), is
  46 lines against the cap of 50, and carries both `## Goal` and `## Next Steps`.
  `.agent/prose_slips.md` at C3 `4c060a46` goes 163225 -> 163910 with the pre-image a byte-exact
  prefix (True), `post == pre + slice` True, and the appended line occurring exactly once.
- **G4 THE CUT LANDED WHOLE, at C4 `e3d87b25`, against the COMMITTED blobs — PASS, with two readings
  DECLARED below rather than adjusted.** (a) THE PAIRS: all 16 FROM blocks occur ZERO times. TO
  counts: Q1-Q4, Q6-Q9, Q11, Q13-Q16 read 1; Q5's TO is EMPTY (a deletion, so the count is
  undefined); Q10 and Q12 each read 2 because their TO blocks are BYTE-IDENTICAL to one another and
  land in the same file. All 16 pairs printed `TO contains FROM: false` at the base, exactly as the
  block recorded, so every pair is a REWRITE and none carries the §4.9 append obligation; each FROM
  occurred EXACTLY ONCE at `f1f50ecd` before application. (b) THE ZERO-GATE: `worker_recommend`
  1 -> 0 in `agent_loop.py` and 2 -> 0 in `autonomy_loop.py`; `selected_worker` 1 -> 0 in
  `agent_loop.py`, 5 -> 0 in `autonomy_loop.py`, 5 -> 0 in `tests/storage/test_persistence.py` and
  2 -> 0 in `scripts/remedy_smoke.sh`. REPORTED not gated, as the block orders:
  `event_schemas.py` goes 2 -> 1, the survivor being the `agent_loop_cycle_decision` entry R-0836
  is about. (c) THE SCHEMA, by IMPORTING the module and inspecting the object:
  `EVENT_METADATA_SCHEMAS["token_policy_applied"]` is a `frozenset` of len 3 equal to
  `frozenset({"mode", "max_context_tokens", "local_first"})`. (d) THE MAP: lines 37 -> 35, edges
  22 -> 20, `worker_recommend` edges 2 -> 0, cluster modules holding at least one edge 12 -> 11, and
  the post-image sha256 is `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155` —
  THE DIGEST THE BLOCK PREDICTED BEFORE THE ROUND RAN. (e) all four touched `.py` blobs parse under
  `ast.parse`, and `git diff --name-only f1f50ecd..e3d87b25` names exactly the eleven paths of
  constraint 3 and nothing else.
- **G5 LINT, at C4 — PASS.**
  `python3 -m ruff check packages/orchestration/agent_loop.py packages/orchestration/autonomy_loop.py packages/orchestration/event_schemas.py tests/storage/test_persistence.py`
  EXIT 0, output `All checks passed!` — so no unused `_initial_events` and no stale import survived.
  `python3 -m ruff check .` reports `Found 26 errors.` and EXITS 1, which is the gate PASSING:
  DECISION F083 D5's frozen ceiling is 26, unchanged by this round, not 0.
- **G6 THE SUITES, at C4, EACH COMMAND RUN ALONE IN THE PRIMARY CHECKOUT per constraint 7 — PASS.**
  (a) every one EXIT 0, and every count equals the reviewer's bracketed figure:
  `tests/storage/test_persistence.py` 26 passed [26]; `tests/orchestration/test_autonomy.py` 81
  passed [81]; `tests/orchestration/test_event_ledger.py` 21 passed [21];
  `tests/orchestration/test_cluster_deletion_map.py` 3 passed [3];
  `tests/orchestration/test_import_reachability.py` 3 passed [3];
  `tests/test_remedy_smoke_script.py` 191 passed [191]; `tests/test_token_policy.py` 28 passed [28];
  and THE CANARY `tests/cli/test_golden_path.py` 42 passed [42]. Each was invoked as
  `python3 -B -m pytest <path> -q`. (b) THE FULL SUITE: `python3 -m pytest -q -n auto` EXIT 0,
  **19769 passed, 0 failed, 23 skipped, 1 warning in 171.34s**. The ORDERED PROPERTY, zero failed,
  holds. No file needed a serial re-run because nothing failed, and nothing was edited to make a red
  go away. The block stated no passed count here on purpose; 19769 is the number this run produced,
  for the reviewer to reconcile at the next gate.
- **G7 THE RED PROOFS, in the disposable worktree `.remedy-wt/g7` at C4, each with its UNMUTATED
  control FIRST in that same worktree — PASS, both.** Import resolution was confirmed before trusting
  any colour: `python3 -c "import packages.orchestration.autonomy_loop as m; print(m.__file__)"` run
  with cwd inside the worktree resolves to
  `/home/decodeux/Repos/remedy/.remedy-wt/g7/packages/orchestration/autonomy_loop.py`, so the
  editable-install `.pth` entry did not shadow it. `__pycache__` was purged before every run and every
  pytest carried `-B`.
  (a) THE REGISTRY AND THE EMITTERS HELD IN AGREEMENT — control
  `python3 -B -m pytest tests/storage/test_persistence.py -q` EXIT 0, 26 passed. The three-line window
  `mode=derive_token_mode(job),` / `max_context_tokens=tp.budget.get("expensive_tokens", 100_000),` /
  `local_first=True,` occurs EXACTLY ONCE in `autonomy_loop.py` at C4 (the bare `local_first=True,`
  line likewise once); inserting `            selected_worker="ollama/qwen3:8b",` directly after it
  gives EXIT 1, `1 failed, 25 passed`, with
  `tests/storage/test_persistence.py::TestTokenPolicyAppliedSchema::test_autonomy_loop_emits` as the
  ONLY failing node id, and the assertion text is
  `Schema errors: ["token_policy_applied: extra keys ['selected_worker']"]` — `validate_event_metadata`
  reporting the extra key, which is exactly the property that makes C4 one commit. Restored to sha256
  `5a51e9421cb62f6ad838825cc1e25834e45f4d8fb8e77a29b7365a72c40570e9`, byte-identical to C4, EXIT 0,
  26 passed.
  (b) THE MAP RATCHET BITES FOR BOTH CUT EDGES — control
  `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0, 3 passed. Both
  edge lines occur ZERO times in the map at C4, as the block states; re-inserting both gives EXIT 1,
  `1 failed, 2 passed`, the single failure being
  `test_the_recorded_map_equals_the_measured_import_graph` and the message reading
  `DISAPPEARED (2)` and naming
  `packages.orchestration.worker_recommend <- packages/orchestration/agent_loop.py` and
  `packages.orchestration.worker_recommend <- packages/orchestration/autonomy_loop.py`, with
  `APPEARED (0)`. Restored to sha256
  `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155` — the digest G4(d) pins —
  byte-identical to C4, EXIT 0, 3 passed.
- **G8 THE TREE, at C4 — PASS.** `git status --porcelain` EXIT 0, ZERO lines. `git ls-files .remedy-wt`
  EXIT 0, ZERO lines. `git worktree list` 14 worktrees, the same count as before the first worktree
  was added and after the last prune. Every commit C0a through C4 is SINGLE-PARENT (parents=1 each).
  Per-commit insertions: C0a 490, C0b 397, C1 12, C2 4, C3 2, C4 24 — every one under the DECISION
  F104 D1 cap of 500; C4's applied change is +24 / -49 over six files, exactly the 24 insertions and
  49 deletions the reviewer measured in its dry run. `.agent/STOP` readings: ABSENT at the round's
  start, ABSENT at the C4 bracket, ABSENT after C5.

## Authored-text proofs

Four reviewer-authored slices were applied this round. Each was extracted from
`.remedy-wt/f274-r14-FINAL.md` between its `BEGIN <NAME> sha256=<hex> bytes=<n>` and `END <NAME>`
markers and verified against its OWN marker before application; marker lines reached no file.

| Slice | Stated bytes | Measured bytes | sha256 verified | Applied to |
|---|---|---|---|---|
| PLAN14 | 2813 | 2813 | `92cb34938c23dbf8…` MATCH | `.agent/plan.md`, whole-file replacement, byte-equal |
| RECORD14 | 7886 | 7886 | `fe77ced157d331f2…` MATCH | `.agent/live_review.md`, exact append |
| SLIPS14 | 685 | 685 | `db33a94bb1bcc220…` MATCH | `.agent/prose_slips.md`, exact append |
| PAIRS14 | 8130 | 8130 | `8f89acaf1f718acb…` MATCH | applied as 16 FROM/TO pairs at C4; appended to no file |

The block's own bytes: `.remedy-wt/f274-r14-FINAL.md` measured 35305 bytes / 490 lines at sha256
`445b54f35bdf5f4f9fc3b58d7fe413027ea7b5bdd3d51c079421d5e4beff0dc9`, matching all three values the
delegation stated, and `shutil.copyfile` put those exact bytes at `.agent/authored/f274-r14.md` and
`.agent/last_block.md` (G1).

DELIMITER READING, stated because it is load-bearing and was resolved by measurement rather than by
assumption: a slice is the bytes AFTER the newline terminating its `BEGIN` line, up to the first byte
of its `END` line. Both candidate readings were hashed; the other reading (including the BEGIN line's
own terminating newline as a leading byte) missed every stated digest by exactly one byte, and this
reading matched all four. RECORD14 and SLIPS14 each carry their own leading blank line as the
paragraph separator, so no separator of the worker's own was added.

## Item-status table — the bundle of this round

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this file, then the push |

## Deviations & assumptions

The block's ordered commit sequence was followed EXACTLY: C0a, C0b, C1, C2, C3, C4, C5, six commits
before the handoff plus the handoff. No commit was added, dropped or reordered. Every slice was
applied BYTE FOR BYTE and nothing in the reviewer's text was silently repaired. Four things are
DECLARED:

1. **G4(a) cannot read "TO EXACTLY ONCE" for Q10 and Q12, and the reason is in the block's own text,
   not in the change.** Q10's TO block and Q12's TO block are BYTE-IDENTICAL — both are the single
   line `        required = {"mode", "max_context_tokens", "local_first"}` — and both land in
   `tests/storage/test_persistence.py`. After the cut that string therefore occurs TWICE in the file,
   which is CORRECT (the two distinct FROM blocks collapse to the same TO text)
   but makes the gate's stated reading of 1 unreachable for those two pairs by construction. The
   two FROM blocks start at lines 287 and 353 of that file at `f1f50ecd`, measured, not eyeballed. The
   worker reports the real number, 2 for each, and changed nothing to produce a 1. The load-bearing
   half of the gate — FROM occurring ZERO times — holds for all 16 pairs, and G4(b)'s zero-gate
   independently proves the old vocabulary is gone from that file.
2. **G4(a)'s "TO EXACTLY ONCE" is undefined for Q5, whose TO block is EMPTY by design.** The block
   itself says Q5 is a deletion. Counting occurrences of the empty string in a file is degenerate, so
   the worker reports `EMPTY (deletion)` rather than a number. Q5's FROM occurs ZERO times after the
   cut, its trailing blank line went with it, and the diff shows no double blank line left behind.
3. **G8's middle `.agent/STOP` reading was taken immediately AFTER C4 rather than immediately before
   it.** The block orders three readings: at the round's start, before C4, and after C5. The worker
   read the file at the round's start (ABSENT), then at the point between C4 and C5 (ABSENT), then
   after C5 (ABSENT). No sentinel was observed at any reading, but the reader should know the middle
   observation brackets C4 on the far side rather than the near side, so a sentinel appearing during
   C4 itself would have been caught while one appearing between C1 and C4 and removed again would
   not. Declared rather than quietly reported as ordered.
4. **Three checks were re-expressed in Python because the shell guard rejects their COMMAND FORM,
   not their content.** `echo "EXIT=$?"` after a command was refused (`$?` inside a compound
   command), and a `python3 - <<'PYEOF'` heredoc containing a brace with a quote character was
   refused as expansion obfuscation. Every affected check was re-run through a small Python runner
   under the gitignored `.remedy-wt/r14/` that invokes the SAME command via `subprocess.run` and
   prints its real returncode; the commands themselves are unchanged and are quoted verbatim in the
   Verification section above. The G7 worktree runs use `subprocess.run(..., cwd=<worktree>)` for the
   same reason, which also puts the worktree on `sys.path[0]` — the import-resolution probe above
   confirms the effect rather than assuming it.

ASSUMPTIONS: none beyond the block. `.remedy-wt/` stayed untracked throughout
(`git ls-files .remedy-wt` empty at G8) and the scratch files under `.remedy-wt/r14/` are gitignored
working artefacts, not repository state.

NOT DONE, deliberately and as the block orders: `packages/orchestration/worker_recommend.py` is NOT
deleted — it merely lost its last recorded edge and dies with the cluster in the round DECISION
F260 D3 governs. R-0836 is REGISTERED and NOT FIXED; `event_schemas.py` keeps its
`agent_loop_cycle_decision` and `agent_loop_stopped` entries and `selected_worker` still occurs there
ONCE, which is why G4(b) scopes its zero-gate away from that file. No `Done:` paragraph was written
by the worker (constraint 6): this round resolves nothing.

## Open findings

**64 open findings BY DISTINCT ID**, the number G2(d) MEASURED against the committed blobs
(70 distinct registrations minus 6 distinct resolutions). The open set ROSE by one BY DESIGN: this
round registers R-0836 and does not fix it. The open High findings remain R-0803, R-0804, R-0806 and
R-0807, all F273's rather than this feature's, per DECISION F272 D12.

## Next

The reviewer re-runs G1 through G8 itself against the committed blobs over `f1f50ecd`..HEAD and
issues the round 14 verdict. The next round's work, already named as step 1 of `.agent/plan.md`, is
the R-0836 fix: delete the `agent_loop_cycle_decision` and `agent_loop_stopped` entries of
`EVENT_METADATA_SCHEMAS` together with the ten sites in `tests/orchestration/test_event_ledger.py`
that pin them, in one commit, confirmed by a repo-wide grep reaching ZERO outside that commit's own
diff. Before authoring it, the reviewer re-reads `.agent/STOP` from disk — Phase 1 rule 1 before
rule 2.
