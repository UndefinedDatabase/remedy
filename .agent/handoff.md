# Handback — F086 Release capability, R12 (embed the build revision; record R11)

Branch `feature/f086-release-capability`, pushed, unmerged, no PR. R12 registers
R-0581; the open set moves 161 → 162. T002 is closed: the wheel now carries the
revision it was built from and the reader looks where hatchling actually puts it.

## Range

Review of ee22186c..HEAD.

## Commits

### 747457d8 chore(agent): save the F086 R12 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r12.md | +490/-0 | C0a, the block saved byte-verbatim |

### b955f84a chore(agent): mirror the F086 R12 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +403/-233 | C0b, mirror of the COMMITTED C0a file |

### 16362381 docs(state): advance the F086 plan to R12
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-10 | C1, the PLAN12 slice, whole file |

### 2e4ec7ed docs(review): register R-0581 and record the F086 R11 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, FIND0581 then RECORD10, EOF-append |

### 337d2df3 feat(packaging): embed the build revision in the wheel metadata
| Path | +/- | Reason |
|---|---|---|
| hatch_build.py | +57/-12 | C3, the HATCH slice; hook renamed RemedyBuildHook |

### 61dc35cb fix(cli): read the revision at hatchlings extra_metadata path
| Path | +/- | Reason |
|---|---|---|
| apps/cli/version_report.py | +5/-1 | C4, the single VERFROM occurrence → VERTO |

### 61618567 test(packaging): pin the build revision writer and reader path
| Path | +/- | Reason |
|---|---|---|
| tests/test_build_revision.py | +71/-0 | C5, the TESTS slice, new at the tests root |

### C6 — this handoff (self-reference exception, handback template R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | a handoff cannot table its own commit |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this file |

## External actions

- `git push -u origin feature/f086-release-capability` after C5 → `ee22186c..61618567`, OK.
- `git push` after C6 → outcome in the round report.
- `git worktree add --detach /home/decodeux/remedy-r12-probes/base ee22186c` → OK, then removed.
- `git worktree add --detach /home/decodeux/remedy-r12-probes/head HEAD` → OK, then removed.
- `git worktree add --detach /home/decodeux/remedy-r12-probes/mut HEAD` → OK, then removed.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- No PR created, nothing merged, no force-push, no rebase, no amend.

## Verification

Every gate below was executed; the exit codes and values are the real ones.

G1 HYGIENE — `git status --porcelain` 0 lines at every commit and at the
handback; `git worktree list` 1 line at the handback; `.agent/STOP` absent,
re-read from disk before C0a and again at the handback; branch
`feature/f086-release-capability`.

G2 TRANSPORT — `.remedy-wt/f086-r12.md`, the committed
`.agent/authored/f086-r12.md` and the committed `.agent/last_block.md` are all
three byte-EQUAL. sha256
cf95003c5e898b1e6ca409bac936a37e389d6f442bd548c80c5e6041150f1b25, 30277 B,
490 lines.

G3 PLAN — `.agent/plan.md` byte-equal to PLAN12. sha256
17d11ea5cff5747c19ff4ec875d0a7dba9ae892755b411dde529c05d346a51c4, 38 lines,
under 50. Contains `## Goal`, `## Next Steps` and `F086`.

G4 LEDGER APPEND — the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob;
the remainder is byte-equal to FIND0581 followed by RECORD10, that order. sha256
071a2aee0b8b4c7f47019f7ca604f3f53209c5ee6b8de7c77d5b0929fa765ecc, 4 lines.

G5 LEDGER SETS — both extractions AGREE at both revisions. ee22186c: 163
registered / 2 resolved / 0 duplicate ids / 0 unregistered resolutions / 0
anchored `Landed:` / 161 open. HEAD: 164 / 2 / 0 / 0 / 0 / 162. The registered id
SETS are EQUAL under both. Symmetric difference HEAD vs ee22186c = `['R-0581']`
under both.

