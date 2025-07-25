from sqlmodel import SQLModel, Field


class UserAccounts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    password: str = Field(max_length=4000, nullable=False)
