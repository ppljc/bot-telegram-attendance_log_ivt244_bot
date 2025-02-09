# Python модули
from aiogram import BaseMiddleware
from aiogram.types import *
from typing import *


# Локальные модули
from utilities.values import read_values


# Классы
class StandardMiddleware(BaseMiddleware):
	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: Message | CallbackQuery,
			data: Dict[str, Any]
	) -> Any:
		user = event.from_user

		admins = await read_values('admins')

		if user.id not in admins:
			return

		data['user'] = user

		return await handler(event, data)
