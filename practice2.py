import requests
import json

response = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
champion_data = response.json()

with open('champion_data.json', 'w') as json_file:
        json.dump(champion_data, json_file)

print('Data saved successfully.')

with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
        
print(champion_data['data']['Aatrox'])