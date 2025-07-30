from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session
from starlette.status import (HTTP_400_BAD_REQUEST,
                              HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from db import get_session
from exceptions.PowTooLargeError import PowTooLargeError
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
        logger.info(f"{request.method} {request.url.path} - "
                    f"base={data.base}, exponent={data.exponent}")
        result = compute_pow(data.base, data.exponent)
        logger.info(f"POW result: {result}")
        save_operation(session, "pow", data.model_dump(), str(result))
        return OperationResponse(operation="pow",
                                 input=data.model_dump(),
                                 result=result)

    except PowTooLargeError as e:
        logger.warning("Pow too large to compute", exc_info=True)
        raise HTTPException(
            status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"code": 413, "message": str(e)}
        )

    except ValueError as e:
        logger.warning("Invalid input", exc_info=True)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": str(e)}
        )

    except Exception as e:
        logger.error("Unexpected error during POW computation", exc_info=True)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"Internal server error: {e}"}
        )
