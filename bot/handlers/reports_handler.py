from bot.config.bot import bot
from bot.markup import InlineMarkup, TextMarkup
from bot.middleware.context_middleware import message_context_manager
from database.session import async_session
from database.dal.transactions import TransactionDAL
from gCreds import basedir


async def send_report(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    async with async_session() as session:
        tx_dal = TransactionDAL(session)

        total_amount = await tx_dal.total_recharge_amount()
        last_month_amount = await tx_dal.total_recharge_amount_last_month()

        msg = await bot.send_photo(
            chat_id=message.chat.id,
            photo=open(fr"{basedir}/static/report_sort.jpg", "rb"),
            caption=TextMarkup.report_text(total_amount=total_amount, last_month_amount=last_month_amount),
            reply_markup=InlineMarkup.report_btn(),
            parse_mode="html"
        )

    message_context_manager.add_msgId_to_help_menu_dict(chat_id=message.chat.id, msgId=msg.message_id)