from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Technology, Product, UsageEvent, Integration

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    total_technologies = db.query(Technology).count()
    total_products = db.query(Product).count()
    total_usage_events = db.query(UsageEvent).count()

    totals = (
        db.query(
            func.sum(UsageEvent.active_users),
            func.sum(UsageEvent.playback_hours),
            func.avg(UsageEvent.error_rate)
        )
        .first()
    )

    top_technology = (
        db.query(Technology.name, func.sum(UsageEvent.active_users).label("users"))
        .join(UsageEvent)
        .group_by(Technology.name)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .first()
    )

    top_region = (
        db.query(Product.region, func.sum(UsageEvent.active_users).label("users"))
        .join(UsageEvent)
        .group_by(Product.region)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .first()
    )

    return {
        "total_technologies": total_technologies,
        "total_products": total_products,
        "total_usage_events": total_usage_events,
        "total_active_users": int(totals[0] or 0),
        "total_playback_hours": round(float(totals[1] or 0), 2),
        "average_error_rate": round(float(totals[2] or 0), 3),
        "highest_adoption_technology": top_technology[0] if top_technology else None,
        "top_region": top_region[0] if top_region else None,
    }


@router.get("/technology-adoption")
def technology_adoption(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Technology.name.label("technology"),
            Technology.category.label("category"),
            func.sum(UsageEvent.active_users).label("active_users"),
            func.sum(UsageEvent.playback_hours).label("playback_hours"),
            func.avg(UsageEvent.error_rate).label("average_error_rate"),
        )
        .join(UsageEvent)
        .group_by(Technology.name, Technology.category)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .all()
    )

    return [
        {
            "technology": row.technology,
            "category": row.category,
            "active_users": int(row.active_users),
            "playback_hours": round(float(row.playback_hours), 2),
            "average_error_rate": round(float(row.average_error_rate), 3),
        }
        for row in rows
    ]


@router.get("/regional-usage")
def regional_usage(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Product.region.label("region"),
            Product.platform.label("platform"),
            func.sum(UsageEvent.active_users).label("active_users"),
            func.sum(UsageEvent.playback_hours).label("playback_hours"),
        )
        .join(UsageEvent)
        .group_by(Product.region, Product.platform)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .all()
    )

    return [
        {
            "region": row.region,
            "platform": row.platform,
            "active_users": int(row.active_users),
            "playback_hours": round(float(row.playback_hours), 2),
        }
        for row in rows
    ]


@router.get("/integration-health")
def integration_health(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Integration.source_name,
            Integration.source_type,
            Integration.status,
            Integration.last_sync,
            func.count(UsageEvent.id).label("events_received"),
            func.avg(UsageEvent.error_rate).label("average_error_rate"),
        )
        .join(UsageEvent, UsageEvent.integration_id == Integration.id)
        .group_by(
            Integration.source_name,
            Integration.source_type,
            Integration.status,
            Integration.last_sync
        )
        .all()
    )

    return [
        {
            "source_name": row.source_name,
            "source_type": row.source_type,
            "status": row.status,
            "last_sync": row.last_sync,
            "events_received": int(row.events_received),
            "average_error_rate": round(float(row.average_error_rate), 3),
        }
        for row in rows
    ]
