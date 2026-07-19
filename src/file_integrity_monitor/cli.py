from __future__ import annotations

import argparse
import json
from pathlib import Path

from .monitor import build_baseline, compare_baseline


def main() -> None:
    parser = argparse.ArgumentParser(description="File integrity monitor")
    sub = parser.add_subparsers(dest="command", required=True)

    baseline_cmd = sub.add_parser("baseline")
    baseline_cmd.add_argument("directory", type=Path)
    baseline_cmd.add_argument("baseline_file", type=Path)

    check_cmd = sub.add_parser("check")
    check_cmd.add_argument("directory", type=Path)
    check_cmd.add_argument("baseline_file", type=Path)
    check_cmd.add_argument("--report", type=Path, default=Path("integrity-report.json"))

    args = parser.parse_args()

    if not args.directory.is_dir():
        raise SystemExit(f"Directory not found: {args.directory}")

    if args.command == "baseline":
        data = build_baseline(args.directory, ignored_names={".git", "__pycache__"})
        args.baseline_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Baseline created for {len(data)} files")
        return

    baseline = json.loads(args.baseline_file.read_text(encoding="utf-8"))
    current = build_baseline(args.directory, ignored_names={".git", "__pycache__"})
    report = compare_baseline(current, baseline)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    changes = sum(len(v) for v in report.values())
    print(f"Integrity check completed. Changes: {changes}")


if __name__ == "__main__":
    main()
