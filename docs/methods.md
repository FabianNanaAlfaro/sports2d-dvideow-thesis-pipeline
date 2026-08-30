# Methods and public contracts

This page makes the interfaces concrete enough for another researcher to understand or reimplement the workflow with their own authorized data.

## Canonical identifiers

Use semantic identifiers rather than filename suffixes:

| Field | Meaning | Public example |
| --- | --- | --- |
| `trial_id` | One kick/trial unit | `trial-demo-001` |
| `side` | Anatomical side being analyzed | `right` |
| `camera_role` | Camera position in the pair | `CAM_1` or `CAM_2` |
| `route` | Observation source | `dvideow_manual`, `sports2d`, `mediapipe`, `deeplabcut` |
| `frame_index` | Zero-based video frame | `0`, `1`, `2` |
| `impact_frame` | Temporal anchor | symbolic in public examples |

The camera role comes from the canonical folder/manifest map. It is never inferred from a copied `c3`/`c4` suffix.

## 2D observation contract

Each point observation has this logical shape:

```json
{
  "trial_id": "trial-demo-001",
  "side": "right",
  "camera_role": "CAM_1",
  "route": "sports2d",
  "frame_index": 0,
  "landmark": "ankle",
  "x_px": 421.5,
  "y_px": 238.0,
  "likelihood": 0.91,
  "valid": true,
  "transform_ref": "full-frame"
}
```

The values above are synthetic. A real input must also declare its frame rate, image dimensions, crop/ROI transform if any, preprocessing version and missingness policy. `x_px`/`y_px` are pixel coordinates; meters are not introduced until the DLT stage.

## Routes

### Sports2D route card

- Pose representation: body-with-feet / Halpe-26-compatible output.
- Detector/tracker: declared RTMPose + YOLOX configuration in the private run manifest.
- Subject policy: one selected subject, with identity and displacement rules recorded.
- Detection frequency and thresholds: configuration fields, never hidden in code.
- Short-gap interpolation is bounded; long gaps remain missing.
- Export adapter maps the route output to the DVIDEOW-compatible 2D contract.

### MediaPipe route card

- Landmark model: MediaPipe Pose, 33 landmarks.
- Region-of-interest coordinates are represented by a safe camera/side template; a real run records the selected transform and maps crop coordinates back to the full frame once.
- Laterality candidates are compared against the manual temporal anchor in a small offset window.
- Curation may include Hampel derivative screening, PCHIP for short gaps and Savitzky–Golay/acceleration checks.
- Final route metadata preserves whether a point was observed, interpolated or rejected.

### DeepLabCut route card

- Eight functional points are homologated to the common vocabulary.
- The model benchmark declares the detector, architecture, seed, split, snapshot and confidence cutoff.
- A fixed detector and a held-out selection protocol are required for comparisons.
- The benchmark is descriptive when training defaults differ across model configurations; it is not advertised as a pure architecture-only ablation.
- Model weights, labeled images, snapshots and predictions are withheld.

## Reference and DLT contract

DVIDEOW manual tracking is the reference route, not a fourth markerless detector. The adapter preserves the legacy 2D/3D column semantics, frame base and missing-value behavior. A two-camera reconstruction uses the same homologous landmark and the same calibration reference for both views.

Public acceptance conditions:

- both camera roles are present for the same semantic trial/side;
- the calibration reference exists in the private package;
- the frame-base adapter is declared;
- finite 3D values and reprojection checks pass the configured gate;
- the executable [`quality_gate.py`](../src/quality_gate.py) records the accept/reject reason;
- no manual coordinate is copied into an automated route;
- every generated output points back to a manifest version.

The public [`derive_biomechanics.py`](../src/derive_biomechanics.py) example
implements the downstream finite-difference velocity, speed and joint-angle
interfaces. It is a transparent contract utility, not a claim that synthetic
values reproduce the withheld thesis results.

## Temporal contract

The comparison is restricted to the declared pre-impact-to-impact window. The normalized curve has 101 positions in that window. The pipeline does not claim to reconstruct a complete kick cycle or post-impact motion. A frame offset must be explicit and testable; the public validator rejects an omitted frame convention.

## Metrics contract

The analysis plan can request the following families:

| Family | Examples | Interpretation boundary |
| --- | --- | --- |
| 2D point error | MAE, RMSE, centered RMSE, P95, NME, PCK, CCC | agreement in image space |
| 3D reconstruction | MAE, RMSE, centered RMSE, P95, reprojection | spatial reconstruction |
| Temporal shape | Pearson, Spearman, CCC, peak magnitude/phase | preservation of time-varying behavior |
| Agreement | Bland–Altman, cluster bootstrap | bias/limits with repeated observations |
| Inferential | repeated measures, paired tests, SPM, Holm/FDR | uncertainty and multiplicity control |
| Symmetry | predeclared bilateral index | only when both sides pass validity |

Metric values, participant rows and result plots are intentionally not stored in this public repository.

## Branch and version discipline

The local work contains historical and current DLC experiments with different splits/configuration details. They must remain separate branches in provenance. A manifest must name its branch, source commit, model/config version and analysis window. The public repository therefore documents the distinction without publishing conflicting result tables as if they were one experiment.
