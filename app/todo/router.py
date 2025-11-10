from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.todo import schemas
from app.todo import service

router = APIRouter()

@router.post("/", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return service.create_todo(db, todo)

@router.get("/", response_model=list[schemas.TodoOut])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list_todos(db, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model=schemas.TodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    found = service.get_todo(db, todo_id)
    if not found:
        raise HTTPException(status_code=404, detail="Todo not found")
    return found

@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    return service.update_todo(db, todo_id, todo)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    service.delete_todo(db, todo_id)
    return None
