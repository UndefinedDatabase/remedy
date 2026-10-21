# Job certificate v1

> Built by F060 (DECISIONs F060 D1 to D4). A certificate lets a job that has ended prove itself to
> someone who was not there.

## What it is

A certificate is one small ZIP file made from a job that has ended. It holds the files that show
how the job ended, and a file named `manifest.json` that lists each of them with its SHA-256
fingerprint and its size and states what the job claims about itself. Anyone with Remedy installed
can check it on any machine, without the job's data folder and without the project's repository.

A certificate proves that its files are intact and agree with each other. It is not a signature:
it does not prove who made it. The manifest keeps a `signature` field for a later version, and in
version 1 that field is always empty.

## Making one

`remedy job certificate <job-id>` writes the certificate of a job whose state is blocked,
cancelled, completed, failed or stopped. A certificate of a failed or stopped run is as valid as
one of a completed run, and it says plainly how the run ended. A job that is still pending,
planned, running or paused is refused, and so is an id that names no job.

The certificate is written to `--out`, or, without it, to a file in the current folder named after
the job and the issue number. Remedy never overwrites a file: a path that already exists is
refused before anything is written. Each certificate of a job gets the next issue number, so a
certificate made after the job was resumed and ended again supersedes the earlier one.

`--max-bytes` sets the size budget, 8 MiB unless you give another. The report, the cost record,
the checks, the ownership record and the run manifest are always included. A diff or a run log is
included only while the budget allows; otherwise the manifest names it with its fingerprint, its
size and where to fetch it, and leaves it out of the ZIP.

## What a certificate holds

| Member | Class | Where it comes from |
|---|---|---|
| `report.md` | report | the job's final report, or the same report rendered in memory when the saved one is missing or describes an earlier state |
| `token/budget_actuals.json` | token_truth | the token and cost record of the job |
| `token/token_truth.json` | token_truth | the job's evidence export, when there is one |
| `verdicts/dod_result.json` | verdicts | the Definition of Done check result |
| `verdicts/final_verifier_report.json` | verdicts | the evidence export's final verifier report |
| `ownership/ownership.json` | ownership | the evidence export's record of who did what |
| `run_manifest/run_manifest_index.json`, `run_manifest/run_manifest.json` | run_manifest | the job's run manifest |
| `diff/result.diff` | diff | the job's result diff, for a job that ran in a worktree |
| `logs/<file>` | log | the job's run logs |

A member is present only when the job has its file; the report is always present.

## The claims

The manifest states six claims: how the run ended, the Definition of Done summary (how many checks
passed, of how many, and whether the result was released), the cost and the basis it was measured
on, the number of decisions the job raised, and the regression status of the final verifier. Each
claim except the number of decisions is computed from the bytes of the member that carries it, by
the same function when the certificate is made and when it is checked.

## Checking one

`remedy verify <bundle>` checks a certificate and prints a verdict. It exits 0 when the
certificate is intact and 1 when it is not. Its first line says how the run ended, so a sound
certificate of a failed run never reads as a success. It then checks, in this order:

1. that the file is a ZIP holding a `manifest.json` of version 1 with every key it must have;
2. that every member the manifest lists is in the ZIP with exactly its fingerprint and size, that
   nothing else is, and that the members fit the manifest's budget;
3. that every claim agrees with its member: the report names the claimed terminal state, and the
   cost, the Definition of Done summary and the regression status are what their members give.

Every problem names the member it concerns. A report or cost record that was changed together with
its fingerprint in the manifest still fails the third check. With `--json` the answer carries the
problems and the manifest instead of the verdict text.
