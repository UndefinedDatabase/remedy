# Handoff — F260 One world · round 15 · ONE RUN PER INVOCATION

## Session

SESSION 6 of feature F260 · round 15 · rounds so far 15

**`.agent/STOP` APPEARED DURING THIS ROUND.** It did not exist when the round
started (`ls .agent/STOP` → "No such file or directory") and it exists now: an
EMPTY, untracked, not-gitignored file with mtime `2026-09-06 10:20:01 +0200`,
which is twenty minutes AFTER this round's last code commit (`9487e1c8`,
committed `10:00:57`). Nothing in `tests/`, `packages/`, `apps/` or `scripts/`
writes that path — grep finds zero references — so it is an operator signal and
not fixture residue. Self-drive guardrail G6 says: "If `.agent/STOP` appears at
any point, finish the current commit if one is half-written, then hand off and
end." All eight gates were already executed when it appeared, so this handback IS
that finish. **No further round may be authored without the operator clearing it;
rule 1 of Phase 1 is to re-read `.agent/STOP` from disk before anything else.**

Context self-assessment (amend0905-throughput): context was never a constraint —
comfortable throughout. WALL CLOCK was the whole cost again: `tests/orchestration/`
744.74 s and `tests/cli/` 303.73 s, run SERIALLY, on top of G4's base-worktree
probe and G6's three worktree runs. The soft limit is 25 rounds or 7 sessions; at
15 rounds and 6 sessions the SESSION budget is the binding one and is reached next
session, so split-and-close is the endgame and this round leaves a self-consistent
tree.

## Range

Review of `1d344b485ce6c4e5e7768c6ab001a10bf8ab69d2`..`HEAD`.

SIX commits plus this handback, all single-parent (verified by
`git log --format="%H %P"` — every commit has exactly one parent and the chain
runs back to `1d344b48`), and they are EXACTLY the Bundle's ordered sequence
C0a → C0b → C1 → C2 → C3 → C4 → C5. No commit was added, dropped or reordered.
Largest insertion count 333 (`.agent/authored/f260-r15.md`, a single `.agent/**`
state write); largest CODE commit 73 insertions (`9487e1c8`). Nothing approached
the 500-insertion cap.

## Commits

`+/-` taken from `git log --numstat`, never re-derived by eye.

### daddf265 f260: save the round 15 block verbatim as the authored source
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r15.md | +333 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r15-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### 4fd49c6a f260: mirror the round 15 block into the last block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +291 / -355 | C0b — same source file, same `shutil.copyfile` route, same two proofs |

