from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from db import get_session
from schemas.math_schemas.factorial_schema import FactorialRequest
from schemas.responses_schemas.response_schema import OperationResponse
from services.db_service import save_operation
from services.math_services.n_factorial_service import compute_factorial
from logger import logger
from services.utils.jwt_check import verify_jwt

router = APIRouter()




@router.post("/factorial", response_model=OperationResponse)
def factorial_endpoint(
    data: FactorialRequest,
    request: Request,
    session: Session = Depends(get_session),
    token_data: dict = Depends(verify_jwt)
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
