from motor.motor_asyncio import AsyncIOMotorClient
import config

# Class to store a database client
class Database():
	def __init__(self, host, port, database, collection_list):
		self.client = AsyncIOMotorClient(f"mongodb://{host}:{port}")
		self.database_name = database
		self.collection_list = collection_list

## Collections
	async def collections_create(self, name, db):
		await db.create_collection(name)

## Initialize
## Certify that all collections are created
	async def initialize(self):
		# Initialize the MongoDB client
		db = self.client[self.database_name]

		# Get collections already created
		existing_collections = await db.list_collection_names()

		# In the required collections create the ones wich are not created
		for collection_name in self.collection_list:
			if not collection_name in existing_collections:
				await self.collections_create(collection_name, db)

	def get_db(self):
		return self.client[self.database_name]

# To run the function in an async context
if __name__ == "__main__":
	import asyncio
	motor_db = Database(config.db_host, config.db_port, config.db_database, config.db_collection_list)
	asyncio.run(motor_db.initialize())
