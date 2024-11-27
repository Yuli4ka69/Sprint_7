import allure
from unittest.mock import patch
from pages.order_page import OrderPage
import pytest


# Фикстуры
@pytest.fixture
def mock_missing_order_id_response():
    return {"message": "Order ID is required"}


@pytest.fixture
def mock_not_found_order_response():
    return {"message": "Order not found"}


@pytest.mark.parametrize("order_id, expected_status, expected_message", [
    (1, 200, "id"),
    (None, 400, "Order ID is required"),
    (99999, 404, "Order not found")
])
@patch('requests.get')
@allure.feature("Order API")
@allure.story("Get order by ID")
def test_get_order(mock_get, order_id, expected_status, expected_message, mock_successful_get_order_response,
                   mock_missing_order_id_response, mock_not_found_order_response):
    """
    Тест для получения заказа по ID.
    Проверяет успешный запрос, отсутствие ID и несуществующий заказ.
    """

    # Настроим моки для различных случаев
    if order_id is None:
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_missing_order_id_response
        with allure.step("Setup: Simulate missing order ID"):
            pass
    elif order_id == 99999:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = mock_not_found_order_response
        with allure.step("Setup: Simulate order not found"):
            pass
    else:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_successful_get_order_response
        with allure.step("Setup: Simulate successful order retrieval"):
            pass

    # Выполнение запроса
    with allure.step(f"Send GET request for order ID {order_id}"):
        response = OrderPage.get_order_by_id(order_id)

    # Проверка
    with allure.step(f"Validate response status and content for order ID {order_id}"):
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        if expected_status == 200:
            assert "id" in response.json(), "Expected 'id' in response"
            assert response.json()["id"] == order_id, f"Expected order ID {order_id}, got {response.json()['id']}"
        else:
            assert "message" in response.json(), "Expected 'message' in response"
            assert response.json()[
                       "message"] == expected_message, f"Expected '{expected_message}' message, got {response.json()['message']}"
