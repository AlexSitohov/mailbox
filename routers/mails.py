from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
from database import get_session
from hash import hash_password
from JWT import get_current_user

from schemas import MailCreate, MailResponse

router = APIRouter(tags=['mail'])


@router.post("/mails", status_code=status.HTTP_201_CREATED, response_model=MailResponse)
async def create_mail(mail_data: MailCreate, session: AsyncSession = Depends(get_session),
                      current_user=Depends(get_current_user)):
    current_user_email = current_user.get('user_email')
    try:
        new_mail = models.Mail(**mail_data.dict(), from_email=current_user_email)
        session.add(new_mail)
        await session.commit()
        await session.refresh(new_mail)
        return new_mail
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого email адреса не существует')


@router.get("/mails", status_code=status.HTTP_200_OK, response_model=list[MailResponse])
async def get_list_of_my_mails(session: AsyncSession = Depends(get_session), limit: int = Query(default=50),
                               current_user=Depends(get_current_user)):
    current_user_email = current_user.get('user_email')
    list_of_my_mails = await session.execute(
        select(models.Mail).where(models.Mail.from_email == current_user_email).order_by(models.Mail.id.asc()).limit(
            limit))
    return list_of_my_mails.scalars().all()
