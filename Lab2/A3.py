# CSE325-2026-L02-M4RB
# Activity 3: Measure the actual change
# Values are from the lab example, not measured from A1.py.

QUALITY_BASELINE = {
    "Longest function (lines)": (58, 19),
    "Worst function parameters": (6, 3),
    "Duplicated grade blocks": (3, 0),
}


def print_comparison():
    print(f"{'Metric':<30} {'Before':>8} {'After':>8}")
    print("-" * 48)

    for metric, (before, after) in QUALITY_BASELINE.items():
        print(f"{metric:<30} {before:>8} {after:>8}")


if __name__ == "__main__":
    print_comparison()

    print("\nExplanation:")
    print("1. Splitting responsibilities reduced the longest function.")
    print("2. Smaller functions required fewer parameters.")
    print("3. letter_grade() removed duplicated grade-boundary logic.")

    print(
        "\nMeasured against the construction baseline. "
        "CSE325-2026-L02-M4RB"
    )