G6 NO MARKER LEAKED — 0 marker LINES in each of `.agent/plan.md`,
`.agent/live_review.md`, `.agent/handoff.md`, `hatch_build.py`,
`apps/cli/version_report.py`, `tests/test_build_revision.py`.

G7 VERDICT PARAGRAPHS — paragraphs beginning `Gate: `: 9 at ee22186c naming R3,
R4, R5, R6, R7, R8, R9, R10, R11; 10 at HEAD, the added one naming R12. R12's own
entry is absent by construction; none was added.

G8 THE CODE IS THE SLICE — `hatch_build.py` byte-equal to HATCH, sha256
aa6d90779d6fd50188c3f083a1be1eccd6c0d487fd625b8ff2b53baf0b6d5b90, 90 lines.
`tests/test_build_revision.py` byte-equal to TESTS, sha256
5e6f26cfa797475ebdd13ebae815f7700cd08e545ea14ce286e715a6a5012255, 71 lines, and
ABSENT at ee22186c (`git ls-tree` returned nothing). `apps/cli/version_report.py`
by ORDERED EQUALITY: the base blob with its single VERFROM occurrence replaced by
VERTO EQUALS the HEAD blob. VERFROM base 1x / HEAD 0x; VERTO base 0x / HEAD 1x.

G9 WHEEL CARRIES THE REVISION — worktree at 61618567 outside this repository,
`apps/ui/dist/index.html` stand-in written in. Build exit 0,
`remedy-0.1.0-py3-none-any.whl`, 417 total members. Members whose name contains
REVISION = `['remedy-0.1.0.dist-info/extra_metadata/REVISION']`; that member's
exact bytes `b'616185673fc8c45fb9d13e42e0ff78c7c99f2fb1\n'`; that worktree's
`git rev-parse HEAD` = `616185673fc8c45fb9d13e42e0ff78c7c99f2fb1`. Over the
unpacked `remedy-0.1.0.dist-info`, PathDistribution
`read_text("extra_metadata/REVISION")` =
`'616185673fc8c45fb9d13e42e0ff78c7c99f2fb1\n'`; `read_text("REVISION")` = None.

G10 RED CONTROL AT THE BASE — second worktree at ee22186c, unmodified, same
stand-in and toolchain. Build exit 0, 416 total members, members whose name
contains REVISION = `[]`, `read_text("REVISION")` = None. Both worktrees removed;
`git worktree list` after = 1 line.

G11 TESTS PASS AND CAN FAIL — primary checkout, `python3 -m pytest
tests/test_build_revision.py tests/test_packaging_smoke.py
tests/cli/test_version_report.py -q -rf` → exit 0, 17 passed. Throwaway worktree
baseline exit 0, 17 passed. Mutation (i) `if revision is None:` / `return {}` →
`if False:` / `return {}` in `hatch_build.py`, replaced string counted 1x first →
exit 1, 1 failed / 16 passed, red test
`test_no_revision_writes_nothing_and_maps_nothing`. Mutation (ii)
`REVISION_METADATA_FILE` back to `"REVISION"`, replaced string counted 1x first →
exit 1, 1 failed / 16 passed, red test
`test_the_reader_carries_hatchlings_extra_metadata_prefix`. Each reverted before
the next; after the last revert that worktree's `git status --porcelain` read
0 lines.

G12 NO REGRESSION — three runs in the primary checkout, NONE overlapping, each
started only after the previous returned: (a) ended 13:31:51, (b) 13:31:51 to
13:32:11, (c) started 13:32:11. (a) `tests/test_grouped_cli.py
tests/cli/test_cli_ux.py -q` → exit 0, 560 passed. (b) the four state readers
`-q -rf` → exit 0, 160 passed. (c) `tests/cli/test_golden_path.py -q` → exit 0,
42 passed.

