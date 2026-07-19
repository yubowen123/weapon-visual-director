#!/usr/bin/env python3
"""Validate weapon visual test definitions and their registered artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_text(item: dict[str, Any], key: str, where: str, errors: list[str]) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}.{key} must be non-empty text")
        return ""
    return value.strip()


def validate(definition_path: Path) -> list[str]:
    errors: list[str] = []
    root = definition_path.parent.parent
    data = load_object(definition_path)
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["cases must be a non-empty list"]

    seen: set[str] = set()
    for index, case in enumerate(cases, start=1):
        where = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{where} must be an object")
            continue
        case_id = require_text(case, "id", where, errors)
        if case_id in seen:
            errors.append(f"duplicate case id: {case_id}")
        seen.add(case_id)
        require_text(case, "input", where, errors)
        expected = case.get("expected_checks")
        if not isinstance(expected, list) or not expected:
            errors.append(f"{where}.expected_checks must be a non-empty list")

        fixture_value = case.get("fixture")
        if not fixture_value:
            continue
        fixture_path = root / str(fixture_value)
        if not fixture_path.is_file():
            errors.append(f"{where}.fixture not found: {fixture_value}")
            continue
        fixture = load_object(fixture_path)
        if fixture.get("case_id") != case_id:
            errors.append(f"{fixture_value}: case_id does not match {case_id}")
        artifacts = fixture.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f"{fixture_value}: artifacts must be a non-empty list")
            continue
        for artifact_index, artifact in enumerate(artifacts, start=1):
            artifact_where = f"{fixture_value}.artifacts[{artifact_index}]"
            if not isinstance(artifact, dict):
                errors.append(f"{artifact_where} must be an object")
                continue
            path_value = require_text(artifact, "path", artifact_where, errors)
            role = require_text(artifact, "role", artifact_where, errors)
            require_text(artifact, "model", artifact_where, errors)
            file_path = root / path_value
            if not file_path.is_file():
                errors.append(f"{artifact_where}.path not found: {path_value}")
                continue
            expected_hash = require_text(artifact, "sha256", artifact_where, errors)
            if expected_hash and sha256(file_path) != expected_hash:
                errors.append(f"{artifact_where}.sha256 mismatch: {path_value}")
            if role == "negative_fixture" and not artifact.get("expected_issues"):
                errors.append(f"{artifact_where} negative fixture requires expected_issues")
            if role in {"positive_fixture", "recommended_output"} and not artifact.get("expected_checks"):
                errors.append(f"{artifact_where} positive artifact requires expected_checks")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("definition", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(args.definition.resolve())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Visual test set is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
