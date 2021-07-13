import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFrends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email, password):
        '''Метод делает к API сервера и возвращает статус запроса
        результат в формате JSON с уникальным ключем пользователя найденного по
        указанным email и password'''
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_api_pets(self, auth_key, filter):

        headers = {
            'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_api_pets(self, auth_key, name, animal_type, age, pet_photo):
        '''Метод делает в API Post  запрос и добавляет на сайт нового питомца
               и возвращает статус код и имя питомца '''

        data = MultipartEncoder(
            {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/cat.jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def del_api_pet(self, auyh_key, pet_id):
        '''Метод далеат запрос в API запрос и удаляет  питомца '''
        headers = {
            'auth_key': auyh_key['key'],

        }
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_api_pet(self, auth_key, pet_id, name, animal_type, age):

        headers = {
            'auth_key': auth_key['key']
        }

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
