# Engineering quickstart

This repository is executable at the level of contracts and synthetic examples. The real experiment still requires an authorized private environment containing the videos, calibration records and model artifacts.

## 1. Install the public numerical core

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Run the complete public smoke test:

```powershell
.\scripts\run_public_demo.ps1
```

If Windows has more than one Python installation, pass the interpreter used
for the public environment with `-PythonExecutable`.

It validates the manifest, audits the release tree, triangulates one synthetic point, normalizes one synthetic curve and expands the DLC benchmark plan. It never searches for or opens the thesis database.

## 2. Sports2D 2D route

Install the external package in a private environment, then use the checked-in template and wrapper. The wrapper is dry-run by default:

```powershell
python -m pip install sports2d
python src/run_sports2d.py `
  --video $env:THESIS_PRIVATE_ROOT\videos\trial.mp4 `
  --output-dir $env:THESIS_PRIVATE_ROOT\runs\sports2d `
  --print-config
```

When the rendered configuration has been reviewed, add `--execute --keep-config`. The wrapper uses `Body_with_feet` (the official Sports2D name for the Halpe-26 body model), `balanced` mode, one subject, `greatest_displacement`, detection on every frame, `onnxruntime` with automatic device selection, the largest valid section, outlier rejection, interpolation only for gaps shorter than six frames, `NaN` for larger gaps, no internal filter, no output video/images, pose/angle exports enabled, and pixel-space output for the later common DLT step.

The upstream CLI can also be called directly after editing a private copy of [`configs/sports2d.thesis.toml`](../configs/sports2d.thesis.toml):

```powershell
sports2d --config path\to\private\sports2d.generated.toml
```

Sports2D writes its own pose/angle formats such as TRC/MOT. The thesis pipeline does not treat that export as the final 3D result: [`homologate.py`](../src/homologate.py) makes the point vocabulary explicit, and [`dlt.py`](../src/dlt.py) applies the common two-view geometry.

## 3. MediaPipe route

Use the pinned optional environment only in a private workspace:

```powershell
python -m pip install mediapipe==0.10.21 opencv-python
python src/run_mediapipe.py `
  --video $env:THESIS_PRIVATE_ROOT\videos\trial.mp4 `
  --output $env:THESIS_PRIVATE_ROOT\runs\mediapipe\trial.json `
  --side right `
  --camera-role CAM_1 `
  --roi-config configs/mediapipe.roi.example.json
```

The adapter emits pixel coordinates, normalized coordinates, visibility and frame indices for hip/knee/ankle/foot. It keeps segmentation disabled, uses model complexity 2, applies the declared padded ROI when supplied, and maps the resized crop back to the original 848 × 480 pixel system exactly once. A visibility threshold marks low-confidence points invalid instead of replacing them with zero. Laterality selection, Hampel/PCHIP/Savitzky–Golay curation and the frame-offset decision remain explicit downstream steps.

## 4. Homologation and DLT

Run the synthetic adapter:

```powershell
python src/homologate.py examples/keypoints.example.json
python src/reconstruct_json.py examples/dlt-input.example.json
python src/reconstruct_json.py examples/dlt-trajectory.example.json --max-reprojection-px 5
```

For an authorized run, replace the synthetic JSON with a private per-frame contract. The DLT code accepts projection matrices or the legacy 11-coefficient form through `projection_matrix_from_dlt`; it triangulates one point or a frame sequence, returns per-camera reprojection errors, and attaches an explicit quality decision so bad geometry is rejected before biomechanics. Invalid frames remain in the output with a reason.

This public core deliberately does not parse a DVIDEOW `.CAL` file or infer a
camera from a legacy suffix. A private adapter must map the verified
`CAM_1`/`CAM_2` calibration records into projection matrices and validate the
frame convention against the original DVIDEOW output before accepting a run.

Normalize only after the validity gate:

```powershell
python src/normalize_window.py `
  path\to\private\normalized-input.json `
  --points 101 `
  --output path\to\private\normalized-output.json
```

Derive kinematics only from the quality-approved 3D contract. Missing rows are
preserved as `null`; no manual reference coordinate is copied into the
automated route:

```powershell
python src/derive_biomechanics.py `
  path\to\private\quality-approved-3d.json `
  --output path\to\private\derived-kinematics.json
```

The public example is executable without research data:

```powershell
python src/derive_biomechanics.py examples/biomechanics-input.example.json
```

## 5. DeepLabCut benchmark

Inspect the public matrix and create a run plan:

```powershell
python src/dlc_benchmark_plan.py --config configs/dlc_benchmark.example.json
```

For a private DeepLabCut project, the safe runner defaults to dry-run:

```powershell
python src/run_dlc.py `
  --action analyze `
  --config-yaml path\to\private\config.yaml `
  --video path\to\private\CAM_1_trial.mp4 `
  --video path\to\private\CAM_2_trial.mp4 `
  --output-dir path\to\private\runs\dlc `
  --execute
```

Training and evaluation use the same high-level DeepLabCut API through `--action train`; the exact backend/version must be written into the private run manifest. No weights, snapshots, labels, predictions or benchmark outputs belong in this repository.

## Reproducibility boundary

The public code proves that the interfaces run. It does not claim that a researcher can regenerate human-subject results from this tree alone. The complete methodological order and all limitations are in [`pipeline.md`](pipeline.md) and [`limitations.md`](limitations.md).
