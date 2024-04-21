from sqlalchemy import select, and_
from telebot import formatting, types

from database.dal.client import ClientDAL
from database.models import Client
from database.session import async_session


class TextMarkup(object):

    _sub_menu_text: str = None
    _error_custom_invoice = None
    _set_custom_invoice: str = None
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

    @classmethod
    def set_custom_invoice(cls):
        cls._set_custom_invoice = "Укажите сумму доната в рублях"
        return cls._set_custom_invoice

    @classmethod
    def error_custom_invoice(cls):
        cls._error_custom_invoice = "Вы указали не верную сумму для пополнения, попробуйте еще раз"
        return cls._error_custom_invoice

    @classmethod
    def sub_menu_text(cls):
        cls._sub_menu_text = "Хотите ли вы получать ежемесячное напоминание о донатах?"
        return cls._sub_menu_text


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
    def back_to_invoice_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Назад в меню", callback_data="donation_menu"
                    )
                ]
            ],
        )

    @classmethod
    def feed_menu(cls):
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
    async def sub_on_donation_alert(cls, chat_id: int):
        async with async_session() as session:
            existing_user = await session.execute(
                select(Client).where(and_(Client.chat_id == chat_id))
            )
            existing_user = existing_user.scalars().first()

            if existing_user.donation_status:
                return types.InlineKeyboardMarkup(
                    row_width=1,
                    keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="Отписаться от рассылки", callback_data="unsub_on_donation_alert"
                            )
                        ],
                        [
                            types.InlineKeyboardButton(
                                text="Назад в меню", callback_data="donation_menu"
                            )
                        ]
                    ],
                )

            else:

                return types.InlineKeyboardMarkup(
                    row_width=1,
                    keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="Подписаться на рассылку", callback_data="sub_on_donation_alert"
                            )
                        ],
                        [
                            types.InlineKeyboardButton(
                                text="Назад в меню", callback_data="donation_menu"
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
                        "Мои донаты", callback_data="my_donations"
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
                [
                    types.InlineKeyboardButton(
                        "Выбрать свою сумму", callback_data=f"payment_n_sum#{chat_id}"
                    )
                ],
                [types.InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")],
            ],
        )