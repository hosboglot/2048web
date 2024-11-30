import re
from typing import Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
from app.auth.utils import get_password_hash


class SGameCreate(BaseModel):
    name: str
    password: str

class SGameCreateDB(SGameCreate):
    host_id: int
