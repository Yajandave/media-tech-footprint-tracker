from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import UsageEvent
from ..schemas import UsageEventOut

router = APIRouter(prefix="/usage-events", tags=["usage-events"])

@router.get("", response_model=list[UsageEventOut])
def list_usage_events(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return db.query(UsageEvent).order_by(UsageEvent.date.desc()).limit(limit).all()
