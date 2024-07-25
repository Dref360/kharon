from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(...)


class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_key: str = Field(index=True, unique=True)
    key_name: str
    user_id: int = Field(foreign_key="user.id")
    is_active: bool = True
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=True),
    )
