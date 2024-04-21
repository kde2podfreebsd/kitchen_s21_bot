from bot.config.bot import bot
from bot.handlers.feedback_handler import feedback_handler, my_feedbacks
from bot.handlers.invoice_handler import my_tx
from bot.handlers.start_handler import main_menu
from bot.handlers.invoice_handler import invoice_menu
from bot.handlers.invoice_handler import payment100, payment200, payment500, payment1000, set_custom_invoice_1, sub_donation_menu
from database.dal.client import ClientDAL
from database.session import async_session


@bot.callback_query_handler(func=lambda call: True)
async def HandlerInlineMiddleware(call):
    if call.data == "feedback":
        await feedback_handler(call.message)

    if call.data == "back_main_menu":
        await main_menu(call.message)

    if "my_feedbacks" in call.data:
        data = call.data.split("#")
        page = int(data[1])
        await my_feedbacks(call.message, page)

    if "my_donations" in call.data:
        await my_tx(call.message, 1)

    if "my_tx" in call.data:
        data = call.data.split("#")
        page = int(data[1])
        await my_tx(call.message, page)

    if "donat_sub_menu" in call.data:
        await sub_donation_menu(call.message)

    if call.data == "my_feed":
        await my_feedbacks(call.message, 1)

    if call.data == "donation_menu":
        await invoice_menu(call.message)

    if "payment100" in call.data:
        await payment100(call.message)

    if "payment200" in call.data:
        await payment200(call.message)

    if "payment500" in call.data:
        await payment500(call.message)

    if "payment1000" in call.data:
        await payment1000(call.message)

    if "payment_n_sum" in call.data:
        await set_custom_invoice_1(call.message)

    if "sub_on_donation_alert" in call.data:
        async with async_session() as session:
            client_dal = ClientDAL(session)
            client_chat_id = call.message.chat.id
            await client_dal.update_donation_status(client_chat_id, donation_status=True)
        await sub_donation_menu(call.message)

    if "unsub_on_donation_alert" in call.data:
        async with async_session() as session:
            client_dal = ClientDAL(session)
            client_chat_id = call.message.chat.id
            await client_dal.update_donation_status(client_chat_id, donation_status=False)
        await sub_donation_menu(call.message)