from fastapi import HTTPException, status


WrongLoginOrPassword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Wrong login or password'
)
