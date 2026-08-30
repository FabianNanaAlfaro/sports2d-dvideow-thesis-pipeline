# Public research brief

## What the thesis investigates

The project asks how markerless motion-analysis algorithms can support a defensible assessment of lower-limb movement and asymmetry during the futsal instep kick. The design keeps the observation routes separate until they can be compared through the same anatomical, geometric and temporal contracts.

## What was actually built

1. A source/integrity map for synchronized camera views and semantic trials.
2. A manually tracked DVIDEOW reference route.
3. A Sports2D route for markerless 2D pose extraction and tracking.
4. A MediaPipe Pose route with laterality selection and temporal curation.
5. A DeepLabCut route and a declared multi-configuration benchmark.
6. A common two-camera DLT reconstruction interface.
7. Derived 3D, kinematic, angular and bilateral variables inside a declared pre-impact-to-impact window.
8. A validation plan that distinguishes 2D agreement, 3D reconstruction, temporal preservation, symmetry and robustness.

## What can be said publicly about the results

The evidence supports a trade-off interpretation rather than a universal ranking: different routes answer different error questions, and the method that is useful for one downstream criterion is not automatically the best for all of them. The public release therefore explains the evaluation layers and preserves the detailed numeric results in the private thesis package.

Two safeguards are especially important:

- 2D route selection is not the same claim as independent external 3D validation.
- The DeepLabCut benchmark is descriptive when configuration defaults differ; it should not be marketed as a pure architecture-only ablation.

## International context

The preliminary international work is associated with the assigned DOI [10.1080/14763141.2026.2680520](https://doi.org/10.1080/14763141.2026.2680520) and an oral presentation at [ISBS 2026](https://isbs.org/conferences/conferences/29-isbs2026). The public repository includes the presentation certificate, but not the journal proof or result figures.

