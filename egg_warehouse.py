# docker build -t egg_warehouse .
# docker run -it --name egg_warehouse_c --network mynet egg_warehouse
# $: python3 egg_warehouse.py --eggs
# $: python3 egg_warehouse.py --check
# $: python3 egg_warehouse.py --clear
# $: python3 egg_warehouse.py --check

import sys
import argparse
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

from warehouse import Warehouse
from egg import Egg

MONGO_CLIENT = "mongodb:27017"
DB_NAME = "egg_warehouse"

client = MongoClient(MONGO_CLIENT)
db = client[DB_NAME]

WAREHOUSE_COL = "warehouse"
EGG_COL = "egg"


def get_warehouses():
    return db[WAREHOUSE_COL].find()


def get_eggs(column=None, value=None):
    if column != None and value != None:
        regex = {
            "day": "^.{8}(" + value + ").*$",
            "month": "^.{10}(" + value + ").*$",
        }
        return db[EGG_COL].find({"registration": {"$regex": regex[column]}})

    return db[EGG_COL].find()


def get_eggs_by_warehouse(id: ObjectId):
    return db[EGG_COL].find({"warehouse": id})


def get_egg_by_registration(registration: str):
    egg = db[EGG_COL].find_one({"registration": registration})
    return egg


def remove_eggs(eggs):
    db[EGG_COL].delete_many({"_id": {"$in": [e["_id"] for e in eggs]}})


def make_argparser():
    parser = argparse.ArgumentParser(description="Command Line Interface.")

    parser.add_argument(
        "--check", action="store_true", default=False, help="check warehouses validity"
    )

    parser.add_argument(
        "--warehouses", action="store_true", default=False, help="show warehouses list"
    )

    parser.add_argument(
        "--eggs", action="store_true", default=False, help="show eggs list"
    )

    parser.add_argument(
        "--registration",
        "-r",
        dest="registration",
        type=str,
        help="show egg information for a given registration",
    )

    parser.add_argument(
        "--day",
        "-d",
        dest="day",
        type=str,
        choices=[
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
        ],
        help="show eggs which have this registration day",
    )

    parser.add_argument(
        "--month",
        "-m",
        dest="month",
        type=str,
        choices=[
            "JA",
            "FE",
            "MA",
            "AV",
            "MI",
            "JU",
            "JL",
            "AO",
            "SE",
            "OC",
            "NO",
            "DE",
        ],
        help="show eggs which have this registration month",
    )

    parser.add_argument(
        "--clear", action="store_true", default=False, help="remove invalid eggs"
    )

    return parser


def main(args):
    """Main function"""
    parser = make_argparser()
    opts = parser.parse_args(args)

    if opts.check:
        eggs = get_eggs()
        if eggs == []:
            print("Aucun oeuf")
        else:
            for egg in eggs:
                e = Egg(egg["origin"], egg["color"], egg["registration"])
                if not e.is_valid():
                    print(
                        f"L'oeuf qui a pour immatriculation {e.get_registration()} n'est pas valide."
                    )
    elif opts.warehouses:
        whs = get_warehouses()
        if whs == []:
            print("Aucun warehouse.")
        else:
            for wh in whs:
                warehouse = Warehouse(wh["capacity"])
                eggs = get_eggs_by_warehouse(wh["_id"])
                if eggs == []:
                    print(f'Aucun oeuf pour le warehouse qui a pour id {wh["_id"]}')
                else:
                    for egg in eggs:
                        warehouse.add_egg(
                            Egg(egg["origin"], egg["color"], egg["registration"])
                        )
                    print(warehouse)
    elif opts.eggs:
        eggs = get_eggs()
        if eggs == []:
            print("Aucun oeuf.")
        else:
            for egg in eggs:
                print(Egg(egg["origin"], egg["color"], egg["registration"]))
    elif opts.registration:
        egg = get_egg_by_registration(opts.registration)
        if not egg:
            print("Aucun oeuf trouvé pour cette immatriculation.")
        else:
            print(Egg(egg["origin"], egg["color"], egg["registration"]))
    elif opts.day:
        eggs = get_eggs("day", opts.day)
        if eggs == []:
            print(f"Aucun oeuf qui a pour jour de ponte {opts.day}")
        else:
            for egg in eggs:
                print(Egg(egg["origin"], egg["color"], egg["registration"]))
    elif opts.month:
        eggs = get_eggs("month", opts.month)
        if eggs == []:
            print(f"Aucun oeuf qui a pour mois de ponte {opts.month}")
        else:
            for egg in eggs:
                print(Egg(egg["origin"], egg["color"], egg["registration"]))
    elif opts.clear:
        eggs_to_remove = []

        eggs = get_eggs()
        if eggs == []:
            print("Aucun oeuf")
        else:
            for egg in eggs:
                e = Egg(egg["origin"], egg["color"], egg["registration"])
                if not e.is_valid():
                    print(
                        f"L'oeuf qui a pour immatriculation {e.get_registration()} va être retiré car il n'est pas valide."
                    )
                    eggs_to_remove.append(egg)

            if eggs_to_remove == []:
                print("Aucun oeuf à retirer. Tous valides.")
            else:
                remove_eggs(eggs_to_remove)


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
