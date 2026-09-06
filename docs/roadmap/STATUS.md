# REMEDY STATUS — Execution-Order Truth

> Grammar: see ROADMAP.md Part C. States: `[ ]` todo · `[~]` in progress · `[x]` done (PR/evidence ref REQUIRED) · `[!]` blocked (reason).
> Rule A5: the next feature is the first unchecked line, top to bottom. Update this file in the same PR as the work (A4).
> Packages (operator decision 2026-08-10): Package 1 "Self-Use" below is the active execution order. Package 2 "Parked: Product & Governance" holds registered features deliberately scheduled last, so Rule A5 never selects them while Package 1 has open lines. Every registered feature appears exactly once in this file; parking or unparking a feature means moving its line between the packages by operator decision, in a reviewed docs round. New registrations land in Package 1 (Self-Use) by default, at the operator-chosen position or, absent one, at the end of the matching tier block; registering directly into Package 2 requires an explicit parking note in the registration commit. Grammar is identical in both packages; F080 parses this file unchanged.

## Package 1 — Self-Use (active execution order)

The tier-block order below is the operator-decided Self-Use sequence of 2026-08-10; it intentionally no longer mirrors the numeric tier order of ROADMAP.md Part F. Rule A5 reads this file top to bottom, so this order IS the strategy.

<!-- operator ruling amend0830-cost-first (2026-08-30): the six lines below are pulled forward from their Tier 3 block (originally directly after F113 — see the "## Tier 3 — Full Token Economy & Autonomy Extension" heading further down, where F113 now sits alone) so that, once no feature is in progress, Rule A5 proposes F106 first and consumes F106/F108/F109/F110/F112/F114 in this order before any other unchecked feature. Reversible by moving these six lines back to immediately before F113's line and deleting this heading and comment. -->
## Tier 3 — Cost-First Pull-Forward (operator ruling amend0830)

- [x] F106 — Session resume instead of rebuild (T001–T003 complete; accepted 2026-09-02 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f106-closure · package remedy-review-20260902-115928-READY_FOR_REVIEW.zip · SHA-256 939f841e486a4361ec503f21bc697fc18dd9834b3312f34024339f7a865b2a65 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 82278107ecea9e291d668caa9180f3d847d13e88)
- [x] F108 — Tiered artifact summaries (T001–T003 complete; accepted 2026-09-02 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f108-closure · package remedy-review-20260902-192835-READY_FOR_REVIEW.zip · SHA-256 a28313788d23607789ed8eaa25449a5329358392240c05a61509d70aae5dd73f · package path NOT ARCHIVED · accepted HEAD 28040b4bdb366e09d3f30feccf030dbdf7f8eabe)
- [x] F109 — Semantic dedupe (T001–T003 complete; accepted 2026-09-03 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f109-closure · package remedy-review-20260903-073602-READY_FOR_REVIEW.zip · SHA-256 92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 00084eef9de84b01e207a621d05d9b55378a2abc)
- [x] F110 — Model routing by task class (T001–T003 complete; accepted 2026-09-03 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f110-closure · package remedy-review-20260903-181544-READY_FOR_REVIEW.zip · SHA-256 767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 953cade0f62b2687d7dafb5cf1e0b9631849b532)
- [x] F112 — Prompt budget per task class (T001–T003 complete; accepted 2026-09-04 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 79b21c8cba8b4352 · package remedy-review-20260904-123332-READY_FOR_REVIEW.zip · SHA-256 b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 346c178f3241fad3984dca9baea3f37e34c3892a)
- [x] F114 — Cost preview per command (T001–T003 complete; accepted 2026-09-04 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f114-closure · package remedy-review-20260904-185732-READY_FOR_REVIEW.zip · SHA-256 8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6)

<!-- operator order amend0905-vocab-rebuild (2026-09-05, DECISION amend0905-vocab D12): the twelve lines below are the amend0831 registrations (F259–F266, inserted 2026-08-31 directly after the amend0830 cost-first block) plus the four amend0905 registrations (F268–F271), in the operator-decided execution order F259, F260, F261, F266, F268, F269, F270, F271, F263, F264, F265 — the vocabulary rebuild is the very next work, and `remedy do` (F268) needs `remedy study` (F266) before it. They carry five tier headings because that order falls into five contiguous tier runs (Tier 2, Tier 4, Tier 2, Tier 2, Tier 5) and tests/docs/test_docs_consistency.py::TestFeatureLedger::test_the_filename_tier_matches_the_status_tier pins each line's STATUS-derived tier — the enclosing '## Tier <n>' heading — against its T<tier>_F<id>.md filename; repeated '## Tier 2' headings are accepted by that test. Reversible by moving these lines back into the amend0831 order (or into their tier blocks further down) and deleting these headings and this comment. -->
## Tier 2 — Vocabulary & Concept Block (operator order amend0831, reordered amend0905)

