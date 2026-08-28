# Handback — F037 R1 (claim, ledger reset, source inventory)

## Session

SESSION 1 of feature F037 · round 1 · rounds so far 1

## Range

Review of 9dde54956afbe5f432bfd429bf4ba0bb272f6d07..HEAD

## Commits

### 3f0e0ab4 docs(agent): save the F037 R1 block as authored
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r1.md | 458 / 0 | C0a — the block copied byte for byte from `.remedy-wt/f037-r1.md` |

### f7b5e638 docs(agent): mirror the F037 R1 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 446 / 393 | C0b — mirror written from the committed C0a blob; same git blob `2da50bdb` |

### 89b96df7 docs(agent): point the plan and the context at F037
| Path | +/- | Reason |
|------|-----|--------|
| .agent/context.md | 15 / 13 | C1 — byte-equal to slice CTXF037R1 |
| .agent/plan.md | 34 / 31 | C1 — byte-equal to slice PLANF037R1 |

### 689f181f docs(roadmap): claim F037 as the active feature
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | 1 / 1 | C2 — SFROM to STO, `[ ]` becomes `[~]` on the F037 line |

### d4aef1db docs(agent): reset the live-review header for F037 and book the F032 R19 gate
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 26 / 23 | C3 — LFROM/LTO header rewrite plus the GATEF032R19 EOF append; findings region byte-identical |

### 7d9b32df docs(agent): add the F037 source inventory
| Path | +/- | Reason |
|------|-----|--------|
| .agent/f037_inventory.md | 435 / 0 | C4 — Q1 through Q8, each measured |

### C5 docs(agent): hand back the F037 R1 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | a handoff cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `.agent/authored/f037-r1.md`, byte-identical |
| C0b mirror it into `last_block` | done | same git blob as C0a |
| C1 the plan and the context | done | both byte-equal to their slices |
| C2 the STATUS claim | done | `[ ]` → `[~]` on the F037 line |
| C3 the live-review header reset and the F032 R19 gate append | done | header rewritten, gate appended, findings region untouched |
| C4 the inventory | done | `.agent/f037_inventory.md`, Q1-Q8 |
| C5 the handback | done | this file |
| push | done | ordered after C5; outcome reported in the round report, not here |
| Q1 the parsers that already exist | done | one reader exists; a new module is needed |
| Q2 the file-status vocabulary | done | seven statuses; `binary` absent |
| Q3 where a diff comes from at runtime | done | per task run and per job; none per attempt |
| Q4 the server route table | done | 10 GET shapes, 14 dict endpoints, 1 POST; guards cited |
| Q5 the attempt identifier | done | three notions, no canonical id |
| Q6 the client entry point | done | 0 hits; 4 props; no test pins the component |
| Q7 the fetch seam and the bundle budget | done | `fetchJson` throws; no budget exists |
| Q8 the guards a new module must satisfy | done | equality guards cited; the status vocabulary is unguarded directly |

Open findings after this round: **251** (275 registered, 24 resolved, maximum id
`R-0714`). No finding was registered or resolved this round.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — run
  twice: once before the branch was cut, as the AGENTS.md Open PR Gate requires,
  and once at G8. Both read `[]`. Nothing merged, nothing created.
- `git checkout -b feature/f037-rendered-diff-viewer` from `main` at
  `9dde54956afbe5f432bfd429bf4ba0bb272f6d07` — the branch this round's six
  commits land on.
- `git push -u origin feature/f037-rendered-diff-viewer` is INTENDED immediately
  after this commit. Its exit code and the resulting remote tip do not appear
  here: this file is authored before the push exists, so stating either would be
  a value that cannot be true when written. Both are reported in the round
  report instead, per the block's G8.
- No pull request was created. No worktree was added or removed. No merge.

## Verification

- **G1 — hygiene, branch, sentinel · exit 0.** `git rev-parse HEAD` before the
  cut: `9dde54956afbe5f432bfd429bf4ba0bb272f6d07`. `git branch --show-current`
  after C0a: `feature/f037-rendered-diff-viewer`. `git status --porcelain` line
  count after C0a, C0b, C1, C2, C3, C4: `0 0 0 0 0 0`. `.agent/STOP` read from
  disk before C0a: ABSENT; read again before C5: ABSENT.
