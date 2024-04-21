from bot.config.bot import bot
from bot.handlers.feedback_handler import feedback_handler, my_feedbacks
from bot.handlers.start_handler import main_menu
from bot.handlers.invoice_handler import invoice_menu
from bot.handlers.invoice_handler import payment100, payment200, payment500, payment1000


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