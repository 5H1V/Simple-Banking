# Simple Banking — Implemented Features

This update adds the five planned workstreams to the uploaded project baseline.

## 1. Transfers between accounts

- Customer dashboard account rows include a Transfer action when the user owns at least two accounts.
- The source account is preselected when the user opens the transfer page from an account row.
- Source and destination dropdowns list the signed-in user's accounts and prevent selecting the same account twice.
- A review/confirmation step precedes submission.
- `POST /api/accounts/transfer` checks account access and same-owner rules, conditionally debits the source, credits the destination, and writes paired `TRANSFER_OUT` and `TRANSFER_IN` records in one MongoDB transaction.
- Transfers require MongoDB multi-document transaction support (MongoDB Atlas or a replica-set/sharded deployment). A standalone local MongoDB instance will not support this endpoint as configured.

## 2. Consistent styling

- Added shared CSS design tokens and aligned the primary page backgrounds, headers, cards, controls, tables, and messages.
- Added shared styles for the new transfer, analytics, and administrator fraud-monitoring pages.

## 3. Light and dark mode

- Added a shared theme provider and toggle across the welcome, authentication, customer, admin, account, transaction, analytics, transfer, user-management, and not-found pages.
- Theme choice is saved in browser storage; the operating-system preference is used when no saved choice exists.

## 4. User-wide deposit/withdrawal analytics

- Added `GET /api/analytics/me/cash-flow?days=90`.
- Aggregates activity across all accounts owned by the signed-in customer.
- Includes total deposits, withdrawals, net external cash flow, monthly comparison chart, and monthly breakdown.
- Internal transfers are shown separately and excluded from external cash-flow totals.

## 5. Administrator-only fraud/anomaly monitoring

- Added a rules-based baseline for unusually large transactions and high transaction velocity.
- Added an Isolation Forest anomaly-detection prototype using scikit-learn when at least eight transaction records are available; rules remain available otherwise.
- Configurable thresholds are documented in `.env.example`.
- Flagged records are stored in MongoDB's `risk_alerts` collection.
- `GET /api/admin/fraud-alerts` and `PATCH /api/admin/fraud-alerts/{alert_id}/review` require an `AdminToken`. Review status, note, timestamp, and reviewer ID are recorded.
- The frontend includes status, severity, detection-method, and date filters.
- Fraud/anomaly flags are indicators for human review, not proof of fraud. The prototype does not block transactions or freeze accounts.

## Verification performed in the implementation environment

- Python syntax compilation passed (`python -m compileall -q simple-bank-api`).
- Frontend lint passed (`npm run lint`).
- The user-wide cash-flow unit test passed (`PYTHONPATH=. pytest -q tests/test_analytics_service.py`).
- A fraud-detection smoke test passed using in-memory test doubles.
- Full backend test collection could not be run because `pymongo` is not installed in the implementation environment and package downloads were unavailable.
- The Vite production build could not be completed because the supplied `node_modules` lacked the platform-specific Rolldown native binding; package installation timed out in the implementation environment. `node_modules` is excluded from this ZIP; run `npm install` from `simple-bank-ui` before building locally.

## Before real-world use

This remains an educational banking application. Existing balance fields use floating-point numbers; financial-grade integer/decimal money handling, idempotency, broader transaction consistency, model validation against labeled data, monitoring, and security review are still required before any real financial deployment.
