import uuid
import allure

from config.constants import BASE_URL
from conftest import random_item_id


class TestItems():

    endpoint = f'{BASE_URL}/api/v1/items/'
    deleted_item_id = ""

    @allure.step("Create item")
    def test_create_item(self, item_data, auth_session):
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        data = response.json()
        item_id = data.get("id")
        assert item_id is not None
        assert data.get("title") == item_data["title"]
        assert data.get("description") == item_data["description"]

        #Зачем нужна это строка?
        self.created_item_id = item_id

    def test_get_items(self, auth_session):
        response = auth_session.get(self.endpoint)
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"

        data = response.json()
        assert "data" in data, "Response missing 'data' key"
        assert isinstance(data["data"], list), "'data' is not a list"
        assert isinstance(data.get("count"), int), "'count' should be integer"

    # 1 pozitive обновление данных записи
    def test_update_items(self, auth_session, item_data, random_item_id):
        response = auth_session.put(f"{self.endpoint}{random_item_id}", json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        data = response.json()
        assert data.get("title") == item_data["title"], "Название не соответствует заданному"
        assert data.get("description") == item_data["description"], "Содержание не соответствует заданному"

    # 2 pozitive удаление элемента
    def test_delete_items(self, auth_session, item_data, random_item_id):
        response = auth_session.delete(f"{self.endpoint}{random_item_id}")
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"

        data = response.json()
        item_id = data.get("id")
        assert data.get("message") == "Item deleted successfully", "В процессе удаления произошла ошибка"

        get_items = auth_session.get(f"{self.endpoint}/{random_item_id}")
        assert get_items.status_code == 404, f"Response: {response.status_code}, {response.text}"

        self.deleted_item_id = item_id

    # 3 negative пустые поля при создании
    def test_create_empty_fields(self, auth_session):
        response = auth_session.post(self.endpoint, json={"title": "", "description": ""})
        assert response.status_code == 422, f"Response: {response.status_code}, {response.text}"

    # 4 negative длинная строка
    def test_create_long_text(self, auth_session, long_item_data):
        response = auth_session.post(self.endpoint, json=long_item_data)
        assert response.status_code == 422, f"Response: {response.status_code}, {response.text}"

    # 5 negative получение без токена
    def test_get_items_no_token(self, auth_session):
        response = auth_session.get(self.endpoint, headers={"Authorization": None})
        assert response.status_code == 401, f"Response: {response.status_code}, {response.text}"

    # 6 negative получение с id без токена
    def test_get_items_id_no_token(self, auth_session, random_item_id):
        response = auth_session.get(f"{self.endpoint}{random_item_id}", headers={"Authorization": None})
        assert response.status_code == 401, f"Response: {response.status_code}, {response.text}"

    # 7 negative создание без токена
    def test_create_item_no_token(self, item_data, auth_session):
        response = auth_session.post(self.endpoint, headers={"Authorization": None}, json=item_data)
        assert response.status_code == 401, f"Response: {response.status_code}, {response.text}"

    # 8 negative обновление без токена
    def test_update_items_no_token(self, auth_session, item_data, random_item_id):
        response = auth_session.put(f"{self.endpoint}{random_item_id}", headers={"Authorization": None}, json=item_data)
        assert response.status_code == 401, f"Response: {response.status_code}, {response.text}"

    # 9 negative удаление без токена
    def test_delete_items_no_token(self, auth_session, item_data, random_item_id):
        response = auth_session.delete(f"{self.endpoint}{random_item_id}", headers={"Authorization": None})
        assert response.status_code == 401, f"Response: {response.status_code}, {response.text}"

    # 10 negative Обновление несуществующего элемента
    def test_update_none_items(self, auth_session, item_data, random_item_id):
        response = auth_session.put(f"{self.endpoint}{uuid.uuid4()}", json=item_data)
        assert response.status_code == 404, f"Response: {response.status_code}, {response.text}"

    # 10 negative Обновление несуществующего элемента
    def test_delete_none_items(self, auth_session, item_data, random_item_id):
        response = auth_session.delete(f"{self.endpoint}{uuid.uuid4()}")
        assert response.status_code == 404, f"Response: {response.status_code}, {response.text}"

    # 11 negative Удаление элемента дважды
    def test_delete_items_repeat(self, auth_session, item_data, random_item_id):
        response = auth_session.delete(f"{self.endpoint}{self.deleted_item_id}")
        assert response.status_code == 405, f"Response: {response.status_code}, {response.text}"