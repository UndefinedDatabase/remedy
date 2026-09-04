"""
Domain tests: cli/test_review_cmd.py
"""

from __future__ import annotations

import json
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

import pytest


def _recs():
    return [{
        "id": "rec1",
        "title": "Add tests",
        "status": "pending",
        "created_at": "2026-09-04T00:00:00+00:00",
    }]


def test_text_output_shows_created_date(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=False)
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        _cmd_review_list(args)

    out = capsys.readouterr().out
    assert "created=2026-09-04T00:00:00+00:00" in out


def test_json_output_carries_created_at(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=True)
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        _cmd_review_list(args)

    data = json.loads(capsys.readouterr().out)
    assert data["recommendations"][0]["created_at"] == "2026-09-04T00:00:00+00:00"


def test_limit_caps_returned_recommendations(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    recs = [
        {"id": "rec1", "title": "A", "status": "pending", "created_at": "2026-09-01T00:00:00+00:00"},
        {"id": "rec2", "title": "B", "status": "pending", "created_at": "2026-09-02T00:00:00+00:00"},
        {"id": "rec3", "title": "C", "status": "pending", "created_at": "2026-09-03T00:00:00+00:00"},
    ]
    args = Namespace(job_id=str(job_stub.id), json=True, limit="2")
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=recs):
        _cmd_review_list(args)

    data = json.loads(capsys.readouterr().out)
    assert len(data["recommendations"]) == 2


def test_unknown_sort_field_exits_nonzero():
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=True, sort="bogus")
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        with pytest.raises(SystemExit) as exc:
            _cmd_review_list(args)
    assert exc.value.code == 1
