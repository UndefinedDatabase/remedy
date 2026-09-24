"""The closure's self-use track readings, run with the tree given as argv[1] as cwd and sys.path."""
import os
import subprocess
import sys

TREE = sys.argv[1]
os.chdir(TREE)
sys.path.insert(0, TREE)
from packages.orchestration.self_use_generator import generate_and_append_if_empty  # noqa: E402
from packages.orchestration.self_use_queue import next_self_use_item  # noqa: E402

print("next_self_use_item() before:", next_self_use_item())
print("generate_and_append_if_empty():", generate_and_append_if_empty())
print("next_self_use_item() after:", next_self_use_item())
print("git status --porcelain:", repr(subprocess.run(["git", "status", "--porcelain"],
                                                      capture_output=True, text=True).stdout))
