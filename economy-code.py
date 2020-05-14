'''from pymongo import MongoClient

client = MongoClient("mongodb+srv://bot-dev:linusgun@horoscope-bot-efytb.mongodb.net/test?retryWrites=true&w=majority")
db = client.botuserdata
d = db.economyvalues.find_one({"name":"Anand"})
print(d)'''
import json
econ_stats =[
    {
        "user" : "Ares#7286",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0

    },
    {
        "user" : "Sir Poopy Pants#0136",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0
    }
]

with open("economy-user-data.json","w+") as data:
    json.dump(econ_stats,data)

