"""F041 R5 C9 — the round 5 mutation tool (G5's red proofs, DECISION F041 D5).

Takes ONE argument: the path of a worktree checked out at C9. For each mutation below it edits
the named production file INSIDE that worktree — asserting its FROM text occurs EXACTLY ONCE
there — runs the ONE runner the mutation names (`vitest`, scoped to `artifactPreview.test.ts`
and `previewSend.test.ts`, for the pure TypeScript layer; `pytest`, scoped to
`tests/ui_contracts/test_artifact_preview.py`, for the components no vitest DOM harness can
render), restores the file's original bytes, and reports whether the mutation was CAUGHT: real
exit code 1 with at least one failed test. A collection or import error (any other non-zero
exit, or a zero exit) is a broken edit, not a reading.

BOTH runners are also run, unmutated, as the control — once before the first mutation and once
after the last.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FAILED_RE = re.compile(r"(\d+) failed")

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY_ROOT / "apps" / "ui" / "vitest.config.ts"
VITEST_TEST_FILES = ("src/api/artifactPreview.test.ts", "src/api/previewSend.test.ts")
PYTEST_CONTRACT_TEST = "tests/ui_contracts/test_artifact_preview.py"


@dataclass(frozen=True)
class Mutation:
    label: str
    prod_path: str
    runner: str  # "vitest" or "pytest"
    from_text: str
    to_text: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "m1 readmeCockpitHtml leaves an image outside captures/ in place",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '    const found = images.find((image) => image.path === decodedSrc);\n'
        '    if (found === undefined) {\n'
        '      return alt;\n'
        '    }\n',
        '    const found = images.find((image) => image.path === decodedSrc) ?? images[0];\n',
    ),
    Mutation(
        "m2 readmeCockpitHtml drops the token from the rewritten address",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '    const address = escapeAttributeValue(artifactFilePath(request, "evidence", found.path));\n',
        '    const address = escapeAttributeValue('
        'artifactFilePath({ ...request, token: "" }, "evidence", found.path));\n',
    ),
    Mutation(
        "m3 previewCardView offers the link while probing",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '    case "probing":\n'
        '      return {\n'
        '        line: "The app started. Checking that it answers…", detail: "",\n'
        '        action: "stop", actionLabel: "Stop app", link: null,\n'
        '      };\n',
        '    case "probing":\n'
        '      return {\n'
        '        line: "The app started. Checking that it answers…", detail: "",\n'
        '        action: "stop", actionLabel: "Stop app", link: view.url,\n'
        '      };\n',
    ),
    Mutation(
        "m4 previewCardView offers a link to any address while live",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '        link: HTTP_URL_PATTERN.test(view.url) ? view.url : null,\n',
        '        link: view.url,\n',
    ),
    Mutation(
        "m5 decodePreviewView accepts a state outside PREVIEW_STATES",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '  if (typeof stateCandidate !== "string"\n'
        '      || !(PREVIEW_STATES as readonly string[]).includes(stateCandidate)) {\n'
        '    return null;\n'
        '  }\n',
        '  if (typeof stateCandidate !== "string") {\n'
        '    return null;\n'
        '  }\n',
    ),
    Mutation(
        "m6 lightboxIndexAfter wraps from the last picture to the first",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        '  if (key === "ArrowRight") return Math.min(index + 1, count - 1);\n',
        '  if (key === "ArrowRight") return (index + 1) % count;\n',
    ),
    Mutation(
        "m7 previewPollDelayMs answers the slow delay while starting",
        "apps/ui/src/api/artifactPreview.ts",
        "vitest",
        'export function previewPollDelayMs(view: PreviewView | null): number {\n'
        '  if (view !== null && (view.state === "starting" || view.state === "probing")) {\n'
        '    return PREVIEW_POLL_FAST_MS;\n'
        '  }\n'
        '  return PREVIEW_POLL_SLOW_MS;\n'
        '}\n',
        'export function previewPollDelayMs(view: PreviewView | null): number {\n'
        '  if (view !== null && view.state === "probing") {\n'
        '    return PREVIEW_POLL_FAST_MS;\n'
        '  }\n'
        '  return PREVIEW_POLL_SLOW_MS;\n'
        '}\n',
    ),
    Mutation(
        "m8 buildPreviewSendRequest leaves out the CSRF header",
        "apps/ui/src/api/previewSend.ts",
        "vitest",
        '      Authorization: `Bearer ${target.serverToken}`,\n'
        '      "X-Remedy-CSRF": target.serverToken,\n'
        '      "Content-Type": "application/json",\n',
        '      Authorization: `Bearer ${target.serverToken}`,\n'
        '      "Content-Type": "application/json",\n',
    ),
    Mutation(
        "m9 loadPreviewView lets a failed read throw",
        "apps/ui/src/api/remedyApi.ts",
        "vitest",
        'export async function loadPreviewView(\n'
        '  request: { jobId: string; token: string; baseUrl?: string },\n'
        '  fetchPayload: PreviewFetcher = fetchJson,\n'
        '): Promise<PreviewView | null> {\n'
        '  try {\n'
        '    return decodePreviewView(await fetchPayload(previewViewPath(request)));\n'
        '  } catch {\n'
        '    return null;\n'
        '  }\n'
        '}\n',
        'export async function loadPreviewView(\n'
        '  request: { jobId: string; token: string; baseUrl?: string },\n'
        '  fetchPayload: PreviewFetcher = fetchJson,\n'
        '): Promise<PreviewView | null> {\n'
        '  return decodePreviewView(await fetchPayload(previewViewPath(request)));\n'
        '}\n',
    ),
    Mutation(
        "m10 the panel renders in place, without createPortal",
        "apps/ui/src/components/artifacts/ArtifactsPanel.tsx",
        "pytest",
        '  return createPortal(\n',
        '  return (\n',
    ),
    Mutation(
        "m11 the lightbox writes its caption through dangerouslySetInnerHTML",
        "apps/ui/src/components/artifacts/ArtifactLightbox.tsx",
        "pytest",
        '        <p data-ui="artifact-lightbox-caption" className={styles.caption}>\n'
        '          {`${index + 1} of ${images.length} · ${caption}`}\n'
        '        </p>\n',
        '        <p data-ui="artifact-lightbox-caption" className={styles.caption}\n'
        '           dangerouslySetInnerHTML={{ __html: '
        '`${index + 1} of ${images.length} · ${caption}` }} />\n',
    ),
    Mutation(
        "m12 the card's effect cleanup no longer clears its timeout",
        "apps/ui/src/components/artifacts/AppPreviewCard.tsx",
        "pytest",
        '    return () => {\n'
        '      cancelled = true;\n'
        '      window.clearTimeout(timeoutId);\n'
        '    };\n',
        '    return () => {\n'
        '      cancelled = true;\n'
        '    };\n',
    ),
    Mutation(
        "m13 the Results button is removed from RightLivePanel.tsx",
        "apps/ui/src/components/panels/RightLivePanel.tsx",
        "pytest",
        '      {onOpenResults && (<button type="button" className={styles.advancedToggle} '
        'onClick={onOpenResults}>Results</button>)}\n',
        '',
    ),
)


def run_vitest(worktree: Path) -> tuple[int, int, str]:
    root = worktree / "apps" / "ui"
    result = subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(root), "--config", str(VITEST_CONFIG),
         *VITEST_TEST_FILES],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    output = result.stdout + result.stderr
    match = FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed, output


def run_pytest_contract(worktree: Path) -> tuple[int, int, str]:
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", PYTEST_CONTRACT_TEST],
        cwd=str(worktree), capture_output=True, text=True, check=False,
    )
    output = result.stdout + result.stderr
    match = FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed, output


def run_for_runner(worktree: Path, runner: str) -> tuple[int, int, str]:
    if runner == "vitest":
        return run_vitest(worktree)
    return run_pytest_contract(worktree)


def run_control(worktree: Path, label: str) -> bool:
    clean = True
    for runner in ("vitest", "pytest"):
        code, failed, output = run_for_runner(worktree, runner)
        print(f"control ({label}) {runner}: exit={code} failed={failed}")
        if code != 0 or failed != 0:
            clean = False
            print(output)
    return clean


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: f041-r5-mutations.py <worktree-path>", file=sys.stderr)
        sys.exit(2)
    worktree = Path(sys.argv[1]).resolve()

    all_clean = True
    all_clean &= run_control(worktree, "first")

    for mutation in MUTATIONS:
        prod_file = worktree / mutation.prod_path
        original = prod_file.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(mutation.from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{mutation.label}: FROM text occurs {occurrences} times in "
                f"{mutation.prod_path}, expected exactly 1")
        mutated_text = text.replace(mutation.from_text, mutation.to_text, 1)
        prod_file.write_text(mutated_text, encoding="utf-8")

        try:
            code, failed, output = run_for_runner(worktree, mutation.runner)
        finally:
            prod_file.write_bytes(original)

        caught = code == 1 and failed >= 1
        print(f"{mutation.label}: runner={mutation.runner} exit={code} failed={failed} caught={caught}")
        if not caught:
            print(output)
            all_clean = False

        restored = prod_file.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_clean = False

    all_clean &= run_control(worktree, "last")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")
    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
