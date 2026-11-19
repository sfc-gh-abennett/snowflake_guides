"""Local checks for WORKED-EXAMPLE.md; not a Snowflake compiler or Agent evaluation.

Pair-programmed by SE Community + Cortex Code

Conventions the worked example follows (all names and data synthetic):
  <!-- fixture: TABLE -->   then a ```csv block   -> loaded into in-memory SQLite as TABLE
  <!-- example: NAME -->    then a ```yaml/json/sql block -> parsed (YAML rejects duplicate keys)
  <!-- check: NAME -->      then a ```sql block   -> portable SQL run against the fixtures
  <!-- expect: NAME -->     then a ```csv block   -> the exact rows the check must return

Run: uv run --with pyyaml --with pytest pytest tests -q
"""

import csv
import io
import json
import re
import sqlite3
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = (ROOT / "WORKED-EXAMPLE.md").read_text(encoding="utf-8")
BLOCK = r"<!-- {kind}: ([A-Za-z0-9_.-]+) -->\s*\n```({lang})\n(.*?)\n```"


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently accepting overwritten config."""


def _unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def blocks(kind, lang=r"[a-z]+"):
    found = re.findall(BLOCK.format(kind=kind, lang=lang), DOCUMENT, re.DOTALL)
    names = [name for name, _, _ in found]
    duplicates = {n for n in names if names.count(n) > 1}
    if duplicates:
        raise AssertionError(f"Duplicate {kind} names: {sorted(duplicates)}")
    return {name: (language, body) for name, language, body in found}


def typed(value):
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    return None if value == "" else value


def same(actual, expected):
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return abs(actual - expected) < 0.005
    return str(actual) == str(expected)


class WorkedExampleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = sqlite3.connect(":memory:")
        cls.fixtures = blocks("fixture", "csv")
        for table, (_, body) in cls.fixtures.items():
            rows = list(csv.reader(io.StringIO(body)))
            header, data = rows[0], rows[1:]
            cls.db.execute(f'CREATE TABLE "{table}" ({", ".join(f"{c} " for c in header)})')
            cls.db.executemany(f'INSERT INTO "{table}" VALUES ({", ".join("?" * len(header))})',
                               [[typed(v) for v in row] for row in data])

    def test_has_fixture_and_checks(self):
        self.assertTrue(self.fixtures, "Worked example needs at least one <!-- fixture: --> csv block")
        self.assertTrue(blocks("check", "sql"), "Worked example needs at least one <!-- check: --> sql block")

    def test_example_blocks_parse(self):
        for name, (language, body) in blocks("example").items():
            with self.subTest(example=name):
                if language in ("yaml", "yml"):
                    self.assertIsNotNone(yaml.load(body, Loader=UniqueLoader))  # nosec B506
                elif language == "json":
                    json.loads(body)
                self.assertNotRegex(body, r"\{\{[A-Z0-9_]+\}\}", "unfilled template placeholder")

    def test_checks_and_expectations_pair(self):
        self.assertEqual(set(blocks("check", "sql")), set(blocks("expect", "csv")),
                         "Every check needs exactly one expect block with the same name")

    def test_checks_return_expected_rows(self):
        expects = blocks("expect", "csv")
        for name, (_, sql) in blocks("check", "sql").items():
            with self.subTest(check=name):
                cursor = self.db.execute(sql)
                header = [d[0].upper() for d in cursor.description]
                actual = cursor.fetchall()
                rows = list(csv.reader(io.StringIO(expects[name][1])))
                self.assertEqual(header, [c.upper() for c in rows[0]], "column names differ")
                expected = [[typed(v) for v in row] for row in rows[1:]]
                self.assertEqual(len(actual), len(expected), "row count differs")
                for got, want in zip(actual, expected):
                    self.assertTrue(all(same(a, e) for a, e in zip(got, want)), f"{got} != {want}")


if __name__ == "__main__":
    unittest.main()
