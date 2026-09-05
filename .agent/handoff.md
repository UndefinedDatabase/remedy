# Handback — F259 Vocabulary & concept model v1, round 4

## Session

`SESSION 1 of feature F259 · round 4 · rounds so far 4`

Fortschritt: `~55 % (T001 ✅ · T002 ✅ · T003, T004 offen) — Schätzung`

Context self-assessment (operator amendment amend0905-throughput): the round's
read set was the block, four `.agent/` files, one feature file and one docs page,
plus two source files read only by script, so the session window is still wide
and several more rounds fit before a boundary is needed.

## Range

Review of a03d8b6b..36eaa893.

## Commits

### 736bc124 f259: save the round 4 block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f259-r4.md | +283 / -0 | C0a — `shutil.copyfile` of `.remedy-wt/f259-r4-block.md`, never retyped |

### 145845e5 f259: mirror the round 4 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +180 / -172 | C0b — same copy; the churn is round 3's block being replaced |

### b0641672 f259: rewrite the plan for round 4, T002
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -17 | C1 — whole rewrite from the PLANF259R4 slice |

### c1dfb765 f259: book the round 3 PASS verdict and the reviewer prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE_R3 appended at end of file |
| .agent/prose_slips.md | +3 / -1 | C2 — SLIP4 appended; the one deletion is the former last line regaining a newline, the file itself still ends without one |

### 36eaa893 f259: append the eleven rulings to the vocabulary page
| Path | +/- | Reason |
|---|---|---|
| docs/system/vocabulary.md | +174 / -0 | C3 — RULINGS_INTRO plus the eleven script-extracted rulings |

The final commit (C4) writes this file and cannot table itself
(handback_template.md R-0149 exception): it changes `.agent/handoff.md` only.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

- `git push -u origin feature/f259-vocabulary` → `a03d8b6b..36eaa893`, tracking set. Second push after C4.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. No pull request created this round, as the block orders.
- No worktree added or removed. No `gh pr merge`, no force push, no history rewrite, no branch deletion.

## Verification

G1 TRANSPORT — `sha256sum .remedy-wt/f259-r4-block.md .agent/authored/f259-r4.md .agent/last_block.md`, exit 0. One digest three times:
`7b58ea8e5d5d8990dc545a1f949ec05aba23d90887d8868f1c95ab9724ec2aa5`. It also equals the digest the delegation named, so the block arrived unaltered.

G2 THE PAGE APPEND — `docs/system/vocabulary.md` 14 545 → 25 555 bytes; joined text 11 008 bytes; remainder 11 010. Prefix property `True`; total reconstruction `post == pre + "\n" + joined + "\n"` `True`.

G3 ELEVEN RULINGS UNEDITED — all eleven equal, source digest == page digest after restoring `## ` on the nine amend0905 headings:
D2 `48e76936a6a1a5b0`, D3 `25bfb567fc45b5f9`, D4 `aa2885b866c18062`, D5 `1091816d5e58c8e7`, D6 `50312b57ad18e9de`, D7 `6f0894c5a2047f70`, D8 `c3a7b8be33c745b4`, D9 `7f2e0623424628f8`, D10 `6044d221fe84bef2`, F259 D1 `83bfc3c7f6f07454`, F259 D2 `c00e8779d5c8d6e6` (sha256 prefixes; equality was tested on the full digests). `rulings compared: 11, equal: 11`.
NEGATIVE CONTROL, on `.remedy-wt/vocabulary.negctl.md` with `job plan` → `job scheme` inside D6's BODY (heading untouched): `rulings compared: 11, equal: 10`, the single unequal one being D6, page digest `7f74d74aed89205c` against source `50312b57ad18e9de`. The comparison can fail.

