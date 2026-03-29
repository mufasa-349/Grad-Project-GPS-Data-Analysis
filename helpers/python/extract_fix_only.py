#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def derive_output_path(input_path: Path) -> Path:
    if input_path.suffix.lower() == ".txt":
        return input_path.with_name(f"{input_path.stem}_FixOnly.txt")
    return input_path.with_name(f"{input_path.name}_FixOnly.txt")


def extract_fix_lines(input_path: Path, output_path: Path) -> tuple[int, int]:
    read_lines = 0
    written_lines = 0

    with input_path.open("r", encoding="utf-8", errors="replace", newline="") as fin, output_path.open(
        "w", encoding="utf-8", newline="\n"
    ) as fout:
        for line in fin:
            read_lines += 1
            if line.startswith("Fix,"):
                fout.write(line.rstrip("\r\n") + "\n")
                written_lines += 1

    return read_lines, written_lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a *_FixOnly.txt file containing only lines starting with 'Fix,' from a GNSS Logger log."
    )
    parser.add_argument("input", nargs="?", help="Input GNSS log .txt file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output .txt file path (default: <input>_FixOnly.txt)",
    )
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input).expanduser()
    else:
        raw = input("Input GNSS log file path: ").strip()
        if not raw:
            raise SystemExit("No input path provided.")
        input_path = Path(raw).expanduser()

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise SystemExit(f"Input path is not a file: {input_path}")

    output_path = Path(args.output).expanduser() if args.output else derive_output_path(input_path)
    if output_path.resolve() == input_path.resolve():
        raise SystemExit("Output path must be different from input path.")

    read_lines, written_lines = extract_fix_lines(input_path, output_path)

    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(f"Read lines:    {read_lines}")
    print(f"Written Fix,:  {written_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