- **G2 — transport · exit 0.** Four points, all EQUAL: sha256
  `906b7ee592aed02e7161797030d5adfc2906390f7367feae446f55fe2b2e1231`, 32631
  bytes, 458 lines, at `.remedy-wt/f037-r1.md`, the C0a commit blob, the C0b
  commit blob and the working copy at C4. C0a and C0b are the SAME git blob,
  `2da50bdba5ca4a632eac5e5255fc0bdf34a7c2df`. Lines that are a run of one
  repeated character at length 4 or more: NONE. What this proof covers: the
  scratch file, the saved copy, its mirror and the working copy — and NOT the
  bytes of any prompt, which no party to this round measured.
- **G3 — extraction and caps · exit 0.** Extractor printed 7 slices from the
  committed C0a blob at their marker lines: PLANF037R1 47, CTXF037R1 55, LFROM
  26, LTO 27, GATEF032R19 1, SFROM 1, STO 1. CONTENT 158, TOTAL 458, PROSE
  = 458 − 158 = 300. PROSE 300 ≤ 400 and TOTAL 458 ≤ 490; both caps hold.
- **G4 — plan and context · exit 0.** `.agent/plan.md` at C1 BYTE-EQUAL to
  PLANF037R1: True; negative control against the slice minus its trailing
  newline: False. `.agent/context.md` at C1 BYTE-EQUAL to CTXF037R1: True;
  negative control: False. Contract readings — plan: `^## Goal$` 1,
  `^## Next Steps$` 1, `\bF\d{3}\b` matched (`F037`), `wc -l` 47, strictly under
  50; context: `^## Active Branch$` 1, `feature/` matched, `\bF\d{3}\b` matched,
  substring `Steps` present.
- **G5 — ledger reset, gate append, findings region · exit 0.** Reconstruction
  BYTE-EQUAL to `.agent/live_review.md` at C3: True. Negative control, one byte
  flipped at offset 1126777, which lies inside the appended paragraph (starting
  at 1126577, file ending at 1130704): False. Pair readings — LFROM 1 before,
  0 after; LTO 0 before, 1 after; the pre-commit blob is NOT a byte prefix of
  the result, because the header changed. The region from the first byte of
  `## Findings` to the end of the pre-commit blob measured 1124868 bytes, sha256
  `abc8bdb4f682d04bc84d56ca0eda9d23dc17c32cb5987fab8e3d91c932a7f528`, IDENTICAL
  at both points and equal to the reviewer's base measurement. Line-anchored
  counts, pre then C3: `^- R-\d+ — ` 275 → 275, `^Done: R-\d+ — ` 24 → 24,
  `^Landed: R-` 1 → 1, `^Gate: R\d+ — ` 19 → 19, `^Gate: F\d+ R\d+ — ` 70 → 71.
  Finding ids added `[]`, removed `[]`; resolved ids added `[]`, removed `[]`.
  All ids DISTINCT at both points. Maximum id `R-0714` at both points. Open set
  251 at both points. `^## Findings$` exactly 1 at both points. `Steps` present
  at both. Literal `Gate: F032 R19 — ` 0 before, exactly 1 after.
- **G6 — STATUS claim and docs gate · REAL exit 0.**
  `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q`,
  run from the repository root BEFORE C2 was committed. Summary line verbatim:
  `325 passed in 0.62s`. Matches the reviewer's `325 passed` reference at a real
  exit 0. `docs/roadmap/STATUS.md` at C2: SFROM 0 occurrences, STO exactly 1.
  Line-anchored counts, base then C2: `^- \[ \] ` 196 → 195, `^- \[x\] `
  59 → 59, `^- \[~\] ` 0 → 1. Total lines matching `^- \[`: 255 at both points,
  UNCHANGED.
