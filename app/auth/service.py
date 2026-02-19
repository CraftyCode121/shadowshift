from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.config import settings
from app.auth.models import User
from app.auth.schemas import UserCreate, UserLogin
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Create short-lived access token (30 min)"""
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"  # ✅ Token type
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def create_refresh_token() -> str:
        """Create long-lived refresh token (7 days) - just a random string"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_refresh_token_expiry() -> datetime:
        """Calculate refresh token expiry"""
        return datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> User:
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = User(
            email=user_data.email,
            hashed_password=AuthService.hash_password(user_data.password),
            name=user_data.name,
            full_name=user_data.full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def login(db: Session, login_data: UserLogin) -> tuple[User, str, str]:
        """Login and return user + tokens"""
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user or not AuthService.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        access_token = AuthService.create_access_token(user.id)
        refresh_token = AuthService.create_refresh_token()
        
        user.refresh_token = refresh_token
        user.refresh_token_expires_at = AuthService.get_refresh_token_expiry()
        db.commit()
        
        return user, access_token, refresh_token
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> str:
        """Use refresh token to get new access token"""
        
        user = db.query(User).filter(User.refresh_token == refresh_token).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        if user.refresh_token_expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired, please login again"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        new_access_token = AuthService.create_access_token(user.id)
        
        return new_access_token
    
    @staticmethod
    def logout(db: Session, user: User):
        """Invalidate refresh token"""
        user.refresh_token = None
        user.refresh_token_expires_at = None
        db.commit()