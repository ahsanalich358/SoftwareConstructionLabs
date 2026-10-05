# CSE325-2026-L02-M4RB-T4

import importlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

QUALITY_BASELINE = sys.argv.pop(1) if len(sys.argv) > 1 else "A1"
grades = importlib.import_module(QUALITY_BASELINE)


class GradeTests(unittest.TestCase):

    def test_average(self):
        record = grades.StudentRecord("Ahsan", [80, 90, 100])
        self.assertEqual(grades.calculate_average(record), 90.0)

    def test_empty_grades(self):
        record = grades.StudentRecord("Ali", [])
        self.assertEqual(grades.calculate_average(record), 0.0)

    def test_grade_boundaries(self):
        cases = [
            (100, "A"),
            (90, "A"),
            (89.99, "B"),
            (80, "B"),
            (79.99, "C"),
            (70, "C"),
            (69.99, "D"),
            (60, "D"),
            (59.99, "F"),
            (0, "F"),
        ]

        for average, expected in cases:
            with self.subTest(average=average):
                self.assertEqual(
                    grades.letter_grade(average),
                    expected,
                )

    def test_csv_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "students.csv"
            path.write_text(
                "name,grade1,grade2\n"
                "Sara,80,90\n"
                "\n"
                "Ali,,\n",
                encoding="utf-8",
            )

            records = grades.load_records(str(path))

            self.assertEqual(
                [(record.name, record.grades) for record in records],
                [("Sara", [80.0, 90.0]), ("Ali", [])],
            )

    def test_report_format_and_order(self):
        records = [
            grades.StudentRecord("Sara", [80, 90]),
            grades.StudentRecord("Ali", []),
        ]
        output = io.StringIO()

        with redirect_stdout(output):
            grades.print_report(records)

        self.assertEqual(
            output.getvalue(),
            "Sara: Average = 85.00, Grade = B\n"
            "Ali: Average = 0.00, Grade = F\n",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)