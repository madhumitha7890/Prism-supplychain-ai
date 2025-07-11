from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from app.models import models
from datetime import datetime

import logging
logging.info("Simulation new disruption:{new_disruption.name} (ID: {new_disruption.id})")

router = APIRouter()

@router.post("/simulate")
def simulate_disruption(db: Session = Depends(get_db)):
    # Simulate a test disruption (e.g., Port of Mundra blocked)
    new_disruption = models.Disruption(
        name="Port of Mundra Blocked",
        location="Gujarat",
        severity="High",
        created_at=datetime.utcnow()
    )
    
    db.add(new_disruption)
    db.commit()
    db.refresh(new_disruption)

    return {
        "message": "Disruption recorded",
        "disruption_id": new_disruption.id,
        "location": new_disruption.location,
        "severity": new_disruption.severity
    }
@router.get("/impact/{disruption_id}")
def get_disruption_impact(disruption_id: int, db: Session = Depends(get_db)):
    try:
        disruption = db.query(models.Disruption).filter(models.Disruption.id == disruption_id).first()
        if not disruption:
            return {"error": f"Disruption ID {disruption_id} not found"}

        # Mocked prediction
        return {
            "disruption_id": disruption.id,
            "impact_prediction": {
                "predicted_loss": "₹4.2 Cr",
                "delay_days": 14,
                "affected_zones": ["Delhi", "Mumbai"]
            }
        }

    except Exception as e:
        return {"error": str(e)}


@router.post("/intervene/{disruption_id}")
def suggest_intervention(disruption_id: int, db: Session = Depends(get_db)):
    disruption = db.query(models.Disruption).filter(models.Disruption.id == disruption_id).first()

    if not disruption:
        return {"error": "Disruption not found"}

    # 🔮 MOCK RL-based recommendation (replace later)
    mock_action = {
        "action": "Reroute via Chennai port using air freight",
        "cost_saved": 3.8,  # in Cr
        "delay_avoided": 7  # in days
    }

    # Save to database
    new_intervention = models.Intervention(
        disruption_id=disruption.id,
        action=mock_action["action"],
        cost_saved=mock_action["cost_saved"],
        delay_avoided=mock_action["delay_avoided"]
    )

    db.add(new_intervention)
    db.commit()
    db.refresh(new_intervention)

    return {
        "message": "Intervention saved",
        "intervention_id": new_intervention.id,
        "recommended_action": mock_action["action"],
        "cost_saved (Cr)": mock_action["cost_saved"],
        "delay_avoided (days)": mock_action["delay_avoided"]
    }
@router.get("/health")
def health_check():
    return {"status": "Backend is alive", "docker": True}
