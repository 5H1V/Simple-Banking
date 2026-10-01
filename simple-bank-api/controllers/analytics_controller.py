from fastapi import APIRouter, Depends, Query
from api.dependencies import get_current_principal
from repos.repositories import account_repository, transaction_repository
from services.analytics_service import AnalyticsService
from services.transaction_service import TransactionService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
analytics_service = AnalyticsService(account_repository, TransactionService(transaction_repository))


@router.get("/me/cash-flow")
def my_cash_flow(days: int = Query(default=90, ge=7, le=3650), principal: dict = Depends(get_current_principal)):
    if principal.get("role") != "CustomerToken":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Customer analytics are only available to customer accounts")
    return analytics_service.cash_flow(principal["sub"], days)
