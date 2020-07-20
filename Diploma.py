import requests
import json
from urllib.parse import urlencode
import time

TOKEN = input("Введите токен ")

class User:
    def __init__(self, id):
        self.id = id

    # Получаю информацию по фотографиям пользователя
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
        time.sleep(3)
        return photo_json["response"]["items"]


    # Создаю список с именами фото
    def photo_name(self):
        name = []
        dates = []
        for elements in self.user_photos():
            likes = (str(elements["likes"]["count"]))
            date = (str(elements["date"]))
            name.append(likes)
            dates.append(date)
        lenght = len(name)
        for i in range(lenght - 1):
            for j in range(i+1, lenght):
                if name[i] == name[j]:
                    name[i] += dates[i]
                    name[j] += dates[j]
                    continue
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

    # Создаю список с информацией по размерам фотографий для создания json
    def size_info(self):
        size_list = []
        for size in self.user_photos():
            type = size["sizes"][-1]["type"]
            size_list.append(type)
        return size_list

    # Создаю json файл с информацией по фотографиям
    def preparing_for_json(self):
        dict_name_size = dict(zip(self.photo_name(), self.size_info()))
        list_json = []
        for names, size in dict_name_size.items():
            dict_json = {"file_name": names, "size": size}
            list_json.append(dict_json)
        with open("photo.json", "w") as file:
            json.dump(list_json, file, indent=2)
        print("Файл JSON с информацией по фотографиям успешно создан")


mikhail = User(id=int(input("Введите ID профиля ")))

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

header = {"Authorization": "OAuth AgAAAABDbZzbAADLW94rCjiptk_Muh1Ci04nKrI"}
new_folder = requests.put("https://cloud-api.yandex.net:443/v1/disk/resources?path=profile_photo", headers=header)

# Получение ссылок для загрузки фотографий профиля
def download_links():
    links_list = []
    dictionry = mikhail.dict_name_link_photo()
    for names, links in dictionry.items():
        link_base = "https://cloud-api.yandex.net:443/v1/disk/resources/upload?path="
        link_base = link_base + names + "&url=" + links
        links_list.append(link_base)
    return links_list

print("Список ссылок для загрузки фото на диск", download_links())
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")

# Загрузка фотографий на Яндекс диск
def load_on_disk():
    for links in download_links():
        load = requests.post(links, headers=header)
    print("Все фото успешно загружены на диск!")

load_on_disk()
print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
