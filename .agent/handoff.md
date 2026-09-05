# Handback — F259 Vocabulary & concept model v1, round 6 (T004)

## Session

SESSION 1 of feature F259 · round 6 · rounds so far 6

Branch `feature/f259-vocabulary`, cut from `main` at `25961794`. Rounds 1-5 PASSED;
the round-5 verdict is booked into `.agent/live_review.md` by this round's C2, per
operator amendment amend0827-process-diet rule 1. Soft limit (25 rounds / 7
sessions) is far away.

Fortschritt: `~90 % (T001 ✅ · T002 ✅ · T003 ✅ · T004 ✅ · Integration Gate + Closure offen) — Schätzung`

Context self-assessment: context is comfortable — this round was byte work over
four small files with no retries, and further rounds of this size fit without a
session boundary.

Open findings: 299 registrations against 5 `Done:` lines in `.agent/live_review.md`
= **294 open**, unchanged this round. No new finding raised. Three reviewer prose
slips (SLIP5-SLIP7) appended to `.agent/prose_slips.md`, which spends no id
(amend0827-process-diet rule 2).

T004 is complete. F259's build work is done; only the integration gate and the
closure sequence remain.

## Range

Review of cc8834bf..549e39d9

## Commits

Seven commits, all single-parent, all pushed. The C6 commit that writes this file
cannot table itself (R-0149 pattern) and is listed last without its own numbers.

### 34215224 f259: save round 6 block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f259-r6.md | +344 -0 | C0a — the round's block saved by `shutil.copyfile`, never retyped |

### 1cde0bd7 f259: mirror round 6 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +268 -333 | C0b — same bytes mirrored to the last-block slot |

### 57ad83f7 f259: plan.md for round 6, T004
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 -20 | C1 — whole rewrite from the PLANF259R6 slice + one newline |

### 776d4711 f259: book the round 5 PASS verdict and three reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 -0 | C2 — `"\n" + GATE_R5 + "\n"` appended at end of file |
| .agent/prose_slips.md | +7 -1 | C2 — `"\n\n"+SLIP5+"\n\n"+SLIP6+"\n\n"+SLIP7`, still no trailing newline |

### 91fecaa4 f259: put the concept diagram into the README under the description
| Path | +/- | Reason |
|---|---|---|
| README.md | +10 -0 | C3 — the READMEBLOCK mermaid fence inserted between the description paragraph and `**Local-first.**` |

### 8972af01 f259: register the vocabulary page in the doc index tables
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +2 -0 | C4 — QUICKFIND and SYSTABLE rows for `system/vocabulary.md` |

### 549e39d9 f259: pin the README concept diagram byte-equal to the vocabulary page
| Path | +/- | Reason |
|---|---|---|
| tests/docs/test_vocabulary.py | +14 -0 | C5 — the `README` constant and one new test, written to the SPEC |

