
from tqdm import tqdm
import requests
import json
class VkClient:
    url_vk = 'https://api.vk.com/method/'


    def __init__(self, token_vk, version):
        self.params = {'access_token': token_vk, 'v': version}

    def id_get(self, user_id):

        method_url = self.url_vk + 'users.get'
        params = { 'fields': 'last_seen', 'user_ids': user_id }
        res = requests.get(method_url, params={**self.params, **params})
        return res.json()['response'][0]['id']

    def get_photos(self, owner_id, count, album_id='profile',extended='1' ):
        if count == '':
            count = 5
        method_url = self.url_vk + 'photos.get'
        if type(user_id) == str:
            params = {'owner_id': self.id_get(owner_id), 'album_id': album_id, 'extended': extended, 'count': count}
        else:
            params = { 'owner_id': owner_id, 'album_id': album_id, 'extended' : extended, 'count': str(count) }
        res = requests.get(method_url, params={**self.params, **params})
        photo_dict = {}
        for photo in res.json()['response']['items']:
            photo_data = []
            photo_url = photo['sizes'][-1]['url']
            photo_likes = photo['likes']['count']
            photo_date = photo['date']
            photo_size = photo['sizes'][-1]['type']
            photo_data.append(photo_url)
            photo_data.append(photo_date)
            photo_data.append(photo_size)
            if photo_likes in photo_dict:
                photo_dict[photo_date] = photo_data
            else:
                photo_dict[photo_likes] = photo_data

        json_data = {}
        json_data['items'] = []

        for key, value in photo_dict.items():
            dict = {}
            dict['file_name'] = str(key) + '.jpg'
            dict['size'] = value[-1]
            json_data['items'].append(dict)

        with open('list.json', 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        return photo_dict

class DiskClient:

    url_disl = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token_disk):
        self.token_disk = token_disk

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token_disk)}

    def put_folder(self, folder_name):
        url = self.url_disl
        headers = self.get_headers()
        params = {'path': folder_name}
        res = requests.put(url, headers=headers, params=params)
        return res

    def post_upload(self, user_id, count):
        self.put_folder(user_id)
        url = self.url_disl + '/upload'
        headers = self.get_headers()

        for photo_likes, photo_data in tqdm(vk_client.get_photos(user_id, count).items()):

            params = {'path': str(user_id) + '/' + str(photo_likes), 'url': photo_data[0]}
            res = requests.post(url, headers=headers, params=params).json()
        print('???????????????????? ?????????????? ?????????????????? ???? ????????????.????????')



if __name__ == "__main__":

    TOKEN_VK = ''
    TOKEN_DISK = ''

    vk_client = VkClient(TOKEN_VK, '5.131')
    disk_client = DiskClient(TOKEN_DISK)

    user_id = input('?????????????? id ????????????????????????: ')
    count = input('?????????????? ???????????????????? ?????????????????????? ???????? (enter, ???????? ???????????????? ???? ??????????????????): ')


    disk_client.post_upload(user_id, count)
