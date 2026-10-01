class DashboardService:
    def __init__(self, account_repository, transaction_service):
        self.account_repository = account_repository
        self.transaction_service = transaction_service

    def get_accounts(self, user_id):
        return self.account_repository.find_by_user_id(user_id)

    def get_transactions(self, user_id):
        accounts = self.get_accounts(user_id)
        return [
            {"txnId": txn.txn_id, "accountId": txn.account_id, "type": txn.txn_type,
             "amount": txn.amount, "createdAt": txn.created_at.isoformat() if txn.created_at else None,
             "transferId": txn.transfer_id, "relatedAccountId": txn.related_account_id}
            for txn in self.transaction_service.get_transactions_for_accounts(accounts)
        ]
