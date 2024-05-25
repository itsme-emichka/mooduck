from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from db.db import TORTOISE_ORM
from users.routers import router as users_router
from moodboards.routers import router as moodboards_router


app = FastAPI()

app.include_router(users_router)
app.include_router(moodboards_router)


register_tortoise(
    app,
    TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
