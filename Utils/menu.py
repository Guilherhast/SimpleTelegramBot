from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

async def send(message: Message):
		msg = "Which operation do you want to make?"
		buttons = [
					[KeyboardButton(text="Balance")],
					[KeyboardButton(text="Withdraw")],
					[KeyboardButton(text="Deposit")],
				]
		keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
		await message.answer(msg, reply_markup=keyboard)
