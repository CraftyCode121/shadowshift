from pydantic import BaseModel
from datetime import datetime
from app.billing.plans import SubscriptionTier, TIER_LIMITS, MediaType

class SubscriptionResponse(BaseModel):
    tier: SubscriptionTier
    images_used_this_month: int
    videos_used_this_month: int
    current_period_end: datetime | None
    
    class Config:
        from_attributes = True

class SubscriptionWithLimits(BaseModel):
    tier: SubscriptionTier
    tier_name: str
    price: float
    
    images_used: int
    images_limit: int
    videos_used: int
    videos_limit: int
    
    max_image_size_mb: float
    max_video_duration_seconds: int
    max_video_size_mb: float
    
    features: list[str]

class TierInfo(BaseModel):
    """Info about a specific tier (for pricing page)"""
    tier: SubscriptionTier
    name: str
    price: float
    features: list[str]
    
    image_limit: int
    video_limit: int
    max_video_duration_seconds: int