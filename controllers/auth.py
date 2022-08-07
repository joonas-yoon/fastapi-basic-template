from datetime import datetime, timedelta
from typing import List, Union

from configs import Configs
from fastapi import Depends, HTTPException
from fastapi import status as Status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import User
from models.auth import TokenData
from models.entity import UserEntity
from passlib.context import CryptContext

from .db import get_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

collection = get_collection("users")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user_entity(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Configs.SECRET_KEY, algorithm=Configs.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=Status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Configs.SECRET_KEY,
                             algorithms=[Configs.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_user_entity(username: str) -> UserEntity:
    user = collection.find_one({"username": username})
    return UserEntity(**user)


def get_user(username: str) -> User:
    return entity_to_user(get_user_entity(username))


def get_users() -> List[User]:
    records = list(collection.find())
    return list(map(lambda record: User(**record), records))


def create_user(user: User, password: str) -> UserEntity:
    hash = get_password_hash(password)
    user_form = UserEntity(**user.dict(), hashed_password=hash)
    encoded_user = jsonable_encoder(user_form)
    try:
        new_user = collection.insert_one(encoded_user)
        created_user_dict = collection.find_one({"_id": new_user.inserted_id})
        return UserEntity(**created_user_dict)
    except Exception as e:
        print(e)
    return None


def user_to_entity(user: User) -> UserEntity:
    json = jsonable_encoder(user)
    return UserEntity(**json)


def entity_to_user(user: UserEntity) -> User:
    entity = jsonable_encoder(user)
    return User(**entity)
