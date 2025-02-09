# Python модули
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Локальные модули
from create_bot import bot
from utilities.values import read_values
from utilities.logger import logger
from utilities.schedule_api import schedule_get
from data_base.operations import day_add, day_get


# Переменные
scheduler = AsyncIOScheduler()


# Функции
async def schedule_remove(admin, message_id):
	try:
		await bot.delete_message(chat_id=admin, message_id=message_id)
		logger.debug(f'USER={admin}, MESSAGE="schedule removed"')
	except Exception as e:
		logger.error(f'USER={admin}, MESSAGE="{e}"')


async def schedule_send(text, builder, endLesson):
	admins = await read_values('admins')

	for admin in admins:
		message = await bot.send_message(
			chat_id=admin,
			text=text,
			reply_markup=builder.as_markup()
		)
		scheduler.add_job(
			func=schedule_remove,
			args=[admin, message.message_id],
			trigger='date',
			run_date=endLesson + datetime.timedelta(minutes=10)
		)


async def today_attendance_result():
	text = await day_get()

	admins = await read_values('admins')

	for admin in admins:
		await bot.send_message(
			chat_id=admin,
			text=text,
		)


async def today_schedule_get():
	schedule, attendance, texts, builders = await schedule_get()

	await day_add(
		schedule=schedule,
		attendance=attendance
	)

	endLesson = None

	for i in range(len(schedule)):
		endLesson = datetime.datetime.strptime(schedule[i]['endLesson'], '%Y-%m-%d %H:%M:%S')
		beginLesson = datetime.datetime.strptime(schedule[i]['beginLesson'], '%Y-%m-%d %H:%M:%S')
		scheduler.add_job(
			func=schedule_send,
			args=[texts[i], builders[i], endLesson],
			trigger='date',
			run_date=beginLesson
		)

	if endLesson:
		scheduler.add_job(
			func=today_attendance_result,
			trigger='date',
			run_date=endLesson + datetime.timedelta(minutes=15)
		)


async def schedule_get_job():
	scheduler.add_job(
		func=today_schedule_get,
		trigger='cron',
		hour=7,
		minute=0
	)
	scheduler.start()
