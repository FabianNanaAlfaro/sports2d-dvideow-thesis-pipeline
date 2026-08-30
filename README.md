# Sports2D × DVIDEOW — thesis pipeline

[![CI](https://github.com/FabianNanaAlfaro/sports2d-dvideow-thesis-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/FabianNanaAlfaro/sports2d-dvideow-thesis-pipeline/actions/workflows/ci.yml)
[![DOI status](https://img.shields.io/badge/DOI-assigned%20%2F%20in%20production-315cbb)](https://doi.org/10.1080/14763141.2026.2680520)
[![License](https://img.shields.io/badge/original%20code%20and%20docs-MIT-2ea44f)](LICENSE)

Companion repository for the undergraduate thesis **“Implementación y validación de algoritmos de inteligencia artificial para analizar la asimetría en el movimiento del pateo en futsal”**. It explains, audits and demonstrates the complete processing pipeline used to compare markerless motion-analysis routes with a manually tracked DVIDEOW reference.

> **Public-release rule.** This is a methodological release, not a copy of the thesis working folder. It contains the process, contracts, synthetic examples, audit tools and public attribution. It intentionally contains no participant-level data, videos, calibrations, executable video software, model weights, raw/curated result tables, result figures, thesis document or journal proof.

## What this project makes clear

The work has one shared funnel and several detector routes:

```text
research question → source/integrity map → synchronized 2D views
        ├─ manual DVIDEOW reference
        ├─ Sports2D
        ├─ MediaPipe Pose
        └─ DeepLabCut benchmark
              ↓
      homologous points → common DLT → temporal treatment
              ↓
  trajectories / velocities / angles / symmetry → validation and audit
```

The central comparison is **2D agreement and 3D reconstruction against the manual DVIDEOW reference**. MediaPipe and DeepLabCut are complementary automated routes that pass through the same coordinate, DLT and temporal contracts; they are not silently presented as interchangeable models or as a single universal winner.

## Pipeline at a glance

| Stage | Public contract | Private boundary |
| --- | --- | --- |
| 0. Framing | Objective, ethics boundary, variables and acceptance criteria | Consent records and institutional files |
| 1. Integrity map | Semantic trial/camera schema and versioned manifest | Actual names, paths and source inventory |
| 2. Acquisition | Resolution, sampling and synchronization assumptions | Original videos and participant identities |
| 3. 2D routes | DVIDEOW, Sports2D, MediaPipe and DLC route cards | Tracking files, snapshots and weights |
| 4. Harmonization | Anatomical-point vocabulary, frame base and missingness rules | Frame-level rows and coordinates |
| 5. Reconstruction | DLT equation, camera-pair contract and reprojection checks | Calibration files and 3D exports |
| 6. Temporal/biomechanics | Pre-impact window, normalization and derived variables | Participant-level results |
| 7. Validation | 2D, 3D, temporal, symmetry and robustness audit plan | Result tables/figures and statistical exports |
| 8. Release | Public manifest, tests, audit script and interactive guide | Everything listed in the boundary document |

## Start here

1. [Complete pipeline](docs/pipeline.md) — every stage from research question to public release.
2. [Methods and contracts](docs/methods.md) — conventions that keep the routes comparable.
3. [Public/private boundary](docs/data-boundary.md) — what is deliberately excluded.
4. [Contributors and affiliations](docs/contributors.md) — roles, institutions and public profiles.
5. [Publication and presentation evidence](docs/publication.md) — assigned DOI, related work and certificate.
6. [Interactive pipeline explorer](https://fabiannanaalfaro.github.io/sports2d-dvideow-thesis-pipeline/) — a visual, responsive guide with no result data.

## Reproducible, safe example

The repository runs only on synthetic metadata. It is useful for checking whether a pipeline manifest is complete and whether a release tree contains forbidden files:

```powershell
python src/validate_manifest.py examples/manifest.example.json
python src/audit_public_release.py .
```

Both checks use the standard Python library only. They do not look for, open or process the private thesis database.

## Research status

The thesis is organized as a multi-level validation: 2D agreement, common DLT reconstruction, temporal preservation, derived biomechanical variables, symmetry analysis and robustness limits. The current interpretation is deliberately nuanced: a method can perform well for one error family and not dominate every downstream criterion. Detailed numeric tables and result graphics remain outside this public companion repository.

The international preliminary work is identified by the **assigned DOI** [10.1080/14763141.2026.2680520](https://doi.org/10.1080/14763141.2026.2680520). At this release it is labelled **assigned / in production**, not described as a final indexed article. The presentation certificate is included in [the evidence page](docs/publication.md); the proof file itself is intentionally not included.

## Attribution

The research context brings together the Pontificia Universidad Católica del Perú, the University of São Paulo and the Federal University of Espírito Santo. Roles are scoped to the thesis and preliminary international work, and public links are provided only where they were verified. See [contributors.md](docs/contributors.md) and [sources.md](docs/sources.md).

## License

Original documentation, diagrams and small utility scripts are released under the MIT License. The ISBS certificate and institutional marks remain third-party materials; see [NOTICE.md](NOTICE.md).

