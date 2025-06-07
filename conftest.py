from config.constants import BASE_URL, DATA, API_HEADERS, AUTH_HEADERS
import requests
import pytest
import random
from faker import Faker
faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)

    auth_response = session.post(f"{BASE_URL}/api/v1/login/access-token", data=DATA, headers=AUTH_HEADERS)
    assert auth_response.status_code == 200, f"Сервер недоступен: {auth_response.status_code}, {auth_response.text}"

    token = auth_response.json().get("access_token")
    assert token is not None, f"Токен не получен"

    session.headers.update(API_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope="class")
def item_data():
    return  {
        "title": faker.word().capitalize(),
        "description": faker.paragraph()
    }

@pytest.fixture(scope="class")
def long_item_data():
    return  {
        "title": faker.paragraph(3).capitalize(),
        "description": faker.paragraph(10)
    }

@pytest.fixture(scope="function")
def random_item_id():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)

    auth_response = session.post(f"{BASE_URL}/api/v1/login/access-token", data=DATA, headers=AUTH_HEADERS)
    assert auth_response.status_code == 200, f"Сервер недоступен: {auth_response.status_code}, {auth_response.text}"

    token = auth_response.json().get("access_token")
    assert token is not None, f"Токен не получен"

    session.headers.update(API_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})

    response = session.get(f"{BASE_URL}/api/v1/items/?skip=0&limit=5", headers=API_HEADERS)
    assert response.status_code == 200, f"Сервер недоступен: {auth_response.status_code}, {auth_response.text}"

    lst_ids = response.json()["data"]
    random_item_id = random.choice(lst_ids)["id"]
    return random_item_id