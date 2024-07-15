import requests
import json, os

response = requests.get("https://ddragon.leagueoflegends.com/cdn/14.6.1/data/en_US/champion.json")
champion_data = response.json()

with open('champion_data.json', 'w') as json_file:
        json.dump(champion_data, json_file)

with open('champion_data.json', 'r') as json_file:
        champion_data = json.load(json_file)
        
save_dir = "./static/img/champ_img"
os.makedirs(save_dir, exist_ok=True)

champion_name=[]
for data in champion_data["data"]:
        champion_name.append(data)

# 이미지 다운로드 함수
def download_champion_image(champion_name):
    base_url = "http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/"
    image_url = f"{base_url}{champion_name}.png"
    response = requests.get(image_url)

    if response.status_code == 200:
        file_path = os.path.join(save_dir, f"{champion_name}.png")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"{champion_name}.png 파일이 성공적으로 다운로드되었습니다.")
    else:
        print(f"{champion_name} 이미지를 다운로드할 수 없습니다. 상태 코드: {response.status_code}")

# 모든 챔피언 이미지 다운로드
for i in champion_name:
    download_champion_image(i)