#!/usr/bin/env python3
"""Derive transparent kinematics from a private or synthetic 3D contract."""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path

try:
    from .biomechanics import derived_kinematics
except ImportError:
    from biomechanics import derived_kinematics


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        sampling_hz = float(payload["sampling_hz"])
        if sampling_hz <= 0:
            raise ValueError("sampling_hz must be positive")
        result = {
            "sampling_hz": sampling_hz,
            "source_note": "derived from the supplied contract; no reference coordinates are copied",
            **derived_kinematics(payload["landmarks"], sampling_hz),
        }
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
