import requests

champion = []
datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
datas = datas.json()
for data in datas["data"]:
    champion.append(data)
print(champion)
"""
for champ in champion:
    save_path = "C:\\Users\\window10\\OneDrive\\諛뷀깢 �솕硫�\\Portfolio\\project01\\static\\img\\champion_img\\" + champ + ".png"
    image_url = "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champ + ".png"
    download_image = requests.get(image_url)
    
    with open(save_path, 'wb') as file:
        file.write(download_image.content)
"""  