### C6 (this file)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | C6 — the round-6 handback; a handoff cannot table its own commit |

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f259-vocabulary` (after C5) | exit 0 — `cc8834bf..549e39d9  feature/f259-vocabulary -> feature/f259-vocabulary` |
| `git worktree add --detach .remedy-wt/f259-r6-redproof 549e39d9` | exit 0 — G6's disposable worktree |
| `git worktree remove --force .remedy-wt/f259-r6-redproof` | exit 0 |
| `git worktree prune` | exit 0 |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | exit 0 — `[]` |
| PR create / edit / merge | **None.** No pull request was created; F259's PR belongs to its closure round. |
| `git push` (after C6) | run after this file is committed; its result is not reported here, because C6 may report no reading that only exists after it is pushed |

## Verification

One line per ordered gate, each executed, with its real reading.

**G1 TRANSPORT — PASS.** `sha256sum` over the three paths, one digest three times:
`96a4ddf9376d64a0d722251ccab71d27482c098644ae82a87194c1f96224f44e` for
`.remedy-wt/f259-r6-block.md`, `.agent/authored/f259-r6.md` and
`.agent/last_block.md`, all 28 255 bytes. Copy chain, never a retype.

**G2 THE README INSERTION — PASS.** Anchor count BEFORE = 1, AFTER = 0. README
13 893 → 14 219 bytes (delta 326 = len(READMEBLOCK) 324 + the two added newlines),
still ending in exactly one newline. Reconstruction
`before.replace(ANCHOR, REPLACEMENT, 1) == disk` → **True**: nothing else in the
file differs. Mermaid body digests, under the block's stated convention (the bytes
between the opening fence's newline and the newline before the closing fence), all
309 bytes / seven lines:
`README.md` → `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`;
`docs/system/vocabulary.md` → same; `docs/roadmap/features/T2_F259.md` → same;
each equals the block's pin. The U+00B7 MIDDLE DOT and the four-space indentation
landed unchanged (bytes were extracted and written; no re-indent, no normalisation).

**G3 THE INDEX PAIRS — PASS.**
QUICKFIND: FROM count before = 1; `TO contains FROM: true` → **APPEND**; FROM count
after = 1; the new row `| vocabulary | [vocabulary.md](system/vocabulary.md) | system |`
occurs 1× among the lines `git show 8972af01` reports as ADDED.
SYSTABLE: FROM count before = 1; `TO contains FROM: true` → **APPEND**; FROM count
after = 1; the new `| [vocabulary.md](system/vocabulary.md) | The binding vocabulary: … |`
row occurs 1× among the ADDED lines.
`git show --numstat 8972af01` → `2  0  docs/README.md`; 2 added lines, 0 removed.
`docs/README.md` contains `system/vocabulary.md` exactly **2×**. Reconstruction:
post-commit bytes == pre-commit bytes with exactly those two replacements applied →
**True**; 21 616 → 21 946 bytes, still one trailing newline. Both rows land in sorted
position (between `UI` and `watchdog`; between `token-economy-…` and `worker.md`).

**G4 THE GUARDED README REGION (finding R-0797's binding clause) — PASS.** Extracted
after C3 with the guard test's own paragraph convention
(`Accepted[^\n]*:\n((?:[^\n]+\n)+)`): 5 `Accepted…:` blocks in the file, of which
**4** are `Accepted in Tier N so far:` blocks — Tier 1, Tier 2, Tier 3, Tier 5 — and
they carry **31 distinct `F\d{3}` tokens**. Full sorted list, each with its
`docs/roadmap/STATUS.md` `- [x]` status:

     1 F008  STATUS '- [x]': True      17 F052  STATUS '- [x]': True
     2 F009  STATUS '- [x]': True      18 F053  STATUS '- [x]': True
     3 F013  STATUS '- [x]': True      19 F086  STATUS '- [x]': True
     4 F014  STATUS '- [x]': True      20 F103  STATUS '- [x]': True
     5 F016  STATUS '- [x]': True      21 F104  STATUS '- [x]': True
     6 F021  STATUS '- [x]': True      22 F105  STATUS '- [x]': True
     7 F022  STATUS '- [x]': True      23 F106  STATUS '- [x]': True
     8 F031  STATUS '- [x]': True      24 F107  STATUS '- [x]': True
     9 F032  STATUS '- [x]': True      25 F251  STATUS '- [x]': True
    10 F034  STATUS '- [x]': True      26 F252  STATUS '- [x]': True
    11 F037  STATUS '- [x]': True      27 F254  STATUS '- [x]': True
    12 F046  STATUS '- [x]': True      28 F255  STATUS '- [x]': True
    13 F047  STATUS '- [x]': True      29 F256  STATUS '- [x]': True
    14 F048  STATUS '- [x]': True      30 F257  STATUS '- [x]': True
    15 F050  STATUS '- [x]': True      31 F262  STATUS '- [x]': True
    16 F051  STATUS '- [x]': True

Thirty-one tokens enumerated, thirty-one rows above; `every token is [x] in
STATUS.md: True`. No token is reported as a summary count alone.

Those blocks' BYTES are identical before and after C3: 4 510 bytes both times,
sha256 `3841a684b692dc330c60e221051e723a0cc0fff1520d8b3fcda2ada55c1e3824` before and
after. The round's README slice contains no `F\d{3}` token at all.
`python3 -m pytest tests/docs/test_docs_consistency.py -q` → exit **0**, **295 passed**.

**G5 THE TEST IS GREEN AND THE DOCS SUITE GREW BY ONE — PASS.**
`python3 -m pytest tests/docs/test_vocabulary.py -q` → exit **0**, **8 passed**
(7 at cc8834bf + the one test this round adds).
`python3 -m pytest tests/docs/ -q` → exit **0**, **303 passed**.
Arithmetic against the number the first command reported: 302 at cc8834bf, and
test_vocabulary.py moved 7 → 8, so 302 + (8 − 7) = **303**. Measured 303. Exact.

**G6 THE RED PROOF — PASS.** Full transcript in its own section below. Control exit
0 / 8 passed; mutated exit 1 / 1 failed 7 passed with only
`tests/docs/test_vocabulary.py::test_the_readmes_mermaid_block_is_byte_equal_to_the_pages`
failing; restored control exit 0 / 8 passed. Whole-`tests/docs/` runs in each stage:
303 / 302+1 / 303 — so no test other than the new pin moved.

**G7 THE RECORD, THE SLIPS AND THE SUITES — PASS.**
`.agent/live_review.md`: 834 169 → 839 318 bytes; pre-append bytes are a byte-exact
PREFIX of the post-append bytes → True; the 5 149-byte remainder equals exactly
`"\n" + GATE_R5 + "\n"` → True; `grep -c '^Gate: R5 — ' .agent/live_review.md` went
**0 → 1**.
`.agent/prose_slips.md`: 79 043 → 82 415 bytes; prefix property → True; the
3 372-byte remainder equals exactly `"\n\n"+SLIP5+"\n\n"+SLIP6+"\n\n"+SLIP7` → True;
the file still does **not** end with a newline (last 20 bytes
`b'rocess-diet rule 2).'`).
The six suites, run serially at C5, real exit codes:

| Suite | Exit | Passed | Expected |
|---|---|---|---|
| `tests/orchestration/test_roadmap_index.py` | 0 | 30 | 30 ✅ |
| `tests/ui_server/` | 0 | 515 | 515 ✅ |
| `tests/orchestration/test_test_runner.py` | 0 | 52 | 52 ✅ |
| `tests/regression/test_resource_safety.py` | 0 | 21 | 21 ✅ |
| `tests/orchestration/test_integrity_gate.py` | 0 | 16 | 16 ✅ |
| `tests/cli/test_golden_path.py` | 0 | 42 | 42 ✅ |

No failing node ids anywhere. `tests/docs/` is covered by G4 and G5 and was not
repeated here.

**G8 THE PLAN AND THE STRUCTURE — PASS.** `wc -l .agent/plan.md` = **42**, under 50.
`## Goal` count = 1, `## Next Steps` count = 1.
`filecmp.cmp('.agent/plan.md', PLANF259R6 + '\n', shallow=False)` → **True**
(slice 2 082 bytes, sha `58ee5f4d93b46fbb062b558aeb3db4c4f63b0bab48985887b951e4e21c0df6e2`;
file 2 083 bytes, exactly one trailing newline).
`python3 -m py_compile tests/docs/test_vocabulary.py` → exit **0** (silent).
`ruff check tests/docs/test_vocabulary.py` → **REFUSED by this session's permission
layer**, verbatim: `Permission to use Bash has been denied. IMPORTANT: You *may*
attempt to accomplish this action using other tools that might naturally be used to
accomplish this goal, e.g. using head instead of cat. But you *should not* attempt
to work around this denial in malicious ways…` — the same denial round 5 measured;
`py_compile` was run either way, as constraint 8 requires.
`git status --porcelain` immediately before C6 was staged → **empty**.
`git ls-files .remedy-wt` → **empty** (the scratch dir is gitignored, `.gitignore`
line 235).
Every commit single-parent; per-commit `git diff --numstat <parent> <commit>`:

