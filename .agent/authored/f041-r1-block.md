STEP F041 R1 — CLAIM F041 AND LAND T001's PIPELINE: the README rendered and sanitized on the server, the attack corpus, the artifact roots and the artifacts route

GOAL
Pull request 294 is merged; `main` is at `45c584e6e` and F041 Artifact preview is the first
unchecked STATUS line. Cut F041's branch, claim it, re-head the live review record, book F286's
round 4 verdict and record DECISION F041 D1. Then land T001's pipeline against the reviewer's
tests: `packages/orchestration/artifact_markdown.py` (a markdown subset rendered with every source
character escaped, then an allowlist sanitizer), `packages/orchestration/artifact_preview.py`
(the derived roots, the path gate, the view) and the `artifacts` endpoint of the UI server.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the allowlist lines travel as payloads and are the acceptance, and you
write the production code against them and against S1 to S6 below. You never edit a payload
test; if one looks wrong to you, STOP and report it. Read DECISION F041 D1 in the claim diff
before you write code, and read whole, before you edit them:
`packages/orchestration/ui_server.py` around `_build_tour_json` and the `handlers` dict of
`do_GET`, `packages/orchestration/data_paths.py` (`data_class_dir`, `job_evidence_dir`) and
`packages/orchestration/staging_workspace.py` (`STAGING_DATA_CLASS`, `staging_dir_name`).

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f041-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f041-r1-dry/`, `.remedy-wt/f041-r1-sim/`, `.remedy-wt/f041-r1-scratch/`,
  `.remedy-wt/f041-r1-proto/`     The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f041-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `45c584e6e`. Report all three. Then
   `git checkout -b feature/f041-artifact-preview` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 130 | 14415 | b9cb95cc97e6a62fe8a19f216d7e1cd22203911c7826dc0e155005166424bf29 |
| allowlist.diff | 13 | 661 | 65dcef5d0168034618271f631980bb7cc8d5767bda32b94c27c0de1db5f70e1b |
| corpus.diff | 296 | 13346 | 38099b22ba532a83019c62f2e0ce7ae8eb40cb8097b4d973dbf5a67eb2e7f49d |
| roots.diff | 279 | 11901 | 09e19be22f00c663ac87fc2ba9f77386c39ccb4fa72900c04df7eef78c2bf11f |
| plan.md | 31 | 1049 | b08b0a8e7926c31e3c7cbb9a76030ccc748772ec41b5e5ca7e2696a79396fba8 |
| context.md | 33 | 1356 | 2874123d5d1ab88f090fdd659180564fc79d962997f99704ca897eddc5fa4488 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. Every
`.diff` goes on with `git apply`; the reviewer generated them with `git diff HEAD` from a tree at
`45c584e6e`. `claim.diff` edits `.agent/live_review.md` (the re-head, which replaces everything
above the `## Findings` heading line, then F286's round 4 gate entry appended),
`.agent/decisions.md` (DECISION F041 D1 appended) and `docs/roadmap/STATUS.md` (F041's line `[ ]`
to `[~]`). `allowlist.diff` adds the round's new modules to
`tests/orchestration/import_reachability_allowlist.txt`. `corpus.diff` adds the NEW FILE at
`tests/orchestration/test_artifact_markdown.py`. `roots.diff` adds the NEW FILE at
`tests/orchestration/test_artifact_preview.py` and the NEW FILE at
`tests/ui_server/test_artifacts_route.py`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `packages/orchestration/artifact_markdown.py`, NEW, standard library only, with a module
   docstring naming F041 T001 and DECISION F041 D1. Public names: `MARKDOWN_MAX_BYTES = 262_144`;
   `ALLOWED_TAGS` (a, blockquote, br, code, em, h1 to h6, hr, img, li, ol, p, pre, strong, ul);
   `ALLOWED_ATTRIBUTES` (`a`: href, title; `img`: alt, src, title); `VOID_TAGS` (br, hr, img);
   `DROPPED_WITH_CONTENT` (embed, iframe, math, noscript, object, script, style, svg, template,
   textarea, title, xmp); `LINK_SCHEMES` (http, https, mailto);
   `LINK_REL = "noopener noreferrer nofollow"`; and the functions of S2 to S4.
