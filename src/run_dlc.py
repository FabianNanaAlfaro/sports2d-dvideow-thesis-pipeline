#!/usr/bin/env python3
"""Safe entry point for optional DeepLabCut analysis/training.

Without ``--execute`` this prints the intended action and touches nothing.
The real config YAML, videos and outputs must remain outside this repository.
"""

from __future__ import print_function

import argparse
import json
import shutil
import sys
from pathlib import Path


def run(action, config_yaml, videos, output_dir, shuffle, maxiters):
    try:
        import deeplabcut
    except ImportError as exc:
        raise RuntimeError("install DeepLabCut in the private environment first") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    if action == "analyze":
        deeplabcut.analyze_videos(
            str(config_yaml),
            [str(video) for video in videos],
            shuffle=shuffle,
            save_as_csv=True,
            destfolder=str(output_dir),
        )
        return

    deeplabcut.create_training_dataset(str(config_yaml), num_shuffles=1)
    deeplabcut.train_network(
        str(config_yaml),
        shuffle=shuffle,
        maxiters=maxiters,
        allow_growth=True,
    )
    deeplabcut.evaluate_network(
        str(config_yaml),
        Shuffles=[shuffle],
        plotting=False,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action", choices=("analyze", "train"), default="analyze")
    parser.add_argument("--config-yaml", type=Path, required=True)
    parser.add_argument("--video", type=Path, action="append", default=[])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--shuffle", type=int, default=1)
    parser.add_argument("--maxiters", type=int, default=35000)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)

    summary = {
        "action": args.action,
        "config_yaml": "PRIVATE_DLC_CONFIG_YAML",
        "videos": len(args.video),
        "output_dir": "PRIVATE_DLC_OUTPUT_DIR",
        "shuffle": args.shuffle,
        "maxiters": args.maxiters,
    }
    print(json.dumps(summary, indent=2))
    if not args.execute:
        print("DRY RUN: no DeepLabCut module was imported and no file was written")
        return 0
    if not args.config_yaml.is_file():
        print("FAIL: config YAML not found", file=sys.stderr)
        return 2
    if args.action == "analyze" and not args.video:
        print("FAIL: analyze requires at least one --video", file=sys.stderr)
        return 2
    if shutil.which("python") is None:
        print("FAIL: active Python executable is unavailable", file=sys.stderr)
        return 2
    try:
        run(args.action, args.config_yaml, args.video, args.output_dir, args.shuffle, args.maxiters)
    except (RuntimeError, OSError, ValueError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    print("PASS: DeepLabCut action completed in the private output directory")
    return 0


if __name__ == "__main__":
    sys.exit(main())

