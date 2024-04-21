from bot.config.bot import bot


@bot.message_handler(commands=['get_chat_info'])
async def get_chat_info(message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_title = message.chat.title
    await bot.send_message(message.chat.id, f'ID чата: {chat_id}\nТип чата: {chat_type}\nНазвание чата: {chat_title}')