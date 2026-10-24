"""F157 R9 — mask what the agent-state guard refuses in the self-use run's recorded job diff.

Run once from the primary checkout: python3 .agent/authored/f157-r9-mask-job-diff.py [root]
The self-use job of F157's closure wrote the first tests of the public-text redaction module, whose
fixtures are fake credentials and fake home-folder paths by design, and the commit hook refuses
those lines under `.agent/` (DECISION F157 D7). This script replaces each match the guard's rules
find in `.agent/selfuse_f157/job_diff.txt` with a marker naming the rule, puts a header above the
diff that states the count and the sha256 of the unmasked file, and writes nothing unless the
guard then finds nothing. The job's branch, named in the diff's first line, keeps the diff whole.
"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))

from scripts.check_agent_hygiene import _RULES, scan_agent_text  # noqa: E402

REL = ".agent/selfuse_f157/job_diff.txt"
HEADER = "MASKED COPY"
path = root / REL
raw = path.read_text(encoding="utf-8")
if raw.startswith(HEADER):
    sys.exit(f"refused: {REL} is already masked")
before = scan_agent_text(REL, raw)
count = 0


def _marker(reason: str):
    def replace(match) -> str:
        lead = match.group(0)[0] if match.group(0)[:1] in " \t'\"`(" else ""
        return f"{lead}[MASKED: {reason}]"
    return replace


lines = []
for line in raw.splitlines(keepends=True):
    for reason, pattern in _RULES:
        line, n = pattern.subn(_marker(reason), line)
        count += n
    lines.append(line)
header = (
    f"{HEADER}: {count} match(es) on {len(before)} line(s) that the agent-state guard refuses are\n"
    "replaced by a [MASKED: <rule>] marker (DECISION F157 D7). The job branch named in the diff's\n"
    f"first line keeps the diff whole. Unmasked sha256: {hashlib.sha256(raw.encode('utf-8')).hexdigest()}\n\n"
)
masked = header + "".join(lines)
after = scan_agent_text(REL, masked)
if after:
    sys.exit(f"refused: the guard still finds {len(after)} line(s): {after}")
path.write_text(masked, encoding="utf-8")
print(f"lines refused before {len(before)}, matches masked {count}, refused after {len(after)}")
print(f"unmasked sha256 {hashlib.sha256(raw.encode('utf-8')).hexdigest()}")
print(f"masked sha256 {hashlib.sha256(masked.encode('utf-8')).hexdigest()}")
