# Handoff — F262 List commands v2 (dates, sort, filter), round 21 (SCOPE REPORT — session soft limit reached)

## Session

SESSION 7 of feature F262 · round 21 · rounds so far 21.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

This feature has now run 7 sessions, the operator's stated soft limit
per amendment amend0827-process-diet rule 6
(docs/agents/planner_reviewer_prompt.md §3,
docs/agents/self_drive_protocol.md "Ending a session"). Per that rule,
this round's obligation is a SCOPE REPORT, not more build work: round
21 books round 20's already-PASSED verdict (GATE20) into
`.agent/live_review.md`, registers finding R-0795, replaces
`.agent/plan.md` with PLAN22, and writes this handback as the scope
report the limit obliges. No production, test, or docs path was
touched this round — see item 4 below.

### SCOPE REPORT

**DONE:**
- T001 — shared list-command surface: the catalog's `_is_list_command`
  match and mechanical `_with_list_options` attachment of
  `--sort`/`--desc`/`--since`/`--until`/`--limit` to every catalog
  entry whose id is `list` or ends `-list`.
- T002 — every list command shows a CREATED and an UPDATED date (per
  Acceptance), across all list commands in scope.
- T003 — sort/filter/limit fully wired for five commands:
  `job.list`, `patch.list`, `queue.list`, `memory.list`, `loop.list`.
  Two of these five — `queue.list` and `loop.list` — carry a
  deliberate, DECISION-documented (D2/D3) opt-out from the
  newest-first default sort field (`default_sort_field=None`,
  config-declaration order stays default for those two).

