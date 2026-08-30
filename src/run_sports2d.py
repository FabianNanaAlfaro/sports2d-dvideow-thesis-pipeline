#!/usr/bin/env python3
"""Render and optionally execute the public Sports2D thesis configuration.

The default is a dry run. Real videos and generated outputs must live outside
the public repository. The wrapper calls the official ``sports2d`` executable
without a shell so paths are not interpolated into a command string.
"""

from __future__ import print_function

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = REPO_ROOT / "configs" / "sports2d.thesis.toml"


def toml_string(path):
    """Return a portable single-quoted TOML string for a filesystem path."""
    return path.resolve().as_posix().replace("'", "''")


def render_config(template, video, result_dir):
    text = template.read_text(encoding="utf-8")
    return text.replace("__VIDEO_INPUT__", toml_string(video)).replace(
        "__RESULT_DIR__", toml_string(result_dir)
    )


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True, help="authorized input video; keep it outside this repository")
    parser.add_argument("--output-dir", type=Path, required=True, help="private output directory for Sports2D artifacts")
    parser.add_argument("--config-template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--execute", action="store_true", help="invoke the installed sports2d executable")
    parser.add_argument("--keep-config", action="store_true", help="retain the generated config in the output directory")
    parser.add_argument("--print-config", action="store_true", help="print the rendered TOML in dry-run mode")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.config_template.is_file():
        print("FAIL: template not found: {}".format(args.config_template), file=sys.stderr)
        return 2
    if args.execute and not args.video.is_file():
        print("FAIL: input video does not exist: {}".format(args.video), file=sys.stderr)
        return 2

    rendered = render_config(args.config_template, args.video, args.output_dir)
    command = ["sports2d", "--config", str(args.output_dir / "sports2d.generated.toml")]
    print("Sports2D route: Body_with_feet / Halpe-26 · balanced · pixel-space output")
    print("Command: {}".format(" ".join(command)))

    if not args.execute:
        print("DRY RUN: no video was opened and no output was written")
        if args.print_config:
            print("--- rendered config ---")
            print(rendered)
        return 0

    executable = shutil.which("sports2d")
    if executable is None:
        print("FAIL: sports2d is not installed in the active environment", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = args.output_dir / "sports2d.generated.toml"
    generated.write_text(rendered, encoding="utf-8")
    try:
        subprocess.run([executable, "--config", str(generated)], check=True)
    finally:
        if not args.keep_config and generated.exists():
            generated.unlink()
    print("PASS: Sports2D completed; inspect the private output directory and manifest it separately")
    return 0


if __name__ == "__main__":
    sys.exit(main())

