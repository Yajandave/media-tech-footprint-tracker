from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

    usage_events = relationship("UsageEvent", back_populates="technology")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    region = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)

    usage_events = relationship("UsageEvent", back_populates="product")


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    last_sync = Column(DateTime, default=datetime.utcnow)


class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(Integer, primary_key=True, index=True)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=False)

    date = Column(Date, nullable=False)
    active_users = Column(Integer, nullable=False)
    playback_hours = Column(Float, nullable=False)
    api_calls = Column(Integer, nullable=False)
    error_rate = Column(Float, nullable=False)

    technology = relationship("Technology", back_populates="usage_events")
    product = relationship("Product", back_populates="usage_events")
    integration = relationship("Integration")
