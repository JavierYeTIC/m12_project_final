import datetime
from pydantic import BaseModel, EmailStr, SkipValidation

class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str
    created_at: SkipValidation[datetime.datetime]
    updated_at: SkipValidation[datetime.datetime]

    class Config:
        arbitrary_types_allowed = True


class LoginRequest(BaseModel):
    email: str
    password: str