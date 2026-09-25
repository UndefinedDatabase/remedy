"""F024 T002 — the scrubber's snapshots are spaced as the spec says and checked against the reducer.

`apps/ui/src/components/timeline/scrubSnapshots.ts` serves the reducer state at any seq
from a memoized snapshot plus at most one spacing of reductions (T5_F024.md T002,
DECISION F024 D2). The spacing is a binding figure of the feature file and the roadmap,
which the vitest environment cannot read, and the property test is only worth its name
while its oracle is the reducer's own fresh fold rather than the memo under test. This
guard pins both.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TIMELINE = ROOT / "apps" / "ui" / "src" / "components" / "timeline"
MEMO = TIMELINE / "scrubSnapshots.ts"
PROPERTY = TIMELINE / "scrubSnapshots.test.ts"
FEATURE = ROOT / "docs" / "roadmap" / "features" / "T5_F024.md"
ROADMAP = ROOT / "docs" / "roadmap" / "ROADMAP.md"


def _code(path: Path) -> str:
    # Comments are stripped first, so a WHY comment naming a word cannot satisfy or
    # trip a guard about the code (finding R-0584).
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def test_the_spacing_is_the_one_the_feature_file_and_the_roadmap_state():
    feature = re.search(r"memoized every (\d+) seq", FEATURE.read_text(encoding="utf-8"))
    roadmap = re.search(r"memoized snapshots every (\d+) seq", ROADMAP.read_text(encoding="utf-8"))
    assert feature and roadmap, "the spec no longer states the snapshot spacing"
    assert feature.group(1) == roadmap.group(1)
    constant = re.search(r"^export const SNAPSHOT_EVERY = (\d+);$", _code(MEMO), re.MULTILINE)
    assert constant, "scrubSnapshots.ts declares no `export const SNAPSHOT_EVERY = <n>;`"
    assert constant.group(1) == feature.group(1)


def test_the_cap_is_a_positive_whole_number():
    constant = re.search(r"^export const SNAPSHOT_CAP = (\d+);$", _code(MEMO), re.MULTILINE)
    assert constant and int(constant.group(1)) > 0


def test_the_memo_is_pure_and_folds_with_the_reducer_itself():
    src = _code(MEMO)
    imports = sorted(set(re.findall(r'^import [^;]*from "([^"]+)";$', src, re.MULTILINE)))
    assert imports == ["../graph/brainOntology", "../graph/brainReducer", "./phaseMapping"]
    assert "reduceBrainEvent(" in src and "timelineSeedOf(" in src
    for word in ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch("):
        assert word not in src, f"scrubSnapshots.ts reaches for {word}"


def test_the_property_test_s_oracle_is_a_fresh_reduction():
    src = _code(PROPERTY)
    assert re.search(r'^import \{[^}]*\brebuildBrainModel\b[^}]*\} from "\.\./graph/brainReducer";$', src, re.MULTILINE)
    assert "toEqual(fresh(" in src
    assert "Math.random" not in src, "a fuzzed position must replay: use the seeded generator"
