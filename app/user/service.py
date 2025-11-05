from sqlalchemy.orm import Session
from app.user import model as models
from app.user import schemas as schemas
from app.core.passwords import get_password_hash

def create_user(db: Session, data: schemas.UserCreate):
    user = models.User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user