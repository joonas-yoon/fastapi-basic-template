from controllers.auth import (create_user, entity_to_user,
                              get_current_active_user, get_user_entity, get_users)
from fastapi import APIRouter, Body, Depends
from fastapi import status as Status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import User

router = APIRouter()


@router.get("/users")
async def get_all_users():
    return get_users()


@router.get("/users/{username}", response_model=User)
async def get_all_users(username: str):
    user = get_user_entity(username=username)
    return user


@router.get("/user/me/", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/user/create", response_description="Add new User", response_model=User)
async def create_student(user: User = Body(...), password: str = Body(...)):
    created_entity = create_user(user, password)
    created_user = entity_to_user(created_entity)
    decoded_user = jsonable_encoder(created_user)
    return JSONResponse(status_code=Status.HTTP_201_CREATED, content=decoded_user)
