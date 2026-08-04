# sampleproj

A small records pipeline: read `name = value` lines, import them into a
directory, and report on what is there. It exists to give the F075 gauntlet a
real project to work on — small enough to read in one sitting, real enough that
a Definition of Done has something to check.

## Commands

    python3 -m sampleproj.cli import <source|-> <target-dir>
    python3 -m sampleproj.cli report <target-dir>

`import` prints progress to stdout; every error goes to stderr with an
`error: ` prefix and exit code 2.

## Configuration

Three settings, each an integer: `max_records`, `retry_attempts`,
`report_width`.

Values resolve in this order, first match wins:

1. an explicit argument passed to `config.resolve(...)`
2. the setting's environment variable
3. a `sampleproj.conf` file (`key = value` lines; `#` comments ignored)
4. the built-in default in `config.DEFAULTS`

## Environment variables

| Setting | Variable |
| --- | --- |
| `max_records` | `SAMPLEPROJ_MAX_RECORDS` |
| `retry_attempts` | `SAMPLEPROJ_RETRY_ATTEMPTS` |
| `report_width` | `SAMPLEPROJ_REPORT_WIDTH` |

## Retries

`retry.backoff_for(attempt)` doubles from one second and is capped at
`BACKOFF_CAP_SECONDS`.

## Tests

    python3 -m pytest tests -q
