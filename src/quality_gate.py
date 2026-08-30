#!/usr/bin/env python3
"""Explicit acceptance gates for public DLT outputs."""

from __future__ import print_function

import math


def evaluate_reconstruction(reconstruction, max_reprojection_error_px=5.0):
    """Return an auditable accept/reject decision for one 3D point."""
    reasons = []
    xyz = reconstruction.get("xyz", [])
    if len(xyz) != 3 or not all(math.isfinite(float(value)) for value in xyz):
        reasons.append("xyz is not a finite three-dimensional point")
    cameras = reconstruction.get("cameras", [])
    if len(cameras) < 2:
        reasons.append("fewer than two camera observations")
    error = reconstruction.get("max_reprojection_error_px")
    if error is None or not math.isfinite(float(error)):
        reasons.append("missing or non-finite reprojection error")
    elif float(error) > max_reprojection_error_px:
        reasons.append("max reprojection error exceeds {:.3f} px".format(max_reprojection_error_px))
    return {
        "accepted": not reasons,
        "threshold_max_reprojection_error_px": float(max_reprojection_error_px),
        "reasons": reasons,
    }


def evaluate_trajectory(frames, max_reprojection_error_px=5.0):
    """Add a quality decision to each successful trajectory frame."""
    output = []
    for frame in frames:
        item = dict(frame)
        if frame.get("status") != "ok":
            item["quality"] = {"accepted": False, "reasons": [frame.get("reason", "invalid frame")]}
        else:
            item["quality"] = evaluate_reconstruction(frame, max_reprojection_error_px)
        output.append(item)
    return output
