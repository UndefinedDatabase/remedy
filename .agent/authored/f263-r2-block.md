STEP F263 R2 — BOOK ROUND 1 AND FINISH T001: the human change record joins the evidence package

GOAL
Book round 1's PASS and DECISION F263 D2, then finish T001: the job's evidence export copies
every human change record into the bundle, verifies each COPY into
`human_change_integrity.json`, and a record that does not verify blocks the final verifier and
the review package's READY gate, exactly as a lost post-mortem does.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS SHAPE
T2_F263.md's Design gives the record "the same standing as any other evidence artifact".
DECISION F263 D2 (the decisions.md payload) states how: a third integrity artifact beside
`postmortem_integrity.json` and `manifest_integrity.json`, read by the final verifier and
required by `scripts/build_review_manifest.py` as a closed-schema READY gate, and written
intact-and-empty by the closure's own manual-completion producer so a closure package stays
READY. Two existing fixture helpers that assemble an all-pass gate set gain the new gate; the
reviewer measured that without them 29 review-package tests go red.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r2-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f263-r2-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f263-human-change-absorption`, and `git log --oneline -1` must read `a34cc4b0`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2337 | 4337975386093b44ed87b9f704a2ed8e98161069f1171ad7b0eebb159dd4a9c6 |
| decisions.md | 43 | 3200 | 24204db03f40651fd460abe6752560f69117cb560ee0072ae5f430670d6309e1 |
| plan.md | 31 | 1272 | dc323c4f92daeefe6710069fcc88f9b971df6f54636e2178b624518b92587790 |
| product.diff | 173 | 9741 | f8d31e3e732a5f223ec9d0f34e27975662a4aa7749787385553b726442ef26b5 |
| fixtures.diff | 35 | 2637 | daf155063e706dfd7815b0455842aef74c747e8897fd389e25208eef5b18d17d |
| docs.diff | 14 | 807 | 0a046113ac039460dee5d2392ded33c8c3edebd536402cb0879da102ab7afd06 |
| test_human_change_evidence.py | 155 | 6925 | abeb56888b1a7da7eb16aa24484333330a98dbc7073e7032ef001cb18249a512 |
| mutations.py | 81 | 3178 | 129b7815e2a5dd9f2fb778893f3cda6ffc81012dc6b6a21967be2694608b6e07 |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation: each begins with the single
newline that separates records, because `.agent/live_review.md` and `.agent/decisions.md` each
end in exactly one newline. `plan.md` is a REWRITE of `.agent/plan.md`.
`test_human_change_evidence.py` is a NEW FILE at
`tests/orchestration/test_human_change_evidence.py`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated each from a tree at `a34cc4b0` and applied all three, in
the order below, to a fresh worktree at `a34cc4b0`, every `git apply --check` and `git apply`
at real exit code 0. `product.diff` edits `packages/orchestration/human_change.py`,
`packages/orchestration/job_evidence.py`, `packages/orchestration/final_verifier.py`,
`packages/orchestration/manual_attestation.py` and `scripts/build_review_manifest.py`;
`fixtures.diff` edits `tests/orchestration/test_review_authoritative_e2e.py` and
`tests/orchestration/test_review_package_status.py`; `docs.diff` edits
`docs/roadmap/STATUS_closure_protocol.md`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f263-r2-block.md` := this block, and one
  `.agent/authored/f263-r2-<name>` for each of ledger.md, decisions.md and plan.md, keeping
  each payload's own file name. All by `shutil.copyfile`.
  Subject: `F263 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 76. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  One `.agent/authored/f263-r2-<name>` for each of product.diff, fixtures.diff, docs.diff,
  test_human_change_evidence.py and mutations.py, by `shutil.copyfile`.
  Subject: `F263 R2 C1b: copy round 2 product payloads into .agent/authored/`
  Expected insertions: 458.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F263 R2 C2: book round 1's PASS and DECISION F263 D2`
  Expected insertions by `git show --numstat`: 43 decisions.md, 2 live_review.md, 8 plan.md.

