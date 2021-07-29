import pytest
from urllib.parse import urlparse
from api import PetFrends
from settings import valid_email, valid_password, not_valid_email

pf = PetFrends()


def log(func):
    def logirovanie(get_key, *args, **kwargs):
        auth_key = get_key
        result, status, request = func(auth_key, *args, **kwargs)
        url = urlparse(request.request.url)
        file_name= 'function_log.txt'
        file=open(file_name, mode='a', encoding="utf-8")
        file.write('Запрос:\n')
        file.write(f' Метод запроса     : {request.request.method}\n')
        file.write(f' Параметры запроса : {url.query}\n')
        file.write(f' Параметры пути    : {url.path}\n')
        file.write(f' Заголовки запроса : {request.request.headers}\n')
        file.write(f' Тело запроса      : {request.request.body}\n')
        file.write('Ответ:\n')
        file.write(f' Тело ответа       : {result}\n')
        file.write(f' Статус ответа     : {status}\n')
        file.write('-------------------------------------------------------------------------------------------------\n')
        return result, status, request
    return logirovanie

@pytest.mark.api
@pytest.mark.post_pet
@log
def test_pet_frends_post_api_pets(auth_key, name='Алена', animal_type='Кошка', age='1', pet_photo='images/cat.jpg', ):

    status, result, request = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    return result, status, request










@pytest.mark.api
@pytest.mark.get_pet
def test_getAllPetsWithValidKey(get_key, filter=''):
    auth_key = get_key
    status, result = pf.get_api_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


@pytest.mark.api
@pytest.mark.delete_pet
@log
def test_del_pet_uspex(get_key):
    '''Тест проверяет возможность удаления питомца '''
    auth_key=get_key
    pf.post_api_pets(auth_key, name='sel', animal_type='cat', age='1', pet_photo='images/cat.jpg')
    _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
    pet_id = pet_test['pets'][0]['id']
    status, result, request = pf.del_api_pet(auth_key, pet_id)
    _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
    pet_id2 = pet_test['pets'][0]['id']
    if pet_id2 != '':
        assert status == 200
        assert pet_id != pet_id2
    else:
        pf.post_api_pets(auth_key, name='sel', animal_type='cat', age='1', pet_photo='images/cat.jpg')
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id3 = pet_test['pets'][0]['id']
        assert status == 200
        assert pet_id != pet_id3
    return result, status, request


@pytest.mark.api
@pytest.mark.put_pet
@log
def test_put_api_put_seccessful(get_key):
    '''Тест проверяет возможность обновления данных питомца'''
    auth_key=get_key
    _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
    print(pet_test)

    if len(pet_test['pets']) == 0:
        pf.post_api_pets(auth_key, name='Gahu', animal_type='cat', age='1', pet_photo='images/cat.jpg')
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id = pet_test['pets'][0]['id']

        status, result, request = pf.put_api_pet(auth_key, pet_id, name='Киска', animal_type='cat', age='1')
        assert status == 200
        assert pet_id not in pet_test.values()
    else:
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id = pet_test['pets'][0]['id']

        status, result, request = pf.put_api_pet(auth_key, pet_id, name='Gah555', animal_type='cat', age='1')
        assert status == 200
        assert pet_id not in pet_test.values()
    return status, result, request

@pytest.mark.api
@pytest.mark.get_auth
def test_pet_friends_api_key_valid_user(email=not_valid_email, password=valid_password):
    '''Тест проверяет невозможность авторизации с неверым Email'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


@pytest.mark.api
@pytest.mark.post_pet
@log
def test_pet_frends_post_api_pets_seccessful_none_name(get_key, name='', animal_type='', age='1', pet_photo='images/cat.jpg'):
    '''Тест проверяет возможность создание питомца без имени'''
    auth_key=get_key
    status, result,request = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''
    print(result['name'])
    return status, result,request

@pytest.mark.api
@pytest.mark.post_pet
@log
def test_pet_frends_pos_api_pets_seccessful_negative_age(get_key,name='Васька', animal_type='Кот', age='-1', pet_photo='images/cat.jpg'):
    '''Тест проверяет возможность добавления питомца с отрицательным возрастом '''
    auth_key=get_key
    status, result, request = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    age = int(result['age'])
    assert status == 200
    assert age < 0
    return status, result,request


@pytest.mark.api
@pytest.mark.post_pet
@log
def test_pet_frends_pos_api_pets_seccessful_full_age(get_key,name='Васька', animal_type='Кот', age='101',pet_photo='images/cat.jpg'):
    '''Тест проверяет возможность добавления питомца с слишком большим возрастом '''
    auth_key=get_key
    status, result, request = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    age = int(result['age'])
    assert status == 200
    assert age > 100
    return status, result,request


@pytest.mark.api
@pytest.mark.post_pet
@log
def test_pet_frends_post_api_pets_seccessfull_simvolnoe_name(get_key, name='%;$,#@)(*:^&?', animal_type='Кот', age='101', pet_photo='images/cat.jpg'):
    ''' Тест проверяет возможность добавления имя с символами'''
    auth_key=get_key
    status, result, request = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != ''
    return status, result,request
