from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.user import User
from services.user_service import UserService
from repos.repositories import user_repository


user_controller = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_service = UserService(user_repository)


class UserRequest(BaseModel):
    name: str
    email: str


@user_controller.get("")
def get_all_users():

    users = user_service.get_all_users()

    return [
        user.to_dict()
        for user in users
    ]


@user_controller.get("/{user_id}")
def get_user(user_id: str):

    user = user_service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user.to_dict()


@user_controller.post("", status_code=201)
def create_user(data: UserRequest):

    user = User(
        user_id=None,
        name=data.name,
        email=data.email
    )

    created_user, error = user_service.create_user(user)

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return created_user.to_dict()


@user_controller.put("/{user_id}")
def update_user(
    user_id: str,
    data: UserRequest
):

    user, error = user_service.update_user(
        user_id,
        data.name,
        data.email
    )

    if error:

        if error == "User not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )

        raise HTTPException(
            status_code=400,
            detail=error
        )

    return user.to_dict()


@user_controller.delete("/{user_id}")
def delete_user(user_id: str):

    deleted = user_service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }