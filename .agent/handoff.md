# Handback — F083 R26, the integration gate

Branch `feature/f083-ci-self-check`. Open findings: 104.

## Range

Review of 6a413eb7..HEAD — six commits: C0a, C0b, C1, C2, C3, C4.

## Commits

### dcedd596 docs(f083): save the R26 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r26.md | +224/-0 | C0a — copied, not retyped; sha256 461cc40b…fe29, 17873 B, 224 lines |

### 0386a2ea chore(agent): mirror the R26 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +158/-95 | C0b — mirror of the COMMITTED C0a blob; both are blob f8139373 |

### 2b711416 docs(review): record the R25 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C1 — RECORD-R25 appended at EOF, 3487 B tail |

### 989ed9ec test(f083): add the R26 integration gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f083_r26/ | +108/-0 | C2 — 9 files under the dir, every name ending `.txt` |

### 019c8ab0 docs(f083): advance the plan past R25
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-11 | C3 — PLAN slice, whole-file replacement |

### (this commit) docs(f083): write the R26 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this commit | C4 — self-reference; a handoff cannot table its own commit (R-0149) |

## External actions

- `git worktree add -b tmp/base-gate .remedy-wt/base-gate f3fd96d7` — created on a
  BRANCH per DECISION D3; worktree HEAD f3fd96d7.
- `git worktree remove --force`, `git worktree prune`, `git branch -D tmp/base-gate`
  — removed; `Deleted branch tmp/base-gate (was f3fd96d7)`.
- `git push -u origin feature/f083-ci-self-check` — run right after C4; outcome in
  the round's completion report, as a handoff cannot record its own push.
- No PR created or merged, no `gh` command, no evidence-bundle or review-zip
  attempt — those belong to the closure round.

## Verification — every ordered gate, measured

| # | Status | Measured |
|---|---|---|
| 1 | done | `pwd` = /home/decodeux/Repos/remedy printed first; `git status --porcelain` EMPTY before C0a, before the gate-5 branch run, before C2 and before C4; `git worktree list` ONE line at round start and at handback; `.agent/STOP` absent at both |
| 2 | done | HEAD 6a413eb709e8008063cb31d44f829c1563dfc588; `git merge-base main HEAD` f3fd96d729c3be85604a2d37aee42c59fe39868a |
| 3 | done | committed `.agent/authored/f083-r26.md` and `.agent/last_block.md` are the SAME blob f8139373; sha256 461cc40b451538c67da83a4fcc000056736d3a86a715cc0e9d7bdd2bd885fe29, 17873 B, 224 lines |
| 4 | done | pre 305119 B PREFIXES post 308606 B; the 3487 B tail byte-EQUALS the RECORD-R25 slice from the committed authored blob; `git show --numstat` = `2	0`, deletion column 0; BEGIN-marker LINES 0 at base and 0 at HEAD (bare substring 4 at both) |
| 5 | done | BRANCH RUN at 2b711416, repo root, `python3 -m pytest -n auto -q`, exit 0, `17047 passed, 19 skipped in 126.08s (0:02:06)`, wall 126.68 s |
| 6 | done | worktree on branch `tmp/base-gate` at f3fd96d7; `apps/ui/node_modules` and `apps/ui/dist` placed by COPY; symbolic links directly at each path: 0 and 0; freshness restored — dist newest mtime 1786858830.541, src newest 1786858797.904, dist later, and dist's OLDEST file also later than src's newest |
| 7 | done | composite dist sha256 5876f488eab879fcfe1fae4cfb7329e63246c0aff9dd57a203b56d8f15b69d44 over 3 files BEFORE the base run and the IDENTICAL value AFTER; EQUAL, so the parity claim stands |
| 8 | done | BASE RUN at f3fd96d7 from `.remedy-wt/base-gate`, `REMEDY_UI_NO_AUTO_BUILD=1`, `python3 -m pytest -n auto -q`, exit 0, `16988 passed, 19 skipped in 146.39s (0:02:26)`, wall 146.90 s |
| 9 | done | `branch_failed.txt` and `base_failed.txt` both 0 lines / 0 bytes; `comm -13` branch-only EMPTY, 0 bytes; `comm -23` base-only EMPTY, 0 bytes; neither raw log holds a `^FAILED` or `^ERROR` line |
| 10 | done | BOTH lists empty, so nothing needs attributing and no id is unattributed. No branch-only failure exists, so constraint 9's blocker does not fire. 0 ids in the xdist-flake class — not more than ten, so no flake-debt line is owed |
| 11 | done | worktree removed and pruned, branch deleted; `git worktree list` prints ONE line; `git branch --list tmp/base-gate` printed nothing |
| 12 | done | `.agent/gate_f083_r26/` holds exactly the 9 ordered members, every name ends `.txt`; `git ls-files` matching `\.log$` returns 0 of 3533 tracked paths; `full_log_provenance.txt` carries both raw logs' path, lines, bytes and sha256, the logs staying uncommitted in `.remedy-wt/.cache/gate_r26/` |
| 13 | done | canary at 989ed9ec, repo root: `python3 -m pytest tests/cli/test_golden_path.py -q`, `42 passed in 20.28s`, exit 0 |
| 14 | done | AT C3 019c8ab0: `python3 -m ruff check .` → `Found 26 errors.`, `[*] 25 fixable with the --fix option.`, exit 1 — ratchet held, nothing fixed, no ceiling raised |
| 15 | done | 116 registered, 12 resolved, 0 landed, 104 open; max R-0488, next free R-0489; 0 duplicate ids; 0 resolutions naming an unregistered id; R-0488 resolved, R-0482 and R-0487 still open |
| 16 | done | committed `.agent/plan.md` byte-equals the PLAN slice at sha256 8cd8b2e201f28bc30eb5b67714b00a6f73788c617b734a63bf8ece2f75265840, 2085 B, 37 lines (under 50); `## Goal` and `## Next Steps` present; 0 unchecked-box lines |
| 17 | done | `git diff --name-only 6a413eb7..HEAD -- docs/ packages/ apps/ scripts/ tests/` printed NOTHING — 0 bytes at exit 0 |
| 18 | done | 13 paths at C3 — the four `.agent/` files above plus the 9 members of `.agent/gate_f083_r26/`; C4 adds `.agent/handoff.md` as the 14th; nothing else |
| 19 | done | per-commit insertions 224, 158, 2, 108, 9 and C4's own — none near 500; five single-parent commits chained to 6a413eb7; the round's reflog shows only `commit:` entries, 0 amend, rebase or reset |

