# Handback — F110 Model routing by task class, round 2 — T001b, THE SINGLE RESOLVER SEAM

## Session

SESSION 1 of feature F110 · round 2 · rounds so far 2

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 2 rounds and 1 session it is nowhere near, so no scope report is due.
`.agent/STOP` was read from disk twice — before the first commit (C0a) and again
before C6 — and does not exist at either point.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **BASE** | `bbfbb83b` — the round 1 handback commit |
| **Runde** | 2 (Session 1) — T001b: consolidation order E.a, the production seam |
| **Fortschritt** | ~25 % (T001a ✅ inventory · T001b ✅ the resolver seam · T001c, T002, T003 open) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. ALLE GRÜN. |
| **Offene Findings** | 278 (Mengendifferenz über 347 registrierte und 69 aufgelöste ids; −1 gegen Runde 1, weil `R-0768` diese Runde BY NAME aufgelöst wurde) |

THIS ROUND CHANGED PRODUCTION CODE. `packages/orchestration/pingpong_job.py`
no longer answers "which provider is the product default" with a literal: the
new `default_role_provider_name` returns an injected provider's own `name` when
one was passed and otherwise `role_config.resolve_role_config(role).provider`.
That is consolidation order E.a of the T001a inventory and it is also `R-0768`'s
own expected fix, which is why the finding is resolved by name in the same round.

## Range

Review of `bbfbb83b..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `03cfd2c6` | done | block written verbatim to `.agent/authored/f110-r2.md`, 263 insertions |
| C0b `0a9fe003` | done | mirrored with `shutil.copyfile`; one sha256 for both copies (G1) |
| C1 `ff9dcce3` | done | PLAN2 extracted by delimiter index from the COMMITTED authored copy and applied whole; `cmp` exit 0, 46 lines. FIRST substantive commit |
| C2 `299e7c64` | done | RECORD1 appended to `.agent/live_review.md` and SLIPS2 to `.agent/prose_slips.md`, each with the two-byte separator; full arithmetic in G3, byte-equality in G4 |
| C3 `5bbb0cde` | done | THE PRODUCTION COMMIT — the new function plus the two third arguments, +28 / -2, nothing else (G5) |
| C4 `fd92ce72` | done | THE TEST COMMIT — the new 14-test file and exactly six fixture repairs, no assertion weakened |
| C5 `9bd3ea87` | done | DONE1 appended; `R-0768` resolved by name, AFTER C3 and C4, as constraint 3 fixes the order |
| C6 (this commit) | done | handback rewritten per `docs/agents/handback_template.md` |

Every ordered item appears exactly once. No item was skipped and none deviated
from its ordered position.

## Commits

### 03cfd2c6 F110 R2 C0a: save the round 2 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r2.md` | +263 / -0 | the reviewer's block saved verbatim; the first link of the transport chain |

### 0a9fe003 F110 R2 C0b: mirror the round 2 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +212 / -347 | round 1's block replaced by this one; byte-identical copy of the authored file |

### ff9dcce3 F110 R2 C1: the plan turns to T001b, the single resolver seam
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20 / -17 | PLAN2 applied whole; 46 lines, under the AGENTS.md 50-line rule |

### 299e7c64 F110 R2 C2: book the round 1 PASS verdict and its prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD1 appended — round 1's PASS verdict, booked in the first substantive-adjacent commit of the next round (amend0827 rule 1) |
| `.agent/prose_slips.md` | +7 / -1 | SLIPS2 appended — three dated reviewer/worker prose slips; no R-id spent (amend0827 rule 2) |

### 5bbb0cde F110 R2 C3: resolve run_job provider defaults through role_config
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_job.py` | +28 / -2 | the new module-level `default_role_provider_name` immediately above `_resolve_cfg`, plus the two third arguments at the builder and reviewer call sites. Nothing else moved |

### fd92ce72 F110 R2 C4: pin the resolver seam and repair the six literal-default fixtures
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_role_routing.py` | +84 / -0 | 14 unit tests over the pure function only; every uninjected expectation states `role_config.resolve_role_config(role).provider`, never the literal `"ollama"` |
| `tests/orchestration/test_job_task_runner.py` | +9 / -5 | the six named fixtures now pass `builder="fake", reviewer="fake"`; no assertion weakened, no test deleted, no expected value changed |

