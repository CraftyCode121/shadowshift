from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.billing.plans import SubscriptionTier
import enum

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE)
    
    # ✅ Track monthly usage
    images_used_this_month = Column(Integer, default=0)
    videos_used_this_month = Column(Integer, default=0)
    
    # ✅ Track when to reset counts
    current_period_start = Column(DateTime, server_default=func.now())
    current_period_end = Column(DateTime)  # 30 days from start
    
    user = relationship("User", back_populates="subscription")