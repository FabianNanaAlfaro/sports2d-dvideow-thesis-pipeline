# Pipeline acceptance gates

These gates are intentionally expressed as questions. A real private run should answer them with a versioned manifest and evidence, not with a screenshot.

## Identity and synchronization

- Does every trial/side have the expected camera pair?
- Is camera role taken from the semantic map rather than a filename suffix?
- Is the video-to-DAT-to-3D frame base explicit?
- Is the impact anchor traceable without exposing a participant or local path?

## 2D route integrity

- Are DVIDEOW, Sports2D, MediaPipe and DeepLabCut kept as distinct routes?
- Does the adapter preserve frame index, pixel coordinates, likelihood and missingness?
- Are ROI/crop transformations reversible and versioned?
- Were manual coordinates kept out of automated observations?

## 3D reconstruction

- Are both camera observations homologous and paired semantically?
- Is the private calibration reference present and immutable for the run?
- Do finite-value, reprojection and geometry checks pass?
- Is the legacy frame convention preserved by an explicit adapter?

## Temporal and statistical validity

- Is the pre-impact-to-impact window declared?
- Are interpolation, filters, cutoff, order and sampling rate recorded?
- Are bilateral indices calculated only when both sides pass the validity gate?
- Are repeated observations, cluster structure and multiplicity handled by the declared plan?
- Are exploratory runs separated from confirmatory claims?

## Public release

- Are database, video, calibration, executable, model and result artifacts absent?
- Are there no participant IDs, frame rows, local Windows paths, emails or credentials?
- Is the DOI status labelled honestly as assigned/in production when appropriate?
- Are collaborators credited with scoped roles and public links only?
- Does the static guide render at desktop and mobile widths?

## Executable public smoke test

The repository-level smoke test is intentionally synthetic. It exercises the
numerical contracts without opening a video, database, calibration, model or
result file:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/reconstruct_json.py examples/dlt-input.example.json
python src/reconstruct_json.py examples/dlt-trajectory.example.json --max-reprojection-px 5
python src/normalize_window.py examples/normalize-input.example.json --points 101
python src/derive_biomechanics.py examples/biomechanics-input.example.json
python src/dlc_benchmark_plan.py --config configs/dlc_benchmark.example.json
```

Optional adapters are separate from this gate. They run only after an
authorized private environment is configured and default to dry-run where
possible. Their generated outputs must be stored outside this repository.
