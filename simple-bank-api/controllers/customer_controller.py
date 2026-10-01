from fastapi import APIRouter, Depends
from security import require_roles
from repos.repositories import account_repository, transaction_repository

router = APIRouter(prefix="/customer", tags=["Customer Dashboard"])
customer_only = require_roles("CustomerToken")

@router.get("/me/accounts")
def my_accounts(principal: dict = Depends(customer_only)):
    accounts = [a for a in account_repository.find_all() if a.user_id == principal["sub"]]
    return [a.to_dict() for a in accounts]

@router.get("/me/transactions")
def my_transactions(principal: dict = Depends(customer_only)):
    owned_ids = {a.account_id for a in account_repository.find_all() if a.user_id == principal["sub"]}
    result = []
    for account_id in owned_ids:
        result.extend({"txnId": t.txn_id, "accountId": t.account_id, "type": t.txn_type, "amount": t.amount} for t in transaction_repository.find_by_account_id(account_id))
    return result
