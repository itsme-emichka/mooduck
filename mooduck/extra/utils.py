from datetime import timedelta, datetime

from jose import jwt
import bcrypt

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
