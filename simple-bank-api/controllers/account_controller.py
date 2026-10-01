from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_principal
from core.security import enforce_account_ownership
from schemas.account import AmountRequest, CreateAccountRequest
from repos.repositories import (
    user_repository,
    account_repository,
    transaction_repository
)

from services.account_service import AccountService
from services.transaction_service import TransactionService

account_controller = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

transaction_service = TransactionService(
    transaction_repository
)

account_service = AccountService(
    account_repository,
    user_repository,
    transaction_service
)

@account_controller.get("/me")
def get_my_accounts(principal: dict = Depends(get_current_principal)):
    return [
        account.to_dict()
        for account in account_service.get_accounts_for_user(principal["sub"])
    ]

@account_controller.post("", status_code=201)
def create_account(
    data: CreateAccountRequest,
    principal: dict = Depends(get_current_principal)
):
    if (
        principal["role"] != "AdminToken"
        and principal["sub"] != data.userId
    ):
        raise HTTPException(status_code=403, detail="You can only create your own accounts")
    account, error = account_service.create_account(data.userId, data.accountType)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return account.to_dict()

@account_controller.get("/{account_id}")
def get_account(
    account_id: str,
    principal: dict = Depends(get_current_principal)
):
    account = account_service.get_account(account_id)
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    enforce_account_ownership(account, principal)
    return account.to_dict()

@account_controller.post("/{account_id}/deposit")
def deposit(
    account_id: str,
    data: AmountRequest,
    principal: dict = Depends(get_current_principal)
):
    account = account_service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    enforce_account_ownership(account, principal)
    account, error = account_service.deposit(account_id, data.amount)
    if error:
        if error == "Account not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return account.to_dict()

@account_controller.post("/{account_id}/withdraw")
def withdraw(
    account_id: str,
    data: AmountRequest,
    principal: dict = Depends(get_current_principal)
):
    account = account_service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    enforce_account_ownership(account, principal)
    account, error = account_service.withdraw(
        account_id,
        data.amount
    )
    if error:
        if error == "Account not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )
        raise HTTPException(
            status_code=400,
            detail=error
        )
    return account.to_dict()

@account_controller.get("/{account_id}/transactions")
def get_transactions(
    account_id: str,
    principal: dict = Depends(get_current_principal)
):
    account = account_service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    enforce_account_ownership(account, principal)
    transactions, error = account_service.get_transactions(account_id)
    if error:
        raise HTTPException(
            status_code=404,
            detail=error
        )

    return [transaction.to_dict() for transaction in transactions]