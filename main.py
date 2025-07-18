from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from db import engine

from controllers import factorial_controller, pow_controller, fibonacci_controller
from logger import logger
from fastapi import Request

app = FastAPI()
app.include_router(fibonacci_controller.router, prefix="/api")
app.include_router(factorial_controller.router, prefix="/api")
app.include_router(pow_controller.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(rq: Request,
                                       exc: RequestValidationError):
    logger.error(f"Validation error on {rq.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "message": "Invalid input"},
    )
