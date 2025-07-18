from pydantic import BaseModel


class PowRequest(BaseModel):
    base: float
    exponent: float
