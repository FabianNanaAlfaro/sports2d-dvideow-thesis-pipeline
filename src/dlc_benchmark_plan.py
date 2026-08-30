#!/usr/bin/env python3
"""Validate and expand the public five-configuration DLC benchmark plan.

The output is a run plan, not a result table. It contains placeholders instead
of paths so it can be committed safely and then applied to an authorized DLC
project elsewhere.
"""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path


EXPECTED_MODELS = ("rtmpose-s", "rtmpose-m", "rtmpose-x", "hrnet-w48", "resnet-101")
REQUIRED_PROTOCOL = (
    "annotation_count", "training_count", "validation_selection_count", "fixed_detector",
    "epochs", "batch_size", "seed", "pcutoff", "views_for_2d_stage", "trials_for_3d_stage",
    "selection_subject_groups", "selection_is_final_external_test",
)


def validate(spec):
    errors = []
    if spec.get("synthetic") is not True:
        errors.append("synthetic must be true for the public plan")
    protocol = spec.get("protocol", {})
    for field in REQUIRED_PROTOCOL:
        if field not in protocol:
            errors.append("missing protocol.{}".format(field))
    if protocol.get("fixed_detector") != "SSDLite":
        errors.append("fixed_detector must remain SSDLite")
    if protocol.get("seed") != 42:
        errors.append("seed must remain 42")
    if protocol.get("selection_is_final_external_test") is not False:
        errors.append("selection groups cannot be labelled a final external test")
    models = spec.get("models", [])
    model_ids = [model.get("id") for model in models]
    if tuple(model_ids) != EXPECTED_MODELS:
        errors.append("model order must be RTMPose-S/M/X, HRNet-W48, ResNet-101")
    if len(set(model_ids)) != len(model_ids):
        errors.append("model ids must be unique")
    if spec.get("functional_points") != ["hip", "knee", "ankle", "foot"]:
        errors.append("functional_points must match the common four-point contract")
    return errors


def expand_plan(spec):
    protocol = spec["protocol"]
    runs = []
    for model in spec["models"]:
        model_id = model["id"]
        runs.append({
            "model_id": model_id,
            "family": model["family"],
            "fixed_detector": protocol["fixed_detector"],
            "declared_steps": [
                "prepare identical subject/trial split",
                "train with the declared seed and schedule",
                "select snapshot on the 2D validation/selection partition",
                "analyze the declared 2D views",
                "adapt points without copying reference coordinates",
                "reconstruct with the common DLT contract",
                "record metrics and limitations outside this public tree",
            ],
            "private_artifacts": {
                "config_yaml": "PRIVATE_DLC_CONFIG_YAML",
                "weights": "PRIVATE_MODEL_WEIGHTS",
                "predictions": "PRIVATE_PREDICTIONS",
                "results": "PRIVATE_RESULT_TABLES",
            },
        })
    return {
        "experiment_id": spec["experiment_id"],
        "protocol": protocol,
        "model_order": list(EXPECTED_MODELS),
        "runs": runs,
        "interpretation": "descriptive configuration benchmark; not a pure architecture ablation",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--write", type=Path, help="optional output path for the expanded plan")
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    errors = validate(spec)
    if errors:
        print("FAIL: benchmark plan is invalid")
        for error in errors:
            print(" - {}".format(error))
        return 1
    plan = expand_plan(spec)
    text = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(text, encoding="utf-8")
        print("PASS: expanded five-model plan written to {}".format(args.write))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