C3 — THE EVIDENCE PATH, one commit, because the product, the fixtures it forces and the tests
  that verify it stand or fall together: `git apply --check` then `git apply` for
  product.diff, fixtures.diff and docs.diff in that order, then copy
  test_human_change_evidence.py to `tests/orchestration/test_human_change_evidence.py` and
  `git add` every path.
  Subject: `F263 R2 C3: carry human change records into the evidence package and block on a broken one`
  Expected insertions: 2 STATUS_closure_protocol.md, 9 final_verifier.py, 38 human_change.py,
  8 job_evidence.py, 3 manual_attestation.py, 9 build_review_manifest.py,
  155 test_human_change_evidence.py, 3 test_review_authoritative_e2e.py,
  2 test_review_package_status.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`,
  WITH the item-status table AGENTS.md requires — one row per commit and per gate. Round 1's
  handback omitted it; this round's must carry it.
  Subject: `F263 R2 C4: rewrite handoff for round 2`
  Then `git push origin feature/f263-human-change-absorption` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f263-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/human_change.py`, `packages/orchestration/job_evidence.py`,
   `packages/orchestration/final_verifier.py`, `packages/orchestration/manual_attestation.py`,
   `scripts/build_review_manifest.py`, `tests/orchestration/test_review_authoritative_e2e.py`,
   `tests/orchestration/test_review_package_status.py`,
   `docs/roadmap/STATUS_closure_protocol.md`,
   `tests/orchestration/test_human_change_evidence.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only a34cc4b0 <C4>` gives. `scripts/build_review_zip.py` is NOT in it
   (DECISION F263 D2 (6)).
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite (amend0917 rule 1); F263's one run belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f263-r2-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f263-r2-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `a34cc4b0` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 373452 | 1ed2113b5de484068134735d52690072871b06d0b2364c1f3271e62e6efd70c7 |
 | .agent/decisions.md | 1881309 | b1ce8ec76905935c5572d0722588e3a54c4d62ca4b7280f7d49d850c2c3c8894 |
 | .agent/plan.md | 1272 | dc323c4f92daeefe6710069fcc88f9b971df6f54636e2178b624518b92587790 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `a34cc4b0` and at C2, with both set differences (the reviewer read 28, 28, both empty).

G3 THE PRODUCT BYTES — at C3, the sha256 of each file read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/human_change.py | 11553 | e6c99c569a46728c94f4bc44f7e3665194069b1c9f77fd4bab3dc36b0caad3a1 |
 | packages/orchestration/job_evidence.py | 137619 | a0f8f792e72c70825253945f299a2ef4e839d50b96d06b119c2455ade420817f |
 | packages/orchestration/final_verifier.py | 45021 | 098f313906c57335760dffbb1697eb14bad44216edc96693dd814a3fc6eb4eea |
 | packages/orchestration/manual_attestation.py | 16334 | 11cc966952dd572d5217d82a7d99cc6b6ed41868602ff27e3fb501dd7c1888e3 |
 | scripts/build_review_manifest.py | 180741 | 3ef54bb3fa9e8aa0280702d5edf7630c74374126f2f41c5eb426520b40a66d6f |
 | tests/orchestration/test_review_authoritative_e2e.py | 20641 | 2c58f0ad10e2f91e84b01cefeed522aebf49f09cc4a2144113ee7f04c003b45b |
 | tests/orchestration/test_review_package_status.py | 37968 | d7cafa28e2debcbda059debbfea2f39279a22171ffcb199f224667979658a841 |
 | docs/roadmap/STATUS_closure_protocol.md | 20232 | 689ab1f11cba0565023b1557f4b9f8b391655172cacefa45d3fa84dfe173c344 |
 | tests/orchestration/test_human_change_evidence.py | 6925 | abeb56888b1a7da7eb16aa24484333330a98dbc7073e7032ef001cb18249a512 |

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_human_change_evidence.py tests/orchestration/test_human_change.py tests/orchestration/test_review_*.py tests/orchestration/test_failure_wiring.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_f018_package_pipeline_e2e.py tests/orchestration/test_repair_attest.py tests/orchestration/test_job_evidence.py tests/orchestration/test_job_evidence_verification_contract.py tests/orchestration/test_final_verifier.py tests/orchestration/test_manual_attestation.py tests/orchestration/test_manual_completion_bundle.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path, serially, in a disposable worktree
 carrying C2 and C3 and read `1874 passed, 2 skipped` at real exit code 0; report what you
 read. Then `python3 -m ruff check` over every Python path of the G3 table — the docs file
 excluded — real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r2-mut <C3>`, then
 `python3 -B .remedy-wt/f263-r2-payloads/mutations.py .remedy-wt/f263-r2-mut` and report its
 whole output. The script runs `tests/orchestration/test_human_change_evidence.py` and
 `tests/orchestration/test_review_package_status.py`. The reviewer read, over the same script
 against its own tree carrying C2 and C3:
 control_before `43 passed` at exit 0;
 m1 (the export never verifies a copy) 2 failed at exit 1;
 m2 (the job export writes no integrity file) 2 failed at exit 1;
 m3 (the final verifier reads no failures) 2 failed at exit 1;
 m4 (the verdict ignores the block) 1 failed at exit 1;
 m5 (the manifest does not require the gate) 2 failed at exit 1;
 m6 (the manifest ignores a blocked verifier) 1 failed at exit 1;
 m7 (the manual completion bundle writes no integrity file) 1 failed at exit 1;
 control_after `43 passed` at exit 0, with every `restored byte-identical` line `True`.
 Then `git worktree remove --force .remedy-wt/f263-r2-mut`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C4, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 6`, showing C4, C3, C2, C1b, C1a and then `a34cc4b0`;
 `git worktree list`, the primary checkout and the three `.remedy-wt/job-*` worktrees only;
 the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the ITEM-STATUS
TABLE, the deviations, and the next expected action. Your Session section reads SESSION 1 of
feature F263, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then T002 — `remedy absorb`, the explicit command over the same `absorb` path.
State the open-findings count, 28, and the operator-questions count, 0.
