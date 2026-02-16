from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin
from app.auth.models import User
from app.billing import schemas, service

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/subscription", response_model=schemas.SubscriptionWithLimits)
def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's subscription with usage and limits"""
    return service.BillingService.get_subscription_details(db, current_user)

@router.get("/plans", response_model=list[schemas.TierInfo])
def get_all_plans():
    """Get all available plans (for pricing page)"""
    return service.BillingService.get_all_tiers()

@router.post("/admin/upgrade-user/{user_id}")
def upgrade_user(
    user_id: int,
    tier: schemas.SubscriptionTier,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Admin upgrades user's subscription"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    subscription = service.BillingService.get_or_create_subscription(db, user)
    subscription.tier = tier
    db.commit()
    
    return {"message": f"Upgraded {user.email} to {tier}"}