### d810d8ad f260: point the plan at one run per invocation for round 15
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -18 | C1 — whole-file replacement by the PLAN slice plus one trailing newline; 2531 bytes, 48 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps` |

### b06899b9 f260: record the round 14 gate, finding R-0816 and decision D7
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | C2 — GATE_R14 then FIND816 appended, in that order; 937682 → 947109 bytes |
| .agent/decisions.md | +3 / -0 | C2 — DEC_D7 appended in the SAME commit, AFTER the live_review append (constraint 4); 842038 → 845072 bytes |

### 97161332 f260: append the two round 14 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +4 / -0 | C3 — SLIP18 then SLIP19, blank-line separated; 117457 → 118817 bytes |

### 9487e1c8 f260: give the timeline one run id per process so an invocation is one run
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/timeline.py | +7 / -3 | C4 SPEC (1) — module-level `from packages.orchestration.run_log import RunLogWriter, new_run_id`; `_PROCESS_RUN_ID = new_run_id()` with its three-line WHY comment directly above it; the FUNCTION-LOCAL import DELETED; `run_id=_PROCESS_RUN_ID` passed at the one construction |
| tests/test_timeline.py | +66 / -1 | C4 SPEC (2) — `append_run_event` added to the existing `timeline` import, plus the new class `TestOneRunPerInvocation` carrying its three tests |

### C5 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — a handoff cannot table the commit that writes it (R-0149 pattern; constraint 10). No gate reading was taken after this file existed; the reviewer measures C5's own insertion count at the next gate |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f260-r15-base 1d344b485ce6c4e5e7768c6ab001a10bf8ab69d2` | exit 0; detached HEAD at `1d344b48` for G4 |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f260-r15-base --force` | exit 0; removed BY EXACT PATH |
| `git worktree prune` | exit 0 |
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f260-r15-head 9487e1c8968a34e175d8248b62ec41740694bd6e` | exit 0; detached HEAD at the round head for G6 |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f260-r15-head --force` | exit 0; removed BY EXACT PATH |
| `git worktree prune` | exit 0; `git worktree list` then shows **12 rows** — the primary checkout and the ELEVEN pre-existing `remedy/job-*` worktrees — and neither `f260-r15-base` nor `f260-r15-head` |
| `git push -u origin feature/f260-one-world` | runs AFTER this file is committed; see the note under Verification |

No PR created. No PR merged. No `gh` command run. No force push. No branch
deleted. No glob was used to remove anything. No file under `.remedy-wt/` was
ever `git add`ed.

## Verification

ONE LINE PER GATE, with its REAL exit code. Every suite ran SERIALLY — never two
at once — captured to its own file under `.remedy-wt/` and read from the capture.
The sandbox bash guard rejects `$?`, `$( )` and shell loop forms BY FORM, so
every exit code below came from a Python `subprocess.run(...).returncode` written
into the capture as a trailing `__EXIT_CODE__` line; none was inferred from
output text.

| Gate | Command / reading | Exit | Result |
|---|---|---|---|
| G1 | ONE comparison: sha256 of `.remedy-wt/f260-r15-block.md`, `.agent/authored/f260-r15.md`, `.agent/last_block.md`, checked BEFORE staging | **0** | all three **`454d291c41432e5c296dc56b28bbaabbcefa1c770f5d18b1555361acb4983d84`** at **32568** bytes, equal to the digest the DELEGATION names. Both writes were `shutil.copyfile` from the delegation's source path; `filecmp.cmp(shallow=False)` True for both |
| G2(a) live_review | exact-image byte equality | **0** | `post == pre + b"\n" + GATE_R14 + b"\n\n" + FIND816 + b"\n"` is **True**; prefix check `post[:len(pre)] == pre` **True**. **937682 → 947109** bytes. Recipe derived from THIS target's measured terminal byte, asserted == 1 before writing |
| G2(b) live_review | structural, whole file split on `"\n\n"` | **0** | units **435 → 437**; last-but-one unit EQUALS GATE_R14, last unit ends with exactly ONE newline and EQUALS FIND816 once that newline is removed — GATE_R14 then FIND816, in that order |
| G2(c) live_review | negative control, IN MEMORY on a `bytes` object | **0** | byte at offset **937723**, inside the appended region, XOR-flipped: reader (a) REJECTS, reader (b) REJECTS. After restore BOTH ACCEPT and the restored image EQUALS the disk image |
| G2(a) decisions | exact-image byte equality | **0** | `post == pre + b"\n" + DEC_D7 + b"\n"` **True**; prefix check **True**. **842038 → 845072** bytes |
| G2(b) decisions | structural, split on `"\n\n"` | **0** | units **1893 → 1894**; last unit ends with exactly ONE newline and EQUALS DEC_D7 once removed |
| G2(c) decisions | negative control, IN MEMORY | **0** | byte at offset **842079** flipped: both readers REJECT; after restore both ACCEPT and the restored image EQUALS the disk image |
| G2(d) | CENSUS after C2, counted by the script | **0** | `^Gate: ` **24** · registrations `^- R-\d+ — ` **301** over **301** DISTINCT ids · `^Done: ` **5** lines over **3** DISTINCT ids · **OPEN SET 298 BY DISTINCT ID**. Exactly the block's expected post reading (24 / 301 over 301 / 5 over 3 / 298). `R-0816` registered **True**; `R-0816` carries a `Done:` paragraph **False**, as constraint 5 requires |
| G3 (plan) | `.agent/plan.md` | **0** | disk bytes `== PLAN slice + b"\n"` **True**; **2531** bytes, **48 lines**, under the 50-line cap; `## Goal` present, `## Next Steps` present; `BEGIN `/`END ` lines **0** |
| G3 (slips) | `.agent/prose_slips.md` | **0** | `post == pre + b"\n" + SLIP18 + b"\n\n" + SLIP19 + b"\n"` **True**; **117457 → 118817** bytes; blank-line units **148 → 150**; last-but-one unit EQUALS SLIP18, last unit EQUALS SLIP19 — in that order; `BEGIN `/`END ` lines **0** |
| G4 | THE DEFECT IS REAL AT THE BASE — disposable worktree at `1d344b48`, `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`, run BEFORE C4 | **0** | `__pycache__` purged 0 → re-enumerated at **0**; `timeline.__file__` = `…/.remedy-wt/f260-r15-base/packages/orchestration/timeline.py`, resolves inside that worktree **True**; LIVE construction line printed as `writer = RunLogWriter(jid, data_root=Path(data_dir))`. Five events, one job, read from the BYTES: **jsonl files 5 · event lines 5 · DISTINCT run_id values 5** |
| G5 | THE FIX IS REAL AT THE HEAD — same probe, same shape, primary checkout after C4, `python3 -B` | **0** | `__pycache__` purged 28 → re-enumerated at **0**; LIVE construction line printed as `writer = RunLogWriter(jid, run_id=_PROCESS_RUN_ID, data_root=Path(data_dir))`. **jsonl files 1 · event lines 5 · DISTINCT run_id values 1**; TWO jobs in the same process → job A dir **1** file, job B dir **1** file, the two directories differ **True** |
| G6(i) | CONTROL, unmutated, disposable worktree at `9487e1c8`, `python3 -B`, selection `tests/test_timeline.py tests/test_run_log.py tests/test_data_paths.py` | **0** | **140 passed** in 0.81 s, 0 FAILED. `__pycache__` purged then RE-ENUMERATED at **0**. Module resolution CONFIRMED to that worktree: `timeline.__file__` = `…/.remedy-wt/f260-r15-head/packages/orchestration/timeline.py`, live construction line printed WITH `run_id=_PROCESS_RUN_ID` |
| G6(ii) | revert-target uniqueness, then the mutation | **1** | the exact bytes `run_id=_PROCESS_RUN_ID, ` occur **EXACTLY 1** time before mutating; after DELETING them the count is **0** and the LIVE construction line re-printed as `writer = RunLogWriter(jid, data_root=Path(data_dir))` — the pre-round behaviour exactly. **IT WENT RED: exit 1, 1 failed, 139 passed.** Failing node id: `tests/test_timeline.py::TestOneRunPerInvocation::test_all_events_of_one_invocation_share_one_run`. Only ONE of the three SPEC (2) tests is a discriminator for this mutation — **deviation 3** |
| G6(iii) | restore + clean worktree + removal | **0** | mutated byte count back at **0**, revert target back at **1**, file byte-identical to the pre-mutation image **True**; `__pycache__` re-enumerated at **0**; control re-run **exit 0, 140 passed**, the same reading as (i). That worktree's `git status --porcelain` **EMPTY** (`''`) and `git diff HEAD --stat` **EMPTY** (`''`). Worktree removed BY EXACT PATH, `git worktree prune` exit 0, path gone **True** |
| G7(1) | `python3 -m pytest tests/test_timeline.py tests/test_run_log.py tests/test_data_paths.py tests/test_patch_apply.py -q -p no:randomly` | **0** | **264 passed** in 2.04 s, 0 FAILED |
| G7(2) | `python3 -m pytest tests/orchestration/ -q -p no:randomly` | **0** | **12805 passed, 10 skipped**, 1 warning in 744.74 s. `^FAILED` lines **0**, `^ERROR` lines **0**. Identical pass/skip counts to the reviewer's `1d344b48` reading |
| G7(3) | `python3 -m pytest tests/cli/ -q -p no:randomly` | **0** | **1537 passed** in 303.73 s. `^FAILED` lines **0**, `^ERROR` lines **0**. Identical to the reviewer's `1d344b48` reading. Canary presence verified separately: `python3 -m pytest tests/cli/test_golden_path.py --collect-only` exit **0**, **42 tests collected**, so the canary IS inside the selection |
| G7(4) | `python3 -m apps.cli.grouped integrity check --json` | **0** | `"passed": true`, `"fail_count": 0`, `"check_count": 5`; all five checks `"status": "pass"` |
| G8 (lint) | `python3 -m ruff check` over the code files I counted myself — **TWO** | **0** | `All checks passed!` |
| G8 (tree) | `git status --porcelain` / `git ls-files .remedy-wt` | 0 / 0 | `git ls-files .remedy-wt` **EMPTY**. `git status --porcelain` is **NOT empty**: its single line is `?? .agent/STOP` — the operator's stop file, created at 10:20:01 during this round's gate phase and NOT mine to delete. **Deviation 4.** No other path appears; nothing of mine is uncommitted |

