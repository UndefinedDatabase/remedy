# Live Review — Steps 1917-1960: Token-Aware Repair Loop v1/v2

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): repair loop metadata/state machine; repair work items from failure artifacts; repair
work items from review findings; token-aware repair context packs; route recommendations; candidate
intake state tracking; review gate tracking; re-test gate tracking; mission contract integration; CLI
visibility; command catalog / run_contract entries; progress ledger / feature planner / review bundle /
cockpit summaries; integrity checks; docs/tests. Existing bounded test execution may be CONSUMED but
must stay bounded/synchronous (no unbounded/background exec).
Must NOT: provider/Claude/Pi/OpenCode/Ollama execution; direct worker execution; ARBITRARY command
execution; auto-apply; auto-approval; autonomous repair mutation; auto-PR/git automation; real rollback
restore; internal MemPalace memory; embeddings/vector DB; UI redesign; MCP activation.
BRIDGE BLOCK — test failure → controlled repair. Hard invariants: failure artifact is EVIDENCE not raw
log dump; repair context minimal + token-aware; candidates UNTRUSTED until reviewed; candidate quality
pass ≠ applied; applied ≠ repaired until re-test passes; `Done:` ≠ reviewer `Resolved`; open review
findings block repair completion; failed/timeout latest relevant test blocks repair completion; max
attempts/retests prevent infinite loops; required blockers vs optional ideas separated; token reduction
must NOT drop safety-critical evidence; NO provider/model/worker exec; NO auto-apply/approval/mutation;
no fake repaired state; no fake autonomy.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
PENDING — block opened; awaiting committed code for independent line-level review + targeted suite.
Builder must NOT claim merge-ready while PENDING or FAIL.

## Check matrix (live)
1. Mainline closure — PASS (closure discipline). Real Test Execution v1 (1877-1916) reviewer PASS @
   7230268 merged via PR #73 → main `43197d9`. Fresh branch `feature/steps-1917-1960-token-aware-repair-
   loop-v1-v2` off merged main `43197d9`; ZERO feature commits before closure (`git log 43197d9..HEAD`
   empty); working tree clean. NOTE: `.agent/plan.md` Current Step still reads 1899-1916 (stale) —
   expect builder to reconcile plan/context to the new block as first step; re-verify on first commit.
2. Repair models (RepairPolicy/WorkItem/Attempt/LoopEvaluation safe+bounded; explicit statuses; no
   raw/private leak; unknown explicit) — PENDING.
3. Failure artifact integration (idempotent repair item; output_ref not raw; missing→safe error;
   suspected files = safe refs) — PENDING.
4. Review finding integration (open Blocker/High/Medium create/keep required items; Done≠Resolved still
   blocks; Resolved doesn't create required; reviewer verdict beats self-report) — PENDING.
5. Token-aware context pack (no full raw logs/repo dump/raw candidate output; bounded only; oversized→
   compress or human decision; unknown not cheap/local-ready; safety-critical evidence retained as
   refs/summaries) — PENDING.
6. Route recommendation (Worker Registry/Route Policy/Token Economy/Tournament respected; expensive/
   unknown→approval; disabled/blocked not recommended; external→package-create not exec; no fake
   provider readiness) — PENDING.
7. Candidate/review/apply/retest gates (received≠repaired; quality≠applied; apply proof when policy;
   reviewer PASS/Resolved when policy; passed latest re-test required for repaired; failed/timeout
   blocks; no re-test after apply→waiting) — PENDING.
8. State machine / loop safety (no infinite loop; max attempts/retests enforced; every state has
   next_safe_action/blocked reason; blocked honest; user decision at limits; no fake repaired) — PENDING.
9. Mission contract integration (required repair items block satisfaction; repaired satisfies repair
   gate only after required gates; blocked/abandoned→user decision; mission summary explains repair
   state) — PENDING.
10. CLI/catalog/run_contract (commands work; invalid ids safe; JSON safe; no traceback; catalog entries
    exist; read_only/write_metadata only; NO may_execute_commands) — PENDING.
11. Progress/Feature/Review/Cockpit (repair_loop_summary safe; cockpit read-only; ledger understandable;
    Feature Planner separates required vs optional + Impact/Effort; no raw/private) — PENDING.
12. Integrity (catches: repaired+failed-latest-retest; repaired+open-review-finding; repaired-without-
    required-apply-proof; Done-counted-as-Resolved; max-attempts/retests-exceeded-without-blocked/user;
    raw-output/candidate/diff-in-public; non-catalog-next_safe_action; optional-idea-marked-required-
    without-evidence) — PENDING.
13. Architecture guards (no provider SDK / network / browser / shell=True / arbitrary exec / git-write /
    apply-approve-PR automation / Ollama-cloud-local-model exec / embeddings-vector-DB / MemPalace) —
    PENDING.

## Findings — Steps 1917-1960
(none yet)

Next id: R-0105.

## Reviewer audit log
- Block opened. Check 1 (mainline closure) PASS @ branch base `43197d9` (PR #73 merged Real Test
  Execution v1 → main). Prior block 1877-1916 PASS @ 7230268 (R-0104 Resolved) merged; fresh branch at
  main tip; no work before closure. Plan.md not yet reconciled (stale 1899-1916) — re-verify on commit.
- WATCH (BRIDGE failure→repair): failure artifact = evidence not raw dump; context minimal+token-aware
  (no full logs/repo/candidate dumps; oversized→compress/human; unknown≠cheap; safety-critical evidence
  kept); candidates UNTRUSTED (received≠repaired, quality≠applied, applied≠repaired until passed
  re-test; failed/timeout re-test blocks); open Blocker/High/Medium findings block completion;
  Done≠Resolved; reviewer verdict beats self-report; max attempts/retests (no infinite loop, user
  decision at limit, no fake repaired); required blockers vs optional ideas separated; route reco
  respects registry/policy/economy/tournament (expensive/unknown→approval, disabled not recommended,
  external→package-create not exec); mission gate (required repair blocks satisfaction); integrity 8
  detections; CLI read_only/write_metadata no may_execute; NO provider/worker/model exec, NO auto-apply/
  approve/mutate/PR/git, NO real rollback restore, NO MemPalace/embeddings/MCP/UI-redesign; all
  project-facing text English.
- Merge-autonomy: PR #73 (prior block) auto-merged on reviewer PASS per merge-autonomy. No PR for THIS
  block; NO PR unless user asks.
