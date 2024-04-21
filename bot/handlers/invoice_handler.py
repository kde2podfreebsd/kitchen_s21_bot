import os
from math import ceil

from dotenv import load_dotenv
from telebot import types

from bot.config.bot import bot
from telebot.types import LabeledPrice
from telebot.types import ShippingOption
from telebot.asyncio_handler_backends import State, StatesGroup

from bot.markup import InlineMarkup, TextMarkup
from database.dal.transactions import TransactionDAL
from bot.middleware.context_middleware import message_context_manager
from bot.config import provider_token
from database.session import async_session, DBTransactionStatus


class Prices:

    prices100 = [
        LabeledPrice(label="Задонатить 100₽", amount=100 * 100)
    ]

    prices200 = [
        LabeledPrice(label="Задонатить 200₽", amount=200 * 100)
    ]

    prices500 = [
        LabeledPrice(label="Задонатить 500₽", amount=500 * 100)
    ]

    prices1000 = [
        LabeledPrice(label="Задонатить 1000₽", amount=1000 * 100)
    ]


async def invoice_menu(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    msg = await bot.send_message(
        message.chat.id,
        text=TextMarkup.invoice_text(),
        parse_mode="html",
        reply_markup=InlineMarkup.PaymentBtnList(chat_id=message.chat.id)
    )

    message_context_manager.add_msgId_to_help_menu_dict(chat_id=message.chat.id, msgId=msg.message_id)


async def payment100(message):

    msg = await bot.send_invoice(
        message.chat.id,  # chat_id
        "Задонатить 100₽",  # title
        "Задонатить 100₽",  # description
        "Задонатить 100₽",  # invoice_payload
        provider_token,
        "RUB",
        Prices.prices100,
        photo_url='https://www.meme-arsenal.com/memes/b96241565f04a5a8506a74c7558615ee.jpg'
    )
    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


async def payment200(message):

    msg = await bot.send_invoice(
        message.chat.id,  # chat_id
        "Задонатить 200₽",  # title
        "Задонатить 200₽",  # description
        "Задонатить 200₽",  # invoice_payload
        provider_token,
        "RUB",
        Prices.prices200,
        photo_url='https://www.meme-arsenal.com/memes/b96241565f04a5a8506a74c7558615ee.jpg'
    )
    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


async def payment500(message):

    msg = await bot.send_invoice(
        message.chat.id,  # chat_id
        "Задонатить 500₽",  # title
        "Задонатить 500₽",  # description
        "Задонатить 500₽",  # invoice_payload
        provider_token,
        "RUB",
        Prices.prices500,
        photo_url='https://www.meme-arsenal.com/memes/b96241565f04a5a8506a74c7558615ee.jpg'
    )
    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


async def payment1000(message):

    msg = await bot.send_invoice(
        message.chat.id,  # chat_id
        "Задонатить 1000₽",  # title
        "Задонатить 1000₽",  # description
        "Задонатить 1000₽",  # invoice_payload
        provider_token,
        "RUB",
        Prices.prices1000,
        photo_url='https://www.meme-arsenal.com/memes/b96241565f04a5a8506a74c7558615ee.jpg'
    )
    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


class PaymentState(StatesGroup):
    set_payment = State()
    error_payment = State()


async def set_custom_invoice_1(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=TextMarkup.set_custom_invoice(),
        reply_markup=InlineMarkup.back_to_invoice_menu(),
        parse_mode="html"
    )

    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )

    await bot.set_state(message.chat.id, PaymentState.set_payment)


@bot.message_handler(state=PaymentState.set_payment)
async def set_custom_invoice_2(message):
    if not message.text.isdigit() or int(message.text) < 1:
        await bot.send_message(
            chat_id=message.chat.id,
            text=TextMarkup.error_custom_invoice(),
            reply_markup=InlineMarkup.hide_reply_markup,
            parse_mode="html"
        )
        await set_custom_invoice_1(message)
    else:
        await payment_custom_price(message, price=int(message.text))


