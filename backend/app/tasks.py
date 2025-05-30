from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, SQLModel, select

from .database import get_session
from .models import Task, TaskPriority, TaskStatus

router = APIRouter(prefix="/tasks")


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None


def _require_user(request: Request):
    user = getattr(request.state, "current_user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.get("/", response_model=List[Task])
def list_tasks(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    user = _require_user(request)
    statement = (
        select(Task)
        .where(Task.user_id == user.id)
        .offset(offset)
        .limit(limit)
    )
    tasks = session.exec(statement).all()
    return tasks


@router.post("/", response_model=Task)
def create_task(
    task_in: TaskCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    user = _require_user(request)
    if task_in.due_datetime and task_in.due_datetime <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="due_datetime must be in the future")
    task = Task.from_orm(task_in)
    task.user_id = user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session),
):
    user = _require_user(request)
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task_in.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    user = _require_user(request)
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@router.post("/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    user = _require_user(request)
    task = session.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = TaskStatus.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
