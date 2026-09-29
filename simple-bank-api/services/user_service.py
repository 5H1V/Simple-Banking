class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_all_users(self):
        return self.user_repository.find_all()

    def get_user_by_id(self, user_id):
        return self.user_repository.find_by_id(user_id)

    def create_user(self, user):
        if not user.name or not user.name.strip():
            return None, "Name cannot be empty"

        if self.user_repository.find_by_email(user.email):
            return None, "Email already exists"

        return self.user_repository.save(user), None

    def update_user(self, user_id, name, email):
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            return None, "User not found"

        if not name or not name.strip():
            return None, "Name cannot be empty"

        existing_email_user = self.user_repository.find_by_email(email)

        if (
            existing_email_user is not None
            and existing_email_user.user_id != user_id
        ):
            return None, "Email already exists"

        user.name = name
        user.email = email

        self.user_repository.save(user)

        return user, None

    def delete_user(self, user_id):
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            return False

        return self.user_repository.delete_by_id(user_id)