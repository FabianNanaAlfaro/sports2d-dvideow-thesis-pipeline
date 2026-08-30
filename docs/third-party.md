# Third-party methods and image credits

The public release uses small original diagrams and links to upstream projects. It does not copy screenshots, result figures or model files from the thesis.

## Sports2D

Sports2D is attributed to David Pagnon and HunMin Kim. Use the [official GitHub repository](https://github.com/davidpagnon/Sports2D), the [official configuration example](https://github.com/davidpagnon/Sports2D/blob/main/Sports2D/Demo/Config_demo.toml) and [JOSS DOI 10.21105/joss.06849](https://doi.org/10.21105/joss.06849). The route uses the upstream `Body_with_feet` / Halpe-26 naming, with a local adapter for the thesis' four functional points.

## Halpe-26

[`site/assets/halpe-26-keypoints.svg`](../site/assets/halpe-26-keypoints.svg) is an original schematic created for this repository. It is not a copied dataset image and it is not a thesis result. The 26 body-point names and indices follow the public [Halpe-FullBody repository](https://github.com/Fang-Haoshu/Halpe-FullBody) and its [AlphaPose implementation](https://github.com/MVIG-SJTU/AlphaPose/blob/master/alphapose/datasets/halpe_26.py). The upstream Halpe/AlphaPose work should be cited when the keypoint definition is used; see [AlphaPose](https://doi.org/10.1109/TPAMI.2022.3222784).

## DeepLabCut

DeepLabCut is attributed to its official project and publications. The code/benchmark card links the [official repository](https://github.com/deeplabcut/DeepLabCut), the original [Nature Neuroscience paper](https://doi.org/10.1038/s41593-018-0209-y) and the [3D protocol](https://doi.org/10.1038/s41596-019-0176-0). No DeepLabCut model artifact is redistributed here.

## MediaPipe and DVIDEOW

MediaPipe and DVIDEOW are named as route/dependency context only. The repository does not redistribute their software, source videos, calibration records or generated files. The public MediaPipe adapter is a small interface example and must be run only in an environment where the optional dependency is authorized. Cite the [MediaPipe Pose documentation](https://mediapipe.readthedocs.io/en/latest/solutions/pose.html) when reusing the legacy detector/tracker settings.
