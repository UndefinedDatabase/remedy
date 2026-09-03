# Handback — F110 Model routing by task class, round 3 — T001c, THE ORCHESTRATOR MODEL SEAM

## Session

SESSION 1 of feature F110 · round 3 · rounds so far 3

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 3 rounds and 1 session it is nowhere near, so no scope report is due.
`.agent/STOP` was read from disk twice — before the first commit (C0a) and again
before C5 — and does not exist at either point.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **BASE** | `490f575f` — the round 2 handback commit |
| **Runde** | 3 (Session 1) — T001c: consolidation order E.b, the orchestrator model seam |
| **Fortschritt** | ~35 % (T001a ✅ inventory · T001b ✅ provider seam · T001c ✅ orchestrator model seam · T002, T003 open) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. ALLE GRÜN. |
| **Offene Findings** | 278 (Mengendifferenz über 347 registrierte und 69 aufgelöste ids; UNVERÄNDERT gegen Runde 2 — diese Runde registriert und löst nichts) |

THIS ROUND CHANGED PRODUCTION CODE AND CHANGED NO BEHAVIOUR, deliberately.
`packages/orchestration/role_config.py` gains `resolve_orchestrator_model()`,
and the two call sites that read `orchestrator.model` straight out of the config
now ask that function instead. At today's configuration the key is unset and
role_config answers the same model id the Ollama planner would have picked, so
the seam moves without the running system moving — which is precisely why every
fall-through test patches `resolve_role_config` to a SENTINEL rather than
comparing the two live sources.

## Range

Review of `490f575f..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `a106dcb6` | done | block written verbatim to `.agent/authored/f110-r3.md`, 236 insertions |
| C0b `531d2267` | done | mirrored with `shutil.copyfile`; one sha256 for both copies (G1) |
| C1 `42531555` | done | PLAN3 extracted by delimiter index from the COMMITTED authored copy and applied whole; `cmp` exit 0, 46 lines. FIRST substantive commit, item 23 |
| C2 `95c69c6e` | done | RECORD2 appended to `.agent/live_review.md` and SLIPS3 to `.agent/prose_slips.md`, each with the two-byte separator; full arithmetic in G3, byte-equality in G4 |
| C3 `fabaebfe` | done | THE PRODUCTION COMMIT — the new function, its docstring entry and the two `model=` arguments; +33 / -4, nothing else (G5) |
| C4 `8eeb57fa` | done | THE TEST COMMIT — the new 19-test file, every fall-through case on a patched discriminator |
| C5 (this commit) | done | handback rewritten per `docs/agents/handback_template.md` |

Every ordered item appears exactly once. No item was skipped and none deviated
from its ordered position. Constraint 3's order — C3 production BEFORE C4 tests
— was honoured.

## Commits

### a106dcb6 F110 R3 C0a: save the round 3 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r3.md` | +236 / -0 | the reviewer's block saved verbatim; the first link of the transport chain |

### 531d2267 F110 R3 C0b: mirror the round 3 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +169 / -196 | round 2's block replaced by this one; byte-identical copy of the authored file |

### 42531555 F110 R3 C1: the plan turns to T001c, the orchestrator model seam
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +17 / -17 | PLAN3 applied whole; 46 lines, under the AGENTS.md 50-line rule |

### 95c69c6e F110 R3 C2: book the round 2 PASS verdict and its prose slip
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD2 appended — round 2's PASS verdict, booked in the first substantive-adjacent commit of the next round (amend0827 rule 1, item 23) |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS3 appended — one dated reviewer prose slip; no R-id spent (amend0827 rule 2) |

### fabaebfe F110 R3 C3: resolve the orchestrator model through role_config
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/role_config.py` | +29 / -0 | the new `resolve_orchestrator_model` at module tail plus its one line in the docstring's Public API list |
| `packages/orchestration/gauntlet_runner.py` | +2 / -2 | `_default_move_call_fn`: the `model=` argument, and the now-unused `get_config` import replaced by the `resolve_orchestrator_model` import |
| `apps/cli/commands/mission_cmd.py` | +2 / -2 | `_orchestrator_call_fn`: the same two lines, same reason |

### 8eeb57fa F110 R3 C4: pin the orchestrator model seam with a patched discriminator
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_orchestrator_model_routing.py` | +154 / -0 | 19 unit tests over the new function only; no concrete model id asserted anywhere |

### C5 (this commit) F110 R3 C5: the round 3 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern). Its own numbers go to neither a round report nor this file, per the block: the reviewer measures them at the next gate |

