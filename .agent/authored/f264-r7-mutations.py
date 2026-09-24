"""F264 R7 G5 — mutation red-proofs of the cockpit's steering acknowledgement, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
vitest cannot start inside a worktree (it has no node_modules), so each vitest run is made from
the PRIMARY apps/ui with a scratch config whose `include` names the WORKTREE's test files by
absolute path and whose cache lives under `.remedy-wt/` (checklist item 33); pytest runs the
worktree's own Python guard under `python3 -B`. Each FROM is asserted to occur exactly once, the
file is restored byte-for-byte after each mutation, and an unmutated control runs first and last.
"""
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
PRIMARY_UI = pathlib.Path("/home/decodeux/Repos/remedy/apps/ui")
SCRATCH = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt/f264-r7-mut-vitest")
SCRATCH.mkdir(exist_ok=True)
CONFIG = SCRATCH / "vitest.config.mjs"
CONFIG.write_text("export default " + json.dumps({
    "root": str(PRIMARY_UI), "cacheDir": str(SCRATCH / "vite-cache"),
    "test": {"environment": "node", "include": [
        str(WT / "apps/ui/src/api/steeringAck.test.ts"),
        str(WT / "apps/ui/src/api/feedRow.test.ts")]},
}) + ";\n")
PYTESTS = ["tests/ui_contracts/test_steering_send_contract.py"]
ACK = "apps/ui/src/api/steeringAck.ts"
MUTATIONS = {
    "u1_feed_keeps_the_catalog_line": (
        "apps/ui/src/api/feedRow.ts",
        "    line: ack ? steeringAckLine(ack) : humanized.line,\n",
        "    line: humanized.line,\n",
    ),
    "u2_round_left_unchecked": (
        ACK,
        '      || typeof roundNumber !== "number" || !Number.isInteger(roundNumber)) {\n',
        "      ) {\n",
    ),
    "u3_any_kind_read_as_an_ack": (
        ACK,
        "  if (envelope[\"event\"] !== STEERING_ACK_EVENT) {\n    return null;\n  }\n",
        "",
    ),
    "u4_restatement_dropped_from_the_line": (
        ACK,
        "  return `Steering taken in at round ${ack.roundNumber}: ${ack.understood}.`;\n",
        "  return `Steering taken in at round ${ack.roundNumber}.`;\n",
    ),
    "p1_reader_key_drifts_from_the_stream": (
        ACK,
        '  const understood = steering["understood"];\n',
        '  const understood = steering["restatement"];\n',
    ),
}


def run(label: str) -> None:
    v = subprocess.run([str(PRIMARY_UI / "node_modules/.bin/vitest"), "run", "--config", str(CONFIG)],
                       cwd=PRIMARY_UI, capture_output=True, text=True)
    vkeep = [ln.strip() for ln in (v.stdout + v.stderr).splitlines() if ln.strip().startswith("Tests ")]
    p = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTESTS],
                       cwd=WT, capture_output=True, text=True)
    pkeep = [ln for ln in p.stdout.splitlines()
             if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} VITEST_EXIT={v.returncode} {' '.join(vkeep)} PYTEST_EXIT={p.returncode}")
    print("\n".join(pkeep))


run("control_before")
for name, (rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
