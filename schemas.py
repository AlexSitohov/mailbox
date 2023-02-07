import re
import uuid
from datetime import datetime

from fastapi import HTTPException

from pydantic import BaseModel, validator, Field, EmailStr

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    password: str
    name: str
    surname: str
    created_at: datetime

    class Config:
        orm_mode = True


class MailCreate(BaseModel):
    mail_body: str
    to_email: EmailStr

    class Config:
        orm_mode = True


class MailResponse(BaseModel):
    id: uuid.UUID
    mail_body: str
    from_email: EmailStr
    to_email: EmailStr

    class Config:
        orm_mode = True