**THE TWO CODE FILES G8 LINTED, counted from my own change set rather than taken
from the block:** `git diff --name-only 1d344b48..HEAD` returns eight paths, six
of them under `.agent/`; the code files are exactly
`packages/orchestration/timeline.py` and `tests/test_timeline.py`. The two
pre-existing errors G8 warns about (`UP035` at `dag_schedule.py:36`, `F821` at
`gauntlet_injection.py:286`) were not approached; neither file is in the change
set and neither was opened.

**G4 AND G5 ARE THE PAIR, AND THE PAIR IS THE PROOF.** The same probe, the same
shape, the same five `event_replay` resume events, run at the base and at the
head:

    BASE (1d344b48)   jsonl files 5   event lines 5   DISTINCT run_id values 5
    HEAD (9487e1c8)   jsonl files 1   event lines 5   DISTINCT run_id values 1
    HEAD, two jobs    job A: 1 file   job B: 1 file   directories differ: True

Both readings come from parsing the `.jsonl` bytes the SHIPPED
`timeline.append_run_event` left on disk, not from asking the writer what it did.
`load_run_events` returns the five event names in append order at BOTH commits —
which is why test (iii) is a non-regression guard rather than a discriminator
(deviation 3).

The push runs AFTER this file is committed, so its transcript cannot appear in
the commit that carries it (the R-0149 self-reference pattern, the same reason the
C5 row of the commit table has no `+/-`). Its outcome is verifiable directly:
`origin/feature/f260-one-world` points at the C5 commit.

