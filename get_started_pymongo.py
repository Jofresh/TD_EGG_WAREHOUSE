######

# docker run -d --name mongodb --network mynet mongo

# docker run -it --name python-mongo --network mynet python:alpine
### Il faut installer le package pymongo, mais comme on est sur l'image python:alpine,
### on doit le faire dans l'interpréteur Python. Méthode trouvée pour installer un package :
# >>> import sys
# >>> import subprocess
# >>> subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymongo'])

import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])

# Script de base, rempli par les bonnes valeurs

import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb:27017")
db = client["market"]
col = db["fruits"]
fruit = {"name": "banana", "color": "yellow"}
res = col.insert_one(fruit)
print(f"Le fruit {res.inserted_id} a bien été créé")
col.find_one()

# docker exec -it mongodb mongosh
# $> show dbs
# $> use market
# $> db.fruits.find({})