S2 `safe_url(value: str, *, image: bool) -> str | None`. It tests a probe: the value with every
   character from U+0000 to U+0020 and U+007F removed, lowercased. An empty probe, one starting
   `//`, or one holding a backslash gives None. A scheme is present when a colon occurs before the
   first `/`, `?` or `#` of the probe; then an image gives None, and a link gives None unless the
   text before that colon is in `LINK_SCHEMES`. Otherwise it returns `value.strip()`.
S3 `sanitize_fragment(markup: str) -> str`, an `html.parser.HTMLParser` with
   `convert_charrefs=True` rebuilding the markup. Inside a `DROPPED_WITH_CONTENT` element every
   event is dropped until that element's own end tag, counting nested elements of the same name.
   A start tag outside `ALLOWED_TAGS` is dropped and its text kept. Kept attributes are those in
   `ALLOWED_ATTRIBUTES` with a value, in source order; `href` and `src` pass `safe_url` (image
   True for `img`) and are dropped on None. An `img` left without `src` is replaced by its `alt`
   text, escaped. Every `a` gains `rel` = `LINK_REL` as its LAST attribute. Attribute values are
   written `name="html.escape(value, quote=True)"`; text is written `html.escape(data,
   quote=False)`. A self-closing non-void tag is opened and closed. An end tag closes the open
   tags down to its own and is dropped when that tag is not open. Comments, declarations and
   processing instructions are dropped. Tags still open at the end are closed in reverse order.
S4 `RenderedMarkdown`, a frozen dataclass of `html: str`, `truncated: bool`, `source_bytes: int`,
   and `render_markdown(text: str) -> RenderedMarkdown`. A source over `MARKDOWN_MAX_BYTES`
   UTF-8 bytes is cut to that many bytes, decoded ignoring a split character, then cut before its
   last newline when it has one; `source_bytes` is always the whole source's byte length. Blocks,
   read over `splitlines()` with each line stripped for matching, in this order of tests: a
   fence (a line starting three backticks or three tildes) runs to the next line starting the
   same marker or the end, as `<pre><code>` of its lines joined with newlines and escaped; a
   blank line ends a paragraph; an ATX heading `^(#{1,6})\s+(.*?)\s*#*$`; a rule
   `^([-*_])(\s*\1){2,}$` as `<hr>`; consecutive lines starting `>` as one
   `<blockquote><p>…</p></blockquote>` of their text after the marker, joined with spaces; a run
   of list items `^([-*+]|\d+\.)\s+(.*)$` of one kind as `<ul>` or `<ol>` of `<li>`; otherwise the
   line joins the paragraph, whose lines are stripped and joined with spaces. Inline, scanning left
   to right: a backtick up to the next backtick is `<code>` of the escaped text between; `![` or
   `[` followed by `label](url)` or `label](url "title")`, where the url holds no space and no
   `)`, is an `img` (src, alt, then title) or an `a` (href, then title) whose label is rendered
   inline; `**`, `__`, `*`, `_`, tried in that order, up to the next same marker with text between,
   are `strong`, `strong`, `em`, `em`; any other character is escaped. The whole rendered string
   then passes `sanitize_fragment`.
S5 `packages/orchestration/artifact_preview.py`, NEW, with a module docstring naming F041 T001
   and DECISION F041 D1. `ROOT_WORKSPACE = "workspace"`, `ROOT_EVIDENCE = "evidence"`,
   `ARTIFACT_ROOTS = (ROOT_WORKSPACE, ROOT_EVIDENCE)`, `README_NAME = "README.md"`,
   `CAPTURES_DIRNAME = "captures"`, `IMAGE_CONTENT_TYPES` (`.gif`, `.jpeg`, `.jpg`, `.png`,
   `.webp` to their `image/…` types), `MAX_LISTED_IMAGES = 200`.
   `artifact_root(job_id, root, data_root=None) -> Path | None`: for `workspace`,
   `data_class_dir(STAGING_DATA_CLASS, data_root) / staging_dir_name(job_id)`; for `evidence`,
   `job_evidence_dir(job_id, data_root)`; None for any other name or a directory that is absent.
   `resolve_artifact_path(base, relative) -> Path | None`: None for an empty name, a backslash, a
   NUL, an absolute `PurePosixPath` or one with a `..` part; else `(base.resolve() /
   relative).resolve()` when it `is_relative_to(base.resolve())` and `is_file()`, else None.
   `artifacts_view(job_id, data_root=None) -> dict` with exactly the keys `readme`, `images`,
   `error`: the README from the first root of `ARTIFACT_ROOTS` whose `README.md` resolves, read as
   bytes and decoded UTF-8 with `errors="replace"`, as `root`, `path`, `html`, `truncated`,
   `source_bytes`; an `OSError` reading it gives `readme` None and `error`
   "the README could not be read". `images`: the entries of `captures/` under the evidence root,
   by name, whose lowercased suffix is in `IMAGE_CONTENT_TYPES` and which resolve through
   `resolve_artifact_path`, as `root`, `path`, `bytes`, `content_type`, at most
   `MAX_LISTED_IMAGES`.
