from fastapi import APIRouter, HTTPException, Request, Depends
from sqlmodel import Session, select
from starlette.responses import JSONResponse

from db import get_session
from schemas.auth_schemas.auth_schema import UserAccounts
from schemas.auth_schemas.user_register_schema import UserRegister
from services.utils.passwd_services import hash_password

from logger import logger

router = APIRouter()

@router.post("/register")
def register_controller(user: UserRegister, session: Session = Depends(get_session)):
    logger.info(f"Attempting to register user: {user.email}")
    statement = select(UserAccounts).where(UserAccounts.email == user.email)
    existing = session.exec(statement).first()
    if existing:
        logger.warning(f"Registration failed: email already registered - {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = UserAccounts(email=user.email, password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    logger.info(f"User registered successfully: {new_user.email} (ID: {new_user.id})")
    return JSONResponse(status_code=200, content={"message": "User registered successfully", "user_id": new_user.id})