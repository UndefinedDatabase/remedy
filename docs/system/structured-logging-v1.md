# Structured logging v1: Remedy's operations log

> Status (F203, 2026-10-13): being built. The setup, its keys, the file, the wiring into every
> command, the mirror of the job timeline, the `print` lint and `remedy doctor logs` exist; the
> read on the public API and in the cockpit follow. DECISIONs F203 D1 to D4 in
> `.agent/decisions.md` hold the rules this page states; the feature is
> `docs/roadmap/features/T12_F203.md`.

## What it does

Every `remedy` command writes what it does to one operations log on this machine, so that what
happened during a night's run can be looked up in the morning. The log is operations data and
never evidence: no verdict, proof or closure reads it, and the job's own timeline and evidence
stay the record of what a job did.

## Where it is

The file is `<data root>/logs/remedy.log`. The folder is readable by the owner only (0700) and so
is every file in it (0600). The folder is made by the first line written, so a command that logs
nothing leaves the data root as it found it. When the file reaches `logging.max_bytes` it is
renamed to `remedy.log.1`, the older ones move up by one, and at most `logging.backup_count`
rotated files are kept. Remedy keeps nothing outside its data root.

## One line

With `logging.json` true, the default, every record is one JSON object on one line, with these
keys in this order: `ts` (UTC with milliseconds, for example `2026-10-13T08:05:09.042Z`),
`level`, `logger`, `message`, `job_id`, `task_id`, `run_id`, and `exception` when the record
carries one. An id the record does not know is `null`. With `logging.json` false, the line is
plain text: the time, the level, the logger, `job=`, `task=` and `run=` with `-` for an unknown
id, then the message. Every line passes through the same redaction as evidence before it is
written, so a secret that reaches a message or a traceback is written as `[REDACTED]`.

## The ids

Every event the job timeline records is also written to this log as one INFO line on the logger
`packages.orchestration.run_log`, carrying the event's job id, its task id and, as `run_id`, the
id of the task's execution, which is the ping-pong run id under `<data root>/runs/`. A job's
lines can therefore be found by its job id in the order they happened. Code that knows the ids
may bind them for everything it logs with `bind_log_context`; an id a record already carries
wins over a bound one.

## The terminal

What a person sees in the terminal does not change. Warnings and errors that Remedy's modules log
are printed on the error stream as their bare message, exactly as before this log existed. A
command that ends on an unexpected error writes that error with its traceback to the log only;
the terminal shows the same one-line message and the crash report's location as before. A line
that cannot be written, for example because the data root cannot be written to, is dropped
silently and never breaks a command.

## Reading one job's lines

`remedy doctor logs <job>` prints the lines of one job, oldest first, across the current file and
every rotated one: the time, the level, the logger, `task=` and `run=` with `-` for an unknown
id, then the message, and an exception, when a line carries one, below it indented by four
spaces. The job id may be given by its first characters, as everywhere else. `--run <run id>`
keeps only the lines of one run of a task. `--json` answers the same lines as JSON objects, with
the names of the files read and the number of lines skipped. A line that is not JSON, such as a
line written while `logging.json` was false, is skipped and counted. A job with no line gets an
answer that says so, and the command still exits 0; it reads the log and changes nothing.

## Settings

| Key | Variable | Default | Meaning |
|---|---|---|---|
| `logging.level` | `REMEDY_LOG_LEVEL` | `INFO` | The lowest level written to the file; an unknown name falls back to `INFO` and writes one warning naming it |
| `logging.json` | `REMEDY_LOG_JSON` | true | JSON lines, or plain text lines when false |
| `logging.max_bytes` | `REMEDY_LOG_MAX_BYTES` | 10000000 | The size at which the file is rotated |
| `logging.backup_count` | `REMEDY_LOG_BACKUP_COUNT` | 5 | How many rotated files are kept |

## What it deliberately does not do

Remedy deliberately does not send its log anywhere and does not use it as evidence. It does not
use structlog: the standard library's `logging` does the job without a new dependency.
OpenTelemetry export is F197's and metrics are F198's.