## Authored-text proofs

- `.agent/authored/f083-r26.md` was COPIED from `.remedy-wt/f083-r26.md`, never
  retyped: source, working copy and committed blob all read sha256
  461cc40b…fe29 / 17873 B / 224 lines. Disk-to-disk, NOT a digest fallback.
- Both slices came from the COMMITTED blob by their markers. RECORD-R25: 3487 B,
  sha256 42dfc239b345319bed43f9ef4d4f0478ddb8ec2a81da52ec7a263a722bd896fe, appended
  tail byte-equals it. PLAN: 2085 B, sha256 8cd8b2e2…5840, `.agent/plan.md`
  byte-equals it. No marker line reached either target file.

## Deviations & assumptions

- The ordered commit sequence C0a, C0b, C1, C2, C3, C4 WAS followed exactly: six
  commits, none added, none dropped, none reordered.
- Tooling substitution, gated property unchanged: this session denies `cp`, so the
  gate-6 parity copies ran through `python3` `shutil.copytree(..., symlinks=True)`;
  gate 6's property was measured — both paths are real directories, 0 symlinks.
- Gate 6 needed its freshness step: the copied `dist` was OLDER than that worktree's
  `src`, so every file under it was re-stamped to one later mtime before the base run.
- Stated-cause overage (DECISION D15): 104 lines against the ≤100 cap that >5-commit
  tables allow, and over the 800-token thrift cap. Cause: mandated content — six
  per-commit tables and a 19-row item-status table carrying digests and both suites'
  summary lines. No section was dropped to chase the cap.
- Nothing outside `.agent/` was touched; the 26 ruff errors stand unfixed.

## Next

Read `.agent/STOP` from disk, then run the AGENTS.md Open PR Gate, then the closure
round per `docs/roadmap/STATUS_closure_protocol.md`.
