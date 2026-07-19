from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_baseline(root: Path, ignored_names: Iterable[str] = ()) -> dict[str, str]:
    root = root.resolve()
    ignored = set(ignored_names)
    baseline: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in ignored for part in path.parts):
            relative = path.relative_to(root).as_posix()
            baseline[relative] = sha256_file(path)
    return baseline


def compare_baseline(
    current: dict[str, str],
    baseline: dict[str, str],
) -> dict[str, list[str]]:
    current_keys = set(current)
    baseline_keys = set(baseline)

    added = sorted(current_keys - baseline_keys)
    deleted = sorted(baseline_keys - current_keys)
    modified = sorted(
        key
        for key in current_keys & baseline_keys
        if current[key] != baseline[key]
    )
    return {"added": added, "modified": modified, "deleted": deleted}
