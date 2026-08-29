# Handback — F033 Hunk-level diff approval · ROUND 13

## Session

SESSION 4 of feature F033 · round 13 · rounds so far 13

## Range

Review of `d526dfb5bb89bf83c5a23ed506f3843b1278e496`..`55c365d6619e3b10d56b3f452b178b0db357bb91`
(C6, the commit that writes this file, follows and is tabled below under the
self-reference exception).

BASE = `d526dfb5bb89bf83c5a23ed506f3843b1278e496`, confirmed with
`git rev-parse HEAD` before C0a.

## Commits

All `+/-` cells are the two columns of `git diff --numstat <sha>^ <sha>`, read
off the tool, and were compared cell by cell against the insertion counts G8's
commit walk produced (408, 259, 14, 2, 4, 46, 91) — they agree.

### bcb3dd39 chore(f033): save the round 13 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r13.md | +408/-0 | C0a — the reviewer's block copied byte for byte with `shutil.copyfile` (NEW FILE) |

### 1a529363 chore(f033): mirror the round 13 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +259/-258 | C0b — the same bytes mirrored, so both paths hold ONE blob id |

### e2d813bc docs(f033): point the plan at the shared evidence-directory resolver
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +14/-14 | C1 — whole-file PLANF033R13, SESSION 4, round 12 closed, this round's item opened |

### 2e521057 docs(f033): book the round 12 verdict into the record
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C2 — RECORDF033R13 appended under amend0827 rule 1; a verdict buys no round of its own |

### 4202cad9 docs(f033): record the round 12 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4/-0 | C3 — SLIPSF033R13, the two dated round-12 slips, under amend0827 rule 2 |

### 8889ff60 refactor(f033): move the evidence-directory rule into evidence_index
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/evidence_index.py | +38/-0 | C4 — the moved rule as the public `resolve_job_evidence_dir` |
| packages/orchestration/ui_server.py | +8/-16 | C4 — `_resolve_evidence_dir` becomes a delegation; nothing outside that function moves |

### 55c365d6 test(f033): pin the shared evidence-directory rule and its delegation
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_evidence_index.py | +91/-0 | C5 — seven added tests plus the module docstring's property list |

### C6 (this commit) docs(f033): hand back the round 13 evidence-resolver move
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | this file | C6 — a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/g7-r13 55c365d6 --detach` | exit 0 — "Preparing worktree (detached HEAD 55c365d6)"; every G7 mutation ran here, never in the primary checkout |
| `git -C .remedy-wt/g7-r13 checkout -q d526dfb5` | exit 0 — used only to measure the BASE test count G7's control is compared against |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/g7-r13 --force` | exit 0 — removed BY EXACT PATH |
| `git worktree prune` | exit 0 — `git worktree list` then shows the primary checkout only |
| `git push -u origin feature/f033-hunk-approval-v2` | see the transcript recorded below this table |

PUSH: `git push -u origin feature/f033-hunk-approval-v2` — exit 0, branch
`feature/f033-hunk-approval-v2` updated on `origin` and tracking set. No PR was
created, edited or merged this round; no `gh` command was run.

## Verification

