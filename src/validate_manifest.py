#!/usr/bin/env python3
"""Validate the public, synthetic pipeline manifest.

This utility intentionally validates metadata only. It never opens research data.
"""

from __future__ import print_function

import json
import re
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {"schema_version", "project", "release", "study_design", "stages", "example_trial"}
REQUIRED_STAGE = {"id", "name", "input_contract", "output_contract", "public_boundary"}
EXPECTED_STAGE_IDS = ["S{:02d}".format(index) for index in range(9)]
PRIVATE_TEXT_PATTERNS = [
    re.compile(r"(?i)\b[a-z]:[\\/][^\s]+"),
    re.compile(r"(?i)\b(?:/users/|/home/|/mnt/)[^\s]+"),
    re.compile(r"(?i)\b[^\s]+@[^\s]+\.[a-z]{2,}\b"),
]


def fail(message):
    print("FAIL: {}".format(message))
    return 1


def validate(path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail("cannot read JSON: {}".format(exc))

    if not isinstance(payload, dict):
        return fail("manifest root must be an object")

    missing = sorted(REQUIRED_TOP_LEVEL.difference(payload))
    if missing:
        return fail("missing top-level fields: {}".format(", ".join(missing)))

    release = payload["release"]
    if release.get("synthetic") is not True:
        return fail("public manifest must set release.synthetic=true")
    for field in ("contains_participant_data", "contains_frame_level_observations", "contains_results"):
        if release.get(field) is not False:
            return fail("release.{} must be false".format(field))

    design = payload["study_design"]
    if design.get("sampling_hz") != 240:
        return fail("study_design.sampling_hz must preserve the declared 240 Hz contract")
    if design.get("camera_roles") != ["CAM_1", "CAM_2"]:
        return fail("camera roles must be CAM_1 and CAM_2 in that order")
    if design.get("normalized_window_points") != 101:
        return fail("normalized window must declare 101 points")
    if design.get("landmarks") != ["hip", "knee", "ankle", "foot"]:
        return fail("landmark vocabulary must be hip/knee/ankle/foot")

    stages = payload["stages"]
    if not isinstance(stages, list) or len(stages) != len(EXPECTED_STAGE_IDS):
        return fail("manifest must contain exactly nine stages S00-S08")
    stage_ids = []
    for stage in stages:
        if not isinstance(stage, dict):
            return fail("each stage must be an object")
        missing_stage = sorted(REQUIRED_STAGE.difference(stage))
        if missing_stage:
            return fail("stage is missing: {}".format(", ".join(missing_stage)))
        stage_ids.append(stage["id"])
    if stage_ids != EXPECTED_STAGE_IDS:
        return fail("stage order must be S00, S01, ..., S08")

    serialized = json.dumps(payload, ensure_ascii=False)
    for pattern in PRIVATE_TEXT_PATTERNS:
        if pattern.search(serialized):
            return fail("manifest contains a private path or contact-like value")

    example = payload["example_trial"]
    if example.get("trial_id") != "trial-demo-001" or example.get("side") not in ("left", "right"):
        return fail("example_trial must use a synthetic trial id and a valid side")
    cameras = [view.get("camera_role") for view in example.get("views", [])]
    if cameras != ["CAM_1", "CAM_2"]:
        return fail("example trial must expose exactly one CAM_1 and one CAM_2 view")

    print("PASS: public manifest is complete, synthetic and contract-compatible")
    print("      stages={} landmarks={} camera_pair={} window_points={}".format(
        len(stages), ",".join(design["landmarks"]), "+".join(design["camera_roles"]), design["normalized_window_points"]
    ))
    return 0


def main(argv):
    if len(argv) != 2:
        print("Usage: python src/validate_manifest.py examples/manifest.example.json")
        return 2
    return validate(Path(argv[1]))


if __name__ == "__main__":
    sys.exit(main(sys.argv))

