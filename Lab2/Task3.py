# CSE325-2026-L02-M4RB-T3

import csv
from dataclasses import dataclass
from pathlib import Path

QUALITY_BASELINE = {
    "input_file": str(Path(__file__).with_name("students.csv")),
    "grade_boundaries": (
        (90, "A"),
        (80, "B"),
        (70, "C"),
        (60, "D"),
    ),
}


@dataclass
class StudentRecord:
    name: str
    grades: list[float]


def parse_record(row: list[str]) -> StudentRecord:
    """Convert a CSV row to a record, ignoring blank grade fields."""
    grades = [
        float(value) for value in row[1:] if value.strip()
    ]
    return StudentRecord(row[0], grades)


def load_records(path: str) -> list[StudentRecord]:
    """Read a CSV with a header; preserve row order and skip empty rows."""
    student_records = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if not row:
                continue

            student_records.append(parse_record(row))

    return student_records


def calculate_average(record: StudentRecord) -> float:
    """Return the average, or 0.0 when the student has no grades."""
    if not record.grades:
        return 0.0

    return sum(record.grades) / len(record.grades)


def letter_grade(average: float) -> str:
    """Check thresholds from highest to lowest; otherwise return F."""
    for threshold, grade in QUALITY_BASELINE["grade_boundaries"]:
        if average >= threshold:
            return grade

    return "F"


def print_report(records: list[StudentRecord]) -> None:
    """Print student results in their original order."""
    for record in records:
        average = calculate_average(record)
        grade = letter_grade(average)
        print(f"{record.name}: Average = {average:.2f}, Grade = {grade}")


if __name__ == "__main__":
    student_records = load_records(QUALITY_BASELINE["input_file"])
    print_report(student_records)