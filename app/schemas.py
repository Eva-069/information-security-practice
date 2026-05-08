import re
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from fastapi import HTTPException, status


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username: only latin letters, digits and _")
        return v

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if re.search(r"[<>&\"']", v):
            raise ValueError("Full name cannot contain < > & \" '")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user_id: int
    username: str
    roles: list[str] = []


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

    @field_validator("text")
    @classmethod
    def validate_no_html(cls, v):
        if re.search(r"[<>&]", v):
            raise ValueError("Text cannot contain HTML tags")
        return v