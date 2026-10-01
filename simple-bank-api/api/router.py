from fastapi import APIRouter

from controllers.account_controller import account_controller
from controllers.admin_controller import router as admin_router
from controllers.auth_controller import router as auth_router
from controllers.analytics_controller import router as analytics_router
from controllers.transaction_controller import transaction_controller
from controllers.user_controller import user_controller

api_router = APIRouter()
api_router.include_router(user_controller)
api_router.include_router(account_controller)
api_router.include_router(transaction_controller)
api_router.include_router(auth_router)
api_router.include_router(admin_router)
api_router.include_router(analytics_router)