from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.auth import decode_access_token
from backend.app.dependencies import get_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = decode_access_token(
            token
        )

        username = payload.get(
            "sub"
        )

        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = (
        db.query(models.UserModel)
        .filter(
            models.UserModel.username
            == username
        )
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


def require_roles(
    *allowed_roles
):
    def role_checker(
        current_user=Depends(
            get_current_user
        )
    ):
        if (
            current_user.role
            not in allowed_roles
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "You do not have permission "
                    "to perform this action"
                )
            )

        return current_user

    return role_checker