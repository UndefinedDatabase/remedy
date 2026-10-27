# Context — operator amendment amend1027-green-builds

## Active Branch
`feature/amend1027-green-builds`, from `main` at `e8ca3bd5c` (no open pull request).

## Scope
Parts A to F of the operator's order of 2026-10-27: builder test permissions and environment,
honest test counting, claude-cli call timeouts, one slug per project, the evidence route and
contract 1.31, and two real green orders as F319's evidence.

## Do not touch
The non-human content policy; `dangerous-skip` stays opt-in only.

## Active assumptions
- universe-chat's tests are green outside the sandbox (2073 of 2073 on 2026-10-27) and red in a
  job worktree or the sandbox only because they cannot find universe-kit.
- The project edition `~/Repos/universe/remedy` has no CHANGELOG yet; F2's builder creates it.
- Job evidence under `.data` is read with `remedy job show` and `remedy run show`.

## Constraints
- At most 500 insertions per commit; no leading-slash tokens in commit subjects.
- One full pytest run at the end, then review and repair until green.
