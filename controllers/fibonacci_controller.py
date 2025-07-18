from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from db import get_session
from schemas.math_schemas.fibonacci_schema import FibonacciRequest
from schemas.response_schema import OperationResponse
from services.db_service import save_operation
from services.math_services.n_fibonacci_service import compute_fibonacci
from logger import logger

router = APIRouter()


@router.post("/fibonacci", response_model=OperationResponse)
def fibonacci_endpoint(
        data: FibonacciRequest,
        request: Request,
        session: Session = Depends(get_session)
):
    try:
        logger.info(f"{request.method} {request.url.path} - n={data.n}")
        result = compute_fibonacci(data.n)
        logger.info(f"FIBONACCI result: {result}")
        save_operation(session, "fibonacci", data.model_dump(), str(result))
        return OperationResponse(operation="fibonacci", input=data.model_dump(), result=result)
    except Exception as e:
        logger.error("Error during FIBONACCI computation", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
