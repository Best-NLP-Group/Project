import os
import json

def move_resolution(FILE, curr_map): 
    with open(FILE, 'r') as f:
        orders = json.load(f)["orders"]
    
    EMPTY = []
    FILLED = []
    
    for place in orders:
        for order in orders[place]:
            if orders[place][order]["result"] != "SUCCEEDS":
                if "retreat" not in orders[place][order]:
                    continue
                if orders[place][order]["retreat"]["result"] == "FAILS":
                    EMPTY.append(order)
                elif orders[place][order]["retreat"]["type"] == "MOVE":
                    curr_map[orders[place][order]["retreat"]["to"]]["unitType"] = curr_map[order]["unitType"]
                    curr_map[orders[place][order]["retreat"]["to"]]["currentControl"] = place
                    EMPTY.append(order)
                    FILLED.append(orders[place][order]["retreat"]["to"])
                elif orders[place][order]["retreat"]["type"] == "DISBAND":
                    EMPTY.append(order)
            elif orders[place][order]["type"] == "MOVE":
                curr_map[orders[place][order]["to"]]["unitType"] = curr_map[order]["unitType"]
                curr_map[orders[place][order]["to"]]["currentControl"] = place
                EMPTY.append(order)
                FILLED.append(orders[place][order]["to"])
            elif orders[place][order]["type"] == "BUILD":
                curr_map[order]["unitType"] = orders[place][order]["unit_type"]
                curr_map[order]["currentControl"] = place
    
    for place in EMPTY:
        if place not in FILLED:
            curr_map[place]["unitType"] = "None"
                    
    if "winter" in FILE:
        for place in curr_map:
            if curr_map[place]["unitType"] != "None":
                curr_map[place]["controlledBy"] = curr_map[place]["currentControl"]
            
    return curr_map


ORDER = ["spring", "fall", "winter"]
for i in range(1, 13):
    FILES = os.listdir("moves")
    FILES = [f for f in FILES if f"Game{i}_" in f]
    FILES = sorted(FILES, key=lambda x: (int(x.split("_")[1]), ORDER.index(x.split("_")[2].split(".")[0])))
    with open("map.json", 'r') as f:
        curr_map = json.load(f)
        with open("moves_map/" + FILES[0], 'w') as f:
            json.dump(curr_map, f, indent=4)
    for i, FILE in enumerate(FILES):
        curr_map = move_resolution(os.path.join("moves", FILE), curr_map)
        if i == len(FILES) - 1:
            break
        with open("moves_map/" + FILES[i+1], 'w') as f:
            json.dump(curr_map, f, indent=4)