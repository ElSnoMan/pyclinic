from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: str = Field(..., alias="userID")
    username: str
    books: List


class Nate(BaseModel):
    """The only difference between this class and Useris the alias...

    which is bad design... but a great example!
    """

    user_id: str = Field(..., alias="userId")
    username: str
    books: List


class Error(BaseModel):
    code: str
    message: str


class Token(BaseModel):
    token: str
    expires: str
    status: str
    result: str
