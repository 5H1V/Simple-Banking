from fastapi import APIRouter, Depends

from api.dependencies import get_current_principal
from repos.repositories import account_repository, transaction_repository
from services.dashboard_service import DashboardService
from services.transaction_service import TransactionService

transaction_controller = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)
transaction_service = TransactionService(transaction_repository)
dashboard_service = DashboardService(
    account_repository,
    transaction_service
)


@transaction_controller.get("/me")
def get_my_transactions(principal: dict = Depends(get_current_principal)):
    return dashboard_service.get_transactions(principal["sub"])