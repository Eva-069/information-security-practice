import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=150)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
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