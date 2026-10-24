# Sandbox Model

> GENERATED from the sandbox profile and enforcement records in
> `packages/orchestration/sandbox_profiles.py` and
> `packages/orchestration/sandbox_container.py`, by `render_sandbox_model()`. Do not
> edit it by hand: `tests/docs/test_sandbox_model_doc.py` fails whenever this file and
> the rendering differ. Regenerate it from the repository root with
> `python3 scripts/render_sandbox_model.py`.

A sandbox profile fixes five dimensions a worker's sandbox decides: the filesystem
scope it may touch, its network reach, its resource ulimits, which binaries it may
run, and its tmp quota; the three `ulimits` keys each get their own row below, for
seven rows per profile. A dimension is marked enforced when a real mechanism stops the
run going past the declared value, never merely because the profile declares one
(DECISION F162 D3 (4)). Off Linux, every dimension that declares an actual limit reports
unenforced for both runners, because neither has a verified mechanism there; a
dimension with nothing to limit still reports enforced, trivially.

### strict

| Dimension | Declared | Process runner | Container runner | Proof |
|---|---|---|---|---|
| `fs_scope` | `["{workspace}"]` | prevents — the tool sandbox makes the workspace the one writable tree | prevents — the container's root is read-only and the workspace is its one writable mount | process: tests/orchestration/test_sandbox_profiles.py::test_strict_pins_the_workspace_as_the_one_writable_tree; container: tests/orchestration/test_sandbox_container.py::test_container_strict_pins_the_workspace_as_the_one_writable_tree |
| `net` | `deny` | prevents — a private network namespace with its own loopback only | prevents — the container has no network | process: tests/orchestration/test_sandbox_profiles.py::test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can; container: tests/orchestration/test_sandbox_container.py::test_container_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can |
| `ulimits.cpu_s` | `600` | prevents — RLIMIT_CPU on the process tree | prevents — --ulimit cpu inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds; container: tests/orchestration/test_sandbox_container.py::test_container_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds |
| `ulimits.mem_mb` | `2048` | prevents — RLIMIT_AS on the process tree | prevents — the container's cgroup memory limit | process: tests/orchestration/test_sandbox_profiles.py::test_a_mem_limit_of_256_mib_refuses_1gib_and_allows_64mib; container: tests/orchestration/test_sandbox_container.py::test_container_a_mem_limit_of_256_mib_refuses_1gib_and_allows_64mib |
| `ulimits.nofile` | `256` | prevents — RLIMIT_NOFILE on the process tree | prevents — --ulimit nofile inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24; container: tests/orchestration/test_sandbox_container.py::test_container_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24 |
| `allowed_binaries` | `["git", "python3", "sh"]` | does not prevent — binaries are not filtered by name | does not prevent — binaries are not filtered by name | process: tests/orchestration/test_sandbox_profiles.py::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_strict_with_a_runtime |
| `tmp_quota_mb` | `64` | does not prevent — the private /tmp has no size limit | prevents — a size-limited /tmp inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux; container: tests/orchestration/test_sandbox_container.py::test_container_tmp_quota_of_64_mib_refuses_a_100_mib_write_with_errno_28 |

### standard

| Dimension | Declared | Process runner | Container runner | Proof |
|---|---|---|---|---|
| `fs_scope` | `["{workspace}"]` | prevents — the tool sandbox makes the workspace the one writable tree | prevents — the container's root is read-only and the workspace is its one writable mount | process: tests/orchestration/test_sandbox_profiles.py::test_strict_pins_the_workspace_as_the_one_writable_tree; container: tests/orchestration/test_sandbox_container.py::test_container_strict_pins_the_workspace_as_the_one_writable_tree |
| `net` | `deny` | prevents — a private network namespace with its own loopback only | prevents — the container has no network | process: tests/orchestration/test_sandbox_profiles.py::test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can; container: tests/orchestration/test_sandbox_container.py::test_container_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can |
| `ulimits.cpu_s` | `1800` | prevents — RLIMIT_CPU on the process tree | prevents — --ulimit cpu inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds; container: tests/orchestration/test_sandbox_container.py::test_container_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds |
| `ulimits.mem_mb` | `unlimited` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `ulimits.nofile` | `1024` | prevents — RLIMIT_NOFILE on the process tree | prevents — --ulimit nofile inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24; container: tests/orchestration/test_sandbox_container.py::test_container_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24 |
| `allowed_binaries` | `any` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `tmp_quota_mb` | `512` | does not prevent — the private /tmp has no size limit | prevents — a size-limited /tmp inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux; container: tests/orchestration/test_sandbox_container.py::test_container_tmp_quota_of_64_mib_refuses_a_100_mib_write_with_errno_28 |