ONE LINE PER GATE, with real exit codes and real numbers.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again
  before C6: `ls: cannot access '.agent/STOP': No such file or directory` both
  times, so ABSENT both times. `git status --porcelain` printed empty after
  every one of the seven commits (C0a, C0b, C1, C2, C3, C4, C5). Branch
  `feature/f033-hunk-approval-v2` throughout (`git rev-parse --abbrev-ref HEAD`).
  No force-push, no history rewrite, no branch deletion; `git rev-parse
  feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
  unchanged.
- **G2 TRANSPORT — PASS.** `<C0a>:.agent/authored/f033-r13.md` = 29026 bytes,
  sha256 `7655c0b3310200d16921d6d83d82f708b389085117b637ac8ef8ee8474103a2f`;
  `.remedy-wt/f033-r13-block.md` = 29026 bytes, same sha256; EQUAL True. `git
  rev-parse <C0b>:.agent/authored/f033-r13.md` and `git rev-parse
  <C0b>:.agent/last_block.md` both print ONE blob id,
  `7499904122ed955ccac42f3f59872ae1df611bd2`.
- **G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1512826 bytes (sha256
  `dba6ffb8…6cb26`) + one newline + RECORDF033R13 (5021 bytes, sha256
  `29192f8b…57818`) = 1517848 bytes, and the C2 blob is 1517848 bytes (sha256
  `f23d379f…ecf61`) — RECONSTRUCTION EQUALS C2 BLOB True; BASE is a byte PREFIX
  True; C2 ends in exactly one newline True. (b) N COUNTED by the script = 1;
  the LAST 1 blank-line unit of the C2 blob equals the slice's single paragraph
  (len 5020) IN ORDER, True. FIRST appended paragraph byte span computed on
  BYTES: 1512827 to 1517847 (length 5020), and `c2[1512827:1517847]` equals that
  paragraph. NEGATIVE CONTROL at byte offset 1515337, PROVED inside the span
  (1512827 ≤ 1515337 < 1517847), flipping `r` → `X`: reader 1 (whole-blob
  reconstruction equality) rejects True, reader 2 (last-N paragraph compare)
  rejects True — BOTH readers reject.
- **G4 THE LEDGER at C2 — PASS.** BASE: registered `^- R-\d+ — ` 303 lines /
  303 distinct; `^Done: R-\d+ — ` 48 lines / 46 distinct; `^Landed: R-` 15;
  `^Gate: F\d+ R\d+ — ` 129; `^Gate: F033 R12 — ` 0; `^DECISION F033 D\d+ — `
  4; OPEN SET 257. C2: registered 303 / 303 UNMOVED; `Done:` 48 / 46 UNMOVED;
  `Landed:` 15 UNMOVED; `Gate:` 130 (129 → 130); `^Gate: F033 R12 — ` exactly 1
  (0 → 1); `DECISION F033 D` 4 UNMOVED; OPEN SET 257 at BOTH. Every ordered
  reading reproduced.
- **G5 THE PROSE FILES — PASS.** `.agent/plan.md` at C1: 2750 bytes, sha256
  `be7c3cc5…56417`, BYTE-EQUAL to PLANF033R13 (same length, same sha256); 49
  lines, under the 50-line cap AGENTS.md sets. `.agent/prose_slips.md`: BASE
  blob 23007 bytes + one newline + SLIPSF033R13 (785 bytes, sha256
  `4d4c4ce0…a9cfe`) = 23793 = the C3 blob, RECONSTRUCTION EQUALS C3 BLOB True,
  BASE a byte PREFIX True. `^2026-\d\d-\d\d · F033 R12 · ` = 0 at BASE and 2 at
  C3; lines beginning `- R-` in the whole file at C3 = 0.
- **G6 THE CODE AGAINST THE SPEC at C4 — PASS.** (a) `python3 -m ruff check
  packages/orchestration/evidence_index.py packages/orchestration/ui_server.py
  tests/orchestration/test_evidence_index.py` — REAL exit 0, summary line "All
  checks passed!" (run at C4 and again over the C5 tree; both exit 0, both the
  same summary line). (b) THE MOVE IS A MOVE: AST-extracted
  `resolve_job_evidence_dir`'s body from the C4 blob (quoted in full below); the
  `except` clause's exception names read `['ImportError', 'OSError',
  'ValueError', 'KeyError']` IN THAT ORDER; the text `remedy-job-evidence-`
  occurs in the body True; the names `find_record` and `load_index_records` are
  both absent (False, False). (c) THE DELEGATION: AST-extracted
  `_resolve_evidence_dir`'s body from the C4 blob of `ui_server.py` (quoted in
  full below); its call list is exactly `['resolve_job_evidence_dir']`; the
  names `json`, `resolve_data_root` and `evidence_dir_local` are all absent
  (False, False, False) and the text `remedy-job-evidence-` is absent (False).
  Its extracted signature at C4 is `'def _resolve_evidence_dir(job_id: str) ->
  Path | None:\n'` and at BASE is the same string — BYTE-IDENTICAL True.
  (d) `git show --numstat 8889ff60 -- packages/orchestration/ui_server.py` →
  `8	16	packages/orchestration/ui_server.py`, i.e. +8 / -16, and the diff hunk
  is confined to lines 164-180, the one function; nothing outside it moved.
  (e) Both functions run directly, in a `tempfile.TemporaryDirectory` with the
  CWD moved into it and a hand-written index record naming a directory that
  exists: `resolve_job_evidence_dir('jobG6')` → `/tmp/tmp8_1qpku7/ev_dir`,
  `_resolve_evidence_dir('jobG6')` → `/tmp/tmp8_1qpku7/ev_dir`, SAME VALUE True,
  NOT None True.
