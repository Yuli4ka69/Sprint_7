import allure
import pytest
from pages.courier_page import CourierPage
from unittest.mock import patch


def mock_delete_request(mock_delete, status_code, json_response):
    """Общий метод для настройки мока delete-запроса."""
    mock_delete.return_value.status_code = status_code
    mock_delete.return_value.json.return_value = json_response


# Параметризованный тест для разных сценариев удаления курьера
@pytest.mark.parametrize("courier_id, expected_status, expected_json", [
    ("3", 200, {"ok": True}),  # Успешное удаление курьера
    (None, 400, {"message": "Недостаточно данных для удаления курьера"}),  # Без указания ID
    ("99999", 404, {"message": "Курьер не найден"}),  # Несуществующий ID
    ("", 400, {"message": "Некорректный запрос"})  # Некорректный запрос
])
@patch('requests.delete')
@allure.feature("Courier API")
@allure.story("Delete Courier")
def test_delete_courier(mock_delete, courier_id, expected_status, expected_json):
    """Параметризованный тест для проверки удаления курьера."""

    with allure.step(f"Set up mock response for courier_id {courier_id}"):
        mock_delete_request(mock_delete, expected_status, expected_json)

    with allure.step(f"Send delete request for courier_id {courier_id}"):
        response = CourierPage.delete_courier(courier_id)

    with allure.step("Validate response status code"):
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}"

    with allure.step("Validate response JSON"):
        assert response.json() == expected_json, \
            f"Expected {expected_json}, got {response.json()}"
