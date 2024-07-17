import requests
import pandas as pd

datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.9.1/data/ko_KR/champion.json")
datas = datas.json()
#print(datas['data']['Aatrox']['tags'])
#datas['data']['Aatrox']
#datas = datas.json()
armor = []
for i in (datas['data']):
    #print(i, datas['data'][i]['stats']['armor'], datas['data'][i]['stats']['armorperlevel'])
    print(datas['data'][i]['blurb'])