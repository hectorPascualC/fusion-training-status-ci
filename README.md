# Fusion Training Status — public GitHub Actions runner

This **public repository does not publish private Fusion source code**. It runs checks on standard public GitHub-hosted runners through a temporary, read-only checkout of the private repository **hectorPascualC/fusion-training-status**, branch **performance/master-audit**. The source, Git history, private signing keys, APKs and PRGs are not committed or uploaded here.

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
