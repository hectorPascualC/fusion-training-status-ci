# Fusion beta V2 — authorized one-shot public cloud packaging request

- Requested: 2026-10-18 (Worker 04; the account owner confirmed the GitHub secrets have been configured).
- Use source: private `hectorPascualC/fusion-training-status` branch `performance/master-audit` at the commit resolved by the workflow.
- Publish only to a PRIVATE Release in the source repository.
- Expected assets: `FusionTrainingStatus-SignedPrivateBeta-V2.iq` and `FusionCompanion-Android-Worker04-debug.apk`.
- Preserve the persistent encrypted signing key in the PRIVATE repository.
- If any credential or compile check fails, do not publish an unverified release.
- This request does not authorize a public Connect IQ release, external publication of sources, paid runners, or a production-ready declaration.
