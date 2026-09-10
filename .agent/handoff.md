# Handoff — F275 One world completion, part three — ROUND 27

## Session

SESSION 14 of feature F275 · round 27 · rounds so far 27

Context self-assessment (amend0905-throughput): the worker context for this round stayed
comfortable — one block, ten pairs, one described production change, two appends, eight
gates. The wall clock was dominated by one thing only, G8's suite at 255 seconds, because
this round is the first of the session to touch `packages/` and `tests/`. Nothing in the
round argues for ending the session.

Soft-limit note (amend0908-f275-finish): F275's limit is 20 sessions and 60 rounds, by
operator order and by name. At session 14 and round 27 the feature is inside both.

## Range

Review of `c370dcee`..`6335babf`, plus the C5 handback commit that writes this file and
whose SHA cannot exist while it is being written (R-0149 pattern).

## Commits

### 4ba30f28 F275 R27 C0a: save the round 27 block verbatim as the authored original.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r27.md` | +421 / -0 | the round 27 block, copied with `shutil.copyfile` from `.remedy-wt/f275-r27-block.md`, never retyped |

### c2a5dca7 F275 R27 C0b: mirror the committed round 27 block into the working copy.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +390 / -275 | the bytes of the COMMITTED C0a blob, read with `git show 4ba30f28:.agent/authored/f275-r27.md`, not from the working copy |

### 8fe426b3 F275 R27 C1: point the plan at the advertisement-guard widening.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21 / -18 | rewritten byte-identical to the PLAN27 slice as extracted from the committed C0a blob |

### f4390b10 F275 R27 C2: book the round 26 PASS verdict, add the R-0847 evidence note, register R-0872 and resolve R-0847, record three prose slips.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | LEDGER27 appended: the round 26 `Gate:` verdict, `Note: F275 R27`, the `- R-0872` registration, `Done: R-0847` |
| `.agent/prose_slips.md` | +6 / -0 | SLIPS27 appended: session 13's three dated lines |

### 088e7e7d F275 R27 C3: repair the R-0843 banner residue - drop the invented catalog command and state the span the section really covers.
| Path | +/- | Reason |
|---|---|---|
| `docs/system/architecture.md` | +16 / -12 | pairs U1 and U2, applied byte for byte from the committed block blob |

### 3225d876 F275 R27 C4: widen the advertisement scanner past the group pre-filter, the single-token form and the backtick tail, and repair the eight dead next-action strings it exposes, completing R-0847.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_advertised_commands.py` | +183 / -26 | SPEC-GUARD (a) to (j): backtick tail, single-token regex, one shared tail helper, no `GROUPS` pre-filter, `_resolves`, `UnresolvedAdvertisement` records keyed without the line number, the generated 43-entry `KNOWN_DEAD_DOC_ADVERTISEMENTS`, the subtracting operator-facing assert and the new ratchet test |
| `packages/orchestration/brain_detail.py` | +5 / -5 | pairs P4, P5, P6, P7, P8 |
| `packages/orchestration/cockpit.py` | +2 / -2 | pairs P1 and P2 |
| `packages/orchestration/trust_report.py` | +1 / -1 | pair P3 |

### 6335babf F275 R27 C4b: pin the allowlist ceiling to its measured literal so the ratchet assertion can fail.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_advertised_commands.py` | +5 / -2 | UNORDERED EXTRA COMMIT, declared below: `_ALLOWLIST_CEILING = len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` as first written could never fail, so it became the measured literal `43` |

### (C5) F275 R27 C5: the round 27 handback.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | the round 27 handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add .remedy-wt/r27-g6 6335babf` — created, detached HEAD at C4b, for G6 only.
- `git worktree remove .remedy-wt/r27-g6 --force` then `git worktree prune` — removed;
  `git worktree list` afterwards holds exactly ONE entry.
- `git push -u origin feature/f275-one-world-completion-part-three` — pushed at the end of
  the round.
- NO pull request created, NO PR edited, NO merge. F275's closure sequence is not this round.

## Verification

Every gate run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. One line per gate.

- **G1 TRANSPORT (at C0b)** — REAL_EXIT=0. `sha256sum` over the scratch original
  `.remedy-wt/f275-r27-block.md`, the committed `.agent/authored/f275-r27.md` and the
  committed `.agent/last_block.md` is ONE comparison and reads
  `08809a29128b5f02856eb00f26cc40499d51f9df3c0ca53dfdd427b369ea2078` for all three, each
  39740 bytes / 421 lines. This covers the SAVED COPY, its MIRROR and the WORKING COPY and
  NOT the emitted bytes (§3 item 37).