| Commit | Path | + | − | Insertions vs 500 cap |
|---|---|---:|---:|---|
| 34215224 | .agent/authored/f259-r6.md | 344 | 0 | 344 OK |
| 1cde0bd7 | .agent/last_block.md | 268 | 333 | 268 OK |
| 57ad83f7 | .agent/plan.md | 20 | 20 | 20 OK |
| 776d4711 | .agent/live_review.md | 2 | 0 | 9 OK (both files) |
| 776d4711 | .agent/prose_slips.md | 7 | 1 | — |
| 91fecaa4 | README.md | 10 | 0 | 10 OK |
| 8972af01 | docs/README.md | 2 | 0 | 2 OK |
| 549e39d9 | tests/docs/test_vocabulary.py | 14 | 0 | 14 OK |

No commit approaches the 500-insertion cap. Push after C5: exit 0,
`cc8834bf..549e39d9`. `origin/feature/f259-vocabulary` = `549e39d9`.
**No pull request was created**, and `gh pr list --state open` returns `[]`.

`.agent/STOP` was read from disk before C0a, before C3 and before C6 — absent all
three times.

## G6 — full red-proof transcript

Guardrail G5 / block constraint 6: destructive verification ran ONLY inside a
disposable worktree created from this branch's head; the primary checkout was never
mutated.

    === G6 RED PROOF — disposable worktree at 549e39d930d3543f1b3064266a21d023bfd26e9b ===
    git worktree add --detach .remedy-wt/f259-r6-redproof 549e39d9 -> exit 0
    Preparing worktree (detached HEAD 549e39d9)
    HEAD is now at 549e39d9 f259: pin the README concept diagram byte-equal to the vocabulary page
    worktree README.md: 14219 bytes, sha 079d47c8b38530e0d61f3df691e4c782269a5142a197b720a6dcb84eb7ef101b

    --- RUN 1: UNMUTATED CONTROL ---
      __pycache__ dirs purged under the worktree: 0
      worktree self-reading probe (exit 0):
      apps.cli.command_catalog.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/apps/cli/command_catalog.py
      test module REPO           = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      test module README         = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/README.md
    [control] python3 -B -m pytest, cwd=/home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      tests/docs/test_vocabulary.py: exit 0 | 8 passed in 0.26s
      tests/docs/ (whole suite): exit 0 | 303 passed in 0.65s

    --- RUN 2: MUTATION (worktree README.md only) ---
      exact byte changed: offset 505 in the worktree's README.md; 0x6e ('n') -> 0x4e ('N')
      line BEFORE:     Job --> Task["Task 1..n"]
      line AFTER :     Job --> Task["Task 1..N"]
      worktree README.md now: 14219 bytes, sha 6f851933bb04b66dec9d900d53276471d9cf2e8419fd035917513f39109771ad
      __pycache__ dirs purged under the worktree: 0
      worktree self-reading probe (exit 0):
      apps.cli.command_catalog.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/apps/cli/command_catalog.py
      test module REPO           = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      test module README         = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/README.md
    [mutated] python3 -B -m pytest, cwd=/home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      tests/docs/test_vocabulary.py: exit 1 | 1 failed, 7 passed in 0.28s
          failing node id: FAILED tests/docs/test_vocabulary.py::test_the_readmes_mermaid_block_is_byte_equal_to_the_pages
      tests/docs/ (whole suite): exit 1 | 1 failed, 302 passed in 0.79s
          failing node id: FAILED tests/docs/test_vocabulary.py::test_the_readmes_mermaid_block_is_byte_equal_to_the_pages

    --- RUN 3: RESTORED CONTROL ---
      worktree README.md byte-identical to before the mutation: True | sha 079d47c8b38530e0d61f3df691e4c782269a5142a197b720a6dcb84eb7ef101b
      __pycache__ dirs purged under the worktree: 0
      worktree self-reading probe (exit 0):
      apps.cli.command_catalog.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/apps/cli/command_catalog.py
      test module REPO           = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      test module README         = /home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof/README.md
    [restored] python3 -B -m pytest, cwd=/home/decodeux/Repos/remedy/.remedy-wt/f259-r6-redproof
      tests/docs/test_vocabulary.py: exit 0 | 8 passed in 0.22s
      tests/docs/ (whole suite): exit 0 | 303 passed in 0.70s

    --- TEARDOWN ---
    git worktree remove -> exit 0
    git worktree prune -> exit 0
    scratch worktree path still exists on disk: False
    git worktree list -> exit 0
    /home/decodeux/Repos/remedy                                  549e39d9 [feature/f259-vocabulary]
    /home/decodeux/Repos/remedy/.remedy-wt/job-21c19578b8754287  79a73b5a [remedy/job-21c19578b8754287]
    /home/decodeux/Repos/remedy/.remedy-wt/job-2ac1522a7034440b  3afc78c5 [remedy/job-2ac1522a7034440b]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-6f74dd7367704fd5  cf0e00e9 [remedy/job-6f74dd7367704fd5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-848fc4c67d7b405b  7bea3efc [remedy/job-848fc4c67d7b405b]
    /home/decodeux/Repos/remedy/.remedy-wt/job-962cb3c9b96244ed  05852956 [remedy/job-962cb3c9b96244ed]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]
    primary git status --porcelain -> exit 0 | output: ''

