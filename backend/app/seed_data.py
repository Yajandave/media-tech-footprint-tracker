from datetime import date, datetime, timedelta
from random import choice, randint, uniform, seed
from .database import Base, engine, SessionLocal
from .models import Technology, Product, Integration, UsageEvent

seed(42)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_seed_data():
    db = SessionLocal()

    technologies = [
        Technology(name="Spatial Audio", category="Audio", description="Immersive audio experience"),
        Technology(name="HDR Video", category="Video", description="High dynamic range visual experience"),
        Technology(name="Voice Enhancement", category="Voice", description="Speech clarity and noise reduction"),
        Technology(name="Noise Reduction", category="Audio", description="Signal processing for cleaner audio"),
        Technology(name="Gaming Audio", category="Audio", description="Low-latency interactive audio"),
        Technology(name="Cinema Audio", category="Audio", description="Theatrical sound experience"),
    ]

    products = []
    regions = ["Europe", "North America", "Asia-Pacific", "Latin America"]
    platforms = ["Streaming", "Gaming", "Mobile", "Cinema", "Automotive"]
    business_units = ["Consumer Entertainment", "Partner Platforms", "Cinema", "Automotive"]

    for i in range(1, 25):
        products.append(
            Product(
                product_name=f"Product {i}",
                platform=choice(platforms),
                region=choice(regions),
                business_unit=choice(business_units),
            )
        )

    integrations = [
        Integration(source_name="Partner API", source_type="API", status="Active", last_sync=datetime.utcnow()),
        Integration(source_name="Daily CSV Upload", source_type="CSV", status="Active", last_sync=datetime.utcnow()),
        Integration(source_name="Internal Product Tool", source_type="Internal", status="Warning", last_sync=datetime.utcnow() - timedelta(hours=6)),
        Integration(source_name="Legacy Reporting Feed", source_type="Batch", status="Delayed", last_sync=datetime.utcnow() - timedelta(days=1)),
    ]

    db.add_all(technologies + products + integrations)
    db.commit()

    for item in technologies + products + integrations:
        db.refresh(item)

    start_date = date(2026, 1, 1)

    for day_offset in range(120):
        current_date = start_date + timedelta(days=day_offset)

        for _ in range(12):
            tech = choice(technologies)
            product = choice(products)
            integration = choice(integrations)

            base_users = randint(1000, 25000)
            if tech.name == "Spatial Audio":
                base_users = int(base_users * 1.25)
            if product.region == "Europe":
                base_users = int(base_users * 1.10)

            event = UsageEvent(
                technology_id=tech.id,
                product_id=product.id,
                integration_id=integration.id,
                date=current_date,
                active_users=base_users,
                playback_hours=round(base_users * uniform(1.2, 3.8), 2),
                api_calls=base_users * randint(15, 80),
                error_rate=round(uniform(0.1, 2.5), 3),
            )
            db.add(event)

    db.commit()
    db.close()

if __name__ == "__main__":
    reset_database()
    create_seed_data()
    print("Seed data created successfully.")
