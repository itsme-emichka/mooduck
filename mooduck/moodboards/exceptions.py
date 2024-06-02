from fastapi import HTTPException, status


AlreadyInFavorite = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Already in favorite'
)

CantDeleteChaotic = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Cant delete Chaotic'
)
