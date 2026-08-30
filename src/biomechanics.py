#!/usr/bin/env python3
"""Small dependency-light kinematic derivations for valid 3D trajectories."""

from __future__ import print_function

import math

import numpy as np


def _positions(rows):
    converted = []
    for row in rows:
        if row is None or len(row) != 3:
            converted.append([np.nan, np.nan, np.nan])
        else:
            converted.append([np.nan if value is None else float(value) for value in row])
    return np.asarray(converted, dtype=float)


def velocity_from_positions(positions, sampling_hz):
    """Return per-frame velocity while preserving missing coordinates."""
    if sampling_hz <= 0:
        raise ValueError("sampling_hz must be positive")
    values = _positions(positions)
    if len(values) == 0:
        return []
    dt = 1.0 / float(sampling_hz)
    velocity = np.full_like(values, np.nan, dtype=float)
    for index in range(len(values)):
        previous = values[index - 1] if index > 0 else None
        following = values[index + 1] if index + 1 < len(values) else None
        if previous is not None and following is not None and np.isfinite(previous).all() and np.isfinite(following).all():
            velocity[index] = (following - previous) / (2.0 * dt)
        elif previous is not None and np.isfinite(previous).all() and np.isfinite(values[index]).all():
            velocity[index] = (values[index] - previous) / dt
        elif following is not None and np.isfinite(following).all() and np.isfinite(values[index]).all():
            velocity[index] = (following - values[index]) / dt
    return _json_rows(velocity)


def speed_from_velocity(velocity):
    values = _positions(velocity)
    speeds = np.full(len(values), np.nan, dtype=float)
    valid = np.isfinite(values).all(axis=1)
    speeds[valid] = np.linalg.norm(values[valid], axis=1)
    return _json_values(speeds)


def angle_at_vertex(proximal, vertex, distal):
    """Return the angle in degrees at ``vertex`` or ``None`` if invalid."""
    vectors = [_positions([proximal])[0], _positions([vertex])[0], _positions([distal])[0]]
    if not all(np.isfinite(vector).all() for vector in vectors):
        return None
    first = vectors[0] - vectors[1]
    second = vectors[2] - vectors[1]
    denominator = np.linalg.norm(first) * np.linalg.norm(second)
    if denominator == 0:
        return None
    cosine = float(np.dot(first, second) / denominator)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def angle_series(landmarks, proximal, vertex, distal):
    rows = [landmarks.get(name, []) for name in (proximal, vertex, distal)]
    length = max((len(row) for row in rows), default=0)
    output = []
    for index in range(length):
        points = [row[index] if index < len(row) else None for row in rows]
        output.append(angle_at_vertex(*points))
    return output


def symmetry_index(left, right):
    """Percent difference relative to the mean absolute magnitude."""
    if left is None or right is None:
        return None
    left = float(left)
    right = float(right)
    if not math.isfinite(left) or not math.isfinite(right):
        return None
    denominator = (abs(left) + abs(right)) / 2.0
    if denominator == 0:
        return None
    return 100.0 * abs(left - right) / denominator


def derived_kinematics(landmarks, sampling_hz):
    """Derive velocities, speeds and lower-limb angles from valid 3D points."""
    result = {"landmarks": {}, "angles_deg": {}}
    for name, rows in landmarks.items():
        velocity = velocity_from_positions(rows, sampling_hz)
        result["landmarks"][name] = {
            "velocity": velocity,
            "speed": speed_from_velocity(velocity),
        }
    if all(name in landmarks for name in ("hip", "knee", "ankle")):
        result["angles_deg"]["knee"] = angle_series(landmarks, "hip", "knee", "ankle")
    if all(name in landmarks for name in ("knee", "ankle", "foot")):
        result["angles_deg"]["ankle"] = angle_series(landmarks, "knee", "ankle", "foot")
    return result


def _json_values(values):
    return [None if not np.isfinite(value) else float(value) for value in values]


def _json_rows(values):
    return [None if not np.isfinite(row).all() else [float(value) for value in row] for row in values]
