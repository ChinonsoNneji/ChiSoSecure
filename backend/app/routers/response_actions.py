from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.response import (
    execute_response_action,
)
from backend.app.schemas import (
    ResponseActionCreate,
)
from backend.app.security import (
    require_roles,
)


router = APIRouter(
    tags=["Response Actions"]
)


@router.post("/response-actions")
def create_response_action(
    action: ResponseActionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst"
        )
    )
):
    incident = (
        db.query(models.IncidentModel)
        .filter(
            models.IncidentModel.id
            == action.incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    execution = execute_response_action(
        action.action_type,
        action.target
    )

    response_action = (
        models.ResponseActionModel(
            incident_id=action.incident_id,
            action_type=action.action_type,
            target=action.target,
            status=execution["status"],
            result=execution["result"]
        )
    )

    db.add(response_action)
    db.commit()
    db.refresh(response_action)

    return {
        "message": (
            "Response action executed"
        ),
        "response_action": response_action
    }


@router.get("/response-actions")
def get_response_actions(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst",
            "viewer"
        )
    )
):
    actions = (
        db.query(
            models.ResponseActionModel
        )
        .order_by(
            models.ResponseActionModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(actions),
        "response_actions": actions
    }


@router.get(
    "/incidents/{incident_id}/response-actions"
)
def get_incident_response_actions(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst",
            "viewer"
        )
    )
):
    incident = (
        db.query(models.IncidentModel)
        .filter(
            models.IncidentModel.id
            == incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    actions = (
        db.query(
            models.ResponseActionModel
        )
        .filter(
            models.ResponseActionModel.incident_id
            == incident_id
        )
        .order_by(
            models.ResponseActionModel.id.desc()
        )
        .all()
    )

    return {
        "incident_id": incident_id,
        "count": len(actions),
        "response_actions": actions
    }