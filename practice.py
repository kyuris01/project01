import requests
import pandas as pd

datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
datas = datas.json()
print(datas['data']['Aatrox']['tags'])
#datas['data']['Aatrox']
#datas = datas.json()
armor = []
for i in (datas['data']):
    #print(i, datas['data'][i]['stats']['armor'], datas['data'][i]['stats']['armorperlevel'])
    armor.append(datas['data'][i]['stats']['armor'])
    
re = pd.cut(armor, 5)
print(re)