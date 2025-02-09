# Python модули
from pyrogram.types import Message, Chat


# Локальные модули
from create_bot import bot
from utilities.logger import logger
from utilities.values import read_values


# Функции
async def new_message_mail_admins(message: Message, keyword, link):
	admins = await read_values('admins')

	text = (
		f'Новая заявка!\n\n'
		f'Текст: {message.text}\n\n'
		f'Ключевое слово: {keyword}\n\n'
		f'<a href="{message.link}">Ссылка на сообщение</a>\n\n'
		f'Чат: <a href="{link}">{message.chat.title}</a>\n\n'
		f'Контакт: @{message.from_user.username}'
	)

	counter = 0
	for admin in admins:
		try:
			await bot.send_message(
				chat_id=admin,
				text=text
			)
			counter += 1
		except Exception as e:
			logger.error(f'USER={admin}, MESSAGE="{e}"')

	logger.info(f'USER=BOT, MESSAGE="send={counter}/{len(admins)}"')


async def chat_enter_mail_admins(chat):
	admins = await read_values('admins')

	text = (
		f'Бот вступил в чат!\n\n'
		f'Чат'
	)

	counter = 0
	for admin in admins:
		try:
			await bot.send_message(
				chat_id=admin,
				text=text
			)
			counter += 1
		except Exception as e:
			logger.error(f'USER={admin}, MESSAGE="{e}"')

	logger.info(f'USER=BOT, MESSAGE="send={counter}/{len(admins)}"')
