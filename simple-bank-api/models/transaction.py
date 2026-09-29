class Transaction:
    def __init__(self, txn_id, account_id, txn_type, amount):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount

    def to_dict(self):
        return {
            "transactionId": self.txn_id,
            "accountId": self.account_id,
            "type": self.txn_type,
            "amount": self.amount
        }