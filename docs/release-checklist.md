# Public release checklist

Run this checklist before adding a new public artifact or changing the scope.

- [ ] The artifact explains the method or provides a synthetic example.
- [ ] It contains no participant-level data, frame-level coordinates or source filenames.
- [ ] It contains no video, calibration, executable, model-weight or result artifact.
- [ ] It contains no local path, email, phone number, credential or unreviewed metadata.
- [ ] The source/author attribution is explicit and scoped.
- [ ] A version/commit or manifest field explains where the artifact belongs.
- [ ] `python src/validate_manifest.py examples/manifest.example.json` passes.
- [ ] `python src/audit_public_release.py .` passes.
- [ ] The interactive guide still works at desktop and mobile widths.
- [ ] The change has a focused commit message.

