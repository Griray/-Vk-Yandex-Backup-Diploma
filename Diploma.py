import requests
import json
from pprint import pprint

TOKEN = input("Введите токен ")

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
    def dict_name_link_photo(self):
        photo_dict = dict(zip(self.photo_name(), self.photo_link()))
        return photo_dict

    def size_info(self):
        size_list = []
        for size in self.user_photos():
            type = size["sizes"][-1]["type"]
            size_list.append(type)
        return size_list

    def preparing_for_json(self):
        dict_name_size = dict(zip(self.photo_name(), self.size_info()))
        list_json = []
        for names, size in dict_name_size.items():
            dict_json = {"file_name": names, "size": size}
            list_json.append(dict_json)
        with open("photo.json", "w") as file:
            json.dump(list_json, file, indent=2)
        print("Файл JSON с информацией по фотографиям успешно создан")


# 958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008
mikhail = User(id = 552934290)

print("Все фото пользователя", mikhail.user_photos())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Названия фотографий пользователя", mikhail.photo_name())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Ссылки на фотографии пользователя", mikhail.photo_link())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Словарь названий и ссылок на фотографии", mikhail.dict_name_link_photo())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
print("Тип размеров фотографий", mikhail.size_info())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
mikhail.preparing_for_json()
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")

