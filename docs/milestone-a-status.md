# Milestone A — phases 1–5 delivered to isolated preview

Scope: account-level entitlements, assigned-course teachers, no production cutover. UAT waived by Nicola.

1. Identity/security: owner/teacher login, password provisioning/reset, enabled-account checks, assigned resource scope, persistent session revocation, rate limit. Backend suite passes; actual public-preview browser proves login, provisioning, logout-all and teacher financial denial.
2. Authoring/catalog: course/chapter/lesson, publication, image validation, worksheet upload/delete, order/search/favorites. Browser tests cover authoring desktop/mobile; source and integration regressions cover catalog/navigation.
3. Commerce: existing package/voucher/single pending/expiry/provider reconciliation/idempotency/grants preserved. All backend suites pass against isolated PostgreSQL; external payment provider mocked, no real charge.
4. Learning: notes/bookmarks ownership and expiry, resume/lifecycle, navigation/completion. Desktop/mobile fixture tests and actual preview browser pass notes/completion. Teacher artwork review now scoped in list/image/feedback; finance/gallery/delete excluded. PostgreSQL tests prove assignment revocation; public browser proves upload→teacher score/feedback→member readback.
5. Integration/preview: 40 backend tests pass, build 10 routes, desktop/mobile public URL tested without API response fixtures. Database dump/restore with course/lesson/account counts verified. Preview: https://machinery-considerations-writings-brain.trycloudflare.com (temporary process-bound tunnel). No UAT required.

Verification limits: no production deployment, real Midtrans/SMTP transaction, or human visual acceptance. DOM overflow and JS errors checked; screenshot decoder unavailable. Preview uses synthetic records only. Credentials remain local in /tmp/nala-lms-preview-access.json (0600), never in Git/chat.

Run backend tests with MEMBER_TEST_DATABASE_URL exclusively at 127.0.0.1:55439/member_test. Start server/lms-preview.js with LMS_PREVIEW_ORIGIN; build frontend with matching PUBLIC_API_URL. Run scripts/qa-lms-integrated.py using LMS_QA_URL for public browser acceptance. Preview has no production mail/payment adapters.
