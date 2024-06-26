import asyncio
import os
from bot.config.bot import bot
from bot.filters import FloodingMiddleware
from telebot.asyncio_filters import (
    ForwardFilter,
    IsDigitFilter,
    IsReplyFilter,
    StateFilter,
)

from bot.handlers.start_handler import welcome_handler, _start_message, main_menu
from bot.handlers.inline_handler import HandlerInlineMiddleware
from bot.handlers.chat_info_handler import get_chat_info
from bot.middleware.scheduler import scheduled_tasks
from database.dal.admin_groups import AdminGroupsDAL
from database.session import create_all, async_session


async def add_admin_chat():
    async with async_session() as session:
        admin_groups_dal = AdminGroupsDAL(session)
        await admin_groups_dal.create(chat_id=-1002119293760)


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())

        bot.setup_middleware(FloodingMiddleware(1))
        self.scheduled_tasks = scheduled_tasks

        self.provider_token: str = os.getenv("TELEGRAM_PAYMENT_BOT_TOKEN")

    async def polling(self):
        await create_all()
        await add_admin_chat()
        task1 = asyncio.create_task(bot.infinity_polling())
        self.scheduled_tasks.run()
        await task1


b = Bot()


asyncio.run(b.polling())