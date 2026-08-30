#!/usr/bin/env python3
"""Audit a repository tree before a public push.

The audit is conservative: forbidden artifact suffixes fail, while the prose
scan only looks for local machine paths, credentials-like tokens and emails.
It is safe to run on the repository because it never follows the source data.
"""

from __future__ import print_function

import re
import sys
from pathlib import Path


FORBIDDEN_SUFFIXES = {
    ".avi", ".mp4", ".mov", ".mkv", ".dat", ".cal", ".3d", ".trc",
    ".pbix", ".exe", ".dll", ".pt", ".pth", ".h5", ".onnx", ".pickle",
    ".pkl", ".mat", ".npy", ".npz", ".csv", ".tsv", ".xlsx", ".xls",
    ".docx", ".pptx",
}
FORBIDDEN_NAME_PARTS = ("proof", "database", "calibration", "weights", "checkpoint")
PRIVATE_PATH = re.compile(r"(?i)(?:\b[a-z]:[\\/]|/users/|/home/|/mnt/)")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SECRET = re.compile(r"(?i)\b(?:ghp|github_pat|sk)-[A-Za-z0-9_-]{12,}\b")
SKIP_CONTENT = {"src/audit_public_release.py", "src/validate_manifest.py"}


def relative(path, root):
    return path.relative_to(root).as_posix()


def iter_files(root):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = relative(path, root)
        if rel == ".git" or rel.startswith(".git/") or rel.startswith("work/") or rel.startswith("__pycache__/") or "/__pycache__/" in rel:
            continue
        yield path, rel


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    if not root.is_dir():
        print("FAIL: release root does not exist: {}".format(root))
        return 2

    findings = []
    for path, rel in iter_files(root):
        lower = rel.lower()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append("forbidden artifact type: {}".format(rel))
        if any(part in lower for part in FORBIDDEN_NAME_PARTS):
            findings.append("forbidden artifact name: {}".format(rel))
        if rel in SKIP_CONTENT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if PRIVATE_PATH.search(text):
            findings.append("private machine path in {}".format(rel))
        if EMAIL.search(text):
            findings.append("email address in {}".format(rel))
        if SECRET.search(text):
            findings.append("credential-like token in {}".format(rel))

    if findings:
        print("FAIL: public release audit found {} issue(s)".format(len(findings)))
        for item in findings:
            print(" - {}".format(item))
        return 1

    print("PASS: public release audit found no blocked artifacts, local paths, emails or credentials")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
