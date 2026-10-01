from datetime import datetime, timezone
from models.transaction import Transaction


class TransactionService:
    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    def create_transaction(self, account_id, txn_type, amount, **metadata):
        transaction = Transaction(
            txn_id=None,
            account_id=account_id,
            txn_type=txn_type,
            amount=amount,
            created_at=metadata.get("created_at") or datetime.now(timezone.utc),
            transfer_id=metadata.get("transfer_id"),
            related_account_id=metadata.get("related_account_id"),
        )
        return self.transaction_repository.save(transaction)

    def get_transactions(self, account_id):
        return self.transaction_repository.find_by_account_id(account_id)

    def get_transactions_for_accounts(self, accounts):
        transactions = [transaction for account in accounts for transaction in self.get_transactions(account.account_id)]

        def timestamp(transaction):
            value = transaction.created_at
            if value is None:
                return 0
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return value.timestamp()

        return sorted(transactions, key=timestamp, reverse=True)