- **G7 THE MUTATION RED-PROOFS at C5 — PASS, all three RED.** Disposable
  worktree `/home/decodeux/Repos/remedy/.remedy-wt/g7-r13` at `55c365d6`,
  `python3 -B` throughout, import first proved to resolve to the WORKTREE's copy
  (`import packages.orchestration.evidence_index` → exit 0 →
  `/home/decodeux/Repos/remedy/.remedy-wt/g7-r13/packages/orchestration/evidence_index.py`).
  UNMUTATED CONTROL: REAL exit 0, `32 passed in 1.78s`, which exceeds the 25 the
  same file gives at BASE (measured in the same worktree at `d526dfb5`: `25
  tests collected`, then REAL exit 0 at `25 passed in 1.73s`). Each mutation's
  anchor was asserted UNIQUE inside its named file (1 occurrence each) before
  replacement, and the module was restored byte-identically after each (True
  each time):
  (i) drop the `is_dir()` check on the index branch of `evidence_index.py` —
  REAL exit 1, `1 failed, 31 passed in 1.64s`, failing test
  `tests/orchestration/test_evidence_index.py::TestResolveJobEvidenceDir::test_record_naming_an_absent_directory_answers_none`.
  (ii) make the index branch additionally require the record's `job_id` key to
  equal `job_id` (the `find_record` re-expression this round refuses) — REAL
  exit 1, `1 failed, 31 passed in 1.69s`, failing test
  `tests/orchestration/test_evidence_index.py::TestResolveJobEvidenceDir::test_record_without_a_job_id_key_still_resolves`.
  (iii) make `ui_server._resolve_evidence_dir` return None unconditionally —
  REAL exit 1, `1 failed, 31 passed in 1.73s`, failing test
  `tests/orchestration/test_evidence_index.py::TestUiServerDelegatesToTheSameRule::test_ui_server_resolver_answers_the_same_directory`.
  Post-restore control: REAL exit 0, `32 passed in 1.47s`, and `git status
  --porcelain` inside the worktree printed empty. Worktree removed BY EXACT
  PATH, then `git worktree prune`; `git worktree list` then shows the primary
  checkout only.
- **G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time,
  every REAL exit 0: `tests/orchestration/test_evidence_index.py` exit 0, `32
  passed in 1.44s` (25 at BASE); `tests/orchestration/test_final_audit_evidence.py`
  exit 0, `37 passed in 0.25s` (37 at BASE); `tests/ui_server/test_diff_endpoint.py`
  exit 0, `8 passed in 2.51s` (8 at BASE);
  `tests/orchestration/test_hunk_decision_record.py` exit 0, `15 passed in
  0.60s` (15 at BASE); `tests/test_command_catalog.py` exit 0, `18 passed in
  0.20s` (18 at BASE); canary `tests/cli/test_golden_path.py` exit 0, `42 passed
  in 20.68s` (42 at BASE). `git rev-list --reverse BASE..C5` walks SEVEN
  commits, each with exactly ONE parent, each under 500 INSERTIONS measured as
  the `+` column of `git diff --numstat`: bcb3dd39 408, 1a529363 259, e2d813bc
  14, 2e521057 2, 4202cad9 4, 8889ff60 46, 55c365d6 91. PATH SET both
  directions: touched-but-not-in-the-change-set is EMPTY; in-the-change-set-but-
  not-touched is `['.agent/handoff.md']` alone, which C6 writes and which G8
  measures at C5 — see the deviations. Delimiter residue at C5, `<<<SLICE ` /
  `<<<END `: `.agent/plan.md` 0/0, `.agent/prose_slips.md` 0/0,
  `packages/orchestration/evidence_index.py` 0/0,
  `packages/orchestration/ui_server.py` 0/0,
  `tests/orchestration/test_evidence_index.py` 0/0, against the non-zero control
  `.agent/authored/f033-r13.md` at 5/6 (5 `<<<SLICE ` = 3 real markers plus 2
  prose mentions at block lines 10 and 384; 6 `<<<END ` = 3 real markers plus 3
  prose mentions at block lines 10, 14 and 384). `git ls-files .remedy-wt` reads
  0 (empty list). DO-NOT-TOUCH PATHS, blob id at BASE vs at C5, one line per
  path — 13 of 13 identical:
  `packages/orchestration/hunk_decision_record.py` `0563c5a00660` True;
  `packages/orchestration/hunk_ledger.py` `57c00fcfde62` True;
  `packages/orchestration/hunk_apply.py` `195f0d223210` True;
  `packages/orchestration/hunk_approval.py` `25d1a8d0d08d` True;
  `packages/orchestration/hunk_subset_diff.py` `6c47c2083795` True;
  `packages/orchestration/diff_view_source.py` `30a86b1b977d` True;
  `packages/orchestration/diff_parser.py` `b6632f657426` True;
  `apps/cli/command_catalog.py` `2c71af53fae4` True;
  `apps/cli/commands/patch.py` `051789258623` True;
  `apps/cli/grouped.py` `c9c5265d0b87` True;
  `tests/ui_server/test_command_channel.py` `7ff931e2f005` True;
  `tests/test_command_catalog.py` `265c21de1d7d` True;
  `docs/roadmap/STATUS.md` `a370be066b7a` True.