### 9bd3ea87 F110 R2 C5: resolve R-0768 by name in the ledger
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | DONE1 appended AFTER the production and test commits, which is what lets it state facts about its own round |

### C6 (this commit) F110 R2 C6: the round 2 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern). Its own numbers go to neither a round report nor this file, per the block: the reviewer measures them at the next gate |

The `+` column above is the INSERTION count from `git show --numstat`
(AGENTS.md DECISION F104 D1). The cell-by-cell comparison is in G8.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f110r2_mut fd92ce72` | `Preparing worktree (detached HEAD fd92ce72)` — the G6 red proof ran ONLY here |
| `git worktree remove .remedy-wt/f110r2_mut` | removed; `git worktree list` afterwards shows no worktree of this round's making |
| `git worktree prune` | no output |
| `git push -u origin feature/f110-model-routing-by-task-class` | run after this commit; the real result is in the completion report |

No pull request was created and nothing was merged, as the block orders. Nothing
was force-pushed, no history was rewritten, no commit was made on `main`. The
five `.remedy-wt/job-*` worktrees listed by `git worktree list` are retained job
worktrees from earlier features; this round created none of them and removed
none of them.

## Verification

One line per gate first, then the transcripts.

| Gate | Reading |
|---|---|
| G1 TRANSPORT | GREEN — one sha256 twice, `f7a27a7f…4f27c`. WORKER SELF-CONSISTENCY ONLY: the reviewer stated it holds no scratch original, so this proves the mirror equals the saved copy and nothing about the emitted bytes (§3 item 37) |
| G2 THE PLAN | GREEN — `cmp` exit 0, 46 lines (< 50), `^## Goal` 1, `^## Next Steps` 1 |
| G3 THE TWO LEDGER APPENDS | GREEN — RECORD1 2140941 + 2 + 5690 = 2146633 real; DONE1 2146633 + 2 + 2425 = 2149060 real; both second readers accept IN ORDER, both negative controls REJECT; the two greps read 0 before / 1 after, each in its own commit |
| G4 THE PROSE FILE | GREEN — `.agent/prose_slips.md` final 1545 bytes byte-equal to the extracted SLIPS2, pre-C2 content an exact byte PREFIX, file still ends WITHOUT a newline |
| G5 THE PRODUCTION CHANGE | GREEN — +28 / -2, `"fake")` 5 before / 3 after, `default_role_provider_name` 3 after, `ast.parse` exit 0; the diff is the new function plus the two third arguments and nothing else |
| G6 THE MUTATION RED PROOF | GREEN, AND THE DISCRIMINATOR HOLDS — control 14 passed exit 0; mutated 9 failed / 5 passed exit 1, every reddened id a no-injection assertion, every injected-provider test still GREEN. Ran only in the disposable worktree, which is removed and pruned |
| G7 THE SUITES | GREEN — 191, 75, 383, 14, 42, each its own invocation, run serially, every one exit 0. The task-runner count HELD at 191: no seventh test moved |
| G8 THE TREE, THE COMMITS AND THE SWEEP | GREEN — tree EMPTY before C6 was staged, `git ls-files .remedy-wt` no output, no worktree of this round's making, all nine insertion cells agree with the Commits table |

### G1 TRANSPORT — GREEN

    $ sha256sum .agent/authored/f110-r2.md .agent/last_block.md
    f7a27a7fb401e8d4859af018daa75ebd3f06515da8e4716f27f3276d70c4f27c  .agent/authored/f110-r2.md
    f7a27a7fb401e8d4859af018daa75ebd3f06515da8e4716f27f3276d70c4f27c  .agent/last_block.md
    REAL_EXIT=0

One digest, twice, both lines verbatim. The reviewer stated up front that it
holds no scratch original this round, so this is WORKER SELF-CONSISTENCY ONLY:
it proves the mirror equals the saved copy and nothing about what the reviewer
emitted. That is the §3 item 37 shape and it is reported as such, not
overclaimed. Every APPLIED slice below was extracted BY DELIMITER INDEX from the
COMMITTED `.agent/authored/f110-r2.md` — read with
`git show HEAD:.agent/authored/f110-r2.md`, never from the working copy — and
written by script. Nothing was retyped. Each marker string was asserted to occur
exactly once before any write.

    PLAN2    begin line  200  end line  247   46 lines   2224 bytes (with trailing newline)   2223 without
    RECORD1  begin line  249  end line  251    1 line    5691 bytes (with trailing newline)   5690 without
    SLIPS2   begin line  253  end line  259    5 lines   1546 bytes (with trailing newline)   1545 without
    DONE1    begin line  261  end line  263    1 line    2426 bytes (with trailing newline)   2425 without

