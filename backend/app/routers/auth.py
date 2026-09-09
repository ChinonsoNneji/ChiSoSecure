from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.dependencies import get_db
from backend.app.schemas import (
    TokenResponse,
    UserRegister,
    UserResponse,
)
from backend.app.security import (
    get_current_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.UserModel)
        .filter(
            models.UserModel.username
            == user.username
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    db_user = models.UserModel(
        username=user.username,
        hashed_password=hash_password(
            user.password
        ),
        role="viewer"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.UserModel)
        .filter(
            models.UserModel.username
            == form_data.username
        )
        .first()
    )

    if (
        user is None
        or not verify_password(
            form_data.password,
            user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = create_access_token(
        username=user.username,
        role=user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(
        get_current_user
    )
):
    return current_user