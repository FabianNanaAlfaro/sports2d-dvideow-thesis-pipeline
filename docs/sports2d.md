# Sports2D model card and application

## Nomenclature and attribution

The tool is **Sports2D**, not “Sparse2D”. Its official public repository is [davidpagnon/Sports2D](https://github.com/davidpagnon/Sports2D), maintained by David Pagnon. The software paper is by David Pagnon and HunMin Kim: [Pagnon & Kim (2024), DOI 10.21105/joss.06849](https://doi.org/10.21105/joss.06849).

The name sometimes remembered as “David Packard” is not the author identity used by the official repository or paper; this repository keeps the verifiable citation **David Pagnon**.

## What this thesis uses

The thesis route uses the official `Body_with_feet` model family, whose upstream configuration describes the default body model as **HALPE_26**. The route is kept in 2D pixel space so the four functional points can be homologated and reconstructed later with the common two-camera DLT contract.

```text
video view
  → Sports2D / RTMPose + YOLOX / Body_with_feet (Halpe-26)
  → one-person selection + tracking
  → pixel-space pose export
  → common hip/knee/ankle/foot adapter
  → two-camera DLT
```

This is why the repository does not use a single-view meters conversion as the thesis' 3D result. The route-specific detector is allowed to be different; the geometry and downstream comparison contract are not.

## Reproduce the route with the checked-in wrapper

```powershell
python src/run_sports2d.py `
  --video $env:THESIS_PRIVATE_ROOT\videos\trial.mp4 `
  --output-dir $env:THESIS_PRIVATE_ROOT\runs\sports2d `
  --print-config
```

The public template records the important settings used in the thesis route:

| Setting | Public value | Why |
| --- | --- | --- |
| Pose model | `Body_with_feet` / Halpe-26 | Includes feet and maps to the lower-limb contract. |
| Mode | `balanced` | Matches the declared RTMPose/YOLOX route family. |
| Persons | `1` | Keeps the selected subject explicit. |
| Ordering | `greatest_displacement` | Declared subject-selection heuristic. |
| Detection frequency | `1` | Detector is run on every frame. |
| Keypoint threshold | `0.30` | Low-confidence points are not silently accepted. |
| Average threshold | `0.40` | Person-level confidence gate. |
| Keypoint-number threshold | `0.60` | Completeness gate. |
| Tracking | `sports2d` / `keypoints` | Route-specific tracking, not a hidden manual correction. |
| Post-processing | largest section; reject outliers; interpolate gaps `< 6` frames; larger gaps `NaN` | Matches the closed 2D export contract. |
| Internal filter | off | The thesis curation/filtering stage is explicit downstream. |
| Saving | pose/angles on; video/images off | Keeps the method output useful without creating presentation artifacts. |
| Meters conversion | off | Common DLT is applied after homologation. |

The command is intentionally dry-run by default. Add `--execute` only in a private environment and use `--keep-config` if the generated configuration should be retained with the private provenance record.

## Upstream limitations retained

Sports2D is a 2D pose/angle tool. The upstream paper notes that 2D methods are appropriate when the analyzed motion is sufficiently represented in a sagittal or frontal plane; the thesis therefore treats Sports2D's 2D output and the independent two-view 3D reconstruction as separate validation questions. See the [upstream paper](https://joss.theoj.org/papers/10.21105/joss.06849) and this project's [limitations](limitations.md).