The scratch worktree is gone; the ten pre-existing `remedy/job-*` worktrees are
untouched. Every run resolved `apps.cli.command_catalog` and the test module's
`REPO`/`README` to the WORKTREE's own copies — the editable-install shadow that
would have made the proof measure the wrong tree is excluded.

## Authored-text proofs

Every slice was extracted BY MARKER, in bytes, from the COMMITTED
`.agent/authored/f259-r6.md`, never retyped, and applied verbatim.

| Slice | Applied to | Proof |
|---|---|---|
| PLANF259R6 | .agent/plan.md | `filecmp.cmp(shallow=False)` against slice + one newline → **True**; slice sha `58ee5f4d…`, 2 082 B |
| GATE_R5 | .agent/live_review.md | post == pre + `"\n" + slice + "\n"`, byte-exact → **True** |
| SLIP5 / SLIP6 / SLIP7 | .agent/prose_slips.md | post == pre + `"\n\n"+S5+"\n\n"+S6+"\n\n"+S7`, byte-exact → **True**, no trailing newline |
| READMEBLOCK | README.md | reconstruction `before.replace(ANCHOR, REPLACEMENT, 1) == disk` → **True**; slice sha `fe7e6186…`, 324 B; body sha `6f6d59ee…` equals the page's and the feature file's |
| QUICKFIND_FROM/TO, SYSTABLE_FROM/TO | docs/README.md | reconstruction with exactly the two `str.replace(FROM, TO, 1)` → **True** |
| (none) | tests/docs/test_vocabulary.py | production code, written by the worker to the SPEC; no slice was shipped for it |

