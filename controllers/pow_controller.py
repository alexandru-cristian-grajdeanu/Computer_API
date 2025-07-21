from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from db import get_session
from schemas.math_schemas.pow_schema import PowRequest
from schemas.responses_schemas.response_schema import OperationResponse
from services.db_service import save_operation
from services.math_services.pow_service import compute_pow
from logger import logger
from services.utils.jwt_check import verify_jwt

router = APIRouter()


@router.post("/pow", response_model=OperationResponse)
def pow_endpoint(
        data: PowRequest,
        request: Request,
        session: Session = Depends(get_session),
        token_data: dict = Depends(verify_jwt)
):
    try:
        logger.info(f"{request.method} {request.url.path} - base={data.base}, exponent={data.exponent}")
        result = compute_pow(data.base, data.exponent)
        logger.info(f"POW result: {result}")
        save_operation(session, "pow", data.model_dump(), str(result))
        return OperationResponse(operation="pow", input=data.model_dump(), result=result)
    except Exception as e:
        logger.error("Error during POW computation", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
