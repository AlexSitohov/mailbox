from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, authentication, mails

from database import engine

app = FastAPI(title='mailbox')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(mails.router)

# При запуске программы создаются таблицы в бд. Сейчас для создания и обновления таблиц я использую Alembic.

# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