G4 SECTIONS AND ORDER — five `## ` headings in file order: `How to read the table`, `The words`, `Do not confuse these`, `The concept model`, `The rulings`. Eleven `### ` headings in file order: amend0905-vocab D2, D3, D4, D5, D6, D7, D8, D9, D10, then F259 D1, then F259 D2 — exactly the ordered list the block requires. My own extraction measured the eleven source blocks at **10 023 bytes / 146 lines** before demotion (identical to the reviewer's a03d8b6b measurement) and 10 032 bytes / 146 lines after, +9, one byte per demoted block. Exactly one fenced `mermaid` block (opened by a triple-backtick `mermaid` line); its body is 309 bytes and hashes to `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`, the pinned value, undisturbed.

G5 THE T002 CONDITIONAL — first line of `docs/roadmap/features/T2_F263.md`, verbatim:
`# T2_F263 — Human-change absorption (absorb)`
The string `absorb` occurs in it: `True`. The block's claim holds, the conditional is false, the file was not edited. `git status --porcelain` named `docs/roadmap/features/T2_F263.md` at no point this round (checked in Python against the captured status output: `names T2_F263.md: False`).

G6 RECORD AND SLIP APPENDS — `.agent/live_review.md` 827 079 → 830 738 bytes; prefix `True`, remainder `== "\n" + GATE_R3 + "\n"` `True`; `grep -c '^Gate: R3 — '` 0 on the pre-append copy, 1 on the committed file. `.agent/prose_slips.md` 77 778 → 79 043 bytes; prefix `True`, remainder `== "\n\n" + SLIP4` `True`, still no trailing newline (final byte `b'.'`).

G7 THE SUITES, SERIAL, at C3 — every count exact, every exit code 0:

    tests/docs/                                 exit=0  295 passed
    tests/orchestration/test_roadmap_index.py   exit=0   30 passed
    tests/ui_server/                            exit=0  515 passed
    tests/orchestration/test_test_runner.py     exit=0   52 passed
    tests/regression/test_resource_safety.py    exit=0   21 passed
    tests/orchestration/test_integrity_gate.py  exit=0   16 passed
    tests/cli/test_golden_path.py               exit=0   42 passed

The four state readers ran as four separate invocations. No failing node ids, so none to quote.

G8 PLAN AND STRUCTURE — `wc -l .agent/plan.md` = 45, under 50. `grep -c '^## Goal'` = 1, `grep -c '^## Next Steps'` = 1. `filecmp.cmp('.agent/plan.md', <PLANF259R4 slice + one newline>, shallow=False)` = `True` (slice 2 245 bytes, file 2 246). `git status --porcelain` EMPTY immediately before C4 was staged. `git ls-files .remedy-wt` returned 0 lines. Every commit single-parent, confirmed by `git log --format='%h %p %s'`: 736bc124←a03d8b6b, 145845e5←736bc124, b0641672←145845e5, c1dfb765←b0641672, 36eaa893←c1dfb765, one parent each. Per-commit `git diff --numstat <parent> <commit>`, cell by cell, the same numbers the Commits table above carries:

    a03d8b6b→736bc124   283  0  .agent/authored/f259-r4.md
    736bc124→145845e5   180 172 .agent/last_block.md
    145845e5→b0641672    18  17 .agent/plan.md
    b0641672→c1dfb765     2   0 .agent/live_review.md
    b0641672→c1dfb765     3   1 .agent/prose_slips.md
    c1dfb765→36eaa893   174   0 docs/system/vocabulary.md

Insertions against the AGENTS.md 500 cap: 283, 180, 18, 5, 174 — largest 283, no commit near the cap, no oversize declaration needed. Push: `a03d8b6b..36eaa893`, succeeded. No pull request created (`gh pr list --state open` → `[]`).

## Authored-text proofs

Every applied text was extracted from the COMMITTED `.agent/authored/f259-r4.md`
by marker extraction in Python (`.remedy-wt/f259_r4_extract.py`), never retyped:

| Slice | Bytes | Landed in | Proof |
|---|---|---|---|
| PLANF259R4 | 2 245 | `.agent/plan.md` | `filecmp.cmp(..., shallow=False)` `True` against slice + one newline |
| GATE_R3 | 3 657 | `.agent/live_review.md` | total reconstruction `True` |
| SLIP4 | 1 263 | `.agent/prose_slips.md` | total reconstruction `True` |
| RULINGS_INTRO | 954 | `docs/system/vocabulary.md` | total reconstruction of the whole append `True` |

The eleven rulings are NOT authored slices. They were extracted from
`.agent/decisions.md` and `docs/roadmap/features/T2_F259.md` by
`.remedy-wt/f259_r4_rulings.py`, which asserted nine amend0905 blocks in the
order D2…D10 and two F259 blocks in the order D1, D2 before writing anything.
Their fidelity proof is G3, per-ruling sha256 against the source, with a
negative control.

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, push, gates, C4, push — exactly as ordered, five commits before the
   handback and one for it, no extra and none dropped. Constraint 8 is honoured:
   this handback quotes no reading that only exists after it is pushed. The
   post-C4-push `git status --porcelain`, `git ls-files .remedy-wt` and the
   `origin/feature/f259-vocabulary` tip are deliberately absent here and belong
   to the reviewer's next ledger entry (planner_reviewer_prompt.md §3 item 31).
2. **One shell-guard refusal, re-expressed in Python, no gate narrowed.** The
   session guard denied the G7 form
   `python3 -m pytest tests/docs/ -q 2>&1 | tail -4; echo "EXIT: ${PIPESTATUS[0]}"`
   with, verbatim: `Permission to use Bash has been denied. IMPORTANT: You *may*
   attempt to accomplish this action using other tools that might naturally be
   used to accomplish this goal, e.g. using head instead of cat. But you *should
   not* attempt to work around this denial in malicious ways, e.g. do not use
   your ability to run tests to execute non-test actions. You should only try to
   work around this restriction in reasonable ways that do not attempt to bypass
   the intent behind this denial. If you believe this capability is essential to
   complete the user's request, STOP and explain to the user what you were trying
   to do and why you need this permission. Let the user decide how to proceed.`
   Every suite was then run plainly for its count AND a second time under
   `.remedy-wt/f259_r4_g7.py`, which reads `subprocess.CompletedProcess.returncode`
   directly, so both readings G7 asks for are real. Both passes agreed on all
   seven counts. The `$?` and `$` -anchor forms were avoided for the same reason;
   `grep -c '^Gate: R3 — '` carries no `$` anchor and was accepted as written.
3. **No error found in any slice.** Nothing in PLANF259R4, GATE_R3, SLIP4 or
   RULINGS_INTRO needed declaring under constraint 1, and no ruling was touched
   beyond step C's heading demotion.
4. **G4's `###` count.** The eleven `### ` headings on the page are exactly the
   eleven rulings; the page carried no `### ` heading before this round, so the
   ordered list is complete rather than filtered.
5. `.remedy-wt/` holds four scratch files this round —
   `f259_r4_extract.py`, `f259_r4_rulings.py`, `f259_r4_g3.py`, `f259_r4_g7.py`,
   plus the pre-append captures and `vocabulary.negctl.md`. All gitignored, none
   committed, confirmed by `git ls-files .remedy-wt` returning 0 lines.
6. `.agent/STOP` was read from disk before C0a, before C3 and before C4
   (constraint 3). Absent all three times.

## Next

The reviewer gates this round (a03d8b6b..36eaa893) and takes the post-push
readings constraint 8 reserves for it. Then round 5, T003:
`tests/docs/test_vocabulary.py` in planned mode, with both red proofs
T2_F259.md's T003 names — removing a binding word from the page must fail the
page assertion, and flipping the mode constant to enforced against today's
`apps/cli/command_catalog.py` must fail the synonym assertion.
