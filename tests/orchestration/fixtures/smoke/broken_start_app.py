"""A real mini-app whose UNIT TESTS pass but whose STARTUP is broken.

This fixture is the whole feature in one file (F062 T001). Its pure logic is
correct and a unit test of it goes green — exactly the situation the smoke
exists for: green tests, broken product.

``main()`` fails the way real apps fail on startup: it reads a required
setting that is not there and exits non-zero before ever binding a port. The
smoke's ``app_starts`` check therefore never gets an answer on the health
path, and the job that owns it is held open with a concrete reason.
"""
from __future__ import annotations

import os
import sys


#: The pure logic. It works — that is the point.
def tax_cents(amount_cents: int, rate_percent: int) -> int:
    if amount_cents < 0:
        raise ValueError("amount must not be negative")
    return amount_cents * rate_percent // 100


def main() -> int:
    # The startup bug: a required setting nobody provides. The app dies here,
    # long before it could listen on PORT.
    endpoint = os.environ.get("PAYMENTS_ENDPOINT")
    if not endpoint:
        sys.stdout.write(
            "broken-start-app: FATAL config error: PAYMENTS_ENDPOINT is not set\n")
        sys.stdout.flush()
        return 78
    sys.stdout.write("broken-start-app: unreachable in this fixture\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
