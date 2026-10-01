class DashboardService:
    def __init__(self, account_repository, transaction_service):
        self.account_repository = account_repository
        self.transaction_service = transaction_service

    def get_accounts(self, user_id):
        return self.account_repository.find_by_user_id(user_id)

    def get_transactions(self, user_id):
        accounts = self.get_accounts(user_id)
        return [
            {
                "txnId": transaction.txn_id,
                "accountId": transaction.account_id,
                "type": transaction.txn_type,
                "amount": transaction.amount
            }
            for transaction in self.transaction_service.get_transactions_for_accounts(accounts)
        ]
