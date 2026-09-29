"""F041 R6 C7 — the round 6 mutation tool (G5's red proofs, DECISION F041 D6).

Takes ONE argument: the path of a worktree checked out at C7. For each mutation below it
edits the named production file INSIDE that worktree — asserting its FROM text occurs
EXACTLY ONCE there — runs the ONE runner the mutation names (`vitest`, scoped with
`--root <worktree>/apps/ui --config` the primary's own `vitest.config.ts`; `pytest`, with
the worktree as the working directory and `python3 -B`), restores the file's original
bytes, and reports whether the mutation was CAUGHT: real exit code 1 with at least one
failed test. A collection or import error (any other non-zero exit, or a zero exit) is a
broken edit, not a reading.

BOTH runners are also run, unmutated, as the control — once before the first mutation and
once after the last, over every test file any mutation below targets.

n8 mutates `idle_stop_due` in `preview_control.py` so it never answers true, then runs
ONLY `tests/ui_server/test_preview_end_to_end.py` — its own 60-second wait for the record
to read `stopped` must time out and FAIL the test rather than hang the tool; that file's
`finally` still stops the fixture app and its supervisor even when the test itself fails.
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

CONTROL_VITEST_FILES = ("src/api/artifactPreview.test.ts", "src/api/resultTour.test.ts")
CONTROL_PYTEST_TARGETS = (
    "tests/orchestration/test_result_tour.py",
    "tests/ui_contracts/test_artifact_preview.py",
)
CONTROL_E2E_TARGET = ("tests/ui_server/test_preview_end_to_end.py",)


@dataclass(frozen=True)
class Mutation:
    label: str
    prod_path: str
    runner: str  # "vitest" or "pytest"
    test_target: tuple[str, ...]
    from_text: str
    to_text: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "n1 readmeCockpitHtml restored whole from fd124cc9b (R-1106's revert probe)",
        'apps/ui/src/api/artifactPreview.ts',
        'vitest',
        ('src/api/artifactPreview.test.ts',),
        '/** The one image shape the server\'s renderer and sanitizer emit, or any other `<img …>` tag: the\n *  first alternative captures a recognised image\'s `src` and `alt`; the second matches every\n *  other shape, with nothing captured. */\nconst README_IMG_PATTERN = /<img src="([^"]*)" alt="([^"]*)">|<img\\b[^>]*>/g;\n\n/** An address this cockpit may offer as a link: `http` or `https` only. */\nconst HTTP_URL_PATTERN = /^https?:\\/\\//i;\n\n/** A README image\'s `src`, decoded the way the sanitizer\'s own escaping is undone: the four\n *  named entities that are not `&amp;` first, `&amp;` last (so a doubly-escaped ampersand never\n *  decodes twice), then one leading `./` dropped. */\nfunction decodeReadmeImageSrc(raw: string): string {\n  const decoded = raw\n    .replace(/&lt;/g, "<")\n    .replace(/&gt;/g, ">")\n    .replace(/&quot;/g, "\\"")\n    .replace(/&#x27;/g, "\'")\n    .replace(/&amp;/g, "&");\n  return decoded.startsWith("./") ? decoded.slice(2) : decoded;\n}\n\n/** The address `U` this function writes into an `src` attribute: every `&` and `"` escaped so\n *  the URL stays one attribute value. */\nfunction escapeAttributeValue(value: string): string {\n  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;");\n}\n\n/** The README\'s html, rewritten for the cockpit (DECISION F041 D5): every image whose decoded\n *  source names a listed capture becomes a link through the file route, with `loading="lazy"`;\n *  every other recognised image becomes its own alt text; every image of another shape is\n *  dropped. Nothing else in the html changes.\n *\n *  R-1106: ONE `replace` over `README_IMG_PATTERN`\'s alternation settles every image\'s fate as\n *  it is matched — a match of the recognised shape becomes the rewritten tag or the alt text,\n *  a match of any other shape becomes "". No marker, no placeholder and no second pass: a tag\n *  this function just built is never read again, so it can never be mistaken for one of the\n *  "other shapes" a second pass would have removed, and text that merely spells a marker-shaped\n *  string is never touched at all. */\nexport function readmeCockpitHtml(\n  html: string, images: readonly ImageArtifact[], request: ArtifactRequest,\n): string {\n  return html.replace(README_IMG_PATTERN, (_match, src?: string, alt?: string) => {\n    if (src === undefined || alt === undefined) {\n      return "";\n    }\n    const decodedSrc = decodeReadmeImageSrc(src);\n    const found = images.find((image) => image.path === decodedSrc);\n    if (found === undefined) {\n      return alt;\n    }\n    const address = escapeAttributeValue(artifactFilePath(request, "evidence", found.path));\n    return `<img src="${address}" alt="${alt}" loading="lazy">`;\n  });\n}\n',
        '/** The one image shape the server\'s renderer and sanitizer emit. */\nconst README_IMG_PATTERN = /<img src="([^"]*)" alt="([^"]*)">/g;\n\n/** Every `<img …>` of any other shape, removed once the shape above has already been handled. */\nconst STRAY_IMG_PATTERN = /<img\\b[^>]*>/g;\n\n/** An address this cockpit may offer as a link: `http` or `https` only. */\nconst HTTP_URL_PATTERN = /^https?:\\/\\//i;\n\n/** A README image\'s `src`, decoded the way the sanitizer\'s own escaping is undone: the four\n *  named entities that are not `&amp;` first, `&amp;` last (so a doubly-escaped ampersand never\n *  decodes twice), then one leading `./` dropped. */\nfunction decodeReadmeImageSrc(raw: string): string {\n  const decoded = raw\n    .replace(/&lt;/g, "<")\n    .replace(/&gt;/g, ">")\n    .replace(/&quot;/g, "\\"")\n    .replace(/&#x27;/g, "\'")\n    .replace(/&amp;/g, "&");\n  return decoded.startsWith("./") ? decoded.slice(2) : decoded;\n}\n\n/** The address `U` this function writes into an `src` attribute: every `&` and `"` escaped so\n *  the URL stays one attribute value. */\nfunction escapeAttributeValue(value: string): string {\n  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;");\n}\n\n/** The README\'s html, rewritten for the cockpit (DECISION F041 D5): every image whose decoded\n *  source names a listed capture becomes a link through the file route, with `loading="lazy"`;\n *  every other recognised image becomes its own alt text; every image of another shape is\n *  dropped. Nothing else in the html changes. */\nexport function readmeCockpitHtml(\n  html: string, images: readonly ImageArtifact[], request: ArtifactRequest,\n): string {\n  // A recognised image is placed behind a MARKER, printable ASCII a real README could not spell\n  // as this exact run, rather than its final tag: the broad removal pass below has to run AFTER\n  // this replacement (S1\'s own stated order), and without a marker it would delete the very\n  // `<img …>` this function just built, mistaking it for one of the "other shapes" it exists to\n  // drop.\n  const finals: string[] = [];\n  const withPlaceholders = html.replace(README_IMG_PATTERN, (_match, src: string, alt: string) => {\n    const decodedSrc = decodeReadmeImageSrc(src);\n    const found = images.find((image) => image.path === decodedSrc);\n    if (found === undefined) {\n      return alt;\n    }\n    const address = escapeAttributeValue(artifactFilePath(request, "evidence", found.path));\n    const index = finals.push(`<img src="${address}" alt="${alt}" loading="lazy">`) - 1;\n    return `@@artifact-image-${index}@@`;\n  });\n  const withoutStray = withPlaceholders.replace(STRAY_IMG_PATTERN, "");\n  return withoutStray.replace(/@@artifact-image-(\\d+)@@/g, (_match, index: string) => finals[Number(index)]);\n}\n',
    ),
    Mutation(
        'n2 anchor_problem resolves a preview anchor whatever previewable says',
        'packages/orchestration/result_tour.py',
        'pytest',
        ('tests/orchestration/test_result_tour.py',),
        '        resolved = context.previewable and ref == TOUR_PREVIEW_REF\n',
        '        resolved = ref == TOUR_PREVIEW_REF\n',
    ),
    Mutation(
        'n3 _project_previewable asks resolve_spec for an empty repo_path too',
        'packages/orchestration/result_tour.py',
        'pytest',
        ('tests/orchestration/test_result_tour.py',),
        '    if not isinstance(repo_path, str) or not repo_path or not Path(repo_path).is_dir():\n        return False\n',
        '    if not isinstance(repo_path, str) or not Path(repo_path).is_dir():\n        return False\n',
    ),
    Mutation(
        'n4 fallback_tour_stops leaves the preview stop out',
        'packages/orchestration/result_tour.py',
        'pytest',
        ('tests/orchestration/test_result_tour.py',),
        '    if preview_stop is not None:\n        stops.append(preview_stop)\n',
        '',
    ),
    Mutation(
        'n5 build_tour_prompt lists preview app for every context',
        'packages/orchestration/result_tour.py',
        'pytest',
        ('tests/orchestration/test_result_tour.py',),
        '    if context.previewable:\n        anchor_lines.append(f"preview {TOUR_PREVIEW_REF}")\n',
        '    anchor_lines.append(f"preview {TOUR_PREVIEW_REF}")\n',
    ),
    Mutation(
        'n6 tourCanShow answers false for preview',
        'apps/ui/src/api/resultTour.ts',
        'vitest',
        ('src/api/resultTour.test.ts',),
        '  return anchor.kind === "node" || anchor.kind === "diff" || anchor.kind === "preview";\n',
        '  return anchor.kind === "node" || anchor.kind === "diff";\n',
    ),
    Mutation(
        'n7 handleTourShowAnchor no longer opens the results panel for preview',
        'apps/ui/src/components/shell/RemedyShell.tsx',
        'pytest',
        ('tests/ui_contracts/test_artifact_preview.py',),
        '    } else if (anchor.kind === "preview") {\n      // DECISION F041 D6: a preview stop\'s "Show me" opens the Results panel, where the app\n      // card lives, the same way a diff stop opens the job\'s whole diff.\n      setResultsOpen(true);\n    }\n',
        '    }\n',
    ),
    Mutation(
        'n8 idle_stop_due in preview_control.py never answers true',
        'packages/orchestration/preview_control.py',
        'pytest',
        ('tests/ui_server/test_preview_end_to_end.py',),
        '    return (now - moment).total_seconds() >= ttl_seconds\n',
        '    return False\n',
    ),
)


def run_vitest(worktree: Path, test_files: tuple[str, ...]) -> tuple[int, int, str]:
    root = worktree / "apps" / "ui"
    result = subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(root), "--config", str(VITEST_CONFIG),
         *test_files],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    output = result.stdout + result.stderr
    match = FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed, output


def run_pytest(worktree: Path, test_targets: tuple[str, ...]) -> tuple[int, int, str]:
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_targets],
        cwd=str(worktree), capture_output=True, text=True, check=False,
    )
    output = result.stdout + result.stderr
    match = FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed, output


def run_for_mutation(worktree: Path, mutation: Mutation) -> tuple[int, int, str]:
    if mutation.runner == "vitest":
        return run_vitest(worktree, mutation.test_target)
    return run_pytest(worktree, mutation.test_target)


def run_control(worktree: Path, label: str) -> bool:
    clean = True
    code, failed, output = run_vitest(worktree, CONTROL_VITEST_FILES)
    print(f"control ({label}) vitest: exit={code} failed={failed}")
    if code != 0 or failed != 0:
        clean = False
        print(output)
    code, failed, output = run_pytest(worktree, CONTROL_PYTEST_TARGETS)
    print(f"control ({label}) pytest: exit={code} failed={failed}")
    if code != 0 or failed != 0:
        clean = False
        print(output)
    code, failed, output = run_pytest(worktree, CONTROL_E2E_TARGET)
    print(f"control ({label}) pytest (end-to-end): exit={code} failed={failed}")
    if code != 0 or failed != 0:
        clean = False
        print(output)
    return clean


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: f041-r6-mutations.py <worktree-path>", file=sys.stderr)
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
            code, failed, output = run_for_mutation(worktree, mutation)
        finally:
            prod_file.write_bytes(original)

        caught = code == 1 and failed >= 1
        print(f"{mutation.label}: runner={mutation.runner} exit={code} failed={failed} "
              f"caught={caught}")
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
