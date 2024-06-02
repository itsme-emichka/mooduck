from fastapi import HTTPException, status


UnAuthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)

NotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND
)

BadRequest = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST
)

AlreadyExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Already exists'
)
