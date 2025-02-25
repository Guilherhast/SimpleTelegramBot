import datetime

acceptable_types = ["Deposits", "Withdraws"]

class Operation():

	def __init__(self, database, user_service, op_type) -> None:
		if not op_type in acceptable_types: raise Exception("Inacceptable type: " + op_type)

		self.collection = database.get_db()[op_type]
		self.user_service = user_service

	async def insert(self, user_id, amount):
		try:
			trimmed_amount = int(amount)
			validated = await self.validate(user_id, amount)
			if not validated:
				return False
			# Update user balance
			update = await self.user_service.change_balance(user_id, trimmed_amount)
			# Add operation record
			return await self.__insert(user_id, trimmed_amount)
		except Exception as error:
			raise error

	async def __insert(self, user_id, amount):
			document = {"amount": amount, "user": user_id, "stamp": datetime.datetime.now()}
			self.collection.insert_one(document)

	async def validate(self, user_id, amount):
		return True
