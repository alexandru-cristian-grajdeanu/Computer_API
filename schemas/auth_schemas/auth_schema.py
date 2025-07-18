from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserAccounts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(max_length=255, unique=True, nullable=False)
    password: str = Field(max_length=4000, nullable=False)
