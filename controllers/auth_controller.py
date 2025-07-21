from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from credentials import ACCESS_TOKEN_EXPIRE_MINUTES
from db import get_session
from schemas.auth_schemas.auth_schema import UserAccounts
from schemas.auth_schemas.token_schema import Token
from schemas.auth_schemas.user_login_schema import UserLogin
from services.utils.passwd_services import hash_password, verify_password, create_access_token

from logger import logger

router = APIRouter()
@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    logger.info(f"Login attempt for: {user.email}")
    db_user = session.exec(select(UserAccounts).where(UserAccounts.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning(f"Login failed for: {user.email} - Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"sub": db_user.email}
    access_token = create_access_token(token_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    logger.info(f"Login successful for: {user.email}")
    return Token(access_token=access_token)