- **G7 — state readers and canary · REAL exit 0.** One pytest process, run
  after C4 and before C5: `python3 -m pytest tests/ui_server/
  tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
  tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`.
  Summary line verbatim: `620 passed in 66.51s (0:01:06)`. Count of lines
  matching `^FAILED`: 0. The `^FAILED` extractor is NOT blind: run over the
  control string `one\nFAILED tests/x.py::test_y - AssertionError\ntwo\n` it
  matched 1 line, `FAILED tests/x.py::test_y - AssertionError`.
- **G8 — structure, artifacts, Open PR Gate · exit 0.** Path set of
  `git diff --name-only 9dde5495..7d9b32df` compared BOTH WAYS against the
  Change list minus `.agent/handoff.md`: residue GOT−WANT `[]`, residue
  WANT−GOT `[]`. `git diff --stat` restricted to `apps/`, `packages/` and
  `tests/`: EMPTY, EMPTY, EMPTY; restricted to `docs/`:
  `docs/roadmap/STATUS.md | 2 +-`, that file alone. Per-commit insertions from
  `git diff --numstat`, each single-parent and under 500: C0a 458, C0b 446,
  C1 49, C2 1, C3 26, C4 435. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
  and 0 in `.agent/plan.md` and `.agent/context.md` at C1 and in
  `.agent/live_review.md` at C3, against a CONTROL over the C0a blob reading 7
  and 7. `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line,
  `git branch --list "tmp/*"` 0 lines. Open PR Gate output verbatim: `[]`.

## Authored-text proofs

Every slice applied this round was extracted PROGRAMMATICALLY from the committed
C0a blob via `git show 3f0e0ab4…:.agent/authored/f037-r1.md` and applied from
there in Python; nothing was retyped.

| Slice | Applied to | Disk-to-disk result |
|-------|-----------|---------------------|
| PLANF037R1 | `.agent/plan.md` at C1 | BYTE-EQUAL True, trailing-newline control False |
| CTXF037R1 | `.agent/context.md` at C1 | BYTE-EQUAL True, trailing-newline control False |
| LFROM → LTO | `.agent/live_review.md` at C3 | FROM 1 → 0, TO 0 → 1 |
| GATEF032R19 | `.agent/live_review.md` at C3 | EOF append reconstructed BYTE-EQUAL, one-byte-flip control False |
| SFROM → STO | `docs/roadmap/STATUS.md` at C2 | FROM 1 → 0, TO 0 → 1 |

The block itself: `.agent/authored/f037-r1.md` and `.agent/last_block.md` carry
the identical sha256 as `.remedy-wt/f037-r1.md` and are ONE git blob.

## Deviations & assumptions

**Commit sequence.** The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was
followed exactly. No extra commit, no dropped commit, no reordering. ANY COMMIT
MADE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN `## Commits` ROW AND ITS OWN
ITEM-STATUS ROW; none was made, so no such row exists.

**One wording disagreement, applied as written and declared here rather than
corrected.** G5 orders the reconstruction built as "LTO plus two newlines plus
everything from the first byte of `## Findings`". Constraint 2 defines a slice's
text as its content lines joined with a newline PLUS ONE TRAILING NEWLINE. Under
that definition the two readings differ by one byte, and I measured both against
the applied edit:

- LTO's content lines joined, then two newlines: BYTE-EQUAL True.
- LTO's newline-included slice text, then two newlines: BYTE-EQUAL False.

The applied edit is the plain LFROM→LTO replacement plus exactly one newline plus
GATEF032R19, which is the first reading. Nothing in the slice was altered. The
pre-commit blob separates the header from `## Findings` with exactly one `\n`
after LFROM's own trailing newline, so the two readings cannot both be satisfied;
the reviewer holds the ruling.

**Every numeral the block stated about the round base was reproduced exactly**,
so there is nothing to reconcile: 275 / 24 / 1 / 19 / 70 line-anchored counts,
maximum id `R-0714`, open set 251, findings region 1124868 bytes at sha256
`abc8bdb4…f528`, STATUS counts 196 / 59 / 0, `325 passed`, `620 passed`, Open PR
Gate `[]`.

