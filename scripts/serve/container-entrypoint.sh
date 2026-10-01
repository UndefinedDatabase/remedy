#!/usr/bin/env bash
# container-entrypoint.sh — runs the F200 serve supervisor as a container's main process.
#
# Run the container with an init process, e.g. `docker run --init ...`: a job
# run started by the supervisor spawns its own helper processes, and only an
# init process reaps the ones that outlive their parent.
#
# Requires REMEDY_DATA_DIR to be set; refuses with a plain message and exit 2
# otherwise, rather than guessing a data root inside a throwaway container
# filesystem. Creates that directory if it does not already exist.
#
# REMEDY_BIN overrides the `remedy` executable this script execs (default:
# `remedy`, resolved on PATH). Any arguments given to this script are passed
# after `serve start`, e.g.:
#   container-entrypoint.sh --json
set -eu

if [ -z "${REMEDY_DATA_DIR:-}" ]; then
  echo "container-entrypoint.sh: REMEDY_DATA_DIR must be set" >&2
  exit 2
fi

mkdir -p "${REMEDY_DATA_DIR}"

REMEDY_BIN="${REMEDY_BIN:-remedy}"

# exec replaces this shell with the supervisor, so it receives the container's
# stop signal directly instead of a shell forwarding (or failing to forward) it.
exec "${REMEDY_BIN}" serve start "$@"
