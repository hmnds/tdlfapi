from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.user import model as models
from app.user import schemas as schemas
from app.core.passwords import get_password_hash, verify_password


def create_user(db, data):
    user = models.User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(user)
    return user


def list_users(db, skip=0, limit=100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db, user_id, data):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.email is not None:
        user.email = data.email
    if data.password is not None:
        user.password = get_password_hash(data.password)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(user)
    return user


def delete_user(db, user_id):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


def get_user_by_email(db, email):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db, email, password):
    user = get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None
    return user
