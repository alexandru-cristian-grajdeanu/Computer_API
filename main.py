from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from logger import logger
from fastapi import Request
from schemas.factorial_schema import FactorialRequest
from schemas.fibonacci_schema import FibonacciRequest
from schemas.pow_schema import PowRequest
from schemas.response_schema import OperationResponse
from services.n_factorial_service import compute_factorial
from services.n_fibonacci_service import compute_fibonacci
from services.pow_service import compute_pow

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(rq: Request,
                                       exc: RequestValidationError):
    logger.warning(f"Validation error on {rq.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "message": "Invalid input"},
    )


@app.post("/api/pow", response_model=OperationResponse)
def pow_endpoint(data: PowRequest, request: Request):
    try:
        logger.info(f"{request.method} {request.url.path} - "
                    f"Input: base={data.base}, "
                    f"exponent={data.exponent}")
        result = compute_pow(data.base, data.exponent)
        logger.info(f"POW result: {result}")
        return OperationResponse(operation="pow",
                                 input=data.model_dump(), result=result)
    except Exception as e:
        logger.exception(f"Error during POW: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/fibonacci", response_model=OperationResponse)
def fibonacci_endpoint(data: FibonacciRequest, request: Request):
    try:
        logger.info(f"{request.method} {request.url.path} - Input: n={data.n}")
        result = compute_fibonacci(data.n)
        logger.info(f"FIBONACCI result: {result}")
        return OperationResponse(operation="fibonacci",
                                 input=data.model_dump(), result=result)
    except Exception as e:
        logger.exception(f"Error during FIBONACCI: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/factorial", response_model=OperationResponse)
def factorial_endpoint(data: FactorialRequest, request: Request):
    try:
        logger.info(f"{request.method} {request.url.path} - Input: n={data.n}")
        result = compute_factorial(data.n)
        logger.info(f"FACTORIAL result: {result}")
        return OperationResponse(operation="factorial",
                                 input=data.model_dump(), result=result)
    except Exception as e:
        logger.exception(f"Error during FACTORIAL: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