Constraint 4 settles which form each target takes: `.agent/plan.md` ends WITH a
newline and took the 2224-byte form; `.agent/live_review.md` and
`.agent/prose_slips.md` end WITHOUT one and took the 5690 / 2425 / 1545 forms.
The TARGET's convention wins, exactly as ordered, so round 1's SLIPS1 ambiguity
does not recur and there is nothing to declare here.

### G2 THE PLAN — GREEN

    $ cmp .remedy-wt/f110r2/PLAN2.extracted .agent/plan.md
    (no output)
    REAL_EXIT=0
    $ wc -l .agent/plan.md
    46 .agent/plan.md            (must be under 50 — it is)
    REAL_EXIT=0
    $ grep -c '^## Goal' .agent/plan.md
    1
    REAL_EXIT=0
    $ grep -c '^## Next Steps' .agent/plan.md
    1
    REAL_EXIT=0

### G3 THE TWO LEDGER APPENDS — GREEN, FULL ARITHMETIC

THE COUNTS TAKEN BEFORE EACH COMMIT, so the 1 is provably this round's append
and not a pre-existing line. `grep -c` exits 1 when it counts 0; that is the
real exit code and it is reported rather than smoothed:

    BEFORE C2:  $ grep -c '^Gate: F110 R1 — ' .agent/live_review.md   -> 0   REAL_EXIT=1
    BEFORE C2:  $ grep -c '^Done: R-0768 — ' .agent/live_review.md    -> 0   REAL_EXIT=1
    BEFORE C5:  $ grep -c '^Done: R-0768 — ' .agent/live_review.md    -> 0   REAL_EXIT=1
    AFTER  C5:  $ grep -c '^Gate: F110 R1 — ' .agent/live_review.md   -> 1   REAL_EXIT=0
    AFTER  C5:  $ grep -c '^Done: R-0768 — ' .agent/live_review.md    -> 1   REAL_EXIT=0

(a) RECORD1 at C2, against the file size IMMEDIATELY BEFORE that commit:

    size BEFORE C2                      2140941
    separator bytes                           2   (newline newline)
    RECORD1 slice length                   5690   (extractor yields 5691; the target takes no trailing newline)
    before + 2 + slice                  2146633
    real new size                       2146633
    equal                                  True
    new file ends WITHOUT a newline        True
    pre-append content an exact PREFIX     True
    final 5690 bytes equal the slice       True

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, never taken from the
block: N = 1.

    blank-line units in the WHOLE file                  897
    unit[-1] equals RECORD1 paragraph 1: True (len 5671 vs 5671 characters)
    last N file units == RECORD1 paragraphs IN ORDER:   True

NEGATIVE CONTROL, on a SCRATCH COPY under `.remedy-wt/` — the tracked file was
never mutated:

    first appended paragraph found at byte offset   2140943
    flipped byte at offset 2143788 (was 'A') with XOR 0x01
    second reader ACCEPTS the mutated copy:         False
    second reader REJECTS it:                       True

(b) DONE1 at C5, against the file size IMMEDIATELY BEFORE that commit:

    size BEFORE C5                      2146633
    separator bytes                           2
    DONE1 slice length                     2425   (extractor yields 2426)
    before + 2 + slice                  2149060
    real new size                       2149060
    equal                                  True
    new file ends WITHOUT a newline        True
    pre-append content an exact PREFIX     True
    final 2425 bytes equal the slice       True

    N counted BY THE SCRIPT from the DONE1 slice        1
    blank-line units in the WHOLE file                  898
    unit[-1] equals DONE1 paragraph 1: True (len 2415 vs 2415 characters)
    last N file units == DONE1 paragraphs IN ORDER:     True

    first appended paragraph found at byte offset   2146635
    flipped byte at offset 2147847 (was 'i') with XOR 0x01
    second reader ACCEPTS the mutated copy:         False
    second reader REJECTS it:                       True

