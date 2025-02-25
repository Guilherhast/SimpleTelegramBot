import asyncio
import logging
import sys
from os import getenv

# aiogram imports
from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import  CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# Local imports
import config
from Utils import FSM, database, menu

OperationFSM = FSM.OperationFSM

# Service imports
from Services import User, Deposits, Withdraws

# Configuration

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

main_router = Router()

## Creating database
db = database.Database(config.db_host, config.db_port, config.db_database, config.db_collection_list)

## Creating services
user_service = User.user_service(db)
withdraw_service = Withdraws.withdraw_service(db, user_service)
deposit_service = Deposits.deposits_service(db, user_service)

simple_operations = {
		"balance": user_service.get_balance,
	}

complex_operations = {
		"withdraw": withdraw_service.insert,
		"deposit": deposit_service.insert
	}

## Functions
async def send_balance(message: Message):
	balance = await simple_operations[message.text.lower()](message.from_user.id)
	await message.answer(f"Your balance is: {balance}")


## Start
@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
	await state.set_state(OperationFSM.type)
	await user_service.start(message.from_user)
	await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
	await menu.send(message)

### Set operation
@main_router.message(OperationFSM.type)
async def choose_operation(message: Message, state: FSMContext):
	if message.text.lower() in simple_operations:
		await send_balance(message)
		await state.clear()
	elif message.text.lower() in complex_operations:
		await state.update_data(type=message.text)
		await state.set_state(OperationFSM.amount)
		await message.reply(f"Enter the amount to {message.text.lower()}")
	else:
		await menu.send(message)

### Set amount
@main_router.message(OperationFSM.amount)
async def choose_amount(message: Message, state: FSMContext):
	await state.update_data(amount=message.text)
	data = await state.get_data()
	await state.clear()
	await complex_operations[data["type"].lower()](message.from_user.id, data["amount"])
	await message.reply(f"Operation: {data['type']}\nAmount: {data['amount']}")

### Any message
@main_router.message()
async def echo_handler(message: Message, state: FSMContext) -> None:
	await state.set_state(OperationFSM.type)
	await menu.send(message)

## Running
async def main() -> None:
	# Initialize Bot instance with default bot properties which will be passed to all API calls
	bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

	# And the run events dispatching
	await dp.start_polling(bot)


if __name__ == "__main__":
	dp = Dispatcher()
	dp.include_router(main_router)
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())
