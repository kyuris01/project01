import requests

champion = []
datas = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
datas = datas.json()
print(datas["data"]["Aatrox"]["tags"])
"""
for champ in champion:
    save_path = "C:\\Users\\window10\\OneDrive\\바탕 화면\\Portfolio\\project01\\static\\img\\champion_img\\" + champ + ".png"
    image_url = "http://ddragon.leagueoflegends.com/cdn/12.7.1/img/champion/" + champ + ".png"
    download_image = requests.get(image_url)
    
    with open(save_path, 'wb') as file:
        file.write(download_image.content)
"""  