from datetime import timedelta, datetime
from hashlib import sha256
import base64

from jose import jwt
import bcrypt

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_DAYS,
    MEDIA_URL,
    MEDIA_ROOT,
    BASE_URL
)


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


def save_image_from_base64(base64_data: str) -> str:
    if not base64_data:
        return ''
    format, imgstr = base64_data.split(';base64,')
    ext = format.split('/')[-1]
    img_name = sha256(imgstr.encode()).hexdigest()
    image_url = f'{BASE_URL}/{MEDIA_URL}/{img_name}.{ext}'
    with open(MEDIA_ROOT / f'{img_name}.{ext}', 'wb') as file:
        try:
            file.write(base64.b64decode(imgstr))
        except Exception as ex:
            print(ex)
            return ''
    return image_url