**WHAT Q1 MEASURED, stated plainly because it decides the contract.** The
repository already holds ONE structured unified-diff reader,
`packages/orchestration/review_scope.py`, and it cannot be extended into F037's
JSON contract v1 without breaking its current consumers. `_parse_diff`
(`review_scope.py:73`) discards the OLD line numbers at the regex level —
`_HUNK_RE` at `review_scope.py:51` matches `-\d+(?:,\d+)?` with NO capture group
— records no per-line kind (only `+` bodies reach `added_lines`,
`review_scope.py:127-128`), keeps the hunk header only as raw text, drops the old
path of a rename (`review_scope.py:97-99`), and NEVER SEES A BINARY FILE AT ALL,
because a `Binary files … differ` stanza carries no `---`/`+++` pair. I proved
the last two empirically against the real module: a binary diff parses to `[]`,
and a rename diff comes back keyed by the new path only. Meanwhile
`parse_diff_line_ranges` is pinned by `diff_repair` and `source_apply`, both of
which state in source that they deliberately hold no parser of their own
(`diff_repair.py:8-13`, `diff_repair_apply.py:16`). CONCLUSION: T001 needs a NEW
module, and the existing seam should be left exactly as it is.

**WHAT Q2 MEASURED, stated plainly for the same reason.**
`packages/orchestration/review_subject.py` defines seven statuses at
`review_subject.py:72-78` — `added`, `modified`, `deleted`, `renamed`, `copied`,
`type_changed`, `dirty` — with `_GIT_STATUS_MAP` at `:80-86` and `_VALID_STATUSES`
at `:597-598`. Against F037's `modified|added|deleted|renamed|binary`: four of
the five EXIST, `binary` DOES NOT EXIST anywhere in the module, and the contract
OMITS `copied`, `type_changed` and `dirty`. Nothing in this repository maps a
binary file to a review file STATUS today: binary is a BLOCKER rejection in
`provider_trust.py:627-629`, an omission REASON in `diff_repair.py:68-73`, a
refusal in `source_apply.py:379`, and a rendered PLACEHOLDER `[binary file]` in
`pingpong_loop.py:1769-1770` — four vocabularies, none of them
`review_subject`'s. So the feature file's five-value status list is neither a
subset nor a superset of the built one, and the reviewer's DECISION is owed
before T001 fixes a schema.

**Three further measurements the inventory records and the reviewer may want to
rule on.** (a) There is TODAY no per-attempt diff anywhere on disk — diffs exist
per task run (`safe.diff`) and per job (`workspace.diff`) only, and
`repair_loop_v2` forbids diffs in its attempt records by name
(`repair_loop_v2.py:24`, `:45`, `:595`) — so the feature file's endpoint
parameter has nothing to key on yet. (b) `rg -n 'onOpenDiff|DiffViewer'
apps/ui/src/` returns 0 hits: the entry point the design reference names at
`docs/ui/design_reference/component_spec.md:114-115` does not exist, and no
vitest file anywhere under `apps/ui` names `DetailPopover`. (c) No bundle-size or
asset-size budget exists in `tests/` or in `apps/ui/vite.config.ts`, so the
"bundle-budget discipline" `T5_F037.md:37` leans on would be CREATED by T003, not
satisfied by it.

**One defect observed, not fixed, per Constraint 7.** The docstring at
`tests/ui_server/test_command_channel.py:1240` says "The thirteen job endpoints
live in a dict literal inside `do_GET`", while that dict at
`ui_server.py:3429-3444` holds FOURTEEN keys. It is a docstring, not an
assertion, so nothing is red; I minted no id and wrote no `Gate:` or `Done:`
line. The reviewer rules.

**Assumptions.** The `## Findings` region of `.agent/live_review.md` was treated
as beginning at the first byte of the line `## Findings` and running to the end
of the pre-commit blob, which is the block's own wording; that region is proved
byte-identical across C3.

## Next

The reviewer books the R1 verdict as a `Gate:` paragraph and rules on the Q1/Q2
findings above — whether F037's contract v1 keeps its `binary` status and its
attempt parameter — before T001 is planned.