G13 LINT — HEAD, `python3 -m ruff check hatch_build.py
apps/cli/version_report.py tests/test_build_revision.py` → exit 0, rule-code
multiset `{}`. Base worktree over the two paths existing at ee22186c → exit 0,
multiset `{}`. HEAD contains no code more often than base; the path new at HEAD
contributes 0 codes.

G14 COMMIT SIZE — insertions per commit in ee22186c..HEAD before C6: 747457d8
490, b955f84a 403, 16362381 5, 2e4ec7ed 4, 337d2df3 57, 61dc35cb 5, 61618567 71.
None exceeds 500.

G15 HISTORY — 7 commits, each exactly one parent, each parent the previous, so
the chain is linear: ee22186c → 747457d8 → b955f84a → 16362381 → 2e4ec7ed →
337d2df3 → 61dc35cb → 61618567. `git reflog` over this round shows only
`commit:` entries — no amend, rebase, reset or force-push.

G16 PATH SET — `git diff --name-only ee22186c..HEAD` before C6 is exactly the
seven paths constraint 2 lists other than `.agent/handoff.md`:
`.agent/authored/f086-r12.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `apps/cli/version_report.py`, `hatch_build.py`,
`tests/test_build_revision.py`. `pyproject.toml` and every path under
`packages/`, `docs/`, `scripts/` ABSENT from the range; `git ls-tree ee22186c`
confirms all four EXIST at the base.

G17 OPEN PR GATE, READ-ONLY — `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` → `[]`. Nothing merged.

SIZE re-measured from the COMMITTED C0a file: 490 lines TOTAL, 223 slice (209
content + 14 marker lines), 267 prose — agreeing with the block's stated numbers.

## Authored-text proofs

All seven slices were extracted programmatically by their one-line marker pair
from the COMMITTED `.agent/authored/f086-r12.md` and applied byte-verbatim; none
was retyped and none was edited. Disk-to-disk equality against that committed
file holds for every one: PLAN12 → `.agent/plan.md` (G3); FIND0581 then RECORD10
→ `.agent/live_review.md` as a prefix-plus-remainder equality (G4); HATCH →
`hatch_build.py` and TESTS → `tests/test_build_revision.py` (G8); VERFROM/VERTO →
`apps/cli/version_report.py` by ordered equality rather than by occurrence count
(G8). Every sha256 above is written in full, all 64 characters, never elided —
that is the fix R-0581 asks for.

Slice sizes as extracted: PLAN12 2083 B / 38 lines, FIND0581 1795 B / 2,
RECORD10 3041 B / 2, HATCH 3673 B / 90, VERFROM 36 B / 1, VERTO 329 B / 5,
TESTS 2709 B / 71.

## Deviations & assumptions

- No departure from the block's ordered commit sequence. C0a, C0b, C1, C2, C3,
  C4, C5 and C6 were committed in exactly that order, one commit each, none
  added, none dropped, none reordered.
- OVERAGE DECLARED under AGENTS.md DECISION D15: this file stands at 223
  lines, over the 100-line cap. The cause is mandated content — eight per-commit
  tables plus the seventeen-gate verification transcript G1 to G17, which this
  round's block ordered reported with real exit codes and with every digest in
  full, since R-0581 makes an elided digest the defect being fixed. No mandated
  section was dropped to meet the cap.
- Probe and mutation worktrees were sited under `/home/decodeux/remedy-r12-probes/`,
  outside this repository, per constraint 4 (finding R-0574). All three removed.
- Assumption, stated because it shaped the method: this session's permission
  layer refuses `mkdir` outside the repository, but `git worktree add` creates
  its own directory and is permitted; that is how constraint 4 was met.

## Next

1. Re-read `.agent/STOP` from disk (Phase 1 rule 1).
2. Then the Open PR Gate (rule 2).

After those, the pending handback over ee22186c..HEAD awaits review; the next
build round is T003 — the release CI stage, the changelog and tag gate, the
wheel-size budget and the seeded-failure tests.
