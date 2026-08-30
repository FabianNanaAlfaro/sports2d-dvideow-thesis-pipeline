# Complete research pipeline

This is the public reconstruction of the workflow carried out in the thesis project. It describes the sequence, interfaces and audit decisions without publishing the underlying database.

## Study context

The thesis evaluates markerless motion-analysis routes for futsal instep kicking and the downstream analysis of lower-limb asymmetry. The working study context is 13 professional male futsal participants, 78 trials and 156 synchronized camera views. Each trial is treated as a semantic unit; participant identifiers, files and frame rows are not public.

The experimental setup used synchronized high-speed action-camera views at 240 Hz and a manually tracked DVIDEOW reference. The public documentation keeps these design facts because they explain the pipeline, while the original recordings, calibration and tracking files remain private.

## Stage 0 — research question, ethics and scope

**Question.** Can markerless 2D tracking and a common two-camera DLT reconstruction support a defensible analysis of lower-limb trajectories, velocities, joint angles and asymmetry during the pre-impact phase of a futsal instep kick?

**Controls.** Before processing, the private package records the approved study protocol, consent boundary, source version and the intended variables. The public release only records the existence of that gate; it does not reproduce consent forms or participant information.

**Output.** A versioned analysis plan with explicit acceptance criteria and a list of artifacts that may never enter a public repository.

## Stage 1 — source inventory and integrity map

The canonical key is semantic:

```text
trial_id + side + camera_role (CAM_1 | CAM_2)
```

Folder meaning is authoritative. Historical suffixes or copied filenames are aliases to resolve, not evidence that a camera has changed. Every repair is logged as a new manifest version; source files are not renamed, moved or overwritten during mapping.

The integrity pass checks that each logical trial has the expected camera pair, a compatible frame template, an explicit side, and a traceable relation between the 2D observation and its later 3D reconstruction. The public example uses `trial-demo-001`, never a real participant or path.

## Stage 2 — synchronized views and temporal anchor

The private source route uses the canonical video representation and retains the original frame rate and dimensions. A manual impact event anchors the time axis. The public contract represents the anchor as `impact_frame` without revealing a frame number, filename or participant.

Only the pre-impact-to-impact window is analyzed in the thesis comparison. It is not a full-kick or post-impact reconstruction. Each route keeps the frame index it observed; alignment is an explicit step, not an assumption hidden in a plot.

## Stage 3 — parallel 2D observation routes

The routes are deliberately parallel and are not collapsed into one opaque “AI model”.

### A. DVIDEOW manual reference

DVIDEOW manual tracking and its associated calibration/reconstruction workflow provide the reference coordinate system. The public repository describes the data shape and the DLT contract; it does not redistribute `.DAT`, `.CAL`, `.3D` or calibration values.

### B. Sports2D

The Sports2D route uses a pose detector/tracker configuration suitable for full-body-with-feet keypoints, keeps one subject, preserves the camera identity and exports a 2D representation that can be adapted to the DVIDEOW column semantics. Detection, tracking, interpolation and outlier decisions are recorded as route metadata rather than silently mixed with the reference.

### C. MediaPipe Pose

MediaPipe produces 33 landmarks per view. The thesis route uses camera/side regions of interest, laterality selection and a temporal curation chain. Candidates are selected against the manual temporal anchor; short gaps may be interpolated, while large gaps remain missing. Hampel speed screening, shape-preserving interpolation and Savitzky–Golay/acceleration checks are part of the auditable curation history.

### D. DeepLabCut

DeepLabCut is an additional automated 2D route with eight functional points and the same DLT semantics. The model benchmark compares configurations under a declared protocol. It is treated as a descriptive benchmark, not as a pure architecture ablation, because defaults such as optimizer, scheduler, head and pretraining can vary with the configuration. The held-out selection logic is documented, but no weights, snapshots, labeled images or prediction files are public.

## Stage 4 — homologation and 2D contract

Every route is adapted to the same functional vocabulary:

```text
hip → knee → ankle → foot
```

The adapter preserves, at minimum, `frame_index`, `x_px`, `y_px`, `likelihood`, `valid`, `source_route` and `camera_role`. Missingness is explicit. A point missing in both coordinates is not silently converted to a zero. Coordinate remapping from a crop back to the full image is recorded with the crop transform, not applied ad hoc in a later spreadsheet.

The final temporal selector tests the small synchronization offset neighborhood against the manual anchor. It never copies manual coordinates into an automated route, fills an automated gap from the reference or exchanges views because a filename happens to contain `c3` or `c4`.

## Stage 5 — common two-camera DLT reconstruction

The reconstruction applies the classical projective relation for each camera:

```text
[u, v, 1]ᵀ × P [X, Y, Z, 1]ᵀ = 0
```

where `P` is the 3 × 4 camera projection matrix represented by the 11 DLT coefficients. Two views of the same homologous point are combined to solve the 3D location. Reprojection error and finite-value checks are calculated before a trajectory can move downstream.

The local experiment uses a measured calibration volume and six camera-calibration records. This repository exposes neither the calibration numbers nor the files. Its synthetic manifest exposes only the relationship `camera_pair → calibration_ref → reconstruction_contract`.

The legacy frame convention is preserved by an explicit adapter: video row 0, DVIDEOW DAT frame 1, and 3D frame derived from the DAT convention. Any adapter that changes this base must fail validation rather than shifting a whole trajectory silently.

## Stage 6 — temporal treatment and biomechanical variables

Route-specific curation is kept visible. After reconstruction and quality checks, the common comparison window is normalized to 101 points between the pre-impact anchor and impact. The pipeline then derives, where valid:

- 3D position and speed for hip, knee, ankle and foot;
- knee and ankle angles and angular speeds;
- temporal curves and peak magnitude/phase descriptors;
- bilateral symmetry descriptors defined in the analysis plan.

Filtering is not treated as a cosmetic step. Cutoff, order, sampling rate, interpolation policy and the source of every retained point belong in the manifest. The public example uses parameter labels only; it contains no trajectory values.

## Stage 7 — validation and statistical audit

The thesis separates several questions instead of relying on one score:

1. **2D agreement:** coordinate errors, centered errors, confidence-aware completeness and concordance.
2. **3D reconstruction:** absolute and relative errors, RMSE/P95, reprojection and calibration diagnostics.
3. **Temporal preservation:** Pearson/Spearman/CCC, peak magnitude and phase.
4. **Agreement structure:** Bland–Altman limits and cluster bootstrap where specified.
5. **Between-route effects:** repeated-measures omnibus/paired comparisons and SPM with multiplicity control.
6. **Symmetry:** predeclared bilateral indices applied only when both sides satisfy the validity gate.
7. **Robustness:** explicit separation between what was run once, what was exploratory and what remains pending.

The release does not include the numeric tables, statistical exports or result images. It does include the acceptance logic so that a future authorized rerun can be audited without guessing what “good” meant.

## Stage 8 — integrity, provenance and public release

Before publication, the release process:

1. validates the synthetic/public manifest;
2. scans tracked files for private paths, credentials and blocked artifact types;
3. checks that the proof, database, video/software artifacts and result figures are absent;
4. confirms that all public links and attribution pages are explicit;
5. runs the static interactive guide at desktop and mobile widths;
6. records the commit that changed each public layer.

The final repository is therefore a **pipeline companion**: reproducible at the level of contracts and checks, intentionally non-reproducible from the public tree alone at the level of human-subject observations.

