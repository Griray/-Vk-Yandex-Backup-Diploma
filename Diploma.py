import requests
import json
from pprint import pprint


TOKEN = input("Введите токен ")


# noinspection PyUnreachableCode
class User:
    def __init__(self, id):
        self.id = id

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
        return photo_json["response"]["items"]

        # Создаю список с именами фото
    def photo_name (self):
        name = []
        # Название для фото делаю сразу состоящее из лайков и даты (название разных форматов напрягает)
        for elements in self.user_photos():
            likes = (str(elements["likes"]["count"]))
            date = (str(elements["date"]))
            nick = likes+date
            name.append(nick)
        return name

    # Ссылки на фото беру последние, они самые большие, поэтому использую "-1" чтобы брать ссылку с конца
    def photo_link(self):
        link_list = []
        for reference in self.user_photos():
            link = reference["sizes"][-1]["url"]
            link_list.append(link)
        return link_list

    # Создаю словарь где keys = имя фото, values = ссылка на фото
    def dict_name_link_photo (self):
        photo_dict = dict(zip(self.photo_name(), self.photo_link()))
        return photo_dict

mikhail = User(id = 552934290)

print("Все фото пользователя", mikhail.user_photos())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Названия фотографий пользователя", mikhail.photo_name())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Ссылки на фотографии пользователя", mikhail.photo_link())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Словарь названий и ссылок на фотографии", mikhail.dict_name_link_photo())

