from typing import Union
from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., description='Nickname')
    email: str = Field(..., description='E-mail address')
    name: Union[str, None] = None
