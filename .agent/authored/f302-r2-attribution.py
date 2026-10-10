"""F302 T002: what a claude-cli worker's first call reads before it does any work, source by source.

DECISION F302 D1 (2). One fixed task whose answer needs no tool, started through Remedy's own
provider path (`build_claude_cli_args`, `_guarded_cli_run`, `parse_cli_envelope`) exactly as a
builder call is started, with the builder's write mode and model, once with everything loaded and
once per source switched off, in a scratch repository and in a worktree of Remedy, with a repeat of
each baseline for the noise. At most twenty provider calls: the plan below holds exactly that many,
the counter refuses a twenty-first, and a second `run` refuses to start once the readings exist.

    python3 -B f302-r2-attribution.py run --out <dir> --work <dir> --remedy-rev <sha> [--claude <path>]
    python3 -B f302-r2-attribution.py render --out <dir>

`run` writes `f302_claude_help.txt` (the installed CLI's own `--version` and `--help`, which are not
provider calls) and `f302_attribution.jsonl` (one line per call, written as each call ends), then
`render` writes `f302_attribution.md` from the JSON lines alone. No cost in US dollars is kept
(DECISION amend1007b D7).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import statistics
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from packages.orchestration.claude_cli_command import build_claude_cli_args  # noqa: E402
from packages.orchestration.pingpong_provider import _guarded_cli_run, _stderr_tail  # noqa: E402
from packages.orchestration.token_actuals import parse_cli_envelope  # noqa: E402

MAX_CALLS = 20
TIMEOUT_SEC = 300
MODEL = "claude-sonnet-4-6"
WRITE_MODE = "allowed-tools"
PROMPT = "This is a measurement call. Answer with the one word READY and nothing else. Use no tool."
BUILDER_TOOLS = "Read,Edit,Write,MultiEdit,Glob,Grep"
LEAN = ["--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands",
        "--tools", BUILDER_TOOLS, "--exclude-dynamic-system-prompt-sections"]
CONFIGS = (
    ("baseline", []),
    ("no-mcp", ["--strict-mcp-config"]),
    ("no-settings", ["--setting-sources", ""]),
    ("no-skills", ["--disable-slash-commands"]),
    ("builder-tools", ["--tools", BUILDER_TOOLS]),
    ("no-dynamic", ["--exclude-dynamic-system-prompt-sections"]),
    ("safe-mode", ["--safe-mode"]),
    ("bare", ["--bare"]),
    ("lean", LEAN),
    ("baseline-repeat", []),
)
PLACES = ("scratch", "remedy")
PLAN = [(place, name, switches) for place in PLACES for name, switches in CONFIGS]
assert len(PLAN) <= MAX_CALLS
KINDS = ("input", "output", "cache_creation", "cache_read")


def _git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True, text=True)


def _places(work: pathlib.Path, rev: str) -> dict[str, pathlib.Path]:
    scratch, remedy = work / "scratch", work / "remedy"
    if work.exists():
        raise SystemExit(f"refusing: {work} exists; the places are made fresh")
    scratch.mkdir(parents=True)
    _git("-C", str(scratch), "init", "-q")
    (scratch / "README.md").write_text("A scratch repository for one measurement.\n")
    _git("-C", str(REPO), "worktree", "add", "--detach", str(remedy), rev)
    return {"scratch": scratch, "remedy": remedy}


def _remove_places(work: pathlib.Path) -> None:
    remedy = work / "remedy"
    if remedy.exists():
        _git("-C", str(REPO), "worktree", "remove", "--force", str(remedy))
    shutil.rmtree(work, ignore_errors=True)


def run(out: pathlib.Path, work: pathlib.Path, rev: str, claude: str) -> int:
    lines_path = out / "f302_attribution.jsonl"
    if lines_path.exists():
        raise SystemExit(f"refusing: {lines_path} exists; the readings are taken once")
    claude = claude or shutil.which("claude") or ""
    if not claude:
        raise SystemExit("refusing: no claude on PATH")
    help_parts = []
    for flag in ("--version", "--help"):
        proc = _guarded_cli_run([claude, flag], timeout_sec=30, cwd=str(REPO))
        help_parts.append(f"=== claude {flag} (exit {proc.returncode}) ===\n{proc.stdout}{proc.stderr}")
    (out / "f302_claude_help.txt").write_text("".join(p if p.endswith("\n") else p + "\n" for p in help_parts))
    env_names = sorted(k for k in os.environ if k.startswith(("CLAUDE", "ANTHROPIC")))
    places = _places(work, rev)
    calls = 0
    try:
        for seq, (place, name, switches) in enumerate(PLAN, 1):
            calls += 1
            if calls > MAX_CALLS:
                raise SystemExit("refusing: the call cap is reached")
            argv = build_claude_cli_args(claude, PROMPT, write_mode=WRITE_MODE, model=MODEL) + switches
            start = time.monotonic()
            row = {"seq": seq, "place": place, "config": name, "switches": switches,
                   "env_names": env_names}
            try:
                proc = _guarded_cli_run(argv, timeout_sec=TIMEOUT_SEC, cwd=str(places[place]))
            except subprocess.TimeoutExpired:
                row.update(exit_code=None, error="timeout")
            else:
                env = parse_cli_envelope(proc.stdout or "")
                u = env.usage_actuals
                row.update(
                    exit_code=proc.returncode, is_error=env.is_error, subtype=env.subtype,
                    result=(env.result_text or "")[:60],
                    error=_stderr_tail(proc.stderr or "") if proc.returncode else "",
                    input=u.input_tokens if u else None, output=u.output_tokens if u else None,
                    cache_creation=u.cache_creation if u else None,
                    cache_read=u.cache_read if u else None,
                    num_turns=u.num_turns if u else None,
                    cli_version=(u.cli_version if u else None),
                )
            row["elapsed_ms"] = int((time.monotonic() - start) * 1000)
            with lines_path.open("a") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            print(seq, place, name, row.get("exit_code"), *(row.get(k) for k in KINDS), flush=True)
    finally:
        _remove_places(work)
    print("calls made:", calls)
    return calls


def _context(r: dict) -> int | None:
    if any(not isinstance(r.get(k), int) for k in ("input", "cache_creation", "cache_read")):
        return None
    return r["input"] + r["cache_creation"] + r["cache_read"]


def _fmt(v) -> str:
    return f"{v:,}" if isinstance(v, int) else "—"


def render(out: pathlib.Path) -> None:
    rows = [json.loads(x) for x in (out / "f302_attribution.jsonl").read_text().splitlines()]
    w = []
    w.append("# F302 T002 — what a claude-cli worker's first call reads, source by source")
    w.append("")
    w.append("> Written by `.agent/authored/f302-r2-attribution.py render` from")
    w.append("> `.agent/f302_attribution.jsonl` alone; every figure below is computed, none typed.")
    w.append("")
    w.append(f"Provider calls made: {len(rows)}, of at most {MAX_CALLS} (DECISION F302 D1 (2); the")
    w.append("feature file allows 40). The task: \"" + PROMPT + "\", with the")
    w.append(f"builder's write mode `{WRITE_MODE}` and model `{MODEL}`, through `build_claude_cli_args` and")
    w.append("`_guarded_cli_run`, the path every job's builder call takes. Context is input plus cache")
    w.append("creation plus cache read: what the call's requests read, however much of it was cached.")
    w.append("A call of more than one turn read its context once per turn, so its row is marked.")
    versions = sorted({r.get("cli_version") or "not reported" for r in rows})
    w.append("Claude Code version: " + ", ".join(f"`{v}`" for v in versions) + ".")
    env_names = rows[0].get("env_names", []) if rows else []
    w.append("Environment variables named `CLAUDE*` or `ANTHROPIC*` in the run (names only): "
             + (", ".join(f"`{n}`" for n in env_names) or "none") + ".")
    w.append("")
    for place in PLACES:
        pr = [r for r in rows if r["place"] == place]
        base = [_context(r) for r in pr if r["config"] in ("baseline", "baseline-repeat") and r.get("exit_code") == 0]
        base = [b for b in base if b is not None]
        mean = int(statistics.mean(base)) if base else None
        noise = (max(base) - min(base)) if len(base) == 2 else None
        title = "a scratch repository" if place == "scratch" else "a worktree of Remedy"
        w.append(f"## In {title}")
        w.append(f"Baseline context: mean {_fmt(mean)}, the two baselines {_fmt(noise)} apart.")
        w.append("")
        w.append("| Config | Switches | Exit | Turns | Input | Output | Cache creation | Cache read | Context | Context minus baseline |")
        w.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in pr:
            ctx = _context(r) if r.get("exit_code") == 0 else None
            delta = ctx - mean if (ctx is not None and mean is not None) else None
            sw = " ".join(f"`{s}`" if s else '`""`' for s in r["switches"]) or "none"
            turns = r.get("num_turns")
            turns_cell = _fmt(turns) + (" (more than one)" if isinstance(turns, int) and turns > 1 else "")
            w.append(f"| {r['config']} | {sw} | {r.get('exit_code')} | {turns_cell} | "
                     + " | ".join(_fmt(r.get(k)) for k in KINDS)
                     + f" | {_fmt(ctx)} | {_fmt(delta)} |")
        refused = [r for r in pr if r.get("exit_code") != 0]
        for r in refused:
            w.append("")
            w.append(f"`{r['config']}` ended with exit {r.get('exit_code')}: "
                     + (r.get("error") or r.get("result") or "no text").replace("\n", " ")[:300])
        w.append("")
    (out / "f302_attribution.md").write_text("\n".join(w).rstrip("\n") + "\n")
    print("rendered", len(rows), "rows")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("run", "render"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default="")
    ap.add_argument("--remedy-rev", default="")
    ap.add_argument("--claude", default="")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.mode == "run":
        if not a.work or not a.remedy_rev:
            raise SystemExit("run needs --work and --remedy-rev")
        run(out, pathlib.Path(a.work), a.remedy_rev, a.claude)
    render(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
