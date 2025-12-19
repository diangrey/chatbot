from pymongo import MongoClient

import config

RADHEdb = MongoClient(config.MONGO_URL)
RADHE = RADHEdb["RADHEDb"]["RADHE"]


from .chats import *
from .users import *
