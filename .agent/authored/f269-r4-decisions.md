
## DECISION F269 D5 (2026-09-18, reviewer, round 4) — the three hygiene criteria, the check that measures them, and the reviewer's rule
CONTEXT: T2_F269.md Design puts three blocking hygiene criteria in every template and gives the
reviewer role the matching rule, and DECISION F269 D1 (5) held them back until a check measures
them. Measured at `fc9aae2b`: F061's check kinds are fixed and this feature may not add one, and
`custom_cmd` runs an argv whose first word is on `test_runner._EXECUTION_SAFE_EXECUTABLES`, which
holds `python3` and not `git`; a `run_job` worktree has the base commit as `HEAD` and the builder's
changes uncommitted, so `git` inside it lists what the job added and changed; the orchestrator's
job workspace is not a git tree; `FakeProvider`'s reviewer never reads its prompt; the reviewer's
system text in `packages/orchestration/pingpong_loop.py` is pinned byte for byte by
`tests/orchestration/test_reviewer_prompt_golden.py`.
CHOSEN: (1) THE CHECK. A new standard-library module `packages/orchestration/contract_hygiene.py`
holds three pure rules over a root and a list of files, and a command line
`python3 -m packages.orchestration.contract_hygiene <rule>` that finds, with `git` run from the
current directory, the files added since `HEAD` (untracked and not ignored, plus added in the index)
and the files changed since `HEAD` with their added lines, applies one rule, prints one line per
finding naming the path, and exits 0 on none, 1 on findings, and 2 when it cannot measure (not a
git work tree, or `git` failing) — so a tree it cannot read is a red check, never a met criterion.
CODE FILES are `.py`, `.js`, `.jsx`, `.ts` and `.tsx`. (2) `unreferenced`: an added code file is
reported unless another file of the tree — tracked or added, not ignored, read as text up to one
megabyte — contains the file's stem where neither neighbouring character is a word character, or
the file is exempt: named `__init__.py`, `__main__.py`, `conftest.py` or `setup.py`, a test file
(its name starts with `test_` or ends with `_test.py`, or it holds `.test.` or `.spec.`, or a
directory on its path is named `tests` or `test`). (3) `replaced`: an added file is reported when
removing one marker from its name — a `_new`, `_old`, `_copy`, `_backup`, `_bak` or `_v<digits>`
suffix of the stem, a `new_` or `old_` prefix, or a trailing `.bak` or `.orig` — gives the path of
a file that still exists beside it; this measures the file-level form of the criterion, and the
reviewer's prompt rule covers replaced code inside a file. (4) `stubs`: in added code files, every
line, and in changed code files, every added line, holding `TODO`, `FIXME` or `XXX` as a word is
reported; in Python files that parse, every function whose definition line is added and whose body,
after an optional docstring, is only `pass`, `...` or `raise NotImplementedError` is reported,
unless it is decorated `abstractmethod` or `overload`. (5) THE TEMPLATES. Every template gains the
three criteria, blocking, each with a `check:` line of kind `custom_cmd` running its rule. (6) THE
REVIEWER'S RULE. The reviewer's system text gains one sentence: a change that adds a file nothing
references, or leaves replaced code beside its replacement, is rejected with the path named. The
round enforces the measurable half itself: after the reviewer answered, the `unreferenced` and
`replaced` rules run over the files the job has added so far (new against the job's base in a job
worktree, absent from the original repository in a staging copy); each finding is appended to the
reviewer's findings with the path in `file` and in the summary, and a `pass` verdict becomes
`needs_repair`, so the repair decision treats it as any reviewer finding.
ALTERNATIVES: a new F061 check kind, rejected because the feature file forbids touching F061's
kinds and runners; leaving the three criteria to F061's compiler, rejected because it would judge
them by the test suite, which does not measure them; enforcing the rule only through the prompt,
rejected because the fake reviewer cannot prove it and a real reviewer can miss it. REVERSE:
delete `contract_hygiene.py` and its tests, the three criteria from the templates, the sentence
and the round hook, restore the golden renders, and delete this paragraph.
