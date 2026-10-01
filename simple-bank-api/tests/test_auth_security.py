from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from security import hash_password, verify_password, create_access_token, get_current_principal, require_roles, enforce_account_ownership


def test_password_is_hashed_and_verifies():
    password = "CorrectHorse123"
    stored = hash_password(password)
    assert stored != password
    assert stored.startswith("$argon2id$")
    assert verify_password(password, stored)
    assert not verify_password("wrong-password", stored)


def test_customer_cannot_pass_admin_role_check():
    guard = require_roles("AdminToken")
    with pytest.raises(HTTPException) as exc:
        guard({"sub": "customer-1", "role": "CustomerToken"})
    assert exc.value.status_code == 403


def test_customer_cannot_access_another_users_account():
    class Account:
        user_id = "owner-1"
    with pytest.raises(HTTPException) as exc:
        enforce_account_ownership(Account(), {"sub": "customer-2", "role": "CustomerToken"})
    assert exc.value.status_code == 403


def test_owner_can_access_own_account_and_admin_can_access_any_account():
    class Account:
        user_id = "owner-1"
    enforce_account_ownership(Account(), {"sub": "owner-1", "role": "CustomerToken"})
    enforce_account_ownership(Account(), {"sub": "admin-1", "role": "AdminToken"})
