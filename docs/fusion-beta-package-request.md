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

## 2026-10-19 — retry RX diagnostic beta after single-use assertion comment restoration

Source security guard re-established the literal single-use marker while preserving one-time request IDs; rerun full public cloud packaging from latest performance/master-audit. Previous run 39322307199 failed at static transport-security before build; do not reuse its outputs.

## 2026-10-19 — final retry after Garmin typed RX error callback

Previous public run 39322443644 PASSED source, Android JUnit/lint/APK audits and signer recovery but failed Garmin compilation at FusionPhoneBridge.mc line 35: onPhoneMessageError err must be typed Comm.PhoneAppMessageError (not Any). Private source corrected and source guard updated. Rebuild signed beta with the same persistent signer; publish only to PRIVATE Release. Verify no errors.

## 2026-11-04 — Fēnix 8 RX: WRONG TYPE fix

Compile and privately package a new signed Fēnix 8 stable beta V2 from performance/master-audit. Live watch RX: WRONG TYPE, NO CACHE despite Android SUCCESS and computed real Fitbit/Garmin inputs. Root cause in Monkey C is string identity vs content equality across type check, request ID, payload status/confidence/freshness and screen color. Strict schema/anti-replay checks preserved. Source includes regression guard validate_watch_wire_string_equality.py, no Android functional changes.

Run full audit/test, signed Garmin IQ using **existing persistent signer** and private Release, no public artifacts. See private docs/WORKER04_WATCH_RX_WRONG_TYPE_20261104.md.

## 2026-11-04 — correct static guard and rerun Garmin string-value beta

Previous beta run #41843630897 rejected a valid local extraction `response.get("requestId")` because new static test unintentionally banned any call, rather than banning only `!= _pendingRequestId`. New source commit corrects this assertion without changing the newly fixed watch code. Re-run complete signed private packaging and security checks.

## 2026-11-04 — Fēnix watch BUILD 1104D type-envelope diagnostic

User reports no change after previous correction. The last source bundle may not have been installed. Build from latest private performance/master-audit with visible Data Sources fingerprint **BUILD 1104D**; distinguish RX missing/nontext/echo/unknown type; support strictly validated direct-payload envelope only if full 17-field schema, request ID, timestamps and anti-replay all PASS. No Android, algorithm, permissions, UUID or signing-key changes. Validate all source and Gradle/Garmin stages and upload only to private Release. The private audit is docs/WATCH_RX_DIAGNOSTIC_BUILD_1104D.md.

## 2026-11-04 — Fusion UI V3 full six-screen renderer build/audit

Build an immutable signed **private** beta using the existing stable V2 UUID/key and latest `performance/master-audit`. User requested full functional implementation, not a mockup. Private source adds `garmin/source/FusionVisualRenderer.mc`, activated by FusionStatusView on all six pages; data-faithful recovery semicircle, REAL seven-day activity chart, correct LOW load classification at 0.26, compact WHY and Data Sources. All Android/Health Connect/sync protocols unchanged.

Audit: `scripts/validate_visual_v3.py` plus all original code/security/performance guards, Android tests/lint/build, monkeyc Garmin SDK 9.2.0 signing/export, private release checksum. Do not publish private sources or artifacts in this public repo. Physical Fēnix 8 acceptance remains pending until Garmin Developer beta upload/update.

## 2026-11-04 — V3 layout hotfix after real Garmin emulator QA

User requested a fully readable V3 design rather than source-only success. Six **actual Garmin emulator** page captures of the first V3 release showed multiple clipped labels and overlaps despite green compilation. Private code `FusionVisualRenderer.mc` now fixes adaptive numeric fonts, full OVERVIEW status, short factual training chart title, recovery radial-gauge text spacing, TRAINING load ratio and LOW label, TRENDS caption/footer, Data Sources diagnostic rows, and complete two-line engine WHY rationale.

Run **full** security/source/Android CI and stable signed private Garmin IQ packaging from the latest performance/master-audit commit. Verify the private asset digest. New six-page visual QA workflow runs separately with synthetic data and must be audited before declaring readiness. No Garmin physical hardware claims until actual watch update.

## 2026-11-04 — Fusion V3 final polish compile after second simulator inspection

