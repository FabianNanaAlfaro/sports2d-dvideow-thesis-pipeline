# Audit notes and limitations

This page is part of the release precisely because a professional research repository should state what it does not prove.

## Claims supported by this public release

- The workflow has a documented common funnel from 2D observations to DLT, temporal variables and validation.
- DVIDEOW is treated as a manual reference route; it is not conflated with a markerless detector.
- Sports2D, MediaPipe and DeepLabCut are described as distinct routes with explicit adapters.
- Camera identity, frame base, missingness and versioning are elevated to explicit contracts.
- The repository has a machine-checkable public boundary and synthetic manifest.

## Claims not made

- No claim that the public repository can reproduce participant-level results without the private research package.
- No claim that the assigned DOI is already a final indexed article.
- No claim that DeepLabCut's model comparison is a pure architecture ablation.
- No claim of a universal best detector for every 2D, 3D, temporal or symmetry criterion.
- No claim that a single run establishes multi-seed, GroupKFold or leave-one-subject-out robustness.
- No claim that the thesis database, video software or calibration records are open data.

## Known methodological limits retained from the audit

- The external 3D comparison and the 2D route selection answer different questions and must not be merged into one score.
- The pre-impact-to-impact window is not a full kick-cycle analysis.
- Exploratory filters and route-specific curation can change temporal behavior; their parameters must travel with the manifest.
- A held-out subset used for model selection is not automatically an untouched final external test.
- Historical aliases and missing inputs are handled by the private provenance log; they are not repaired by silently rewriting source files.

## Next responsible step

An authorized continuation should add a preregistered robustness package—multiple seeds and subject-grouped evaluation where feasible—before making stronger generalization claims. That package would require a separate privacy and ethics review; it should not be solved by opening the current raw database.

