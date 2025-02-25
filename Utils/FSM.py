from aiogram.fsm.state  import State, StatesGroup

class OperationFSM(StatesGroup):
	type = State()
	amount = State()