- **G2 THE PLAN (at C1)** — REAL_EXIT=0. `written == slice: True`, 2476 bytes,
  sha256 `6f03426f137c1b4359ea80a03d3a9ef366b0b6e247b2c0b6fcfcb567841601d0`, 44 lines
  against the AGENTS.md cap of 50; `grep -c '^## Goal$'` = 1, `grep -c '^## Next Steps$'` = 1.
- **G3 THE RECORD (at C2)** — REAL_EXIT=0. `.agent/live_review.md` pre 755015 → post 767596,
  `post == pre + NL + slice: True`, joining byte read back from the COMMITTED post-blob at
  offset 755015 = `b'\n'`, N counted by the script from the slice = 4, last-4 blank-line
  units match the slice's 4 paragraphs in order: True; negative control flipping one byte at
  offset 755026 inside the FIRST appended paragraph → byte reader False AND structural reader
  False. `.agent/prose_slips.md` pre 211596 → post 213983, same three readings True /
  `b'\n'` @211596 / N=3 / True, negative control @211607 → both readers False. Whole-post-file
  counts: `^Gate: F275 R26 ` = 1, `^Note: F275 R27 ` = 1, `^- R-0872 — ` = 1,
  `^Done: R-0847 — ` = 1. OPEN SET BY DISTINCT ID = **88** — 101 registration lines / 101
  distinct ids minus 15 `Done:` LINES / **13 DISTINCT** resolved ids; resolutions naming an
  unregistered id: none; ids carrying more than one `Done:` line: `R-0721`, `R-0725`, the
  landed state this round does not touch. 88 at the base and 88 after registering one and
  resolving one, as the block predicted.
- **G4 THE DOC PAIR (at C3)** — REAL_EXIT=0. U1 FROM 1 → 0 and TO 0 → 1; U2 FROM 1 → 0 and
  TO 0 → 1, measured before and after the write. As extracted from the committed block blob:
  U1 FROM 774 bytes `5d8888bbca907e44186d980a52518ace44ed9a6212d2ff44a11d49ba53da7ef2`, U1 TO
  945 bytes `3d81fc9fb79e3af1913050483d96c6a572259e00cd86f2584e67bcd3d8a397af`, U2 FROM 306
  bytes `2688ef8af6b24a3c648da9c3233a71e152fb41a60f5dab624009431597460bda`, U2 TO 426 bytes
  `21461f9a3a1cf9ee97c2b459b33e5cc3a852bbb2bc8f074bc09984b5cd96e6ff`. TWO readings of the
  invented command: (a) the BACKTICK-DELIMITED form 1 at `c370dcee` → **0** after C3;
  (b) the RAW substring 3 at `c370dcee` → **2** after C3, printed with line numbers — line
  675 `remedy list-patch-intents` and line 1897 `remedy list-projects`, both flat
  pre-Step-38 commands that merely begin with the same eleven characters and both R-0872's.
  `Steps 38 to 43` 1 → **0** over the whole file. `## Group-first CLI v0 (Steps 38–40)` at
  line **2908**, file total **3076** lines (3072 at the base plus U1's +2 and U2's +2), and
  the first `> ` after that heading is separated from it by exactly one blank line
  (line 2909 = `''`, line 2910 = the banner).
- **G5 THE GUARD (at C4)** — REAL_EXIT=0, through the worker's own `import` of the edited
  module under `python3 -B` with `__pycache__` purged, not by grep. PRODUCTION sweep
  **seen=542, unresolved=0**, `seen > 100` True. OPERATOR-FACING sweep **seen=417,
  unresolved=68 sites over 43 DISTINCT keys across 7 paths**.
  `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` = 43 and `_ALLOWLIST_CEILING` = 43, EQUAL. Allowlist
  digest over the sorted keys joined as `f"{path}\t{invocation}"`, `\n`-separated, no
  trailing newline = `364eb51c60942c14da584ce3a822a555b737c36cf54b5027d13f03586dcd64c0`,
  the value the block ordered. `python3 -m pytest tests/cli/test_advertised_commands.py -q`
  → **6 passed**, REAL_EXIT=0.
