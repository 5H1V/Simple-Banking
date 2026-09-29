from models.transaction import Transaction

class TransactionService:
    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    def create_transaction(self, account_id, txn_type, amount):
        transaction = Transaction(None, account_id, txn_type, amount)
        return self.transaction_repository.save(transaction)

    def get_transactions(self, account_id):
        return self.transaction_repository.find_by_account_id(account_id)