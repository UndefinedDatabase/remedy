"""The one classifier of repository paths whose CONTENT Remedy never reads into a job (amend1014c, R1).

Remedy deliberately does not keep a second list of credential spellings: the context pack, the
apply blocklist and the dirty-baseline capture all ask this module, and a path is judged by its
NAME alone, so nothing is opened, hashed or diffed to decide. `.gitignore` plays no part: a file
that Git ignores is exactly as sensitive as one it lists.
"""
from __future__ import annotations

import os

#: Exact base names that hold credentials.
SECRET_BASENAMES = frozenset({
    "credentials.json", "secrets.json", ".secrets", "api_key.txt",
    "service-account.json", "secrets.yaml", "secrets.yml",
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
})
#: Suffixes of private keys, certificates and key containers.
KEY_SUFFIXES = frozenset({".pem", ".key", ".p12", ".pfx", ".jks"})


def is_environment_file_name(name: str) -> bool:
    """True for `.env`, `.env.*` and `.env-*` by base name."""
    return name == ".env" or name.startswith((".env.", ".env-"))


def is_secret_file_name(name: str) -> bool:
    """True for an environment file or a credentials file by base name."""
    return is_environment_file_name(name) or name in SECRET_BASENAMES


def sensitive_path_category(rel_path: str) -> str:
    """The category name of a path Remedy must not read into a job, or "" for an ordinary path.

    The category is a short phrase safe to print; it never carries file content.
    """
    norm = rel_path.replace("\\", "/")
    parts = [p for p in norm.split("/") if p not in ("", ".")]
    if os.path.isabs(rel_path) or ".." in parts:
        return "a path outside the repository"
    if ".git" in parts:
        return "git metadata"
    base = parts[-1] if parts else ""
    if is_environment_file_name(base):
        return "an environment file"
    if base in SECRET_BASENAMES:
        return "a credentials file"
    if os.path.splitext(base)[1].lower() in KEY_SUFFIXES:
        return "a private key or certificate file"
    return ""


def sensitive_exclude_pathspecs() -> list[str]:
    """Git pathspecs that exclude every sensitive NAME, so a `git add` never reads or hashes them.

    Used where Remedy snapshots a whole checkout (the target's last known state): the excluded
    files are not opened, so their bytes never become a blob in the repository's object database.
    """
    names = [".env", ".env.*", ".env-*", *sorted(SECRET_BASENAMES), *(f"*{s}" for s in sorted(KEY_SUFFIXES))]
    return [f":(exclude,glob)**/{name}" for name in names]
