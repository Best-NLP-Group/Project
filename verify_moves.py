import json 

with open("moves_map/DiplomacyGame1_1910_spring.json", 'r') as f:
    data = json.load(f)
    
COUNTRIES = {
    "Austria": [],
    "England": [],
    "France": [],
    "Germany": [],
    "Italy": [],
    "Russia": [],
    "Turkey":[]
}

for place in data:
    if data[place]["controlledBy"] != "None" and data[place]["supplyCentre"]:
        COUNTRIES[data[place]["controlledBy"]].append(place)
        
for country in COUNTRIES:
    print(country, len(COUNTRIES[country]), COUNTRIES[country])