## Authored-text proofs

| Slice | Target | Shape | Proof |
|---|---|---|---|
| the whole block | `.agent/authored/f260-r15.md` | file copy | `shutil.copyfile`, then `filecmp.cmp(shallow=False)` = True, then sha256 equal to the delegation digest |
| the whole block | `.agent/last_block.md` | file copy | same source, same route, same two proofs |
| PLAN | `.agent/plan.md` | whole-file REWRITE | disk bytes `== slice + b"\n"`, True (G3) |
| GATE_R14 | `.agent/live_review.md` | APPEND, first | exact-image equality + structural reader + in-memory negative control (G2 a/b/c) |
| FIND816 | `.agent/live_review.md` | APPEND, second, same commit | same three readers; it is the LAST unit of the file |
| DEC_D7 | `.agent/decisions.md` | APPEND, same commit, AFTER live_review | exact-image equality + structural reader + in-memory negative control (G2 a/b/c) |
| SLIP18, SLIP19 | `.agent/prose_slips.md` | APPEND, IN ORDER | exact-image equality over the derived recipe, plus the two-unit reading (G3) |

Every slice was extracted from the COMMITTED `.agent/authored/f260-r15.md` — not
from a retype and not from the delegation message — by taking the lines strictly
between its marker lines, joined by `"\n"`, with no trailing newline. All **TWELVE**
marker lines were enumerated and each occurs EXACTLY ONCE; the six slices measure
PLAN 2530 bytes, GATE_R14 5737, FIND816 3686, DEC_D7 3032, SLIP18 722, SLIP19 634,
none of them ending in a newline. Every target file was re-read afterwards and
contains **ZERO** lines beginning `BEGIN ` or `END ` — `.agent/plan.md` 0,
`.agent/live_review.md` 0, `.agent/decisions.md` 0, `.agent/prose_slips.md` 0.
NO MARKER LINE REACHED ANY TARGET FILE.

