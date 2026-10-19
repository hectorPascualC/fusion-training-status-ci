# Fusion beta V2 — authorized one-shot public cloud packaging request

- Requested: 2026-10-18 (Worker 04; the account owner confirmed the GitHub secrets have been configured).
- Use source: private `hectorPascualC/fusion-training-status` branch `performance/master-audit` at the commit resolved by the workflow.
- Publish only to a PRIVATE Release in the source repository.
- Expected assets: `FusionTrainingStatus-SignedPrivateBeta-V2.iq` and `FusionCompanion-Android-Worker04-debug.apk`.
- Preserve the persistent encrypted signing key in the PRIVATE repository.
- If any credential or compile check fails, do not publish an unverified release.
- This request does not authorize a public Connect IQ release, external publication of sources, paid runners, or a production-ready declaration.

## 2026-10-18 — Android Health Connect permissions hotfix

Trigger exactly one updated private beta+APK package build on the public cloud runner, consuming **no private GitHub Actions minutes**.
Private source includes PermissionsRationaleActivity, Android 14+ VIEW_PERMISSION_USAGE alias, visible permission result/errors and diagnostics-preserving UI.
Verify source validators, Android tests/lint/build, merged-manifest permission gate, IQ packaging and final private Release assets. Garmin watch code/signing key/UUID remain stable.
See private `docs/WORKER04_HEALTH_CONNECT_PERMISSION_FIX.md`.

## 2026-10-19 — Fēnix 8 RX/NO CACHE diagnostic beta

Trigger exactly one public cloud beta package build from the private performance master branch, using persistent signing key and private Release only. No repository or token leak.

Physical evidence: Android reports Garmin payload SUCCESS, but watch DATA SOURCES shows PHONE: NO CACHE. Private source now reports short states on watch (RX: STORED / RX: INVALID DATA / RX: ID MISMATCH / RX: FORMAT / TX: SENT / TX: FAILED / RX: DELIVERY ERR), supports only one-entry bounded array envelopes, preserves strict FusionStore validation and Garmin protocol, and adds source guard.

Ensure source, Garmin SDK compile, Android tests/security and signed private release all PASS. See private docs/WORKER04_WATCH_RX_AUDIT.md.
