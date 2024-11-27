import pytest
from unittest.mock import patch
from pages.order_page import OrderPage
import allure


# Функция для мокирования get-запросов
def mock_get_request(mock_get, mock_response, status_code=200):
    mock_get.return_value.status_code = status_code
    mock_get.return_value.json.return_value = mock_response


# Тест для получения списка заказов без указания courierId
@patch('requests.get')
@allure.feature("Orders")
@allure.story("Get orders without courierId")
def test_get_orders_without_courier_id(mock_get, mock_orders_response):
    """Получение списка заказов без указания courierId."""

    with allure.step("Mock the get request response"):
        mock_get_request(mock_get, mock_orders_response)

    with allure.step("Make the request to get orders"):
        response = OrderPage.get_orders()

    with allure.step("Verify the response status and content"):
        assert response.status_code == 200
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
        assert len(response_json["orders"]) > 0


# Тест для получения списка заказов с courierId
@allure.feature("Orders")
@allure.story("Get orders with courierId")
def test_get_orders_with_courier_id(valid_courier_payload, mock_orders_response):
    """Получение списка заказов с courierId."""

    courier_id = valid_courier_payload["id"]

    with patch('pages.order_page.requests.get') as mock_get:
        with allure.step("Mock the get request response"):
            mock_get_request(mock_get, mock_orders_response)

        with allure.step("Make the request to get orders"):
            response = OrderPage.get_orders(params={"courierId": courier_id})

        with allure.step("Verify the response status and content"):
            assert response.status_code == 200
            response_json = response.json()
            assert "orders" in response_json
            assert isinstance(response_json["orders"], list)


# Параметризованный тест для разных courier_id
@pytest.mark.parametrize("courier_id, expected_status", [
    (999999, 404),  # Несуществующий ID
    (None, 200)  # Без ID
])
@allure.feature("Orders")
@allure.story("Get orders with parameterized courierId")
def test_get_orders_with_parametrized_courier_id(mock_orders_response, valid_courier_payload, courier_id,
                                                 expected_status):
    """Параметризованный тест для получения заказов с различными courier_id."""

    with patch('pages.order_page.requests.get') as mock_get:
        with allure.step("Mock the get request response based on courier_id"):
            mock_get_request(mock_get, mock_orders_response, expected_status)

        with allure.step("Determine the courier_id and make the request"):
            if courier_id is None:
                courier_id = valid_courier_payload["id"]
            response = OrderPage.get_orders(params={"courierId": courier_id})

        with allure.step("Verify the response status"):
            assert response.status_code == expected_status


# Тест с ограничением на количество заказов
@allure.feature("Orders")
@allure.story("Get orders with limit")
def test_get_orders_with_limit():
    """Проверка получения ограниченного списка заказов с параметром limit."""

    with patch('pages.order_page.requests.get') as mock_get:
        with allure.step("Mock the get request response with orders list"):
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"orders": [{"id": i} for i in range(10)]}

        with allure.step("Make the request to get orders with limit"):
            limit = 10
            response = OrderPage.get_orders(params={"limit": limit})

        with allure.step("Verify the response status and content"):
            assert response.status_code == 200
            response_json = response.json()
            assert "orders" in response_json
            assert len(response_json["orders"]) <= limit