## Deviations & assumptions

**1. SPEC (2)'s PLACEMENT ANCHOR DOES NOT EXIST IN `tests/test_timeline.py`.**
The spec says "Put it after the existing class that covers `append_run_event`; if
no such class exists, put it directly after the last `append_run_event` test."
Measured at the base, `git show 1d344b48:tests/test_timeline.py | grep -n
"append_run_event"` returns **ZERO** lines: that file had no class covering
`append_run_event` AND no `append_run_event` test, so NEITHER anchor was
available. `append_run_event` was exercised only from `tests/orchestration/`,
`tests/ui_server/` and `tests/ui_contracts/`, none of which this round may touch
(constraint 6). I placed `TestOneRunPerInvocation` directly after
`TestLoadRunEvents` — the class covering the sibling reader in the same module —
which keeps the two run-log-byte-reading classes adjacent and follows the order
the module itself declares. Nothing else in the file moved.

**2. SPEC (1)(c)'s TWO ANCHORS CANNOT BOTH HOLD.** It orders the constant
"Immediately BELOW the import block and ABOVE the first `# ---` banner". In
`timeline.py` at `1d344b48` the FIRST `# ---` banner is at line **31** (the
"Symbols" banner) and it sits INSIDE the import block, which continues to line
**43** — so "below the import block" and "above the first `# ---` banner" name
disjoint places and the two clauses cannot both be honoured. I applied the evident
intent: the constant sits below the LAST import line (the new `run_log` import)
and above the first `# ---` banner that FOLLOWS the import block, the "Load"
banner. The three-line WHY comment is byte-for-byte the slice's and sits directly
above the definition, which is what AGENTS.md's discoverability rule asks for.

**3. G6's MUTATION WENT RED, BUT ONLY ONE OF THE THREE SPEC (2) TESTS IS A
DISCRIMINATOR FOR IT.** The gate orders "that the run goes RED and that the
failures include the three tests SPEC (2) adds". The COLOUR clause — the one the
gate itself calls the ordered property — is MET: exit **1**. The three-test
clause is NOT. Deleting `run_id=_PROCESS_RUN_ID, ` reddens
`test_all_events_of_one_invocation_share_one_run` and nothing else.
`test_two_jobs_do_not_share_a_run_file` appends ONE event per job, so under
per-event run ids each job still gets exactly one file — it cannot tell the two
behaviours apart BY CONSTRUCTION, and it is a non-regression guard rather than a
discriminator. `test_events_come_back_in_append_order` is insensitive for the
reason FIND816 itself states: "`timeline.load_run_events` globs the job directory
and sorts by timestamp, so it returns all five events in order regardless" — G4
measured exactly that at the base, five events in order across five files. I did
NOT adjust, strengthen or re-scope any test to make the gate read as ordered
(constraint 1). The block's STOP condition is a GREEN mutation; the mutation was
RED, so I proceeded and declare the gap. If the reviewer wants all three to bite,
that is a change to SPEC (2) — (ii) would have to append TWO events per job and
(iii) would have to assert the FILE the events land in, not their order — and it
belongs in a later block, not in an edit I make to a test to satisfy a gate.

