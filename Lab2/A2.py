# CSE325-2026-L02-M4RB
# Activity 2: Apply the real fixes, skip the cosmetic ones

import csv
from dataclasses import dataclass
from pathlib import Path

QUALITY_BASELINE = str(Path(__file__).with_name("students.csv"))


@dataclass
class StudentRecord:
    name: str
    grades: list[float]


def load_records(path: str) -> list[StudentRecord]:
    student_records = []

    # CSV format: name,grade1,grade2,grade3
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if not row:
                continue

            grades = [
                float(value) for value in row[1:] if value.strip()
            ]
            student_records.append(StudentRecord(row[0], grades))

    return student_records


def calculate_average(record: StudentRecord) -> float:
    if not record.grades:
        return 0.0

    return sum(record.grades) / len(record.grades)


def letter_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def print_report(records: list[StudentRecord]) -> None:
    for record in records:
        average = calculate_average(record)
        grade = letter_grade(average)
        print(f"{record.name}: Average = {average:.2f}, Grade = {grade}")


if __name__ == "__main__":
    student_records = load_records(QUALITY_BASELINE)
    print_report(student_records)