The byte length (5690 / 2425) and the character length (5671 / 2415) differ
because both paragraphs carry multi-byte characters; both readings are of the
same string and neither is a discrepancy.

### G4 THE PROSE FILE — GREEN, BYTE-EQUALITY ONLY

Which is all amend0827 rule 5 allows a `.agent/` prose file:

    size BEFORE C2                        48513
    separator bytes                           2
    SLIPS2 slice length                    1545
    before + 2 + slice                    50060
    real new size                         50060
    equal                                  True
    file's final 1545 bytes equal the extracted SLIPS2 slice:   True
    pre-C2 content preserved as an exact byte PREFIX:           True
    file still ends WITHOUT a newline:                          True

### G5 THE PRODUCTION CHANGE — GREEN

    $ git show --numstat 5bbb0cde -- packages/orchestration/pingpong_job.py
    28	2	packages/orchestration/pingpong_job.py
    REAL_EXIT=0

Counts read from the git OBJECTS, not from the working copy, so BEFORE means
`5bbb0cde^` and AFTER means `5bbb0cde`. Both the occurrence count and the
line count are reported; they are identical here:

    BEFORE C3   occurrences of '"fake")': 5    lines containing it: 5
    AFTER  C3   occurrences of '"fake")': 3    lines containing it: 3
    BEFORE C3   occurrences of 'default_role_provider_name': 0    lines: 0
    AFTER  C3   occurrences of 'default_role_provider_name': 3    lines: 3

The three surviving `"fake")` occurrences are `builder=d.get("builder", "fake")`
and `reviewer=d.get("reviewer", "fake")` in the execution-config DESERIALIZER,
and `getattr(attempt, "provider", "fake") == "fake"` in an evidence reader —
none of them the run-time product default this round was ordered to move.

    $ python3 -c "import ast,pathlib;ast.parse(pathlib.Path('packages/orchestration/pingpong_job.py').read_text())"
    (no output)
    REAL_EXIT=0

THE DIFF, ADDED AND REMOVED LINES VERBATIM:

    +# The recorded provider must NAME WHAT ACTUALLY RAN: a literal default made an
    +# unflagged run report a provider it never used (finding R-0768). One function so
    +# ``run_job``'s own precedence chain stops being a rival answer to role_config's.
    +def default_role_provider_name(role: str, injected_provider: Any = None) -> str:
    +    """Return the provider name to record for ``role`` when nothing was given.
    +
    +    Used as ``_resolve_cfg``'s product default, i.e. only when neither an
    +    explicit CLI value nor a persisted one exists. An INJECTED provider object
    +    wins, because that object is what will really run; otherwise the answer
    +    comes from ``role_config``, the single seam that owns provider defaults.
    +
    +    ``role_config`` is imported inside the body on purpose: this module has no
    +    module-level import of it, and adding one risks an import cycle.
    +    """
    +    if injected_provider is not None:
    +        name = getattr(injected_provider, "name", None)
    +        if isinstance(name, str) and name:
    +            return name
    +
    +    from packages.orchestration import role_config
    +
    +    return role_config.resolve_role_config(role).provider
    +
    +

    -        builder_name, ec.builder if ec else None, "fake")
    +        builder_name, ec.builder if ec else None,
    +        default_role_provider_name("builder", builder_provider))
    -        reviewer_name, ec.reviewer if ec else None, "fake")
    +        reviewer_name, ec.reviewer if ec else None,
    +        default_role_provider_name("reviewer", reviewer_provider))

That is the whole diff: the new function immediately above the single
`def _resolve_cfg(` line, plus the two third arguments. `max_rounds`,
`test_command`, `claude_cli_write_mode` and every later `_resolve_cfg` call keep
their current defaults, and the SOURCE taxonomy is untouched — a resolved
default still reports source `"default"`.

THE SHIPPED FUNCTION WAS RUN, not merely read:

    default_role_provider_name('builder')                    -> 'ollama'
    default_role_provider_name('reviewer')                   -> 'ollama'
    default_role_provider_name('builder', <name='fake'>)     -> 'fake'
    default_role_provider_name('builder', <no name attr>)    -> 'ollama'
    role_config.resolve_role_config('builder').provider      -> 'ollama'

### G6 THE MUTATION RED PROOF — GREEN, AND THE DISCRIMINATOR HOLDS

