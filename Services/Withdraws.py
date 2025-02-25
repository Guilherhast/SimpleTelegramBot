#from Operation import Operation
from Services import Operation

def validator(amount, balance):
	return (amount + balance) >= 0

class withdraw_service(Operation.Operation):
	def __init__(self, database, user_service):
		op_type = "Withdraws"
		#super.__init__(database, user_service, validator, type)
		super().__init__(database, user_service, op_type)

	async def validate(self, user_id, amount):
		balance = await self.user_service.get_balance(user_id)
		return validator(amount, balance)

	async def insert(self, user_id, amount):
		return await super().insert(user_id, -int(amount))
