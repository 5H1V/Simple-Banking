from models.account import Account

class AccountRepository:
    def __init__(self):
        self.accounts = [Account(1, 1, "SAVINGS", 1000.00)]
        self.next_id = 2

    def find_all(self):
        return self.accounts

    def find_by_id(self, account_id):
        for account in self.accounts:
            if account.account_id == account_id:
                return account

        return None

    def find_by_user_id(self, user_id):
        return [
            account for account in self.accounts
            if account.user_id == user_id
        ]

    def save(self, account):
        existing = self.find_by_id(account.account_id)
        if existing:
            existing.user_id = account.user_id
            existing.account_type = account.account_type
            existing.balance = account.balance
            return existing

        self.accounts.append(account)
        return account

    def delete_by_id(self, account_id):
        account = self.find_by_id(account_id)
        if account:
            self.accounts.remove(account)
            return True
        
        return False