- **G6 THE RED PROOFS (after C4, inside `.remedy-wt/r27-g6`, a disposable worktree at
  `6335babf`)** — REAL_EXIT=0 for the driver; every mutation reverted byte-exactly before
  the next; `__pycache__` purged and `python3 -B -p no:cacheprovider` on every run.
  CONTROL first: whole guard file exit=0, **6 passed**. M1 (restore `, or run `remedy list`,`
  into the U1 TO sentence in `docs/system/architecture.md`) → operator-facing test **exit=1,
  1 failed** — RED. M2 (restore P1's FROM in `packages/orchestration/cockpit.py`) →
  production test **exit=1, 1 failed** — RED. M3 (add one entry to
  `KNOWN_DEAD_DOC_ADVERTISEMENTS`) → ratchet test **exit=1, 1 failed** — RED, first assertion
  `the known-dead advertisement list GREW`, i.e. ON THE CEILING as ordered. M4 (add an
  allowlist entry naming an advertisement that does NOT occur) → ratchet test **exit=1,
  1 failed** — RED, but the first assertion is again `the known-dead advertisement list
  GREW`: the CEILING, not staleness — see deviation 2. M4b, ADDED by the worker as the
  discriminator M4 as written cannot be (it SWAPS one entry for a non-occurring one so the
  count stays 43) → ratchet test **exit=1, 1 failed** — RED, first assertion `the known-dead
  advertisement list excuses advertisements that are no longer there`, i.e. ON STALENESS.
  CONTROL re-run: exit=0, **6 passed**; `architecture.md`, `cockpit.py` and
  `test_advertised_commands.py` each restored BYTE-EXACTLY (True, True, True) against bytes
  captured before the first mutation. No mutation came back green.
- **G7 THE PRODUCTION PAIRS (at C4)** — REAL_EXIT=0. P1..P8 each **FROM 1 → 0 and TO 0 → 1**,
  measured before and after the write, FROM/TO texts parsed out of the committed block blob
  and never retyped. Through the SHIPPED dispatcher, in process, with NO `--help`:
  `remedy brain timeline` exit=2 first line `Usage: remedy brain timeline JOB_ID`;
  `remedy dev agent-loop` exit=2 `Usage: remedy dev agent-loop JOB_ID`;
  `remedy brain constitution` exit=2 `Usage: remedy brain constitution JOB_ID`;
  `remedy worker list` exit=**0** `Worker Adapters`. CONTROL `remedy timeline` exit=2 first
  line `Usage: remedy [OPTIONS] COMMAND [ARGS]...` — the PARENT's usage line, never its own.
  Each replacement therefore prints its own command or succeeds and the control does not.
  `python3 -m ruff check` over the four edited Python files → `All checks passed!`, REAL_EXIT=0.
- **G8 NOTHING ELSE MOVED (at C4b, before C5)** — REAL_EXIT=0.
  `python3 -m pytest tests/docs/ tests/cli/ tests/test_timeline.py
  tests/test_project_constitution.py tests/test_agent_loop.py tests/test_cockpit.py
  tests/test_trust_report.py tests/test_brain_detail.py -q` → **2024 passed, 0 failed**,
  255.42s, run SERIALLY. The canary `tests/cli/test_golden_path.py` is INSIDE `tests/cli/`
  and collects **42 tests**, so it is inside that figure. Through the shipped reader
  `apps.cli.command_catalog`: `len(_BASE_CATALOG)` = **222**, `len(GROUPS)` = **44**,
  dangling `related=` references = **0** — all three unchanged from `c370dcee`, correct for
  a round that adds and deletes no command. `.agent/STOP` ABSENT from disk (checked before
  the first commit, again before C4, and here); `git status --porcelain` EMPTY;
  `git worktree list` exactly ONE entry; branch
  `feature/f275-one-world-completion-part-three`. `git diff --name-only c370dcee..6335babf`
  is an EXACT SET MATCH against the change set minus `.agent/handoff.md` — MISSING: none;
  EXTRA: none; the ten paths are `.agent/authored/f275-r27.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
  `docs/system/architecture.md`, `packages/orchestration/brain_detail.py`,
  `packages/orchestration/cockpit.py`, `packages/orchestration/trust_report.py`,
  `tests/cli/test_advertised_commands.py`. Per-commit insertions before the handback commit,
  each against the AGENTS.md DECISION F104 D1 cap of 500: C0a 421, C0b 390, C1 21, C2 14,
  C3 16, C4 191, C4b 5. None oversize.

## Authored-text proofs

Every applied text was extracted from the COMMITTED C0a blob
`4ba30f28:.agent/authored/f275-r27.md` by a marker-delimited reader, never retyped, and no
`<<<BEGIN ...>>>` / `<<<END ...>>>` marker line reached any target file.

| Text | Bytes | sha256 | Disk-to-disk result |
|---|---|---|---|
| PLAN27 | 2476 | `6f03426f137c1b4359ea80a03d3a9ef366b0b6e247b2c0b6fcfcb567841601d0` | `.agent/plan.md` compares BYTE-EQUAL to the slice (G2) |
| LEDGER27 | 12580 | `392d1f26002c3d35127d263059ddfa461160d14355a138947fabfe87f08f24e5` | committed post-blob == pre + `\n` + slice (G3) |
| SLIPS27 | 2386 | `e23426031719d72bf993a41ac54f72ba719c4663bb23153ea4fd4100e695a9cf` | committed post-blob == pre + `\n` + slice (G3) |
| U1 FROM | 774 | `5d8888bbca907e44186d980a52518ace44ed9a6212d2ff44a11d49ba53da7ef2` | 1 → 0 occurrences (G4) |
| U1 TO | 945 | `3d81fc9fb79e3af1913050483d96c6a572259e00cd86f2584e67bcd3d8a397af` | 0 → 1 occurrences (G4) |
| U2 FROM | 306 | `2688ef8af6b24a3c648da9c3233a71e152fb41a60f5dab624009431597460bda` | 1 → 0 occurrences (G4) |
| U2 TO | 426 | `21461f9a3a1cf9ee97c2b459b33e5cc3a852bbb2bc8f074bc09984b5cd96e6ff` | 0 → 1 occurrences (G4) |
| P1..P8 FROM/TO | inline | parsed from the same blob | each FROM 1 → 0 and each TO 0 → 1 (G7) |

Pair-shape readings, one per pair, from the worker's own mechanical containment test:
`TO contains FROM: false` for U1, U2, P1, P2, P3, P4, P5, P6, P7 and P8 — ten REWRITES,
matching constraint 3 exactly. No append-shaped pair was ordered and none was applied.

## Deviations & assumptions

1. **AN EXTRA, UNORDERED COMMIT: `6335babf` "C4b".** The block's ordered sequence is C0a,
   C0b, C1, C2, C3, C4, C5 and this round has EIGHT commits, not seven. SPEC-GUARD (g) says
   "`_ALLOWLIST_CEILING` is its measured length"; I first wrote that as
   `_ALLOWLIST_CEILING = len(KNOWN_DEAD_DOC_ADVERTISEMENTS)`, committed it in C4, and then,
   preparing G6, saw that it makes the ceiling assertion UNFAILABLE — adding an entry raises
   `len` and the ceiling together, so `len(...) <= _ALLOWLIST_CEILING` is true by
   construction and G6's M3 could never go red on it. That is precisely the "gate that
   cannot fail" class this repository treats as a finding, so the ceiling became the
   measured LITERAL `43`. I did NOT amend `3225d876`: guardrail G2 forbids a history
   rewrite without qualification, so the repair is a new commit and this paragraph is its
   declaration. Both readings are in the record above — C4 and C4b — and G5 through G8 were
   run against the C4b state.
2. **G6's M4 DOES NOT PROVE WHAT IT NAMES, AND I RAN AN EXTRA MUTATION SO SOMETHING DOES.**
   M4 as written is "add an allowlist entry naming an advertisement that does NOT occur →
   the ratchet test must go RED on staleness". With the ceiling pinned at 43, ADDING any
   entry makes the count 44 and the CEILING assertion — which SPEC-GUARD (i) lists first —
   fires before the staleness assertion is reached. I ran M4 exactly as ordered and report
   its real first assertion (`the known-dead advertisement list GREW`, the ceiling), and
   then ran M4b, which SWAPS an entry for a non-occurring one so the count stays 43; M4b
   fires the staleness assertion by name. The two ordered mutations M3 and M4 cannot both
   discriminate under any assertion ordering: every live unresolved key is ALREADY in the
   43-entry allowlist, so no addition can be a key that occurs, which means with staleness
   first M3 would hit staleness instead. Both halves of the ratchet are proved to bite —
   M3 the ceiling, M4b the staleness — but by three mutations, not the two named.
3. **A DOUBT I APPLIED ANYWAY, per constraint 1.** LEDGER27's `- R-0872` paragraph says the
   next round lowers the allowlist "to 22", while PLAN27 says the same round lowers it "by
   21" and the finding's own path breakdown sums the four dying pages plus
   `core-product-spine-v0.md` to 6 + 7 + 2 + 1 + 5 = 21 of 43, leaving 22. The two numerals
   agree; I record the reading because "by 21" and "to 22" are stated in different files and
   a later round will resolve one of them without the other in view. Applied byte for byte,
   unrepaired.
4. **The block's line-3072 reading is a BASE reading, not a post-state one.** U1's preamble
   says "the file ends at line 3072"; that is `c370dcee`. After U1 and U2 the file is 3076
   lines. G4 asked for the file's total line count and I report the measured 3076; nothing
   is wrong in the block, but a reviewer re-running G4 against the committed blob will read
   3076 and should not read it as a mismatch.
5. **G7's `remedy worker list` probe exits 0 and PRINTS.** The block ordered the probe with
   no `--help`, and `worker list` is a real, read-only listing command, so running it wrote
   `Worker Adapters` and its table to a captured buffer. No state was written; the other
   four probes all exit 2 on a missing argument before doing anything.
6. **No assumption was made about anything the block did not state.** The 43 allowlist
   entries were GENERATED from the worker's own sweep per constraint 8 and never transcribed
   from the block; the digest gate confirms them. Round 26's deleted-module sweeps were NOT
   re-verified, per constraint 10.

## Open findings

**88 open by DISTINCT id** at `6335babf`, computed mechanically from
`.agent/live_review.md`: 101 distinct `^- R-\d+ — ` registrations minus 13 distinct
`^Done: R-\d+ — ` resolutions. This round registered one (R-0872) and resolved one
(R-0847), so the count is unchanged from the base `c370dcee`. Four are High — R-0803,
R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `4ba30f28`, block copied verbatim, digest verified three ways |
| C0b | done | `c2a5dca7`, mirrored from the COMMITTED C0a blob |
| C1 | done | `8fe426b3`, `.agent/plan.md` byte-identical to PLAN27 |
| C2 | done | `f4390b10`, both appends byte-exact, open set 88 |
| C3 | done | `088e7e7d`, U1 and U2 applied |
| C4 | done | `3225d876`, SPEC-GUARD (a)-(j) and P1..P8 |
| C4b | deviated | UNORDERED extra commit `6335babf`; deviation 1 |
| C5 | done | this file |
| U1 | done | FROM 1→0, TO 0→1; the invented `remedy list` is gone and the span is enumerated |
| U2 | done | FROM 1→0, TO 0→1 |
| P1 | done | `cockpit.py` — `remedy timeline` → `remedy brain timeline` |
| P2 | done | `cockpit.py` — the next-action f-string |
| P3 | done | `trust_report.py` — `remedy constitution` → `remedy brain constitution` |
| P4 | done | `brain_detail.py` — run-event next action |
| P5 | done | `brain_detail.py` — `remedy agent-loop` → `remedy dev agent-loop` |
| P6 | done | `brain_detail.py` — the prose the widened guard does NOT reach, repaired anyway; G7's pair proof gates it |
| P7 | done | `brain_detail.py` — constitution next action |
| P8 | done | `brain_detail.py` — `remedy workers` → `remedy worker list` |
| G1 | done | REAL_EXIT=0, one digest for all three copies |
| G2 | done | REAL_EXIT=0, `written == slice: True`, 44 lines, both headings 1 |
| G3 | done | REAL_EXIT=0, both appends, both negative controls reject, open set 88 |
| G4 | done | REAL_EXIT=0, (a) 1→0, (b) 3→2 with line numbers, `Steps 38 to 43` 1→0 |
| G5 | done | REAL_EXIT=0, 542/0 and 417/68/43, digest matches, 6 passed |
| G6 | deviated | REAL_EXIT=0 and every ordered mutation RED, but M4 fires the ceiling rather than staleness and needed the added M4b; deviation 2 |
| G7 | done | REAL_EXIT=0, eight pairs, five dispatcher probes, ruff clean |
| G8 | done | REAL_EXIT=0, 2024 passed, 222/44/0, exact set match, all commits under 500 |
| R-0847 | done | resolved at C4; `Done: R-0847` written at C2 under constraint 4, which fixes C4 in the same round and before the handback |
| R-0872 | done | registered at C2 with its 43-key measurement and its two-round fix clause; the ratchet that carries it lands at C4/C4b |

## Next

The planner/reviewer re-runs G1 through G8 independently against the committed blobs over
`c370dcee`..HEAD and issues the round 27 verdict; before authoring round 28 it re-reads
`.agent/STOP` from disk (Phase 1 rule 1 before rule 2). Round 28 is R-0872's first half:
delete the four dying pages, repair `docs/system/core-product-spine-v0.md`, and lower
`KNOWN_DEAD_DOC_ADVERTISEMENTS` and `_ALLOWLIST_CEILING` from 43 to 22 in the same commit.