async def payment_custom_price(message, price: int):

    msg = await bot.send_invoice(
        message.chat.id,  # chat_id
        f"Задонатить {price}₽",  # title
        f"Задонатить {price}₽",  # description
        f"Задонатить {price}₽",  # invoice_payload
        provider_token,
        "RUB",
        [
            LabeledPrice(label=f"Задонатить {price}₽", amount=price * 100)
        ],
        photo_url='https://www.meme-arsenal.com/memes/b96241565f04a5a8506a74c7558615ee.jpg'
    )
    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


async def db_communication_erorr(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(message.chat.id)
    msg = await bot.send_message(
        message.chat.id,
        f"<b>❌ Произошла ошибка при обращении к базе данных, попробуйте еще раз через некоторое время или обратитесь в тех поддержку</b> ",
        reply_markup=InlineMarkup.main_user_menu(),
        parse_mode='html'
    )
    message_context_manager.add_msgId_to_help_menu_dict(message.chat.id, msg.id)


async def successful_tx(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(message.chat.id)
    msg = await bot.send_message(
        message.chat.id,
        f"<b>✅ Ваша оплата успешно прошла!</b> Спасибо за пополнение баланса на сумму {(message.successful_payment.total_amount / 100)} {message.successful_payment.currency}.",
        reply_markup=InlineMarkup.PaymentBtnList(chat_id=message.chat.id),
        parse_mode='html'
    )
    message_context_manager.add_msgId_to_help_menu_dict(message.chat.id, msg.id)


@bot.shipping_query_handler(func=lambda query: True)
async def shipping(shipping_query):
    print(shipping_query)
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        # shipping_options=Prices.shipping_options,
        error_message="Ошибка, попробуйте позже или напишите в тех поддержку",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Что-то случилось на стороне эквайринга, попробуйте позже или напишите в тех поддержку",
    )


@bot.message_handler(content_types=["successful_payment"])
async def got_payment(message):
    async with async_session() as session:
        tx_dal = TransactionDAL(session)
        await tx_dal.create(
            client_chat_id=message.chat.id,
            amount=message.successful_payment.total_amount / 100
        )
    await successful_tx(message)


async def sub_donation_menu(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=TextMarkup.sub_menu_text(),
        reply_markup=await InlineMarkup.sub_on_donation_alert(chat_id=message.chat.id),
        parse_mode="html"
    )

    message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id,
        msgId=msg.id
    )


load_dotenv()
TRANSACTION_STRINGS_PER_PAGE = int(os.getenv("TRANSACTION_STRINGS_PER_PAGE"))


async def my_tx(message, page):
    await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
    async with async_session() as session:
        tx_dal = TransactionDAL(session)
        txs = await tx_dal.get_tx_by_client_chat_id(client_chat_id=message.chat.id)

        if txs == DBTransactionStatus.NOT_EXIST:
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text="У вас пока нет транзакций.",
                reply_markup=types.InlineKeyboardMarkup(
                    row_width=1,
                    keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="🔙 Назад",
                                callback_data="donation_menu"
                            )
                        ]
                    ]
                )
            )
        else:
            amount_of_pages = ceil(len(txs) / TRANSACTION_STRINGS_PER_PAGE)

            chunks = []
            i = 0
            while i < len(txs):
                chunks.append(txs[i:i + TRANSACTION_STRINGS_PER_PAGE])
                i += TRANSACTION_STRINGS_PER_PAGE

            data_to_display = chunks[page - 1]

            msg_text = ""
            number = 1 + (page - 1) * TRANSACTION_STRINGS_PER_PAGE
            for data in data_to_display:
                msg_text += f"{number}. Сумма: {data.amount} | Дата и время: {data.tx_date.strftime('%d-%m-%Y %H:%M:%S')}\n"
                number += 1

            mp = types.InlineKeyboardMarkup(row_width=3)
            if amount_of_pages != 1:
                back = types.InlineKeyboardButton(
                    text="<", callback_data=f"my_tx#{page - 1 if page - 1 >= 1 else page}"
                )
                page_cntr = types.InlineKeyboardButton(
                    text=f"{page}/{amount_of_pages}", callback_data="nullified"
                )
                forward = types.InlineKeyboardButton(
                    text=">",
                    callback_data=f"my_tx#{page + 1 if page + 1 <= amount_of_pages else page}",
                )
                mp.add(back, page_cntr, forward)

            back_to_profile_menu = types.InlineKeyboardButton(
                text="🔙 Назад", callback_data="donation_menu"
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