### What G6 extracted, quoted

`resolve_job_evidence_dir`'s final signature, from the C4 blob of
`packages/orchestration/evidence_index.py`:

    def resolve_job_evidence_dir(job_id: str, index_dir: Path | None = None) -> Path | None:

Its AST-extracted body, from the same blob:

    """Resolve a job's evidence directory — index record first, then the local default.

    This is what decides which directory the F037 diff viewer and the F033
    decision doors read a diff out of, so both get ONE answer. A second rule
    could disagree with this one, and a decision recorded over hunks nobody was
    shown is exactly the harm the recorder's no-diff refusal exists to prevent.

    It reads ``<job_id>.json`` BY NAME and deliberately does NOT go through
    ``find_record``, which matches on the ``job_id`` key INSIDE the file: a
    record written without that key resolves here and would stop resolving
    through ``find_record``.

    ``packages/orchestration/ui_server.py``'s ``_resolve_evidence_dir`` is now a
    delegation to this function, kept only because callers import that name.
    """
    try:
        idx_file = (index_dir or job_evidence_index_dir()) / f"{job_id}.json"
        if idx_file.exists():
            record = json.loads(idx_file.read_text())
            local_dir = record.get("evidence_dir_local", "")
            if local_dir and Path(local_dir).is_dir():
                return Path(local_dir)
    # ``ImportError`` is retained from the moved original, where the data-paths
    # import sat inside this try; here that import is module level, so the name
    # is now unreachable. It is kept rather than dropped so the move stays
    # behaviour-preserving in both directions.
    except (ImportError, OSError, ValueError, KeyError):
        pass
    # RELATIVE on purpose: this resolves against the current working directory,
    # exactly as it did before the move. It is not an absolute path.
    default = Path(f"remedy-job-evidence-{job_id}")
    if default.is_dir():
        return default
    return None

`_resolve_evidence_dir`'s AST-extracted body, from the C4 blob of
`packages/orchestration/ui_server.py`:

    """Find evidence dir for a job — the implementation moved to
    `packages.orchestration.evidence_index.resolve_job_evidence_dir`, so the
    viewer here and the F033 decision doors resolve by ONE rule. The name
    survives because callers import it, including
    `tests/orchestration/test_final_audit_evidence.py`, which imports it from
    `ui_server` directly."""
    from packages.orchestration.evidence_index import resolve_job_evidence_dir
    return resolve_job_evidence_dir(job_id)

### The tests written at C5, and the property each pins

