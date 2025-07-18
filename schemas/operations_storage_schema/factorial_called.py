from sqlmodel import SQLModel, Field


class FactorialCalled(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    n: int
    result: str = Field(max_length=4000)  # VARCHAR2(100)
