# Python модули
import datetime
import json


# Локальные модули
from create_bot import db


# Функции
async def students_get():
	students = await db.select(
		table='students',
	)

	return students


async def students_format():
	students = await students_get()

	result = {}
	for student in students:
		result[student[0]] = student[1]

	return result


async def day_add(schedule, attendance):
	date = datetime.datetime.now().strftime('%Y-%m-%d')

	await db.insert(
		table='log',
		what={'date': date, 'schedule': json.dumps(schedule), 'attendance': json.dumps(attendance)},
	)


async def day_edit(number, username, attend):
	date = datetime.datetime.now().strftime('%Y-%m-%d')

	attendance = await db.select(
		table='log',
		what=('attendance',),
		where={'date': date}
	)
	attendance = json.loads(attendance[0][0])

	attendance[number][username] = attend

	attendance = json.dumps(attendance)

	await db.update(
		table='log',
		what={'attendance': attendance},
		where={'date': date}
	)


async def day_get():
	date = datetime.datetime.now().strftime('%Y-%m-%d')

	log = await db.select(
		table='log',
		where={'date': date}
	)
	schedule = json.loads(log[0][1])
	attendance = json.loads(log[0][2])

	students = await students_format()

	max_surname_length = max(len(value) for _, value in students.items())

	attend_types = {
		'present': 'Явка',
		'absent': 'Н/я н/у',
		'valid_reason': 'Н/я ув.',
		'subgroup': 'Др/подгр.'
	}

	text = ''

	for i in range(len(schedule)):
		text += f'<b>{i + 1}) {schedule[i]["discipline"]}:</b>\n<code>'

		for key, value in attendance[i].items():
			text += f'• {students[key].ljust(max_surname_length)} — {attend_types[value]}\n'

		text += '</code>\n'

	return text