**MISSING:**
- The T001 catalog test that proves no list command is missing a
  flag (T001's own Acceptance bullet; never built).
- `config.list`/`worker.list`/`execution.list` PARSE all four T003
  flags via the catalog's mechanical attachment, but their handlers
  silently discard them — measured directly this round (R-0795,
  registered below): `--sort bogus` against any of the three raises
  nothing, where T2_F262.md's Acceptance requires a non-zero exit
  naming the valid fields.
- The Acceptance ten-second-demo integration smoke test (a named run
  findable by one command with `--since`/`--sort`) — not yet built.
- `change.list`'s event-log CREATED date — tracked separately as OUT
  OF SCOPE per DECISION F262 D1's Alternative section, unrelated to
  R-0795.

### PROPOSAL TO THE OPERATOR (documented only, not executed this session)

Per PLAN22's Next Steps, two options, neither acted on by this
session's own authority:

- **Option A**: authorize an 8th session to (1) build the T001
  catalog test deriving the list-command set from the CLI catalog,
  (2) wire `config.list`/`worker.list`/`execution.list`'s handlers to
  `apply_list_options` (they already receive the parsed flags), (3)
  build the Acceptance ten-second-demo smoke test, then close F262.
- **Option B**: register a DECISION narrowing T003's Acceptance to
  explicitly exempt these three commands by name and reason, correct
  `.agent/plan.md`'s Risks section to state the exemption precisely
  (accepted-but-ignored, not the current imprecise blanket "excused"
  phrasing), and close F262 without the catalog test or the smoke
  test.

This is a proposal for the operator to choose between at the next
session's Phase 0 — it is not a decision this round makes for itself.

**No code, test or docs path was touched this round.** Only
`.agent/authored/f262-r21.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md` and this handback
(`.agent/handoff.md`) were written — five `.agent/**` paths, matching
the block's constraint 1 exactly. Why: this round's entire obligation,
per the soft-limit rule, was booking GATE20, registering R-0795, and
reporting scope — not more build work.

## Range

Review of `22915c4b..d4760aa2`. That is C0a through C3 (five content
commits: C0a, C0b, C1, C2, C3). This handback (C4) follows and is not
part of the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | branch `feature/f262-list-commands-v2`, tree clean, `.agent/STOP` absent, all confirmed before C0a |
| C0a | done | `.agent/authored/f262-r21.md` saved verbatim, new file; sha256 matches source block file exactly |
| C0b | done | mirrored to `.agent/last_block.md` via `shutil.copyfile`; identical sha256 to C0a's file |
| C1 | done | PLAN22 applied to `.agent/plan.md`, whole-file replace, byte-for-byte verified 2350/2350, 49 lines |
| C2 | done | GATE20 appended to `.agent/live_review.md`: before 2473689, after 2476468 — matches 2473689+1+2778 exactly |
| C3 | done | FINDING R-0795 appended to `.agent/live_review.md`: before 2476468, after 2479698 — matches 2476468+2+3228 exactly |
| C4 (this handback) | done | |
| G1 (sha256sum transport) | done | one identical digest, twice |
| G2 (live_review.md byte forensics, C2) | done | before 2473689, after 2476468 — both match |
| G3 (live_review.md byte forensics, C3) | done | before 2476468, after 2479698 — both match |
| G4 (plan.md byte-for-byte) | done | 2350 bytes, byte-for-byte equal to PLAN22, 49 lines |
| G5 (git status --porcelain, twice) | done | empty before C0a, empty immediately before C4 |
| G6 (git ls-files .remedy-wt) | done | empty output |

## Commits

### 655f71ae F262 R21 C0a: save step block verbatim to .agent/authored/f262-r21.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r21.md` | +104/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 2909d2b4 F262 R21 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +68/-240 | mirror of the round's authored block (whole-file rewrite via `shutil.copyfile`; diff hunk counts differ from C0a's raw insert count because this is a content replacement over the prior round's mirrored block, not an append — content is byte-identical to C0a's file, confirmed by G1's matching sha256) |

### 76c8c6b9 F262 R21 C1: replace plan.md with PLAN22
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +28/-26 | whole-file replace with PLAN22, byte-for-byte verified (2350/2350 bytes, 49 lines, no trailing newline) |

### 8d141dd4 F262 R21 C2: append GATE20 to live_review.md - books round 20's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE20, `\n` + GATE20's own 2778 bytes appended to the base file |

### d4760aa2 F262 R21 C3: append FINDING R-0795 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +3/-1 | byte-exact append of FINDING R-0795, `\n\n` + R-0795's own 3228 bytes appended immediately after GATE20 |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f262-list-commands-v2` — runs
  immediately after this commit; result reported in the closing
  message, not here, since it happens after this file is committed.
  No `gh pr` command of any kind was run (forbidden this round: no PR,
  no merge, no Open PR Gate, no `main` touched).

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f262-list-commands-v2
$ ls .agent/STOP
No such file or directory
```
All confirmed.

**BYTE PRECONDITIONS, verified before any write (per block arithmetic):**
```
GATE20 text: 2778 bytes, 0 internal newlines — matches block's stated 2778 exactly
FINDING R-0795 text: 3228 bytes, 0 internal newlines — matches block's stated 3228 exactly
live_review.md size before any write: 2473689 — matches block's stated base exactly
```

**TRANSPORT (after C0b):**
```
$ sha256sum .agent/authored/f262-r21.md .agent/last_block.md
62077e148db6644c38030ef6fe3c94f225f8020448fa53d1e75d927871ba984f  .agent/authored/f262-r21.md
62077e148db6644c38030ef6fe3c94f225f8020448fa53d1e75d927871ba984f  .agent/last_block.md
```
One digest, twice — PASS. Also confirmed against
`.remedy-wt/block21.md` itself (the source file the block was read
from): identical sha256, verified before C0a's commit.

**LEDGER APPEND, GATE20 (live_review.md), byte-forensics:**
```
before size: 2473689
gate20 length: 2778
after size: 2476468
ALL ASSERTIONS PASSED
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append).

