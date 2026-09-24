"""F264 R3 G5 — mutation red-proofs of the cockpit's steering input, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
vitest cannot start inside a worktree (it has no node_modules), so each vitest run is made from
the PRIMARY apps/ui with a scratch config whose `include` names the WORKTREE's test file by
absolute path and whose cache lives under `.remedy-wt/` (checklist item 33); pytest runs the
worktree's own Python guards under `python3 -B`. Each FROM is asserted to occur exactly once, the
file is restored byte-for-byte after each mutation, and an unmutated control runs first and last.
"""
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
PRIMARY_UI = pathlib.Path("/home/decodeux/Repos/remedy/apps/ui")
SCRATCH = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt/f264-r3-mut-vitest")
SCRATCH.mkdir(exist_ok=True)
CONFIG = SCRATCH / "vitest.config.mjs"
CONFIG.write_text("export default " + json.dumps({
    "root": str(PRIMARY_UI), "cacheDir": str(SCRATCH / "vite-cache"),
    "test": {"environment": "node", "include": [str(WT / "apps/ui/src/api/steeringSend.test.ts")]},
}) + ";\n")
PYTESTS = ["tests/ui_contracts/test_steering_send_contract.py",
           "tests/ui_contracts/test_brain_stream_ring.py"]
SEND = "apps/ui/src/api/steeringSend.ts"
MUTATIONS = {
    "u1_every_state_open": (
        SEND,
        "  return !STEERING_ENDED_STATES.includes(stage.trim().toLowerCase());\n",
        "  return true;\n",
    ),
    "u2_length_counted_in_code_units": (
        SEND,
        "      || Array.from(cleaned).length > STEERING_MAX_CHARS) {\n",
        "      || cleaned.length > STEERING_MAX_CHARS) {\n",
    ),
    "u3_untrimmed_message_sent": (
        SEND,
        "      args: { message: cleaned },\n",
        "      args: { message },\n",
    ),
    "u4_ended_job_unnamed": (
        SEND,
        '    case 409:\n      return { tone: "error", sentence: ENDED_SENTENCE };\n',
        "",
    ),
    "u5_request_without_job_or_token": (
        SEND,
        '  if (target.jobId === "" || target.serverToken === "" || cleaned === null\n',
        "  if (cleaned === null\n",
    ),
    "p1_refused_text_cleared": (
        "apps/ui/src/components/panels/ChatInput.tsx",
        '    if (answer.tone === "ok") {\n',
        "    if (true) {\n",
    ),
    "p2_limit_drifts_from_the_server": (
        SEND,
        "export const STEERING_MAX_CHARS = 2000;\n",
        "export const STEERING_MAX_CHARS = 1999;\n",
    ),
    "p3_card_never_closes_the_input": (
        "apps/ui/src/components/panels/ActivityFeedCard.tsx",
        '  const open = steeringIsOpen(stage ?? "");\n',
        "  const open = true;\n",
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
