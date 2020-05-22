import json
econ_stats =[
    {
        "user" : "Ares#7286",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        

    },
    {
        "user" : "Sir Poopy Pants#0136",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "Foxwid#8333",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "MANDARIN#8024",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "humanboiii#5837",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "Windsmith#4272",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "BOOOZ#4084",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "CrashGamer#7883",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "maafi_username#7152",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "prakhar5723#3126",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "smelly farts#9535",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "Sugeeth2401#3350",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    },
    {
        "user" : "shreyash0368#2025",
        "bal" : 0,
        "inv" : [
            {"stock" : 0}
        ],
        "debt" : 0,
        
    }
]

rpg_data = [
    {
        "user" : "Ares#7286",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}

    },
    {
        "user" : "Sir Poopy Pants#0136",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "Foxwid#8333",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "MANDARIN#8024",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "humanboiii#5837",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "Windsmith#4272",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "BOOOZ#4084",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}

    },
    {
        "user" : "CrashGamer#7883",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "maafi_username#7152",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "prakhar5723#3126",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "smelly farts#9535",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "Sugeeth2401#3350",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    },
    {
        "user" : "shreyash0368#2025",
        "zodiac_sign" : "",
        'hp': 100,
        'attack':10,
        'defense':10,
        'battle_options':['attack','defend','use item'],
        'battle_counters':{}
    }
]

store_data = [
    {
        "name" : "Stock",
        "price" : 25,
        "stock" : 10000
    }
]

with open("economy-data.json","w+") as data:
    json.dump(econ_stats,data)

with open("store-data.json","w+") as data:
    json.dump(store_data,data)

with open("rpg-data.json","w+") as data:
    json.dump(rpg_data,data)
