from bson import ObjectId
from database import db
from models.user import User


class UserRepository:

    def __init__(self):
        self.collection = db["users"]

    def find_all(self):
        users = self.collection.find()

        return [
            User(
                user_id=str(user["_id"]),
                name=user["name"],
                email=user["email"]
            )
            for user in users
        ]

    def find_by_id(self, user_id):
        try:
            object_id = ObjectId(user_id)
        except Exception:
            return None

        user = self.collection.find_one({
            "_id": object_id
        })

        if user is None:
            return None

        return User(
            user_id=str(user["_id"]),
            name=user["name"],
            email=user["email"]
        )

    def find_by_email(self, email):
        user = self.collection.find_one({
            "email": email
        })

        if user is None:
            return None

        return User(
            user_id=str(user["_id"]),
            name=user["name"],
            email=user["email"]
        )

    def save(self, user):

        if user.user_id is None:

            result = self.collection.insert_one({
                "name": user.name,
                "email": user.email
            })

            user.user_id = str(result.inserted_id)

        else:

            self.collection.update_one(
                {
                    "_id": ObjectId(user.user_id)
                },
                {
                    "$set": {
                        "name": user.name,
                        "email": user.email
                    }
                }
            )

        return user

    def delete_by_id(self, user_id):

        try:
            object_id = ObjectId(user_id)
        except Exception:
            return False

        result = self.collection.delete_one({
            "_id": object_id
        })

        return result.deleted_count > 0