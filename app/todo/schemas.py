from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):      
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoUpdate(BaseModel):             
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoOut(BaseModel):                 
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        orm_mode = True