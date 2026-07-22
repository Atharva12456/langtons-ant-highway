#!/usr/bin/env python3
"""Regenerate the repository artifact manifest deterministically.

The manifest covers every tracked file plus every non-ignored untracked release
file.  It deliberately excludes itself, since a file cannot contain its own
cryptographic digest.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = "results/artifact_hashes.json"
TARGET = ROOT / TARGET_REL


def repository_files() -> list[str]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        check=True,
        stdout=subprocess.PIPE,
    )
    names = completed.stdout.decode("utf-8").split("\0")
    result: set[str] = set()
    for name in names:
        if not name or name == TARGET_REL:
            continue
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe repository path: {name!r}")
        disk_path = ROOT.joinpath(*path.parts)
        if not disk_path.is_file():
            raise FileNotFoundError(disk_path)
        result.add(path.as_posix())
    return sorted(result)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    names = repository_files()
    files = {
        name: sha256(ROOT.joinpath(*PurePosixPath(name).parts)) for name in names
    }
    manifest = {
        "schema": "langtons-ant-highway-artifact-manifest-v2",
        "algorithm": "SHA-256",
        "repository": "https://github.com/Atharva12456/langtons-ant-highway",
        "concept_doi": "10.5281/zenodo.21381637",
        "snapshot": "working revision 2026-07-21; not yet version-archived",
        "coverage": (
            "all tracked and non-ignored untracked repository files, excluding "
            "this self-referential manifest"
        ),
        "file_count": len(files),
        "files": files,
    }
    TARGET.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {TARGET_REL}: {len(files)} files")


if __name__ == "__main__":
    main()
