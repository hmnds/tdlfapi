from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.todo import model as models
from app.todo import schemas as schemas

def create_todo(db: Session, data: schemas.TodoCreate):
    todo = models.Todo(
        title=data.title,
        description=data.description,
        completed=bool(data.completed or False),
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def list_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def update_todo(db: Session, todo_id: int, data: schemas.TodoUpdate):
    todo = get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.completed is not None:
        todo.completed = bool(data.completed)

    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
