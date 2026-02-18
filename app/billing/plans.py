from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

# Tier configurations
TIER_LIMITS = {
    SubscriptionTier.FREE: {
        "name": "Free",
        "price": 0,
        "limits": {
            MediaType.IMAGE: {
                "count_per_month": 5,
                "max_size_mb": 5,
                "max_resolution": "1920x1080"
            },
            MediaType.VIDEO: {
                "count_per_month": 2,
                "max_duration_seconds": 30,
                "max_size_mb": 50,
                "max_resolution": "1280x720"
            }
        },
        "features": [
            "5 images/month",
            "2 videos/month (30 sec max)",
            "HD quality (720p)",
            "Basic enhancement"
        ]
    },
    
    SubscriptionTier.BASIC: {
        "name": "Basic",
        "price": 2500,
        "limits": {
            MediaType.IMAGE: {
                "count_per_month": 50,
                "max_size_mb": 20,
                "max_resolution": "3840x2160"
            },
            MediaType.VIDEO: {
                "count_per_month": 20,
                "max_duration_seconds": 300,
                "max_size_mb": 500,
                "max_resolution": "1920x1080"
            }
        },
        "features": [
            "50 images/month",
            "20 videos/month (5 min max)",
            "Full HD quality (1080p)",
            "Advanced enhancement",
            "Priority processing"
        ]
    },
    
    SubscriptionTier.PRO: {
        "name": "Pro",
        "price": 7500,
        "limits": {
            MediaType.IMAGE: {
                "count_per_month": 200,
                "max_size_mb": 50,
                "max_resolution": "7680x4320"
            },
            MediaType.VIDEO: {
                "count_per_month": 100,
                "max_duration_seconds": 1800,
                "max_size_mb": 5000,
                "max_resolution": "3840x2160"
            }
        },
        "features": [
            "200 images/month",
            "100 videos/month (30 min max)",
            "4K quality",
            "Premium enhancement",
            "Fastest processing",
            "Bulk processing",
            "API access"
        ]
    }
}

def get_tier_limit(tier: SubscriptionTier, media_type: MediaType, limit_key: str):
    """Helper to get specific limit"""
    return TIER_LIMITS[tier]["limits"][media_type][limit_key]