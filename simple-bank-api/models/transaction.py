from datetime import datetime, timezone


class Transaction:
    def __init__(self, txn_id=None, account_id=None, txn_type=None, amount=None,
                 created_at=None, transfer_id=None, related_account_id=None):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount
        self.created_at = created_at or datetime.now(timezone.utc)
        self.transfer_id = transfer_id
        self.related_account_id = related_account_id

    def to_dict(self):
        return {
            "txnId": self.txn_id,
            "accountId": self.account_id,
            "txnType": self.txn_type,
            "type": self.txn_type,
            "amount": self.amount,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "transferId": self.transfer_id,
            "relatedAccountId": self.related_account_id,
        }
