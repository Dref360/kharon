from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(...)


class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_key: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="user.id")
