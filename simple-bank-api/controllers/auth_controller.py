from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_principal
from core.config import ADMIN_SETUP_KEY
from repos.auth_repository import AuthRepository
from schemas.auth import AdminSetupRequest, LoginRequest, RegisterRequest
from services.auth_service import AuthService, AuthServiceError

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService(AuthRepository(), ADMIN_SETUP_KEY)


def _invoke_service(operation, *args):
    try:
        return operation(*args)
    except AuthServiceError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.detail
        ) from error


@router.post("/register", status_code=201)
def register(data: RegisterRequest):
    return _invoke_service(
        auth_service.register,
        data.name,
        str(data.email),
        data.password
    )


@router.post("/login")
def customer_login(data: LoginRequest):
    return _invoke_service(
        auth_service.login_customer,
        str(data.email),
        data.password
    )


@router.post("/admin/setup", status_code=201)
def setup_admin(data: AdminSetupRequest):
    return _invoke_service(
        auth_service.setup_admin,
        data.setupKey,
        data.name,
        str(data.email),
        data.password
    )


@router.post("/admin/login")
def admin_login(data: LoginRequest):
    return _invoke_service(
        auth_service.login_admin,
        str(data.email),
        data.password
    )


@router.get("/me")
def me(principal: dict = Depends(get_current_principal)):
    return {
        "id": principal["sub"],
        "email": principal["email"],
        "role": principal["role"]
    }
