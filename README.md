# Fusion Training Status — public GitHub Actions runner

This **public repository does not publish private Fusion source code**. It runs checks on standard public GitHub-hosted runners through a temporary, read-only checkout of the private repository **hectorPascualC/fusion-training-status**, default engineering branch **ui/v5-device-alignment-20261106** (V5 test work). The signed beta packaging workflow still targets **performance/master-audit** until explicit release approval. The source, Git history, private signing keys, APKs and PRGs are not committed or uploaded here.

## One-time activation

1. Create a [fine-grained GitHub personal access token](https://github.com/settings/personal-access-tokens/new), scoped to **only** the private repository **hectorPascualC/fusion-training-status**, with **Contents: Read-only** and no write/admin permissions. Set an expiry.
2. In this public repository open **Settings → Secrets and variables → Actions → New repository secret**. Name it **FUSION_PRIVATE_READ_TOKEN** and paste the token **there only**, never in chat or in a commit. Restrict who can edit workflows and protect main: a workflow editor could extract secrets.
3. Open **Actions → Fusion engineering (private ephemeral checkout) → Run workflow**. A schedule also checks every six hours (subject to GitHub scheduling delays).
4. Review jobs **source-audit**, **android**, **garmin-engineering**, **audit-result**. A green result only validates engineering checks; it does not prove physical-device or production signing acceptance.

## Safety / cost

- Standard public GitHub-hosted runners avoid the private 2,000-minute Actions allowance. No premium runner, build-cache upload or artifact upload is used. Separate billing policies can still apply.
- Public workflow logs are visible. Never print FIT, sleep/HRV, passwords, tokens or private source in CI logs.
- No pull-request trigger, no public commit of private source, no private Git history copy. Temporary checkouts are discarded when jobs finish.
- **Until FUSION_PRIVATE_READ_TOKEN is installed, real execution is BLOCKED**, not PASS.
- Garmin job uses pinned unofficial test device metadata only. Official Garmin package, real watch timing/memory/battery and release signing are still separate blockers.

Audit progress: [AUDITS/PHASE_PROGRESS.md](AUDITS/PHASE_PROGRESS.md).

## Fusion V5 autonomous audit and bounded repair

[Autonomous supervisor workflow](.github/workflows/fusion-autonomous-v5.yml) runs at **07:17 and 19:17 UTC** every day, and can also be started with **Run workflow**. This is GitHub-hosted background execution, not a promise that ChatGPT runs while the chat is closed.

It checks out the private V5 feature branch ephemerally, executes the pre-approved deterministic geometry repair rules in `scripts/fusion_auto_repair.py` (private), then requires the real source/security tests. Its protected writer may persist **only** `garmin/source/FusionVisualRenderer.mc` and `garmin/source/FusionStatusView.mc` back to that same private feature branch with remote-SHA conflict checks. Prefer a separate fine-grained `FUSION_PRIVATE_AUTOFIX_TOKEN` with private-repository Contents Write and no other permissions; if absent, the previously configured `FUSION_PRIVATE_RELEASE_TOKEN` is the fallback. The write token is never used when no repair is needed.

On source PASS, the supervisor dispatches the existing engineering workflow (Android + Garmin) and the real six-page Connect IQ simulator workflow. The simulator now calls `scripts/fusion_simulator_pixel_gate.py` (private) to require a complete native simulator screenshot and colored primitives on each page; compile SUCCESS alone is not enough. Failed **infrastructure installation** is retried once. Unknown compilation, semantic, simulator or pixel failures block the cycle and are **not** silently “fixed” by speculative AI edits. The next schedule runs a new check. Each controller run writes a link-rich audit summary to GitHub Actions.

**Acceptance rules:** CI PASS is an engineering + visual-smoke PASS using synthetic fixture values. It does **not** prove pixel-for-pixel equality to the original sketch, real user physiological data or physical Fēnix 8 acceptance. No auto-publication, signing, release creation or Garmin Connect IQ upload is wired into this controller. The existing signed beta remains unchanged.

[Controller executions](https://github.com/hectorPascualC/fusion-training-status-ci/actions/workflows/fusion-autonomous-v5.yml) · [Six-page real simulator](https://github.com/hectorPascualC/fusion-training-status-ci/actions/workflows/fusion-v3-final-gallery.yml)
