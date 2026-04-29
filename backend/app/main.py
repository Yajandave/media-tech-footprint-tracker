import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import technologies, products, usage_events, analytics

LOCAL_FRONTEND_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


def get_allowed_origins():
    configured_origins = os.getenv("ALLOWED_ORIGINS")
    if not configured_origins:
        return LOCAL_FRONTEND_ORIGINS

    return [
        origin.strip().rstrip("/")
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Technology Footprint Tracker API",
    version="0.1.0",
    description="Synthetic internal analytics platform for media technology usage tracking."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(technologies.router)
app.include_router(products.router)
app.include_router(usage_events.router)
app.include_router(analytics.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
