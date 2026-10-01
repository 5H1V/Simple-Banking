from pymongo.errors import DuplicateKeyError

from core.database import db


class AuthRepository:
    def __init__(self):
        self.users = db["users"]
        self.admins = db["admins"]
        self.settings = db["system_settings"]

    def create_user(self, name: str, email: str, password_hash: str):
        self.users.create_index("email", unique=True)
        return self.users.insert_one({
            "name": name,
            "email": email,
            "password_hash": password_hash
        })

    def find_user_by_email(self, email: str):
        return self.users.find_one({"email": email})

    def find_admin_by_email(self, email: str):
        return self.admins.find_one({"email": email})

    def create_first_admin(self, name: str, email: str, password_hash: str):
        self.admins.create_index("email", unique=True)
        if self.settings.find_one({"_id": "admin_setup_complete"}):
            return None
        if self.find_admin_by_email(email):
            raise DuplicateKeyError("An admin with this email already exists")

        result = self.admins.insert_one({
            "name": name,
            "email": email,
            "password_hash": password_hash
        })
        try:
            self.settings.insert_one({
                "_id": "admin_setup_complete",
                "admin_id": str(result.inserted_id)
            })
        except DuplicateKeyError:
            self.admins.delete_one({"_id": result.inserted_id})
            return None
        return result