| Test | Property it pins |
|------|------------------|
| `TestResolveJobEvidenceDir::test_record_naming_an_existing_directory_resolves_to_it` | An index record whose `evidence_dir_local` EXISTS resolves to exactly that directory, as a `Path`. |
| `TestResolveJobEvidenceDir::test_record_naming_an_absent_directory_answers_none` | The discriminator for the `is_dir()` check: a NAMED but absent directory falls through to None rather than being handed back. Mutation (i) kills only this one. |
| `TestResolveJobEvidenceDir::test_record_without_a_job_id_key_still_resolves` | THE DISCRIMINATOR FOR THE WHOLE MOVE: a record file carrying NO `job_id` key still resolves, because the read is BY NAME. It fails under any re-expression through `find_record`. Mutation (ii) kills only this one. |
| `TestResolveJobEvidenceDir::test_malformed_record_falls_through_instead_of_raising` | Bytes that are not JSON fall through to None rather than raising — the `ValueError` arm of the preserved `except`. |
| `TestResolveJobEvidenceDir::test_relative_fallback_resolves_against_the_cwd` | With no index record and the CWD at `tmp_path`, a real `remedy-job-evidence-<job_id>` directory there is returned, as a RELATIVE path. |
| `TestResolveJobEvidenceDir::test_no_record_and_no_fallback_directory_answers_none` | With neither a record nor a fallback directory, the answer is None. |
| `TestUiServerDelegatesToTheSameRule::test_ui_server_resolver_answers_the_same_directory` | THE DELEGATION PROOF: `ui_server._resolve_evidence_dir` and `resolve_job_evidence_dir` answer the SAME value for the same job id, over a case that is NOT None. Mutation (iii) kills only this one. |

Every test in the first class passes `index_dir` explicitly and uses
`monkeypatch.chdir(tmp_path)`, so the relative fallback of SPEC step 4 can never
resolve against this repository's own working tree. The delegation test needs
the DEFAULT index dir, so it reuses this file's existing `isolate_data_root`
fixture, which sets `REMEDY_DATA_DIR` — no second mechanism was invented.

## Authored-text proofs

Three reviewer-authored slices applied this round, every one extracted from the
COMMITTED C0a blob (`git show <C0a>:.agent/authored/f033-r13.md`) per convention
4, never retyped:

| Slice | Applied to | Disk-to-disk result |
|-------|-----------|---------------------|
| PLANF033R13 | `.agent/plan.md` (whole file, C1) | BYTE-EQUAL: 2750 bytes, sha256 `be7c3cc5961232a45b2de055fde37972583338420d588185413ffdc1e3156417`, both sides |
| RECORDF033R13 | `.agent/live_review.md` (append, C2) | 1512826 + 1 newline + 5021 = 1517848 = the C2 blob, byte for byte; BASE a byte PREFIX |
| SLIPSF033R13 | `.agent/prose_slips.md` (append, C3) | 23007 + 1 newline + 785 = 23793 = the C3 blob, byte for byte; BASE a byte PREFIX |

The block itself: `.remedy-wt/f033-r13-block.md` was verified at 29026 bytes /
sha256 `7655c0b3310200d16921d6d83d82f708b389085117b637ac8ef8ee8474103a2f`
BEFORE anything else was done, copied to `.agent/authored/f033-r13.md` with
`shutil.copyfile`, and the committed C0a blob re-measured to the same length and
digest.

## Item-status table

Every ordered item appears exactly once.

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `.agent/authored/f033-r13.md`, `shutil.copyfile`, digest re-verified from the commit |
| C0b mirror it | done | `.agent/last_block.md`; ONE blob id `7499904122ed955ccac42f3f59872ae1df611bd2` across both paths |
| C1 `.agent/plan.md` | done | whole-file PLANF033R13, byte-equal |
| C2 the round 12 verdict into `.agent/live_review.md` | done | RECORDF033R13 appended; reconstruction exact |
| C3 the two dated prose slips into `.agent/prose_slips.md` | done | SLIPSF033R13 appended; reconstruction exact |
| C4 `resolve_job_evidence_dir` + `ui_server` delegating to it, ONE commit | done | `8889ff60`, both files in the same commit, so no tree ever holds a delegation without its target |
| C5 its tests in `tests/orchestration/test_evidence_index.py` | done | `55c365d6`, seven tests added, 25 → 32 |
| C6 the handback | done | this file |
| SPEC — `packages/orchestration/evidence_index.py` | done | one public function ADDED beside `find_record`; every existing name, signature and behaviour untouched |
| SPEC — `packages/orchestration/ui_server.py` | done | one function BODY replaced; signature byte-identical to BASE; the four call sites unchanged |
| SPEC — `tests/orchestration/test_evidence_index.py` | done | every existing test untouched and still passing; module docstring's property list extended |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS |
| G3 THE RECORD APPEND at C2 | done | PASS |
| G4 THE LEDGER at C2 | done | PASS |
| G5 THE PROSE FILES | done | PASS |
| G6 THE CODE AGAINST THE SPEC at C4 | deviated | PASS on every reading; (a) ordered "at C4" over a file whose C4 content is its BASE content — see deviation 1 |
| G7 THE MUTATION RED-PROOFS at C5 | done | PASS — all three RED, control green both before and after |
| G8 SUITES AND STRUCTURE | deviated | PASS on every reading; the path-set direction reports `.agent/handoff.md` as untouched at C5 by construction — see deviation 2 |
| Handback (`.agent/handoff.md` rewrite) | done | this file, written once |
| Push the branch | done | `git push -u origin feature/f033-hunk-approval-v2`, exit 0 |

