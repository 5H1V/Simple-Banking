class AdminService:
    def __init__(self, user_repository, account_repository, transaction_repository):
        self.user_repository = user_repository
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def get_users(self):
        return [user.to_dict() for user in self.user_repository.find_all()]

    def get_accounts(self):
        return [
            account.to_dict()
            for account in self.account_repository.find_all()
        ]

    def get_transactions(self):
        return [
            {
                "txnId": transaction.txn_id,
                "accountId": transaction.account_id,
                "type": transaction.txn_type,
                "amount": transaction.amount,
                "createdAt": transaction.created_at.isoformat() if transaction.created_at else None,
                "transferId": transaction.transfer_id,
                "relatedAccountId": transaction.related_account_id
            }
            for transaction in self.transaction_repository.find_all()
        ]
