import requests
import json
import time
from datetime import timedelta
from tqdm import tqdm
import datetime


TOKEN = input("Введите токен ")

class User:

    def __init__(self, id):
        self.id = id


    def id_nick(self):
        response = requests.get(
            "https://api.vk.com/method/users.get",
            params={
                "access_token": TOKEN,
                "v": 5.89,
                "user_ids": self.id,
                "fields": "screen_name"
            }
        )
        id_nick_json = response.json()
        return id_nick_json["response"][0]["id"]


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
            }
        )
        photo_json = response.json()
        time.sleep(0.34)
        return photo_json["response"]["items"]


    # Создаю список с именами фото
    def photo_name(self):
        name = []
        dates = []
        for elements in self.attr:
            likes = str(elements["likes"]["count"])
            date_timestap = elements["date"]
            date = datetime.datetime.fromtimestamp(date_timestap)
            date = date.strftime("%d.%m.%Y-%H:%M:%S")
            name.append(likes)
            dates.append(date)
        lenght = len(name)
        for i in range(lenght - 1):
            for j in range(i+1, lenght):
                if name[i] == name[j]:
                    name[i] += dates[i]
                    name[j] += dates[j]
        return name

    # Ссылки на фото беру последние, они самые большие, поэтому использую "-1" чтобы брать ссылку с конца
    def photo_link(self):
        link_list = []
        for reference in self.attr:
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
        for size in self.attr:
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

# Получение ссылок для загрузки фотографий профиля
def download_links():
    links_list = []
    dictionry = username.dict_name_link_photo()
    for names, links in dictionry.items():
        link_base = "https://cloud-api.yandex.net:443/v1/disk/resources/upload?path=disk:/profile_photo/"
        link_base = link_base + names + "&url=" + links
        links_list.append(link_base)
    return links_list

# Загрузка фотографий на Яндекс диск
def load_on_disk():
    for links in download_links():
        load = requests.post(links, headers=header)
    print("Все фото успешно загружены на диск!")


if __name__ == "__main__":
    username = User(id=input("Введите VK логин или VK ID "))
    if username.id.isdigit():
        username.id = int(username.id)
    else:
        username.id = username.id_nick()
    username.attr = username.user_photos()
    oauth_token = input("Введите OAUTH token ")
    header = {"Authorization": oauth_token}
    new_folder = requests.put("https://cloud-api.yandex.net:443/v1/disk/resources?path=profile_photo", headers=header)

    with tqdm(total=100) as pbar:
        print("Данные по фотографиям пользователя", username.user_photos())
        time.sleep(0.34)
        pbar.update(12.5)
        print("Названия фотографий пользователя", username.photo_name())
        time.sleep(0.34)
        pbar.update(12.5)
        print("Ссылки на фотографии пользователя", username.photo_link())
        time.sleep(0.34)
        pbar.update(12.5)
        print("Словарь, где ключ - название фото, а значение - ссылка на фото", username.dict_name_link_photo())
        time.sleep(0.34)
        pbar.update(12.5)
        print("Тип-размер фотографий максимального размера", username.size_info())
        time.sleep(0.34)
        pbar.update(12.5)
        username.preparing_for_json()
        time.sleep(0.34)
        pbar.update(12.5)
        print("Ссылки на загрузку фотографий на Я.Диск", download_links())
        time.sleep(0.34)
        pbar.update(12.5)
        load_on_disk()
        time.sleep(0.34)
        pbar.update(12.5)

