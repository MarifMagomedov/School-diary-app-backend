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
            payload = jwt.decode(token, self.config.jwt_secret, algorithms=[self.config.algorithm])
            email = payload.get("email")
            if email is None:
                raise errors.InvalidToken()
            return payload
        except jwt.exceptions.PyJWTError:
            print(1)
            raise errors.InvalidToken()

    async def register_user(self, form: RegisterModel, user_registered: bool) -> None:
        if user_registered:
            raise errors.UserAlreadyRegister()
        form.hashed_password = self.context.hash(form.hashed_password)
        token = await self.create_token(email=form.email)
        return token

    async def login_user(self, email: str, password: str, hashed_password: str, user_registered: bool) -> str:
        if not self.context.verify(password, hashed_password):
            raise errors.InvalidLoginData()
        if not user_registered:
            errors.UserAlreadyNotRegister()
        return await self.create_token(email=email)
