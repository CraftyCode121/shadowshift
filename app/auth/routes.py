from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import schemas, service
from app.auth.dependencies import get_current_user
from app.auth.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return service.AuthService.register(db, user_data)

@router.post("/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login and receive access + refresh tokens"""
    user, access_token, refresh_token = service.AuthService.login(db, login_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # ✅ Return both tokens
        "token_type": "bearer"
    }

# ✅ NEW: Refresh token endpoint
@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(
    token_data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Use refresh token to get new access token"""
    new_access_token = service.AuthService.refresh_access_token(db, token_data.refresh_token)
    
    return {
        "access_token": new_access_token,
        "refresh_token": token_data.refresh_token,  # Same refresh token
        "token_type": "bearer"
    }

# ✅ NEW: Logout endpoint
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout and invalidate refresh token"""
    service.AuthService.logout(db, current_user)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info"""
    return current_user