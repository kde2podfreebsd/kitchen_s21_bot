import asyncio
from typing import Union
from datetime import datetime
from psycopg2 import IntegrityError
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models.client import Client
from database.models.transaction import Transaction
from database.session import DBTransactionStatus, async_session


class TransactionDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        client_chat_id: int,
        amount: float,
    ) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK]:
        existing_client = await self.db_session.execute(
            select(Client).where(and_(Client.chat_id == client_chat_id))
        )
        existing_client = existing_client.scalars().first()

        if existing_client:
            new_transaction = Transaction(
                amount=amount,
                client_chat_id=existing_client.chat_id,
                tx_date=datetime.now()
            )

            self.db_session.add(new_transaction)

            try:
                await self.db_session.commit()
                return DBTransactionStatus.SUCCESS
            except IntegrityError as e:
                await self.db_session.rollback()
                return DBTransactionStatus.ROLLBACK
        else:
            return DBTransactionStatus.ROLLBACK

    async def get_tx_by_client_chat_id(
        self,
        client_chat_id: int
    ) -> Union[list, None]:
        existing_client = await self.db_session.execute(
            select(Client).where(and_(Client.chat_id == client_chat_id))
        )
        existing_client = existing_client.scalars().first()

        if existing_client:
            client_transactions = await self.db_session.execute(
                select(Transaction).where(
                    and_(Transaction.client_chat_id == existing_client.chat_id)
                )
            )
            client_transactions = client_transactions.scalars().all()
            return client_transactions
        else:
            return None

    async def get_all_tx(self) -> Union[list, None]:
        all_transactions = await self.db_session.execute(
            select(Transaction).order_by(Transaction.id)
        )
        all_transactions = all_transactions.scalars().all()
        return all_transactions