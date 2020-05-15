import json
horoscopes=[
    {
        "date_low" : '21-03',
        "date_high" : '19-04',
        "Zodiac" : "Aries"
    },
    {
        "date_low" : '20-04',
        "date_high" : '20-05',
        "Zodiac" : "Taurus" 
    },
    {
        "date_low" : '21-05',
        "date_high" : '20-06',
        "Zodiac" : "Gemini"
    },
    {
        "date_low" : '21-06',
        "date_high" : '22-07',
        "Zodiac" : "Cancer"
    },
    {
        "date_low" : '23-07',
        "date_high" : '22-08',
        "Zodiac" : "Leo"
    },
    {
        "date_low" : '23-08',
        "date_high" : '22-09',
        "Zodiac" : "Virgo"
    },
    {
        "date_low" : '23-09',
        "date_high" : '22-10',
        "Zodiac" : "Libra"
    },
    {
        "date_low" : '23-10',
        "date_high" : '21-11',
        "Zodiac" : "Scorpio"
    },
        
    {
        "date_low" : '22-11',
        "date_high" : '21-12',
        "Zodiac" : "Sagittarius"
    },
    {
        "date_low" : '22-12',
        "date_high" : '19-01',
        "Zodiac" : "Capricorn"
    },
    {
        "date_low" : '20-01',
        "date_high" : '18-02',
        "Zodiac" : "Aquarius"
    },
    {
        "date_low" : '19-02',
        "date_high" : '20-03',
        "Zodiac" : "Pisces"
    }
    
]

with open("horo-data.json","w+") as data:
    json.dump(horoscopes,data)
