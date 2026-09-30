from models.account import Account


class AccountService:

    def __init__(
        self,
        account_repository,
        user_repository,
        transaction_service
    ):
        self.account_repository = account_repository
        self.user_repository = user_repository
        self.transaction_service = transaction_service

    def create_account(self, user_id, account_type):

        user = self.user_repository.find_by_id(user_id)

        if user is None:
            return None, "User not found"

        account = Account(
            account_id=None,
            user_id=user_id,
            balance=0.00,
            account_type=account_type
        )

        account = self.account_repository.save(account)

        return account, None

    def get_account(self, account_id):
        return self.account_repository.find_by_id(account_id)

    def deposit(self, account_id, amount):

        if amount <= 0:
            return None, "Deposit amount must be positive"

        account = self.account_repository.find_by_id(account_id)

        if account is None:
            return None, "Account not found"

        account.balance += amount

        self.account_repository.save(account)

        self.transaction_service.create_transaction(
            account_id,
            "DEPOSIT",
            amount
        )

        return account, None

    def withdraw(self, account_id, amount):

        if amount <= 0:
            return None, "Withdrawal amount must be positive"

        account = self.account_repository.find_by_id(account_id)

        if account is None:
            return None, "Account not found"

        if amount > account.balance:
            return None, "Insufficient balance"

        account.balance -= amount

        self.account_repository.save(account)

        self.transaction_service.create_transaction(
            account_id,
            "WITHDRAW",
            amount
        )

        return account, None

    def get_transactions(self, account_id):

        account = self.account_repository.find_by_id(account_id)

        if account is None:
            return None, "Account not found"

        transactions = self.transaction_service.get_transactions(
            account_id
        )

        return transactions, None