"""Shared bases for structured-output models (F005).

Extracted from ``schemas.models`` so a contract defined in another module can
use the same bases WITHOUT importing ``models`` — which is what lets ``models``
import that contract to register its tag in ``SCHEMA_REGISTRY`` (F061 R3).

It sits OUTSIDE the ``schemas`` package deliberately. Importing
``schemas.anything`` runs ``schemas/__init__``, which imports ``models`` — so a
base module inside the package would re-enter the very cycle it exists to
break. This module imports nothing but pydantic and can therefore never take
part in one.

``models`` re-exports both names, so every existing
``from ...schemas.models import _Strict`` keeps working unchanged.
"""
from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class _Strict(BaseModel):
    """Base that rejects any field the schema did not declare."""

    model_config = ConfigDict(extra="forbid")


class _Structured(_Strict):
    """A top-level structured response.

    ``schema_v`` is a REQUIRED field (a bare ``Literal`` with no default) so a
    response that omits it is a validation failure, not a silently defaulted
    value. The model's version is read from the ``SCHEMA_V`` class constant — the
    validator never depends on a field default to know its own version.
    """

    #: The compact version this model enforces. Set by each concrete subclass.
    SCHEMA_V: ClassVar[str]
