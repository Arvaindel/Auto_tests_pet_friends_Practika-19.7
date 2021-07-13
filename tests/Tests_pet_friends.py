import pytest
from api import PetFrends
from settings import valid_email, valid_password, not_valid_email

pf = PetFrends()

print(pf)


def test_pet_friends_api_key_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_pet_friends_api_pets_all(filter=''):
    _,auth_key= pf.get_api_key(valid_email, valid_password)
    status, result =pf.get_api_pets(auth_key, filter)
    assert status==200
    assert len(result['pets'])>0

def test_pet_frends_post_api_pets(name='Шпрота', animal_type='Кошка', age='1', pet_photo='images/cat.jpg' ):
    _, auth_key = pf.get_api_key(email=valid_email,password=valid_password )
    status, result=pf.post_api_pets(auth_key,name, animal_type,age,pet_photo )
    assert status==200

def test_del_pet_uspex():
    '''Тест проверяет возможность удаления питомца '''
    _, auth_key = pf.get_api_key(email=valid_email, password=valid_password)
    pf.post_api_pets(auth_key, name='sel', animal_type='cat', age='1', pet_photo='images/cat.jpg')
    _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
    pet_id=pet_test['pets'][0]['id']
    status, result = pf.del_api_pet(auth_key, pet_id)
    _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
    pet_id2 = pet_test['pets'][0]['id']
    if pet_id2!='':
        assert status == 200
        assert pet_id != pet_id2
    else:
        pf.post_api_pets(auth_key, name='sel', animal_type='cat', age='1', pet_photo='images/cat.jpg')
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id3 = pet_test['pets'][0]['id']
        assert status == 200
        assert pet_id != pet_id3

def test_put_api_put_seccessful():
    '''Тест проверяет возможность обновления данных питомца'''
    _, auth_key = pf.get_api_key(email=valid_email, password=valid_password)
    _,pet_test=pf.get_api_pets(auth_key, filter='my_pets')
    print(pet_test)

    if len(pet_test['pets'])== 0:
        pf.post_api_pets(auth_key, name='Gahu', animal_type='cat', age='1', pet_photo='images/cat.jpg')
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id = pet_test['pets'][0]['id']

        status, result = pf.put_api_pet(auth_key,pet_id, name='Киска', animal_type='cat', age='1')
        assert status == 200
        assert pet_id not in pet_test.values()
    else:
        _, pet_test = pf.get_api_pets(auth_key, filter='my_pets')
        pet_id = pet_test['pets'][0]['id']

        status, result = pf.put_api_pet(auth_key, pet_id, name='Gah555', animal_type='cat', age='1')
        assert status == 200
        assert pet_id not in pet_test.values()

def test_pet_friends_api_key_valid_user(email=not_valid_email, password=valid_password):
    '''Тест проверяет невозможность авторизации с неверым Email'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_pet_frends_post_api_pets_seccessful_none_name(name='', animal_type='', age='1', pet_photo='images/cat.jpg' ):
    '''Тест проверяет возможность создание питомца без имени'''
    _, auth_key = pf.get_api_key(email=valid_email,password=valid_password )
    status, result=pf.post_api_pets(auth_key,name, animal_type,age,pet_photo )
    assert status==200
    assert result['name']==''
    print(result['name'])

def test_pet_frends_pos_api_pets_seccessful_negative_age(name='Васька', animal_type='Кот', age='-1', pet_photo='images/cat.jpg' ):
    '''Тест проверяет возможность добавления питомца с отрицательным возрастом '''
    _, auth_key = pf.get_api_key(email= valid_email, password= valid_password)
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    age=int(result['age'])
    assert status==200
    assert age<0

def test_pet_frends_pos_api_pets_seccessful_full_age(name='Васька', animal_type='Кот', age='101', pet_photo='images/cat.jpg' ):
    '''Тест проверяет возможность добавления питомца с слишком большим возрастом '''
    _, auth_key = pf.get_api_key(email= valid_email, password= valid_password)
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    age=int(result['age'])
    assert status==200
    assert age>100

def test_pet_frends_post_api_pets_seccessfull_simvolnoe_name(name='%;$,#@)(*:^&?', animal_type='Кот', age='101', pet_photo='images/cat.jpg'):
    ''' Тест проверяет возможность добавления имя с символами'''
    _, auth_key = pf.get_api_key(email=valid_email, password=valid_password)
    status, result = pf.post_api_pets(auth_key, name, animal_type,age, pet_photo)
    assert status==200
    assert result['name']!=''
    re