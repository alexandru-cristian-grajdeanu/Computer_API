from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session

from db import get_session
from exceptions.FibonacciTooLargeError import FibonacciTooLargeError
from schemas.math_schemas.fibonacci_schema import FibonacciRequest
from schemas.responses_schemas.response_schema import OperationResponse
from services.db_service import save_operation
from services.math_services.n_fibonacci_service import compute_fibonacci
from logger import logger
from services.utils.jwt_check import verify_jwt

from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_500_INTERNAL_SERVER_ERROR
)

router = APIRouter()


@router.post("/fibonacci", response_model=OperationResponse)
def fibonacci_endpoint(
        data: FibonacciRequest,
        request: Request,
        session: Session = Depends(get_session),
        token_data: dict = Depends(verify_jwt)
):
    try:
        logger.info(f"{request.method} {request.url.path} - n={data.n}")
        result = compute_fibonacci(data.n)
        logger.info(f"FIBONACCI result: {result}")
        save_operation(session, "fibonacci", data.model_dump(), str(result))
        return OperationResponse(operation="fibonacci", input=data.model_dump(), result=result)

    except FibonacciTooLargeError as e:
        logger.error("Fibonacci too large to compute", exc_info=True)
        return JSONResponse(
            status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"code": 413, "message": str(e)}
        )

    except ValueError as e:
        logger.warning("Invalid Fibonacci input", exc_info=True)
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"code": 400, "message": str(e)}
        )

    except Exception as e:
        logger.error("Unexpected error during FIBONACCI computation", exc_info=True)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "message": f"Internal server error: {e}"}
        )