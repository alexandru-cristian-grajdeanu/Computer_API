from sqlmodel import SQLModel, Field


class PowCalled(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    base: float
    exponent: float
    result: str = Field(max_length=4000)  # VARCHAR2(100)
