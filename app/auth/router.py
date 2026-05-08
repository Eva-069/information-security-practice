from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.models import User
from app.auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from app.auth.dependencies import get_current_user
from app.schemas import TokenResponse, TokenRefreshRequest, UserInfo, UserCreate, UserResponse, CommentCreate
from app.security import verify_password, hash_password
from app.middleware.rate_limiter import limiter
from app.validators.sanitizer import sanitize_text, contains_sql_patterns

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail=f"User '{user_data.username}' already exists")

    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail=f"Email '{user_data.email}' already registered")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    role = user.roles[0].name if user.roles else "student"
    access_token = create_access_token(user.id, role)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: TokenRefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_token(body.refresh_token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token required")

    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = user.roles[0].name if user.roles else "student"
    return TokenResponse(
        access_token=create_access_token(user_id, role),
        refresh_token=create_refresh_token(user_id)
    )


@router.get("/me", response_model=UserInfo)
def get_me(current_user: User = Depends(get_current_user)):
    role = current_user.roles[0].name if current_user.roles else "student"
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=role,
    )


@router.post("/demo/comment")
def demo_comment(comment: CommentCreate):
    if contains_sql_patterns(comment.text):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SQL patterns detected"
        )
    clean_text = sanitize_text(comment.text)
    return {"original": comment.text, "sanitized": clean_text}