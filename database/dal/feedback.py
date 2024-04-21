import asyncio
from typing import Union
from datetime import datetime
from psycopg2 import IntegrityError
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models.client import Client
from database.models.feedback import Feedback
from database.session import DBTransactionStatus, async_session


class FeedbackDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
            self,
            client_chat_id: int,
            text: str
    ) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK]:
        existing_client = await self.db_session.execute(
            select(Client).where(and_(Client.chat_id == client_chat_id))
        )
        existing_client = existing_client.scalars().first()

        if existing_client:
            new_feedback = Feedback(
                text=text,
                client_id=existing_client.chat_id
            )

            self.db_session.add(new_feedback)

            try:
                await self.db_session.commit()
                return DBTransactionStatus.SUCCESS
            except IntegrityError as e:
                await self.db_session.rollback()
                return DBTransactionStatus.ROLLBACK
        else:
            return DBTransactionStatus.ROLLBACK

    async def get_all(self) -> Union[list, None]:
        all_feedbacks = await self.db_session.execute(select(Feedback).order_by(Feedback.id))
        all_feedbacks = all_feedbacks.scalars().all()
        return all_feedbacks

    async def get_feedbacks_by_client_chat_id(
            self,
            client_chat_id: int
    ) -> Union[list, None]:
        existing_client = await self.db_session.execute(
            select(Client).where(and_(Client.chat_id == client_chat_id))
        )
        existing_client = existing_client.scalars().first()

        if existing_client:
            client_feedbacks = await self.db_session.execute(
                select(Feedback).where(and_(Feedback.client_id == existing_client.chat_id))
            )
            client_feedbacks = client_feedbacks.scalars().all()
            return client_feedbacks
        else:
            return None
