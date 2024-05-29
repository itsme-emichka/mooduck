from fastapi import HTTPException, status


NotAuthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='У вас недостаточно прав'
)