The `+` column above is the INSERTION count from `git show --numstat`
(AGENTS.md DECISION F104 D1). The cell-by-cell comparison is in G8.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f110r3_mut 8eeb57fa` | `Preparing worktree (detached HEAD 8eeb57fa)` — the G6 red proof ran ONLY here |
| `git worktree remove .remedy-wt/f110r3_mut` | removed; `git worktree list` afterwards shows no worktree of this round's making |
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
| G1 TRANSPORT | GREEN — one sha256 twice, `187c2d57…d536c`; `wc -l` reads **236**, against the reviewer's pre-emission projection of 233. WORKER SELF-CONSISTENCY ONLY: the reviewer stated it holds no scratch original, so this proves the mirror equals the saved copy and nothing about the emitted bytes (§3 item 37). The 3-line difference is REPORTED, not repaired; 236 is well under the §3 item 1 cap of 400 |
| G2 THE PLAN | GREEN — `cmp` exit 0, 46 lines (< 50), `^## Goal` 1, `^## Next Steps` 1 |
| G3 THE LEDGER APPEND | GREEN — 2149060 + 2 + 4845 = 2153907 real; the second reader accepts the last 1 unit IN ORDER; the negative control REJECTS; the grep reads 0 before C2 and 1 after |
| G4 THE PROSE FILE | GREEN — `.agent/prose_slips.md` final 1026 bytes byte-equal to the extracted SLIPS3, pre-C2 content an exact byte PREFIX, file still ends WITHOUT a newline |
| G5 THE PRODUCTION CHANGE | GREEN — +29/-0, +2/-2, +2/-2; `resolve_orchestrator_model` 0 → 2 in each of the three files; `orchestrator.model` 1 → 0 in gauntlet_runner.py and 2 → 1 in mission_cmd.py; all three `ast.parse` clean. The diff is the new function, its docstring entry and the two `model=` arguments — nothing else |
| G6 THE MUTATION RED PROOF | GREEN, AND THE DISCRIMINATOR HOLDS — control 19 passed exit 0; mutated 14 failed / 5 passed exit 1. Every reddened id is an unset-key fall-through case; BOTH configured-key cases stayed GREEN. Ran only in the disposable worktree, which is removed and pruned |
| G7 THE SUITES | GREEN — 298, 19, 14, 42, each its own invocation, run serially, every one exit 0. The first, third and fourth match the reviewer's base measurements exactly: no count moved |
| G8 THE TREE, THE COMMITS AND THE SWEEP | GREEN — tree EMPTY before C5 was staged, `git ls-files .remedy-wt` no output, no worktree of this round's making, all nine insertion cells agree with the Commits table |

### G1 TRANSPORT — GREEN

    $ sha256sum .agent/authored/f110-r3.md .agent/last_block.md
    187c2d573e7cf04079ef52b2310007abc69c4706519335cc545dbc0ec33d536c  .agent/authored/f110-r3.md
    187c2d573e7cf04079ef52b2310007abc69c4706519335cc545dbc0ec33d536c  .agent/last_block.md
    REAL_EXIT=0

    $ wc -l .agent/authored/f110-r3.md
    236 .agent/authored/f110-r3.md
    REAL_EXIT=0

One digest, twice, both lines verbatim. The reviewer stated up front that it
holds no scratch original this round, so this is WORKER SELF-CONSISTENCY ONLY:
it proves the mirror equals the saved copy and nothing about what the reviewer
emitted. That is the §3 item 37 shape and it is reported as such.

THE `wc -l` READING IS 236 AGAINST A PROJECTION OF 233 — a difference of three
lines, REPORTED and NOT repaired, exactly as the gate orders. This is the
measurement SLIPS3 itself asks for: the slip records that the round 1 and round 2
projections were each off by one in the same direction, and the counter-measure
it institutes from round 3 on is this very gate. Round 3's projection is off by
three, in the same direction. The committed file is 19326 bytes; the cap is 400
lines and 236 is well inside it, so nothing is blocked by the difference. See D1.