Transport digest, one value across all three paths:
`96a4ddf9376d64a0d722251ccab71d27482c098644ae82a87194c1f96224f44e`.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f259-r6.md` — `shutil.copyfile`, digest verified equal |
| C0b | done | `.agent/last_block.md` — same bytes |
| C1 | done | `.agent/plan.md` rewritten whole from PLANF259R6 + one newline, 42 lines |
| C2 | done | GATE_R5 appended to the record; SLIP5-SLIP7 appended to the slips; one commit |
| C3 | done | READMEBLOCK inserted at the single anchor; anchor 1 → 0 |
| C4 | done | both index pairs applied, both APPEND-shaped, both FROM surviving 1× |
| C5 | done | `README` constant + `test_the_readmes_mermaid_block_is_byte_equal_to_the_pages`, reusing `_mermaid_body`; pushed |
| C6 | done | this file, one commit; no post-push-only reading claimed |

No item was skipped. No item deviated from its ordered position; the bundle ran
C0a → C0b → C1 → C2 → C3 → C4 → C5 → push → gates → C6 exactly as ordered, with no
extra, dropped or reordered commit.

## Deviations & assumptions

1. **Two shell FORMS were refused, as constraint 7 predicted; no gate was dropped or
   narrowed.** `python3 .remedy-wt/r6s/c1.py; echo "exit=$?"; wc -l .agent/plan.md`
   and `python3 -m pytest … > file 2>&1; echo $?` were both refused with
   `Permission to use Bash has been denied. …` — the `$?`-in-a-compound-command form.
   Both were re-expressed in Python: `.remedy-wt/r6s/suites.py` runs each pytest
   target through `subprocess.run` and prints `p.returncode`, so every exit code in
   this handback is a REAL measured code, not an inferred one. The Python is on disk
   under the gitignored `.remedy-wt/r6s/` and the output is quoted above.
2. **`ruff check` is denied to the worker as well as to the reviewer.** Attempted on
   `tests/docs/test_vocabulary.py` per constraint 8; the refusal is quoted verbatim
   in G8. `python3 -m py_compile tests/docs/test_vocabulary.py` was run either way
   and exits 0. This confirms what round 5 measured and is not new.
3. **The block's G2 body pin is exact, but it is convention-sensitive — read this
   before re-measuring.** Under the block's own stated convention ("the bytes between
   the opening fence's newline and the newline before the closing fence", i.e.
   EXCLUDING that final newline) the body is 309 bytes, seven lines, sha
   `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c` — exactly as
   the block states, in all three files. Under the SHIPPED `_mermaid_body` helper's
   convention, whose regex `^```mermaid\n(.*?)^``` ` captures the trailing newline,
   the same body reads 310 bytes and sha
   `1da6e9ee983e53b252f5982dc0449dea1473a15b8c028b4e3d1fe42677b0a716`. Both readings
   are reported so a re-measurement that lands on 310 is not mistaken for drift. No
   discrepancy exists in the bytes: README, the page and the feature file are
   byte-identical under either convention.
4. **The SYSTABLE row carries `F260/F261` tokens, and this is in scope.** Constraint
   11 forbids an `F\d{3}` token in a slice bound for `README.md`; this slice is bound
   for `docs/README.md`, which the R-0797 guard test does not scan — it reads
   `REPO / "README.md"` only. Verified two ways: G4 shows README's guarded blocks
   byte-identical before and after, and `tests/docs/test_docs_consistency.py` passes
   at 295. No `F\d{3}` token entered `README.md` this round.
5. **No pull request was created**, as ordered. F259's PR belongs to its closure
   round. No `--force`, no `--force-with-lease`, no history rewrite, no branch
   deletion, no `gh pr merge`.
6. **Scratch scripts left in place.** The Python re-expressions and byte snapshots
   live under `.remedy-wt/r6s/`, which is gitignored (`git ls-files .remedy-wt` is
   empty). They are left on disk deliberately so the reviewer can re-run them; they
   are not deleted by glob (memory rule: clean up by exact path only).

## Next

The reviewer's gate on cc8834bf..549e39d9 — then, on PASS, the **integration gate
round** per `docs/agents/integration_gate.md` (the full suite against this branch, a
regression there being a normal repair round), and after that the **closure
sequence** per `docs/roadmap/STATUS_closure_protocol.md`: the evidence job, a FRESH
review zip, the ledger rotation before the STATUS flip (amend0905-throughput), the
reviewer-authored STATUS line committed last, and the pull request — created but NOT
merged in this session; it merges at the next feature's Open PR Gate.

Phase 1 rule 1 first at the next session start: read `.agent/STOP` from disk before
anything else.
