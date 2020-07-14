import requests
import json
from pprint import pprint


TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"

class User:
    def __init__(self, id):
        self.id = id

    @property
    def user_photos(self):
        response = requests.get(
            "https://api.vk.com/method/photos.get",
            params={
                "access_token": TOKEN,
                "v": 5.77,
                "owner_id": self.id,
                "album_id": "profile",
                "extended": 1,
                "photo_sizes": 0,
                "offset": 2
            }
        )
        photo_json = response.json()
        # Создаю 2 списка один с именами фото, другой с сылками на загрузку фото
        name = []
        link_list = []

        # Название для фото делаю сразу состоящее из лайков и даты (не хотелось названий разных форматов)
        for elements in photo_json["response"]["items"]:
            likes = (str(elements["likes"]["count"]))
            date = (str(elements["date"]))
            nick = likes+date
            name.append(nick)

        # Ссылки на фото беру последние, они самые большие, поэтому использую "-1" чтобы брать ссылку с конца
        for reference in photo_json["response"]["items"]:
            link = reference["sizes"][-1]["url"]
            link_list.append(link)

        # Создаю словарь где keys = имя фото, values = ссылка на фото
        photo_dict = dict(zip(name, link_list))
        return photo_dict

mikhail = User(id = 552934290)

print(mikhail.user_photos)

457239027, 457239029, 457239031
