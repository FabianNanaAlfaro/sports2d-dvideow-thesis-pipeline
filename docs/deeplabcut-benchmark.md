# DeepLabCut benchmark — five configurations

The thesis work includes a separate DeepLabCut benchmark. It is now represented in code by [`configs/dlc_benchmark.example.json`](../configs/dlc_benchmark.example.json) and [`src/dlc_benchmark_plan.py`](../src/dlc_benchmark_plan.py), rather than being reduced to a sentence in the README.

## Declared protocol

| Component | Declared value |
| --- | --- |
| Configurations | RTMPose-S, RTMPose-M, RTMPose-X, HRNet-W48, ResNet-101 |
| Detector | Common SSDLite detector |
| Labels | 3,181 |
| Training / validation-selection | 2,324 / 857 |
| Epochs / batch | 35 / 1 |
| Seed | 42 |
| Confidence cutoff | `pcutoff = 0.6` |
| 2D / 3D scope | 156 views / 78 trials |
| Selection groups | 3 subject groups, identifiers withheld |
| Final external test? | No |

These are protocol metadata from the audited private benchmark. The public repository does not include the labels, frame images, model weights, snapshots, predictions, per-subject rows or result tables.

## Why it is not called a pure architecture ablation

The configurations may differ in optimizer, scheduler, backbone/head and initialization defaults. The public plan therefore labels the comparison **descriptive configuration benchmark**. It records what was run without turning that comparison into a stronger causal claim than the design supports.

## Generate the expanded plan

```powershell
python src/dlc_benchmark_plan.py `
  --config configs/dlc_benchmark.example.json
```

The output expands each model into the same declared steps:

```text
prepare identical split
  → train configuration
  → select snapshot on declared 2D partition
  → analyze 2D views
  → homologate without copying reference coordinates
  → common DLT
  → record metrics and limitations privately
```

## Run an authorized private analysis

```powershell
python src/run_dlc.py `
  --action analyze `
  --config-yaml path\to\private\config.yaml `
  --video path\to\private\view-a.mp4 `
  --video path\to\private\view-b.mp4 `
  --output-dir path\to\private\runs\dlc `
  --execute
```

For training, use `--action train` with a private config and a declared `--maxiters`. The runner prints a dry-run summary unless `--execute` is present. Version, backend, split and snapshot must be captured in the private manifest before any result is interpreted.

## Citations

- [DeepLabCut official repository](https://github.com/deeplabcut/DeepLabCut)
- [Mathis et al. (2018), Nature Neuroscience, DOI 10.1038/s41593-018-0209-y](https://doi.org/10.1038/s41593-018-0209-y)
- [Nath et al. (2019), 3D DeepLabCut protocol, DOI 10.1038/s41596-019-0176-0](https://doi.org/10.1038/s41596-019-0176-0)

