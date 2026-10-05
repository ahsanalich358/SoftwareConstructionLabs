# CSE325-2026-L02-M4RB-T1
import ast
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
QUALITY_BASELINE = Path(__file__).with_name("A1.py")
def run_tool(arguments, output_path, allowed_codes):
    result = subprocess.run(
        [sys.executable, "-m", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    output_path.write_text(result.stdout, encoding="utf-8")
    if result.returncode not in allowed_codes:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)
def main():
    if not QUALITY_BASELINE.is_file():
        raise SystemExit("Keep Task1.py and A1.py in the same folder.")

    folder = QUALITY_BASELINE.parent / "baseline"
    folder.mkdir(exist_ok=True)

    violations = run_tool(
        [
            "ruff", "check",
            "--isolated",
            "--select", "E,F,B,S,UP,RUF",
            "--output-format", "json",
            str(QUALITY_BASELINE),
        ],
        folder / "ruff_output.json",
        allowed_codes=(0, 1),
    )

    complexity_data = run_tool(
        ["radon", "cc", "-j", str(QUALITY_BASELINE)],
        folder / "radon_output.json",
        allowed_codes=(0,),
    )

    tree = ast.parse(
        QUALITY_BASELINE.read_text(encoding="utf-8-sig")
    )

    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    longest = max(
        functions,
        key=lambda node: node.end_lineno - node.lineno + 1,
    )

    # Measure the module-level functions in this grade program.
    complexity_functions = [
        block
        for blocks in complexity_data.values()
        for block in blocks
        if block["type"] == "function"
    ]

    worst = max(
        complexity_functions,
        key=lambda block: block["complexity"],
    )
    worst_node = next(
        node for node in functions
        if node.lineno == worst["lineno"]
    )
    arguments = worst_node.args
    parameter_count = (
        len(arguments.posonlyargs)
        + len(arguments.args)
        + len(arguments.kwonlyargs)
        + int(arguments.vararg is not None)
        + int(arguments.kwarg is not None)
    )
    counts = Counter(item["code"] for item in violations)
    report = "\n".join([
        f"File: {QUALITY_BASELINE.name}",
        f"Violations by code: {dict(sorted(counts.items()))}",
        f"Total violations: {len(violations)}",
        f"Longest function: {longest.name}",
        (
            "Longest function lines: "
            f"{longest.end_lineno - longest.lineno + 1}"
        ),
        f"Highest complexity: {worst['complexity']}",
        f"Worst function: {worst['name']}",
        f"Worst function parameters: {parameter_count}",
        "",
        "Measured against the construction baseline.",
        "CSE325-2026-L02-M4RB CSE325-2026-L02-M4RB-T1",
    ])
    (folder / "baseline.txt").write_text(report, encoding="utf-8")
    print(report)
if __name__ == "__main__":
    main()