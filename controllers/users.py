from typing import Union

from crud.user import UserEntity

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(username: str, db: Union[dict, None] = None):
    if db is None or type(db) is type(dict):
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserEntity(**user_dict)
        return None


def get_users():
    return list(fake_users_db.keys())
