from pydantic import BaseModel, UUID4


class RegisterModel(BaseModel):
    role: int
    register_code: UUID4
    email: str
    hashed_password: str
    vk: str | None = None
    telegram: str | None = None


class LoginModel(BaseModel):
    role: int
    email: str
    password: str