S6 `packages/orchestration/ui_server.py`: `_build_artifacts_json(job)` directly after
   `_build_tour_json`, importing `artifacts_view` inside its body and answering
   `artifacts_view(str(job.job_id))`, with a docstring naming F041 T001 and DECISION F041 D1; and
   `"artifacts": _build_artifacts_json,` directly after the `"tour"` entry of `do_GET`'s
   `handlers` dict. Nothing else in the file changes.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f041-r1-block.md` := this block, and `.agent/authored/f041-r1-plan.md` and
  `.agent/authored/f041-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F041 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 64. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim, allowlist and roots diffs
  `.agent/authored/f041-r1-claim.diff` := claim.diff, `.agent/authored/f041-r1-allowlist.diff` :=
  allowlist.diff and `.agent/authored/f041-r1-roots.diff` := roots.diff.
  Subject: `F041 R1 C1b: copy round 1 claim, allowlist and roots diffs into .agent/authored/`
  Expected insertions: 422.

C1c — copy the corpus diff
  `.agent/authored/f041-r1-corpus.diff` := corpus.diff.
  Subject: `F041 R1 C1c: copy round 1 corpus diff into .agent/authored/`
  Expected insertions: 296.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F041 R1 C2: claim F041, re-head the live review record, book F286 R4, record D1`
  Expected by `git show --numstat` (insertions and deletions): 11/9 .agent/context.md, 51/0 .agent/decisions.md, 21/20 .agent/live_review.md, 17/9 .agent/plan.md, 1/1 docs/roadmap/STATUS.md.

C3 — THE CODE: S1 to S6 and `git apply` allowlist.diff, in one commit, so the two new modules
  are imported and listed at the same commit and no guard is red between commits. If this
  commit would reach 500 insertions, stop and report rather than split it.
  Subject: `F041 R1 C3: render a README to a sanitized fragment and serve the artifacts view`

C4 — THE CORPUS: `git apply` corpus.diff.
  Subject: `F041 R1 C4: add the reviewer's attack corpus for the markdown pipeline`

C5 — THE ROOTS AND THE ROUTE TESTS: `git apply` roots.diff.
  Subject: `F041 R1 C5: add the reviewer's traversal fixtures and artifacts route tests`

C6 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f041-r1-mutations.py`.
  Subject: `F041 R1 C6: add the round 1 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F041 R1 C7: rewrite handoff for round 1`
  Then `git push -u origin feature/f041-artifact-preview`. Do NOT create a pull request: the
  branch opens one at F041's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f041-r1-*` copies and tool, the
   three paths claim.diff edits, the paths allowlist.diff, corpus.diff and roots.diff edit,
   `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/artifact_markdown.py`,
   `packages/orchestration/artifact_preview.py`, `packages/orchestration/ui_server.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 45c584e6e` at the
   branch tip after C7. Do NOT touch `apps/ui/`, `pyproject.toml`, `constraints.txt`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `README.md`.
