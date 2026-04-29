from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Technology
from ..schemas import TechnologyOut

router = APIRouter(prefix="/technologies", tags=["technologies"])

@router.get("", response_model=list[TechnologyOut])
def list_technologies(db: Session = Depends(get_db)):
    return db.query(Technology).order_by(Technology.name).all()