Every APPLIED slice below was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r3.md` — read with `git show HEAD:.agent/authored/f110-r3.md`,
never from the working copy — and written to its target BY SCRIPT. Nothing was
retyped. Each marker string was asserted to occur EXACTLY ONCE before any write
(the extractor raises otherwise).

    PLAN3    begin line 181  end line 228   46 lines   2220 bytes (with trailing newline)   2219 without
    RECORD2  begin line 230  end line 232    1 line    4846 bytes (with trailing newline)   4845 without
    SLIPS3   begin line 234  end line 236    1 line    1027 bytes (with trailing newline)   1026 without

Constraint 4 settles which form each target takes: `.agent/plan.md` ends WITH a
newline and took the 2220-byte form; `.agent/live_review.md` and
`.agent/prose_slips.md` end WITHOUT one and took the 4845 / 1026 forms. The
TARGET's convention wins, exactly as ordered.

### G2 THE PLAN — GREEN

    $ cmp .remedy-wt/f110r3/PLAN3.extracted .agent/plan.md
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

### G3 THE LEDGER APPEND — GREEN, FULL ARITHMETIC

THE COUNT TAKEN BEFORE THE COMMIT, so the 1 is provably this round's append and
not a pre-existing line. `grep -c` exits 1 when it counts 0; that is the real
exit code and it is reported rather than smoothed:

    BEFORE C2:  $ grep -c '^Gate: F110 R2 — ' .agent/live_review.md   -> 0   REAL_EXIT=1
    AFTER  C2:  $ grep -c '^Gate: F110 R2 — ' .agent/live_review.md   -> 1   REAL_EXIT=0

RECORD2 at C2, against the file size IMMEDIATELY BEFORE that commit:

    size BEFORE C2                      2149060
    separator bytes                           2   (newline newline)
    RECORD2 slice length                   4845   (extractor yields 4846; the target takes no trailing newline)
    before + 2 + slice                  2153907
    real new size                       2153907
    equal                                  True
    new file ends WITHOUT a newline        True
    pre-append content an exact PREFIX     True
    final 4845 bytes equal the slice       True

The 2149060 matches the block's own stated base size exactly, so the append
started where the reviewer measured it would.

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, never taken from the
block: N = 1.

    N counted BY THE SCRIPT from the slice   1
    blank-line units in the WHOLE file       899
    unit[-1] equals slice paragraph 1: True (len 4829 vs 4829 characters)
    last N file units == slice paragraphs IN ORDER:   True

The byte length (4845) and the character length (4829) differ because the
paragraph carries multi-byte characters; both readings are of the same string and
neither is a discrepancy.

NEGATIVE CONTROL, on a SCRATCH COPY under `.remedy-wt/` — the tracked file was
never mutated:

    first appended paragraph found at byte offset   2149062
    flipped byte at offset 2151484 (was 'S') with XOR 0x01
    second reader ACCEPTS the mutated copy:         False
    second reader REJECTS it:                       True

### G4 THE PROSE FILE — GREEN, BYTE-EQUALITY ONLY

Which is all amend0827 rule 5 allows a `.agent/` prose file. Re-checked AFTER C2
landed, with the pre-C2 bytes read from the git OBJECT at `95c69c6e^` rather
than from a remembered number:

    size BEFORE C2 (from the git object)                        50060
    separator bytes                                                 2
    SLIPS3 slice length                                          1026
    before + 2 + slice                                          51088
    real new size                                               51088
    equal                                                        True
    final 1026 bytes equal the extracted SLIPS3 slice:           True
    pre-C2 content preserved as an exact byte PREFIX:            True
    file still ends WITHOUT a newline:                           True

### G5 THE PRODUCTION CHANGE — GREEN

    $ git show --numstat fabaebfe -- packages/orchestration/role_config.py
    29	0	packages/orchestration/role_config.py
    REAL_EXIT=0
    $ git show --numstat fabaebfe -- packages/orchestration/gauntlet_runner.py
    2	2	packages/orchestration/gauntlet_runner.py
    REAL_EXIT=0
    $ git show --numstat fabaebfe -- apps/cli/commands/mission_cmd.py
    2	2	apps/cli/commands/mission_cmd.py
    REAL_EXIT=0

Counts read from the git OBJECTS, not from the working copy, so BEFORE means
`fabaebfe^` and AFTER means `fabaebfe`:

    packages/orchestration/role_config.py
        'resolve_orchestrator_model'  BEFORE   0   AFTER   2
        'orchestrator.model'          BEFORE   1   AFTER   4
        ast.parse on the real AFTER text: OK
    packages/orchestration/gauntlet_runner.py
        'resolve_orchestrator_model'  BEFORE   0   AFTER   2
        'orchestrator.model'          BEFORE   1   AFTER   0
        ast.parse on the real AFTER text: OK
    apps/cli/commands/mission_cmd.py
        'resolve_orchestrator_model'  BEFORE   0   AFTER   2
        'orchestrator.model'          BEFORE   2   AFTER   1
        ast.parse on the real AFTER text: OK

READ THE THREE `orchestrator.model` COLUMNS TOGETHER, because on their own they
mislead. In `role_config.py` the count rises 1 → 4: the pre-existing occurrence
is the `KNOWN_ROLES` comment, and the three added ones are all PROSE — the new
function's docstring names the key three times while explaining that a set value
wins and an unset one falls through. NO CODE in role_config.py spells the key as
a literal outside `get_config().get("orchestrator.model")`, which is the single
added read. In `gauntlet_runner.py` the count falls 1 → 0: that file's only
occurrence WAS the config read, and it is gone. In `mission_cmd.py` it falls
2 → 1: the config read is gone and the surviving occurrence is the
`_orchestrator_call_fn` DOCSTRING sentence, which the block's "nothing else"
clause forbids me to touch — see D3.

THE DIFF, ADDED AND REMOVED LINES VERBATIM, ALL THREE FILES:

    packages/orchestration/role_config.py

    +    resolve_orchestrator_model() -> str

    +
    +
    +# The orchestrator's model must have ONE answer: `orchestrator.model` when the
    +# operator set it, and otherwise the same resolution every other role gets —
    +# which is what config.py already promises the key means, stated here in code.
    +def resolve_orchestrator_model() -> str:
    +    """Return the model id the ``orchestrator`` role should run on.
    +
    +    ``orchestrator.model`` (packages/orchestration/config.py) is the ONLY
    +    orchestrator-specific routing surface, and its own documented promise is
    +    that "Unset means the role resolves exactly like every other one". So a set,
    +    non-empty value wins, and anything else — unset, empty, whitespace-only, or
    +    not a string at all — falls through to
    +    :func:`resolve_role_config` for the ``orchestrator`` role. Callers that need
    +    the orchestrator's model ask HERE rather than reading the config key
    +    themselves, so the key stays the operator-facing surface without also being
    +    a second, rival resolver.
    +
    +    ``get_config`` is imported inside the body on purpose: this module has no
    +    module-level import of config and is itself imported early by others.
    +    """
    +    from packages.orchestration.config import get_config
    +
    +    configured = get_config().get("orchestrator.model")
    +    if isinstance(configured, str) and configured.strip():
    +        return configured
    +
    +    return resolve_role_config("orchestrator").model

    (no removed lines in this file — 29 added, 0 removed)

    packages/orchestration/gauntlet_runner.py

    -    from packages.orchestration.config import get_config
     from packages.orchestration.intake import make_structured_call_fn
     from packages.orchestration.orchestrator_move_schema import OrchestratorMove
    +    from packages.orchestration.role_config import resolve_orchestrator_model

    -        OrchestratorMove, model=get_config().get("orchestrator.model") or None)
    +        OrchestratorMove, model=resolve_orchestrator_model())

    apps/cli/commands/mission_cmd.py

    -    from packages.orchestration.config import get_config
     from packages.orchestration.intake import make_structured_call_fn
     from packages.orchestration.orchestrator_move_schema import OrchestratorMove
    +    from packages.orchestration.role_config import resolve_orchestrator_model

    -        OrchestratorMove, model=get_config().get("orchestrator.model") or None)
    +        OrchestratorMove, model=resolve_orchestrator_model())

THE `get_config` IMPORT QUESTION THE BLOCK ASKS ME TO REPORT PER FILE: in BOTH
files it was the UNUSED case and was removed. `grep -n 'get_config'` over each
file after C3 returns nothing at all; before C3 each file's only two occurrences
were the function-local import and the config read on the very next lines
(gauntlet_runner.py 221 and 226, mission_cmd.py 381 and 386). The replacement
import is placed in the same function body, in the existing alphabetical order of
that body's imports.

THE SHIPPED FUNCTION WAS RUN, not merely read, against the real configuration:

    get_config().get('orchestrator.model')                  -> None
    resolve_orchestrator_model()                            -> 'muse-glimmer:latest'
    resolve_role_config('orchestrator').model               -> 'muse-glimmer:latest'

Which is constraint 6, confirmed on this machine rather than taken on trust: the
key is unset, the function falls through, and the answer equals what every other
role gets. Nothing the running system does changes today. The model id appears
here as a measurement; it is asserted NOWHERE in the tests.

### G6 THE MUTATION RED PROOF — GREEN, AND THE DISCRIMINATOR HOLDS

Ran ONLY inside a disposable worktree at the C4 commit, never in the primary
checkout. Every invocation purged `__pycache__` inside that worktree first and
ran with `python3 -B`; the imported module path was printed before each run, so
the mutation demonstrably reaches the test rather than being shadowed by an
installed copy or by the parent checkout:

    imported module file inside the worktree:
    /home/decodeux/Repos/remedy/.remedy-wt/f110r3_mut/packages/orchestration/role_config.py
    __pycache__ dirs purged inside the worktree: 0 (a freshly added worktree has none, and -B writes none)

THE UNMUTATED CONTROL FIRST, as ordered:

    --- CONTROL, UNMUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    ...................                                                      [100%]
    19 passed in 0.21s
    REAL_EXIT=0

THE MUTATION — only the fall-through branch, so the function ignores role_config
and answers from the planner's own default path instead:

    -    return resolve_role_config("orchestrator").model
    +    from packages.providers.ollama_planner.provider import _DEFAULT_MODEL
    +
    +    return _DEFAULT_MODEL

That is the mutant the block names, and it is the exact mutant an UNPATCHED test
could not catch: `_DEFAULT_MODEL` is `resolve_model_alias("ollama-default")` and
role_config's orchestrator default resolves to the same string today, so a test
comparing the two live sources would stay green under it.

    --- MUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    ..FFFFFFFFFFFFFF...
    14 failed, 5 passed in 0.25s
    REAL_EXIT=1

    typical failure: AssertionError: assert 'muse-glimmer:latest' == 'sentinel-role-config-model:test'

THE 14 IDS THAT WENT RED — every one an UNSET-KEY fall-through case:

    TestUnsetKeyFallsThroughToRoleConfig::test_unset_key_returns_the_role_config_model
    TestUnsetKeyFallsThroughToRoleConfig::test_unset_key_does_not_answer_from_a_rival_source
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[None]
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[0]
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[False]
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[configured3]
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[configured4]
    TestUnsetKeyFallsThroughToRoleConfig::test_a_non_string_key_is_treated_as_unset[17]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[empty]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[one-space]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[spaces]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[tab]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[newline]
    TestEmptyConfiguredValueIsUnset::test_blank_value_falls_through_to_role_config[mixed-whitespace]

THE 5 IDS THAT STAYED GREEN — the two CONFIGURED-KEY cases the discriminator
requires to stay green, plus three shape checks:

    TestConfiguredKeyWins::test_configured_value_is_returned                        GREEN
    TestConfiguredKeyWins::test_configured_value_wins_over_the_role_config_answer   GREEN
    TestTheAnswerIsAlwaysUsable::test_the_unpatched_answer_is_a_non_empty_string    GREEN
    TestTheAnswerIsAlwaysUsable::test_the_configured_answer_is_a_non_empty_string   GREEN
    TestTheAnswerIsAlwaysUsable::test_the_fall_through_answer_is_a_non_empty_string GREEN

THE DISCRIMINATOR IS SATISFIED: the unset-key case reddens (14 ids) while the
configured-key case stays GREEN (2 ids). It is NOT "both red" and NOT "neither",
so this is a proof and not a colour. NOT ALL FIVE GREENS ARE CONFIGURED-KEY
CASES and that is stated rather than glossed — the three `TestTheAnswerIsAlwaysUsable`
tests assert only that the return is a non-empty `str`, which `_DEFAULT_MODEL`
also is, so they are shape checks and cannot discriminate BY CONSTRUCTION. Their
class name and docstring say so in the file itself. See D2.

THE REVERT WAS PROVED, not assumed:

    --- REVERTED to the committed bytes ---
    ...................                                                      [100%]
    19 passed in 0.21s
    REAL_EXIT=0
    $ git -C .remedy-wt/f110r3_mut status --porcelain
    '' (empty — the worktree carried the committed bytes again)
    REAL_EXIT=0

    $ git worktree remove .remedy-wt/f110r3_mut
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  8eeb57fa [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

No worktree of THIS round's making remains; the five `job-*` entries predate it.

### G7 THE SUITES — GREEN, EACH AS ITS OWN INVOCATION, RUN SERIALLY

Never two pytest processes alive at once.

    $ python3 -m pytest tests/orchestration/test_orchestrator_loop.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_role_config.py -q
    298 passed in 1.35s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    19 passed in 0.22s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_job_role_routing.py -q
    14 passed in 0.22s
    REAL_EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.68s
    REAL_EXIT=0

298, 19, 14, 42. THE FIRST, THIRD AND FOURTH MATCH THE REVIEWER'S BASE
MEASUREMENTS EXACTLY — 298, 14, 42 — so no count moved and there is nothing to
report as a finding on that clause. The new file reports 19; the block asked for
the count rather than fixing one. The last invocation is the canary every
handback owes.

### G8 THE TREE, THE COMMITS AND THE SWEEP — GREEN

Read immediately before C5 was staged:

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

    commit     path                                                     numstat +   table +   agree
    a106dcb6   .agent/authored/f110-r3.md                                     236       236    yes
    531d2267   .agent/last_block.md                                           169       169    yes
    42531555   .agent/plan.md                                                  17        17    yes
    95c69c6e   .agent/live_review.md                                            3         3    yes
    95c69c6e   .agent/prose_slips.md                                            3         3    yes
    fabaebfe   packages/orchestration/role_config.py                           29        29    yes
    fabaebfe   packages/orchestration/gauntlet_runner.py                        2         2    yes
    fabaebfe   apps/cli/commands/mission_cmd.py                                 2         2    yes
    8eeb57fa   tests/orchestration/test_orchestrator_model_routing.py         154       154    yes

Per-commit insertion totals: C0a 236, C0b 169, C1 17, C2 6, C3 33, C4 154. Every
one is far under the 500-insertion cap. C5's own numbers go to NEITHER a round
report NOR this file, per the block: the reviewer measures them at the next gate.

**THE STALENESS SWEEP over every file this round touched, one entry per file.**

1. `.agent/authored/f110-r3.md` — NOT stale by construction. A verbatim copy of
   the reviewer's block; nothing in it is edited regardless of what any later
   measurement shows, including the 233-vs-236 line count in its own G1 clause.
2. `.agent/last_block.md` — NOT stale, same reason, same bytes, same digest.
3. `.agent/plan.md` — NOT stale. Its `## Current Step` describes exactly what
   this round did, and its first Risk bullet ("E.b is behaviour-neutral at
   today's configuration: the two sources already answer the same model id")
   was CONFIRMED by running the shipped function in G5, not left as a
   prediction. `## Next Steps` names T002 and folds E.d into it, which is where
   the inventory's section E puts the per-call-site class declarations.
4. `.agent/live_review.md` — NOT stale. One `Gate:` paragraph appended for round
   2's PASS; no registration or resolution line was written or edited, and the
   open set is unchanged at 278 over 347 registered and 69 resolved, measured by
   set difference this round.
5. `.agent/prose_slips.md` — NOT stale. One dated record of a reviewer prose
   slip; it is a statement about past rounds and is true of them. Append-only,
   never renumbered, and nothing here gates anything. Its own counter-measure —
   "from round 3 on every block's gate G1 additionally reports `wc -l`" — was
   honoured by this round's G1 and immediately earned its keep (D1).
6. `packages/orchestration/role_config.py` — NOT stale. The module docstring's
   Public API list now names all four public entries; the `KNOWN_ROLES` comment
   about the orchestrator ("its built-in defaults are deliberately the SAME as
   every other role's, because raising the orchestrator to a top-tier model is a
   CONFIGURATION act (`orchestrator.model`)") is MORE true after this change
   than before, because the configuration act now runs through this module.
7. `packages/orchestration/gauntlet_runner.py` — NOT stale.
   `_default_move_call_fn`'s docstring says "the SAME factory `remedy mission
   run` uses", and that is still exactly true — both sites changed identically in
   the same commit, so the sentence describes the new shape as accurately as the
   old.
8. `apps/cli/commands/mission_cmd.py` — ONE STALE-ADJACENT SENTENCE, DECLARED AND
   NOT REPAIRED. `_orchestrator_call_fn`'s docstring says the call_fn is "bound
   to the move schema and to the model named by `orchestrator.model`". That is
   now only half the story: the key still names the model when it is set, but an
   unset key no longer means "no model given", it means role_config's answer. The
   block's G5 clause says the change must be the function, its docstring entry
   and the two model arguments, "nothing else", so I left it. See D3.
9. `tests/orchestration/test_orchestrator_model_routing.py` — NOT stale, and it
   is written not to go stale: no concrete model id appears anywhere in it. Every
   expectation is a sentinel this file itself defines, and the one place a real
   default is read (`_DEFAULT_MODEL`) is read only to assert the answer is NOT
   it. An operator repointing the alias table cannot falsify a single assertion.
10. `.agent/handoff.md` — this file; written once, per the write-once rule.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. Sentences outside it that this round
makes stale are DECLARED, NOT REPAIRED, per constraint 7 — see D4 and D5.

## Authored-text proofs

Every applied reviewer-authored text was extracted by delimiter index from the
COMMITTED `.agent/authored/f110-r3.md` (read with
`git show HEAD:.agent/authored/f110-r3.md`, not from the working copy) and
written to its target BY SCRIPT. Nothing was retyped.

| Authored text | Proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `sha256sum` of `.agent/authored/f110-r3.md` and `.agent/last_block.md` | one digest twice | `187c2d57…d536c` twice | 0 |
| the whole block | `wc -l .agent/authored/f110-r3.md` | projection 233 | 236 — reported, not repaired | 0 |
| PLAN3 (46 lines, 2220 bytes) | `cmp .remedy-wt/f110r3/PLAN3.extracted .agent/plan.md` | identical | identical | 0 |
| RECORD2 (4845 bytes applied) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |
| SLIPS3 (1026 bytes applied) | final-bytes byte-equality + exact byte prefix + newline convention | True / True / True | True / True / True | — |

The production code and the tests are NOT authored text: the block described
them and the worker wrote them (SPEC CODE, SPEC TESTS), so they carry no
transport proof and are gated by G5, G6 and G7 instead.

## Deviations & assumptions

**D0 — NONE OF THE BLOCK'S ORDERED COMMIT SEQUENCE WAS DEPARTED FROM.** C0a,
C0b, C1, C2, C3, C4, C5 ran in exactly that order, with exactly the ten paths the
change set names and nothing else. No commit was added, dropped or reordered.
Constraint 3's fixed order — production BEFORE tests — was honoured. This entry
exists because the handback template asks for the departure to be named HERE even
when there is none.

**D1 — THE BLOCK'S OWN LINE PROJECTION IS OFF BY THREE, AND THE GATE IT
INSTITUTED IS WHAT CAUGHT IT.** G1 states the reviewer's pre-emission projection
as 233 lines; the committed file is 236, at 19326 bytes. The difference is
REPORTED, not repaired, exactly as the gate orders, and it changes nothing: the
§3 item 1 cap is 400 and no gate in this round consumes the projected figure. It
is worth one sentence because SLIPS3, appended in this same round, records the
same off-by-one in rounds 1 and 2 and institutes this very `wc -l` clause as the
counter-measure "from round 3 on" — so the counter-measure took a reading on its
first outing. The direction is the same in all three rounds (projection LOW), and
the magnitude grew from 1 to 1 to 3.

**D2 — THREE TESTS STAYED GREEN UNDER THE MUTANT THAT ARE NOT CONFIGURED-KEY
TESTS, AND I AM NAMING THEM RATHER THAN REPORTING A CLEAN COLOUR.** The whole of
`TestTheAnswerIsAlwaysUsable` asserts only that the return is a non-empty `str`;
the mutant returns `_DEFAULT_MODEL`, which satisfies that. They are shape checks
and cannot discriminate, by construction, and the class docstring in the shipped
file says exactly that so a later reader is not misled either. The G6
discriminator is still satisfied on its own terms — every unset-key case went red
(14 ids) and both configured-key cases stayed green (2 ids) — but "5 passed" is
not "5 configured-key cases passed", and the difference is stated here so the
reviewer does not have to re-derive it. This repeats round 2's D5 pattern
deliberately.

**D3 — A STALE-ADJACENT SENTENCE INSIDE THE CHANGE SET THAT I DID NOT REPAIR,
BECAUSE G5 FORBADE IT.** `apps/cli/commands/mission_cmd.py`'s
`_orchestrator_call_fn` docstring says the call_fn is "bound to the move schema
and to the model named by `orchestrator.model`". After C3 the binding goes
through `resolve_orchestrator_model()`, so an UNSET key now yields role_config's
model rather than `None`. The file IS in the change set, so I could have written
the line — but G5 says the change "must be the new function, its docstring entry,
and the two model arguments — nothing else", and a fourth changed line would have
made that gate read false. I obeyed the gate and am declaring the sentence
instead. It is the surviving `orchestrator.model` occurrence G5 counts in that
file (2 → 1). If the reviewer wants it rewritten, a later block need only widen
its own G5 clause; the path is already in the change set.

**D4 — A STALE SENTENCE OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED:
`packages/orchestration/intake.py`'s `make_structured_call_fn` DOCSTRING.** It
reads "``model`` overrides the planner's configured model for this call_fn only
… Omitted, the planner resolves the model exactly as it always has." After C3
neither orchestrator call site ever omits `model`: both now always pass a
resolved string, where before they passed `None` whenever `orchestrator.model`
was unset. The sentence about the PARAMETER is still true — it describes the
function's own contract, which did not move — but the implied "and callers
sometimes omit it" is now false of these two callers. Not repaired:
`packages/orchestration/intake.py` is not in the change set.

**D5 — A SECOND STALE SENTENCE OUTSIDE THE CHANGE SET:
`.agent/f110_inventory.md` SECTION E ITEM 3.** It reads "The `orchestrator.model`
config key, read directly at B3 and B7" and lists that as one of the four rival
mechanisms at BASE. After C3 the key is no longer read directly at either site;
mechanism 3 is now a caller of mechanism 1, which is exactly what consolidation
order E.b asked for. The inventory stamps its present-tense sentences as measured
at a named base, so it reads as the measurement it is, and section E's own order
list predicted this change by name. Section F's "Both stay REGISTERED and
unrepaired on this branch" remains false for `R-0768` from round 2 and is already
carried as a dated correction inside the RECORD2 paragraph this round appended;
it is not repeated as a new deviation. `.agent/f110_inventory.md` is NOT in the
change set. `.agent/context.md`'s ruff bullet (round 2's D7) is likewise
untouched and still invites a gate the worker cannot run — round 3's block again
ordered no ruff gate, and I said nothing about lint anywhere in the code or the
commits, as constraint 5 requires.

**D6 — THE SPEC'S SIGNATURE WAS SHIPPED EXACTLY, BUT I MADE TWO SEMANTIC CHOICES
THE SPEC LEFT OPEN.** (i) "Set and non-empty" is implemented as
`isinstance(configured, str) and configured.strip()`, so a NON-STRING value —
`0`, `False`, `[]`, `17` — is treated as unset rather than returned or coerced.
`get_config().get()` is typed `-> Any` and a malformed config file can put any
JSON scalar there, so the alternative was returning a non-`str` from a function
annotated `-> str`. All six non-string cases are tested. (ii) A whitespace-only
value is treated as unset per the spec, but a value with SURROUNDING whitespace
that is otherwise non-blank is returned VERBATIM, not stripped, because the spec
says to "return the `orchestrator.model` project-config value" and silently
rewriting an operator's configured id is a bigger decision than this round is
allowed to take. Declared because both readings are defensible.

**D7 — THE OPEN FINDING SET DID NOT MOVE, BY DESIGN.** 278 open over 347 distinct
registered ids and 69 distinct resolved, measured by set difference this round,
identical to round 2's close. This round registers no finding and resolves none:
`R-0767` is still OPEN on the neighbouring seam and was not touched, absorbed or
mentioned in any commit, and RECORD2 is a `Gate:` paragraph, which spends no id.

**D8 — THE SCRATCH IS LEFT IN PLACE UNDER `.remedy-wt/f110r3/`.** The extractor,
the append and second-reader scripts, the G4/G5/G6/G8 scripts, the extracted
slices and the negative-control copy. All of it is gitignored, `git ls-files
.remedy-wt` returns nothing, and nothing was deleted by glob (the
never-delete-by-glob rule). It is left deliberately so the reviewer can re-run
every gate from the same inputs. The G6 worktree, by contrast, WAS removed and
pruned, as ordered.

**Assumptions.** (i) The block's statement that the reviewer holds no scratch
original is taken at face value, so G1 is reported as self-consistency and not as
transport — the weaker claim, on purpose. (ii) "The planner's default path", the
mutation G6 names, is read as
`packages.providers.ollama_planner.provider._DEFAULT_MODEL` — the module constant
`OllamaPlanner` itself falls back to, resolved from
`resolve_model_alias("ollama-default")`. That is the rival source the seam was
built to displace, and it is what makes the mutant invisible to an unpatched
comparison. (iii) `.remedy-wt/` is gitignored session scratch that PERSISTS,
which is what makes D8's decision to leave it the right one.

## Next

REVIEW ROUND 3 AND ISSUE A VERDICT — lint `fabaebfe` and `8eeb57fa`
reviewer-side, since constraint 5 routes that to the reviewer — then author round
4 as T002: the resolver proper, the class table seeded from
`docs/agents/model_routing_policy.md`, the config schema and the hard-rule checks
with one violating fixture per rule refused with the rule named. The next
session's first action is Phase 1 rule 1 — read `.agent/STOP` from disk — before
Phase 1 rule 2, the Open PR Gate, which is currently satisfied: no pull request
is open, because none was created. D3, D4 and D5 need a path in a later block's
change set, and a widened G5 clause, if the reviewer wants any of them acted on.
