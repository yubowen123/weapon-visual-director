#!/usr/bin/env python3
"""Validate the final three-model weapon prompt package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def require_object(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_list(parent: dict[str, Any], key: str, errors: list[str], minimum: int = 1) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{key} must be a list with at least {minimum} item(s)")
        return []
    return value


def require_text(parent: dict[str, Any], key: str, errors: list[str]) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be non-empty text")
        return ""
    return value.strip()


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["top-level JSON must be an object"], warnings

    reference = require_object(data, "selected_reference", errors)
    require_text(reference, "id", errors)
    image_ref = reference.get("image_url") or reference.get("asset_path")
    if not isinstance(image_ref, str) or not image_ref.strip():
        errors.append("selected_reference requires image_url or asset_path")
    require_text(reference, "landing_url", errors)
    require_text(reference, "source", errors)
    require_text(reference, "license", errors)
    if reference.get("license_verified") is not True:
        warnings.append("selected reference license is not verified")

    design = require_object(data, "design", errors)
    preserve = require_list(design, "preserve", errors, 2)
    change = require_list(design, "change", errors, 1)
    avoid = require_list(design, "avoid", errors, 1)
    if normalized := ({str(x).casefold().strip() for x in preserve} & {str(x).casefold().strip() for x in change}):
        errors.append(f"preserve/change conflict: {sorted(normalized)}")
    if not avoid:
        errors.append("design.avoid cannot be empty")

    prompts = require_object(data, "prompts", errors)
    mj = require_object(prompts, "midjourney", errors)
    nano = require_object(prompts, "nano_banana_pro", errors)
    gpt = require_object(prompts, "gpt_image_2", errors)
    mj_prompt = require_text(mj, "prompt", errors)
    nano_prompt = require_text(nano, "prompt", errors)
    gpt_prompt = require_text(gpt, "prompt", errors)

    if mj_prompt:
        if "--v 8.1" not in mj_prompt:
            warnings.append("Midjourney prompt does not declare --v 8.1")
        last_parameter = mj_prompt.rfind("--")
        if last_parameter < 0:
            errors.append("Midjourney prompt requires trailing parameters")
        elif re.search(r"\b(change|preserve|constraints)\s*:", mj_prompt[:last_parameter], re.I):
            warnings.append("Midjourney prompt looks like an edit checklist instead of a final visual description")

    if nano_prompt:
        for heading in ("Preserve:", "Change:", "Composition:", "Constraints:"):
            if heading.casefold() not in nano_prompt.casefold():
                errors.append(f"Nano Banana Pro prompt missing heading: {heading}")
        if "image 1" not in nano_prompt.casefold():
            errors.append("Nano Banana Pro prompt must assign Image 1")

    card = require_object(gpt, "display_text", errors)
    title = require_text(card, "title", errors)
    subtitle = require_text(card, "subtitle", errors)
    labels = require_list(card, "detail_labels", errors, 3)
    description = require_text(card, "description", errors)
    if len(labels) != 3:
        errors.append("GPT Image 2 detail_labels must contain exactly 3 items")
    if len(title) > 8:
        errors.append("GPT Image 2 Chinese title exceeds 8 characters")
    if len(subtitle) > 12:
        errors.append("GPT Image 2 Chinese subtitle exceeds 12 characters")
    for index, label in enumerate(labels, start=1):
        if not isinstance(label, str) or not label.strip() or len(label.strip()) > 8:
            errors.append(f"GPT Image 2 detail label {index} must be 1-8 characters")
    if len(description) > 80:
        errors.append("GPT Image 2 description exceeds 80 characters")
    elif description and len(description) < 20:
        warnings.append("GPT Image 2 description is very short")

    if gpt_prompt:
        for text in [title, subtitle, description, *[str(x) for x in labels]]:
            if text and text not in gpt_prompt:
                errors.append(f"GPT Image 2 prompt does not contain exact display text: {text}")
        if "detail panel" not in gpt_prompt.casefold():
            errors.append("GPT Image 2 card prompt must request detail panels")
        if "do not add any other text" not in gpt_prompt.casefold():
            errors.append("GPT Image 2 card prompt must forbid additional text")

    compact = lambda text: re.sub(r"\s+", " ", text.casefold()).strip()
    if mj_prompt and nano_prompt and compact(mj_prompt) == compact(nano_prompt):
        errors.append("Midjourney and Nano Banana Pro prompts are identical")
    if nano_prompt and gpt_prompt and compact(nano_prompt) == compact(gpt_prompt):
        errors.append("Nano Banana Pro and GPT Image 2 prompts are identical")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    try:
        errors, warnings = validate(args.package)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Prompt package is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