**4. G8's `git status --porcelain` IS NOT EMPTY: `?? .agent/STOP` APPEARED
MID-ROUND.** The gate orders it shown EMPTY, and it is not. The single line is an
untracked, NOT-gitignored, **zero-byte** `.agent/STOP` with mtime
`2026-09-06 10:20:01 +0200`. It did not exist earlier in this round — I checked
that path explicitly before the gate phase and `ls` returned "No such file or
directory" — and its mtime is twenty minutes after this round's last code commit
(`9487e1c8`, `10:00:57`). `grep -rn` for that path across `tests/`, `packages/`,
`apps/` and `scripts/` returns nothing, so no suite or fixture creates it; it is
an operator signal. I did NOT delete it: it is not mine, it is not in this
round's change set, and deleting the operator's stop signal to make a tree
reading green would be exactly the kind of adjustment constraint 1 forbids. I
also did NOT commit it. Everything of MINE is committed — no other path appears
in `git status --porcelain` — and `git ls-files .remedy-wt` is EMPTY. Guardrail
G6 of the self-drive protocol says to finish the current commit, hand off and
end, which is what this file does.

**5. SPEC (1)(b)'s RE-GREP, REPORTED AS ORDERED.** `grep -n "RunLogWriter"
packages/orchestration/timeline.py` before editing returns exactly three lines:
the docstring mention at 59, the FUNCTION-LOCAL import at 62 inside
`append_run_event`, and the construction at 65. There is **exactly ONE**
function-local `RunLogWriter` import in the module and NO other function imports
it, so exactly one deletion was made and the module now has ONE spelling of the
import — which is the point the spec states, rather than a fixed count.

**6. `ruff` ACCEPTED THE SPEC'S OWN PLACEMENT; `I001` DID NOT DISAGREE.**
Constraint 7 asks me to follow `ruff` over the spec's wording if they conflict.
They did not: `from packages.orchestration.run_log import RunLogWriter,
new_run_id` sorts directly after `from packages.orchestration.data_paths import
run_log_dir`, which is where the spec puts it, and `python3 -m ruff check` over
both edited files is exit 0. The import block was not hand-sorted. In
`tests/test_timeline.py` the existing single-line `timeline` import became a
parenthesised three-name block so the added name stays sorted — `ruff` accepts
it and it introduces no second convention.

**7. THE TEST FILE'S MODULE-LEVEL "Coverage:" DOCSTRING LIST WAS NOT EXTENDED.**
`tests/test_timeline.py` opens with a bullet list of what it covers. SPEC (2)
orders one class with three tests and nothing else, so I left that list untouched
rather than make an unordered edit; the new class carries its own docstring
stating the property and why it reads bytes, which is where a reader searches.
Stated so it is a declared choice rather than an oversight.

**8. CONSTRAINT 2's THREE TERMINAL-BYTE MEASUREMENTS, RE-DERIVED FROM EACH
TARGET.** Measured at `1d344b48` by trailing-`\n` enumeration on the raw bytes:
`.agent/live_review.md` **937682** bytes ending in exactly ONE newline,
`.agent/decisions.md` **842038** in exactly ONE, `.agent/prose_slips.md`
**117457** in exactly ONE. The block is CORRECT for all three this round. Each
recipe was nonetheless derived from its own target's measured terminal byte, and
each append `assert`ed the count was 1 before writing — the assertion is IN the
scripts, so a wrong terminal byte would have aborted the write rather than
produced a bad append.

**9. THE STRUCTURAL READER COMPARES THE LAST UNIT WITH ONE TRAILING NEWLINE
REMOVED.** Splitting the whole file on `"\n\n"` makes the final unit
`FIND816 + b"\n"` (respectively `DEC_D7 + b"\n"`, `SLIP19 + b"\n"`), because the
file ends with a newline no `"\n\n"` consumes. The gate is therefore reported as
two separate printed facts: the last unit ends with EXACTLY ONE newline, AND it
equals the slice once that newline is removed. Neither is a hidden `strip`.

**10. `cmp` AND `remedy` ARE DENIED IN THIS SANDBOX (constraint 9).** C0a and C0b
were proved with `filecmp.cmp(shallow=False)` — a full byte comparison, not a
stat comparison — plus sha256 on both files against the delegation's digest.
`remedy` was invoked as `python3 -m apps.cli.grouped` and `ruff` as
`python3 -m ruff`. Every exit code in the Verification table came from a Python
`subprocess.run(...).returncode` written into a capture file under `.remedy-wt/`;
none came from `$?`, none from a shell loop, none from output text.

**11. G2(c)'s NEGATIVE CONTROLS RAN IN MEMORY, ONE PER FILE.** The flip and the
restore were done on `bytes` objects inside the checking process rather than by
writing a corrupted image to `.agent/live_review.md` or `.agent/decisions.md`, so
the primary checkout never held known-bad bytes — the block's own G2(c) wording
and self-drive guardrail G5. The property measured is identical and the restored
image was asserted equal to the disk image both times.

**Not a deviation, recorded because it was checked:**
`packages/orchestration/run_log.py` was NOT edited — its docstring was already
correct and this round makes the CALLER honour it; `new_run_id`, `RunLogWriter`'s
signature, its `path` and `run_id` properties, `log`, `append` and the event shape
are all untouched, and the run id stays a `str`. `load_run_events`,
`summarize_timeline` and every other function in `timeline.py` are unchanged
(SPEC 1's NOT-CHANGED list). `tests/test_run_log.py`, `tests/test_data_paths.py`,
`tests/test_patch_apply.py` and everything under `tests/orchestration/` were NOT
touched (constraint 6) — the first three are in the G6 selection as this round's
observers, and their 140-test control is what makes the red-proof readable. No
`Done:` or `Landed:` paragraph was authored for `R-0816` (constraint 5); that is
the reviewer's to write. `.agent/context.md` was not touched — it is not in the
block's change set. No file under `docs/` or `scripts/` was opened. The eleven
`remedy/job-*` worktrees pre-date this round and were neither created nor
removed; only `.remedy-wt/f260-r15-base` and `.remedy-wt/f260-r15-head` were
added, and both were removed BY EXACT PATH.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `shutil.copyfile`; `filecmp.cmp(shallow=False)` True + sha256 equals the delegation digest, checked before staging |
| C0b mirror the block | done | same source, same route, same two proofs |
| C1 PLAN slice | done | whole-file replacement; 2531 bytes, 48 lines, under the 50-line cap, `## Goal` and `## Next Steps` present |
| C2 GATE_R14 + FIND816 + DEC_D7 | done | ONE commit; live_review appended FIRST (both slices, in order), decisions SECOND |
| C3 SLIP18 + SLIP19 | done | units 148 → 150, in order, blank-line separated |
| C4 SPEC (1) + SPEC (2) | done | one module constant, one import added, one function-local import deleted, one construction changed; one new class with three tests |
| C5 handback | done | this file |
| G1 transport | done | exit 0; both digests equal the delegation's, ONE comparison, `filecmp` True for both |
| G2 the record | done | exit 0; (a) (b) (c) for BOTH files, negative controls reject and restore; (d) census **24 / 301 over 301 / 5 over 3 / OPEN 298**, exactly the expected post reading |
| G3 the prose files | done | exit 0; plan byte-equal at 48 lines, slips byte-equal at 148 → 150 units, zero marker lines in either |
| G4 the defect at the base | done | exit 0; run BEFORE C4 in a disposable worktree at `1d344b48`; **5 / 5 / 5**, matching the reviewer's reading |
| G5 the fix at the head | done | exit 0; **1 / 5 / 1** for one job, **1 file each** in two directories for two jobs |
| G6 mutation red-proof | **deviated** | exit 1 on the mutant, so the ORDERED COLOUR is met; the block's further clause that the failures include all THREE new tests is NOT met — only one of the three discriminates, by construction. Deviation 3. No test was adjusted. Control 140 passed before and after; worktree clean and removed by exact path |
| G7 the suites | done | exit 0 on all four; **264** / **12805 + 10 skipped** / **1537** / integrity `passed: true`; canary **42** collected; `^FAILED` and `^ERROR` both 0 for (2) and (3) |
| G8 lint and tree | **deviated** | lint exit 0, `All checks passed!` over the TWO code files I counted myself; `git ls-files .remedy-wt` EMPTY; but `git status --porcelain` shows `?? .agent/STOP`, an operator file created mid-round that is not mine to delete or commit. Deviation 4 |