Ran ONLY inside a disposable worktree at the C4 commit, never in the primary
checkout. Every invocation purged `__pycache__` inside that worktree first and
ran with `python3 -B`; the imported module path was printed before each run, so
the mutation demonstrably reaches the test rather than being shadowed:

    imported module file inside the worktree:
    /home/decodeux/Repos/remedy/.remedy-wt/f110r2_mut/packages/orchestration/pingpong_job.py

THE UNMUTATED CONTROL FIRST, as ordered:

    --- CONTROL, UNMUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_job_role_routing.py -q
    14 passed in 0.26s
    REAL_EXIT=0

THE MUTATION — only the fallback line of `default_role_provider_name`, so the
function returns the literal `"fake"` when no provider is injected:

    -    return role_config.resolve_role_config(role).provider
    +    return "fake"

    --- MUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_job_role_routing.py -q
    FFFFF.....FFFF
    9 failed, 5 passed in 0.24s
    REAL_EXIT=1

THE IDS THAT WENT RED — every one a NO-INJECTION assertion:

    TestNoInjectedProvider::test_resolves_through_role_config[builder]
    TestNoInjectedProvider::test_resolves_through_role_config[reviewer]
    TestNoInjectedProvider::test_explicit_none_is_the_same_as_omitting_it[builder]
    TestNoInjectedProvider::test_explicit_none_is_the_same_as_omitting_it[reviewer]
    TestNoInjectedProvider::test_the_two_roles_agree_with_their_own_role_config_entries
    TestUnusableInjectedName::test_falls_back_to_role_config[no-attribute]
    TestUnusableInjectedName::test_falls_back_to_role_config[name-is-none]
    TestUnusableInjectedName::test_falls_back_to_role_config[name-is-empty]
    TestUnusableInjectedName::test_falls_back_to_role_config[name-not-a-str]

    typical failure: AssertionError: assert 'fake' == 'ollama'

THE IDS THAT STAYED GREEN under the mutant — every INJECTED-PROVIDER test, plus
one shape check:

    TestInjectedProvider::test_injected_fake_provider_resolves_to_fake          GREEN
    TestInjectedProvider::test_injected_name_wins_over_the_role_config_answer   GREEN
    TestInjectedProvider::test_injection_is_honoured_for_either_role[builder]   GREEN
    TestInjectedProvider::test_injection_is_honoured_for_either_role[reviewer]  GREEN
    TestNoInjectedProvider::test_the_answer_is_a_non_empty_provider_name        GREEN

So the discriminator is satisfied: the no-injection case reddens while the
injected-provider case stays green. NOT ALL FIVE GREENS ARE INJECTED CASES and
that is stated rather than glossed — `test_the_answer_is_a_non_empty_provider_name`
asserts the return is a non-empty `str`, which `"fake"` also is, so it is a shape
check and cannot discriminate. Every no-injection test that names a VALUE went
red; see D5.

