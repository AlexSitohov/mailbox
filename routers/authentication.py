import json
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import get_session
from hash import verify_password
import models
from sqlalchemy.ext.asyncio import AsyncSession
from JWT import create_access_token

router = APIRouter(tags=['authentication'])


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(login_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user_select = await session.execute(
        select(models.User).where(models.User.email == login_data.username).fetch(1))
    curr = user_select.scalars()
    user_data = [(i.id, i.email, i.password) for i in curr]
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not correct email')
    if not await verify_password(login_data.password, user_data[0][2]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not correct password')
    access_token = create_access_token(data={'user_id': json.dumps(user_data[0][0], cls=UUIDEncoder),
                                             'user_email': user_data[0][1]})

    return {"access_token": access_token, "token_type": "bearer"}
