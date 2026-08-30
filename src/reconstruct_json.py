#!/usr/bin/env python3
"""Run the public DLT example from a JSON contract."""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path

try:
    from .dlt import triangulate_point
    from .dlt import triangulate_trajectory
    from .quality_gate import evaluate_reconstruction, evaluate_trajectory
except ImportError:
    from dlt import triangulate_point
    from dlt import triangulate_trajectory
    from quality_gate import evaluate_reconstruction, evaluate_trajectory


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--max-reprojection-px", type=float, default=5.0)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if args.max_reprojection_px <= 0:
            raise ValueError("max-reprojection-px must be positive")
        if "frames" in payload:
            frames = triangulate_trajectory(payload["frames"], payload["projection_matrices"])
            result = {
                "projection_matrices": payload["projection_matrices"],
                "frames": evaluate_trajectory(frames, args.max_reprojection_px),
            }
        else:
            result = triangulate_point(payload["observations"], payload["projection_matrices"])
            result["quality"] = evaluate_reconstruction(result, args.max_reprojection_px)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
