"""One named file (and its tests) is one bounded job whatever the wording (lab orders of 2026-10-17).

Each lab order that day missed a different phrase pattern ("diesen Abschnitt:", "Projekttest",
"Schreibe dazu einen Regressionstest", describing sentences) and fell to the local planner, whose
plan then failed. The lane now rests on the files an order names, not on its sentences.
"""
from __future__ import annotations

import pytest

from packages.orchestration.do_lane import select_do_lane
from packages.orchestration.task_deliverables import deliverable_task

FILES = ["README.md", "package.json", "src/calc.js", "src/format.js", "test/baseline.test.js", ".gitignore"]

PHRASINGS = [
    ("Ergänze am Ende von README.md einen Abschnitt Testbetrieb mit zwei Sätzen.", "README.md", False),
    ("Bitte in der README.md unten noch einen kurzen Abschnitt 'Testbetrieb' hinzufügen, der erklärt, "
     "dass das Repo nur zum Testen da ist. Danach die Tests laufen lassen. Nichts automatisch übernehmen.",
     "README.md", False),
    ("Kannst du README.md um einen Abschnitt erweitern?\n\n## Testbetrieb\n\nHier wird getestet.\n\n"
     "Sonst nichts ändern.", "README.md", False),
    ("Add a 'Testing' section at the end of README.md. Keep everything else unchanged and run npm test.",
     "README.md", False),
    ("add(a, b) in src/calc.js ist kaputt, es subtrahiert. Mach das richtig und leg in test/calc.test.js "
     "einen Test an, der das beweist.", "src/calc.js", True),
    ("In src/calc.js gibt add falsch zurück. Bitte fixen. Ein Regressionstest gehört nach "
     "test/calc.test.js. Tests ausführen, nichts committen.", "src/calc.js", True),
    ("The add function in src/calc.js returns a - b. It should return a + b. Also please cover it with "
     "a test in test/calc.test.js.", "src/calc.js", True),
    ("src/calc.js: add() liefert die Differenz statt der Summe. Das soll behoben werden; "
     "test/calc.test.js soll den Fall abdecken.", "src/calc.js", True),
    ('Die Funktion normalizeName(input) in src/format.js soll bei leerem Text "Unbekannt" zurückgeben. '
     "Schreibe dazu einen Regressionstest in test/format.test.js und korrigiere die Funktion mit "
     "möglichst wenig Code.", "src/format.js", True),
    ("normalizeName in src/format.js crasht bei leerem String. Erwartet wird 'Unbekannt'. Bitte auch "
     "gleich test/format.test.js anlegen.", "src/format.js", True),
    ("Leerer oder nur aus Leerzeichen bestehender Input soll in src/format.js zu 'Unbekannt' führen; "
     "normale Namen wie bisher. Test dazu: test/format.test.js. Keine neuen Abhängigkeiten.",
     "src/format.js", True),
    ("Fix src/format.js so that normalizeName('   ') returns 'Unbekannt', with a regression test in "
     "test/format.test.js.", "src/format.js", True),
]


@pytest.mark.parametrize(("order", "deliverable", "with_tests"), PHRASINGS)
def test_one_named_file_is_one_bounded_job_whatever_the_wording(order, deliverable, with_tests):
    lane = select_do_lane(order, tracked_files=FILES)
    assert (lane.lane, lane.deliverable, lane.with_tests) == ("bounded", deliverable, with_tests)
    if with_tests:
        test_file = "test/calc.test.js" if "calc" in deliverable else "test/format.test.js"
        assert deliverable_task(deliverable, order, with_tests=True).title == (
            f"Deliver {deliverable} and its test {test_file}")


def test_two_named_source_files_are_one_bounded_job_and_four_go_to_the_planner():
    """exec-1017 D14 left two named source files to the local planner, whose plans for small orders
    failed; a small change over a few named files is one bounded task now (2026-10-17 order)."""
    lane = select_do_lane("Fix add in src/calc.js and normalizeName in src/format.js.", tracked_files=FILES)
    assert (lane.lane, lane.deliverable, lane.also) == ("bounded", "src/calc.js", ("src/format.js",))
    many = select_do_lane("Fix src/calc.js, src/format.js, README.md and package.json.", tracked_files=FILES)
    assert many.lane == "full"
