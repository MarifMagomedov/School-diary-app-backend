from pydantic import BaseModel


class UserRegisterForm(BaseModel):
    user_type: str
    user_id: str
    email: str
    password: str
    vk: str | None = None
    telegram: str | None = None


class UserLoginForm(BaseModel):
    email: str
    password: str
