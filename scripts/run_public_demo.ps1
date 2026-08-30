param(
    [int]$NormalizedPoints = 101,
    [string]$PythonExecutable = "python"
)

$ErrorActionPreference = "Stop"
$python = $PythonExecutable

Write-Host "[1/8] validating public manifest"
& $python src/validate_manifest.py examples/manifest.example.json

Write-Host "[2/8] auditing public tree"
& $python src/audit_public_release.py .

Write-Host "[3/8] running numerical/unit tests"
& $python -m unittest discover -s tests -v

Write-Host "[4/8] running synthetic DLT reconstruction"
& $python src/reconstruct_json.py examples/dlt-input.example.json

Write-Host "[5/8] normalizing synthetic curve to $NormalizedPoints points"
& $python src/normalize_window.py examples/normalize-input.example.json --points $NormalizedPoints

Write-Host "[6/8] running the synthetic trajectory quality gate"
& $python src/reconstruct_json.py examples/dlt-trajectory.example.json --max-reprojection-px 5

Write-Host "[7/8] deriving synthetic kinematics"
& $python src/derive_biomechanics.py examples/biomechanics-input.example.json

Write-Host "[8/8] expanding the five-model DeepLabCut benchmark plan"
& $python src/dlc_benchmark_plan.py --config configs/dlc_benchmark.example.json

Write-Host "PASS: public demo complete; no private video, database or model was opened"