## Deviations & assumptions

The block's ordered commit sequence was followed EXACTLY: C0a, C0b, C1, C2, C3,
C4, C5, C6 — seven commits in the measured range plus this handback commit. No
extra commit, no dropped commit, no reordering.

1. **G6(a) names a file whose C4 content is still its BASE content — declared,
   not silently resolved.** G6 is headed "at C4" and its (a) clause orders
   `ruff check` over three paths, one of which is
   `tests/orchestration/test_evidence_index.py`; but the Bundle puts that file's
   edit at C5, so at C4 it is byte-identical to BASE. The GATE is load-bearing,
   so I satisfied it literally — `python3 -m ruff check` over all three paths at
   C4, REAL exit 0, "All checks passed!" — and satisfied its INTENT by running
   the identical command again over the C5 tree, where the file carries this
   round's tests: also REAL exit 0, also "All checks passed!". Both readings are
   reported under G6 above. Nothing was changed to reconcile the two.
2. **G8's path set cannot see `.agent/handoff.md`, by construction.** The change
   set names nine paths; G8 walks `BASE..C5` and therefore sees eight. The ninth,
   `.agent/handoff.md`, is written by C6, which is after the range every gate is
   scoped to, and the block itself says "C6's own numbers are NOT ordered here".
   I report the direction honestly rather than widening the range: touched-but-
   undeclared is EMPTY, and declared-but-untouched is exactly
   `['.agent/handoff.md']`. No other path is missing and no undeclared path was
   touched.
3. **A JSON list in a record file still raises `AttributeError`, deliberately.**
   SPEC step 3 orders the `except` clause preserved exactly as found, so
   `record.get(...)` against a parsed JSON *list* still escapes this function
   uncaught, exactly as it does at BASE. I wrote no test pinning that and no
   code softening it: the SPEC calls changing it "a different change and not
   this round's". Recorded here so the absence is a decision, not an oversight.
4. **`ImportError` in the preserved `except` tuple is now unreachable.** The
   moved original imported `resolve_data_root` INSIDE the `try`; here
   `job_evidence_index_dir` is imported at module level, so no `ImportError` can
   arise from the guarded region. SPEC step 3 orders the name retained rather
   than dropped, with a comment saying so, and that is what the code carries.
   The gate reads the four names in order and passes; the reachability note is
   the code comment's.
5. **Measurement route.** The shell in this environment rejects heredocs, `$( )`
   and `$?` by FORM, so every measurement ran as a script file under the
   gitignored `.remedy-wt/` with `python3 -B`, per convention 6. `git ls-files
   .remedy-wt` reads 0, so none of it entered the tree.

No verdict is written on this round's own work, and no `Done:` paragraph was
added to `.agent/live_review.md` — `Done:` is the reviewer's word. This round
registered no finding and resolved none, so there is no `Landed:` line and no
`Landed:` commit; G4 measures registered, `Done:` and `Landed:` all UNMOVED.

## Next

SESSION 4 carries forward. The next session's first actions, in this order:

1. Read `.agent/STOP` from disk.
2. Run the Open PR Gate (`gh pr list --state open --json
   number,headRefName,baseRefName,isDraft`) and act on what it reports.
3. Book THIS round's verdict into `.agent/live_review.md` in the first commit of
   the next round — under amend0827 rule 1 this committed, pushed handback is
   the durable carrier, and a verdict buys no round of its own.
4. Then the plan's step 2: the CLI command and its handler TOGETHER, in the
   `patch` group, with `TestCatalogLookups.test_get_commands_for_group` in
   `tests/test_command_catalog.py` widened in the SAME commit. It can now take
   its evidence directory from `resolve_job_evidence_dir`, which is the one rule
   the F037 viewer already resolves by.
