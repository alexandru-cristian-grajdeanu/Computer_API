import datetime

from sqlmodel import SQLModel, Field


class Operations(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    operation: str = Field(max_length=50)  # VARCHAR2(50)
    input_data: str = Field(max_length=1000)  # VARCHAR2(1000)
    result: str = Field(max_length=4000)  # VARCHAR2(100)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
