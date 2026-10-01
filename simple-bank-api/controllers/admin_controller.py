from fastapi import APIRouter, Depends

from core.security import require_roles
from repos.repositories import user_repository, account_repository, transaction_repository
from services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])
admin_only = require_roles("AdminToken")
admin_service = AdminService(
    user_repository,
    account_repository,
    transaction_repository
)

@router.get("/users", dependencies=[Depends(admin_only)])
def all_users():
    return admin_service.get_users()

@router.get("/accounts", dependencies=[Depends(admin_only)])
def all_accounts():
    return admin_service.get_accounts()

@router.get("/transactions", dependencies=[Depends(admin_only)])
def all_transactions():
    return admin_service.get_transactions()
