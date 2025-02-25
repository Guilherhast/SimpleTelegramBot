import datetime

class user_service():
	def __init__(self, database) -> None:
		self.collection = database.get_db().Users

	async def start(self, user):
		if user.is_bot: return False

		date = datetime.datetime.now()

		user_document = await self.__get_user(user.id)

		if user_document:
			return await self.__update(user, date)
		else:
			return await self.__insert(user, date)

	async def __get_user(self, id):
		return await self.collection.find_one({"telegram_id": id})

	async def __insert(self, user, date):
		user_data = {
					"telegram_id": user.id,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"username": user.username,
					"last_login": date,
					"last_operation": date,
					"balance": 0
				}
		return self.collection.insert_one(user_data)

	async def __update(self, user, date):
		return self.collection.update_one(
					{"telegram_id": user.id},
					{"$set": {"last_login": date}}
				)

	async def get_balance(self, id):
		user = await self.collection.find_one({"telegram_id": id})
		return user["balance"]

	async def change_balance(self, id, amount):
		return await self.collection.update_one(
					{"telegram_id": id},
					{
						"$inc": {"balance": amount},
						"$set": {"last_operation": datetime.datetime.now()}
					}
				)

