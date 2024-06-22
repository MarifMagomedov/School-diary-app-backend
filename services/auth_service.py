from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext
from pydantic import UUID4

import utils.errors.auth_errors as errors
from config import load_jwt_config
from dto.auth import RegisterModel


class AuthService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.config = load_jwt_config()

    async def create_token(self, **kwargs):
        expire = datetime.now() + timedelta(minutes=self.config.access_token_time)
        kwargs.update({"exp": expire})
        token = jwt.encode(kwargs, self.config.jwt_secret, algorithm=self.config.algorithm)
        return token

    async def verify_token(self, token):
        try:
            payload = jwt.decode(token.credentials, self.config.jwt_secret, algorithms=[self.config.algorithm])
            email = payload.get("email")
            role = payload.get("role")
            if email is None or role is None:
                raise errors.InvalidToken()
            return payload
        except (jwt.exceptions.PyJWTError, AttributeError) as e:
            raise errors.InvalidToken()

    async def register_user(self, form: RegisterModel, user_registered: bool) -> None:
        if user_registered:
            raise errors.UserAlreadyRegister()
        form.hashed_password = self.context.hash(form.hashed_password)
        token = await self.create_token(email=form.email, role=form.role)
        return token

    async def login_user(self, email: str, password: str, user) -> str:
        if not user or not self.context.verify(password, user.hashed_password):
            raise errors.InvalidLoginData()
        if not user.registered:
            errors.UserAlreadyNotRegister()
        return await self.create_token(email=email, role=user.role)

    @staticmethod
    async def check_role(user_role: int, token_role: int):
        if user_role != token_role:
            raise errors.InvalidUserRole()