4. Every test corpus.diff and roots.diff carry passes against your code unedited, at C4 and C5. A test the payload carries is
   never edited to pass; if your code cannot meet one, STOP and report the test and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F041's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f041-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f041-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1356 | 2874123d5d1ab88f090fdd659180564fc79d962997f99704ca897eddc5fa4488 |
 | .agent/decisions.md | C2 | 2452366 | 3256276551325168486cb4b5520ff4451f901caf0f06a0a587264826c9b123a7 |
 | .agent/live_review.md | C2 | 294502 | aec00d33187525c2ed8c0e8a04a8263bf06c456f09915331f4915d3b5afaaa13 |
 | .agent/plan.md | C2 | 1049 | b08b0a8e7926c31e3c7cbb9a76030ccc748772ec41b5e5ca7e2696a79396fba8 |
 | docs/roadmap/STATUS.md | C2 | 57908 | 490f45710241f6f5ac89d68130715849d5047fbb7d448609e6dc94705f56f9d4 |
 | tests/orchestration/test_artifact_markdown.py | C4 | 12817 | 4c21c64685c1c8b030eea27f91ecab7e779c0c205a013e0bd1ace9b2c092a3d4 |
 | tests/orchestration/test_artifact_preview.py | C5 | 6254 | e92681c659bdf80948465b6674fe8d7bc66a436a9e915fc16bbdd86f9943dbdb |
 | tests/ui_server/test_artifacts_route.py | C5 | 4923 | 8319c500a37d3d08e95dd91486879f6bda262e9d7174d66429f3adebfcb2f250 |
 | tests/orchestration/import_reachability_allowlist.txt | C3 | 11019 | fc8aa99f5a24c93d1d9ef5ad3f3cbbd96a840a9adb26261408cf4971ad99c777 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>`, at
 `45c584e6e` and at C2 (the reviewer read `[]` at both); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F286 R4 — `; F041's STATUS line at C2 read back in full, which must read
 `- [~] F041 — Artifact preview`; and `git diff --name-only <C1c> <C2>`, which must name exactly
 the C2 paths of the table above.

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/artifact_markdown.py
 packages/orchestration/artifact_preview.py packages/orchestration/ui_server.py
 tests/orchestration/test_artifact_markdown.py tests/orchestration/test_artifact_preview.py
 tests/ui_server/test_artifacts_route.py .agent/authored/f041-r1-mutations.py` at C6, with its
 real exit code. Report `git show --numstat <C3>` and the diff of
 `packages/orchestration/ui_server.py` at C3, whole. Then, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_artifact_markdown.py tests/orchestration/test_artifact_preview.py tests/ui_server/test_artifacts_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_tour_route.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_development_artifact_boundary.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C2 and the
 tests of this round and the reviewer's own version of S1 to S6 but no
 `.agent/authored/f041-r1-*` copy, and read `661 passed, 1 skipped` at real exit code 0. Your count may
 differ from it by what the round's copies hold, so report the node counts of the three new test
 files by `--collect-only -q` (the reviewer's read 106, 20 and 5). Report every `SKIPPED` line
 the `-rs` summary prints; the reviewer's run printed exactly one, `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12 quarantine. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f041-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs
 `python3 -B -m pytest -q -p no:cacheprovider <the test file named>` with the worktree as the
 working directory and the worktree's root first on `PYTHONPATH` (set through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control of each test file the mutations
 name first and last, reports `restored byte-identical: True` after each restore, and ends with a
 final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `script` is removed from `DROPPED_WITH_CONTENT` (test_artifact_markdown.py);
  m2 `safe_url` no longer removes control characters and spaces from its probe (same file);
  m3 `safe_url` lets an image keep an allowed link scheme (same file);
  m4 a link no longer gains `rel` (same file);
  m5 the inline scanner writes a plain character without escaping it (same file);
  m6 `resolve_artifact_path` no longer checks `is_relative_to` (test_artifact_preview.py);
  m7 `resolve_artifact_path` no longer refuses a `..` part (same file);
  m8 `ARTIFACT_ROOTS` puts the evidence root first (same file);
  m9 the `"artifacts"` entry is removed from the `handlers` dict (test_artifacts_route.py).
 Run it: `git worktree add --detach .remedy-wt/f041-r1-mut <C6>`, then
 `python3 -B .agent/authored/f041-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r1-mut`
 and report its whole output. EVERY mutation must exit non-zero; a mutation that stays green is
 reported as green, never papered over, and you then STOP and report it, because the tests are
 the reviewer's. Then `git worktree remove --force .remedy-wt/f041-r1-mut`, `git worktree prune`,
 and report `git worktree list | wc -l`.

G5 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C7, C6, C5, C4, C3, C2, C1c, C1b, C1a and
 `45c584e6e` in that order; `git worktree list | wc -l`, which must equal your step 4 reading;
 the push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3, C4, C5 and C6 — report
what you measure), every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F041, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then round 2 (the file route and the start of T002). State the open-findings count, 0,
and the operator-questions count, 1.
