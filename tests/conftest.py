from settings import valid_email, valid_password, not_valid_email
from api import PetFrends
import pytest

@pytest.fixture(autouse=True)
def get_key(email=valid_email, password=valid_password):
    pf = PetFrends()
    status, auth_key = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in auth_key
    return auth_key
