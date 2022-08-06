from controllers.auth import get_current_active_user
from controllers.db import get_collection
from controllers.users import get_user, get_users
from crud.user import UserEntity
from fastapi import APIRouter, Body, Depends
from fastapi import status as Status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.User import User

router = APIRouter()


@router.get("/users")
async def get_all_users():
    return get_users()


@router.get("/users/{username}", response_model=User)
async def get_all_users(username: str):
    user = get_user(username=username)
    return user


@router.get("/user/me/", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/user/create", response_description="Add new User", response_model=User)
async def create_student(user: User = Body(...), password: str = Body(...)):
    user_form = UserEntity(**user.dict(), hashed_password=password)
    encoded_user = jsonable_encoder(user_form)

    coll = get_collection("users")
    new_user = await coll.insert_one(encoded_user)
    created_user_dict = await coll.find_one({"_id": new_user.inserted_id})

    decoded_user = User(**created_user_dict)
    decoded_user = jsonable_encoder(decoded_user)
    return JSONResponse(status_code=Status.HTTP_201_CREATED, content=decoded_user)
