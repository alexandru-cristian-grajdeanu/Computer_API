import jwt  # ✅ This is PyJWT, not python-jose
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from credentials import SECRET_KEY, ALGORITHM

# === JWT CONFIG ===

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === PASSWORD HASHING ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# === JWT TOKEN CREATION ===
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
