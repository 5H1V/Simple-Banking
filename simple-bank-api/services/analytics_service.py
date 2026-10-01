from collections import defaultdict
from datetime import datetime, timezone


class AnalyticsService:
    def __init__(self, account_repository, transaction_service):
        self.account_repository = account_repository
        self.transaction_service = transaction_service

    def cash_flow(self, user_id, days=90):
        accounts = self.account_repository.find_by_user_id(user_id)
        transactions = self.transaction_service.get_transactions_for_accounts(accounts)
        now = datetime.now(timezone.utc)
        cutoff = now.timestamp() - days * 86400
        monthly = defaultdict(lambda: {"deposits": 0.0, "withdrawals": 0.0, "transfersIn": 0.0, "transfersOut": 0.0})
        totals = {"deposits": 0.0, "withdrawals": 0.0, "transfersIn": 0.0, "transfersOut": 0.0}
        for txn in transactions:
            timestamp = txn.created_at
            if timestamp is None:
                continue
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            if timestamp.timestamp() < cutoff:
                continue
            kind = (txn.txn_type or "").upper()
            bucket = timestamp.strftime("%Y-%m")
            if kind in {"DEPOSIT", "DEPOSITED"}:
                key = "deposits"
            elif kind in {"WITHDRAW", "WITHDRAWAL", "WITHDRAWN"}:
                key = "withdrawals"
            elif kind in {"TRANSFER_IN", "TRANSFER_INCOMING"}:
                key = "transfersIn"
            elif kind in {"TRANSFER_OUT", "TRANSFER_OUTGOING"}:
                key = "transfersOut"
            else:
                continue
            value = float(txn.amount or 0)
            totals[key] += value
            monthly[bucket][key] += value
        month_rows = [{"month": month, **{key: round(value, 2) for key, value in sums.items()}}
                      for month, sums in sorted(monthly.items())]
        return {
            "days": days,
            "accountCount": len(accounts),
            "totals": {key: round(value, 2) for key, value in totals.items()},
            "netExternalCashFlow": round(totals["deposits"] - totals["withdrawals"], 2),
            "monthly": month_rows,
        }
