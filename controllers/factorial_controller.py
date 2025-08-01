from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from db import get_session
from exceptions.FactorialTooLargeError import FactorialTooLargeError
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
        return OperationResponse(operation="factorial",
                                 input=data.model_dump(), result=result)

    except FactorialTooLargeError as e:
        logger.error("Factorial too large to compute", exc_info=True)
        raise HTTPException(
            status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"code": 413, "message": str(e)}
        )

    except ValueError as e:
        logger.warning("Invalid factorial input", exc_info=True)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": str(e)}
        )

    except Exception as e:
        logger.error("Unexpected error during FACTORIAL computation",
                     exc_info=True)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"Internal server error: {e}"}
        )
