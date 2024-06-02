from fastapi import HTTPException, status


ItemError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Empty request or these items already on moodboard'
)