## Open findings

**298** by DISTINCT ID, measured after C2: 301 registrations over 301 distinct
ids, minus 3 distinct ids carrying a `Done:` line. (The `^Done: ` LINE count is 5;
two findings were each resolved across two paragraphs, so a line-based formula
over-counts by two — the distinct-id reading is the correct one.) The base at
`1d344b48` was 297; this round REGISTERED exactly one finding, `R-0816`, and
resolved none, so 297 + 1 = 298. GATE_R14 is a `Gate:` record, not a registration,
which is why `^Gate: ` rose 23 → 24 without moving the open set. No `Done:` and no
`Landed:` paragraph was authored here.

## Next

**Rule order at session start is Phase 1 rule 1 BEFORE rule 2: re-read
`.agent/STOP` from disk first, then check for an open PR.** As of this handback
**`.agent/STOP` EXISTS** — zero bytes, untracked, created 10:20:01 during this
round. Under self-drive guardrail G6 and Phase 1 rule 1, the correct next action
is to **write nothing further and end the session**; no round may be authored
while it is present. There is no open PR for this branch and none may be created
without an instruction.

**If and only if the operator clears `.agent/STOP`: review round 15.** Read
`git diff 1d344b48..HEAD` bottom-up and re-run the eight gates independently.
Eleven deviations are declared; the two wanting a RULING rather than an
acknowledgement are **3** and **4**. Deviation 3 is G6's own further clause going
unmet while its ordered colour is met — the block asked for three discriminators
and SPEC (2) as written yields one, which is a fact about the block rather than
about the code, and the block itself says a green mutation would be "a finding
about this block and not about your work". Deviation 4 is the operator's stop file
making G8's tree reading unmeetable; nothing of mine is uncommitted. Deviations 1
and 2 are the block's placement anchors not existing on disk — checklist item 16's
shape — and in both cases I applied the evident intent and said so.

