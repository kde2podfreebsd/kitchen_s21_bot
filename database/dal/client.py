import asyncio
from typing import Union
from uuid import uuid4

from psycopg2 import IntegrityError
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.client import Client
from database.session import DBTransactionStatus, async_session


class ClientDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def check_existence(
            self, chat_id: int
    ) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ALREADY_EXIST]:
        existing_user = await self.db_session.execute(
            select(Client).where(and_(Client.chat_id == chat_id))
        )
        existing_user = existing_user.scalars().first()

        if existing_user:
            return DBTransactionStatus.ALREADY_EXIST
        else:
            return DBTransactionStatus.SUCCESS

    async def create(
            self,
            chat_id: int,
            username: str,
            first_name: str,
            last_name: str
    ) -> Union[
        DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK, DBTransactionStatus.ALREADY_EXIST
    ]:
        if await self.check_existence(chat_id=chat_id) == DBTransactionStatus.ALREADY_EXIST:
            return DBTransactionStatus.ALREADY_EXIST

        new_user = Client(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        self.db_session.add(new_user)

        try:
            await self.db_session.commit()
            return DBTransactionStatus.SUCCESS

        except IntegrityError as e:
            await self.db_session.rollback()
            return DBTransactionStatus.ROLLBACK

    async def update_donation_status(self, client_chat_id: int, donation_status: bool) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK]:
        existing_client = await self.db_session.execute(
            select(Client).where(Client.chat_id == client_chat_id)
        )
        existing_client = existing_client.scalars().first()

        if existing_client:
            existing_client.donation_status = donation_status
            try:
                await self.db_session.commit()
                return DBTransactionStatus.SUCCESS
            except IntegrityError as e:
                await self.db_session.rollback()
                return DBTransactionStatus.ROLLBACK
        else:
            return DBTransactionStatus.ROLLBACK