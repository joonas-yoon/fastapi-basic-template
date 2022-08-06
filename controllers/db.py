from configs import Configs
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(Configs.DB_URL)
database = client[Configs.DB_DATABASE]

def get_collection(name: str) -> AsyncIOMotorClient:
  """
  Get collection, create if not exists.

  Args:
      name (str): determines name of collection

  Returns:
      AsyncIOMotorClient: client connected collection
  """
  return database[name]
