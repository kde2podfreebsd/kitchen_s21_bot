import asyncio
from typing import Union
from uuid import uuid4

from psycopg2 import IntegrityError
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.admin_groups import AdminGroups
from database.session import DBTransactionStatus, async_session


class AdminGroupsDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def check_existence(
            self, chat_id: int
    ) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ALREADY_EXIST]:
        existing_group = await self.db_session.execute(
            select(AdminGroups).where(and_(AdminGroups.chat_id == chat_id))
        )
        existing_group = existing_group.scalars().first()

        if existing_group:
            return DBTransactionStatus.ALREADY_EXIST
        else:
            return DBTransactionStatus.SUCCESS

    async def create(
            self,
            chat_id: int,
    ) -> Union[
        DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK, DBTransactionStatus.ALREADY_EXIST
    ]:
        if await self.check_existence(chat_id=chat_id) == DBTransactionStatus.ALREADY_EXIST:
            return DBTransactionStatus.ALREADY_EXIST

        new_group = AdminGroups(
            chat_id=chat_id
        )

        self.db_session.add(new_group)

        try:
            await self.db_session.commit()
            return DBTransactionStatus.SUCCESS

        except IntegrityError as e:
            await self.db_session.rollback()
            return DBTransactionStatus.ROLLBACK

    async def delete(
            self,
            chat_id: int,
    ) -> Union[DBTransactionStatus.SUCCESS, DBTransactionStatus.ROLLBACK]:
        existing_group = await self.db_session.execute(
            select(AdminGroups).where(and_(AdminGroups.chat_id == chat_id))
        )
        existing_group = existing_group.scalars().first()

        if existing_group:
            await self.db_session.delete(existing_group)

            try:
                await self.db_session.commit()
                return DBTransactionStatus.SUCCESS
            except IntegrityError as e:
                await self.db_session.rollback()
                return DBTransactionStatus.ROLLBACK
        else:
            return DBTransactionStatus.ROLLBACK

    async def get_all(
            self,
    ) -> Union[list, None]:
        all_groups = await self.db_session.execute(select(AdminGroups).order_by(AdminGroups.id))
        all_groups = all_groups.scalars().all()
        return all_groups


if __name__ == "__main__":
    import asyncio

    async def test():
        async with async_session() as session:
            admin_groups_dal = AdminGroupsDAL(session)

            print(await admin_groups_dal.create(chat_id=-1002119293760))

            print(await admin_groups_dal.get_all())

    asyncio.run(test())