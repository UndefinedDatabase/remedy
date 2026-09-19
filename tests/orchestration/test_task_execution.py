"""Architecture guards for proposed_tasks.py.

The task-execution port, its executors and budget gate these tests once covered were deleted
for finding R-0927; the guards on proposed_tasks.py stay.
"""

from __future__ import annotations

from pathlib import Path


class TestModularArchitectureGuards:
    def test_proposed_tasks_does_not_import_providers(self):
        src = Path("packages/orchestration/proposed_tasks.py").read_text()
        assert "import ollama" not in src
        assert "from ollama" not in src

    def test_storage_access_through_helpers(self):
        src = Path("packages/orchestration/proposed_tasks.py").read_text()
        assert "open(" not in src or "_atomic_write" in src
