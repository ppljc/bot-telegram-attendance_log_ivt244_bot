# Python модули
import requests
import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder


# Локальные модули
from config import GROUP
from data_base.operations import students_get


# Функции
async def schedule_get():
	students = await students_get()

	today = datetime.datetime.now()
	date = today.strftime('%Y.%m.%d')

	url = f'https://rasp.omgtu.ru/api/schedule/group/{GROUP}'
	params = {
		'start': date,
		'finish': date,
		'lng': 1
	}

	response = requests.get(url, params=params)
	data = response.json()

	schedule = []
	attendance = []

	texts = []
	builders = []

	number = 0
	for item in data:
		beginLesson = datetime.datetime.combine(
			today.date(),
			datetime.datetime.strptime(item['beginLesson'], '%H:%M').time()
		).strftime('%Y-%m-%d %H:%M:%S')

		endLesson = datetime.datetime.combine(
			today.date(),
			datetime.datetime.strptime(item['endLesson'], '%H:%M').time()
		).strftime('%Y-%m-%d %H:%M:%S')

		schedule.append({
			'discipline': item['discipline'],
			'lecturer_title': item['lecturer_title'],
			'auditorium': item['auditorium'],
			'beginLesson': beginLesson,
			'endLesson': endLesson,
			'subGroup': item['subGroup'],
		})

		result = {}
		for student in students:
			if (student[4] == item['subGroup']) or (item['subGroup'] == '0') or (not item['subGroup']):
				result[student[0]] = 'absent'
			else:
				result[student[0]] = 'subgroup'

		attendance.append(result)

		texts.append(
			f'Номер пары: {number + 1}\n'
			f'Дисциплина: {item["discipline"]}\n'
			f'Преподаватель: {item["lecturer_title"]}\n'
			f'Аудитория: {item["auditorium"]}\n'
			f'Время: {beginLesson} - {endLesson}\n'
			f'Подгруппа: {item["subGroup"]}\n'
		)

		builder = InlineKeyboardBuilder()

		for i in range(len(students)):
			if result[students[i][0]] == 'absent':
				builder.button(text=f'{students[i][1]}', callback_data=f'student_surname|{number}|{students[i][0]}')
				builder.button(text=f'Явка', callback_data=f'student|{number}|{students[i][0]}|present')
				builder.button(text=f'✅ Н/я н/у', callback_data=f'student|{number}|{students[i][0]}|absent')
				builder.button(text=f'Н/я ув.', callback_data=f'student|{number}|{students[i][0]}|valid_reason')

		builder.adjust(4, repeat=True)

		builders.append(builder)

		number += 1

	return schedule, attendance, texts, builders
