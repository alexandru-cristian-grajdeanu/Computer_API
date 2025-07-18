from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from db import get_session
from schemas.math_schemas.factorial_schema import FactorialRequest
from schemas.math_schemas.fibonacci_schema import FibonacciRequest
from schemas.math_schemas.pow_schema import PowRequest
from schemas.response_schema import OperationResponse
from services.db_service import save_operation
from services.n_factorial_service import compute_factorial
from services.n_fibonacci_service import compute_fibonacci
from services.pow_service import compute_pow
from logger import logger

router = APIRouter()




@router.post("/factorial", response_model=OperationResponse)
def factorial_endpoint(
    data: FactorialRequest,
    request: Request,
    session: Session = Depends(get_session)
):
    try:
        logger.info(f"{request.method} {request.url.path} - n={data.n}")
        result = compute_factorial(data.n)
        logger.info(f"FACTORIAL result: {result}")
        save_operation(session, "factorial", data.model_dump(), str(result))
        return OperationResponse(operation="factorial", input=data.model_dump(), result=result)
    except Exception as e:
        logger.error("Error during FACTORIAL computation", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
