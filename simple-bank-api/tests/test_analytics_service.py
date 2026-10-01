from datetime import datetime, timezone
from types import SimpleNamespace

from services.analytics_service import AnalyticsService


class FakeAccountRepository:
    def find_by_user_id(self, user_id):
        assert user_id == "user-1"
        return [SimpleNamespace(account_id="account-1"), SimpleNamespace(account_id="account-2")]


class FakeTransactionService:
    def get_transactions_for_accounts(self, accounts):
        assert len(accounts) == 2
        now = datetime.now(timezone.utc)
        return [
            SimpleNamespace(created_at=now, txn_type="DEPOSIT", amount=100.0),
            SimpleNamespace(created_at=now, txn_type="WITHDRAW", amount=25.0),
            SimpleNamespace(created_at=now, txn_type="TRANSFER_IN", amount=50.0),
            SimpleNamespace(created_at=now, txn_type="TRANSFER_OUT", amount=50.0),
        ]


def test_cash_flow_aggregates_user_accounts_and_keeps_transfers_separate():
    service = AnalyticsService(FakeAccountRepository(), FakeTransactionService())
    result = service.cash_flow("user-1", days=90)
    assert result["accountCount"] == 2
    assert result["totals"] == {"deposits": 100.0, "withdrawals": 25.0, "transfersIn": 50.0, "transfersOut": 50.0}
    assert result["netExternalCashFlow"] == 75.0
    assert len(result["monthly"]) == 1
