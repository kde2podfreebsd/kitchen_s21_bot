from bot.config.bot import bot
from bot.middleware.context_middleware import message_context_manager
from database.dal.client import ClientDAL
from database.session import DBTransactionStatus, async_session
from bot.markup import TextMarkup, InlineMarkup


async def _start_message(message):
    async with async_session() as session:
        client_dal = ClientDAL(session)
        result = await client_dal.create(
            chat_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
        )
        if result == DBTransactionStatus.ROLLBACK:
            await bot.send_message(
                text="❌ Произошла ошибка при создании клиента в базе данных, обратитесь в клиентскую поддержку"
            )
        else:
            await main_menu(message)


@bot.message_handler(commands=["start"])
async def welcome_handler(message) -> None:
    await _start_message(message)


async def main_menu(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=TextMarkup.main_user_menu(),
        reply_markup=InlineMarkup.main_user_menu(),
        parse_mode="html"
    )
    message_context_manager.add_msgId_to_help_menu_dict(chat_id=message.chat.id, msgId=msg.message_id)

