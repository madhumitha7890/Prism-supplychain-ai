from app.utils.database import SessionLocal
from app.models.models import Disruption
from datetime import datetime

db = SessionLocal()

sample_disruptions = [
    {"name": "Port Strike – Chennai", "location": "Tamil Nadu", "severity": "High"},
    {"name": "Flooded Highways – Assam", "location": "Assam", "severity": "Medium"},
    {"name": "Cargo Delay – Singapore", "location": "Singapore Route", "severity": "High"},
    {"name": "Labor Protest – Punjab", "location": "Punjab", "severity": "Low"},
    {"name": "Port Congestion – Nhava Sheva", "location": "Maharashtra", "severity": "Medium"},
]

for d in sample_disruptions:
    disruption = Disruption(
        name=d["name"],
        location=d["location"],
        severity=d["severity"],
        created_at=datetime.utcnow()
    )
    db.add(disruption)

db.commit()
db.close()

print("✅ Seeded 5 disruptions into the DB.")
