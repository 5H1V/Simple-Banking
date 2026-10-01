import re

from pymongo.errors import DuplicateKeyError

from core.security import create_access_token, hash_password, verify_password


class AuthServiceError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class AuthService:
    def __init__(self, repository, setup_key: str | None):
        self.repository = repository
        self.setup_key = setup_key

    @staticmethod
    def _validate_password(password: str) -> None:
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise AuthServiceError(
                400,
                "Password must include at least one letter and one number"
            )

    @staticmethod
    def _token_response(identifier, email: str, role: str):
        return {
            "accessToken": create_access_token(str(identifier), email, role),
            "tokenType": "bearer",
            "role": role
        }

    def register(self, name: str, email: str, password: str):
        name = name.strip()
        email = email.strip().lower()
        if not name:
            raise AuthServiceError(400, "Name cannot be empty")
        self._validate_password(password)
        if self.repository.find_user_by_email(email):
            raise AuthServiceError(
                409,
                "An account with this email already exists"
            )
        try:
            result = self.repository.create_user(name, email, hash_password(password))
        except DuplicateKeyError:
            raise AuthServiceError(
                409,
                "An account with this email already exists"
            )
        return {
            "userId": str(result.inserted_id),
            "name": name,
            "email": email,
            **self._token_response(result.inserted_id, email, "CustomerToken")
        }

    def login_customer(self, email: str, password: str):
        email = email.strip().lower()
        user = self.repository.find_user_by_email(email)
        if (
            not user
            or not user.get("password_hash")
            or not verify_password(password, user["password_hash"])
        ):
            raise AuthServiceError(401, "Invalid email or password")
        return {
            "userId": str(user["_id"]),
            "name": user.get("name", ""),
            "email": email,
            **self._token_response(user["_id"], email, "CustomerToken")
        }

    def setup_admin(self, setup_key: str, name: str, email: str, password: str):
        if not self.setup_key:
            raise AuthServiceError(
                503,
                "ADMIN_SETUP_KEY is not configured on the server"
            )
        if setup_key != self.setup_key:
            raise AuthServiceError(403, "Invalid admin setup key")
        name = name.strip()
        email = email.strip().lower()
        if not name:
            raise AuthServiceError(400, "Name cannot be empty")
        self._validate_password(password)
        try:
            result = self.repository.create_first_admin(
                name,
                email,
                hash_password(password)
            )
        except DuplicateKeyError:
            raise AuthServiceError(
                409,
                "An admin with this email already exists"
            )
        if result is None:
            raise AuthServiceError(409, "Admin setup has already been completed")
        return {
            "adminId": str(result.inserted_id),
            "name": name,
            "email": email,
            **self._token_response(result.inserted_id, email, "AdminToken")
        }

    def login_admin(self, email: str, password: str):
        email = email.strip().lower()
        admin = self.repository.find_admin_by_email(email)
        if (
            not admin
            or not verify_password(password, admin.get("password_hash", ""))
        ):
            raise AuthServiceError(401, "Invalid email or password")
        return {
            "adminId": str(admin["_id"]),
            "name": admin.get("name", "Admin"),
            "email": email,
            **self._token_response(admin["_id"], email, "AdminToken")
        }
