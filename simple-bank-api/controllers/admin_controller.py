from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.security import require_roles
from repos.repositories import user_repository, account_repository, transaction_repository
from services.admin_service import AdminService
from database import db
from services.fraud_detection_service import FraudDetectionService

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])
admin_only = require_roles("AdminToken")
fraud_detection_service = FraudDetectionService(account_repository, transaction_repository, db)

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


class AlertReviewRequest(BaseModel):
    status: str
    note: str = Field(default="", max_length=1000)


@router.get("/fraud-alerts", dependencies=[Depends(admin_only)])
def fraud_alerts():
    return fraud_detection_service.analyze()


@router.patch("/fraud-alerts/{alert_id}/review", dependencies=[Depends(admin_only)])
def review_fraud_alert(alert_id: str, data: AlertReviewRequest, principal: dict = Depends(admin_only)):
    try:
        return fraud_detection_service.review(alert_id, data.status, data.note, reviewer_id=principal["sub"])
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
