from pydantic import BaseModel


class OperationResponse(BaseModel):
    operation: str
    input: dict
    result: int | float | str
