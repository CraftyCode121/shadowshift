from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.billing.plans import SubscriptionTier

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE)
    
    # ✅ FIX: Use server_default for integers
    images_used_this_month = Column(Integer, server_default="0")
    videos_used_this_month = Column(Integer, server_default="0")
    
    # ✅ FIX: Remove defaults, set in service layer
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    
    user = relationship("User", back_populates="subscription")