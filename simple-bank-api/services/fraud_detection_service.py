from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import median
import os
from math import log1p

from bson import ObjectId

LARGE_AMOUNT_MIN = float(os.getenv("FRAUD_LARGE_AMOUNT_MIN", "250"))
MEDIAN_MULTIPLIER = float(os.getenv("FRAUD_MEDIAN_MULTIPLIER", "4"))
HOURLY_TRANSACTION_THRESHOLD = int(os.getenv("FRAUD_HOURLY_TRANSACTION_THRESHOLD", "8"))

try:
    from sklearn.ensemble import IsolationForest
except ImportError:  # Rules remain available if optional ML dependency is not installed yet.
    IsolationForest = None


class FraudDetectionService:
    """Explainable rules plus an optional Isolation Forest anomaly detector."""
    def __init__(self, account_repository, transaction_repository, database):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.alerts = database["risk_alerts"]

    def analyze(self):
        accounts = self.account_repository.find_all()
        account_owner = {a.account_id: a.user_id for a in accounts}
        transactions = self.transaction_repository.find_all()
        now = datetime.now(timezone.utc)
        per_user_amounts = defaultdict(list)
        user_events = defaultdict(list)
        normalized = []
        for txn in transactions:
            owner = account_owner.get(txn.account_id, "unknown")
            created = txn.created_at or now
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            amount = abs(float(txn.amount or 0))
            per_user_amounts[owner].append(amount)
            user_events[owner].append((created, txn.txn_id))
            normalized.append((txn, owner, created, amount))

        # Count each user's transactions in the rolling hour ending at that transaction.
        velocity_counts = {}
        for events in user_events.values():
            events.sort(key=lambda event: event[0])
            left = 0
            for index, (created, transaction_id) in enumerate(events):
                window_start = created - timedelta(hours=1)
                while left < index and events[left][0] < window_start:
                    left += 1
                velocity_counts[transaction_id] = index - left + 1

        feature_rows = []
        for txn, owner, created, amount in normalized:
            amounts = per_user_amounts[owner]
            historical_median = median(amounts) if amounts else 0
            velocity = velocity_counts.get(txn.txn_id, 1)
            feature_rows.append([amount, abs(amount - historical_median), velocity, (created.hour + created.minute / 60)])

        ml_scores = [0.0] * len(normalized)
        ml_flags = [False] * len(normalized)
        model_used = False
        # Log-scale amounts and deviations so large currency values do not dominate every feature.
        feature_rows = [[log1p(max(0.0, row[0])), log1p(max(0.0, row[1])), row[2], row[3]] for row in feature_rows]
        if IsolationForest is not None and len(feature_rows) >= 8:
            try:
                model = IsolationForest(n_estimators=100, contamination="auto", random_state=42)
                model.fit(feature_rows)
                predictions = model.predict(feature_rows)
                raw_scores = model.decision_function(feature_rows)
                ml_flags = [prediction == -1 for prediction in predictions]
                model_used = True
                # Higher normalized value means more unusual; scale for dashboard readability.
                ml_scores = [round(max(0.0, min(1.0, 0.5 - float(score))), 3) for score in raw_scores]
            except (ValueError, ArithmeticError):
                ml_flags = [False] * len(normalized)
                ml_scores = [0.0] * len(normalized)

        for index, (txn, owner, created, amount) in enumerate(normalized):
            reasons = []
            amounts = per_user_amounts[owner]
            baseline = median(amounts) if amounts else 0
            # Relative rule: robust enough to demonstrate; review thresholds before real-world use.
            if len(amounts) >= 4 and amount >= max(LARGE_AMOUNT_MIN, baseline * MEDIAN_MULTIPLIER):
                reasons.append("Transaction amount is substantially above this user's median transaction")
            if velocity_counts.get(txn.txn_id, 1) >= HOURLY_TRANSACTION_THRESHOLD:
                reasons.append("High transaction frequency within a rolling one-hour window")
            if ml_flags[index]:
                reasons.append("Isolation Forest identified an unusual transaction pattern")
            if not reasons:
                continue
            score = min(0.99, max(0.35, 0.45 + (0.2 if len(reasons) > 1 else 0) + ml_scores[index]))
            alert_id = txn.txn_id
            document = {
                "transaction_id": txn.txn_id,
                "account_id": txn.account_id,
                "user_id": owner,
                "transaction_type": txn.txn_type,
                "amount": amount,
                "created_at": created,
                "risk_score": round(score, 3),
                "reasons": reasons,
                "detection_methods": (["rules"] if any("Isolation Forest" not in r for r in reasons) else []) + (["isolation_forest"] if ml_flags[index] else []),
                "model_version": "isolation-forest-v1" if model_used else "rules-only-v1",
                "updated_at": now,
            }
            self.alerts.update_one(
                {"transaction_id": alert_id},
                {"$set": document, "$setOnInsert": {"review_status": "pending", "review_note": "", "created_alert_at": now}},
                upsert=True,
            )
        # Return existing alerts too, including ones already reviewed, without auto-deleting history.
        results = list(self.alerts.find().sort("created_at", -1).limit(500))
        return [self._serialize(item) for item in results]

    @staticmethod
    def _serialize(item):
        return {
            "alertId": str(item.get("_id", "")),
            "transactionId": item.get("transaction_id"),
            "accountId": item.get("account_id"),
            "userId": item.get("user_id"),
            "transactionType": item.get("transaction_type"),
            "amount": item.get("amount", 0),
            "createdAt": item.get("created_at").isoformat() if item.get("created_at") else None,
            "riskScore": item.get("risk_score", 0),
            "reasons": item.get("reasons", []),
            "detectionMethods": item.get("detection_methods", []),
            "modelVersion": item.get("model_version", "rules-only-v1"),
            "reviewStatus": item.get("review_status", "pending"),
            "reviewNote": item.get("review_note", ""),
            "reviewedBy": item.get("reviewed_by"),
        }

    def review(self, alert_id, status, note="", reviewer_id=None):
        if status not in {"reviewed", "confirmed_suspicious", "false_positive"}:
            raise ValueError("Invalid review status")
        try:
            oid = ObjectId(alert_id)
        except Exception as exc:
            raise ValueError("Invalid alert ID") from exc
        result = self.alerts.update_one({"_id": oid}, {"$set": {
            "review_status": status,
            "review_note": note[:1000],
            "reviewed_at": datetime.now(timezone.utc),
        }})
        if result.matched_count == 0:
            raise ValueError("Alert not found")
        return self._serialize(self.alerts.find_one({"_id": oid}))
