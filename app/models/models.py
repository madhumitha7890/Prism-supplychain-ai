from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.utils.database import Base
from datetime import datetime

class Disruption(Base):
    __tablename__ = "disruptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    severity = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Intervention(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, index=True)
    disruption_id = Column(Integer, ForeignKey("disruptions.id"))
    action = Column(String)
    cost_saved = Column(Float)
    delay_avoided = Column(Integer)
