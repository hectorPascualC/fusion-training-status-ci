#!/usr/bin/env python3
"""Background Fusion V5 auditor: real engineering + six-page Garmin simulator.

Retries a known transient infrastructure failure once; never masks a source
failure, runs AI-generated patches, or publishes beta binaries.
"""
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REPO = "hectorPascualC/fusion-training-status-ci"
WORKFLOWS = (
    ("engineering", "fusion-private-source-ci.yml"),
    ("simulator", "fusion-v3-final-gallery.yml"),
)
INFRA_STEPS = (
    "Install headless simulator dependencies",
    "Install pinned Connect IQ SDK 9.2.0",
    "Install pinned mirror device metadata and fonts",
    "Install verified Connect IQ SDK manager",
)

def api(route, method="GET", fields=None):
    args = ["gh", "api", "-X", method, route]
    for key, val in (fields or {}).items():
        args += ["-f", f"{key}={val}"]
    output = subprocess.check_output(args, text=True).strip()
    return json.loads(output) if output else {}

def runs(workflow):
    path = f"repos/{REPO}/actions/workflows/{workflow}/runs?per_page=25&event=workflow_dispatch"
    return api(path).get("workflow_runs", [])

def await_new_id(workflow, existing):
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        found = [entry["id"] for entry in runs(workflow) if entry["id"] not in existing]
        if found:
            return max(found)
        time.sleep(7)
    raise RuntimeError("No workflow run created for " + workflow)

def failures_for(run_id):
    response = api(f"repos/{REPO}/actions/runs/{run_id}/jobs?per_page=100")
    failures = []
    for job in response.get("jobs", []):
        if job.get("conclusion") != "failure":
            continue
        failures.append({
            "name": job["name"],
            "steps": [item["name"] for item in job.get("steps", [])
                      if item.get("conclusion") == "failure"],
        })
    return failures

def transient_only(failures):
    return bool(failures) and all(
        job["steps"] and all(
            any(step.startswith(prefix) for prefix in INFRA_STEPS)
            for step in job["steps"]
        )
        for job in failures
    )

def monitor(run_id, label, max_minutes=69):
    start = time.monotonic()
    did_retry = False
    while time.monotonic() - start < 60 * max_minutes:
        run = api(f"repos/{REPO}/actions/runs/{run_id}")
        if run.get("status") == "completed":
            if run.get("conclusion") == "success":
                print(f"{label}: PASS, attempt {run.get('run_attempt')}", flush=True)
                return {"state":"PASS", "run_id":run_id, "url":run["html_url"]}
            failures = failures_for(run_id)
            if not did_retry and transient_only(failures):
                print(f"{label}: infrastructure-only failure, one bounded retry", flush=True)
                api(f"repos/{REPO}/actions/runs/{run_id}/rerun-failed-jobs", method="POST")
                did_retry = True
                time.sleep(20)
                continue
            return {"state":"BLOCKED", "run_id":run_id, "url":run["html_url"],
                    "reason":"Persistent or non-infrastructure CI failure",
                    "failed_jobs":failures}
        time.sleep(25)
    return {"state":"BLOCKED", "run_id":run_id,
            "url":f"https://github.com/{REPO}/actions/runs/{run_id}",
            "reason":"Bounded timeout, next scheduled cycle can retry"}

def main():
    if os.getenv("GITHUB_REPOSITORY") != REPO or not os.getenv("GH_TOKEN"):
        raise RuntimeError("Unauthorized runner or no Actions token")
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    state = "PASS"
    audits = {}
    try:
        # Dispatch both before polling, for real six-page parallel coverage.
        for label, workflow in WORKFLOWS:
            before = {item["id"] for item in runs(workflow)}
            api(f"repos/{REPO}/actions/workflows/{workflow}/dispatches",
                method="POST", fields={"ref":"main"})
            run_id = await_new_id(workflow, before)
            audits[label] = {"run_id":run_id, "state":"STARTED",
                             "url":f"https://github.com/{REPO}/actions/runs/{run_id}"}
            print(f"{label}: {audits[label]['url']}", flush=True)
        for label, _ in WORKFLOWS:
            audits[label] = monitor(audits[label]["run_id"], label)
            if audits[label]["state"] != "PASS":
                state = "BLOCKED"
    except (RuntimeError, subprocess.CalledProcessError, ValueError, KeyError) as err:
        state = "BLOCKED"
        audits["controller"] = {"state":"BLOCKED", "reason":str(err)}
    result = {
        "date_utc":started, "status":state, "audits":audits,
        "release":"NOT PUBLISHED",
        "physical_watch_acceptance":"PENDING OWNER",
        "sketch_exactness":"NOT AUTOMATICALLY CERTIFIED",
    }
    print("FUSION_AUTONOMOUS_AUDIT=" + json.dumps(result,sort_keys=True), flush=True)
    file = Path(os.getenv("GITHUB_STEP_SUMMARY", "/tmp/fusion_summary.md"))
    file.parent.mkdir(parents=True,exist_ok=True)
    with file.open("a",encoding="utf-8") as output:
        output.write(f"## Fusion V5 autonomous CI — {state}\n\n")
        output.write(f"Cycle started (UTC): {started}\n\n")
        for label, item in audits.items():
            url = item.get("url")
            output.write(f"- {label}: **{item['state']}**")
            if url:
                output.write(f" — [run]({url})")
            output.write("\n")
        output.write("\nPrivate beta: **not published**. Physical-device/sketch acceptance is separate.\n")
    return 0 if state=="PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
