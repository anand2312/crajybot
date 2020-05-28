import json
econ_stats =[
    {
        "user" : "Ares#7286",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""

    },
    {
        "user" : "Sir Poopy Pants#0136",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "Foxwid#8333",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "MANDARIN#8024",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "humanboiii#5837",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "Windsmith#4272",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "BOOOZ#4084",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "CrashGamer#7883",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "maafi_username#7152",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "prakhar5723#3126",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "smelly farts#9535",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "Sugeeth2401#3350",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "shreyash0368#2025",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "Jackson Williams#4755",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    },
    {
        "user" : "kaanank90#4243",
        "cash" : 0,
        "bank" : 2500,
        "inv" : [
            {"stock" : 0},
            {"chicken" : 0},
            {"heist tools" : 0}
        ],
        "debt" : 0,
        "zodiac_sign" : ""
    }
]

store_data = [
    {
        "name" : "Stock",
        "price" : 25,
        "stock" :10000
    },
    {
        "name" : "Chicken",
        "price" : 100,
        "stock" : None
    },
    {
        "name" : "Heist tools",
        "price" : 250,
        "stock" : None
    }
]

with open("economy-data.json","w+") as data:
    json.dump(econ_stats,data)

with open("store-data.json","w+") as store:
    json.dump(store_data,store)