"""Red-prove the conformance harness: apply one mutation to a tree, run the harness, restore byte-identical.

Usage: python3 -B harness_redproof.py <tree root> <harness measure.py>
Runs an unmutated control first and last. Each mutation must turn the harness red (exit 1)
with the failed-probe count printed; the control must be green (exit 0).
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
measure = Path(sys.argv[2]).resolve()
STATES = "apps/ui/src/components/graph/renderers/nodeStates.ts"
PAINT = "apps/ui/src/components/graph/renderers/paintNode.ts"

MUTATIONS = [
    ("h1", "a failed node loses its status dot", STATES,
     '    name: "Failed",\n    fillToken: "--remedy-state-blocked",\n    inkToken: "--remedy-graph-node-ring",\n'
     '    lineToken: "--remedy-state-blocked",\n    halo: { token: "--remedy-state-blocked", alpha: 0.4 },\n'
     '    sizeFactor: 1,\n    marks: [{ mark: "status_dot", token: "--remedy-state-blocked", outlineToken: "--remedy-graph-node-ring" }],\n',
     '    name: "Failed",\n    fillToken: "--remedy-state-blocked",\n    inkToken: "--remedy-graph-node-ring",\n'
     '    lineToken: "--remedy-state-blocked",\n    halo: { token: "--remedy-state-blocked", alpha: 0.4 },\n'
     '    sizeFactor: 1,\n    marks: [],\n'),
    ("h2", "the painter draws marks without their outline", PAINT,
     "    if (mark.outlineToken && shape) {\n", "    if (false && mark.outlineToken && shape) {\n"),
    ("h3", "the open state carries the strike too", STATES,
     '    name: "Suggested",\n    fillToken: "--remedy-state-open",\n    inkToken: "--remedy-graph-node-ring",\n'
     '    lineToken: "--remedy-state-open",\n    halo: { token: "--remedy-state-open", alpha: 0.4 },\n    sizeFactor: 1,\n    marks: [],\n',
     '    name: "Suggested",\n    fillToken: "--remedy-state-open",\n    inkToken: "--remedy-graph-node-ring",\n'
     '    lineToken: "--remedy-state-open",\n    halo: { token: "--remedy-state-open", alpha: 0.4 },\n    sizeFactor: 1,\n'
     '    marks: [{ mark: "strike", token: "--remedy-state-vetoed", outlineToken: "--remedy-graph-node-ring" }],\n'),
    ("h4", "the status dot is drawn at the top left", "apps/ui/src/components/graph/renderers/glyphPaths.ts",
     '    fillPath: "M23 4.5A3 3 0 1 1 17 4.5A3 3 0 1 1 23 4.5Z",\n',
     '    fillPath: "M7 4.5A3 3 0 1 1 1 4.5A3 3 0 1 1 7 4.5Z",\n'),
]


def run(tag):
    proc = subprocess.run([sys.executable, "-B", str(measure), str(tree)], capture_output=True, text=True, timeout=300)
    out = proc.stdout
    summary = re.search(r"CONFORMANCE: .*", out)
    failed = len(re.findall(r"^FAILED ", out, re.M))
    line = summary.group(0) if summary else "no summary"
    print(f"{tag}: exit {proc.returncode}, {line}, FAILED lines {failed}")
    return proc.returncode


ok = run("control first") == 0
for mid, name, rel, old, new in MUTATIONS:
    target = tree / rel
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    if text.count(old) != 1:
        print(f"{mid}: SKIPPED, FROM occurs {text.count(old)} times")
        ok = False
        continue
    target.write_text(text.replace(old, new, 1))
    try:
        code = run(f"{mid} ({name})")
    finally:
        target.write_bytes(original)
    restored = hashlib.sha256(target.read_bytes()).hexdigest() == digest
    print(f"{mid}: red={code != 0} restored byte-identical={restored}")
    ok = ok and code != 0 and restored
ok = run("control last") == 0 and ok
print(f"ALL HARNESS MUTATIONS CAUGHT AND RESTORED CLEANLY: {ok}")
sys.exit(0 if ok else 1)