- [x] F262 — List commands v2 (dates, sort, filter) (T001–T003 complete; accepted 2026-09-05 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f262-closure · package remedy-review-20260905-112903-READY_FOR_REVIEW.zip · SHA-256 83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0)
- [x] F259 — Vocabulary & concept model v1 (T001–T004 complete; accepted 2026-09-06 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job ace7fa4d9d782a7a · package remedy-review-20260906-004320-READY_FOR_REVIEW.zip · SHA-256 164f9513a4608030989590daf647d9a96a1c2c0b78f4fb469461966024fd56e3 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD efd2a4fb04bb82b8ee87b812327a7c3f9776853a)
- [x] F260 — One world: mission → job → run (T001 complete and the run half of T002; accepted 2026-09-06 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 017d918464634206 · package remedy-review-20260906-133417-READY_FOR_REVIEW.zip · SHA-256 0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 1eb980675b2c553f4aa8b949265eb3b6f30d6964)
- [ ] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
- [ ] F261 — CLI vocabulary v2 (rename & prune)

## Tier 4 — Repo Comprehension (operator order amend0831)

- [ ] F266 — remedy study (repo comprehension pass)

## Tier 2 — Easy Start & Contract Block (operator order amend0905)

- [ ] F268 — remedy do: the one-command start
- [ ] F269 — Contract & contract templates
- [ ] F270 — History apply: one commit per task, merge on demand
- [ ] F271 — No more legacy: ownership, reachability, replace-is-delete

## Tier 2 — Human-change absorption (operator order amend0831)

- [ ] F263 — Human-change absorption (absorb)

## Tier 5 — Steering & Learning Surfaces (operator order amend0831)

- [ ] F264 — Steering channel (remedy chat)
- [ ] F265 — Teacher learning UI v1 (post-task lessons)

## Tier 0 — Foundation & Trust Core

