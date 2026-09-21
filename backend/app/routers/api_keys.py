from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.security import require_roles
from backend.app.services.api_keys import (
    generate_api_key,
    hash_api_key,
)


router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)


@router.post("")
def create_api_key(
    name: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    ),
):
    raw_key = generate_api_key()

    db_key = models.APIKeyModel(
        name=name,
        key_hash=hash_api_key(raw_key),
        is_active=True,
    )

    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    return {
        "id": db_key.id,
        "name": db_key.name,
        "api_key": raw_key,
        "warning": (
            "Store this API key securely. "
            "It will not be shown again."
        ),
    }
