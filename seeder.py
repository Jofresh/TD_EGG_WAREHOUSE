# docker build -t geoffraygaborit/seed_mongo .
# docker image push geoffraygaborit/seed_mongo

### On peut test en local :
# (conteneur mongodb supprimé, network "mynet" toujours existant)
#   docker run -d --name mongodb --network mynet mongo
#   docker exec -it mongodb mongosh
# Dans un autre terminal :
#   docker run -d --name seed_mongo_c --network mynet geoffraygaborit/seed_mongo

from egg import Egg
from warehouse import Warehouse

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Database information
MONGO_CLIENT = "mongodb:27017"
DB_NAME = "egg_warehouse"
client = MongoClient(MONGO_CLIENT)
db = client[DB_NAME]

WAREHOUSE_COL = "warehouse"
EGG_COL = "egg"

# Warehouse and egg information
CAPACITY = 10
EGG_ORIGIN = "farm"
EGG_COLOR = "yellow"

VALID_EGG = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12301FE")

INVALID_REGISTRATIONS = [
    "12-FR12301FE",
    "05 FR12301FE",
    "05-ZZ12301FE",
    "05-FR12101FE",
    "05-FR12399FE",
    "05-FR12301ZZ",
    "05-FR12302FE",
]

TOO_MANY_EGGS = [VALID_EGG] * (CAPACITY + 5)

# Instanciate classes (Warehouse, Egg)
valid_warehouse = Warehouse(CAPACITY)
valid_warehouse.add_egg(VALID_EGG)

invalid_eggs_warehouse = []
for registration in INVALID_REGISTRATIONS:
    warehouse = Warehouse(CAPACITY)
    egg = Egg(EGG_ORIGIN, EGG_COLOR, registration)
    warehouse.add_egg(egg)

    invalid_eggs_warehouse.append(warehouse)

warehouse_with_too_many_eggs = Warehouse(CAPACITY)
for egg in TOO_MANY_EGGS:
    warehouse_with_too_many_eggs.add_egg(egg)

# Populating the database from created objects
warehouses = [valid_warehouse, warehouse_with_too_many_eggs] + invalid_eggs_warehouse
for warehouse in warehouses:
    print(warehouse)
    inserted_wh = db[WAREHOUSE_COL].insert_one(
        {"_id": ObjectId(), "capacity": warehouse.get_capacity()}
    )

    eggs = warehouse.get_eggs()
    for egg in eggs:
        db[EGG_COL].insert_one(
            {
                "_id": ObjectId(),
                "origin": egg.get_origin(),
                "color": egg.get_color(),
                "registration": egg.get_registration(),
                "warehouse": inserted_wh.inserted_id,
            }
        )
