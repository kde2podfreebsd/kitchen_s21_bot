from bot.config.bot import bot
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

from bot.markup import InlineMarkup, TextMarkup
from database.dal.transactions import TransactionDAL
from bot.middleware.context_middleware import message_context_manager
from bot.config import provider_token
from database.session import async_session


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
        reply_markup=InlineMarkup.main_user_menu(),
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
