from bson import ObjectId
from configs import Configs
from models.User import User
from pydantic import EmailStr, Field

from crud.commons import PyObjectId


class UserEntity(User):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str = Configs.USERPROFILE_DOC_TYPE
    name: str = Field(...)
    email: EmailStr = Field(...)
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "john-doe",
                "name": "Jane Doe",
                "email": "jdoe@example.com",
            }
        }
