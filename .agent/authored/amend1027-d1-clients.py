"""amend1027-green-builds D1: add the project remedy-edition to the clients orb-universe and orb-remedy.

The `remedy client` group has no command that changes a client's projects (DECISION amend1024 D6),
so this writes the registry as `set_client_host_tools` does: read only through `load_api_clients`'s
rules, written whole, readable by its owner only. It prints names and project lists, never a token.
Usage: REMEDY_DATA_DIR=<data root> python3 .agent/authored/amend1027-d1-clients.py
"""
from __future__ import annotations

import json

from packages.common.secure_fs import durable_write
from packages.orchestration.api_clients import api_clients_path, load_api_clients

PROJECT = "remedy-edition"
CLIENTS = ("orb-universe", "orb-remedy")

path = api_clients_path()
assert {c.name for c in load_api_clients()} >= set(CLIENTS), "a named client is missing; nothing changed"
document = json.loads(path.read_bytes().decode("utf-8"))
for entry in document["clients"]:
    if entry["name"] in CLIENTS and PROJECT not in entry["projects"]:
        entry["projects"].append(PROJECT)
durable_write(path, (json.dumps(document, indent=2) + "\n").encode("utf-8"), mode=0o600)
for client in load_api_clients():
    print(client.name, list(client.projects))
