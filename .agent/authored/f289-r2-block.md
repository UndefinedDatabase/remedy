STEP F289 R2 — BOOK ROUND 1, RECORD DECISION F289 D2, AND LAND T001: the documentation-staleness catalog of twelve checks, each proven red on a stale fixture, and the self-use generator's Tier 2

GOAL
Round 1 passed. Book its verdict and R-1073's resolution, record one prose-slip line and DECISION
F289 D2, and land T001: a NEW FILE at `packages/orchestration/doc_staleness.py` holding twelve
checks that compare what the README, the docs index, the guides and the command catalog claim with
what ships, and `_doc_staleness_tier` in `packages/orchestration/self_use_generator.py` rendering
the first stale claim no queue entry targets as a one-task job.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S6 below. Only the `.agent/`
records travel as payloads. Read DECISION F289 D2 in the records payload before you write code.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f289-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f289-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f289-r2-dry/`, `.remedy-wt/f289-r2-sim/`, `.remedy-wt/f289-r2-drafts/` and
  `.remedy-wt/f289-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f289-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f289-self-use-sources`, and `git log --oneline -1` must read `8163cf8b`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f289-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f289-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1047 | 05a0050cbcef3db2483c4a6fd4505b74cb24419c7d78cb6134462fbf0bcbe627 |
| records.diff | 83 | 12528 | d7fd3e1f56f2f345881cabc3c49a6de63e744fac169a8e00f1cefed499988042 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `8163cf8b`. It replaces the `Landed: R-1073` line
of `.agent/live_review.md` with the reviewer's `Done: R-1073` paragraph and appends round 1's gate
entry, appends one line to `.agent/prose_slips.md`, and appends DECISION F289 D2 to
`.agent/decisions.md`.

THE SPECIFICATION
Below, README is `README.md`, INDEX is `docs/README.md`, and GUIDES is every `docs/guides/*.md` in
sorted order, all read relative to the root a check is given. A FENCE is a region between a line
starting with three backticks and the next such line. A LINK is `[text](target)`; a RELATIVE link's
target does not start with `http://`, `https://` or `mailto:`. A SPAN is the text between a pair
of single backticks on one line. A KEY NAME matches `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+`, and a
KEY PREFIX is the first dot-separated segment of any registered config key.
S1 THE TYPES in the NEW FILE `packages/orchestration/doc_staleness.py`, whose docstring names
   T5_F289.md T001 and DECISION F289 D2: frozen `StaleClaim(check_id, document, claim, truth)`
   with a `key` property answering `f"{check_id}:{document}:{claim}"`; frozen `ShippedTruth` of
   `groups` (a mapping of every group id and alias to its group id), `command_pairs` (a frozenset
   of `(group_id, subcommand)`), `command_ids`, `config_keys`, `env_vars` (frozensets of str) and
   `catalog_texts` (a tuple of `(label, text)` pairs, one per `CommandEntry.description`,
   `ArgDef.help` and `GroupDef.description`, labelled like `job.run --reason help`), with a
   classmethod `live()` building it from `apps.cli.command_catalog` (`CATALOG`, `GROUPS`) and
   `packages.orchestration.config.all_key_specs()`, both imported INSIDE `live()`; frozen
   `StalenessCheck(check_id, documents, claim, truth, run)` whose three text fields each say in a
   sentence what the check reads, extracts and compares, and whose `run(root, truth)` answers a
   tuple of `StaleClaim`. `CHECKS` is the tuple of the twelve below, in this order, with unique
   ids. `run_staleness_checks(root: Path | None = None, truth: ShippedTruth | None = None)`
   defaults to the repository root (`Path(__file__).resolve().parents[2]`) and
   `ShippedTruth.live()`, and answers every check's claims in catalog order, each check's in
   document order and then line order. A document absent under the root yields nothing; an
   `OSError` reading one propagates. No `subprocess`, no network, no `except Exception`.
S2 THE CHECKS — each `StaleClaim`'s `document` is the repository-relative path of the file the
   claim was read from (`apps/cli/command_catalog.py` for C12), `claim` is one line of text quoting
   or naming what the document says or omits, and `truth` is one line saying what ships instead.
   Fences are skipped by every check except C08, which reads only fences.
   C01 `docs_index_guide_registration`, INDEX: for every GUIDES file, a link whose target is
     `guides/<name>` must occur in the section under `## Quick-Find Table` and in the section whose
     heading starts `## Guides`, each section running to the next `## ` heading; each missing
     occurrence is a claim naming the file and the section. A link to `guides/<name>` in either
     section that does not exist under the root is a claim too.
   C02 `config_cli_table_complete`, `docs/guides/remedy-toml-user-guide.md`, the section under
     `## CLI commands`: the word after `remedy config ` in every span starting `remedy config ` is
     a documented subcommand. Each documented subcommand no `config` command pair holds is a
     claim, and each subcommand the pairs hold that the section never documents is a claim.
   C03 `docs_index_command_lines`, INDEX: every span starting `remedy ` whose second word starts
     with a lowercase letter. A second word that is not in `groups` is a claim; otherwise a third
     word that starts with a lowercase letter must form, with the resolved group id, a pair in
     `command_pairs`, and a missing pair is a claim. A span with no third word, or one starting
     with `-` or `<`, is not read further.
   C04 `guide_relative_links`, GUIDES: every relative link whose target does not start with `#`,
     with any `#fragment` removed, must resolve to an existing path against the guide's own folder.
   C05 `link_anchors_resolve`, README, INDEX and GUIDES: every relative link carrying a
     `#fragment` whose path part is empty (the same file) or ends in `.md`: the fragment must equal
     the slug of a heading line (`#` to `######`, outside fences) of the target, where a heading's
     slug is its text after the hashes, stripped and lower-cased, with every character that is not
     a word character, a hyphen or a space removed and each space turned into a hyphen. A target
     file that does not exist is left to C04 and yields nothing here.
   C06 `doc_env_var_names`, README, INDEX and GUIDES except `docs/guides/environment.md`: every
     match of `REMEDY_[A-Z0-9_]+` not preceded by a word character. A match followed directly by
     `*`, ending in `_`, or followed by `.` and a letter is skipped; every other must be in
     `env_vars`.
   C07 `doc_config_keys`, README, INDEX and GUIDES: every span that is a whole KEY NAME whose first
     segment is a KEY PREFIX and which is not in `command_ids` must be in `config_keys`.
   C08 `toml_fenced_block_keys`, GUIDES: inside each fence whose opening line is exactly three
     backticks and `toml`, a table line `[remedy]` sets the prefix to empty and `[remedy.a.b]` to
     `a.b`, any other table line suspends reading until the next `[remedy...]` line, and each line
     `name = value` read under a prefix names the key `name` or `a.b.name`, which must be in
     `config_keys`.
   C09 `docs_index_type_column`, INDEX, the Quick-Find Table's rows: each row's third cell,
     stripped, must equal the top folder of every link target in its second cell, where the folder
     `guides` is written `guide`; each mismatching link is a claim.
   C10 `doc_source_paths`, README and INDEX: every match of
     `(packages|apps|tests|scripts)/[A-Za-z0-9_./-]+\.(py|ts|tsx|sh|json|toml)` not preceded by a
     word character or `/` must be an existing file under the root.
   C11 `doc_dotted_command_ids`, README, INDEX and GUIDES: every span that is a whole KEY NAME of
     exactly two segments whose first segment is a group id in `groups` and NOT a KEY PREFIX must
     be in `command_ids`.
   C12 `catalog_text_config_keys`, the catalog's texts: every KEY NAME in each `catalog_texts` text,
     not preceded by a word character or `.`, whose first segment is a KEY PREFIX and which is not
     in `command_ids`, must be in `config_keys`; the claim names the text's label.
S3 TIER 2 in `packages/orchestration/self_use_generator.py`:
   `_DOC_PROVENANCE = "generated (self-use-generator tier 2, doc staleness, {key})"`, a
   `_DOC_PROVENANCE_RE` reading the key back, `_targeted_doc_keys(queue_path)`, and
   `default_docs_root()` answering the repository root, as `default_order_path()` does. The tier
   calls `doc_staleness.run_staleness_checks(default_docs_root())` through the imported module (a
   top-level `from packages.orchestration import doc_staleness`), turns an `OSError` into
   `SelfUseGenerationError`, takes the first claim whose key no entry, consumed or not, targets,
   refuses with `SelfUseGenerationError` a claim or truth holding a line break, and otherwise
   answers an entry with the next `SU-NNN` id, title `Fix stale documentation: CHECK_ID in
   DOCUMENT`, `why` the claim, empty `consumed_by`, the provenance with the key, and the job text
   below, whose lines are shown indented by six spaces that are NOT part of it, in which CHECK_ID,
   DOCUMENT, CLAIM and TRUTH stand for the claim's four fields and every other character, backticks
   included, is literal; the text ends with one newline after its last line:
      # Job: Fix stale documentation: CHECK_ID in DOCUMENT

      ## Task 1
      The documentation-staleness check `CHECK_ID` found a claim in `DOCUMENT` that the shipped code contradicts.

      Claim: CLAIM
      Shipped truth: TRUTH

      Edit `DOCUMENT` so that it matches the shipped truth. Do not change code to match the document, and do not edit any file under `.agent/`.

      Acceptance:
      - The staleness check `CHECK_ID` no longer reports this claim for `DOCUMENT`.
      - No file under `.agent/` is changed by this task.
S4 THE DOCSTRING. The module docstring's opening paragraph and its item 2 are rewritten to describe
   all three sources as built (DECISION F289 D1 and D2), naming `doc_staleness.py`; item 3, items 0
   and 1 and every other paragraph stay. The tier order is unchanged.
S5 THE GUARDS. `packages/orchestration/doc_staleness.py` is imported at the top of
   `self_use_generator.py`, so `tests/test_no_orphan_modules.py` needs no entry, and the generator
   is not reachable from the six entry points `tests/orchestration/test_import_reachability.py`
   walks, so its allowlist is NOT expected to change; if that test goes red, stop under
   constraint 4. No docstring or comment in the new module may carry a `remedy <group> <sub>`
   line naming a command that does not ship (`tests/cli/test_advertised_commands.py` sweeps
   `apps/` and `packages/`), nor the substring `promot`.
S6 THE REAL TREE. At C4, run `run_staleness_checks()` over the repository and report every claim
   it answers. The reviewer measured two stale claims on the shipped tree, which D2 names: C01's
   missing Quick-Find link to `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`, and
   C02's undocumented `config show`. Any further claim is either a real staleness, which you
   report and leave, or a defect of your check, which you fix before C4 and declare. Do NOT edit
   any document to clear a claim: they are the self-use track's work (D2).

THE TESTS
A NEW FILE at `tests/orchestration/test_doc_staleness.py`, every test over a root under
`tmp_path` and a `ShippedTruth` built by the test, except where named: for EACH of the twelve
checks a STALE fixture that yields exactly the expected claims, with their four fields asserted,
and a FRESH fixture that yields none and that carries that check's exemptions — a fenced example of
the stale shape, and for C04 and C05 an `https://` link, for C03 a `remedy <group> <sub>`
placeholder, for C06 `REMEDY_OLLAMA_*` and `REMEDY_UI_REBUILD_SPEC.md`, for C07 and C11 a file name
like `remedy.toml` and a span of the other check's kind, for C12 a word like `e.g.`; `CHECKS` holds
at least ten checks with unique ids and non-empty text fields; `run_staleness_checks` orders claims
by catalog order; an absent document yields nothing; and, on the REAL repository and
`ShippedTruth.live()`, the call does not raise, every claim's document exists, and the live truth
holds the command id `config.list`, the key `data_dir` and the variable `REMEDY_DATA_DIR` — never
an assertion pinning the real tree's stale claims, which a repair would break.
In `tests/orchestration/test_self_use_generator.py`: the autouse `_no_standing_order` also
monkeypatches `run_staleness_checks` on `packages.orchestration.doc_staleness` to answer `()`; and
a new class covering at least: one stubbed claim on an empty ledger answers the Tier 2 item with
its id, title, provenance, `why` and a job text holding the claim, the truth and both acceptance
bullets, which parses as a single-task job (use `isolate_data_root`); of two claims the first,
then after appending it the second, and a consumed entry still withdraws a key; an eligible ledger
finding wins over Tier 2; Tier 2 wins over a stubbed actionable Tier 3 warning; a claim holding a
line break raises; an `OSError` from the checks becomes `SelfUseGenerationError`; and the REAL
chain with no stub: `default_docs_root` monkeypatched to a `tmp_path` root whose `docs/README.md`
omits a guide from its Quick-Find Table answers a Tier 2 item from C01.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f289-r2-block.md` := this block, `.agent/authored/f289-r2-plan.md` := plan.md,
  and `.agent/authored/f289-r2-records.diff` := records.diff, by `shutil.copyfile`.
  Subject: `F289 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 113. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F289 R2 C2: book round 1 and R-1073's resolution, record D2`
  Expected by `git show --numstat` (insertions and deletions): 54/0 decisions.md, 3/1 live_review.md, 8/10 plan.md, 1/0 prose_slips.md.

C3 — THE CATALOG: `packages/orchestration/doc_staleness.py` (`git add`ed).
  Subject: `F289 R2 C3: add the documentation-staleness catalog of twelve checks`

C4 — TIER 2: `packages/orchestration/self_use_generator.py`.
  Subject: `F289 R2 C4: render the first stale documentation claim as the generator's Tier 2`

C5 — THE TESTS AND THE MUTATION TOOL: the two test files and your mutation tool (G5) saved as
  `.agent/authored/f289-r2-mutations.py`.
  Subject: `F289 R2 C5: test the staleness catalog and Tier 2, and add the mutation tool`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F289 R2 C6: rewrite handoff for round 2`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C5a and C5b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f289-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/doc_staleness.py`, `packages/orchestration/self_use_generator.py`,
   `tests/orchestration/test_doc_staleness.py`, `tests/orchestration/test_self_use_generator.py`,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 8163cf8b` at the
   branch tip after C6. Do NOT touch `README.md`, anything under `docs/`, `apps/`,
   `packages/orchestration/config.py`, `packages/orchestration/self_use_queue.py`,
   `packages/orchestration/self_use_runner.py`, `scripts/self_use_queue.json`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/candidates.md` or
   `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F289 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table. Then compare each `.agent/authored/f289-r2-*` copy byte for byte with its
 source (the block copy against `.remedy-wt/f289-r2/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2215932 | 1c39a7a751de2eb7d2f80d6df1108027679342994848892c88bc76bc7b2f4da2 |
 | .agent/live_review.md | 320788 | 40c6a6dcdbfa039987df7939972355a3fdffa7b774c7cb73961ab1c979de7301 |
 | .agent/prose_slips.md | 370558 | be68c4cbba538c47f46e0c5182bacafa2f7dd1399d262eb04ef0028f9fbfa78a |
 | .agent/plan.md | 1047 | 05a0050cbcef3db2483c4a6fd4505b74cb24419c7d78cb6134462fbf0bcbe627 |
 Also: the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's TEXT at `8163cf8b` and at C2 (the reviewer read `R-1073` alone, then empty);
 at C2 the ledger holds no line starting `Landed: R-1073` and its last line begins
 `Gate: F289 R1 — `.

G3 THE CODE — `python3 -m ruff check packages/orchestration/doc_staleness.py
 packages/orchestration/self_use_generator.py tests/orchestration/test_doc_staleness.py
 tests/orchestration/test_self_use_generator.py` at C5; a python `ast` reading at C5 of every
 module `doc_staleness.py` imports (each `Import` and `ImportFrom` node, at any depth), which must
 name neither `subprocess` nor `socket` nor `urllib`; and S6's list of claims on the real tree,
 reported whole with each claim's four fields.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/cli/test_worker_facade_cmd.py tests/cli/test_advertised_commands.py tests/test_command_catalog.py tests/orchestration/test_env_registry.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/test_subprocess_timeouts.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file, serially, inside its authoring
 tree carrying the round's records, and read `794 passed, 1 skipped` at real exit code 0; the skip
 is the D12 quarantine. Report every `SKIPPED` line, the nodes the round adds (`--collect-only -q`
 on the new file and on `tests/orchestration/test_self_use_generator.py` at `8163cf8b` and at C5),
 and account for any other difference. Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f289-r2-mutations.py` takes a worktree path, and for
 each mutation below edits the named module INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_doc_staleness.py` and `tests/orchestration/test_self_use_generator.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: its label, the exit code, the failed count and the failing node
 ids. It runs an unmutated control first and last and ends with `restored byte-identical: True`
 per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 C01 reads only the Guides section;
  m2 C02 ignores a subcommand that ships and is not documented;
  m3 C03 accepts a second word that is not a group;
  m4 C04 resolves a link against the root instead of the guide's folder;
  m5 C05 keeps punctuation in a heading's slug;
  m6 C06 no longer skips a match followed by `*`;
  m7 C07 reads a span whose first segment is not a key prefix;
  m8 C08 drops the table prefix and checks the bare name;
  m9 C09 writes the folder `guides` as `guides`;
  m10 C10 accepts a path without checking that it exists;
  m11 C11 reads a span whose first segment is a key prefix;
  m12 C12 reads only the catalog's descriptions and no `ArgDef.help`;
  m13 fences are no longer skipped by C04;
  m14 Tier 2 ignores the keys the queue already targets;
  m15 `generate_self_use_item` tries Tier 3 before Tier 2;
  m16 Tier 2 accepts a claim holding a line break;
  m17 Tier 2 writes the truth on the `Claim:` line and the claim on the `Shipped truth:` line.
 Run it: `git worktree add --detach .remedy-wt/f289-r2-mut <C5>`, then
 `python3 -B .agent/authored/f289-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f289-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a mutation
 that stays green is reported as green, never papered over, and you then add the test that catches
 it in C5 before C6 and re-run the tool. Then `git worktree remove --force
 .remedy-wt/f289-r2-mut`, `git worktree prune`, and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline
 -n 8`; `git worktree list`, which must show the primary checkout and the worktrees constraint 6
 names, and nothing else; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected (none is expected for C3 to C5), every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Your Session section reads SESSION 1 of feature
F289, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T003 — three consecutive generator calls on an empty ledger produce three distinct
items, and one runs to completion under the test provider inside the default cost cap. State the
open-findings count, 0, and the operator-questions count, 0.
