from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import DEFAULT_DATA, validate_file, validate_record  # noqa: E402


def valid_record() -> dict:
    return {
        "id": "fa-test-case-001",
        "version": "1.0.0",
        "language": "fa-IR",
        "category": "instruction-following",
        "title": "یک عنوان فارسی معتبر",
        "prompt": "این یک پرامپت آزمایشی فارسی با طول کافی برای اعتبارسنجی ساختار داده است.",
        "context": "سناریوی ساختگی برای آزمون واحد.",
        "evaluation_dimensions": ["instruction_following", "persian_language_quality"],
        "review_criteria": ["رعایت دقیق محدودیت خواسته‌شده", "استفاده از فارسی طبیعی و روشن"],
        "failure_modes": ["نادیده گرفتن محدودیت اصلی پرامپت"],
        "risk_level": "low",
        "tags": ["unit-test"],
    }


class RecordValidationTests(unittest.TestCase):
    def test_valid_record_passes(self) -> None:
        self.assertEqual(validate_record(valid_record(), 1), [])

    def test_answer_field_is_rejected(self) -> None:
        record = valid_record()
        record["expected_answer"] = "نباید در داده باشد"
        errors = validate_record(record, 1)
        self.assertTrue(any("forbidden" in error for error in errors))

    def test_unknown_dimension_is_rejected(self) -> None:
        record = valid_record()
        record["evaluation_dimensions"] = ["instruction_following", "brand_preference"]
        errors = validate_record(record, 1)
        self.assertTrue(any("unknown dimensions" in error for error in errors))

    def test_schema_length_boundaries_are_enforced(self) -> None:
        invalid_values = {
            "title": "ف" * 121,
            "prompt": "ف" * 3001,
            "context": "ف" * 1001,
            "review_criteria": ["کوتاه", "معیار معتبر و کافی"],
            "failure_modes": ["کوتاه"],
        }

        for field, value in invalid_values.items():
            with self.subTest(field=field):
                record = valid_record()
                record[field] = value
                errors = validate_record(record, 1)
                self.assertTrue(any(field in error for error in errors), errors)


class DatasetValidationTests(unittest.TestCase):
    def test_repository_dataset_passes(self) -> None:
        count, errors = validate_file(DEFAULT_DATA)
        self.assertGreaterEqual(count, 24)
        self.assertEqual(errors, [])

    def test_duplicate_ids_are_rejected(self) -> None:
        records = []
        for index, category in enumerate(
            [
                "instruction-following",
                "writing-editing",
                "information-literacy",
                "structured-data",
                "localization",
                "safety-privacy",
                "customer-support",
                "reasoning-planning",
            ]
        ):
            record = valid_record()
            record["id"] = "fa-test-dup-001" if index < 2 else f"fa-test-case-{index:03d}"
            record["category"] = category
            records.append(record)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.jsonl"
            path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in records),
                encoding="utf-8",
            )
            _, errors = validate_file(path)
        self.assertTrue(any("duplicate id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