- [x] F001 — Adaptive provider timeouts + retry (PR #123 · commit 4856006 · external transition PASS)
- [x] F002 — Operator repair as a valid evidence path (PR #123 · evidence: remedy-review-20260706-143206-READY_FOR_REVIEW.zip · external PASS_WITH_RISKS)
- [x] F003 — Real token/cost measurement (PR #123 · implementation evidence: remedy-review-20260708-211448-READY_FOR_REVIEW.zip · runtime actuals: job 231d28005af344a1 / run 2ece61689cc046c3 · external PASS_WITH_RISKS)
- [x] F004 — Raw stream evidence (PR #124 · implementation evidence: remedy-review-20260709-225052-READY_FOR_REVIEW.zip · manual job 621369b56e834cd4 · runtime smoke job f22d69ed4c1f491b / run 54d4adc45d964812 · external PASS_WITH_RISKS)
- [x] F005 — Enforced structured outputs (PR #125 · evidence: remedy-review-20260711-132104-READY_FOR_REVIEW.zip · manual job e943e67937ef4124 · external PASS_WITH_RISKS)
- [x] F006 — Worktree isolation per run (PR #126 · evidence: remedy-review-20260712-000713-READY_FOR_REVIEW.zip · manual job 7fa740042a7e4561 · external PASS_WITH_RISKS)
- [x] F007 — Runtime harness (PR #127 · merge 7733a1d · follow-up d0a08a1 · persistent supervisor · accepted 2026-07-13 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 2e820a4dbf9842cf · package remedy-review-20260713-115439-READY_FOR_REVIEW.zip)
- [x] F010 — Automatic failure post-mortems (classifier + call/task/job post-mortems + `remedy stats failures` · accepted 2026-07-14 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 01363c70e13046e2 · package remedy-review-20260714-135557-READY_FOR_REVIEW.zip)
- [x] F011 — Kill switch (`remedy job stop` + safe points + STOPPED state + `job_stopped` event + stopped post-mortem · accepted 2026-07-14 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 49955e41c49f41bc · package remedy-review-20260714-223538-READY_FOR_REVIEW.zip)
- [x] F012 — Deterministic runs (RunManifestV1 + `on_call_finalized` seam + `remedy job rerun --check-manifest` · accepted 2026-07-20 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job r40_authority_contract_closure · package remedy-review-20260720-211130-READY_FOR_REVIEW.zip)
- [x] F017 — Scope fences (T001–T003 built + repaired + cleanup; accepted 2026-07-21 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job da34f448-ad80-49ae-b8eb-8c4e7ec46645 · package remedy-review-20260721-132745-READY_FOR_REVIEW.zip · SHA-256 a6fab50307b1db62fc7491943ba68975757f4177d2f1f1047c9528c9e30b81c4 · accepted HEAD c8c72f5370249ad3239ebd9eecbd65dd252a9d5c)
- [x] F018 — Budgets & stop conditions (T001–T004 complete; accepted 2026-07-22 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job f018_final_closure_684c4eaf027e · package remedy-review-20260722-175112-READY_FOR_REVIEW.zip · SHA-256 41a77d46e5f48c1120937061d33e2c505cee00633f0f31147c14a054fc4aeaad · accepted HEAD 30dd4a8107bf6346e046d2faa098ee8a23f4191a)
- [x] F146 — Project identity & repo autodetection (T001–T003 complete; accepted 2026-07-23 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job f146_project_identity_r4_c5d6e32f7a84 · package remedy-review-20260723-141827-READY_FOR_REVIEW.zip · SHA-256 7d5da77ca555e55f5a969e03340e3cdcd9292f413eedd0490eb53d2d739df16a · accepted HEAD c4d4e476e6057c9ebaf30dad5ce48eb158fbc6f7)
- [x] F081 — remedy init (T001–T003 complete; accepted 2026-07-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f081-closure · package remedy-review-20260723-231507-READY_FOR_REVIEW.zip · SHA-256 79dc8682bba602d475b1aca212c52854f3cfb51a38471f5420a92b2fae758a87 · accepted HEAD 68a2df68ed9873d71f1780d8402205d4cbb6f534)
- [x] F147 — Golden-path CLI (T001–T003 complete; accepted 2026-07-24 · live review PASS — ACCEPTED · Evidence job f147-closure · package remedy-review-20260724-121604-READY_FOR_REVIEW.zip · SHA-256 953410ab4c6aa0d4b639f96d797b7e66e93e36378338a6f9885e736d0e26ea17 · accepted HEAD 6869d82ffb68385d563f1c17d6f86c6590698ea9)
- [x] F148 — Project scoping everywhere (T001–T004 complete; accepted 2026-07-24 · live review PASS — ACCEPTED · Evidence job cf7ca6e8-8d5a-4b0a-ab4b-8f946bcdd42a · package remedy-review-20260724-180532-READY_FOR_REVIEW.zip · SHA-256 d81e54b4ea5716ab3f2c00593a3911457fff79121532bf63e3231c142496e7a9 · accepted HEAD 6799d12ed2b9f2c96b3410b150b09695c551691e)

## Tier 1 — Self-Build Bootstrap

- [x] F013 — Job intake (T001–T003 complete; accepted 2026-07-25 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f013_job_intake_closure · package remedy-review-20260725-184236-READY_FOR_REVIEW.zip · SHA-256 098bb64f72a8d08120852d280227d0805871ec41a0430b8d4c4ed7ee4509b9f1 · accepted HEAD ba6e6fe6d05e97197ca45c201a7914dc4ef20396)
- [x] F014 — Flight Plan (T001–T004 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 9b0a8b6d-f03f-46d2-9dba-7584da178cd9 · package remedy-review-20260726-001936-READY_FOR_REVIEW.zip · SHA-256 bc75040080964f67e3c2a19623f6626ecc7d73df891592c083d56f3c81b997d7 · accepted HEAD 162553a5f175965aa0c51baa6769efc8f9b727f1)
- [x] F016 — Scaling task granularity (T001–T003 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 1cc3b1c0-fd59-4884-9252-f8a8e79b5a59 · package remedy-review-20260726-165629-READY_FOR_REVIEW.zip · SHA-256 0a147595147fa300d0b6b7257e626394b365d689e3af540c536a0c477fb5a991 · accepted HEAD 85004253705e5eae15d969812af84738373e5453)
- [x] F034 — Bundled clarification in the Flight Plan (T001–T004 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job fd549b82-64b0-49c5-85d9-f5d8bf44a266 · package remedy-review-20260726-202004-READY_FOR_REVIEW.zip · SHA-256 429e6243f9c4b7b4e5c3a7465b75c490ae9f9ff567f67401c742bff4f6c348c7 · accepted HEAD d1c036ace9802d20bdb521e77905bdb7998c552e)
- [x] F046 — Multi-cycle loop (T001–T002 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job b4df73c4-f867-4869-b097-62aab0e6974f · package remedy-review-20260726-215057-READY_FOR_REVIEW.zip · SHA-256 8dfb264f92b3736a9a58bb5df82693f543fc5877a9b907a897bfb53a54ab7f90 · accepted HEAD 0216d871290362d4ee81a80c767aa4ba1d2bb985)
- [x] F047 — Checkpoint & resume (kill-proof) (T001–T003 complete; accepted 2026-07-27 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7 · package remedy-review-20260727-101857-READY_FOR_REVIEW.zip · SHA-256 b6f96e888d7e8a6d5494f213b845a644be34538e6fc17df9d469712efe98b380 · accepted HEAD 8e870062feb3487f890232d659ef569cf3aa326e)
- [x] F048 — Job queue (T001–T003 complete; accepted 2026-07-27 · live review PASS — ACCEPTED · Evidence job 58e88dd7-88c7-429f-823f-7b0e9bbb34f5 · package remedy-review-20260727-223612-READY_FOR_REVIEW.zip · SHA-256 6058d0f4d67ee082c852202e910fe05ff42a5e9406a3fd71464c251acf106a4b · accepted HEAD c6a0b58d13cec49abbf15c9dab08fd5e6a9e54ee)
- [x] F251 — Full-suite stabilization (flake-debt paydown) (S1–S5 complete, scope per operator ruling A 2026-07-28; accepted 2026-07-28 · live review PASS — ACCEPTED · Evidence job b680f05b-2cda-468f-a8c5-95dbe9636044 · package remedy-review-20260728-190328-READY_FOR_REVIEW.zip · SHA-256 95af04c380da89879bbf4f10cd2529279553a571c5c72b3870a190a90641af2f · accepted HEAD 86a0df39ee0928742add7ef457dbd3d1e4efb7f2)
- [x] F252 — Standing-red paydown (154 ids, 13 classes) (R1–R3 complete; accepted 2026-07-29 · live review PASS — ACCEPTED · Evidence job d9a16173-0283-40a1-957a-1ee9b7b39343 · package remedy-review-20260729-153036-READY_FOR_REVIEW.zip · SHA-256 7dfb5a511f2a4110997910e24d64ff09ea1d4c3ddf894623edf2569d6a58c6d8 · accepted HEAD d543d445cd1f9ecb6d092e64fe670881bc6fff67)
- [x] F050 — DAG scheduling (T001–T002 complete; accepted 2026-07-30 · live review PASS — ACCEPTED · Evidence job f987e3f1-bbe1-45ce-b964-c23805ecb5e6 · package remedy-review-20260730-145728-READY_FOR_REVIEW.zip · SHA-256 3d04713f33072ce544ab4c0a430e82fc8edeee85bcb0aaa007fa48ef9ee4d8c0 · accepted HEAD 2fd7d6b949b98022b977aa48c0191bbf0efceec1)
- [x] F051 — Escalate instead of block (unattended) (T001–T003 complete; accepted 2026-07-30 · live review PASS — ACCEPTED · Evidence job 785d275a-2f78-4b44-bd29-f8764ff95bb8 · package remedy-review-20260730-172315-READY_FOR_REVIEW.zip · SHA-256 e85932c425acf204d8e9c24a030d4988aecbe4d3779dc5b4a57193f4f7c0648a · accepted HEAD 54df8f7a1adea2f3d140efef22e2e6f991aea6ff)
- [x] F052 — Self-healing test rounds (T001–T002 complete; accepted 2026-07-31 · live review PASS — ACCEPTED · Evidence job 3b0b36c3-35c9-4b08-9f33-9d901bea839e · package remedy-review-20260731-095109-READY_FOR_REVIEW.zip · SHA-256 2f3fd6032cdaceca4461702b128b77a300485eb171a704081df18852d6224efe · accepted HEAD 2203610776926c76956423346c889503516f08d4)
- [x] F053 — Final & interim report (T001–T002 complete; accepted 2026-07-31 · live review PASS — ACCEPTED · Evidence job b4d6d7f5-8059-4c23-8f65-d47b319f35bd · package remedy-review-20260731-150146-READY_FOR_REVIEW.zip · SHA-256 64bcc0c5a97b6ce0c742db1feff61f55fb7b583fb24b9cb6ca864c40bc0a7b6c · accepted HEAD 8cca01f4150ba14791de367e78cd9b39599c299d)
- [x] F056 — Missions: persistent goal, jobs as execution units (T001–T003 complete; accepted 2026-07-31 · live review PASS — ACCEPTED · Evidence job 057a2de1dde14778 · package remedy-review-20260731-210415-READY_FOR_REVIEW.zip · SHA-256 b732f0bdd0a334a62091b127f4efbd392f612de98ec2a687f27e1ef36fd7e555 · accepted HEAD eaa86f51c5ae72ed4e310cdeb249eba3142c7e7c)
- [x] F061 — Definition-of-Done compiler (T001–T004 complete; accepted 2026-08-01 · live review PASS — ACCEPTED · Evidence job c5185517fa2443bf · package remedy-review-20260801-190945-READY_FOR_REVIEW.zip · SHA-256 486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8 · accepted HEAD 8dc6086c4da87ca2ec63c33c3e17904c29ee394d)
- [x] F062 — Product smoke as the closing gate (T001–T003 complete; accepted 2026-08-01 · live review PASS — ACCEPTED · Evidence job 76ee4cb7318e409e · package remedy-review-20260801-214231-READY_FOR_REVIEW.zip · SHA-256 46e684f5954a32c92994781a734bf3c26d830ba288e63d48fe4d5dc441b8ab29 · accepted HEAD 52a283cfb0d3b774d105d6dd5d96bed5464af615)
- [x] F069 — Mission compiler (T001–T003 complete; accepted 2026-08-03 · live review PASS — ACCEPTED · Evidence job cee98ee1ec623232 · package remedy-review-20260803-103015-READY_FOR_REVIEW.zip · SHA-256 4b7433157232acb774101da9885665ce71068a0741ca6c07287260932359c000 · accepted HEAD 4dce6060a4b663a6546e40432c5abbd18e9ddd93)
- [x] F070 — Orchestrator loop inside Remedy (T001–T003 complete; accepted 2026-08-03 · live review PASS — ACCEPTED · Evidence job 2edd34878e5c4fbc · package remedy-review-20260803-143749-READY_FOR_REVIEW.zip · SHA-256 5c559751d7a4710c9495a69899d9f0966b045047392748e709403a8347d16805 · accepted HEAD f1fad962b1ec4203dafdb146f3e90fad8111550e)
- [x] F071 — Mission dossier (T001–T003 complete; accepted 2026-08-03 · live review PASS — ACCEPTED · Evidence job b3b98e3ee1d10668 · package remedy-review-20260803-190339-READY_FOR_REVIEW.zip · SHA-256 aa117e26a55b0ab1b1941d881a4ed510967c2d1669be021abda30ab0f6e9e99e · accepted HEAD acb02acd8a41dc2a8ba89e2db023b1840814adff)
- [x] F075 — MILESTONE GATE: 10 flawless self-runs (T001–T003 complete; accepted 2026-08-05 · live review PASS — ACCEPTED · Evidence job b1b6eb7ed4962309 · package remedy-review-20260805-144354-READY_FOR_REVIEW.zip · SHA-256 d63cda6b2b9e83bf993889d33fa716646f712f90eabc992a472d12390b8910d3 · accepted HEAD 36f3bc8150a9bdaae3c1e3a743c1621998c48691)
- [x] F079 — Context handoffs (T001–T003 complete; accepted 2026-08-06 · live review PASS — ACCEPTED · Evidence job a7f0791c4d6b2e58 · package remedy-review-20260806-203747-READY_FOR_REVIEW.zip · SHA-256 f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec · accepted HEAD abc33f79aac937d3504dddef7a72bdb22d4aa2d1)
- [x] F080 — Machine-readable roadmap mirror & STATUS.md (T001–T003 complete; accepted 2026-08-07 · live review PASS — ACCEPTED · Evidence job f080-closure · package remedy-review-20260807-095605-READY_FOR_REVIEW.zip · SHA-256 5924c6f6ae8f93f790f9d3c9279d026c9682a547206355a580746333d5ca25cd · accepted HEAD 0a22bcbf31322a365354d755b92d90b8fed20493)

## Tier 2 — Minimal Self-Build Runtime

- [x] F103 — Token ledger (SQLite) (T001–T003 complete; accepted 2026-08-08 · live review PASS — ACCEPTED · Evidence job f103-closure · package remedy-review-20260808-210612-READY_FOR_REVIEW.zip · SHA-256 8e967d78e57fa97641365b4baa91ca884f6322bc855f678d1daeb146c9dd38ad · accepted HEAD 65e1eec25e61c1d0fe78539adeb890d3426cb605)
- [x] F104 — Hard budget enforcement (T001–T003 complete; accepted 2026-08-09 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f104-closure · package remedy-review-20260809-033908-READY_FOR_REVIEW.zip · SHA-256 6117b6b02ca6f641f0ef3bfebe7518d0eaf705e609e17e8ee9493e6d7fd8bb6a · accepted HEAD 68a7412019e92232a880625b7fce4e48c7198744)
- [x] F105 — Cache-optimal prompt ordering (T001–T004 complete; accepted 2026-08-12 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f105-closure · package remedy-review-20260812-092055-READY_FOR_REVIEW.zip · SHA-256 23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840 · accepted HEAD b928a0c691dc0a2b86c149a5e732ea07ac03176e)
- [x] F107 — Context compiler v2 (T001–T004 complete; accepted 2026-08-12 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f107-closure · package remedy-review-20260812-235227-READY_FOR_REVIEW.zip · SHA-256 4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d · accepted HEAD b823dff9b4711ec3cc3505b496589cd02e219fc4)
- [x] F111 — Diff-only repair (T001–T003 complete; accepted 2026-08-13 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f111-closure · package remedy-review-20260813-060242-READY_FOR_REVIEW.zip · SHA-256 c44b4a12a5715a66bf3abd55633fc86a77351b0018fab930f374e707458d79e6 · accepted HEAD a2fe520bd16773e4f1536035caeec76e880bbdde)
- [x] F115 — Prompt breakdown & cost report (T001–T003 complete; accepted 2026-08-13 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f115-closure · package remedy-review-20260813-142842-READY_FOR_REVIEW.zip · SHA-256 bf28ae9dfebc9ef9d2e3f57a7ad9d76155cfe35a0cc5e2b7090426aa6f7a447e · accepted HEAD 705feeb19c871db6313828d76ad4e1d9e0cc4d58)
- [x] F045 — Loop definitions (T001–T003 complete; accepted 2026-08-14 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f045-closure · package remedy-review-20260814-032227-READY_FOR_REVIEW.zip · SHA-256 a4dc01e441bdba9713061c6c04012576f6732f0bad20b6a48d1224b21f257723 · accepted HEAD 1c84c81805668e1d0f1e04370d5366389c8a8b20)
- [x] F057 — Rate-limit-aware scheduler (T001–T003 complete; accepted 2026-08-14 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f057-closure · package remedy-review-20260814-085403-READY_FOR_REVIEW.zip · SHA-256 202b289122faf62a8d27c5e658ee6b80fcff0a23ee6db25fbe50c5376f6bda19 · accepted HEAD abda479da68661ce9ed8073bd3887b9fa783e092)
- [x] F077 — Autonomy watchdog (T001–T003 complete; accepted 2026-08-14 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f077-closure · package remedy-review-20260814-161744-READY_FOR_REVIEW.zip · SHA-256 47d66bdafeb5d86ed4c03033553cbc73e8cc09d78dff6e2a6558b4878faf8ccd · accepted HEAD 01764a52923c0d9850fab9cf5f6b52b44c9c69d8)
- [x] F082 — Self-benchmark (T001–T003 complete; accepted 2026-08-15 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f082-closure · package remedy-review-20260815-122333-READY_FOR_REVIEW.zip · SHA-256 3e8e33eb4bb724ce775ea5987e0fee0de5341d1a3bfe902c6e5f4f6f2deb84b2 · accepted HEAD 4b9bc7bc1dabdde5fca68de6ae20f86b11d21eb0)
- [x] F083 — CI self-check (T001–T003 complete; accepted 2026-08-16 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f083-closure · package remedy-review-20260816-082019-READY_FOR_REVIEW.zip · SHA-256 162bacf6265e79651b098c524b5060de44d58e9d89e9ec4d645c158950b78986 · accepted HEAD 83f3eb31f5020bc5201a23b06e23e7558ee01b4e)
- [x] F085 — Sandbox hardening (stage 1) (T001–T003 complete; accepted 2026-08-19 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f085-closure · package remedy-review-20260819-203439-READY_FOR_REVIEW.zip · SHA-256 951d05c41f7c9ab5ee4dc0428b8be17e981b09738c20587f5c6c31b020296ad6 · accepted HEAD 617ef70a3d566abed1ca68a034570636636edad5)
- [x] F254 — Model alias table & dead-model doctor check (R1–R12 complete; accepted 2026-08-07 · live review PASS — ACCEPTED · Evidence job f254-closure · package remedy-review-20260807-204305-READY_FOR_REVIEW.zip · SHA-256 1b4995fa9e3ab76f7be8398be66ed69ec47e99f6e825d16cc97aa826a95a05c0 · accepted HEAD b71c9bdd93cbeb21d4b98842cdf6baa998c3ac26)
- [x] F086 — Release capability (T001–T003 complete; accepted 2026-08-20 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f086-closure · package remedy-review-20260820-200318-READY_FOR_REVIEW.zip · SHA-256 bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855 · accepted HEAD f5fa19c368ed15d14ee6067fc69fde4fbc7863a6)
- [ ] F267 — List commands v2 completion — sort/filter/limit for the remaining nine commands

Milestone R1 — Remedy as the daily tool: Tier 2 complete (F086 as the self-install/update vehicle). Build-first ends here; use-first begins — from here the order follows the Self-Use sequence below.

## Tier 5 — Operator Cockpit (parallel human track)

- [x] F255 — Teacher role (evidence-grounded live explainer & learn-along tutor) (T001–T004 complete; accepted 2026-08-21 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f255-closure · package remedy-review-20260821-051015-READY_FOR_REVIEW.zip · SHA-256 f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2 · accepted HEAD c96f82c3372520bfd0545c7ce640886479197a08)
- [x] F008 — SSE event stream (T001–T003 complete; accepted 2026-08-21 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f008-closure · package remedy-review-20260821-193052-READY_FOR_REVIEW.zip · SHA-256 1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366 · accepted HEAD 870f198ea9c0e4b51075f3386d1025cce805811a)
- [x] F009 — The single write channel (T001–T003 complete; accepted 2026-08-22 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f009-closure · package remedy-review-20260822-085607-READY_FOR_REVIEW.zip · SHA-256 ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f · accepted HEAD 97d028980b5781cbf22a0f651f7e879eea1a0485)
- [x] F021 — Live activity feed + "agent is doing now" (T001–T003 complete; accepted 2026-08-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f021-closure · package remedy-review-20260823-005026-READY_FOR_REVIEW.zip · SHA-256 be70b65dd4a397ac7697a3c37b2f5cfb1a52197c9434cde67dec4a0a502e3dd8 · accepted HEAD a0a883f7bf47e92bd3c084d127bf56f5f4feaad2)
- [x] F022 — Live cost ticker (T001–T003 complete; accepted 2026-08-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f022-closure · package remedy-review-20260823-135731-READY_FOR_REVIEW.zip · SHA-256 85fe27aaeefe0b885b6b2fe081187cff51a0e070ae7d9d5320e7d57d1e150f58 · accepted HEAD f215ced4998f6eb6e5ca82117d889b70777ffe12)
- [x] F031 — Decision inbox (T001–T003 complete; accepted 2026-08-27 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f031-closure · package remedy-review-20260827-122441-READY_FOR_REVIEW.zip · SHA-256 4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa · accepted HEAD f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5)
- [x] F032 — Approval with the evidence triple (T001–T003 complete; accepted 2026-08-28 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f032-closure · package remedy-review-20260828-032101-READY_FOR_REVIEW.zip · SHA-256 a368e28c61381e17de4bb46a5b35ecc975046be85d456983adf469759c1e2cf4 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD c3cf408f537de393bb156e45feae46d5de9f63da)
- [x] F037 — Rendered diff viewer (T001–T003 complete; accepted 2026-08-28 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f037-closure · package remedy-review-20260828-142213-READY_FOR_REVIEW.zip · SHA-256 c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e)
- [x] F256 — Diff viewer completion (T001–T003 complete; accepted 2026-08-28 · live review PASS — ACCEPTED · Evidence job f256-closure · package remedy-review-20260828-233819-READY_FOR_REVIEW.zip · SHA-256 5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD c6775b3c41f1d1fa4b0f4bb7907307573855a61b)
- [x] F257 — Self-use track (T001–T002 complete; accepted 2026-08-29 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f257-closure · package remedy-review-20260829-031830-READY_FOR_REVIEW.zip · SHA-256 0a4b5fc189ac7ed6b968f878b1186a23e2d5ac3425b6d1f46faad271b157acdd · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD fb10b3754978d9fc4112b2818eb9e7e31f4fdc78)
- [x] F033 — Hunk-level diff approval (T001–T003 complete; accepted 2026-08-29 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f033-closure · package remedy-review-20260829-154912-READY_FOR_REVIEW.zip · SHA-256 3b646ca5a18f10ae21f3218a753be00970762ba0fe4513ef53a3f60a9f711ccc · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 8738c5f1643b2bd667bc796257a4ddc502f36191)
- [x] F040 — Completion/return digest (T001–T003 complete; accepted 2026-08-30 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f040-closure · package remedy-review-20260830-033225-READY_FOR_REVIEW.zip · SHA-256 26bacc72356bea20d765736996cb353033d087c328e7af0156548a533d164be1 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 5281987a142b97f222256c987d36c009ae7ab3ae)
- [x] F258 — Self-use track v2 (T001–T003 complete; accepted 2026-08-30 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f258-closure · package remedy-review-20260830-084541-READY_FOR_REVIEW.zip · SHA-256 4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 49fcc2c645601936d8c426b1eb09523b9b3c7f6f)
- [ ] F015 — Interactive plan editing
- [ ] F019 — Live node materialization
- [ ] F020 — Node lifecycle & glyph language
- [ ] F023 — Semantic zoom L0–L3
- [ ] F024 — Phase timeline with scrubber
- [ ] F025 — Pause/resume (global & per node)
- [ ] F026 — Task edit at runtime
- [ ] F027 — Task veto
- [ ] F028 — Task injection
- [ ] F029 — Subtree rerun
- [ ] F030 — Steering messages
- [ ] F035 — Ownership ledger
- [ ] F036 — Guided result tour
- [ ] F038 — Grounded chat & intent dispatch
- [ ] F039 — Story/replay mode
- [ ] F041 — Artifact preview
- [ ] F042 — Multi-project cockpit
- [ ] F043 — Explanation layer
- [ ] F044 — Command palette, keyboard, performance budget

## Tier 12 — Observability & Operations

- [ ] F200 — Daemon mode (remedy serve)
- [ ] F201 — Remote access & mobile view
- [ ] F199 — Self-health & crash reports
- [ ] F203 — Structured logging & correlation
- [ ] F202 — Backup/restore & schema migrations
- [ ] F198 — Prometheus metrics endpoint
- [ ] F204 — Update channel & change transparency
- [ ] F253 — Headless API contract

## Tier 3 — Full Token Economy & Autonomy Extension

- [ ] F113 — Local models for side roles
- [ ] F116 — Cost anomaly alarm
- [ ] F049 — Parallelism
- [ ] F054 — Auto-revert proposal
- [ ] F055 — Rehearsal (dry check)
- [ ] F058 — Model failover chain
- [ ] F059 — Notifications
- [ ] F060 — Long-run certificate
- [ ] F063 — Idea engine v1
- [ ] F064 — Idea queue UI/CLI
- [ ] F065 — Idea engine v2 (continuous, opt-in)
- [ ] F066 — Idea provenance
- [ ] F067 — Routine missions
- [ ] F068 — Autonomy balance (on demand)
- [ ] F072 — Spec-first (living specification)
- [ ] F073 — Post-mortem miner → playbook proposals
- [ ] F074 — Estimate calibration
- [ ] F076 — Vision-capable planner
- [ ] F078 — Autonomy levels
- [ ] F084 — Demo mode

## Tier 4 — Memory & Learning

- [ ] F117 — Card format & store
- [ ] F118 — Deterministic card attachment
- [ ] F119 — Card UI: the collection
- [ ] F120 — Automatic card harvesting
- [ ] F121 — Decision cards from ADRs
- [ ] F122 — Project dossier card
- [ ] F123 — Effectiveness KPI
- [ ] F124 — Card hygiene (manual + periodic)
- [ ] F125 — Card scopes & inheritance
- [ ] F126 — Cards in the graph
- [ ] F127 — Optional retrieval above threshold
- [ ] F128 — Memory as a detachable module
- [ ] F144 — Capability ladder
- [ ] F145 — Playbook distillation
- [ ] F149 — remedy study (initial analysis as a card draw)
- [ ] F150 — Card value & exploration chance

## Tier 7 — Quality & Trust

- [ ] F129 — TDD gate (optional per job)
- [ ] F130 — Mutation sampling
- [ ] F131 — Adversarial second review
- [ ] F132 — Review tournament
- [ ] F133 — Provider trust score
- [ ] F134 — Security gate
- [ ] F135 — Flaky detector
- [ ] F136 — Time-travel checkpoints
- [ ] F137 — Shadow mode
- [ ] F138 — ADR automation
- [ ] F139 — Code churn metric
- [ ] F140 — Bit-exact evidence replay
- [ ] F141 — Permission matrix per autonomy level
- [ ] F142 — Trust dashboard
- [ ] F143 — Genesis run: one prompt → one product

## Tier 6 — Design-to-Code

- [ ] F087 — design_reference as job input
- [ ] F088 — Reference image to the builder
- [ ] F089 — Design decomposition
- [ ] F090 — Screenshot capability
- [ ] F091 — Visual self-comparison
- [ ] F092 — Visual reviewer
- [ ] F093 — Fidelity loop
- [ ] F094 — Interaction verification
- [ ] F095 — Responsive verification
- [ ] F096 — Design token extraction
- [ ] F097 — Component catalog
- [ ] F098 — Baseline guard (visual regression)
- [ ] F099 — Design feedback channel
- [ ] F100 — Multi-reference consistency
- [ ] F101 — Reference fidelity rule
- [ ] F102 — Long-run × design

## Tier 11 — Verification v2

- [ ] F187 — Property-based test generator
- [ ] F188 — API compatibility guard
- [ ] F189 — Service contract tests
- [ ] F190 — Test environment provisioning
- [ ] F191 — Migration safety
- [ ] F192 — Performance budgets for product code
- [ ] F193 — Accessibility gate
- [ ] F194 — i18n checks
- [ ] F195 — Budgeted fuzzing
- [ ] F196 — Flake-resistant E2E discipline

## Tier 8 — Worker Ecosystem & Neutrality

- [ ] F151 — Worker adapter contract v2
- [ ] F152 — Worker config isolation
- [ ] F153 — Codex CLI adapter
- [ ] F154 — Gemini CLI adapter
- [ ] F155 — Local full builder
- [ ] F157 — Capability matrix & honest degradation
- [ ] F158 — Cost normalization & price catalog
- [ ] F161 — MCP passthrough with policy
- [ ] F162 — Sandbox profiles per adapter

## Tier 9 — Evidence & Compliance Product

- [ ] F164 — AI labeling in commits (standard)
- [ ] F171 — Secret hygiene v2 & vault

## Tier 15 — Intelligence v2

- [ ] F223 — Best-of-N builds
- [ ] F224 — Repo archaeology as a context source
- [ ] F225 — Reverse-DoD from legacy
- [ ] F226 — Classic risk prediction
- [ ] F227 — Prompt regression tests
- [ ] F228 — Counterfactual cost replay
- [ ] F229 — Adaptive task-size recommendation
- [ ] F230 — Mission portfolio optimizer
- [ ] F231 — Playbooks v2 with value ranking
- [ ] F232 — Model upgrade playbook

## Tier 13 — Multi-Repo & Organization

- [ ] F205 — Multi-repo missions
- [ ] F206 — Repo dependency catalog
- [ ] F208 — Monorepo workspaces

## Tier 16 — Cockpit v2

- [ ] F233 — Growing Brain stage 2 (GPU renderer)
- [ ] F235 — Diff ghosting on the timeline
- [ ] F236 — Live output stream in the node
- [ ] F237 — Embedded runtime console
- [ ] F240 — Power keyboard & vim navigation
- [ ] F241 — Story export as video
- [ ] F242 — Accessibility of the cockpit itself

## Tier 17 — Self-Improvement & Ecosystem

- [ ] F244 — Security self-audit routine
- [ ] F248 — Remedy builds Remedy: the full loop
- [ ] F250 — Long-term consolidation into a project handbook

## Package 2 — Parked: Product & Governance

Registered, counted and tier-assigned like every other feature — deliberately last. These lines exist for the product path (teams, sales, compliance-as-product, ecosystem APIs) and rest until an operator decision moves them back into Package 1. Known product-scoped dependencies of scheduled features into this package: F201 depends on F176, F236 depends on F174, and F232 depends on F156/F159; the Self-Use rounds for those substitute a local mechanism by operator ruling at claim time (for F232: the F082 self-benchmark stands in for certification and scoreboard), documented in the feature round itself.

## Tier 8 — Worker Ecosystem & Neutrality

- [ ] F156 — Worker certification suite
- [ ] F159 — Cross-vendor benchmark & scoreboard
- [ ] F160 — Cross-vendor failover v2

## Tier 9 — Evidence & Compliance Product

- [ ] F163 — Prompt->code lineage (audit trail v2)
- [ ] F165 — Signed certificates
- [ ] F166 — Retention & archive export
- [ ] F167 — SIEM / audit event export
- [ ] F169 — Human-oversight proof
- [ ] F168 — Technical dossier generator
- [ ] F170 — License & SBOM gate
- [ ] F172 — Policy packs
- [ ] F173 — Air-gap mode
- [ ] F174 — Data classification in the context compiler

## Tier 10 — Team & Multi-User

- [ ] F175 — Identities & roles
- [ ] F176 — SSO/OIDC for the cockpit
- [ ] F177 — Multi-user write channel
- [ ] F178 — Decision assignment & delegation
- [ ] F179 — Node comments
- [ ] F180 — Human reviews as a gate
- [ ] F181 — Team ownership & contribution view
- [ ] F182 — Presence display
- [ ] F183 — Per-person notification routing
- [ ] F184 — Shared card curation
- [ ] F185 — Per-project permissions
- [ ] F186 — Human-to-human handoff package

## Tier 12 — Observability & Operations

- [ ] F197 — OpenTelemetry export (GenAI conventions)

## Tier 13 — Multi-Repo & Organization

- [ ] F207 — Coordinated PR trains
- [ ] F209 — Org conventions with inheritance
- [ ] F210 — Organization dashboard
- [ ] F211 — Card federation
- [ ] F212 — Release train view

## Tier 14 — Productization & Distribution

- [ ] F213 — Licensing & activation
- [ ] F214 — Editions & honest feature gating
- [ ] F215 — Distribution & signed binaries
- [ ] F216 — Docs site generator
- [ ] F217 — Templates & example gallery
- [ ] F218 — Trial mode
- [ ] F219 — Telemetry strictly opt-in
- [ ] F220 — Feedback funnel
- [ ] F221 — Release quality gate & channels
- [ ] F222 — Customer cost calculator

## Tier 16 — Cockpit v2

- [ ] F234 — Organism overview (L-1)
- [ ] F238 — Cockpit plugin API
- [ ] F239 — Theming & white-label

## Tier 17 — Self-Improvement & Ecosystem

- [ ] F243 — Public benchmark participation
- [ ] F245 — Evidence schema registry & versioning
- [ ] F246 — Verification gate plugin API
- [ ] F247 — Community import with provenance
- [ ] F249 — Anonymized research exports
