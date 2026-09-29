class UserRepository:

    def __init__(self):
        self.users = []
        self.next_id = 1

    def find_all(self):
        return self.users

    def find_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None

    def find_by_email(self, email):
        for user in self.users:
            if user.email.lower() == email.lower():
                return user

        return None

    def save(self, user):
        if user.user_id is None:
            user.user_id = self.next_id
            self.next_id += 1

            self.users.append(user)
        else:
            existing_user = self.find_by_id(user.user_id)

            if existing_user is None:
                self.users.append(user)
            else:
                existing_user.name = user.name
                existing_user.email = user.email

        return user

    def delete_by_id(self, user_id):
        user = self.find_by_id(user_id)

        if user is None:
            return False

        self.users.remove(user)
        return True