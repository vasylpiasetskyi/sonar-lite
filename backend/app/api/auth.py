from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, UserCreate, UserLogin, UserRead
from app.services.auth.auth_service import (
    AuthService,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    try:
        user, token = await auth_service.register(data.email, data.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return AuthResponse(user=UserRead.model_validate(user), access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(
    data: UserLogin, auth_service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    try:
        user, token = await auth_service.authenticate(data.email, data.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return AuthResponse(user=UserRead.model_validate(user), access_token=token)
