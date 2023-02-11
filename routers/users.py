from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
from database import get_session
from hash import hash_password

from schemas import UserCreate, UserResponse

router = APIRouter(tags=['users'])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_data.password = await hash_password(user_data.password)
    new_user = models.User(**user_data.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users_list(session: AsyncSession = Depends(get_session), limit: int = Query(default=50)):
    users_list = await session.execute(
        select(models.User).order_by(models.User.email.asc()).limit(limit))
    return users_list.scalars().all()