**Then: `Job.run_refs`**, the plural run list DECISION F260 D1 names and nothing on
disk carries yet. This round is its prerequisite and that is now measured rather
than argued: before it, a "run" was an EVENT (G4: five events, five runs, five
files), so a `run_refs` list built at `1d344b48` would have enumerated events
wearing the name of runs. After it, a run is an INVOCATION (G5: five events, one
run, one file), which is what `RunLogWriter`'s docstring has always promised and
what D7 rules.

**Then THE RE-KEY ITSELF**: `run_log_dir` and `pingpong_run_dir` collapse onto
`run_dir`, keyed by RUN id — DECISION F260 D1. It could not have gone first:
under the pre-round cardinality it would have created one DIRECTORY per event.
The reader side still needs a job to name its runs, so `run_refs` above remains
its prerequisite.

**The test-side sweep stays DECLINED, not forgotten** — DECISION F260 D6. The
re-key round inherits those sites and touches them once, and it must plan its own
red-proof carefully: this round's G6 could go red only because
`tests/test_timeline.py`, `tests/test_run_log.py` and `tests/test_data_paths.py`
still hand-spell `tmp_path / "runs" / str(job_id)`, and a round that sweeps them
consumes its own observer — round 12's finding, and the pre-sweep/post-sweep PAIR
is the shape that round will need.

**A KNOWN CONSEQUENCE THIS ROUND SHIPS, stated rather than hidden** (DECISION F260
D7 records it): a long-lived process — `ui_server.py` is the case — now keeps ONE
run id for its lifetime, so its events form one long run rather than many. That is
a strict improvement on one run per event and the same trade `BUDGET_TICK_RUN_ID`
already makes on the safe-point path; if a server ever needs a run per request,
the run id becomes a parameter of the request and this constant is its default.

After that, the rest of T002: the unified record's own administrative fields —
eight of D1's eleven have no counterpart in `JobPlan` — and the Mission extension.
Then T003 consumer by consumer; T004 the classic runner, the classic store and the
resolver collapse together (DECISION F260 D5); T005 the reachability test and the
cluster deletion.
