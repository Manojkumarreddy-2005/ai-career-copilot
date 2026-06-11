import sys
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, ExpiredSignatureError

from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import register_user, login_user
from app.core.security import decode_token
from app.repositories.user_repository import get_user_by_id
from app.models.user import User

# Keep your local path layout working for now
sys.path.append("../../")
from shared.database.connection import get_db

router = APIRouter()
bearer_scheme = HTTPBearer()


# 1. This reusable dependency protects ANY route you plug it into
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        
        # Guard clause: Ensure they aren't using a refresh token to access data
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Expected access token."
            )
            
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user identity info."
            )
            
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload.email, payload.password, payload.first_name, payload.last_name)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, payload.email, payload.password)


# 2. Look how beautifully clean this route becomes now!
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user