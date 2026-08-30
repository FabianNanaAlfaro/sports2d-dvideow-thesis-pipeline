# Public/private boundary

This repository is intentionally a **public methodological companion**. The public layer explains how the work is performed and gives a synthetic, executable health check. It is not the research database and it is not a mirror of the local thesis folder.

## Included

| Item | Why it is public-safe |
| --- | --- |
| Pipeline narrative and method contracts | Describes transformations without exposing observations. |
| Synthetic manifest and example trial | Demonstrates schema and validation with invented identifiers. |
| Mermaid and SVG process diagrams | Shows the workflow, not a result. |
| Standard-library validation and release-audit scripts | Useful to other researchers without requiring the source data. |
| Collaborator attribution and verified public links | Gives credit without publishing contact details. |
| Assigned DOI and related public references | Makes the international research context discoverable. |
| ISBS 2026 oral-presentation certificate | Documentary evidence requested for this release. |

## Deliberately withheld

| Item | Reason |
| --- | --- |
| Thesis database, participant-level rows and frame coordinates | Sensitive research data and not needed to understand the pipeline. |
| Original or decompressed videos | Participant privacy and large proprietary source material. |
| DVIDEOW `.DAT`, `.CAL`, `.3D` files and camera calibration values | Experimental records and reconstruction inputs. |
| Executable video software and local installations | Redistribution is unnecessary and may carry third-party restrictions. |
| DeepLabCut/MediaPipe/Sports2D weights, snapshots and caches | Large model artifacts and environment-specific files. |
| Raw, curated and final result tables | Keeps participant-level outcomes and unpublished analysis private. |
| Images of results, thesis figures and plots | User requested process visuals only. |
| Thesis DOCX and journal proof PDF | Private working document and production proof; neither is required for the public method. |
| Local Windows paths, emails, phone numbers and credentials | Prevents accidental personal or machine disclosure. |

## Release principle

If an artifact is required to execute the real analysis, it belongs in the private research package unless it has been de-identified, syntheticized and reviewed separately. The public repository exposes the interfaces between steps, not the underlying observations.

