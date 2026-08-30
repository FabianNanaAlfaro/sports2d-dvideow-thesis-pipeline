#!/usr/bin/env python3
"""Normalize a valid time series to the declared 101-point window."""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path

import numpy as np


def normalize_series(frame_index, values, points=101):
    if points < 1:
        raise ValueError("points must be a positive integer")
    frames = np.asarray(frame_index, dtype=float)
    series = np.asarray([np.nan if value is None else float(value) for value in values], dtype=float)
    if frames.shape != series.shape:
        raise ValueError("frame_index and each series must have the same length")
    valid = np.isfinite(frames) & np.isfinite(series)
    if valid.sum() < 2:
        return [None] * points
    source_frames = frames[valid]
    source_values = series[valid]
    if np.any(np.diff(source_frames) <= 0):
        raise ValueError("valid frame_index values must be strictly increasing")
    target = np.linspace(source_frames[0], source_frames[-1], points)
    normalized = np.interp(target, source_frames, source_values)
    return [None if not np.isfinite(value) else float(value) for value in normalized]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--points", type=int, default=101)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = {
            name: normalize_series(payload["frame_index"], values, args.points)
            for name, values in payload["series"].items()
        }
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    text = json.dumps({"points": args.points, "series": result}, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