THE REVERT WAS PROVED, not assumed:

    --- REVERTED to the committed bytes ---
    14 passed in 0.27s
    REAL_EXIT=0
    $ git -C .remedy-wt/f110r2_mut status --porcelain
    (no output — the worktree carried the committed bytes again)

    $ git worktree remove .remedy-wt/f110r2_mut
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  9bd3ea87 [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

No worktree of THIS round's making remains; the five `job-*` entries predate it.

### G7 THE SUITES — GREEN, EACH AS ITS OWN INVOCATION, RUN SERIALLY

Never two pytest processes alive at once. Exit codes come from
`subprocess.run(...).returncode`, never from a pipe (R-0438).

    $ python3 -m pytest tests/orchestration/test_job_task_runner.py -q
    191 passed in 97.33s (0:01:37)
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_role_config.py tests/orchestration/test_provider_mode.py tests/orchestration/test_execution_config_evidence.py -q
    75 passed in 0.86s
    REAL_EXIT=0

    $ python3 -m pytest tests/test_do_job_flow.py tests/orchestration/test_repair_loop.py tests/orchestration/test_long_run_executor.py -q
    383 passed in 28.93s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_job_role_routing.py -q
    14 passed in 0.22s
    REAL_EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.64s
    REAL_EXIT=0

191, 75, 383, 14, 42. THE FIRST COUNT HELD AT 191 WITH THE SIX FIXTURES
REPAIRED, which is the reading the block made load-bearing: no SEVENTH test
moved, so there is nothing to report as a finding on that clause. The new file
reports 14. The last invocation is the canary every handback owes.

### G8 THE TREE, THE COMMITS AND THE SWEEP — GREEN

Read immediately before C6 was staged:

    $ git status --porcelain
    (no output — the tree is EMPTY)
    REAL_EXIT=0
    $ git ls-files .remedy-wt
    (no output)
    REAL_EXIT=0

`git ls-files .remedy-wt` returns NOTHING, so every scratch script, extracted
slice and negative-control copy this round wrote is untracked and cannot enter
the review subject.

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared CELL BY CELL against the Commits table above:

    commit     path                                          numstat +   table +   agree
    03cfd2c6   .agent/authored/f110-r2.md                          263       263    yes
    0a9fe003   .agent/last_block.md                                212       212    yes
    ff9dcce3   .agent/plan.md                                       20        20    yes
    299e7c64   .agent/live_review.md                                 3         3    yes
    299e7c64   .agent/prose_slips.md                                 7         7    yes
    5bbb0cde   packages/orchestration/pingpong_job.py               28        28    yes
    fd92ce72   tests/orchestration/test_job_role_routing.py         84        84    yes
    fd92ce72   tests/orchestration/test_job_task_runner.py           9         9    yes
    9bd3ea87   .agent/live_review.md                                 3         3    yes

Per-commit insertion totals: C0a 263, C0b 212, C1 20, C2 10, C3 28, C4 93,
C5 3. Every one is far under the 500-insertion cap. C6's own numbers go to
NEITHER a round report NOR this file, per the block: the reviewer measures them
at the next gate.

**THE STALENESS SWEEP over every file this round touched, one entry per file.**

1. `.agent/authored/f110-r2.md` — NOT stale by construction. A verbatim copy of
   the reviewer's block; nothing in it is edited regardless of what any later
   measurement shows.
2. `.agent/last_block.md` — NOT stale, same reason, same bytes, same digest.
3. `.agent/plan.md` — NOT stale. Its `## Current Step` describes exactly what
   this round did, and both Risk bullets were CONFIRMED by the round rather than
   left as predictions: six CLI-handler tests did encode the old default and
   were repaired, no seventh moved (G7), and `R-0767` is still OPEN, measured by
   set difference over the ledger this round. `## Next Steps` names T001c as
   consolidation order E.b, which is where the inventory's section E puts it.
4. `.agent/live_review.md` — NOT stale, with one clause a reader should not
   mistake for staleness: `R-0768`'s ORIGINAL registration line still ends
   `OPEN.` and was deliberately not edited. That is this ledger's own
   append-only convention, not an oversight — `R-0761`'s registration line ends
   `OPEN.` too, beside its `Done: R-0761` entry, and the `Done:` line is what
   carries resolution. Editing the historical line would rewrite the record.
5. `.agent/prose_slips.md` — NOT stale. Three dated records of round 1 prose
   slips; each is a statement about a past round and is true of it. Append-only,
   never renumbered, and nothing here gates anything.
6. `packages/orchestration/pingpong_job.py` — NOT stale. The docstring of
   `run_job` still reads "explicit CLI value > persisted config > product
   default", which is exactly what the module now does; only the ANSWER to
   "product default" changed, from a literal to role_config's. The new
   function's own comment names the finding it repairs, per AGENTS.md Code
   Discoverability.
7. `tests/orchestration/test_job_role_routing.py` — NOT stale, and it is the
   file most at risk of going stale, so it is written not to: every uninjected
   expectation is computed from `role_config.resolve_role_config(role).provider`
   at assert time, so a legitimate change of product default cannot falsify it.
   The only literals it asserts are `"fake"` for an INJECTED provider named
   `fake`, which is a statement about injection and not about the default.
8. `tests/orchestration/test_job_task_runner.py` — NOT stale. The six repaired
   fixtures now STATE the fake run their own docstrings already claim ("Normal
   fake two-task job still completes through handler"); no assertion, expected
   value or test was touched otherwise.
9. `.agent/handoff.md` — this file; written once, per the write-once rule.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. Sentences outside it that this round
makes stale are DECLARED, NOT REPAIRED, per constraint 7 — see D6 and D7.

## Authored-text proofs

Every applied reviewer-authored text was extracted by delimiter index from the
COMMITTED `.agent/authored/f110-r2.md` (read with
`git show HEAD:.agent/authored/f110-r2.md`, not from the working copy) and
written to its target BY SCRIPT. Nothing was retyped.

| Authored text | Proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `sha256sum` of `.agent/authored/f110-r2.md` and `.agent/last_block.md` | one digest twice | `f7a27a7f…4f27c` twice | 0 |
| PLAN2 (46 lines, 2224 bytes) | `cmp .remedy-wt/f110r2/PLAN2.extracted .agent/plan.md` | identical | identical | 0 |
| RECORD1 (5690 bytes applied) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |
| SLIPS2 (1545 bytes applied) | final-bytes byte-equality + exact byte prefix + newline convention | True / True / True | True / True / True | — |
| DONE1 (2425 bytes applied) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |

The production code and the tests are NOT authored text: the block described
them and the worker wrote them (SPEC CODE, SPEC TESTS), so they carry no
transport proof and are gated by G5, G6 and G7 instead.

## Deviations & assumptions

**D1 — NONE OF THE BLOCK'S ORDERED COMMIT SEQUENCE WAS DEPARTED FROM.** C0a,
C0b, C1, C2, C3, C4, C5, C6 ran in exactly that order, with exactly the nine
paths the change set names and nothing else. No commit was added, dropped or
reordered. Constraint 3's fixed order — production, then tests, then the DONE1
append — was honoured, which is what lets DONE1 speak about its own round.
This entry exists because the handback template asks for the departure to be
named HERE even when there is none.

**D2 — THREE OF THE SIX REPAIRED TESTS HAVE TWO `_make_args` CALLS AND I
REPAIRED ONLY THE FIRST OF EACH, DELIBERATELY.** The block says to pass
`builder="fake"` and `reviewer="fake"` "to its `_make_args(...)` call",
singular. In `test_full_pause_continue_cycle`,
`test_cli_handler_max_rounds_continuation` and `test_no_config_drift_in_report`
the second call is the CONTINUATION run, which exists precisely to restate no
flags — and in the neighbouring `test_full_config_preserved_through_pause`,
which the block did NOT list, the same shape asserts
`builder_source == "persisted"`. Naming the provider at the continuation call
would have turned a persisted source into a cli source and weakened what those
fixtures prove. Repairing only the first call is sufficient and measured: all
six are green and the suite held at 191. Declared because "its call" admits the
other reading.

**D3 — I ADDED TYPE ANNOTATIONS THE SPEC'S LITERAL SIGNATURE DID NOT SHOW.**
The block writes `def default_role_provider_name(role, injected_provider=None)
-> str`; I shipped `def default_role_provider_name(role: str,
injected_provider: Any = None) -> str`. Same name, same parameters, same return
type, annotated in the module's own style — its immediate neighbour reads
`def _resolve_cfg(cli_val: Any, persisted_val: Any, default: Any) ->
tuple[Any, str]` and the module runs `from __future__ import annotations` with
`Any` already imported. Declared rather than assumed to be invisible.

**D4 — THE DEFAULT IS NOW EVALUATED EAGERLY AT EVERY `run_job` CALL, INCLUDING
CALLS WHERE AN EXPLICIT OR PERSISTED VALUE WINS.** Python evaluates arguments
before the call, so `default_role_provider_name(...)` runs even when
`_resolve_cfg` will discard its result. This is safe and I verified WHY rather
than assuming it: `resolve_role_config` is pure — it reads its arguments,
consults module-level default tables and returns a frozen dataclass; it opens no
file, writes no state and, for the two KNOWN_ROLES `builder` and `reviewer`,
emits no warning. The alternative (a lazy sentinel) would have changed
`_resolve_cfg`'s contract, which the block forbids. Declared because the block's
wording — "the provider NAME to record for `role` when neither an explicit value
nor a persisted one was given" — describes WHEN the value is USED, and a reader
could take it to describe when the function RUNS.

**D5 — ONE TEST STAYED GREEN UNDER THE MUTANT THAT IS NOT AN INJECTED-PROVIDER
TEST, AND I AM NAMING IT RATHER THAN REPORTING A CLEAN COLOUR.**
`TestNoInjectedProvider::test_the_answer_is_a_non_empty_provider_name` asserts
the return is a non-empty `str`; the mutant returns `"fake"`, which satisfies
that. It is a shape check and cannot discriminate, by construction. The G6
discriminator is still satisfied on its own terms — every no-injection
assertion that names a VALUE went red (9 ids) and every injected-provider test
stayed green (4 ids) — but "5 passed" is not "5 injected cases passed", and the
difference is stated here so the reviewer does not have to re-derive it.

**D6 — A STALE SENTENCE OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED:
`.agent/f110_inventory.md` SECTION F NOW READS FALSE FOR `R-0768`.** It says
"Both findings sit on exactly this seam. Both stay REGISTERED and unrepaired on
this branch". After C3, C4 and C5 that is true of `R-0767` and false of
`R-0768`, which this round resolved by name — exactly as the SAME paragraph goes
on to instruct ("when T001b lands that edit, R-0768 is resolved by name"). So
the file predicted its own staleness and the round did what it asked; the
sentence still needs a reader's care. Section E item 2 ("Its default is the
literal `"fake"`, not `role_config.DEFAULT_PROVIDER`, and this module does not
import role_config") is likewise now a historical statement — but that file
stamps every present-tense sentence `MEASURED AT BASE = 6f2230ce…` in its first
paragraph, so it reads as the measurement it is. `.agent/f110_inventory.md` is
NOT in the change set; writing to it is the one thing constraint 7 and the
change set jointly forbid. If the reviewer wants section F updated, it needs a
path in a later block's change set.

**D7 — A SECOND STALE SENTENCE OUTSIDE THE CHANGE SET: `.agent/context.md`'s
RUFF CONSTRAINT IS NOW HALF-TRUE AND INVITES AN UNRUNNABLE GATE.** Its last
Constraints bullet reads "This session's reviewer CAN execute `ruff` … a round
of F110 that ships a `.py` file may gate on ruff." This round shipped a `.py`
file and the block ORDERED NO RUFF GATE (constraint 5), because round 1 measured
that the WORKER's permission layer refuses `ruff` while the reviewer's does not.
The bullet is not false — it speaks about the reviewer — but read alone it
invites a block to order a ruff gate at a worker that cannot run one. Declared,
not repaired: `.agent/context.md` is outside the change set. I said nothing about
lint anywhere in the code or the commits, as constraint 5 requires.

**D8 — `R-0767` WAS NOT TOUCHED, BY ORDER.** Constraint 6. It remains OPEN in
`.agent/live_review.md`, confirmed this round by set difference: 347 distinct
registered ids, 69 distinct resolved, `R-0767` in the difference. The open count
moved 279 → 278 and `R-0768` is the single id that moved.

**D9 — THE SCRATCH IS LEFT IN PLACE UNDER `.remedy-wt/f110r2/`.** The extractor,
the append and second-reader scripts, the extracted slices and the two
negative-control copies. All of it is gitignored, `git ls-files .remedy-wt`
returns nothing, and nothing was deleted by glob (the never-delete-by-glob
rule). It is left deliberately so the reviewer can re-run every gate from the
same inputs. The G6 worktree, by contrast, WAS removed and pruned, as ordered.

**Assumptions.** (i) The block's statement that the reviewer holds no scratch
original is taken at face value, so G1 is reported as self-consistency and not
as transport — the weaker claim, on purpose. (ii) "Non-empty `name` attribute"
is implemented as `isinstance(name, str) and name`, so `None`, `""` and a
non-string `name` all fall back to role_config; the block's third ordered case
("an injected object with no usable name") is read as covering all four, and all
four are tested. (iii) `.remedy-wt/` is gitignored session scratch that
PERSISTS, which is what makes D9's decision to leave it the right one.

## Next

REVIEW ROUND 2 AND ISSUE A VERDICT — lint `5bbb0cde` reviewer-side, since
constraint 5 routes that to the reviewer — then author round 3 as T001c:
consolidation order E.b, reading `orchestrator.model` THROUGH role_config so the
orchestrator stops being a third answer to "which model". The next session's
first action is Phase 1 rule 1 — read `.agent/STOP` from disk — before Phase 1
rule 2, the Open PR Gate, which is currently satisfied: no pull request is open,
because none was created. D6 and D7 need a path in a later block's change set if
the reviewer wants either acted on.