Second real Garmin simulator captures improved Recovery, Overview, WHY, Data Sources. New private source includes final round-display polishing: move recovery radial arc clear of title, compact Overview caption and actual recovery zone, shift mini training bars away from numbers, move Data Source status dots outside label text, and allow complete source WHY clause with width-measured 348 px limit. Training and Trends were improved in prior pass with shorter labels / no footer collisions.

Execute complete source security/performance/Android audit, pinned Garmin SDK 9.2.0 compiler, **same persistent beta signing key and UUID**, PRIVATE binary-only Release. Preserve Health Connect/sync protocol. Physical watch acceptance pending owner's update through Connect IQ.

## 2026-11-04 — final V3 Training legibility correction

Actual simulator screenshots verified 5/6 page designs after first pass. Training remained clipped at "CHRO..." and LOW LOAD touched footer. Current private performance/master-audit fixes: allow 160px CHRONIC caption measured at FONT_XTINY, raise LOW LOAD caption from h*.725 to h*.69, and gates both layout assertions in validate_visual_v3.py. Earlier fixes include recovery arc separation, concise overview summary, Data Sources status dots no longer on letters, and longer real WHY clause.

Run complete private source/Android/security/Garmin compile, same stable beta UUID and developer signer, publish PRIVATE binary release only. No new Android permission/sync changes. User must upload Garmin IQ to beta listing after full audit.

## 2026-11-04 — V3 final Trends visual polish

Reviewed real Garmin simulator screenshot of Trends after six-page gallery run 41883366600: real weekly minute bars and ACTIVE 2/7 are correct and readable, but ACTIVE caption touched FRESH divider. Private source has a final .735 -> .710 vertical shift for its caption plus regression assertion. Keep actual data and chart untouched. Build exact latest `performance/master-audit` with full source/Android/security tests, same encrypted persistent stable beta signer and private-only .iq release. The owner will update in Connect IQ, no Android reinstall.

## 2026-11-05 — Fusion V3 six-screen integrated signed beta

Production watch view now dispatches to the V3 source-faithful renderer (Overview/Recovery/Training/Trends/Data Sources/Why). The first exploratory build found a duplicate renderer declaration; private source commit d4ef5da1 fixes it. Build using persistent same-key private beta signer, run source/Android/Monkey C/security audits, and upload IQ+APK privately. Preserve real Health Connect and Garmin data; no synthetic fixture in release. Real-device Garmin Connect IQ update and screenshot acceptance remain manual.

## 2026-11-05 — V3 final pixel-spacing correction and signed package retest

The six-page Garmin 454px visual simulator run #41982904354 succeeded. Manual pixel inspection found loadRatio 0.26 intersecting the Training band and Recovery zone too close to confidence. Source fix e6b6637d moves the ratio value up and creates space under MODERATE. Build from the latest performance/master-audit including this fix, validate full repository/Android/Garmin stack and upload fresh same-signature IQ into PRIVATE release only. No watch UUID or Android schema change.

## 2026-11-05 — final precise Garmin V3 typography spacing fix

Visual re-audit of signed-pending source e6b6637d showed ratio 0.26 was shifted too near its label and MODERATE too near score 56. Private source 8dcf10b7 applies balanced 454px typography positions. Repeat whole public signed beta pipeline using existing RSA beta key. Verify source, Android and Connect IQ compile, private IQ assets and full V3 six-page simulator.

## 2026-11-05 — Visual V4 approved-mockup fidelity fix, exact signed beta

User reported that V3 real-device display did not match approved concept images. The private branch now implements the actual concept-style rounded status pill, three metric cards, wide recovery arc + score capsule, training load-zone bar, real seven-day training chart/delta, three explanation cards, and compact footer. No fabricated stress, sleep, Body Battery, HRV trends or optimistic statuses. Passed six-page synthetic Garmin simulator screenshots in public workflow 42016581355; re-run full secure source/Android/Garmin checks, export using SAME persistent signing key and unchanged UUID, and upload **only** to PRIVATE GitHub Release. Do NOT auto-publish to Garmin Connect IQ public store. Existing Android Companion remains correct; no mobile APK install needed.
