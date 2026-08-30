#!/usr/bin/env python3
"""Extract a common four-point 2D record with MediaPipe Pose.

This optional adapter follows the thesis' legacy MediaPipe route: model
complexity 2, smoothed landmarks, no segmentation and low tracking thresholds.
The output is written wherever the caller chooses; it must not be committed.
"""

from __future__ import print_function

import argparse
import json
import sys
from pathlib import Path


LANDMARK_INDEX = {
    "right": {"hip": 24, "knee": 26, "ankle": 28, "foot": 32},
    "left": {"hip": 23, "knee": 25, "ankle": 27, "foot": 31},
}


def load_roi(roi_config, camera_role, side):
    if roi_config is None:
        return None
    payload = json.loads(Path(roi_config).read_text(encoding="utf-8"))
    entry = payload.get("entries", {}).get("{}:{}".format(camera_role, side))
    if entry is None:
        raise ValueError("ROI config has no entry for {}:{}".format(camera_role, side))
    required = ("x", "y", "width", "height", "padding", "scale")
    if any(key not in entry for key in required):
        raise ValueError("ROI entry must define {}".format(", ".join(required)))
    if entry["width"] <= 0 or entry["height"] <= 0 or entry["scale"] <= 0 or entry["padding"] < 0:
        raise ValueError("ROI width, height and scale must be positive; padding cannot be negative")
    return {key: float(entry[key]) for key in required}


def crop_with_padding(frame, roi):
    """Return an inference crop plus its unclipped full-frame geometry.

    Coordinates are later remapped using the original crop dimensions. The
    upscale factor changes inference resolution only; it is never applied a
    second time to the output coordinates.
    """
    if roi is None:
        height, width = frame.shape[:2]
        return frame, {"x": 0, "y": 0, "width": width, "height": height, "scale": 1.0}
    height, width = frame.shape[:2]
    x0 = max(0, int(round(roi["x"] - roi["padding"] * roi["width"])))
    y0 = max(0, int(round(roi["y"] - roi["padding"] * roi["height"])))
    x1 = min(width, int(round(roi["x"] + roi["width"] * (1 + roi["padding"]))))
    y1 = min(height, int(round(roi["y"] + roi["height"] * (1 + roi["padding"]))))
    if x1 <= x0 or y1 <= y0:
        raise ValueError("ROI does not intersect the video frame")
    crop = frame[y0:y1, x0:x1]
    scale = float(roi["scale"])
    if scale != 1.0:
        import cv2
        crop = cv2.resize(crop, (int(round(crop.shape[1] * scale)), int(round(crop.shape[0] * scale))), interpolation=cv2.INTER_LANCZOS4)
    return crop, {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0, "scale": scale}


def extract(video_path, output_path, side="right", model_complexity=2, static_image_mode=False,
            camera_role="CAM_1", roi_config=None, visibility_threshold=0.15):
    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        raise RuntimeError("install the optional MediaPipe/OpenCV dependencies first") from exc

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError("could not open the authorized input video")
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    frames = []
    roi = load_roi(roi_config, camera_role, side)

    with mp.solutions.pose.Pose(
        static_image_mode=static_image_mode,
        model_complexity=model_complexity,
        smooth_landmarks=True,
        enable_segmentation=False,
        min_detection_confidence=0.10,
        min_tracking_confidence=0.10,
    ) as pose:
        frame_index = 0
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            inference_frame, geometry = crop_with_padding(frame, roi)
            inference_height, inference_width = inference_frame.shape[:2]
            result = pose.process(cv2.cvtColor(inference_frame, cv2.COLOR_BGR2RGB))
            points = {}
            for landmark_name, landmark_index in LANDMARK_INDEX[side].items():
                if result.pose_landmarks is None:
                    points[landmark_name] = None
                    continue
                landmark = result.pose_landmarks.landmark[landmark_index]
                x_px = geometry["x"] + landmark.x * geometry["width"]
                y_px = geometry["y"] + landmark.y * geometry["height"]
                visibility = float(landmark.visibility)
                points[landmark_name] = {
                    "x_px": round(float(x_px), 6),
                    "y_px": round(float(y_px), 6),
                    "x_normalized": round(float(landmark.x), 8),
                    "y_normalized": round(float(landmark.y), 8),
                    "z_normalized": round(float(landmark.z), 8),
                    "likelihood": round(visibility, 6),
                    "valid": bool(visibility >= visibility_threshold),
                }
            frames.append({
                "frame_index": frame_index,
                "timestamp_s": (frame_index / fps) if fps else None,
                "landmarks": points,
            })
            frame_index += 1
    capture.release()

    payload = {
        "schema_version": "1.0",
        "route": "mediapipe",
        "side": side,
        "video_name": video_path.name,
        "video_fps": fps,
        "image_size_px": [width, height],
        "camera_role": camera_role,
        "roi": roi,
        "roi_visibility_threshold": visibility_threshold,
        "model_complexity": model_complexity,
        "static_image_mode": static_image_mode,
        "segmentation_enabled": False,
        "frames": frames,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    parser.add_argument("--camera-role", choices=("CAM_1", "CAM_2"), default="CAM_1")
    parser.add_argument("--roi-config", type=Path, help="optional public/private ROI JSON")
    parser.add_argument("--visibility-threshold", type=float, default=0.15)
    parser.add_argument("--model-complexity", type=int, choices=(0, 1, 2), default=2)
    parser.add_argument("--static-image-mode", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not 0 <= args.visibility_threshold <= 1:
            raise ValueError("visibility threshold must be between 0 and 1")
        payload = extract(
            args.video, args.output, args.side, args.model_complexity,
            args.static_image_mode, args.camera_role, args.roi_config,
            args.visibility_threshold,
        )
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print("FAIL: {}".format(exc), file=sys.stderr)
        return 2
    print("PASS: MediaPipe wrote {} frames to {}".format(len(payload["frames"]), args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
