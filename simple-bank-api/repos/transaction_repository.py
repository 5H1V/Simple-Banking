class TransactionRepository:
    def __init__(self):
        self.transactions = []
        self.next_id = 1

    def save(self, transaction):
        transaction.txn_id = self.next_id
        self.transactions.append(transaction)
        self.next_id += 1
        return transaction

    def find_by_id(self, txn_id):
        for transaction in self.transactions:
            if transaction.txn_id == txn_id:
                return transaction

        return None

    def find_by_account_id(self, account_id):
        return [
            transaction for transaction in self.transactions
            if transaction.account_id == account_id
        ]

    def find_all(self):
        return self.transactions