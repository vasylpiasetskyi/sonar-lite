from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth.security import create_access_token, hash_password, verify_password

# Precomputed hash with no matching password, compared against on an unknown
# email so a login attempt costs the same bcrypt time whether or not the
# account exists (closes the user-enumeration timing side-channel).
_DUMMY_PASSWORD_HASH = hash_password("not-a-real-password-used-only-for-timing")


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register(self, email: str, password: str) -> tuple[User, str]:
        existing = await self._repository.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegisteredError(f"Email already registered: {email}")

        try:
            user = await self._repository.create(email, hash_password(password))
        except IntegrityError as exc:
            raise EmailAlreadyRegisteredError(f"Email already registered: {email}") from exc

        token = create_access_token(user.id)
        return user, token

    async def authenticate(self, email: str, password: str) -> tuple[User, str]:
        user = await self._repository.get_by_email(email)
        if user is None:
            verify_password(password, _DUMMY_PASSWORD_HASH)
            raise InvalidCredentialsError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        token = create_access_token(user.id)
        return user, token
