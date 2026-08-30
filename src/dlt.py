#!/usr/bin/env python3
"""Small, explicit two-view DLT triangulation core.

The implementation uses NumPy for the SVD and accepts projection matrices
directly. Real calibration coefficients remain outside this repository.
"""

from __future__ import print_function

import numpy as np


def projection_matrix_from_dlt(coefficients):
    """Build a 3x4 projection matrix from 11 legacy DLT coefficients."""
    values = np.asarray(coefficients, dtype=float).reshape(-1)
    if values.size != 11:
        raise ValueError("a classical DLT projection needs exactly 11 coefficients")
    return np.array([
        [values[0], values[1], values[2], values[3]],
        [values[4], values[5], values[6], values[7]],
        [values[8], values[9], values[10], 1.0],
    ], dtype=float)


def project_point(projection_matrix, xyz):
    matrix = np.asarray(projection_matrix, dtype=float).reshape(3, 4)
    point = np.r_[np.asarray(xyz, dtype=float).reshape(3), 1.0]
    projected = matrix.dot(point)
    if abs(projected[2]) < 1e-12:
        raise ValueError("point projects at infinity")
    return projected[:2] / projected[2]


def triangulate_point(observations, projection_matrices):
    """Triangulate one point from two or more camera observations.

    Parameters are dictionaries keyed by the same semantic camera role, e.g.
    ``CAM_1`` and ``CAM_2``. The return value includes reprojection error so a
    caller can enforce a quality gate before deriving biomechanics.
    """
    cameras = [name for name in projection_matrices if name in observations]
    if len(cameras) < 2:
        raise ValueError("at least two camera observations are required")
    rows = []
    for camera in cameras:
        matrix = np.asarray(projection_matrices[camera], dtype=float).reshape(3, 4)
        u, v = np.asarray(observations[camera], dtype=float).reshape(2)
        rows.append(u * matrix[2] - matrix[0])
        rows.append(v * matrix[2] - matrix[1])
    design = np.asarray(rows, dtype=float)
    _, singular_values, vt = np.linalg.svd(design, full_matrices=False)
    homogeneous = vt[-1]
    if abs(homogeneous[3]) < 1e-12:
        raise ValueError("DLT solution is at infinity")
    xyz = homogeneous[:3] / homogeneous[3]
    reprojection = {
        camera: project_point(projection_matrices[camera], xyz).tolist()
        for camera in cameras
    }
    errors = {
        camera: float(np.linalg.norm(np.asarray(reprojection[camera]) - np.asarray(observations[camera], dtype=float)))
        for camera in cameras
    }
    condition_proxy = float(singular_values[0] / max(singular_values[-1], 1e-12))
    return {
        "xyz": xyz.tolist(),
        "cameras": cameras,
        "reprojection_px": reprojection,
        "reprojection_error_px": errors,
        "max_reprojection_error_px": max(errors.values()),
        "condition_proxy": condition_proxy,
    }


def triangulate_trajectory(frames, projection_matrices):
    """Triangulate one homologous landmark across a sequence of frames.

    Each item must contain ``frame_index`` and an ``observations`` mapping.
    Missing or geometrically invalid frames are retained with an explicit
    status so downstream code cannot mistake a dropped row for a zero.
    """
    output = []
    for position, frame in enumerate(frames):
        frame_index = frame.get("frame_index", position)
        observations = frame.get("observations", {})
        try:
            result = triangulate_point(observations, projection_matrices)
        except (KeyError, TypeError, ValueError, np.linalg.LinAlgError) as exc:
            output.append({
                "frame_index": frame_index,
                "status": "invalid",
                "reason": str(exc),
            })
            continue
        result["frame_index"] = frame_index
        result["status"] = "ok"
        output.append(result)
    return output
