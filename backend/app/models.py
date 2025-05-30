from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Calendar(SQLModel, table=True):
    __tablename__ = "calendars"

    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    provider: str
    access_token: str
    refresh_token: Optional[str] = None
    last_synced: Optional[datetime] = None


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: TaskPriority = Field(default=TaskPriority.medium)
    calendar_event_id: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.pending)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
