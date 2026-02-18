from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin
from app.auth.models import User
from app.billing import service
from app.billing.plans import SubscriptionTier

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/my-subscription")
def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get my subscription details"""
    return service.BillingService.get_subscription_details(db, current_user)

@router.get("/plans")
def get_all_plans():
    """Get all available plans"""
    return service.BillingService.get_all_tiers()

@router.post("/admin/upgrade-user/{user_id}")
def admin_upgrade_user(
    user_id: int,
    tier: SubscriptionTier,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin manually upgrades user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    sub = service.BillingService.get_or_create_subscription(db, user)
    sub.tier = tier
    db.commit()
    
    return {"message": f"Upgraded {user.email} to {tier}"}