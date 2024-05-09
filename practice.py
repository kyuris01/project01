import requests

datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
datas = datas.json()
print(datas['data'].keys())
#datas['data']['Aatrox']
#datas = datas.json()