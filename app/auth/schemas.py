from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_lenght=128)
    name: str = Field(..., min_length=4)
    full_name: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_lenght=128)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    full_name: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"