"""F263 R2 G5 — mutation red-proofs of the human change record's evidence path, in a DISPOSABLE
worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_human_change_evidence.py",
         "tests/orchestration/test_review_package_status.py"]
HC = "packages/orchestration/human_change.py"
FV = "packages/orchestration/final_verifier.py"
BRM = "scripts/build_review_manifest.py"
MUTATIONS = {
    "m1_export_never_verifies": (
        HC,
        '        failures.extend(f"{record_id}: {p}" for p in verify_human_change_record(dest / record.name))\n',
        "",
    ),
    "m2_job_export_writes_no_integrity": (
        "packages/orchestration/job_evidence.py",
        "    _write_json(_hc.INTEGRITY_FILE, _hc_integrity)\n",
        "",
    ),
    "m3_verifier_reads_no_failures": (
        FV,
        '        list(_hc_integrity.get("failures") or []) if isinstance(_hc_integrity, dict) else []\n',
        "        []\n",
    ),
    "m4_verdict_ignores_the_block": (
        FV,
        "        or human_change_integrity_blocked\n",
        "",
    ),
    "m5_manifest_does_not_require_the_gate": (
        BRM,
        '_OK_GATES = ("manifest_integrity.json", "postmortem_integrity.json",\n'
        '             "human_change_integrity.json")\n',
        '_OK_GATES = ("manifest_integrity.json", "postmortem_integrity.json")\n',
    ),
    "m6_manifest_ignores_a_blocked_verifier": (
        BRM,
        '            ("human_change_integrity_blocked", False),\n',
        "",
    ),
    "m7_manual_bundle_writes_no_integrity": (
        "packages/orchestration/manual_attestation.py",
        '    _w(os.path.join(evidence_dir, "human_change_integrity.json"),\n'
        '       {"schema_version": "1.0.0", "ok": True, "records": [], "failures": []})\n',
        "",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


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
