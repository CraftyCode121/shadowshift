from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import schemas, service
from app.auth.dependencies import get_current_user, get_current_admin
from app.auth.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return service.AuthService.register(db, user_data)

@router.post("/login", response_model=schemas.Token)
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    
    user = service.AuthService.login(db, login_data)
    token = service.AuthService.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    
    return current_user

@router.get("/admin-only")
def admin_route(admin: User = Depends(get_current_admin)):
    # example for admin endpoint
    return {"message": f"Hello admin {admin.email}"}