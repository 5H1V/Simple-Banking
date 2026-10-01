from models.user import User
from services.user_service import UserService


class FakeUserRepository:
    def __init__(self):
        self.users = {}
        self.next_id = 0

    def find_all(self):
        return list(self.users.values())

    def find_by_id(self, user_id):
        return self.users.get(user_id)

    def find_by_email(self, email):
        return next(
            (user for user in self.users.values() if user.email == email),
            None
        )

    def save(self, user):
        if user.user_id is None:
            self.next_id += 1
            user.user_id = str(self.next_id)
        self.users[user.user_id] = user
        return user

    def delete_by_id(self, user_id):
        return self.users.pop(user_id, None) is not None


def test_user_service_creates_updates_and_deletes_users():
    service = UserService(FakeUserRepository())
    created, error = service.create_user(
        User(name="Casey User", email="casey@example.test")
    )
    assert error is None
    assert created.user_id == "1"

    updated, error = service.update_user(
        created.user_id,
        "Casey Updated",
        "updated@example.test"
    )
    assert error is None
    assert updated.name == "Casey Updated"

    assert service.delete_user(created.user_id)
    assert service.get_user_by_id(created.user_id) is None
