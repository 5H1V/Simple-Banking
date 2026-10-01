from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY

password_hasher = PasswordHasher()
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, ValueError):
        return False


def create_access_token(subject: str, email: str, role: str) -> str:
    if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET_KEY must be configured with at least 32 characters"
        )
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "email": email,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET_KEY must be configured with at least 32 characters"
        )
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        if not payload.get("sub") or payload.get("role") not in {
            "CustomerToken",
            "AdminToken"
        }:
            raise jwt.InvalidTokenError("Required claims are missing")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


def require_roles(*roles: str):
    def dependency(principal: dict = Depends(get_current_principal)):
        if principal.get("role") not in roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )
        return principal
    return dependency


def require_customer_or_admin(
    principal: dict = Depends(get_current_principal)
):
    return principal


def enforce_account_ownership(account, principal: dict) -> None:
    if principal.get("role") == "AdminToken":
        return
    if (
        principal.get("role") != "CustomerToken"
        or account.user_id != principal.get("sub")
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this account"
        )
