from telebot import formatting, types


class TextMarkup(object):

    _invoice_text: str = None
    _after_feedback: str = None
    _feedback_text: str = None
    _start_message: str = None

    @classmethod
    def main_user_menu(cls):
        cls._start_message = "Меню текст"
        return cls._start_message

    @classmethod
    def feedback(cls):
        cls._feedback_text = "Напишите ваши пожелания и наш лЮбИмЫй ADM внесет это в список закупок"
        return cls._feedback_text

    @classmethod
    def after_feedback(cls):
        cls._after_feedback = "Спасибо за Ваше пожелание, мы его уже передали ADM!"
        return cls._after_feedback

    @classmethod
    def invoice_text(cls):
        cls._invoice_text = "Инвойс текст"
        return cls._invoice_text


class InlineMarkup(object):

    _hide_menu: types.ReplyKeyboardRemove = None

    @classmethod
    @property
    def hide_reply_markup(cls) -> types.ReplyKeyboardRemove():
        cls._hide_menu: object = types.ReplyKeyboardRemove()
        return cls._hide_menu

    @classmethod
    def main_user_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Донаты", callback_data="donation_menu"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Отчетность", callback_data="donation_menu"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Ваши пожелания", callback_data="feedback"
                    )
                ],
            ],
        )

    @classmethod
    def back_to_main_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Список моих пожеланий", callback_data="my_feed"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Назад в меню", callback_data="back_main_menu"
                    )
                ]
            ],
        )

    @classmethod
    def PaymentBtnList(cls, chat_id: int):
        return types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "Мои донаты", callback_data=f"my_donations"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Подписаться на ежемесячную рассылку о донатах", callback_data=f"donat_sub_menu"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Задонатить 100₽", callback_data=f"payment100#{chat_id}"
                    ),
                    types.InlineKeyboardButton(
                        "Задонатить 200₽", callback_data=f"payment200#{chat_id}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Задонатить 500₽", callback_data=f"payment500#{chat_id}"
                    ),
                    types.InlineKeyboardButton(
                        "Задонатить 1000₽", callback_data=f"payment1000#{chat_id}"
                    )
                ],
                [types.InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")],
            ],
        )