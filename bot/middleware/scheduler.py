from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.handlers.invoice_handler import scheduled_payment
from bot.config.bot import bot
from database.dal.client import ClientDAL
from database.session import async_session
from bot.markup import InlineMarkup, TextMarkup


class ScheduledTasks:
    _instance = None

    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler
        self.existing_jobs = {}

    async def process(self):
        await self.send_donation_alerts()

    async def send_donation_alerts(self):
        moscow_tz = timezone(timedelta(hours=3))
        today = datetime.now(moscow_tz).date()

        async with async_session() as session:
            client_dal = ClientDAL(session)
            clients = await client_dal.get_donating_clients()

            for client in clients:
                if client.next_donation_time and client.next_donation_time == today:
                    try:
                        await self.send_donation_alert(client)

                        next_donation_time = datetime.now() + timedelta(days=30)
                        await client_dal.update_next_donation_time(
                            client_chat_id=client.chat_id,
                            next_donation_time=next_donation_time
                        )

                    except Exception as e:
                        pass

    @staticmethod
    async def send_donation_alert(client):
        await scheduled_payment(chat_id=client.chat_id)
        await bot.send_message(
            client.chat_id,
            TextMarkup.sub_alert_text(client=client),
            reply_markup=InlineMarkup.back_to_invoice_menu(),
            parse_mode="html"
        )

    def run(self):
        moscow_tz = timezone(timedelta(hours=3))

        trigger = CronTrigger(hour=12, minute=0, second=0, timezone=moscow_tz)

        job_id = "daily_task"
        self.scheduler.add_job(
            self.process, trigger, id=job_id, misfire_grace_time=30, coalesce=True
        )
        self.scheduler.start()


scheduler = AsyncIOScheduler()
scheduled_tasks = ScheduledTasks(scheduler)
