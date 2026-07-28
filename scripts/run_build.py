#!/usr/bin/env python3
"""Run the bundled artifact-tool workbook builder in an isolated temp directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", required=True, help="Bundled Node.js executable")
    parser.add_argument("--node-modules", required=True, help="Bundled node_modules directory")
    parser.add_argument("--input", required=True, help="Workbook input JSON")
    parser.add_argument("--output", required=True, help="Destination .xlsx")
    parser.add_argument("--preview-dir", required=True, help="Directory for rendered PNG previews")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    node = Path(args.node).expanduser().resolve()
    node_modules = Path(args.node_modules).expanduser().resolve()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    preview_dir = Path(args.preview_dir).expanduser().resolve()
    builder_source = Path(__file__).with_name("build_lead_workbook.mjs").resolve()

    for path, label in (
        (node, "Node.js executable"),
        (node_modules, "node_modules directory"),
        (input_path, "input JSON"),
        (builder_source, "workbook builder"),
    ):
        if not path.exists():
            raise SystemExit(f"{label} not found: {path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="public-trade-leads-") as temp_name:
        temp_dir = Path(temp_name)
        builder_copy = temp_dir / builder_source.name
        shutil.copy2(builder_source, builder_copy)
        os.symlink(node_modules, temp_dir / "node_modules", target_is_directory=True)

        command = [
            str(node),
            str(builder_copy),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--preview-dir",
            str(preview_dir),
        ]
        completed = subprocess.run(command, cwd=temp_dir, check=False)
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
