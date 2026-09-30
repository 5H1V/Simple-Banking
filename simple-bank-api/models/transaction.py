class Transaction:

    def __init__(
        self,
        txn_id=None,
        account_id=None,
        txn_type=None,
        amount=None
    ):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount

    def to_dict(self):
        return {
            "txnId": self.txn_id,
            "accountId": self.account_id,
            "txnType": self.txn_type,
            "amount": self.amount
        }