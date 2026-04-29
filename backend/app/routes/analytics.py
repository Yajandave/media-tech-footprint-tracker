from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Technology, Product, UsageEvent, Integration

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _filtered_usage_query(
    db: Session,
    *entities,
    region: str | None = None,
    platform: str | None = None,
    technology: str | None = None,
):
    query = (
        db.query(*entities)
        .select_from(UsageEvent)
        .join(Technology, UsageEvent.technology_id == Technology.id)
        .join(Product, UsageEvent.product_id == Product.id)
    )

    if region:
        query = query.filter(Product.region == region)
    if platform:
        query = query.filter(Product.platform == platform)
    if technology:
        query = query.filter(Technology.name == technology)

    return query


@router.get("/summary")
def analytics_summary(
    region: str | None = Query(None, description="Filter by product region"),
    platform: str | None = Query(None, description="Filter by product platform"),
    technology: str | None = Query(None, description="Filter by technology name"),
    db: Session = Depends(get_db),
):
    total_technologies = _filtered_usage_query(
        db,
        func.count(func.distinct(Technology.id)),
        region=region,
        platform=platform,
        technology=technology,
    ).scalar() or 0
    total_products = _filtered_usage_query(
        db,
        func.count(func.distinct(Product.id)),
        region=region,
        platform=platform,
        technology=technology,
    ).scalar() or 0
    total_usage_events = _filtered_usage_query(
        db,
        func.count(UsageEvent.id),
        region=region,
        platform=platform,
        technology=technology,
    ).scalar() or 0

    totals = _filtered_usage_query(
        db,
        func.sum(UsageEvent.active_users),
        func.sum(UsageEvent.playback_hours),
        func.avg(UsageEvent.error_rate),
        region=region,
        platform=platform,
        technology=technology,
    ).first()

    top_technology = (
        _filtered_usage_query(
            db,
            Technology.name,
            func.sum(UsageEvent.active_users).label("users"),
            region=region,
            platform=platform,
            technology=technology,
        )
        .group_by(Technology.name)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .first()
    )

    top_region = (
        _filtered_usage_query(
            db,
            Product.region,
            func.sum(UsageEvent.active_users).label("users"),
            region=region,
            platform=platform,
            technology=technology,
        )
        .group_by(Product.region)
        .order_by(func.sum(UsageEvent.active_users).desc())
        .first()
    )

    return {
        "total_technologies": int(total_technologies),
        "total_products": int(total_products),
        "total_usage_events": int(total_usage_events),
        "total_active_users": int(totals[0] or 0),
        "total_playback_hours": round(float(totals[1] or 0), 2),
        "average_error_rate": round(float(totals[2] or 0), 3),
        "highest_adoption_technology": top_technology[0] if top_technology else None,
        "top_region": top_region[0] if top_region else None,
    }


@router.get("/technology-adoption")
def technology_adoption(
    region: str | None = Query(None, description="Filter by product region"),
    platform: str | None = Query(None, description="Filter by product platform"),
    technology: str | None = Query(None, description="Filter by technology name"),
    db: Session = Depends(get_db),
):
    rows = (
        _filtered_usage_query(
            db,
            Technology.name.label("technology"),
            Technology.category.label("category"),
            func.sum(UsageEvent.active_users).label("active_users"),
            func.sum(UsageEvent.playback_hours).label("playback_hours"),
            func.avg(UsageEvent.error_rate).label("average_error_rate"),
            region=region,
            platform=platform,
            technology=technology,
        )
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
def regional_usage(
    region: str | None = Query(None, description="Filter by product region"),
    platform: str | None = Query(None, description="Filter by product platform"),
    technology: str | None = Query(None, description="Filter by technology name"),
    db: Session = Depends(get_db),
):
    rows = (
        _filtered_usage_query(
            db,
            Product.region.label("region"),
            Product.platform.label("platform"),
            func.sum(UsageEvent.active_users).label("active_users"),
            func.sum(UsageEvent.playback_hours).label("playback_hours"),
            region=region,
            platform=platform,
            technology=technology,
        )
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
            Integration.last_sync,
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


@router.get("/usage-trends")
def usage_trends(
    region: str | None = Query(None, description="Filter by product region"),
    platform: str | None = Query(None, description="Filter by product platform"),
    technology: str | None = Query(None, description="Filter by technology name"),
    db: Session = Depends(get_db),
):
    rows = (
        _filtered_usage_query(
            db,
            UsageEvent.date.label("date"),
            func.sum(UsageEvent.active_users).label("active_users"),
            func.sum(UsageEvent.playback_hours).label("playback_hours"),
            func.sum(UsageEvent.api_calls).label("api_calls"),
            region=region,
            platform=platform,
            technology=technology,
        )
        .group_by(UsageEvent.date)
        .order_by(UsageEvent.date.asc())
        .all()
    )

    return [
        {
            "date": row.date,
            "active_users": int(row.active_users),
            "playback_hours": round(float(row.playback_hours), 2),
            "api_calls": int(row.api_calls),
        }
        for row in rows
    ]
