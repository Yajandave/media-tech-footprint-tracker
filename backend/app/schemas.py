from pydantic import BaseModel
from datetime import date, datetime

class TechnologyOut(BaseModel):
    id: int
    name: str
    category: str
    description: str | None = None

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: int
    product_name: str
    platform: str
    region: str
    business_unit: str

    model_config = {"from_attributes": True}


class IntegrationOut(BaseModel):
    id: int
    source_name: str
    source_type: str
    status: str
    last_sync: datetime

    model_config = {"from_attributes": True}


class UsageEventOut(BaseModel):
    id: int
    technology_id: int
    product_id: int
    integration_id: int
    date: date
    active_users: int
    playback_hours: float
    api_calls: int
    error_rate: float

    model_config = {"from_attributes": True}
