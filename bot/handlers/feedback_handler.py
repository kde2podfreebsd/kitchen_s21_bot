import datetime
import os
from math import ceil

from dotenv import load_dotenv
from telebot import types

from bot.config.bot import bot
from bot.middleware.context_middleware import message_context_manager
from bot.markup import InlineMarkup, TextMarkup
from telebot.asyncio_handler_backends import State, StatesGroup

from database.dal.admin_groups import AdminGroupsDAL
from database.dal.feedback import FeedbackDAL
from database.session import async_session, DBTransactionStatus


class FeedBackStates(StatesGroup):
    get_feedback = State()


async def feedback_handler(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)

    msg = await bot.send_message(
        message.chat.id,
        text=TextMarkup.feedback(),
        reply_markup=InlineMarkup.feed_menu(),
        parse_mode="html",
    )

    message_context_manager.add_msgId_to_help_menu_dict(chat_id=message.chat.id, msgId=msg.message_id)

    await bot.set_state(message.chat.id, FeedBackStates.get_feedback)


@bot.message_handler(state=FeedBackStates.get_feedback)
async def get_feedback(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    async with async_session() as session:
        admin_groups_dal = AdminGroupsDAL(session)

        adm_groups = await admin_groups_dal.get_all()
        current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        feedback_text = f"User: @{message.chat.username if message.chat.username is not None else message.chat.id}\nFeedback: {message.text}\n\ndate: {current_time}"

        try:
            for adm_group in adm_groups:
                await bot.send_message(
                    chat_id=adm_group.chat_id,
                    text=feedback_text,
                    parse_mode="html"
                )

        except Exception as e:
            print(e)
            pass

    async with async_session() as session:
        feedback_dal = FeedbackDAL(session)
        await feedback_dal.create(
            client_chat_id=message.chat.id,
            text=message.text
        )

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=TextMarkup.after_feedback(),
        reply_markup=InlineMarkup.main_user_menu(),
        parse_mode="html"
    )

    message_context_manager.add_msgId_to_help_menu_dict(chat_id=message.chat.id, msgId=msg.message_id)

load_dotenv()
FEEDBACK_STRINGS_PER_PAGE = int(os.getenv("FEEDBACK_STRINGS_PER_PAGE"))


async def my_feedbacks(message, page):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    async with async_session() as session:
        feedback_dal = FeedbackDAL(session)
        feeds = await feedback_dal.get_feedbacks_by_client_chat_id(client_chat_id=message.chat.id)

        if feeds == DBTransactionStatus.NOT_EXIST:
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text="У вас пока нет отзывов.",
                reply_markup=types.InlineKeyboardMarkup(
                    row_width=1,
                    keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="🔙 Назад",
                                callback_data="feedback"
                            )
                        ]
                    ]
                )
            )
        else:
            amount_of_pages = ceil(len(feeds) / FEEDBACK_STRINGS_PER_PAGE)

            chunks = []
            i = 0
            while i < len(feeds):
                chunks.append(feeds[i:i + FEEDBACK_STRINGS_PER_PAGE])
                i += FEEDBACK_STRINGS_PER_PAGE

            data_to_display = chunks[page - 1]

            msg_text = ""
            number = 1 + (page - 1) * FEEDBACK_STRINGS_PER_PAGE
            for data in data_to_display:
                msg_text += f"{number}. {data.text} | Datetime: {data.time.strftime('%d-%m-%Y %H:%M:%S')}\n"
                number += 1

            mp = types.InlineKeyboardMarkup(row_width=3)
            if amount_of_pages != 1:
                back = types.InlineKeyboardButton(
                    text="<", callback_data=f"my_feedbacks#{page - 1 if page - 1 >= 1 else page}"
                )
                page_cntr = types.InlineKeyboardButton(
                    text=f"{page}/{amount_of_pages}", callback_data="nullified"
                )
                forward = types.InlineKeyboardButton(
                    text=">",
                    callback_data=f"my_feedbacks#{page + 1 if page + 1 <= amount_of_pages else page}",
                )
                mp.add(back, page_cntr, forward)

            back_to_profile_menu = types.InlineKeyboardButton(
                text="🔙 Назад", callback_data="feedback"
            )
            mp.add(back_to_profile_menu)

            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=msg_text,
                reply_markup=mp
            )

    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )