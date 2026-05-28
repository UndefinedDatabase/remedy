"""
packages.memory — Local Memory Gateway for Remedy.

Provides persistent, structured memory storage across job sessions.
Storage is JSONL-based at <DATA_DIR>/memory/<project_id>/memory.jsonl
or <DATA_DIR>/memory/unscoped/<job_id>.jsonl.

Public API::

    from packages.memory.local_gateway import store_memory, recall_memory, list_memory
    from packages.memory.models import MemoryEntry
"""
