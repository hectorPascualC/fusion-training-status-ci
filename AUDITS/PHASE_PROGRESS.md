# Public GitHub Actions migration — phase audits (2026-10-18)

| Phase | Evidence | Result |
|---|---|---|
| 01 — Repository boundary | New repo fusion-training-status-ci verified PUBLIC; original fusion-training-status verified PRIVATE; separate Git history. | PASS |
| 02 — Privacy | Read-only private checkout, no source push, no PR trigger, no cache/artifact upload; disposable Garmin signing key; no private workflow execution. | PASS_STATIC (runtime logs pending) |
| 03 — Workflow engineering | Manual/scheduled workflow, three checks plus aggregate fail-closed gate, SHA-pinned GitHub Actions, pinned SDK/Gradle, all checking the same immutable private source commit SHA. | PASS_STATIC (not yet executed) |
| 04 — Credential activation | FUSION_PRIVATE_READ_TOKEN must be configured in public Actions Secrets by the owner. | BLOCKED |
| 05 — Live proof | Need green public Actions jobs, confirm no private minute use or leaked log data; hardware/official Garmin acceptance separate. | PENDING |

Do not label live CI or physical Garmin acceptance PASS without successful measured evidence.

## First live public-run evidence — 2026-10-18

**Run:** https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39120967478

- Public-run event: trusted `push` to `main`; no pull-request trigger, no source publication.
- Public Actions result: **COMPLETED / SUCCESS** at 2026-10-18 10:55:44 UTC.
- Private commit audited: `d294af35fa8832392ae65a410ad2b2dc2c1fb1e0` (`performance/master-audit`); downstream jobs use exactly this SHA.
- Source audit: **PASS** (repository, security, data, UI, performance validators and secret scan).
- Android: **PASS** (Gradle unit tests, lint, debug/release build and APK security). Release unsigned APK **678,543 B**, release DEX **624,284 B**; under the 2 MiB regression ceiling.
- Garmin engineering: **PASS** (Monkey C compiler 9.2.0, pinned engineering-only `fenix847mm` device metadata, disposable signing key); generated PRG **26,204 B**. This is *not* a production-signed Garmin package.
- Aggregate `audit-result`: **PASS**, all three jobs succeeded.
- Public log sample check: zero literal GitHub PATs, private-key PEM headers or Google API key tokens matched in the checked public job logs. This is **not** a guarantee against every possible sensitive log format.
- Public git tree contains exactly `README.md`, `AUDITS/PHASE_PROGRESS.md`, and `.github/workflows/fusion-private-source-ci.yml`; original Fusion private repository remains private.
- A manual trigger and six-hour scheduled trigger remain enabled. A narrow trusted `push` trigger for edits to the public workflow file also exists.

**Phase audit update:**
- Phase 01 repository boundary: **PASS LIVE**.
- Phase 02 privacy/static policy: **PASS LIVE FOR FIRST RUN** (public file inventory, ephemeral read checkout, selected log secret-pattern scan).
- Phase 03 CI engine: **PASS LIVE**.
- Phase 04 token/authentication: **PASS LIVE** (actual checkout and source audit succeeded).
- Phase 05 public engineering regression: **PASS LIVE** (Android, Garmin and aggregate all green).

**Not passed or claimed:** official Garmin device-package authentication, production-signed Garmin beta V2, physical watch navigation/heap/battery/latency and final `v1.0.0` release. These continue as separate private acceptance gates.