### net-local

| Dimension | Declared | Process runner | Container runner | Proof |
|---|---|---|---|---|
| `fs_scope` | `["{workspace}"]` | prevents — the tool sandbox makes the workspace the one writable tree | prevents — the container's root is read-only and the workspace is its one writable mount | process: tests/orchestration/test_sandbox_profiles.py::test_strict_pins_the_workspace_as_the_one_writable_tree; container: tests/orchestration/test_sandbox_container.py::test_container_strict_pins_the_workspace_as_the_one_writable_tree |
| `net` | `{ allow = ["127.0.0.1", "::1", "localhost"] }` | does not prevent — the host network is shared and hosts are not filtered | does not prevent — the container shares the host network and hosts are not filtered | process: tests/orchestration/test_sandbox_profiles.py::test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can; container: tests/orchestration/test_sandbox_container.py::test_container_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can |
| `ulimits.cpu_s` | `1800` | prevents — RLIMIT_CPU on the process tree | prevents — --ulimit cpu inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds; container: tests/orchestration/test_sandbox_container.py::test_container_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds |
| `ulimits.mem_mb` | `unlimited` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `ulimits.nofile` | `1024` | prevents — RLIMIT_NOFILE on the process tree | prevents — --ulimit nofile inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24; container: tests/orchestration/test_sandbox_container.py::test_container_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24 |
| `allowed_binaries` | `any` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `tmp_quota_mb` | `512` | does not prevent — the private /tmp has no size limit | prevents — a size-limited /tmp inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux; container: tests/orchestration/test_sandbox_container.py::test_container_tmp_quota_of_64_mib_refuses_a_100_mib_write_with_errno_28 |

### claude-cli (adapter default)

| Dimension | Declared | Process runner | Container runner | Proof |
|---|---|---|---|---|
| `fs_scope` | `["{workspace}"]` | does not prevent — no tool sandbox: only the working directory is pinned | prevents — the container's root is read-only and the workspace is its one writable mount | process: tests/orchestration/test_sandbox_profiles.py::test_strict_pins_the_workspace_as_the_one_writable_tree; container: tests/orchestration/test_sandbox_container.py::test_container_strict_pins_the_workspace_as_the_one_writable_tree |
| `net` | `{ allow = ["api.anthropic.com"] }` | does not prevent — the host network is shared and hosts are not filtered | does not prevent — the container shares the host network and hosts are not filtered | process: tests/orchestration/test_sandbox_profiles.py::test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can; container: tests/orchestration/test_sandbox_container.py::test_container_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can |
| `ulimits.cpu_s` | `unlimited` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `ulimits.mem_mb` | `unlimited` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `ulimits.nofile` | `1024` | prevents — RLIMIT_NOFILE on the process tree | prevents — --ulimit nofile inside the container | process: tests/orchestration/test_sandbox_profiles.py::test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24; container: tests/orchestration/test_sandbox_container.py::test_container_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24 |
| `allowed_binaries` | `any` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
| `tmp_quota_mb` | `unlimited` | no limit declared | no limit declared | process: tests/orchestration/test_worker_adapter_slot.py::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal; container: tests/orchestration/test_sandbox_container.py::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime |
