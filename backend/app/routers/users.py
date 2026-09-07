from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.schemas import (
    UserRoleUpdate,
)
from backend.app.security import (
    require_roles,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    )
):
    users = (
        db.query(models.UserModel)
        .order_by(
            models.UserModel.id.asc()
        )
        .all()
    )

    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "created_at": user.created_at
            }
            for user in users
        ]
    }


@router.patch(
    "/{user_id}/role"
)
def update_user_role(
    user_id: int,
    update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    )
):
    user = (
        db.query(models.UserModel)
        .filter(
            models.UserModel.id
            == user_id
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = update.role

    db.commit()
    db.refresh(user)

    return {
        "message": "User role updated",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }