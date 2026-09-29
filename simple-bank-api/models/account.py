class Account:
    def __init__(self, account_id, user_id, account_type, balance=0.00):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance
        self.account_type = account_type

    def to_dict(self):
        return {
            "accountId": self.account_id,
            "userId": self.user_id,
            "balance": self.balance,
            "accountType": self.account_type
        }