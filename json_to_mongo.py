from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
rpg_collection = db["rpg_data"]
store_collection = db["store_data"]

with open("economy-data.json","r") as econ_data:
    econ_data_list = json.load(econ_data)
economy_collection.insert_many(econ_data_list)

with open("rpg-data.json","r") as rpg_data:
    rpg_list = json.load(rpg_data)
rpg_collection.insert_many(rpg_list)

with open("store-data.json","r") as store_data:
    store_list = json.load(store_data)
store_collection.insert_many(store_list)