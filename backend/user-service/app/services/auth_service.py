from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
# 1. Import from your updated file name
from app.core.logger import get_logger

# 2. Pass __name__ so the log accurately reflects it came from this service file
log = get_logger(__name__)

def register_user(db: Session, email: str, password: str, first_name: str, last_name: str):
    existing = get_user_by_email(db, email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(password)
    user = create_user(db, email, hashed, first_name, last_name)
    
    # 3. This placement is 100% valid!
    log.info("user_registered", user_id=user.id, email=user.email)
    return user

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    # 4. This placement is also 100% valid!
    log.info("user_login", user_id=user.id, email=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}