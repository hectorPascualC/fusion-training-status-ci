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

## Worker 3 resumed audit — 2026-10-18

Two audited feature-branch public runs successfully validated Fusion watch UI/performance and data correctness:

| Stage | Private source | Public run | Source | Android/JUnit/lint/APK | Garmin compiler | Aggregate |
|---|---|---|---|---|---|---|
| UI render/unused Garmin snapshot | `d5e3c80a203ce1db394614cc704f8d301d2a147d` | [39121770414](https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39121770414) | PASS | PASS | PASS | PASS |
| Seven UTC calendar-date frequency bound | `9612016ef25a46d09387d4aea760802883d70ccf` | [39121989825](https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39121989825) | PASS | PASS | PASS, PRG 26,220 B | PASS |

The second Android run passed the added eight-UTC-date JUnit regression, lint and release APK security; its unsigned release APK was 678,667 bytes. The feature branch was fast-forwarded into private `performance/master-audit` at audit commit `0a33c4cae2c0072e886794af0092184cda127c8a`.

**No private-release/physical PASS:** an engineering PRG built with test device metadata and a throwaway key is not a signed Garmin release; on-watch frame time, memory, battery and actual user Health Connect permission/transport acceptance remain untested.

### Private Actions quota containment

The private branch received an additional workflow-only change `8a2d5ca8ec102430170550573bad05b06f83a54b` to remove automatic private-runner triggers for performance updates and make private Android beta packaging manually dispatched. Public CI checks that policy. This avoids spending the private 2,000-minute allowance on performance-branch pushes. The latest policy-enforcement public run is subject to actual CI confirmation; do not claim PASS until completed.

## Worker 3 / performance branch — Final phase audit (2026-10-18)

**Final run:** https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39123149906  
**Private source validated:** `hectorPascualC/fusion-training-status@44d15b919a818ca977109a92ecc8a8765ef75387`.

- Phase 01 — Trust boundary: **PASS**; original repo private, public Git repo has only CI code and audit docs, private source checked out ephemerally.
- Phase 02 — Watch UI/performance: **PASS_ENGINEERING**; unused Garmin profile snapshot reads removed; numeric cells width-bounded; Fēnix 8 Monkey C engineering PRG 26,220 bytes.
- Phase 03 — Data correctness: **PASS_ENGINEERING**; eight-UTC-calendar-dates regression covered by JUnit; `frequency7Day` is constrained to 0–7 while rolling training volume remains unchanged.
- Phase 04 — Android security/performance: **PASS_ENGINEERING**; unit tests, lint, release APK (678,667 bytes), DEX (624,408 bytes) and binary security successful.
- Phase 05 — GitHub Actions quota protection: **PASS**. The private performance branch has no automatic private CI push runner. Private Android beta packaging requires a deliberately created/modified request marker (`docs/PRIVATE_ANDROID_COMPANION_BUILD_REQUEST.md`) or manual dispatch when available. Actual private runs stopped after the old pre-migration push; the public run successfully validated the migrated audit contract.
- Phase 06 — Official Fēnix 8/Health Connect physical acceptance and signed V2: **BLOCKED**; not simulated as PASS.

The migration briefly produced failed runs `39122492581` and `39122898176`–`39123073239`; those exposed an obsolete private-branch requirement and a duplicate YAML document, both corrected. Latest all-jobs-green evidence is `39123149906`.

The public workflow remains scheduled every six hours (subject to GitHub scheduling delay). This schedule runs validations but does **not** autonomously implement future code changes.

## Fusion phase 05 — seven-day real-training Trends final engineering closeout (2026-10-18)

**Source integration:** private `performance/master-audit` at `07ce02d9bb99b631fa3d69b09ee74e2a4dd89de5` passed the [public regression #39126894526](https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39126894526), all four jobs (repository/data/security, Android JUnit/lint/release APK, Garmin 9.2.0 engineering PRG, aggregate) **SUCCESS**.

- Versioned transport: old 16-field v1 continues to work with supported old watch clients; v2 uses exactly 17 fields, with bounded `dailyMinutes7` from watch-reported Garmin workouts. Unknown daily coverage is not fabricated as zero when the 64-activity limit is reached.
- UI: v2 Trends shows seven observed UTC-date bars, compact ACTIVE DAYS label, untruncated FRESH/ST​ALE/EXPIRED footer; v1 cache retains two-period comparison.
- Test-only real simulator visual: [#39126589596](https://github.com/hectorPascualC/fusion-training-status-ci/actions/runs/39126589596) **SUCCESS**, visually reviewed, no black Error-popup overlay. Original screenshot archived in **private** repository [phase05-trends-v2-SAMPLE-polished.png](https://github.com/hectorPascualC/fusion-training-status/blob/performance/master-audit/docs/screenshots/phase05-trends-v2-SAMPLE-polished.png), with synthetic values only.
- Release binary measurements: Garmin engineering PRG 27,116 B, unsigned Android release APK 679,383 B.
- Private Actions: no new automatic performance-branch workflow run; public CI retains the six-hour regression schedule.
- Remaining **BLOCKED**: physical Fēnix 8 user acceptance (memory, startup, render, battery, navigation), real phone/Health Connect user data and pairing, official Garmin device package and signed V2. Do not claim release readiness or invent real physiological series.

An independent 18-field experimental branch is not merged and must not supersede the validated 17-field contract without a separate audited migration.
