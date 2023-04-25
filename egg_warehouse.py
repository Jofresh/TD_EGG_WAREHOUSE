import pymongo
from pymongo import MongoClient

from warehouse import Warehouse
from egg import Egg

# Database information
MONGO_CLIENT = "mongodb:27017"
DB_NAME = "egg_warehouse"

client = MongoClient(MONGO_CLIENT)
db = client[DB_NAME]

EGG_COL = "egg"

# Querying database
eggs = db[EGG_COL].find()
for egg in eggs:
    origin = egg["origin"]
    color = egg["color"]
    registration = egg["registration"]

    # Instantiate egg to check if its registration is valid
    e = Egg(origin, color, registration)
    if not e.is_valid():
        print(f"L'oeuf qui a pour immatriculation {e.get_registration()} est invalide.")
