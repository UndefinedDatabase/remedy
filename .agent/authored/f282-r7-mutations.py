"""F282 R7 G5 — red proofs of R-0622 and R-1029, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit
and must already carry `apps/ui/node_modules` from `npm ci --prefix apps/ui`, or the lint tests
skip and prove nothing; this script refuses to run without it. A FROM/TO mutation asserts its
FROM occurs EXACTLY ONCE before it is applied; a REVERT puts the named file back to its bytes at
the named commit. Every file is restored byte-for-byte after each probe, and an unmutated control
runs first and last. pytest runs under `python3 -B` (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
if not (WT / "apps/ui/node_modules/typescript-eslint").is_dir():
    sys.exit("apps/ui/node_modules/typescript-eslint is missing: run `npm ci --prefix apps/ui` first")
TESTS = ["tests/ui_contracts/test_ui_lint.py", "tests/ui_contracts/test_digest_mount.py",
         "tests/docs/test_bootstrap_reads_decisions_by_part.py"]
CFG = "apps/ui/eslint.config.js"
SHELL = "apps/ui/src/components/shell/RemedyShell.tsx"
MUTATIONS = {
    "m1_no_typescript_parser": (CFG, "    languageOptions: { parser: tseslint.parser },\n", ""),
    "m2_no_undef_back_on": (CFG, '      "no-undef": "off",\n', ""),
    "m3_the_effect_misses_its_port": (
        SHELL, "  }, [digestPort, dashboard.jobId]);\n", "  }, [dashboard.jobId]);\n"),
    "m5_the_port_rebuilt_every_render": (
        SHELL, "useMemo(() => browserDigestVisibilityPort(window.localStorage), [])",
        "browserDigestVisibilityPort(window.localStorage)"),
    "m4_phase_0_reads_decisions_whole": (
        "docs/agents/self_drive_protocol.md",
        "`.agent/decisions.md` is NEVER read whole at session start: it holds hundreds\n",
        "`.agent/decisions.md` is read at session start: it holds hundreds\n"),
}
REVERTS = {
    "r1_eslint_config_before_this_round": ("2a8186c4", CFG),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfEs", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith(("FAILED", "ERROR", "SKIPPED")) or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
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
for name, (rev, rel) in REVERTS.items():
    path = WT / rel
    good = path.read_bytes()
    old = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{rel}"], capture_output=True, check=True)
    path.write_bytes(old.stdout)
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
