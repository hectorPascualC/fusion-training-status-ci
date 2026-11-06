#!/usr/bin/env python3
"""Persist allowlisted, validated V5 geometry repairs to the private feature branch."""
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PRIVATE = "hectorPascualC/fusion-training-status"
BRANCH = "ui/v5-device-alignment-20261106"
ALLOWED = {"garmin/source/FusionVisualRenderer.mc", "garmin/source/FusionStatusView.mc"}

def api(*args, payload=None):
    argv = ["gh", "api", *args]
    temporary = None
    if payload is not None:
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
            json.dump(payload, handle)
            temporary = handle.name
        argv += ["--input", temporary]
    try:
        return json.loads(subprocess.check_output(argv, text=True))
    finally:
        if temporary:
            Path(temporary).unlink(missing_ok=True)

def git(folder, *args):
    return subprocess.check_output(["git", "-C", str(folder), *args], text=True).strip()

def persist(root):
    if os.getenv("GITHUB_REPOSITORY") != "hectorPascualC/fusion-training-status-ci":
        raise RuntimeError("Wrong runner repository")
    changes = git(root, "diff", "--name-only").splitlines()
    if not changes:
        print("No deterministic fixes; no private write token used")
        return
    if not set(changes).issubset(ALLOWED):
        raise RuntimeError("Changed path outside exact UI source allowlist")
    if not os.getenv("GH_TOKEN"):
        raise RuntimeError("Known safe fix found but private write token not configured")
    head = git(root, "rev-parse", "HEAD")
    current = api(f"repos/{PRIVATE}/git/ref/heads/{BRANCH}")
    if head != current["object"]["sha"]:
        raise RuntimeError("Private branch advanced during audit; refusing overwrite")
    for path in changes:
        before = git(root, "rev-parse", f"HEAD:{path}")
        remote = api(f"repos/{PRIVATE}/contents/{path}?ref={BRANCH}")
        if remote["sha"] != before:
            raise RuntimeError("Remote file advanced during audit; refusing overwrite")
        raw = (root/path).read_bytes()
        if len(raw)>100000:
            raise RuntimeError("Unexpectedly large source file")
        payload = {
            "branch": BRANCH, "sha": before,
            "message": "fix(ui): bounded autonomous V5 geometry regression repair",
            "content": base64.b64encode(raw).decode("ascii"),
        }
        result = api("-X", "PUT", f"repos/{PRIVATE}/contents/{path}", payload=payload)
        if not result.get("commit", {}).get("sha"):
            raise RuntimeError("No GitHub commit confirmation")
        print(f"Persisted allowed fix {path}: {result['commit']['sha'][:12]}")
    print("All automated changes restricted to private V5 feature branch; beta unchanged")

if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: fusion_commit_layout.py PRIVATE_CHECKOUT")
    try:
        persist(Path(sys.argv[1]).resolve())
    except (RuntimeError, subprocess.CalledProcessError, KeyError, ValueError) as error:
        raise SystemExit("BLOCKED private write safety: " + str(error))
