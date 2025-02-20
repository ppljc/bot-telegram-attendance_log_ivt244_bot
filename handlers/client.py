# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import Command

# Локальные модули
from utilities.logger import logger
from data_base.operations import day_edit, day_get


# Переменные
router = Router(name='client')


# Функции
@router.message(Command(commands=['today_result'], ignore_case=True))
async def message_day_result(message: Message):
	try:
		text = await day_get()

		await message.answer(text=text)

		await message.delete()

		logger.info(f'USER={message.from_user.id}, MESSAGE=""')
	except Exception as e:
		logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.callback_query(F.data == 'student_surname')
async def callback_student_surname(query: CallbackQuery):
	try:
		number = int(query.data.split('|')[1])
		username = query.data.split('|')[2]

		await query.answer(text=f'Номер пары: {number + 1}, юзернейм: {username}.')
	except Exception as e:
		logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')


@router.callback_query(F.data.startswith('student'))
async def callback_student(query: CallbackQuery):
	try:
		number = int(query.data.split('|')[1])
		username = query.data.split('|')[2]
		attend = query.data.split('|')[3]

		inline_keyboard = query.message.reply_markup.inline_keyboard

		for button in inline_keyboard:
			if button[0].callback_data.split('|')[2] == username:
				if attend == 'present':
					button[1].text = f'✅ Явка'
					button[2].text = f'Н/я н/у'
					# button[3].text = f'Н/я ув.'
				elif attend == 'absent':
					button[1].text = f'Явка'
					button[2].text = f'✅ Н/я н/у'
					# button[3].text = f'Н/я ув.'
				elif attend == 'valid_reason':
					button[1].text = f'Явка'
					button[2].text = f'Н/я н/у'
					# button[3].text = f'✅ Н/я ув.'

		try:
			await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))

			await day_edit(
				number=number,
				username=username,
				attend=attend
			)

			await query.answer(text='Отметил, брат.')
		except:
			await query.answer(text='Уже отмечен, брат.')
			logger.error(f'USER={query.from_user.id}, MESSAGE="Attendance not changed."')

		logger.info(f'USER={query.from_user.id}, MESSAGE=""')
	except Exception as e:
		logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')
