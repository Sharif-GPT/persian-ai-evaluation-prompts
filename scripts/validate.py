#!/usr/bin/env python3
"""Validate the Persian prompt JSONL dataset with no third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "prompts.fa.jsonl"

CATEGORIES = {
    "instruction-following",
    "writing-editing",
    "information-literacy",
    "structured-data",
    "localization",
    "safety-privacy",
    "customer-support",
    "reasoning-planning",
}

DIMENSIONS = {
    "instruction_following",
    "persian_language_quality",
    "factual_caution",
    "ambiguity_handling",
    "reasoning_transparency",
    "format_fidelity",
    "safety",
    "privacy",
    "localization",
    "calibration",
}

REQUIRED_FIELDS = {
    "id",
    "version",
    "language",
    "category",
    "title",
    "prompt",
    "context",
    "evaluation_dimensions",
    "review_criteria",
    "failure_modes",
    "risk_level",
    "tags",
}

ID_RE = re.compile(r"^fa-[a-z0-9-]+-[0-9]{3}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
TAG_RE = re.compile(r"^[a-z0-9-]+$")
FORBIDDEN_FIELDS = {
    "answer",
    "expected_answer",
    "model_answer",
    "model_output",
    "result",
    "score",
    "ranking",
    "winner",
}


def _string_list(value: Any, minimum: int, min_item_length: int = 1) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(
            isinstance(item, str) and len(item.strip()) >= min_item_length
            for item in value
        )
    )


def validate_record(record: Any, line_number: int) -> list[str]:
    """Return human-readable errors for one parsed JSON value."""
    prefix = f"line {line_number}"
    if not isinstance(record, dict):
        return [f"{prefix}: record must be a JSON object"]

    errors: list[str] = []
    fields = set(record)
    missing = REQUIRED_FIELDS - fields
    extra = fields - REQUIRED_FIELDS
    if missing:
        errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{prefix}: unsupported fields: {', '.join(sorted(extra))}")
    forbidden = fields & FORBIDDEN_FIELDS
    if forbidden:
        errors.append(f"{prefix}: result/answer fields are forbidden: {', '.join(sorted(forbidden))}")

    record_id = record.get("id")
    if not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
        errors.append(f"{prefix}: id has an invalid format")
    version = record.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        errors.append(f"{prefix}: version must use semantic x.y.z form")
    if record.get("language") != "fa-IR":
        errors.append(f"{prefix}: language must be fa-IR")
    if record.get("category") not in CATEGORIES:
        errors.append(f"{prefix}: category is not recognized")

    for field, minimum, maximum in (
        ("title", 8, 120),
        ("prompt", 40, 3000),
        ("context", 1, 1000),
    ):
        value = record.get(field)
        if not isinstance(value, str) or len(value.strip()) < minimum:
            errors.append(f"{prefix}: {field} must be a string of at least {minimum} characters")
        elif len(value) > maximum:
            errors.append(f"{prefix}: {field} must contain no more than {maximum} characters")

    dimensions = record.get("evaluation_dimensions")
    if not _string_list(dimensions, 2):
        errors.append(f"{prefix}: evaluation_dimensions must contain at least two strings")
    elif len(set(dimensions)) != len(dimensions):
        errors.append(f"{prefix}: evaluation_dimensions contains duplicates")
    elif unknown := set(dimensions) - DIMENSIONS:
        errors.append(f"{prefix}: unknown dimensions: {', '.join(sorted(unknown))}")

    for field, minimum in (("review_criteria", 2), ("failure_modes", 1)):
        value = record.get(field)
        if not _string_list(value, minimum, min_item_length=8):
            errors.append(
                f"{prefix}: {field} must contain at least {minimum} strings "
                "of at least 8 characters"
            )

    if record.get("risk_level") not in {"low", "medium", "high"}:
        errors.append(f"{prefix}: risk_level must be low, medium, or high")

    tags = record.get("tags")
    if not _string_list(tags, 1):
        errors.append(f"{prefix}: tags must contain at least one string")
    elif len(set(tags)) != len(tags):
        errors.append(f"{prefix}: tags contains duplicates")
    elif any(not TAG_RE.fullmatch(tag) for tag in tags):
        errors.append(f"{prefix}: tags must contain lowercase ASCII slugs")

    return errors


def validate_file(path: Path) -> tuple[int, list[str]]:
    """Validate a JSONL file and return (record_count, errors)."""
    errors: list[str] = []
    ids: dict[str, int] = {}
    categories: set[str] = set()
    count = 0

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return 0, [f"cannot read {path}: {exc}"]

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            errors.append(f"line {line_number}: blank lines are not allowed in JSONL")
            continue
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON ({exc.msg})")
            continue

        count += 1
        errors.extend(validate_record(record, line_number))
        if isinstance(record, dict):
            record_id = record.get("id")
            if isinstance(record_id, str):
                if record_id in ids:
                    errors.append(
                        f"line {line_number}: duplicate id {record_id!r}; first seen on line {ids[record_id]}"
                    )
                else:
                    ids[record_id] = line_number
            category = record.get("category")
            if category in CATEGORIES:
                categories.add(category)

    if count == 0:
        errors.append("dataset contains no records")
    missing_categories = CATEGORIES - categories
    if missing_categories:
        errors.append(f"dataset is missing categories: {', '.join(sorted(missing_categories))}")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    count, errors = validate_file(args.path)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {count} records from {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
