from types import SimpleNamespace

import pytest

import services.auth_service as auth_service_module
from core.security import verify_password
from services.auth_service import AuthService, AuthServiceError


class FakeAuthRepository:
    def __init__(self):
        self.users = {}
        self.admins = {}
        self.admin_setup_complete = False
        self.next_id = 0

    def create_user(self, name, email, password_hash):
        self.next_id += 1
        user_id = f"user-{self.next_id}"
        self.users[email] = {
            "_id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash
        }
        return SimpleNamespace(inserted_id=user_id)

    def find_user_by_email(self, email):
        return self.users.get(email)

    def find_admin_by_email(self, email):
        return self.admins.get(email)

    def create_first_admin(self, name, email, password_hash):
        if self.admin_setup_complete:
            return None
        self.admin_setup_complete = True
        admin_id = "admin-1"
        self.admins[email] = {
            "_id": admin_id,
            "name": name,
            "email": email,
            "password_hash": password_hash
        }
        return SimpleNamespace(inserted_id=admin_id)


def test_auth_service_registers_and_authenticates_with_a_password_hash(monkeypatch):
    monkeypatch.setattr(
        auth_service_module,
        "create_access_token",
        lambda subject, email, role: f"{role}:{subject}"
    )
    repository = FakeAuthRepository()
    service = AuthService(repository, setup_key="setup-key")

    registration = service.register(
        "  Casey User ",
        "CASEY@example.test",
        "user-pass123"
    )

    assert registration["name"] == "Casey User"
    assert registration["email"] == "casey@example.test"
    assert registration["accessToken"] == "CustomerToken:user-1"
    assert verify_password(
        "user-pass123",
        repository.users["casey@example.test"]["password_hash"]
    )

    login = service.login_customer("CASEY@example.test", "user-pass123")
    assert login["userId"] == "user-1"
    assert login["role"] == "CustomerToken"


def test_auth_service_rejects_duplicate_emails_and_invalid_passwords(monkeypatch):
    monkeypatch.setattr(auth_service_module, "create_access_token", lambda *_: "token")
    service = AuthService(FakeAuthRepository(), setup_key="setup-key")
    service.register("Casey User", "casey@example.test", "user-pass123")

    with pytest.raises(AuthServiceError) as duplicate:
        service.register("Another User", "casey@example.test", "other-pass123")
    assert duplicate.value.status_code == 409

    with pytest.raises(AuthServiceError) as invalid_password:
        service.register("Another User", "other@example.test", "onlyletters")
    assert invalid_password.value.status_code == 400


def test_auth_service_limits_admin_setup_to_one_success(monkeypatch):
    monkeypatch.setattr(
        auth_service_module,
        "create_access_token",
        lambda subject, email, role: f"{role}:{subject}"
    )
    service = AuthService(FakeAuthRepository(), setup_key="setup-key")
    admin = service.setup_admin(
        "setup-key",
        "Bank Admin",
        "admin@example.test",
        "admin-pass123"
    )

    assert admin["role"] == "AdminToken"
    with pytest.raises(AuthServiceError) as already_setup:
        service.setup_admin(
            "setup-key",
            "Another Admin",
            "other@example.test",
            "admin-pass456"
        )
    assert already_setup.value.status_code == 409