from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password_hash: str, first_name: str, last_name: str):
    user = User(
        email=email,
        password_hash=password_hash,
        first_name=first_name,
        last_name=last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user