**LEDGER APPEND, FINDING R-0795 (live_review.md), byte-forensics:**
```
before size: 2476468
finding length: 3228
after size: 2479698
ALL ASSERTIONS PASSED
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append). Both appends were
verified against the previous append's own post-size before writing,
so C2 and C3 chain correctly with no stale base.

**THE PLAN, BYTE-FOR-BYTE (constraint: byte-exact whole-file replace):**
```
PLAN22 bytes (extracted from block, lines 30-78): 2350
written size: 2350
line count: 49 (under the AGENTS.md 50-line cap)
EXACT MATCH CONFIRMED
```
Whole-file replace applied via a direct `pathlib.Path.write_bytes`
call after extracting PLAN22's exact text from the authored block
(lines 30 through 78 inclusive — line 79 is a blank separator line
before the `====` divider, not part of PLAN22), then re-verified exact
in BINARY mode.

**THE TREE, THE COMMITS AND THE SWEEP:**
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
$ ls .agent/STOP   (re-checked immediately before C4)
No such file or directory
```
Tree clean before C4, nothing under `.remedy-wt/` tracked, STOP absent
both times it was checked.

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat --format="" 655f71ae
104  0    .agent/authored/f262-r21.md
$ git show --numstat --format="" 2909d2b4
68   240  .agent/last_block.md
$ git show --numstat --format="" 76c8c6b9
28   26   .agent/plan.md
$ git show --numstat --format="" 8d141dd4
2    1    .agent/live_review.md
$ git show --numstat --format="" d4760aa2
3    1    .agent/live_review.md
```
Every path and every insertion/deletion count matches the Commits
table exactly.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r21.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/plan.md` — NOT stale. Freshly written PLAN22 content
  accurately describes round 21's actual state (scope report, session
  soft limit reached, R-0795 registered, two-option proposal open).
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE20's
  content describes round 20's own verified facts, and R-0795 is
  registered exactly as measured this round, both new appends with no
  edit to prior content.

No `apps/`, `packages/`, `tests/` or `docs/` path was read for
modification purposes this round (constraint 1); the only reads of
production code this session were the ones already embedded, verbatim,
in R-0795's own text as authored by the reviewer and copied unmodified
into the ledger.

## Authored-text proofs

For every reviewer-authored text applied this round — GATE20 and
FINDING R-0795 (both into `.agent/live_review.md`) and PLAN22 (into
`.agent/plan.md`) — the disk-to-disk comparison against the committed
`.agent/authored/f262-r21.md` slice is reported above under
Verification: all three matched byte-for-byte (GATE20: 2778/2778 bytes
equal; R-0795: 3228/3228 bytes equal; PLAN22: 2350/2350 bytes equal).
All three texts were extracted directly from `.remedy-wt/block21.md`
(the same source `.agent/authored/f262-r21.md` was copied from
byte-for-byte via `shutil.copyfile`, confirmed by G1's matching
sha256), so authored-text identity holds by construction as well as by
direct re-measurement.

## Deviations & assumptions

None. The bundle's commit order (C0a, C0b, C1, C2, C3 — this handback
C4) was followed exactly, one commit per bundle item, in the exact
order the block specified. No byte-count or arithmetic contradiction
was found anywhere in this round's block: GATE20's stated 2778 bytes,
R-0795's stated 3228 bytes, PLAN22's stated 2350 bytes / 49 lines, and
every before/after arithmetic check (2473689+1+2778=2476468;
2476468+2+3228=2479698) were all independently verified true by direct
byte measurement before any write, with no STOP triggered. `.agent/STOP`
was absent every time it was checked (before C0a, and once more
immediately before C4/this handback). No path outside the declared
change set was written under version control: only
`.agent/authored/f262-r21.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, and this handback were
committed — five `.agent/**` paths, matching constraint 1 exactly. No
`apps/`, `packages/`, `tests/` or `docs/` path was touched, per this
round's own point (a scope-report round). No `remedy` CLI command was
attempted (per constraint 7, denied session-wide). No sandbox-override
flag was used for any command; `shutil.copyfile` was used for both
copies per constraint 6.

## Next

**NEXT EXPECTED ACTION: Phase 0, fresh, at the start of the next
session — an OPERATOR DECISION between PLAN22's Option A (authorize an
8th session to build the T001 catalog test, wire
`config.list`/`worker.list`/`execution.list` to `apply_list_options`,
and build the Acceptance smoke test, then close F262) and Option B
(register a DECISION narrowing T003's Acceptance to exempt those three
commands by name, correct `.agent/plan.md`'s Risks section precisely,
and close F262 without the catalog test or smoke test).** This
session (session 7) has reached the operator's stated 7-session soft
limit for this feature, so no further round should be delegated on
this feature without that decision being made first.
