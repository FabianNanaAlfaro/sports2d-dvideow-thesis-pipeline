#!/usr/bin/env python3
"""Map route-specific keypoint names into the common four-point contract."""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path


ALIASES = {
    "right": {
        "hip": ("RHip", "R_Hip", "right_hip", "rightHip", "hip"),
        "knee": ("RKnee", "R_Knee", "right_knee", "rightKnee", "knee"),
        "ankle": ("RAnkle", "R_Ankle", "right_ankle", "rightAnkle", "ankle"),
        "foot": ("RBigToe", "R_BigToe", "right_foot_index", "right_foot", "foot"),
    },
    "left": {
        "hip": ("LHip", "L_Hip", "left_hip", "leftHip", "hip"),
        "knee": ("LKnee", "L_Knee", "left_knee", "leftKnee", "knee"),
        "ankle": ("LAnkle", "L_Ankle", "left_ankle", "leftAnkle", "ankle"),
        "foot": ("LBigToe", "L_BigToe", "left_foot_index", "left_foot", "foot"),
    },
}


def point_xy(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return float(value[0]), float(value[1]), None
    if isinstance(value, dict):
        x = value.get("x_px", value.get("x"))
        y = value.get("y_px", value.get("y"))
        if x is None or y is None:
            return None
        likelihood = value.get("likelihood", value.get("visibility"))
        return float(x), float(y), None if likelihood is None else float(likelihood)
    return None


def homologate(record, side=None):
    side = side or record.get("side", "right")
    if side not in ALIASES:
        raise ValueError("side must be left or right")
    keypoints = record.get("keypoints", record.get("landmarks", {}))
    output = dict(record)
    output["side"] = side
    output["landmarks"] = []
    output.pop("keypoints", None)
    for landmark_name, aliases in ALIASES[side].items():
        raw = next((keypoints[name] for name in aliases if name in keypoints), None)
        xy = point_xy(raw)
        if xy is None:
            output["landmarks"].append({
                "landmark": landmark_name,
                "x_px": None,
                "y_px": None,
                "likelihood": None,
                "valid": False,
            })
            continue
        x, y, likelihood = xy
        output["landmarks"].append({
            "landmark": landmark_name,
            "x_px": x,
            "y_px": y,
            "likelihood": likelihood,
            "valid": True,
        })
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="one synthetic or authorized frame JSON")
    parser.add_argument("--side", choices=("left", "right"))
    parser.add_argument("--output", type=Path, help="optional output path; stdout if omitted")
    args = parser.parse_args(argv)
    try:
        source = json.loads(args.input.read_text(encoding="utf-8"))
        result = homologate(source, args.side)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
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

