from pydantic import BaseModel, Field


class FibonacciRequest(BaseModel):
    n: int = Field(ge=0)
