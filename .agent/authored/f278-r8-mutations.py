"""F278 R8 G5 — mutation red-proofs of the two repairs and the ratchet, in a DISPOSABLE worktree.

Usage: python3 mutations.py <worktree-path>. Each mutation names its file, a FROM text that must
occur EXACTLY ONCE in it, the replacement, and the test it must turn red. The file is restored
byte-for-byte after each, and an unmutated control of every named test runs first and last.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
DO = "packages/orchestration/do_sequence.py"
RS = "packages/orchestration/review_subject.py"
HR = "packages/orchestration/hunk_ledger.py"
PY = "pyproject.toml"
T_DO = "tests/orchestration/test_do_sequence.py"
T_RS = "tests/orchestration/test_review_subject_strict_schema.py::TestMetadataScannerFailsClosed"
T_RATCHET = "tests/test_ble001_ratchet.py"
MUTATIONS = {
    "m1_budgets_dropped_again": (
        DO,
        '            raise OrderJobPlanError(f"job budgets rejected: {exc}") from exc\n',
        "            job_budgets = None\n",
        T_DO),
    "m2_fences_dropped_again": (
        DO,
        '            raise OrderJobPlanError(f"job fences rejected: {exc}") from exc\n',
        "            job_fences = None\n",
        T_DO),
    "m3_scanner_failure_clears_again": (
        RS,
        "    except Exception:  # noqa: BLE001 — a scanner that raised cannot clear the value"
        " (R-1038)\n        return False\n",
        "    except Exception:  # noqa: BLE001 — a scanner that raised cannot clear the value"
        " (R-1038)\n        pass\n",
        T_RS),
    "m4_a_reason_removed": (
        HR,
        "    except Exception:  # noqa: BLE001 — an unreadable ledger import yields empty,"
        " never partial\n",
        "    except Exception:  # noqa: BLE001\n",
        T_RATCHET),
    "m5_a_mark_removed": (
        HR,
        "    except Exception:  # noqa: BLE001 — an unreadable ledger import yields empty,"
        " never partial\n",
        "    except Exception:\n",
        T_RATCHET),
    "m6_rule_deselected": (
        PY,
        'select = ["E", "F", "W", "I", "UP", "BLE001"]\n',
        'select = ["E", "F", "W", "I", "UP"]\n',
        T_RATCHET),
}


def run(label: str, test: str) -> None:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


tests = sorted({m[3] for m in MUTATIONS.values()})
for t in tests:
    run(f"control_before {t}", t)
for name, (rel, frm, to, test) in MUTATIONS.items():
    src = WT / rel
    good = src.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    src.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name, test)
    src.write_bytes(good)
    print(f"{name} restored byte-identical: {src.read_bytes() == good}")
for t in tests:
    run(f"control_after {t}", t)
