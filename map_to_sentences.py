import os
import json
from transformers import BertTokenizer

ORDER = ["spring", "fall", "winter"]
for i in range(1, 13):
    FILES = os.listdir("moves")
    FILES = [f for f in FILES if f"Game{i}_" in f]
    FILES = sorted(FILES, key=lambda x: (int(x.split("_")[1]), ORDER.index(x.split("_")[2].split(".")[0])))
    with open(f"moves_sentences/DiplomacyGame{i}_1901_spring.json", 'w') as f:
        data = {
            'Austria': ["austria: none"],
            'Germany': ["germany: none"],
            'Italy': ["italy: none"],
            'Turkey': ["turkey: none"],
            'Russia': ["russia: none"],
            'England': ["england: none"],
            'France': ["france: none"]
        }
        json.dump(data, f, indent=4)
    for i, FILE in enumerate(FILES):
        if i == len(FILES) - 1:
            break
        with open(os.path.join("moves", FILE), 'r') as f:
            orders = json.load(f)["orders"]
        data = {"Austria": [], "Germany": [], "Italy": [], "Turkey": [], "Russia": [], "England": [], "France": []}
        for country in orders:
            for place in orders[country]:
                sentence = f"{country}: {place}: "
                for key in orders[country][place]:
                    if key == "retreat":
                        continue
                    sentence += f"{key}: {orders[country][place][key]}, "
                sentence = sentence[:-2]
                sentence = sentence.lower()
                data[country].append(sentence)
            if data[country] == []:
                data[country].append(f"{country}: None")
        with open(f"moves_sentences/{FILES[i+1]}", 'w') as f:
            json.dump(data, f, indent=4)