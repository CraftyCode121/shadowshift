from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.billing.models import Subscription
from app.billing.plans import SubscriptionTier, TIER_LIMITS, MediaType, get_tier_limit
from app.auth.models import User
from datetime import datetime, timedelta

class BillingService:
    
    @staticmethod
    def get_or_create_subscription(db: Session, user: User) -> Subscription:
        """Get user's subscription"""
        subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        
        if not subscription:
            now = datetime.utcnow()
            subscription = Subscription(
                user_id=user.id,
                tier=SubscriptionTier.FREE,
                current_period_start=now,
                current_period_end=now + timedelta(days=30)
            )
            db.add(subscription)
            db.commit()
            db.refresh(subscription)
        
        return subscription
    
    @staticmethod
    def reset_usage_if_needed(db: Session, subscription: Subscription):
        """Reset monthly counters if period ended"""
        if subscription.current_period_end and datetime.utcnow() > subscription.current_period_end:
            subscription.images_used_this_month = 0
            subscription.videos_used_this_month = 0
            subscription.current_period_start = datetime.utcnow()
            subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            db.commit()
    
    @staticmethod
    def can_process_media(
        db: Session,
        user: User,
        media_type: MediaType,
        file_size_mb: float = None,
        duration_seconds: int = None
    ) -> tuple[bool, str]:
        """Check if user can process this media"""
        
        subscription = BillingService.get_or_create_subscription(db, user)
        BillingService.reset_usage_if_needed(db, subscription)
        
        tier = subscription.tier
        limits = TIER_LIMITS[tier]["limits"][media_type]
        
        if media_type == MediaType.IMAGE:
            if subscription.images_used_this_month >= limits["count_per_month"]:
                return False, f"Monthly image limit reached ({limits['count_per_month']}). Upgrade to process more."
        else:
            if subscription.videos_used_this_month >= limits["count_per_month"]:
                return False, f"Monthly video limit reached ({limits['count_per_month']}). Upgrade to process more."
        
        if file_size_mb and file_size_mb > limits["max_size_mb"]:
            return False, f"File too large. Max size: {limits['max_size_mb']}MB"
        
        if media_type == MediaType.VIDEO and duration_seconds:
            if duration_seconds > limits["max_duration_seconds"]:
                max_minutes = limits["max_duration_seconds"] / 60
                return False, f"Video too long. Max duration: {max_minutes} minutes"
        
        return True, "OK"
    
    @staticmethod
    def increment_usage(db: Session, user: User, media_type: MediaType):
        """Increment usage counter after processing"""
        subscription = BillingService.get_or_create_subscription(db, user)
        
        if media_type == MediaType.IMAGE:
            subscription.images_used_this_month += 1
        else:
            subscription.videos_used_this_month += 1
        
        db.commit()
    
    @staticmethod
    def get_subscription_details(db: Session, user: User):
        """Get full subscription info with limits"""
        subscription = BillingService.get_or_create_subscription(db, user)
        BillingService.reset_usage_if_needed(db, subscription)
        
        tier = subscription.tier
        tier_config = TIER_LIMITS[tier]
        
        return {
            "tier": tier,
            "tier_name": tier_config["name"],
            "price": tier_config["price"],
            
            "images_used": subscription.images_used_this_month,
            "images_limit": tier_config["limits"][MediaType.IMAGE]["count_per_month"],
            
            "videos_used": subscription.videos_used_this_month,
            "videos_limit": tier_config["limits"][MediaType.VIDEO]["count_per_month"],
            
            "max_image_size_mb": tier_config["limits"][MediaType.IMAGE]["max_size_mb"],
            "max_video_duration_seconds": tier_config["limits"][MediaType.VIDEO]["max_duration_seconds"],
            "max_video_size_mb": tier_config["limits"][MediaType.VIDEO]["max_size_mb"],
            
            "features": tier_config["features"]
        }
    
    @staticmethod
    def get_all_tiers():
        """Get info about all tiers (for pricing page)"""
        tiers = []
        for tier, config in TIER_LIMITS.items():
            tiers.append({
                "tier": tier,
                "name": config["name"],
                "price": config["price"],
                "features": config["features"],
                "image_limit": config["limits"][MediaType.IMAGE]["count_per_month"],
                "video_limit": config["limits"][MediaType.VIDEO]["count_per_month"],
                "max_video_duration_seconds": config["limits"][MediaType.VIDEO]["max_duration_seconds"]
            })
        return tiers